from __future__ import annotations

import os
import unittest
from unittest.mock import patch

import alinacoder.product as product


class Lot19CiBootstrapBudgetTests(unittest.TestCase):
    def test_github_actions_gets_short_model_pull_budget(self) -> None:
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}, clear=False):
            os.environ.pop("ALINACODER_MODEL_PULL_TIMEOUT_SECONDS", None)
            product._apply_ci_bootstrap_timeouts()
            self.assertEqual(os.environ["ALINACODER_MODEL_PULL_TIMEOUT_SECONDS"], "180")

    def test_explicit_timeout_is_never_overridden(self) -> None:
        with patch.dict(
            os.environ,
            {
                "GITHUB_ACTIONS": "true",
                "ALINACODER_MODEL_PULL_TIMEOUT_SECONDS": "240",
            },
            clear=False,
        ):
            product._apply_ci_bootstrap_timeouts()
            self.assertEqual(os.environ["ALINACODER_MODEL_PULL_TIMEOUT_SECONDS"], "240")

    def test_non_ci_runtime_keeps_production_default_unset(self) -> None:
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}, clear=False):
            os.environ.pop("ALINACODER_MODEL_PULL_TIMEOUT_SECONDS", None)
            product._apply_ci_bootstrap_timeouts()
            self.assertNotIn("ALINACODER_MODEL_PULL_TIMEOUT_SECONDS", os.environ)


if __name__ == "__main__":
    unittest.main()
