from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
WIN10_11_GUID = "{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"


class Windows10And11PackagingContractTests(unittest.TestCase):
    def test_prerequisite_policy_targets_windows_major_10(self) -> None:
        policy = json.loads((ROOT / "packaging" / "prerequisites-v0.2.json").read_text(encoding="utf-8"))
        self.assertEqual(policy["minimum_windows_major"], 10)

    def test_manifest_declares_windows_10_and_windows_11_supported_os(self) -> None:
        manifest = (ROOT / "packaging" / "alinacoder-windows.manifest").read_text(encoding="utf-8")
        self.assertIn(WIN10_11_GUID, manifest)
        self.assertIn("urn:schemas-microsoft-com:compatibility.v1", manifest)
        self.assertIn("supportedOS", manifest)
        self.assertIn("asInvoker", manifest)

    def test_both_pyinstaller_targets_embed_the_same_windows_manifest(self) -> None:
        build = (ROOT / "scripts" / "build_windows.py").read_text(encoding="utf-8")
        self.assertIn('WINDOWS_MANIFEST = ROOT / "packaging" / "alinacoder-windows.manifest"', build)
        self.assertGreaterEqual(build.count('"--manifest", str(WINDOWS_MANIFEST)'), 2)
        self.assertIn("if not WINDOWS_MANIFEST.exists()", build)


if __name__ == "__main__":
    unittest.main()
