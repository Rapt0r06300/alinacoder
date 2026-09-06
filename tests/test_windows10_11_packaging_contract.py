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

    def test_release_manifest_proves_both_packaged_executables_carry_windows_contract(self) -> None:
        generator = (ROOT / "scripts" / "generate_release_metadata.py").read_text(encoding="utf-8")
        self.assertIn('setup = DIST / "AlinaCoderSetup.exe"', generator)
        self.assertIn('manifest["windows_compatibility"]', generator)
        self.assertIn('"minimum_windows_major": 10', generator)
        self.assertIn('"supported_os_guid": WIN10_11_GUID', generator)
        self.assertIn('"windows_10": True', generator)
        self.assertIn('"windows_11": True', generator)
        self.assertIn('"app_manifest_embedded": app_manifest_embedded', generator)
        self.assertIn('"setup_manifest_embedded": setup_manifest_embedded', generator)

    def test_publisher_fails_closed_unless_windows_10_11_evidence_is_true(self) -> None:
        publish = (ROOT / ".github" / "workflows" / "publish-v0.2.0.yml").read_text(encoding="utf-8")
        self.assertIn("$windows = $releaseManifest.windows_compatibility", publish)
        self.assertIn("$windows.minimum_windows_major -ne 10", publish)
        self.assertIn(WIN10_11_GUID, publish)
        self.assertIn("-not $windows.windows_10", publish)
        self.assertIn("-not $windows.windows_11", publish)
        self.assertIn("-not $windows.app_manifest_embedded", publish)
        self.assertIn("-not $windows.setup_manifest_embedded", publish)


if __name__ == "__main__":
    unittest.main()
