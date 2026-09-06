from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from alinacoder.product.prerequisites import ComponentReceipt, PrerequisiteManifest
from alinacoder.product.windows_trust import NativeWindowsBootstrapAdapter


class Lot19InstallerProcessBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.manifest = PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")

    def test_silent_installer_uses_devnull_instead_of_captured_child_pipes(self) -> None:
        process = MagicMock()
        process.wait.return_value = 0

        with tempfile.TemporaryDirectory() as td:
            adapter = NativeWindowsBootstrapAdapter(Path(td), self.manifest)
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

    def test_cli_output_with_invalid_locale_byte_does_not_crash_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            adapter = NativeWindowsBootstrapAdapter(Path(td), self.manifest)
            code, output = adapter._default_command_runner(
                [
                    sys.executable,
                    "-c",
                    "import sys; sys.stdout.buffer.write(b'prefix\\x8fsuffix')",
                ],
                timeout=30,
            )

        self.assertEqual(code, 0)
        self.assertIn("prefix", output)
        self.assertIn("suffix", output)

    def test_ollama_post_install_verification_does_not_enumerate_models(self) -> None:
        receipt = ComponentReceipt(
            name="ollama",
            version=self.manifest.ollama.minimum_version,
            origin="managed_by_alinacoder",
            source_url="https://github.com/ollama/ollama/releases/download/v0.0.0/OllamaSetup.exe",
            sha256="0" * 64,
            healthy=True,
        )
        base_adapter = NativeWindowsBootstrapAdapter.__mro__[1]

        with tempfile.TemporaryDirectory() as td:
            adapter = NativeWindowsBootstrapAdapter(Path(td), self.manifest)
            with (
                patch.object(base_adapter, "install_component", return_value=receipt) as base_install,
                patch.object(adapter, "detect_inventory", side_effect=AssertionError("post-install model enumeration must not run")),
                patch.object(adapter, "_find_executable", return_value=Path("C:/Users/test/AppData/Local/Programs/Ollama/ollama.exe")),
                patch.object(adapter, "_component_version", return_value=self.manifest.ollama.minimum_version),
            ):
                actual = adapter.install_component("ollama", operation="install")

        self.assertEqual(actual, receipt)
        base_install.assert_called_once_with(adapter, "ollama", operation="install")


if __name__ == "__main__":
    unittest.main()
