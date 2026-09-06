"""AlinaCoder product runtime bindings.

Windows prerequisite bootstrap is bound here to the native WinVerifyTrust adapter
plus the user-visible event layer so every normal product import path keeps the
same fail-closed trust behavior while graphical setup can observe progress.
"""

from . import prerequisites as _prerequisites
from .windows_trust import NativeWindowsBootstrapAdapter
from .observable_bootstrap import ObservableWindowsBootstrapAdapter

_prerequisites.WindowsBootstrapAdapter = ObservableWindowsBootstrapAdapter

__all__ = ["NativeWindowsBootstrapAdapter", "ObservableWindowsBootstrapAdapter"]
