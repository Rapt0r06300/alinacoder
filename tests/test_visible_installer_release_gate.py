from __future__ import annotations

import unittest
from pathlib import Path


class VisibleInstallerReleaseGateTests(unittest.TestCase):
    def test_publisher_requires_real_default_double_click_and_ui_evidence(self) -> None:
        root = Path(__file__).parents[1]
        workflow = (root / ".github" / "workflows" / "publish-v0.2.0.yml").read_text(encoding="utf-8")
        self.assertIn("Verify real double-click setup window", workflow)
        self.assertIn("AlinaCoderSetup.exe", workflow)
        self.assertIn("HasExited", workflow)
        self.assertIn("--installer-ui-smoke", workflow)
        self.assertIn("visible-installer-evidence.json", workflow)
        self.assertIn("visible_installer_e2e", workflow)
        self.assertIn("setup_sha256", workflow)

    def test_published_asset_set_contains_visible_installer_evidence(self) -> None:
        root = Path(__file__).parents[1]
        workflow = (root / ".github" / "workflows" / "publish-v0.2.0.yml").read_text(encoding="utf-8")
        self.assertGreaterEqual(workflow.count("visible-installer-evidence.json"), 4)
        self.assertIn("gh release upload", workflow)
        self.assertIn("--clobber", workflow)


if __name__ == "__main__":
    unittest.main()
