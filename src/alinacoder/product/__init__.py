"""AlinaCoder product runtime bindings.

The canonical prerequisite bootstrap stays bound to the native WinVerifyTrust
adapter. The graphical setup imports the observable subclass explicitly so adding
UI progress cannot alter the historical LOT19 production binding.
"""

import os


def _apply_ci_bootstrap_timeouts() -> None:
    """Use shorter fail-fast bootstrap budgets only inside GitHub Actions."""

    if os.environ.get("GITHUB_ACTIONS", "").strip().lower() == "true":
        os.environ.setdefault("ALINACODER_MODEL_PULL_TIMEOUT_SECONDS", "180")


_apply_ci_bootstrap_timeouts()

from . import prerequisites as _prerequisites
from . import windows_trust as _windows_trust
from .silent_bootstrap import harden_windows_bootstrap

harden_windows_bootstrap()
NativeWindowsBootstrapAdapter = _windows_trust.NativeWindowsBootstrapAdapter
ObservableWindowsBootstrapAdapter = _windows_trust.ObservableWindowsBootstrapAdapter
_prerequisites.WindowsBootstrapAdapter = NativeWindowsBootstrapAdapter

from .windows_fs_hardening import harden_windows_filesystem

harden_windows_filesystem()

from .self_healing import bind_self_healing_installer

bind_self_healing_installer()

__all__ = ["NativeWindowsBootstrapAdapter", "ObservableWindowsBootstrapAdapter"]
