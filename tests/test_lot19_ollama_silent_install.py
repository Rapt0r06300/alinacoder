from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product.prerequisites import (
    ComponentInventory,
    InstalledComponent,
    PrerequisiteManifest,
    ReleaseAsset,
    WindowsBootstrapAdapter,
)


class Lot19OllamaSilentInstallTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.manifest = PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")

    def test_ollama_installer_suppresses_all_message_boxes(self) -> None:
        calls: list[tuple[list[str], int]] = []

        def runner(args: list[str], *, timeout: int = 300):
            calls.append((list(args), timeout))
            return 0, ""

        asset = ReleaseAsset(
            component="ollama",
            repository="ollama/ollama",
            version="0.33.3",
            name="OllamaSetup.exe",
            url="https://github.com/ollama/ollama/releases/download/v0.33.3/OllamaSetup.exe",
            sha256="a" * 64,
        )
        installed = InstalledComponent(
            name="ollama",
            version="0.33.3",
            origin="managed_by_alinacoder",
            path="C:/Users/test/AppData/Local/Programs/Ollama/ollama.exe",
        )

        with tempfile.TemporaryDirectory() as td:
            adapter = WindowsBootstrapAdapter(Path(td), self.manifest, command_runner=runner)
            with (
                patch.object(adapter, "latest_asset", return_value=asset),
                patch.object(adapter, "download_verified", return_value=Path(td) / "OllamaSetup.exe"),
                patch.object(
                    adapter,
                    "detect_inventory",
                    side_effect=[
                        ComponentInventory(None, None),
                        ComponentInventory(None, installed),
                    ],
                ),
            ):
                adapter.install_component("ollama", operation="install")

        self.assertEqual(len(calls), 1)
        args, timeout = calls[0]
        self.assertIn("/VERYSILENT", args)
        self.assertIn("/NORESTART", args)
        self.assertIn("/SUPPRESSMSGBOXES", args)
        self.assertEqual(timeout, 1800)


if __name__ == "__main__":
    unittest.main()
