from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import threading
from typing import Callable


@dataclass(frozen=True)
class SetupEvent:
    phase: str
    kind: str
    message: str
    detail: str = ""
    current: int | None = None
    total: int | None = None


SetupEventSink = Callable[[SetupEvent], None]


class SetupCancelled(RuntimeError):
    pass


class CancellationToken:
    def __init__(self) -> None:
        self._event = threading.Event()

    @property
    def cancelled(self) -> bool:
        return self._event.is_set()

    def cancel(self) -> None:
        self._event.set()

    def raise_if_cancelled(self) -> None:
        if self.cancelled:
            raise SetupCancelled("installation cancelled by user")


_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[^\s]+"),
    re.compile(r"(?i)((?:api[_-]?key|token|secret|password)\s*[=:]\s*)[^\s,;]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
)


def redact_setup_text(value: str) -> str:
    text = str(value)
    for pattern in _SECRET_PATTERNS:
        if pattern.groups:
            text = pattern.sub(lambda match: f"{match.group(1)}[REDACTED]", text)
        else:
            text = pattern.sub("[REDACTED]", text)
    return text


class SetupLogger:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def __call__(self, event: SetupEvent) -> None:
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        message = redact_setup_text(event.message)
        detail = redact_setup_text(event.detail)
        progress = ""
        if event.current is not None:
            progress = f" current={event.current}"
        if event.total is not None:
            progress += f" total={event.total}"
        line = f"{stamp} phase={event.phase} kind={event.kind}{progress} message={message}"
        if detail:
            line += f" detail={detail}"
        with self._lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")


def combine_event_sinks(*sinks: SetupEventSink | None) -> SetupEventSink:
    active = tuple(sink for sink in sinks if sink is not None)

    def emit(event: SetupEvent) -> None:
        for sink in active:
            sink(event)

    return emit


def default_setup_log_path() -> Path:
    from os import environ

    base = Path(environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / "AlinaCoder" / "logs"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return base / f"setup-{stamp}.log"
