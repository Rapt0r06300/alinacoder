from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product import installer


class Lot19CiFailureCodeTests(unittest.TestCase):
    def _install_dir(self, blocker: str) -> Path:
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        (root / "install.json").write_text(
            json.dumps({"bootstrap_blockers": [blocker]}),
            encoding="utf-8",
        )
        return root

    def test_non_ci_failure_stays_generic(self) -> None:
        root = self._install_dir("ollama_install")
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}, clear=False):
            self.assertEqual(installer._ci_failure_exit_code(root), 2)

    def test_ci_failure_code_identifies_first_bootstrap_blocker(self) -> None:
        expected = {
            "git_install": 20,
            "git_upgrade": 20,
            "git_health": 21,
            "ollama_install": 30,
            "ollama_upgrade": 30,
            "ollama_version": 31,
            "ollama_health": 32,
            "model_pull": 40,
            "model_smoke": 41,
        }
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}, clear=False):
            for blocker, code in expected.items():
                with self.subTest(blocker=blocker):
                    self.assertEqual(installer._ci_failure_exit_code(self._install_dir(blocker)), code)

    def test_missing_or_unknown_receipt_stays_generic(self) -> None:
        with tempfile.TemporaryDirectory() as td, patch.dict(
            os.environ, {"GITHUB_ACTIONS": "true"}, clear=False
        ):
            root = Path(td)
            self.assertEqual(installer._ci_failure_exit_code(root), 2)
            (root / "install.json").write_text(
                json.dumps({"bootstrap_blockers": ["unexpected"]}), encoding="utf-8"
            )
            self.assertEqual(installer._ci_failure_exit_code(root), 2)


if __name__ == "__main__":
    unittest.main()
