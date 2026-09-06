from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


class Lot19CiTransportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_main_ci_cancels_obsolete_runs(self) -> None:
        self.assertIn("concurrency:", self.workflow)
        self.assertIn("cancel-in-progress: true", self.workflow)

    def test_ollama_installer_is_prefetched_by_exact_release_digest(self) -> None:
        self.assertIn("Resolve official Ollama asset", self.workflow)
        self.assertIn("gh api repos/ollama/ollama/releases/latest", self.workflow)
        self.assertIn("OllamaSetup.exe", self.workflow)
        self.assertIn("digest", self.workflow.lower())
        self.assertIn("Get-FileHash", self.workflow)
        self.assertIn("Get-AuthenticodeSignature", self.workflow)
        self.assertIn("actions/cache@0057852bfaa89a56745cba8c7296529d2fc39830", self.workflow)
        self.assertIn("gh release download", self.workflow)
        self.assertIn("ALINACODER_PREREQ_CACHE_DIR", self.workflow)

    def test_lot19_has_a_hard_step_timeout(self) -> None:
        marker = "- name: LOT 19 clean Windows bootstrap E2E and lifecycle matrix"
        start = self.workflow.index(marker)
        tail = self.workflow[start : start + 500]
        self.assertIn("timeout-minutes:", tail)


if __name__ == "__main__":
    unittest.main()
