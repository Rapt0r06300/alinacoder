from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from . import windows_trust as _windows_trust
from .prerequisites import ProvenanceError


def _official_silent_installer_args(args: list[str]) -> list[str]:
    """Match Ollama's official fully-silent Windows installer invocation."""

    if not args or Path(args[0]).name.casefold() != "ollamasetup.exe":
        return args
    switches = {str(item).casefold() for item in args[1:]}
    if "/verysilent" not in switches or "/suppressmsgboxes" in switches:
        return args
    return [*args, "/SUPPRESSMSGBOXES"]


def _safe_release_asset_name(name: str) -> str:
    candidate = str(name)
    if (
        not candidate
        or candidate in {".", ".."}
        or "/" in candidate
        or "\\" in candidate
        or Path(candidate).name != candidate
    ):
        raise ProvenanceError("unsafe release asset name")
    return candidate


def _bind_verified_prefetch_cache(adapter: type[Any]) -> None:
    """Allow an explicit CI prefetch directory without weakening verification."""

    if getattr(adapter, "_alinacoder_prefetch_cache_guard", False):
        return

    original_download = adapter.download_verified

    def hardened_download_verified(
        self: Any,
        asset: Any,
        *,
        require_authenticode: bool = True,
    ) -> Path:
        name = _safe_release_asset_name(str(asset.name))
        prefetch_root = os.environ.get("ALINACODER_PREREQ_CACHE_DIR", "").strip()
        if not prefetch_root:
            return original_download(self, asset, require_authenticode=require_authenticode)

        candidate = Path(prefetch_root) / name
        if not candidate.is_file():
            return original_download(self, asset, require_authenticode=require_authenticode)

        target = self.cache_dir / name
        temporary = target.with_suffix(target.suffix + ".partial")
        temporary.unlink(missing_ok=True)
        digest = hashlib.sha256()
        try:
            with candidate.open("rb") as source, temporary.open("wb") as destination:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    destination.write(chunk)

            actual = digest.hexdigest()
            if actual.lower() != str(asset.sha256).lower():
                raise ProvenanceError(f"SHA-256 mismatch for {name}")
            if require_authenticode and name.lower().endswith(".exe") and os.name == "nt":
                if not self.verify_authenticode(temporary):
                    raise ProvenanceError(f"Authenticode validation failed for {name}")
            temporary.replace(target)
            return target
        except Exception:
            temporary.unlink(missing_ok=True)
            raise

    hardened_download_verified.__name__ = original_download.__name__
    hardened_download_verified.__qualname__ = f"{adapter.__name__}.download_verified"
    hardened_download_verified.__module__ = adapter.__module__
    adapter.download_verified = hardened_download_verified  # type: ignore[method-assign]
    adapter._alinacoder_prefetch_cache_guard = True  # type: ignore[attr-defined]


def harden_windows_bootstrap() -> None:
    """Harden Windows adapters in place while preserving their canonical identities."""

    adapter = _windows_trust.NativeWindowsBootstrapAdapter
    if not getattr(adapter, "_alinacoder_official_silent_guard", False):
        original_run = adapter._run

        def hardened_run(self: Any, args: list[str], *, timeout: int = 300) -> tuple[int, str]:
            return original_run(self, _official_silent_installer_args(list(args)), timeout=timeout)

        hardened_run.__name__ = original_run.__name__
        hardened_run.__qualname__ = f"{adapter.__name__}._run"
        hardened_run.__module__ = adapter.__module__
        adapter._run = hardened_run  # type: ignore[method-assign]
        adapter._alinacoder_official_silent_guard = True  # type: ignore[attr-defined]

    _bind_verified_prefetch_cache(adapter)
    _bind_verified_prefetch_cache(_windows_trust.ObservableWindowsBootstrapAdapter)


__all__ = [
    "harden_windows_bootstrap",
    "_official_silent_installer_args",
    "_safe_release_asset_name",
]
