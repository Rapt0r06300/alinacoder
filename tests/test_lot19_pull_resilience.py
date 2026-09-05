from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from alinacoder.product import prerequisites as p


class Lot19ModelPullResilienceTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.manifest = p.PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")

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

            self.assertTrue(adapter.pull_model("http://127.0.0.1:11434", "qwen3:0.6b"))

        self.assertEqual(len(calls), 3)
        self.assertTrue(all(timeout == 600 for _, timeout in calls))
        self.assertEqual(sleeps, [1.0, 2.0])


if __name__ == "__main__":
    unittest.main()
