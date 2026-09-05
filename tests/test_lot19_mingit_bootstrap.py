from __future__ import annotations

import hashlib
import io
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from alinacoder.product.prerequisites import PrerequisiteManifest
from alinacoder.product.windows_trust import NativeWindowsBootstrapAdapter


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

            managed_git = local / "Programs" / "Git" / "cmd" / "git.exe"
            self.assertTrue(managed_git.is_file())
            self.assertEqual(receipt.origin, "managed_by_alinacoder")
            self.assertEqual(receipt.source_url, asset_url)
            self.assertEqual(receipt.sha256, digest)
            self.assertTrue(all(Path(call[0]).name != asset_name for call in calls))
            self.assertTrue(any(Path(call[0]) == managed_git for call in calls))


if __name__ == "__main__":
    unittest.main()
