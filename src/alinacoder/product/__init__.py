"""AlinaCoder product runtime bindings.

Windows prerequisite bootstrap is bound here to the native WinVerifyTrust adapter
so every normal import path uses OS trust verification rather than a PowerShell
subprocess whose module autoload can vary by host environment.
"""

from . import prerequisites as _prerequisites
from .windows_trust import NativeWindowsBootstrapAdapter

_prerequisites.WindowsBootstrapAdapter = NativeWindowsBootstrapAdapter

__all__ = ["NativeWindowsBootstrapAdapter"]
