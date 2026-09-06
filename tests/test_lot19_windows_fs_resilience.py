from __future__ import annotations

import hashlib
import io
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from alinacoder.product.installer import _write_metadata
from alinacoder.product.prerequisites import PrerequisiteManifest, ReleaseAsset
from alinacoder.product.windows_trust import NativeWindowsBootstrapAdapter


class Lot19WindowsFilesystemResilienceTests(unittest.TestCase):
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

    @staticmethod
    def _runner(args: list[str], *, timeout: int = 300) -> tuple[int, str]:
        if Path(args[0]).name.lower() == "git.exe":
            return 0, "git version 2.55.0.windows.5"
        return 0, ""

    def test_bootstrap_state_atomic_write_retries_transient_access_denied(self) -> None:
        original_replace = Path.replace
        attempts = 0

        def flaky_replace(source: Path, target: Path | str):
            nonlocal attempts
            if source.name == "bootstrap-state.json.tmp":
                attempts += 1
                if attempts == 1:
                    raise PermissionError(5, "Access is denied", str(source))
            return original_replace(source, target)

        with tempfile.TemporaryDirectory() as td:
            state_dir = Path(td) / "AlinaCoder"
            adapter = NativeWindowsBootstrapAdapter(state_dir, self.manifest, sleep=lambda _: None)
            with patch.object(Path, "replace", flaky_replace):
                adapter._atomic_write_json(adapter.state_path, {"ready": True})

            self.assertEqual(attempts, 2)
            self.assertEqual(json.loads(adapter.state_path.read_text(encoding="utf-8")), {"ready": True})

    def test_install_metadata_atomic_write_retries_transient_access_denied(self) -> None:
        original_replace = Path.replace
        attempts = 0

        def flaky_replace(source: Path, target: Path | str):
            nonlocal attempts
            if source.name == "install.json.tmp":
                attempts += 1
                if attempts == 1:
                    raise PermissionError(5, "Access is denied", str(source))
            return original_replace(source, target)

        with tempfile.TemporaryDirectory() as td:
            install_dir = Path(td) / "AlinaCoder"
            with patch.object(Path, "replace", flaky_replace):
                _write_metadata(install_dir, operation="install", deferred=True)

            self.assertEqual(attempts, 2)
            payload = json.loads((install_dir / "install.json").read_text(encoding="utf-8"))
            self.assertFalse(payload["bootstrap_ready"])
            self.assertEqual(payload["bootstrap_blockers"], ["deferred"])

    def test_verified_download_retries_partial_cleanup_and_cache_promotion_locks(self) -> None:
        data = b"verified-release-asset"
        digest = hashlib.sha256(data).hexdigest()
        asset = ReleaseAsset(
            "git",
            "git-for-windows/git",
            "2.55.0.5",
            "MinGit-2.55.0.5-64-bit.zip",
            "https://github.com/git-for-windows/git/releases/download/v2.55.0.windows.5/MinGit-2.55.0.5-64-bit.zip",
            digest,
        )
        original_unlink = Path.unlink
        original_replace = Path.replace
        unlink_attempts = 0
        replace_attempts = 0

        def flaky_unlink(path: Path, *args, **kwargs):
            nonlocal unlink_attempts
            if path.name.endswith(".partial"):
                unlink_attempts += 1
                if unlink_attempts == 1:
                    raise PermissionError(5, "Access is denied", str(path))
            return original_unlink(path, *args, **kwargs)

        def flaky_replace(source: Path, target: Path | str):
            nonlocal replace_attempts
            if source.name.endswith(".partial"):
                replace_attempts += 1
                if replace_attempts == 1:
                    raise PermissionError(5, "Access is denied", str(source))
            return original_replace(source, target)

        with tempfile.TemporaryDirectory() as td:
            state_dir = Path(td) / "AlinaCoder"
            adapter = NativeWindowsBootstrapAdapter(
                state_dir,
                self.manifest,
                download_bytes=lambda _: data,
                sleep=lambda _: None,
            )
            partial = adapter.cache_dir / "MinGit-2.55.0.5-64-bit.zip.partial"
            partial.write_bytes(b"stale")
            with patch.object(Path, "unlink", flaky_unlink), patch.object(Path, "replace", flaky_replace):
                target = adapter.download_verified(asset, require_authenticode=False)

            self.assertGreaterEqual(unlink_attempts, 2)
            self.assertEqual(replace_attempts, 2)
            self.assertEqual(target.read_bytes(), data)
            self.assertFalse(partial.exists())

    def test_stale_mingit_staging_is_not_silently_promoted_after_cleanup_lock(self) -> None:
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
            "assets": [{"name": asset_name, "digest": f"sha256:{digest}", "browser_download_url": asset_url}],
        }

        import shutil

        original_rmtree = shutil.rmtree
        staging_cleanup_attempts = 0

        def flaky_rmtree(path, *args, **kwargs):
            nonlocal staging_cleanup_attempts
            candidate = Path(path)
            if candidate.name == "Git.alinacoder-staging" and candidate.exists():
                staging_cleanup_attempts += 1
                if staging_cleanup_attempts == 1:
                    # Simulate Windows/Defender keeping a stale staging directory alive
                    # while shutil.rmtree(ignore_errors=True) reports no actionable error.
                    return None
            return original_rmtree(path, *args, **kwargs)

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            local = root / "LocalAppData"
            state = root / "AlinaCoder"
            staging = local / "Programs" / "AlinaCoder" / "Git.alinacoder-staging"
            staging.mkdir(parents=True)
            (staging / "obsolete-from-failed-run.txt").write_text("stale", encoding="utf-8")

            with patch.dict(os.environ, {"LOCALAPPDATA": str(local)}, clear=False):
                adapter = NativeWindowsBootstrapAdapter(
                    state,
                    self.manifest,
                    download_bytes=lambda _: archive_bytes,
                    command_runner=self._runner,
                    json_loader=lambda _: release,
                    sleep=lambda _: None,
                )
                with patch("alinacoder.product.windows_trust.shutil.rmtree", flaky_rmtree):
                    adapter.install_component("git", operation="install")

            managed_root = local / "Programs" / "AlinaCoder" / "Git"
            self.assertGreaterEqual(staging_cleanup_attempts, 2)
            self.assertTrue((managed_root / "cmd" / "git.exe").is_file())
            self.assertFalse((managed_root / "obsolete-from-failed-run.txt").exists())


if __name__ == "__main__":
    unittest.main()
