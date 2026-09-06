from __future__ import annotations

from pathlib import Path
from typing import Any

from . import windows_trust as _windows_trust


def _official_silent_installer_args(args: list[str]) -> list[str]:
    """Match Ollama's official fully-silent Windows installer invocation."""

    if not args or Path(args[0]).name.casefold() != "ollamasetup.exe":
        return args
    switches = {str(item).casefold() for item in args[1:]}
    if "/verysilent" not in switches or "/suppressmsgboxes" in switches:
        return args
    return [*args, "/SUPPRESSMSGBOXES"]


def harden_windows_bootstrap() -> None:
    """Harden the native adapter in place while preserving its canonical identity."""

    adapter = _windows_trust.NativeWindowsBootstrapAdapter
    if getattr(adapter, "_alinacoder_official_silent_guard", False):
        return

    original_run = adapter._run

    def hardened_run(self: Any, args: list[str], *, timeout: int = 300) -> tuple[int, str]:
        return original_run(self, _official_silent_installer_args(list(args)), timeout=timeout)

    hardened_run.__name__ = original_run.__name__
    hardened_run.__qualname__ = f"{adapter.__name__}._run"
    hardened_run.__module__ = adapter.__module__
    adapter._run = hardened_run  # type: ignore[method-assign]
    adapter._alinacoder_official_silent_guard = True  # type: ignore[attr-defined]


__all__ = ["harden_windows_bootstrap", "_official_silent_installer_args"]
