from __future__ import annotations

import unittest

from alinacoder.release.acceptance import AcceptanceCaseEvidence, SpecAcceptanceMatrix


class Lot18FullAcceptanceMatrixTests(unittest.TestCase):
    def test_matrix_covers_every_spec_section_18_family(self) -> None:
        matrix = SpecAcceptanceMatrix()
        self.assertEqual(
            set(matrix.families),
            {"conversation", "repository_engineering", "control_safety", "provider_fabric", "continuity", "desktop_ux"},
        )
        self.assertGreaterEqual(len(matrix.required_case_ids()), 43)
        self.assertIn("conversation.evolving_intent", matrix.required_case_ids())
        self.assertIn("provider_fabric.zero_paid_calls", matrix.required_case_ids())
        self.assertIn("continuity.recovery_without_duplicate_effect", matrix.required_case_ids())
        self.assertIn("desktop_ux.all_stop", matrix.required_case_ids())

    def test_matrix_fails_closed_when_any_required_case_is_missing_or_stale(self) -> None:
        matrix = SpecAcceptanceMatrix()
        evidence = [
            AcceptanceCaseEvidence(case_id, "PASS", fresh=True, source="sealed-ci")
            for case_id in matrix.required_case_ids()
        ]
        self.assertTrue(matrix.evaluate(evidence).passed)
        missing = evidence[:-1]
        report = matrix.evaluate(missing)
        self.assertFalse(report.passed)
        self.assertEqual(report.missing, (evidence[-1].case_id,))
        stale = list(evidence)
        stale[0] = AcceptanceCaseEvidence(stale[0].case_id, "PASS", fresh=False, source="old-run")
        report = matrix.evaluate(stale)
        self.assertFalse(report.passed)
        self.assertIn(stale[0].case_id, report.invalid)

    def test_unknown_or_failed_case_cannot_be_counted_as_coverage(self) -> None:
        matrix = SpecAcceptanceMatrix()
        evidence = [
            AcceptanceCaseEvidence(case_id, "PASS", fresh=True, source="sealed-ci")
            for case_id in matrix.required_case_ids()
        ]
        evidence[3] = AcceptanceCaseEvidence(evidence[3].case_id, "FAIL", fresh=True, source="sealed-ci")
        evidence.append(AcceptanceCaseEvidence("made.up.case", "PASS", fresh=True, source="sealed-ci"))
        report = matrix.evaluate(evidence)
        self.assertFalse(report.passed)
        self.assertIn(evidence[3].case_id, report.invalid)
        self.assertIn("made.up.case", report.unknown)


if __name__ == "__main__":
    unittest.main()
