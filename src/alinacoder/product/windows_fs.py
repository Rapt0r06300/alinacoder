from __future__ import annotations

import errno
from pathlib import Path
import shutil
import time
from typing import Callable


_TRANSIENT_WINERRORS = {5, 32, 33}
_TRANSIENT_ERRNOS = {errno.EACCES, errno.EPERM, errno.EBUSY}


def _is_transient_lock(exc: OSError) -> bool:
    """Return True only for filesystem failures that can be transient on Windows."""

    return (
        isinstance(exc, PermissionError)
        or getattr(exc, "winerror", None) in _TRANSIENT_WINERRORS
        or getattr(exc, "errno", None) in _TRANSIENT_ERRNOS
    )


def _delay(attempt: int) -> float:
    return min(0.15 * (2**attempt), 2.0)


def replace_with_retry(
    source: Path | str,
    destination: Path | str,
    *,
    attempts: int = 8,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Atomically promote a path while tolerating short-lived Windows file locks."""

    src = Path(source)
    dst = Path(destination)
    for attempt in range(max(1, attempts)):
        try:
            src.replace(dst)
            return
        except OSError as exc:
            if not _is_transient_lock(exc) or attempt + 1 >= max(1, attempts):
                raise
            sleep(_delay(attempt))


def unlink_with_retry(
    path: Path | str,
    *,
    missing_ok: bool = True,
    attempts: int = 8,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Remove a file with bounded retry for antivirus/indexer sharing violations."""

    candidate = Path(path)
    for attempt in range(max(1, attempts)):
        try:
            candidate.unlink(missing_ok=missing_ok)
            return
        except FileNotFoundError:
            if missing_ok:
                return
            raise
        except OSError as exc:
            if not _is_transient_lock(exc) or attempt + 1 >= max(1, attempts):
                raise
            sleep(_delay(attempt))


def rmtree_with_retry(
    path: Path | str,
    *,
    attempts: int = 8,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Remove a directory completely; never hide a stale partially removed tree."""

    candidate = Path(path)
    limit = max(1, attempts)
    for attempt in range(limit):
        if not candidate.exists():
            return
        last_error: OSError | None = None
        try:
            shutil.rmtree(candidate)
        except FileNotFoundError:
            return
        except OSError as exc:
            if not _is_transient_lock(exc):
                raise
            last_error = exc

        if not candidate.exists():
            return
        if attempt + 1 >= limit:
            if last_error is not None:
                raise last_error
            raise PermissionError(5, "Access is denied", str(candidate))
        sleep(_delay(attempt))
