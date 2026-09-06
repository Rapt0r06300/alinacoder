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
from .silent_bootstrap import NativeWindowsBootstrapAdapter, ObservableWindowsBootstrapAdapter

# Bind both historical import paths to the same hardened production adapters.
_prerequisites.WindowsBootstrapAdapter = NativeWindowsBootstrapAdapter
_windows_trust.NativeWindowsBootstrapAdapter = NativeWindowsBootstrapAdapter
_windows_trust.ObservableWindowsBootstrapAdapter = ObservableWindowsBootstrapAdapter

__all__ = ["NativeWindowsBootstrapAdapter", "ObservableWindowsBootstrapAdapter"]
