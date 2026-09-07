from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from alinacoder.product import installer
from alinacoder.product.prerequisites import BootstrapError, BootstrapReport, ProvenanceError
from alinacoder.product.recovery import RecoveryJournal, RecoveryPolicy
from alinacoder.product.setup_events import CancellationToken, SetupCancelled


class _Bootstrapper:
    def __init__(self, report: BootstrapReport | None = None, failure: BaseException | None = None) -> None:
        self.adapter = object()
        self._report = report
        self._failure = failure

    def run(self, *, online: bool, model_override: str | None = None) -> BootstrapReport:
        if self._failure is not None:
            raise self._failure
        assert self._report is not None
        return self._report


class SelfHealingRunnerTests(unittest.TestCase):
    @staticmethod
    def _report(ready: bool) -> BootstrapReport:
        return BootstrapReport(
            ready=ready,
            selected_model="qwen3:0.6b",
            actions=(),
            blockers=() if ready else ("model_pull",),
            state=None,
        )

    def test_recoverable_failure_is_repaired_automatically_without_manual_retry(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.exe"
            source.write_bytes(b"NEW")
            target = root / "AlinaCoder.exe"
            target.write_bytes(b"OLD")
            reports = [self._report(False), self._report(True)]
            factory_calls: list[int] = []
            events = []

            def factory():
                factory_calls.append(len(factory_calls) + 1)
                return _Bootstrapper(reports.pop(0))

            installed = installer.run_self_healing_operation(
                root,
                operation="upgrade",
                source_exe=source,
                bootstrapper_factory=factory,
                policy=RecoveryPolicy(max_attempts=3, base_delay_seconds=0, max_delay_seconds=0),
                event_sink=events.append,
                sleep=lambda _: None,
            )

            self.assertEqual(installed, target)
            self.assertEqual(target.read_bytes(), b"NEW")
            self.assertEqual(factory_calls, [1, 2])
            journal = json.loads((root / "recovery-state.json").read_text(encoding="utf-8"))
            self.assertEqual(journal["status"], "ready")
            self.assertEqual(journal["attempt"], 2)
            self.assertTrue(any(event.kind == "retry" for event in events))

    def test_exhausted_recovery_preserves_last_healthy_binary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.exe"
            source.write_bytes(b"NEW")
            target = root / "AlinaCoder.exe"
            target.write_bytes(b"OLD")
            calls = 0

            def factory():
                nonlocal calls
                calls += 1
                return _Bootstrapper(self._report(False))

            with self.assertRaises(BootstrapError):
                installer.run_self_healing_operation(
                    root,
                    operation="repair",
                    source_exe=source,
                    bootstrapper_factory=factory,
                    policy=RecoveryPolicy(max_attempts=2, base_delay_seconds=0, max_delay_seconds=0),
                    sleep=lambda _: None,
                )

            self.assertEqual(calls, 2)
            self.assertEqual(target.read_bytes(), b"OLD")
            journal = RecoveryJournal(root).load()
            self.assertEqual(journal["status"], "failed")
            self.assertEqual(journal["attempt"], 2)
            self.assertTrue(journal["recoverable"])

    def test_fatal_provenance_failure_is_never_blindly_retried(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.exe"
            source.write_bytes(b"NEW")
            calls = 0

            def factory():
                nonlocal calls
                calls += 1
                return _Bootstrapper(failure=ProvenanceError("Authenticode validation failed for OllamaSetup.exe"))

            with self.assertRaises(ProvenanceError):
                installer.run_self_healing_operation(
                    root,
                    operation="install",
                    source_exe=source,
                    bootstrapper_factory=factory,
                    policy=RecoveryPolicy(max_attempts=4, base_delay_seconds=0, max_delay_seconds=0),
                    sleep=lambda _: None,
                )

            self.assertEqual(calls, 1)
            journal = RecoveryJournal(root).load()
            self.assertEqual(journal["category"], "security_fatal")
            self.assertFalse(journal["recoverable"])

    def test_cancelled_setup_stops_before_attempting_repair(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.exe"
            source.write_bytes(b"NEW")
            token = CancellationToken()
            token.cancel()
            calls = 0

            def factory():
                nonlocal calls
                calls += 1
                return _Bootstrapper(self._report(True))

            with self.assertRaises(SetupCancelled):
                installer.run_self_healing_operation(
                    root,
                    operation="install",
                    source_exe=source,
                    bootstrapper_factory=factory,
                    cancellation_token=token,
                    sleep=lambda _: None,
                )
            self.assertEqual(calls, 0)

    def test_interrupted_journal_is_safely_resumed_by_next_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.exe"
            source.write_bytes(b"NEW")
            (root / "AlinaCoder.exe.staging").write_bytes(b"PARTIAL")
            journal = RecoveryJournal(root, sleep=lambda _: None)
            journal.record_running(operation="install", attempt=3, max_attempts=4)

            installed = installer.run_self_healing_operation(
                root,
                operation="install",
                source_exe=source,
                bootstrapper_factory=lambda: _Bootstrapper(self._report(True)),
                policy=RecoveryPolicy(max_attempts=2, base_delay_seconds=0, max_delay_seconds=0),
                sleep=lambda _: None,
            )

            self.assertEqual(installed.read_bytes(), b"NEW")
            self.assertFalse((root / "AlinaCoder.exe.staging").exists())
            resumed = RecoveryJournal(root).load()
            self.assertEqual(resumed["status"], "ready")
            self.assertTrue(resumed["ready"])


if __name__ == "__main__":
    unittest.main()
