from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product import prerequisites as p


class Lot19ModelPullResilienceTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.manifest = p.PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")

    def _adapter(self, td: str, runner, sleeps: list[float]):
        adapter = p.WindowsBootstrapAdapter(
            Path(td),
            self.manifest,
            command_runner=runner,
            sleep=sleeps.append,
        )
        adapter._ollama_executable = lambda: Path("C:/Ollama/ollama.exe")  # type: ignore[method-assign]
        adapter.detect_inventory = lambda: p.ComponentInventory(  # type: ignore[method-assign]
            git=None,
            ollama=None,
            models=frozenset({"qwen3:0.6b"}),
        )
        return adapter

    def test_model_pull_retries_timeout_and_transient_failure_with_bounded_attempts(self) -> None:
        calls: list[tuple[list[str], int]] = []
        sleeps: list[float] = []
        outcomes: list[object] = [
            subprocess.TimeoutExpired(cmd="ollama pull qwen3:0.6b", timeout=600),
            (1, "temporary registry failure"),
            (0, "success"),
        ]

        def runner(args: list[str], *, timeout: int = 300):
            calls.append((list(args), timeout))
            outcome = outcomes.pop(0)
            if isinstance(outcome, BaseException):
                raise outcome
            return outcome

        with tempfile.TemporaryDirectory() as td:
            adapter = self._adapter(td, runner, sleeps)
            self.assertTrue(adapter.pull_model("http://127.0.0.1:11434", "qwen3:0.6b"))

        self.assertEqual(len(calls), 3)
        self.assertTrue(all(timeout == 600 for _, timeout in calls))
        self.assertEqual(sleeps, [1.0, 2.0])

    def test_model_pull_timeout_can_be_shortened_for_ci_without_changing_default(self) -> None:
        calls: list[int] = []

        def runner(args: list[str], *, timeout: int = 300):
            calls.append(timeout)
            return 0, "success"

        with tempfile.TemporaryDirectory() as td, patch.dict(
            "os.environ",
            {"ALINACODER_MODEL_PULL_TIMEOUT_SECONDS": "180"},
            clear=False,
        ):
            adapter = self._adapter(td, runner, [])
            self.assertTrue(adapter.pull_model("http://127.0.0.1:11434", "qwen3:0.6b"))

        self.assertEqual(calls, [180])

    def test_model_pull_timeout_is_safely_clamped_and_invalid_value_falls_back(self) -> None:
        calls: list[int] = []

        def runner(args: list[str], *, timeout: int = 300):
            calls.append(timeout)
            return 0, "success"

        with tempfile.TemporaryDirectory() as td:
            with patch.dict("os.environ", {"ALINACODER_MODEL_PULL_TIMEOUT_SECONDS": "5"}, clear=False):
                adapter = self._adapter(td, runner, [])
                self.assertTrue(adapter.pull_model("http://127.0.0.1:11434", "qwen3:0.6b"))
            with patch.dict("os.environ", {"ALINACODER_MODEL_PULL_TIMEOUT_SECONDS": "not-a-number"}, clear=False):
                adapter = self._adapter(td, runner, [])
                self.assertTrue(adapter.pull_model("http://127.0.0.1:11434", "qwen3:0.6b"))

        self.assertEqual(calls, [60, 600])


if __name__ == "__main__":
    unittest.main()
