from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from alinacoder.release.acceptance import AcceptanceCoverageCatalog, SpecAcceptanceMatrix


_REQUIRED = {
    "desktop_ux.live_activity_persistence",
    "desktop_ux.safe_activity_redaction",
    "desktop_ux.observable_run_lifecycle",
    "desktop_ux.responsive_message_execution",
    "desktop_ux.activity_first_progressive_disclosure",
}


class LiveActivityReleaseContractTests(unittest.TestCase):
    def test_release_matrix_requires_live_workbench_cases(self) -> None:
        required = set(SpecAcceptanceMatrix().required_case_ids())
        self.assertTrue(_REQUIRED.issubset(required))

    def test_release_catalog_maps_every_live_workbench_case_to_real_test(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        report = AcceptanceCoverageCatalog(repo_root).validate(SpecAcceptanceMatrix())
        rows = {row.case_id: row for row in report.rows}
        self.assertTrue(_REQUIRED.issubset(rows))
        for case_id in _REQUIRED:
            row = rows[case_id]
            self.assertTrue(row.path.startswith("tests/"))
            self.assertTrue(row.test_name)
            source = (repo_root / row.path).read_text(encoding="utf-8")
            self.assertIn(f"def {row.test_name}(", source)


if __name__ == "__main__":
    unittest.main()
