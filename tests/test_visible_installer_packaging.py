from __future__ import annotations

import unittest
from pathlib import Path


class VisibleInstallerPackagingTests(unittest.TestCase):
    def test_setup_pyinstaller_is_windowed_and_entrypoint_uses_gui_router(self) -> None:
        root = Path(__file__).parents[1]
        build = (root / "scripts" / "build_windows.py").read_text(encoding="utf-8")
        entry = (root / "packaging" / "setup_entry.py").read_text(encoding="utf-8")
        self.assertIn('"--windowed"', build)
        self.assertIn('"AlinaCoderSetup"', build)
        self.assertIn("setup_entrypoint", entry)
        self.assertNotIn("installer import main", entry)

    def test_packaged_ui_smoke_contract_is_exposed_without_opening_tk(self) -> None:
        from alinacoder.product.setup_gui import select_setup_mode

        self.assertEqual(select_setup_mode(["--installer-ui-smoke", "--evidence-out", "x.json"]), "smoke")
        self.assertEqual(select_setup_mode(["--quiet", "--install-dir", "C:/Temp/A"]), "cli")


if __name__ == "__main__":
    unittest.main()
