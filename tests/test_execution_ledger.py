from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


def _load(testcase: unittest.TestCase):
    name = "alinacoder.runtime.ledger"
    try:
        spec = importlib.util.find_spec(name)
    except ModuleNotFoundError:
        spec = None
    testcase.assertIsNotNone(spec, f"missing module: {name}")
    return importlib.import_module(name)


class ExecutionLedgerTests(unittest.TestCase):
    def test_modification_invalidates_only_affected_observations(self) -> None:
        ledger_mod = _load(self)
        with tempfile.TemporaryDirectory() as td:
            ledger = ledger_mod.ExecutionLedger(Path(td) / "ledger.sqlite")
            try:
                a = ledger.record_observation(
                    repo_state="s1", path="src/a.py", selector="full", result_digest="aaa"
                )
                b = ledger.record_observation(
                    repo_state="s1", path="src/b.py", selector="full", result_digest="bbb"
                )
                invalidated = ledger.record_modification(
                    repo_state_before="s1",
                    repo_state_after="s2",
                    paths=("src/a.py",),
                    before_digests={"src/a.py": "aaa"},
                    after_digests={"src/a.py": "ccc"},
                    origin="unit-test",
                )
                self.assertIn(a, invalidated)
                self.assertNotIn(b, invalidated)
                self.assertFalse(ledger.get_observation(a).valid)
                self.assertTrue(ledger.get_observation(b).valid)
            finally:
                ledger.close()

    def test_unchanged_digest_preserves_observation_validity(self) -> None:
        ledger_mod = _load(self)
        with tempfile.TemporaryDirectory() as td:
            ledger = ledger_mod.ExecutionLedger(Path(td) / "ledger.sqlite")
            try:
                observation = ledger.record_observation(
                    repo_state="s1", path="src/a.py", selector="full", result_digest="same"
                )
                invalidated = ledger.record_modification(
                    repo_state_before="s1",
                    repo_state_after="s2",
                    paths=("src/a.py",),
                    before_digests={"src/a.py": "same"},
                    after_digests={"src/a.py": "same"},
                    origin="format-noop",
                )
                self.assertNotIn(observation, invalidated)
                self.assertTrue(ledger.get_observation(observation).valid)
            finally:
                ledger.close()

    def test_read_only_command_can_be_reused_only_under_same_state(self) -> None:
        ledger_mod = _load(self)
        with tempfile.TemporaryDirectory() as td:
            ledger = ledger_mod.ExecutionLedger(Path(td) / "ledger.sqlite")
            try:
                ledger.record_command(
                    repo_state="s1",
                    command="git status --short",
                    arguments=(),
                    effect_class="read",
                    result_digest="clean",
                    success=True,
                )
                self.assertIsNotNone(ledger.reusable_read("git status --short", (), "s1"))
                self.assertIsNone(ledger.reusable_read("git status --short", (), "s2"))
            finally:
                ledger.close()

    def test_failed_mutation_strategy_requires_new_evidence_or_state(self) -> None:
        ledger_mod = _load(self)
        with tempfile.TemporaryDirectory() as td:
            ledger = ledger_mod.ExecutionLedger(Path(td) / "ledger.sqlite")
            try:
                ledger.record_command(
                    repo_state="s1",
                    command="patch",
                    arguments=("src/a.py",),
                    effect_class="write",
                    result_digest="failed",
                    success=False,
                    failure_class="test_failure",
                    strategy_key="replace-parser-v1",
                )
                self.assertTrue(ledger.repeated_failed_strategy("replace-parser-v1", "s1"))
                self.assertFalse(ledger.repeated_failed_strategy("replace-parser-v1", "s2"))
            finally:
                ledger.close()

    def test_ledger_persists_restart_and_inform_summary(self) -> None:
        ledger_mod = _load(self)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.sqlite"
            ledger = ledger_mod.ExecutionLedger(path)
            observation = ledger.record_observation(
                repo_state="s1", path="README.md", selector="full", result_digest="abc"
            )
            ledger.record_command(
                repo_state="s1",
                command="python -m unittest",
                arguments=(),
                effect_class="read",
                result_digest="fail",
                success=False,
                failure_class="tests_failed",
                strategy_key="verify",
            )
            ledger.close()

            reopened = ledger_mod.ExecutionLedger(path)
            try:
                self.assertTrue(reopened.get_observation(observation).valid)
                summary = reopened.inform("s1")
                self.assertGreaterEqual(summary.valid_observation_count, 1)
                self.assertIn("tests_failed", summary.failure_classes)
            finally:
                reopened.close()


if __name__ == "__main__":
    unittest.main()
