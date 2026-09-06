from __future__ import annotations

import hashlib
import os
import subprocess
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from .prerequisites import BootstrapError, ProvenanceError, ReleaseAsset
from .setup_events import CancellationToken, SetupEvent, SetupEventSink
from .windows_trust import NativeWindowsBootstrapAdapter


class ObservableWindowsBootstrapAdapter(NativeWindowsBootstrapAdapter):
    """Native Windows bootstrap adapter with user-visible progress events.

    The event layer is observational only: it never changes trust, digest, ownership
    or readiness decisions made by the existing LOT19 bootstrap implementation.
    """

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
            self._emit(
                "download",
                "progress",
                f"Téléchargement de {asset.component}",
                asset.name,
                current=len(data),
                total=len(data),
            )
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
                    self._emit(
                        "download",
                        "progress",
                        f"Téléchargement de {asset.component}",
                        asset.name,
                        current=current,
                        total=total,
                    )

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

    def install_component(self, component: str, *, operation: str):
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
