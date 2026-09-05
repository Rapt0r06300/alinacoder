from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from alinacoder.product.prerequisites import PrerequisiteManifest
from alinacoder.product.windows_trust import NativeWindowsBootstrapAdapter


class Lot19InstallerProcessBoundaryTests(unittest.TestCase):
    def test_silent_installer_uses_devnull_instead_of_captured_child_pipes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")
        process = MagicMock()
        process.wait.return_value = 0

        with tempfile.TemporaryDirectory() as td:
            adapter = NativeWindowsBootstrapAdapter(Path(td), manifest)
            with patch("alinacoder.product.windows_trust.subprocess.Popen", return_value=process) as popen:
                code, output = adapter._default_command_runner(
                    ["C:/Temp/GitSetup.exe", "/VERYSILENT", "/NORESTART", "/CURRENTUSER"],
                    timeout=120,
                )

        self.assertEqual(code, 0)
        self.assertEqual(output, "")
        kwargs = popen.call_args.kwargs
        self.assertIs(kwargs["stdout"], subprocess.DEVNULL)
        self.assertIs(kwargs["stderr"], subprocess.DEVNULL)
        self.assertIs(kwargs["stdin"], subprocess.DEVNULL)
        process.wait.assert_called_once_with(timeout=120)


if __name__ == "__main__":
    unittest.main()
