from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product.ci_exit_codes import translate_setup_exit_code


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
            self.assertEqual(
                translate_setup_exit_code(2, ["--quiet", "--install-dir", str(root)]),
                2,
            )

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
                    root = self._install_dir(blocker)
                    self.assertEqual(
                        translate_setup_exit_code(2, ["--quiet", "--install-dir", str(root)]),
                        code,
                    )

    def test_success_missing_or_unknown_receipt_stays_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as td, patch.dict(
            os.environ, {"GITHUB_ACTIONS": "true"}, clear=False
        ):
            root = Path(td)
            args = ["--quiet", "--install-dir", str(root)]
            self.assertEqual(translate_setup_exit_code(0, args), 0)
            self.assertEqual(translate_setup_exit_code(2, args), 2)
            (root / "install.json").write_text(
                json.dumps({"bootstrap_blockers": ["unexpected"]}), encoding="utf-8"
            )
            self.assertEqual(translate_setup_exit_code(2, args), 2)


if __name__ == "__main__":
    unittest.main()
