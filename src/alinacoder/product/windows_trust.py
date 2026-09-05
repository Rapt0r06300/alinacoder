from __future__ import annotations

import ctypes
import os
import subprocess
from ctypes import wintypes
from pathlib import Path

from .prerequisites import (
    BootstrapError,
    ComponentReceipt,
    WindowsBootstrapAdapter as _PowerShellWindowsBootstrapAdapter,
    version_at_least,
)


class _GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8),
    ]


class _WINTRUST_FILE_INFO(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("pcwszFilePath", wintypes.LPCWSTR),
        ("hFile", wintypes.HANDLE),
        ("pgKnownSubject", wintypes.LPVOID),
    ]


class _WINTRUST_DATA(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("pPolicyCallbackData", wintypes.LPVOID),
        ("pSIPClientData", wintypes.LPVOID),
        ("dwUIChoice", wintypes.DWORD),
        ("fdwRevocationChecks", wintypes.DWORD),
        ("dwUnionChoice", wintypes.DWORD),
        ("pFile", ctypes.POINTER(_WINTRUST_FILE_INFO)),
        ("dwStateAction", wintypes.DWORD),
        ("hWVTStateData", wintypes.HANDLE),
        ("pwszURLReference", wintypes.LPCWSTR),
        ("dwProvFlags", wintypes.DWORD),
        ("dwUIContext", wintypes.DWORD),
        ("pSignatureSettings", wintypes.LPVOID),
    ]


_WINTRUST_ACTION_GENERIC_VERIFY_V2 = _GUID(
    0x00AAC56B,
    0xCD44,
    0x11D0,
    (ctypes.c_ubyte * 8)(0x8C, 0xC2, 0x00, 0xC0, 0x4F, 0xC2, 0x95, 0xEE),
)

_WTD_UI_NONE = 2
_WTD_REVOKE_NONE = 0
_WTD_CHOICE_FILE = 1
_WTD_STATEACTION_IGNORE = 0


def verify_windows_authenticode(path: Path | str) -> bool:
    """Fail-closed Authenticode verification through Windows WinVerifyTrust.

    The bootstrap already pins the exact SHA-256 advertised by the allow-listed
    GitHub release. WinVerifyTrust supplies the independent OS signature/trust
    decision without spawning PowerShell or depending on module autoload state.
    """

    candidate = Path(path)
    if os.name != "nt" or not candidate.is_file():
        return False

    file_info = _WINTRUST_FILE_INFO()
    file_info.cbStruct = ctypes.sizeof(_WINTRUST_FILE_INFO)
    file_info.pcwszFilePath = str(candidate.resolve())
    file_info.hFile = None
    file_info.pgKnownSubject = None

    trust_data = _WINTRUST_DATA()
    trust_data.cbStruct = ctypes.sizeof(_WINTRUST_DATA)
    trust_data.pPolicyCallbackData = None
    trust_data.pSIPClientData = None
    trust_data.dwUIChoice = _WTD_UI_NONE
    trust_data.fdwRevocationChecks = _WTD_REVOKE_NONE
    trust_data.dwUnionChoice = _WTD_CHOICE_FILE
    trust_data.pFile = ctypes.pointer(file_info)
    trust_data.dwStateAction = _WTD_STATEACTION_IGNORE
    trust_data.hWVTStateData = None
    trust_data.pwszURLReference = None
    trust_data.dwProvFlags = 0
    trust_data.dwUIContext = 0
    trust_data.pSignatureSettings = None

    try:
        win_verify_trust = ctypes.windll.wintrust.WinVerifyTrust
        win_verify_trust.argtypes = [wintypes.HWND, ctypes.POINTER(_GUID), wintypes.LPVOID]
        win_verify_trust.restype = ctypes.c_long
        status = win_verify_trust(
            wintypes.HWND(-1),
            ctypes.byref(_WINTRUST_ACTION_GENERIC_VERIFY_V2),
            ctypes.byref(trust_data),
        )
    except (AttributeError, OSError, ValueError, ctypes.ArgumentError):
        return False
    return status == 0


class NativeWindowsBootstrapAdapter(_PowerShellWindowsBootstrapAdapter):
    """Production Windows adapter using native trust and bounded process execution."""

    def verify_authenticode(self, path: Path | str) -> bool:
        return verify_windows_authenticode(path)

    @staticmethod
    def _is_silent_installer(args: list[str]) -> bool:
        if not args or Path(args[0]).suffix.lower() != ".exe":
            return False
        switches = {str(item).upper() for item in args[1:]}
        return bool(switches.intersection({"/VERYSILENT", "/SILENT"}))

    def _default_command_runner(self, args: list[str], *, timeout: int = 300) -> tuple[int, str]:
        """Run official GUI installers without inheritable output pipes.

        Inno Setup launchers can hand work to a temporary child process. Captured
        stdout/stderr handles may remain inherited by that child after the launcher
        exits, causing ``subprocess.run(..., PIPE)`` to wait for EOF indefinitely.
        GUI installers have no machine-consumed stdout contract, so route all three
        standard handles to DEVNULL and rely on exit code plus post-install inventory.
        Other commands retain the base captured-output behavior.
        """

        if not self._is_silent_installer(args):
            return super()._default_command_runner(args, timeout=timeout)

        process = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass
            raise
        return int(code), ""

    def install_component(self, component: str, *, operation: str) -> ComponentReceipt:
        receipt = super().install_component(component, operation=operation)
        policy = self._policy(component)

        # A verified GUI bootstrapper may return after handing work to its temporary
        # child. Do not declare the dependency installed until inventory observes the
        # expected minimum version. This also makes completion deterministic on CI.
        for attempt in range(180):
            inventory = self.detect_inventory()
            installed = inventory.git if component == "git" else inventory.ollama
            if installed is not None and version_at_least(installed.version, policy.minimum_version):
                return receipt
            self._sleep(min(0.5 + (attempt * 0.05), 2.0))
        raise BootstrapError(f"{component} {operation} launcher exited but verified installation was not observed")

    def pull_model(self, endpoint: str, model: str) -> bool:
        """Pull a model with bounded retries while preserving Ollama's native resume."""

        executable = self._ollama_executable()
        if executable is None:
            return False

        for attempt in range(3):
            try:
                code, _ = self._run([str(executable), "pull", model], timeout=600)
            except subprocess.TimeoutExpired:
                code = -1

            if code == 0:
                inventory = self.detect_inventory()
                if model in inventory.models:
                    return True

            if attempt < 2:
                self._sleep(float(2**attempt))

        return False
