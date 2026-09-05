from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from alinacoder.release.acceptance import AcceptanceCatalogRunner


class Lot18AcceptanceCatalogRunnerTests(unittest.TestCase):
    def _fixture(self, root: Path) -> Path:
        tests_dir = root / "tests"
        tests_dir.mkdir()
        (tests_dir / "sample_acceptance.py").write_text(
            "import unittest\n"
            "class SampleAcceptance(unittest.TestCase):\n"
            "    def test_passes(self):\n"
            "        self.assertEqual(2 + 2, 4)\n"
            "    def test_fails(self):\n"
            "        self.assertTrue(False)\n",
            encoding="utf-8",
        )
        (root / "evidence.txt").write_text("runtime evidence anchor", encoding="utf-8")
        catalog = root / "catalog.json"
        catalog.write_text(
            json.dumps(
                {
                    "cases": [
                        {
                            "case_id": "sample.test_pass",
                            "path": "tests/sample_acceptance.py",
                            "test_name": "test_passes",
                        },
                        {
                            "case_id": "sample.test_fail",
                            "path": "tests/sample_acceptance.py",
                            "test_name": "test_fails",
                        },
                        {
                            "case_id": "sample.external",
                            "path": "evidence.txt",
                            "evidence_key": "windows.clean_install",
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )
        return catalog

    def test_runner_executes_named_tests_and_binds_external_runtime_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            catalog = self._fixture(root)
            evidences = AcceptanceCatalogRunner(root, catalog).run(
                external_evidence={"windows.clean_install": True}
            )
            by_case = {item.case_id: item for item in evidences}
            self.assertEqual(by_case["sample.test_pass"].verdict, "PASS")
            self.assertEqual(by_case["sample.test_fail"].verdict, "FAIL")
            self.assertEqual(by_case["sample.external"].verdict, "PASS")
            self.assertTrue(all(item.fresh for item in evidences))
            self.assertTrue(all(item.source for item in evidences))

    def test_missing_external_evidence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            catalog = self._fixture(root)
            evidences = AcceptanceCatalogRunner(root, catalog).run(external_evidence={})
            by_case = {item.case_id: item for item in evidences}
            self.assertEqual(by_case["sample.external"].verdict, "FAIL")


if __name__ == "__main__":
    unittest.main()
