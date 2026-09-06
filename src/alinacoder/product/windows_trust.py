from __future__ import annotations

import ctypes
import hashlib
import os
import shutil
import subprocess
import urllib.error
import urllib.request
import zipfile
from ctypes import wintypes
from pathlib import Path
from urllib.parse import urlparse

from . import prerequisites as _prerequisites_module
from .prerequisites import (
    BootstrapError,
    ComponentReceipt,
    ProvenanceError,
    ReleaseAsset,
    WindowsBootstrapAdapter as _PowerShellWindowsBootstrapAdapter,
    version_at_least,
)
from .setup_events import CancellationToken, SetupEvent, SetupEventSink


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
    """Fail-closed Authenticode verification through Windows WinVerifyTrust."""

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
    def _managed_git_root() -> Path:
        local = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
        return local / "Programs" / "AlinaCoder" / "Git"

    def _candidate_executables(self, name: str) -> tuple[Path, ...]:
        candidates = list(super()._candidate_executables(name))
        if name == "git":
            managed = self._managed_git_root() / "cmd" / "git.exe"
            candidates = [managed] + [candidate for candidate in candidates if candidate != managed]
        return tuple(candidates)

    @staticmethod
    def _is_silent_installer(args: list[str]) -> bool:
        if not args or Path(args[0]).suffix.lower() != ".exe":
            return False
        switches = {str(item).upper() for item in args[1:]}
        return bool(switches.intersection({"/VERYSILENT", "/SILENT"}))

    def _default_command_runner(self, args: list[str], *, timeout: int = 300) -> tuple[int, str]:
        if not self._is_silent_installer(args):
            completed = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            return int(completed.returncode), completed.stdout or ""

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

    @staticmethod
    def _safe_extract_zip(archive_path: Path, destination: Path) -> None:
        root = destination.resolve()
        destination.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(archive_path) as archive:
                for member in archive.infolist():
                    raw_name = member.filename.replace("\\", "/")
                    candidate = Path(raw_name)
                    if candidate.is_absolute() or ".." in candidate.parts:
                        raise BootstrapError("MinGit archive contains an unsafe path")
                    target = (destination / candidate).resolve()
                    if target != root and root not in target.parents:
                        raise BootstrapError("MinGit archive escapes managed destination")
                    if member.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(member) as source, target.open("wb") as handle:
                        shutil.copyfileobj(source, handle)
        except (OSError, zipfile.BadZipFile) as exc:
            raise BootstrapError("verified MinGit archive could not be extracted") from exc

    def _install_mingit(self, *, operation: str) -> ComponentReceipt:
        policy = self._policy("git")
        asset = self.latest_asset("git")
        if not asset.name.lower().startswith("mingit-") or not asset.name.lower().endswith(".zip"):
            raise BootstrapError("Git bootstrap requires the official MinGit ZIP asset")
        if not version_at_least(asset.version, policy.minimum_version):
            raise BootstrapError("latest MinGit release is below required minimum")

        previous = self.detect_inventory().git
        archive = self.download_verified(asset, require_authenticode=False)
        root = self._managed_git_root()
        staging = root.with_name("Git.alinacoder-staging")
        backup = root.with_name("Git.alinacoder-backup")
        shutil.rmtree(staging, ignore_errors=True)
        self._safe_extract_zip(archive, staging)
        staged_git = staging / "cmd" / "git.exe"
        if not staged_git.is_file():
            shutil.rmtree(staging, ignore_errors=True)
            raise BootstrapError("verified MinGit archive is missing cmd/git.exe")
        code, output = self._run([str(staged_git), "--version"], timeout=30)
        if code != 0 or not version_at_least(output, policy.minimum_version):
            shutil.rmtree(staging, ignore_errors=True)
            raise BootstrapError("extracted MinGit failed version verification")

        shutil.rmtree(backup, ignore_errors=True)
        if root.exists():
            root.replace(backup)
        try:
            root.parent.mkdir(parents=True, exist_ok=True)
            staging.replace(root)
            managed_git = root / "cmd" / "git.exe"
            code, output = self._run([str(managed_git), "--version"], timeout=30)
            if code != 0 or not version_at_least(output, policy.minimum_version):
                raise BootstrapError("managed MinGit failed post-install verification")
        except Exception:
            shutil.rmtree(root, ignore_errors=True)
            if backup.exists():
                backup.replace(root)
            raise
        shutil.rmtree(backup, ignore_errors=True)

        receipt = ComponentReceipt(
            name="git",
            version=asset.version,
            origin="managed_by_alinacoder",
            source_url=asset.url,
            sha256=asset.sha256,
            healthy=True,
            path=str(root / "cmd" / "git.exe"),
            previous_version=previous.version if previous else "",
        )
        self._last_install_receipts["git"] = receipt
        return receipt

    def install_component(self, component: str, *, operation: str) -> ComponentReceipt:
        if component == "git":
            return self._install_mingit(operation=operation)

        receipt = super().install_component(component, operation=operation)
        policy = self._policy(component)
        for attempt in range(180):
            inventory = self.detect_inventory()
            installed = inventory.ollama
            if installed is not None and version_at_least(installed.version, policy.minimum_version):
                return receipt
            self._sleep(min(0.5 + (attempt * 0.05), 2.0))
        raise BootstrapError(f"{component} {operation} launcher exited but verified installation was not observed")

    def managed_uninstall(self, *, purge: bool = False) -> tuple[str, ...]:
        removed = list(super().managed_uninstall(purge=purge))
        if not purge:
            return tuple(removed)
        state = self.load_state()
        receipt = state.components.get("git") if state else None
        root = self._managed_git_root()
        if receipt and receipt.origin == "managed_by_alinacoder" and root.exists():
            try:
                receipt_path = Path(receipt.path).resolve() if receipt.path else None
                root_resolved = root.resolve()
                if receipt_path is not None and receipt_path != root_resolved and root_resolved not in receipt_path.parents:
                    raise BootstrapError("refusing to purge Git outside AlinaCoder managed root")
                shutil.rmtree(root)
                removed.append("git")
            except OSError as exc:
                raise BootstrapError("managed MinGit purge failed") from exc
        return tuple(dict.fromkeys(removed))

    def pull_model(self, endpoint: str, model: str) -> bool:
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

    def smoke_model(self, endpoint: str, model: str) -> str:
        try:
            payload = _prerequisites_module._json_bytes(
                endpoint.rstrip("/") + "/api/generate",
                {
                    "model": model,
                    "prompt": "Reply only with OK.",
                    "think": False,
                    "stream": False,
                    "options": {"num_predict": 16},
                },
            )
            return str(payload.get("response", "")).strip()
        except (OSError, ValueError, urllib.error.URLError, TimeoutError):
            return ""


