from __future__ import annotations

from pathlib import Path
import unittest

from alinacoder.release.acceptance import AcceptanceCoverageCatalog, SpecAcceptanceMatrix


class CognitiveReleaseGateTests(unittest.TestCase):
    REQUIRED = {
        "provider_fabric.anonymous_kilo_free",
        "provider_fabric.measured_capability_routing",
        "provider_fabric.quota_persistence_reset",
        "conversation.causal_correction",
        "conversation.thousand_case_replay",
        "repository_engineering.execution_ledger_invalidation",
        "repository_engineering.phase_aware_memory",
        "repository_engineering.adaptive_context_folding",
        "control_safety.critic_independence",
        "control_safety.verified_learning_quarantine",
        "desktop_ux.cognitive_route_trace",
    }

    def test_acceptance_matrix_requires_every_cognitive_architecture_gate(self) -> None:
        required = set(SpecAcceptanceMatrix().required_case_ids())
        self.assertTrue(self.REQUIRED.issubset(required), self.REQUIRED - required)

    def test_default_acceptance_coverage_maps_every_new_gate_to_executable_proof(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        report = AcceptanceCoverageCatalog(repo_root).validate(SpecAcceptanceMatrix())
        self.assertTrue(report.complete, report.gaps)
        rows = {row.case_id: row for row in report.rows}
        for case_id in self.REQUIRED:
            self.assertIn(case_id, rows)
            row = rows[case_id]
            self.assertTrue(row.path or row.evidence_key)
            if row.path:
                self.assertTrue((repo_root / row.path).is_file())
                self.assertTrue(row.test_name)


if __name__ == "__main__":
    unittest.main()
