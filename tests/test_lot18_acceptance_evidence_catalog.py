from __future__ import annotations

import unittest
from pathlib import Path

from alinacoder.release.acceptance import AcceptanceCoverageCatalog, SpecAcceptanceMatrix


class Lot18AcceptanceEvidenceCatalogTests(unittest.TestCase):
    def test_every_required_case_maps_to_existing_named_evidence(self) -> None:
        root = Path(__file__).parents[1]
        matrix = SpecAcceptanceMatrix()
        report = AcceptanceCoverageCatalog(root).validate(matrix)
        self.assertTrue(report.complete, report.gaps)
        self.assertEqual(report.gaps, ())
        self.assertEqual(report.covered_cases, len(matrix.required_case_ids()))
        for row in report.rows:
            self.assertTrue((root / row.path).exists(), row.case_id)
            self.assertTrue(row.test_name or row.evidence_key, row.case_id)

    def test_catalog_has_no_unknown_or_duplicate_case_ids(self) -> None:
        root = Path(__file__).parents[1]
        matrix = SpecAcceptanceMatrix()
        report = AcceptanceCoverageCatalog(root).validate(matrix)
        self.assertEqual(report.unknown, ())
        self.assertEqual(report.duplicates, ())


if __name__ == "__main__":
    unittest.main()
