from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from . import prerequisites as _prerequisites
from . import windows_trust as _windows_trust
from .prerequisites import BootstrapReport, ProvenanceError
from .windows_fs import replace_with_retry, rmtree_with_retry, unlink_with_retry


def _bind_atomic_state_write() -> None:
    adapter = _prerequisites.WindowsBootstrapAdapter
    if getattr(adapter, "_alinacoder_resilient_atomic_write_guard", False):
        return

    def resilient_atomic_write_json(self: Any, path: Path, payload: dict[str, Any]) -> None:
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        replace_with_retry(temporary, path, sleep=self._sleep)

    adapter._atomic_write_json = resilient_atomic_write_json  # type: ignore[method-assign]
    adapter._alinacoder_resilient_atomic_write_guard = True  # type: ignore[attr-defined]


def _promote_verified_partial(
    self: Any,
    asset: Any,
    temporary: Path,
    target: Path,
    *,
    require_authenticode: bool,
) -> Path:
    digest = hashlib.sha256()
    with temporary.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest().lower() != str(asset.sha256).lower():
        unlink_with_retry(temporary, sleep=self._sleep)
        raise ProvenanceError(f"SHA-256 mismatch for {asset.name}")
    if require_authenticode and str(asset.name).lower().endswith(".exe") and os.name == "nt":
        if not self.verify_authenticode(temporary):
            unlink_with_retry(temporary, sleep=self._sleep)
            raise ProvenanceError(f"Authenticode validation failed for {asset.name}")
    replace_with_retry(temporary, target, sleep=self._sleep)
    return target


def _bind_verified_download(adapter: type[Any]) -> None:
    # Guard per concrete class. getattr() would inherit the Native marker and could
    # incorrectly skip the Observable GUI adapter, leaving its own override unhardened.
    if adapter.__dict__.get("_alinacoder_resilient_download_guard", False):
        return
    original_download = adapter.download_verified

    def resilient_download_verified(
        self: Any,
        asset: Any,
        *,
        require_authenticode: bool = True,
    ) -> Path:
        target = self.cache_dir / str(asset.name)
        temporary = target.with_suffix(target.suffix + ".partial")
        unlink_with_retry(temporary, sleep=self._sleep)
        try:
            return original_download(self, asset, require_authenticode=require_authenticode)
        except PermissionError:
            # Recovery is allowed only after the full verified payload exists. Any
            # other access-denied remains fail-closed instead of being guessed away.
            if not temporary.is_file():
                raise
            recovered = _promote_verified_partial(
                self,
                asset,
                temporary,
                target,
                require_authenticode=require_authenticode,
            )
            emit = getattr(self, "_emit", None)
            if callable(emit):
                emit("download", "complete", f"Téléchargement vérifié : {asset.component}", str(asset.name))
            return recovered

    resilient_download_verified.__name__ = original_download.__name__
    resilient_download_verified.__qualname__ = f"{adapter.__name__}.download_verified"
    resilient_download_verified.__module__ = adapter.__module__
    adapter.download_verified = resilient_download_verified  # type: ignore[method-assign]
    adapter._alinacoder_resilient_download_guard = True  # type: ignore[attr-defined]


def _bind_mingit_staging_cleanup() -> None:
    adapter = _windows_trust.NativeWindowsBootstrapAdapter
    if getattr(adapter, "_alinacoder_resilient_mingit_cleanup_guard", False):
        return
    original_install_mingit = adapter._install_mingit

    def resilient_install_mingit(self: Any, *, operation: str):
        root = self._managed_git_root()
        staging = root.with_name("Git.alinacoder-staging")
        backup = root.with_name("Git.alinacoder-backup")
        # The historical implementation used ignore_errors=True. That can leave a
        # stale tree behind when Defender/indexers hold a transient handle. Ensure
        # those known scratch locations are actually gone before extraction starts.
        rmtree_with_retry(staging, sleep=self._sleep)
        rmtree_with_retry(backup, sleep=self._sleep)
        receipt = original_install_mingit(self, operation=operation)
        # Successful promotion must not leave stale transaction directories behind.
        rmtree_with_retry(staging, sleep=self._sleep)
        rmtree_with_retry(backup, sleep=self._sleep)
        return receipt

    resilient_install_mingit.__name__ = original_install_mingit.__name__
    resilient_install_mingit.__qualname__ = f"{adapter.__name__}._install_mingit"
    resilient_install_mingit.__module__ = adapter.__module__
    adapter._install_mingit = resilient_install_mingit  # type: ignore[method-assign]
    adapter._alinacoder_resilient_mingit_cleanup_guard = True  # type: ignore[attr-defined]


def _bind_install_metadata() -> None:
    # Import after the package has rebound WindowsBootstrapAdapter to the native
    # implementation. installer.py has no import-time side effects beyond definitions.
    from . import installer as _installer

    if getattr(_installer, "_alinacoder_resilient_metadata_guard", False):
        return

    def resilient_write_metadata(
        install_dir: Path,
        *,
        operation: str,
        report: BootstrapReport | None = None,
        deferred: bool = False,
    ) -> None:
        install_dir = Path(install_dir)
        install_dir.mkdir(parents=True, exist_ok=True)
        temporary = install_dir / "install.json.tmp"
        temporary.write_text(
            json.dumps(
                _installer._metadata_payload(operation=operation, report=report, deferred=deferred),
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        replace_with_retry(temporary, install_dir / "install.json")

    _installer._write_metadata = resilient_write_metadata
    _installer._alinacoder_resilient_metadata_guard = True


def harden_windows_filesystem() -> None:
    """Bind bounded, fail-closed recovery at critical Windows filesystem seams."""

    _bind_atomic_state_write()
    _bind_mingit_staging_cleanup()
    _bind_verified_download(_windows_trust.NativeWindowsBootstrapAdapter)
    _bind_verified_download(_windows_trust.ObservableWindowsBootstrapAdapter)
    _bind_install_metadata()


__all__ = ["harden_windows_filesystem"]
