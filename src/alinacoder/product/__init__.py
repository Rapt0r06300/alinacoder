"""AlinaCoder product runtime bindings.

The canonical prerequisite bootstrap stays bound to the native WinVerifyTrust
adapter. The graphical setup imports the observable subclass explicitly so adding
UI progress cannot alter the historical LOT19 production binding.
"""

from . import prerequisites as _prerequisites
from .windows_trust import NativeWindowsBootstrapAdapter, ObservableWindowsBootstrapAdapter

_prerequisites.WindowsBootstrapAdapter = NativeWindowsBootstrapAdapter

__all__ = ["NativeWindowsBootstrapAdapter", "ObservableWindowsBootstrapAdapter"]
