from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from alinacoder.product import prerequisites as p
from alinacoder.product.windows_trust import ObservableWindowsBootstrapAdapter


class VisibleInstallerEventTests(unittest.TestCase):
    def test_setup_event_logger_is_durable_and_redacts_secrets(self) -> None:
        from alinacoder.product.setup_events import SetupEvent, SetupLogger

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "setup.log"
            logger = SetupLogger(path)
            logger(SetupEvent("preparation", "info", "Starting", "Authorization: Bearer super-secret-token"))
            text = path.read_text(encoding="utf-8")
            self.assertIn("preparation", text)
            self.assertIn("Starting", text)
            self.assertNotIn("super-secret-token", text)
            self.assertIn("[REDACTED]", text)

    def test_verified_download_emits_byte_progress(self) -> None:
        from alinacoder.product.setup_events import CancellationToken, SetupEvent

        manifest = p.PrerequisiteManifest.load(Path(__file__).parents[1] / "packaging" / "prerequisites-v0.2.json")
        payload = b"x" * 4096
        events: list[SetupEvent] = []
        asset = p.ReleaseAsset(
            "git",
            "git-for-windows/git",
            "2.55.0",
            "MinGit-2.55.0-64-bit.zip",
            "https://github.com/git-for-windows/git/releases/download/v2.55.0.windows.1/MinGit-2.55.0-64-bit.zip",
            hashlib.sha256(payload).hexdigest(),
        )
        with tempfile.TemporaryDirectory() as td:
            adapter = ObservableWindowsBootstrapAdapter(
                Path(td),
                manifest,
                download_bytes=lambda _url: payload,
                command_runner=lambda *args, **kwargs: (0, ""),
                event_sink=events.append,
                cancellation_token=CancellationToken(),
            )
            adapter.download_verified(asset, require_authenticode=False)

        progress = [event for event in events if event.kind == "progress" and event.phase == "download"]
        self.assertTrue(progress)
        self.assertEqual(progress[-1].current, len(payload))
        self.assertEqual(progress[-1].total, len(payload))

    def test_cancellation_token_stops_work_fail_closed(self) -> None:
        from alinacoder.product.setup_events import CancellationToken, SetupCancelled

        token = CancellationToken()
        token.cancel()
        with self.assertRaises(SetupCancelled):
            token.raise_if_cancelled()


if __name__ == "__main__":
    unittest.main()
