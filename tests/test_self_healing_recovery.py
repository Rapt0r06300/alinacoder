from __future__ import annotations

import tempfile
import unittest
import urllib.error
from pathlib import Path

from alinacoder.product.prerequisites import BootstrapError, ProvenanceError
from alinacoder.product.recovery import (
    RecoveryJournal,
    RecoveryPolicy,
    backoff_seconds,
    classify_failure,
    cleanup_transients,
)
from alinacoder.product.setup_events import SetupCancelled


class SelfHealingRecoveryTests(unittest.TestCase):
    def test_policy_is_bounded_and_backoff_is_capped(self) -> None:
        policy = RecoveryPolicy(max_attempts=4, base_delay_seconds=0.25, max_delay_seconds=1.0)
        self.assertEqual(policy.max_attempts, 4)
        self.assertEqual(backoff_seconds(policy, 1), 0.25)
        self.assertEqual(backoff_seconds(policy, 2), 0.5)
        self.assertEqual(backoff_seconds(policy, 9), 1.0)

    def test_transient_network_lock_and_bootstrap_failures_are_recoverable(self) -> None:
        cases = [
            TimeoutError("network timed out"),
            urllib.error.URLError("temporary network failure"),
            PermissionError(13, "file is temporarily locked"),
            BootstrapError("prerequisite bootstrap incomplete: model_pull"),
            BootstrapError("ollama install failed with exit code 1"),
        ]
        for exc in cases:
            with self.subTest(exc=exc):
                decision = classify_failure(exc)
                self.assertTrue(decision.recoverable)
                self.assertTrue(decision.category)

    def test_security_and_user_cancellation_fail_closed(self) -> None:
        fatal_cases = [
            ProvenanceError("release repository does not match allow-list"),
            ProvenanceError("Authenticode validation failed for OllamaSetup.exe"),
            BootstrapError("Windows 10+ is required"),
            BootstrapError("requested model does not fit hardware: huge"),
            SetupCancelled("installation cancelled by user"),
        ]
        for exc in fatal_cases:
            with self.subTest(exc=exc):
                decision = classify_failure(exc)
                self.assertFalse(decision.recoverable)

    def test_sha_mismatch_can_retry_only_without_bypassing_verification(self) -> None:
        decision = classify_failure(ProvenanceError("SHA-256 mismatch for OllamaSetup.exe"))
        self.assertTrue(decision.recoverable)
        self.assertEqual(decision.category, "integrity_retry")
        self.assertIn("redownload", decision.remediations)

    def test_cleanup_removes_only_owned_transients(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cache = root / ".bootstrap-cache"
            cache.mkdir()
            staging = root / "AlinaCoder.exe.staging"
            metadata_tmp = root / "install.json.tmp"
            partial = cache / "OllamaSetup.exe.partial"
            backup = root / "AlinaCoder.exe.backup"
            user_data = root / "user-project.txt"
            for path in (staging, metadata_tmp, partial, backup, user_data):
                path.write_bytes(b"data")

            removed = cleanup_transients(root)

            self.assertFalse(staging.exists())
            self.assertFalse(metadata_tmp.exists())
            self.assertFalse(partial.exists())
            self.assertTrue(backup.exists(), "recovery must preserve the last app backup")
            self.assertTrue(user_data.exists(), "recovery must never purge arbitrary user data")
            self.assertIn(str(staging), removed)
            self.assertIn(str(partial), removed)

    def test_recovery_journal_is_resumable_and_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            journal = RecoveryJournal(root)
            journal.record_running(operation="install", attempt=1, max_attempts=4)
            first = journal.load()
            self.assertEqual(first["status"], "running")
            self.assertEqual(first["attempt"], 1)
            self.assertFalse((root / "recovery-state.json.tmp").exists())

            decision = classify_failure(TimeoutError("temporary"))
            journal.record_failure(operation="install", attempt=1, max_attempts=4, exc=TimeoutError("temporary"), decision=decision)
            failed = RecoveryJournal(root).load()
            self.assertEqual(failed["status"], "retrying")
            self.assertEqual(failed["category"], decision.category)
            self.assertTrue(failed["recoverable"])

            journal.record_ready(operation="install", attempt=2, max_attempts=4, installed_path=root / "AlinaCoder.exe")
            ready = journal.load()
            self.assertEqual(ready["status"], "ready")
            self.assertTrue(ready["ready"])
            self.assertEqual(ready["attempt"], 2)


if __name__ == "__main__":
    unittest.main()
