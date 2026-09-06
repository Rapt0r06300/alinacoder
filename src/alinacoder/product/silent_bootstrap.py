from __future__ import annotations

from pathlib import Path

from .windows_trust import (
    NativeWindowsBootstrapAdapter as _NativeWindowsBootstrapAdapter,
    ObservableWindowsBootstrapAdapter as _ObservableWindowsBootstrapAdapter,
)


def _official_silent_installer_args(args: list[str]) -> list[str]:
    """Match Ollama's official fully-silent Windows installer invocation."""

    if not args or Path(args[0]).name.casefold() != "ollamasetup.exe":
        return args
    switches = {str(item).casefold() for item in args[1:]}
    if "/verysilent" not in switches or "/suppressmsgboxes" in switches:
        return args
    return [*args, "/SUPPRESSMSGBOXES"]


class NativeWindowsBootstrapAdapter(_NativeWindowsBootstrapAdapter):
    """Native bootstrap with the official non-interactive Ollama installer flags."""

    def _run(self, args: list[str], *, timeout: int = 300) -> tuple[int, str]:
        return super()._run(_official_silent_installer_args(list(args)), timeout=timeout)


class ObservableWindowsBootstrapAdapter(_ObservableWindowsBootstrapAdapter):
    """Observable bootstrap with the same fully-silent Ollama process boundary."""

    def _run(self, args: list[str], *, timeout: int = 300) -> tuple[int, str]:
        return super()._run(_official_silent_installer_args(list(args)), timeout=timeout)


__all__ = [
    "NativeWindowsBootstrapAdapter",
    "ObservableWindowsBootstrapAdapter",
    "_official_silent_installer_args",
]
