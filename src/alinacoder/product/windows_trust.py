from __future__ import annotations

import ctypes
import os
from ctypes import wintypes
from pathlib import Path

from .prerequisites import WindowsBootstrapAdapter as _PowerShellWindowsBootstrapAdapter


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
    """Production Windows adapter using native trust verification."""

    def verify_authenticode(self, path: Path | str) -> bool:
        return verify_windows_authenticode(path)
