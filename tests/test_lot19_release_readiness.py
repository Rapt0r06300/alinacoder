from __future__ import annotations

import unittest
from pathlib import Path

from alinacoder.release.acceptance import ReleaseBundle


ROOT = Path(__file__).parents[1]


class Lot19ReleaseReadinessTests(unittest.TestCase):
    def test_setup_build_bundles_versioned_prerequisite_manifest(self) -> None:
        source = (ROOT / "scripts" / "build_windows.py").read_text(encoding="utf-8")
        self.assertIn("prerequisites-v0.2.json", source)
        self.assertIn("--add-data", source)

    def test_release_bundle_requires_prerequisite_policy(self) -> None:
        old = {"AlinaCoder.exe", "AlinaCoderSetup.exe", "release-manifest.json", "sbom.spdx.json", "USER_GUIDE.md", "OPERATIONS.md"}
        self.assertFalse(ReleaseBundle(old).complete())
        self.assertTrue(ReleaseBundle(old | {"prerequisites-v0.2.json"}).complete())

    def test_release_metadata_includes_external_prerequisite_policy(self) -> None:
        source = (ROOT / "scripts" / "generate_release_metadata.py").read_text(encoding="utf-8")
        self.assertIn("prerequisites-v0.2.json", source)
        self.assertIn("ollama", source.lower())
        self.assertIn("git", source.lower())
        self.assertIn("model", source.lower())

    def test_final_ci_requires_bootstrap_e2e_on_same_artifact(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("bootstrap_e2e", workflow)
        self.assertIn("lot19-bootstrap-evidence.json", workflow)
        self.assertIn("verify_lot19_bootstrap.py", workflow)


if __name__ == "__main__":
    unittest.main()
