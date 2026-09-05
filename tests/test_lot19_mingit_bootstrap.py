from __future__ import annotations

import hashlib
import io
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from alinacoder.product.prerequisites import (
    BootstrapReport,
    BootstrapState,
    ComponentReceipt,
    PrerequisiteManifest,
)
from alinacoder.product.windows_trust import NativeWindowsBootstrapAdapter
from alinacoder.tools.git import GitMainExecutor


class Lot19MinGitBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.manifest = PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")

    @staticmethod
    def _mingit_zip() -> bytes:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("cmd/git.exe", b"fake-git-for-test")
            archive.writestr("etc/gitconfig", b"[core]\n\tautocrlf = false\n")
        return buffer.getvalue()

    def test_missing_git_uses_verified_official_mingit_zip_without_gui_installer(self) -> None:
        archive_bytes = self._mingit_zip()
        digest = hashlib.sha256(archive_bytes).hexdigest()
        asset_name = "MinGit-2.55.0.5-64-bit.zip"
        asset_url = (
            "https://github.com/git-for-windows/git/releases/download/"
            "v2.55.0.windows.5/MinGit-2.55.0.5-64-bit.zip"
        )
        release = {
            "html_url": "https://github.com/git-for-windows/git/releases/tag/v2.55.0.windows.5",
            "tag_name": "v2.55.0.windows.5",
            "assets": [
                {
                    "name": asset_name,
                    "digest": f"sha256:{digest}",
                    "browser_download_url": asset_url,
                }
            ],
        }
        calls: list[list[str]] = []

        def runner(args: list[str], *, timeout: int = 300):
            calls.append(list(args))
            if Path(args[0]).name.lower() == "git.exe":
                return 0, "git version 2.55.0.windows.5"
            return 0, ""

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            local = root / "LocalAppData"
            state = root / "AlinaCoder"
            with patch.dict(os.environ, {"LOCALAPPDATA": str(local)}, clear=False):
                adapter = NativeWindowsBootstrapAdapter(
                    state,
                    self.manifest,
                    download_bytes=lambda _: archive_bytes,
                    command_runner=runner,
                    json_loader=lambda _: release,
                    sleep=lambda _: None,
                )
                receipt = adapter.install_component("git", operation="install")

            managed_git = local / "Programs" / "AlinaCoder" / "Git" / "cmd" / "git.exe"
            self.assertTrue(managed_git.is_file())
            self.assertEqual(receipt.origin, "managed_by_alinacoder")
            self.assertEqual(receipt.source_url, asset_url)
            self.assertEqual(receipt.sha256, digest)
            self.assertTrue(all(Path(call[0]).name != asset_name for call in calls))
            self.assertTrue(any(Path(call[0]) == managed_git for call in calls))

    def test_git_executor_resolves_alinacoder_managed_mingit_without_path_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            local = Path(td) / "LocalAppData"
            managed_git = local / "Programs" / "AlinaCoder" / "Git" / "cmd" / "git.exe"
            managed_git.parent.mkdir(parents=True)
            managed_git.write_bytes(b"managed-git")
            with patch.dict(os.environ, {"LOCALAPPDATA": str(local)}, clear=False):
                executor = GitMainExecutor()
            self.assertEqual(Path(executor.git_executable), managed_git)

    def test_explicit_purge_removes_managed_mingit_without_touching_other_programs(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            local = root / "LocalAppData"
            git_root = local / "Programs" / "AlinaCoder" / "Git"
            managed_git = git_root / "cmd" / "git.exe"
            managed_git.parent.mkdir(parents=True)
            managed_git.write_bytes(b"managed-git")
            other = local / "Programs" / "UserTool" / "keep.txt"
            other.parent.mkdir(parents=True)
            other.write_text("keep", encoding="utf-8")
            state_dir = root / "AlinaCoder"
            state = BootstrapState(
                {
                    "git": ComponentReceipt(
                        "git",
                        "2.55.0.5",
                        "managed_by_alinacoder",
                        "https://github.com/git-for-windows/git/releases/download/"
                        "v2.55.0.windows.5/MinGit-2.55.0.5-64-bit.zip",
                        "a" * 64,
                        True,
                        path=str(managed_git),
                    )
                },
                "qwen3:0.6b",
                True,
            )
            with patch.dict(os.environ, {"LOCALAPPDATA": str(local)}, clear=False):
                adapter = NativeWindowsBootstrapAdapter(state_dir, self.manifest, sleep=lambda _: None)
                adapter.persist_report(BootstrapReport(True, "qwen3:0.6b", (), (), state))
                removed = adapter.managed_uninstall(purge=True)

            self.assertEqual(removed, ("git",))
            self.assertFalse(git_root.exists())
            self.assertTrue(other.is_file())


if __name__ == "__main__":
    unittest.main()
