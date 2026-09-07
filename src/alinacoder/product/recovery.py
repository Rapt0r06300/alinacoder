from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import errno
import json
from pathlib import Path
import urllib.error
from typing import Any, Callable

from .prerequisites import BootstrapError, ProvenanceError
from .setup_events import SetupCancelled, redact_setup_text
from .windows_fs import replace_with_retry, unlink_with_retry


_TRANSIENT_WINERRORS = {5, 32, 33, 121}
_TRANSIENT_ERRNOS = {errno.EACCES, errno.EPERM, errno.EBUSY, errno.ETIMEDOUT}
_FATAL_BOOTSTRAP_MARKERS = (
    "windows 10+ is required",
    "windows 11+ is required",
    "requested model does not fit hardware",
    "unknown model profile",
    "no local model profile fits",
    "below required minimum",
)
_FATAL_PROVENANCE_MARKERS = (
    "authenticode",
    "allow-list",
    "allow-listed",
    "outside the allow-listed repository",
    "release repository does not match",
    "missing a sha-256 digest",
    "release asset url is outside",
)


@dataclass(frozen=True)
class RecoveryPolicy:
    max_attempts: int = 4
    base_delay_seconds: float = 0.5
    max_delay_seconds: float = 4.0

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.base_delay_seconds < 0:
            raise ValueError("base_delay_seconds must be non-negative")
        if self.max_delay_seconds < self.base_delay_seconds:
            raise ValueError("max_delay_seconds must be >= base_delay_seconds")


@dataclass(frozen=True)
class RecoveryDecision:
    category: str
    recoverable: bool
    remediations: tuple[str, ...] = ()


def _message(exc: BaseException) -> str:
    return str(exc).strip().lower()


def classify_failure(exc: BaseException) -> RecoveryDecision:
    """Conservatively classify one setup failure without weakening trust gates."""

    message = _message(exc)

    if isinstance(exc, SetupCancelled):
        return RecoveryDecision("cancelled", False, ())

    # ProvenanceError subclasses BootstrapError, so it must be handled first.
    if isinstance(exc, ProvenanceError):
        if "sha-256 mismatch" in message:
            return RecoveryDecision("integrity_retry", True, ("redownload", "reverify"))
        if any(marker in message for marker in _FATAL_PROVENANCE_MARKERS):
            return RecoveryDecision("security_fatal", False, ())
        return RecoveryDecision("provenance_fatal", False, ())

    if isinstance(exc, (TimeoutError, urllib.error.URLError, ConnectionError)):
        return RecoveryDecision("transient_network", True, ("cleanup_partial", "retry"))

    if isinstance(exc, PermissionError):
        return RecoveryDecision("transient_lock", True, ("preserve_active", "cleanup_staging", "retry"))

    if isinstance(exc, OSError):
        if getattr(exc, "winerror", None) in _TRANSIENT_WINERRORS or getattr(exc, "errno", None) in _TRANSIENT_ERRNOS:
            return RecoveryDecision("transient_os", True, ("cleanup_staging", "retry"))
        return RecoveryDecision("os_fatal", False, ())

    if isinstance(exc, BootstrapError):
        if any(marker in message for marker in _FATAL_BOOTSTRAP_MARKERS):
            return RecoveryDecision("unsupported_environment", False, ())
        return RecoveryDecision("bootstrap_incomplete", True, ("redetect", "resume_bootstrap", "retry"))

    return RecoveryDecision("unexpected_fatal", False, ())


def backoff_seconds(policy: RecoveryPolicy, attempt: int) -> float:
    """Return bounded exponential delay after a 1-based failed attempt."""

    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    return min(policy.base_delay_seconds * (2 ** (attempt - 1)), policy.max_delay_seconds)


def cleanup_transients(
    install_dir: Path | str,
    *,
    sleep: Callable[[float], None] | None = None,
) -> tuple[str, ...]:
    """Remove only known AlinaCoder-owned transient files.

    The active executable, its backup, user data, and complete verified cache files
    are deliberately outside this cleanup allow-list.
    """

    root = Path(install_dir)
    sleeper = sleep if sleep is not None else __import__("time").sleep
    candidates: list[Path] = [
        root / "AlinaCoder.exe.staging",
        root / "AlinaCoder.exe.backup.tmp",
        root / "install.json.tmp",
        root / "bootstrap-state.json.tmp",
        root / "bootstrap-receipt.json.tmp",
        root / "recovery-state.json.tmp",
    ]
    cache = root / ".bootstrap-cache"
    if cache.is_dir():
        candidates.extend(sorted(cache.rglob("*.partial")))

    removed: list[str] = []
    for candidate in candidates:
        try:
            existed = candidate.exists()
            unlink_with_retry(candidate, missing_ok=True, sleep=sleeper)
            if existed and not candidate.exists():
                removed.append(str(candidate))
        except FileNotFoundError:
            continue
    return tuple(removed)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class RecoveryJournal:
    schema_version = 1

    def __init__(self, install_dir: Path | str, *, sleep: Callable[[float], None] | None = None) -> None:
        self.install_dir = Path(install_dir)
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.install_dir / "recovery-state.json"
        self._sleep = sleep if sleep is not None else __import__("time").sleep

    def _write(self, payload: dict[str, Any]) -> None:
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        body = {"schema_version": self.schema_version, "updated_at": _utc_now(), **payload}
        temporary.write_text(json.dumps(body, indent=2, sort_keys=True), encoding="utf-8")
        replace_with_retry(temporary, self.path, sleep=self._sleep)

    def load(self) -> dict[str, Any]:
        if not self.path.is_file():
            return {}
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return {}
        return dict(payload) if isinstance(payload, dict) else {}

    def record_running(self, *, operation: str, attempt: int, max_attempts: int) -> None:
        self._write(
            {
                "status": "running",
                "ready": False,
                "operation": operation,
                "attempt": int(attempt),
                "max_attempts": int(max_attempts),
            }
        )

    def record_failure(
        self,
        *,
        operation: str,
        attempt: int,
        max_attempts: int,
        exc: BaseException,
        decision: RecoveryDecision,
    ) -> None:
        self._write(
            {
                "status": "retrying" if decision.recoverable and attempt < max_attempts else "failed",
                "ready": False,
                "operation": operation,
                "attempt": int(attempt),
                "max_attempts": int(max_attempts),
                "category": decision.category,
                "recoverable": bool(decision.recoverable),
                "remediations": list(decision.remediations),
                "error_type": type(exc).__name__,
                "error": redact_setup_text(str(exc))[:4000],
            }
        )

    def record_ready(
        self,
        *,
        operation: str,
        attempt: int,
        max_attempts: int,
        installed_path: Path | str,
    ) -> None:
        self._write(
            {
                "status": "ready",
                "ready": True,
                "operation": operation,
                "attempt": int(attempt),
                "max_attempts": int(max_attempts),
                "installed_path": str(installed_path),
            }
        )


__all__ = [
    "RecoveryDecision",
    "RecoveryJournal",
    "RecoveryPolicy",
    "backoff_seconds",
    "classify_failure",
    "cleanup_transients",
]
