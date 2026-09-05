from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product import installer, prerequisites as p


ADAPTER_AVAILABLE = hasattr(p, "WindowsBootstrapAdapter")
INSTALLER_BOOTSTRAP_AVAILABLE = hasattr(installer, "build_bootstrapper")


class Lot19WindowsBootstrapContractTests(unittest.TestCase):
    def test_windows_adapter_and_installer_factory_exist(self) -> None:
        self.assertTrue(ADAPTER_AVAILABLE, "WindowsBootstrapAdapter is required")
        self.assertTrue(INSTALLER_BOOTSTRAP_AVAILABLE, "installer.build_bootstrapper is required")


@unittest.skipUnless(ADAPTER_AVAILABLE, "Windows adapter not implemented yet")
class Lot19VerifiedDownloadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = p.PrerequisiteManifest.load(Path(__file__).parents[1] / "packaging" / "prerequisites-v0.2.json")

    def test_download_rejects_digest_mismatch_before_execution(self) -> None:
        payload = b"official-but-corrupted"
        asset = p.ReleaseAsset("ollama", "ollama/ollama", "0.33.3", "OllamaSetup.exe", "https://github.com/ollama/ollama/releases/download/v0.33.3/OllamaSetup.exe", "0" * 64)
        with tempfile.TemporaryDirectory() as td:
            adapter = p.WindowsBootstrapAdapter(Path(td), self.manifest, download_bytes=lambda url: payload, command_runner=lambda *args, **kwargs: (0, ""))
            with self.assertRaises(p.ProvenanceError):
                adapter.download_verified(asset)
            self.assertEqual(list(Path(td).glob("**/OllamaSetup.exe")), [])

    def test_valid_digest_download_is_atomically_promoted(self) -> None:
        payload = b"verified-binary"
        asset = p.ReleaseAsset("git", "git-for-windows/git", "2.55.0", "Git-2.55.0-64-bit.exe", "https://github.com/git-for-windows/git/releases/download/v2.55.0.windows.1/Git-2.55.0-64-bit.exe", hashlib.sha256(payload).hexdigest())
        with tempfile.TemporaryDirectory() as td:
            adapter = p.WindowsBootstrapAdapter(Path(td), self.manifest, download_bytes=lambda url: payload, command_runner=lambda *args, **kwargs: (0, "Valid"))
            path = adapter.download_verified(asset, require_authenticode=False)
            self.assertTrue(path.exists())
            self.assertEqual(path.read_bytes(), payload)

    def test_clean_inventory_override_is_consumed_once_then_real_install_is_visible(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            git = root / "git.exe"
            ollama = root / "ollama.exe"
            git.write_bytes(b"git")
            ollama.write_bytes(b"ollama")

            def runner(args, **kwargs):
                command = str(args[0]).lower()
                if "git" in command:
                    return (0, "git version 2.55.0")
                if len(args) > 1 and args[1] == "list":
                    return (0, "NAME ID SIZE MODIFIED\n")
                return (0, "ollama version is 0.33.3")

            with patch.dict(os.environ, {"ALINACODER_BOOTSTRAP_IGNORE_EXISTING": "git,ollama"}):
                adapter = p.WindowsBootstrapAdapter(root, self.manifest, command_runner=runner)
                adapter._candidate_executables = lambda name: (git if name == "git" else ollama,)  # type: ignore[method-assign]
                first = adapter.detect_inventory()
                second = adapter.detect_inventory()
            self.assertIsNone(first.git)
            self.assertIsNone(first.ollama)
            self.assertIsNotNone(second.git)
            self.assertIsNotNone(second.ollama)


@unittest.skipUnless(ADAPTER_AVAILABLE and INSTALLER_BOOTSTRAP_AVAILABLE, "Installer bootstrap integration not implemented yet")
class Lot19InstallerLifecycleIntegrationTests(unittest.TestCase):
    def fake_report(self, ready: bool):
        return p.BootstrapReport(ready=ready, selected_model="qwen3:0.6b", actions=(), blockers=() if ready else ("network",))

    def test_installer_metadata_is_not_ready_when_bootstrap_is_unproven(self) -> None:
        class FakeBootstrapper:
            def run(self, **kwargs): return self_outer.fake_report(False)
        self_outer = self
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "app.exe"
            source.write_bytes(b"app")
            with self.assertRaises(p.BootstrapError):
                installer.install(root / "dest", source_exe=source, bootstrapper=FakeBootstrapper())
            metadata = json.loads((root / "dest" / "install.json").read_text(encoding="utf-8"))
            self.assertFalse(metadata["bootstrap_ready"])
            self.assertEqual(metadata["bootstrap_blockers"], ["network"])

    def test_deferred_install_copies_app_but_records_not_ready(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "app.exe"
            source.write_bytes(b"app")
            target = installer.install(root / "dest", source_exe=source, deferred_prerequisites=True)
            self.assertTrue(target.exists())
            metadata = json.loads((root / "dest" / "install.json").read_text(encoding="utf-8"))
            self.assertFalse(metadata["bootstrap_ready"])
            self.assertIn("deferred", metadata["bootstrap_blockers"])

    def test_successful_bootstrap_sets_ready_and_selected_model(self) -> None:
        class FakeBootstrapper:
            def run(self, **kwargs): return self_outer.fake_report(True)
        self_outer = self
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "app.exe"
            source.write_bytes(b"app")
            installer.install(root / "dest", source_exe=source, bootstrapper=FakeBootstrapper())
            metadata = json.loads((root / "dest" / "install.json").read_text(encoding="utf-8"))
            self.assertTrue(metadata["bootstrap_ready"])
            self.assertEqual(metadata["selected_model"], "qwen3:0.6b")

    def test_normal_uninstall_does_not_request_external_prerequisite_removal(self) -> None:
        class FakeBootstrapper:
            def managed_uninstall(self, purge=False):
                calls.append(purge)
        calls = []
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            root.mkdir(exist_ok=True)
            (root / "AlinaCoder.exe").write_bytes(b"app")
            (root / "install.json").write_text("{}", encoding="utf-8")
            installer.uninstall(root, bootstrapper=FakeBootstrapper())
        self.assertEqual(calls, [False])


if __name__ == "__main__":
    unittest.main()