class ObservableWindowsBootstrapAdapter(NativeWindowsBootstrapAdapter):
    """Native trusted bootstrap plus user-visible progress and cancellation."""

    def __init__(
        self,
        *args,
        event_sink: SetupEventSink | None = None,
        cancellation_token: CancellationToken | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._event_sink = event_sink
        self._cancellation_token = cancellation_token or CancellationToken()

    @property
    def cancellation_token(self) -> CancellationToken:
        return self._cancellation_token

    def _check_cancelled(self) -> None:
        self._cancellation_token.raise_if_cancelled()

    def _emit(
        self,
        phase: str,
        kind: str,
        message: str,
        detail: str = "",
        *,
        current: int | None = None,
        total: int | None = None,
    ) -> None:
        if self._event_sink is not None:
            self._event_sink(SetupEvent(phase, kind, message, detail, current, total))

    def detect_machine(self):
        self._check_cancelled()
        self._emit("analyse", "start", "Analyse du PC")
        machine = super().detect_machine()
        self._emit(
            "analyse",
            "complete",
            "Configuration détectée",
            f"Windows {machine.windows_major}; {machine.architecture}; RAM {machine.ram_gb:.1f} Go; "
            f"GPU {machine.gpu_vendor}; VRAM {machine.vram_gb:.1f} Go; disque {machine.disk_free_gb:.1f} Go",
        )
        return machine

    def download_verified(self, asset: ReleaseAsset, *, require_authenticode: bool = True) -> Path:
        self._check_cancelled()
        target = self.cache_dir / asset.name
        temporary = target.with_suffix(target.suffix + ".partial")
        temporary.unlink(missing_ok=True)
        digest = hashlib.sha256()
        self._emit("download", "start", f"Téléchargement de {asset.component}", asset.name, current=0)

        if self._download_bytes is not None:
            data = self._download_bytes(asset.url)
            self._check_cancelled()
            digest.update(data)
            temporary.write_bytes(data)
            self._emit("download", "progress", f"Téléchargement de {asset.component}", asset.name, current=len(data), total=len(data))
        else:
            parsed = urlparse(asset.url)
            if parsed.scheme != "https" or parsed.hostname != "github.com":
                raise ProvenanceError("downloads are restricted to HTTPS GitHub release assets")
            request = urllib.request.Request(asset.url, headers={"User-Agent": "AlinaCoder/0.2"})
            with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as handle:
                length = response.headers.get("Content-Length")
                total = int(length) if length and length.isdigit() else None
                current = 0
                while True:
                    self._check_cancelled()
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    handle.write(chunk)
                    current += len(chunk)
                    self._emit("download", "progress", f"Téléchargement de {asset.component}", asset.name, current=current, total=total)

        actual = digest.hexdigest()
        if actual.lower() != asset.sha256.lower():
            temporary.unlink(missing_ok=True)
            self._emit("download", "error", f"Vérification SHA-256 échouée pour {asset.component}", asset.name)
            raise ProvenanceError(f"SHA-256 mismatch for {asset.name}")
        if require_authenticode and asset.name.lower().endswith(".exe") and os.name == "nt":
            self._emit("download", "info", f"Vérification de la signature {asset.component}", asset.name)
            if not self.verify_authenticode(temporary):
                temporary.unlink(missing_ok=True)
                self._emit("download", "error", f"Signature Authenticode invalide pour {asset.component}", asset.name)
                raise ProvenanceError(f"Authenticode validation failed for {asset.name}")
        temporary.replace(target)
        self._emit("download", "complete", f"Téléchargement vérifié : {asset.component}", asset.name)
        return target

    def install_component(self, component: str, *, operation: str) -> ComponentReceipt:
        self._check_cancelled()
        phase = "git" if component == "git" else "ollama"
        self._emit(phase, "start", f"{operation.capitalize()} de {component}")
        try:
            receipt = super().install_component(component, operation=operation)
        except Exception as exc:
            self._emit(phase, "error", f"Échec de {component}", str(exc))
            raise
        self._emit(phase, "complete", f"{component} prêt", f"version {receipt.version}")
        return receipt

    def wait_ollama(self, endpoint: str, *, attempts: int = 30) -> bool:
        self._check_cancelled()
        self._emit("ollama", "info", "Démarrage et vérification d'Ollama", endpoint)
        result = super().wait_ollama(endpoint, attempts=attempts)
        self._emit("ollama", "complete" if result else "error", "Ollama répond" if result else "Ollama ne répond pas", endpoint)
        return result

    def pull_model(self, endpoint: str, model: str) -> bool:
        self._check_cancelled()
        executable = self._ollama_executable()
        if executable is None:
            self._emit("model", "error", "Ollama introuvable pour télécharger le modèle", model)
            return False

        self._emit("model", "start", f"Téléchargement du modèle {model}", "Ollama reprend automatiquement un téléchargement interrompu")
        for attempt in range(3):
            self._check_cancelled()
            self._emit("model", "info", f"Téléchargement du modèle — tentative {attempt + 1}/3", model)
            try:
                code, output = self._run([str(executable), "pull", model], timeout=600)
            except subprocess.TimeoutExpired:
                code, output = -1, "timeout after 600 seconds"
            if output.strip():
                self._emit("model", "detail", "Sortie Ollama", output[-2000:])
            if code == 0:
                inventory = self.detect_inventory()
                if model in inventory.models:
                    self._emit("model", "complete", f"Modèle {model} prêt")
                    return True
            if attempt < 2:
                self._emit("model", "retry", "Nouvelle tentative du téléchargement du modèle", f"code={code}")
                self._sleep(float(2**attempt))
        self._emit("model", "error", f"Impossible de télécharger le modèle {model}")
        return False

    def smoke_model(self, endpoint: str, model: str) -> str:
        self._check_cancelled()
        self._emit("validation", "start", "Test réel de l'IA locale", model)
        response = super().smoke_model(endpoint, model)
        if response.strip():
            self._emit("validation", "complete", "IA locale validée", response[:200])
        else:
            self._emit("validation", "error", "Le test d'inférence locale a échoué", model)
        return response
