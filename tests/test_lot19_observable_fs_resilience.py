from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product.prerequisites import PrerequisiteManifest, ReleaseAsset
from alinacoder.product.windows_trust import ObservableWindowsBootstrapAdapter


class Lot19ObservableFilesystemResilienceTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.manifest = PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")

    def test_gui_verified_download_retries_transient_partial_and_promotion_locks(self) -> None:
        data = b"gui-verified-release-asset"
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
            events = []
            adapter = ObservableWindowsBootstrapAdapter(
                state_dir,
                self.manifest,
                download_bytes=lambda _: data,
                event_sink=events.append,
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
            self.assertTrue(any(event.kind == "complete" for event in events))


if __name__ == "__main__":
    unittest.main()
