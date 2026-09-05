from __future__ import annotations

import unittest
from pathlib import Path

from alinacoder.evaluation.torture import FailureCard, IntegratedTortureHarness, TortureLab
from alinacoder.release.acceptance import (
    AcceptanceCaseEvidence,
    AcceptanceEvidence,
    FinalAcceptanceGate,
    RuleTraceabilityBuilder,
    SpecAcceptanceMatrix,
)


class Lot17IntegratedTortureTests(unittest.TestCase):
    def test_integrated_campaign_injects_real_faults_and_contains_known_critical_cases(self) -> None:
        report = IntegratedTortureHarness().run()
        names = {result.name for result in report.results}
        self.assertTrue(
            {
                "stale_state",
                "duplicate_effect",
                "provider_loss",
                "handoff_storm",
                "resource_pressure",
                "prompt_injection",
                "concurrency_race",
                "ui_interrupt",
                "flaky_verifier",
                "malicious_package",
            }.issubset(names)
        )
        self.assertTrue(all(result.detected for result in report.results))
        self.assertTrue(all(card.reproduced for card in report.failure_cards))
        self.assertTrue(all(card.contained for card in report.failure_cards))
        self.assertTrue(report.readiness.ready)
        self.assertEqual(report.readiness.critical_failures, 0)

    def test_uncontained_critical_fault_fails_readiness_closed(self) -> None:
        card = FailureCard("seed", "authority", "no escalation", True, True, contained=False)
        readiness = TortureLab().evaluate([card], passed_checks=99, total_checks=100)
        self.assertFalse(readiness.ready)
        self.assertGreater(readiness.critical_failures, 0)

    def test_integrated_campaign_is_deterministic(self) -> None:
        first = IntegratedTortureHarness(seed="lot17-fixed").run()
        second = IntegratedTortureHarness(seed="lot17-fixed").run()
        self.assertEqual(
            [card.fingerprint for card in first.failure_cards],
            [card.fingerprint for card in second.failure_cards],
        )


class Lot18TraceabilityTests(unittest.TestCase):
    def test_every_active_rule_id_maps_to_existing_code_test_and_evidence_family(self) -> None:
        root = Path(__file__).parents[1]
        report = RuleTraceabilityBuilder(root).build()
        self.assertTrue(report.complete, report.unknown_families)
        self.assertGreater(report.rule_count, 0)
        self.assertEqual(report.unknown_families, ())
        for row in report.rows:
            self.assertTrue((root / row.code_path).exists(), row.rule_id)
            self.assertTrue((root / row.test_path).exists(), row.rule_id)
            self.assertTrue(row.evidence_name)


class Lot18FinalGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).parents[1]
        self.trace = RuleTraceabilityBuilder(self.root).build()
        self.commit = "abc123"
        self.artifact = "f" * 64
        self.required = ("core", "desktop_e2e", "torture", "final_audit")
        self.matrix = SpecAcceptanceMatrix()

    def evidence(self, name: str, *, fresh: bool = True, commit: str | None = None, independent: bool = False) -> AcceptanceEvidence:
        return AcceptanceEvidence(
            name,
            "PASS",
            commit or self.commit,
            self.artifact,
            fresh,
            source="sealed-ci" if independent else "runtime",
            independent=independent,
        )

    def matrix_evidence(self) -> list[AcceptanceCaseEvidence]:
        return [AcceptanceCaseEvidence(case_id, "PASS", True, "sealed-ci") for case_id in self.matrix.required_case_ids()]

    def test_final_gate_rejects_stale_or_wrong_commit_proof(self) -> None:
        gate = FinalAcceptanceGate(self.trace, self.required, commit_sha=self.commit, artifact_sha256=self.artifact, acceptance_matrix=self.matrix)
        evidences = [
            self.evidence("core"),
            self.evidence("desktop_e2e", fresh=False),
            self.evidence("torture"),
            self.evidence("final_audit", independent=True),
        ]
        result = gate.evaluate(evidences, self.matrix_evidence())
        self.assertFalse(result.runtime_v0_2_ready)
        self.assertIn("desktop_e2e", result.missing_or_invalid_evidence)

    def test_final_gate_requires_independent_final_audit(self) -> None:
        gate = FinalAcceptanceGate(self.trace, self.required, commit_sha=self.commit, artifact_sha256=self.artifact, acceptance_matrix=self.matrix)
        evidences = [self.evidence(name) for name in self.required]
        result = gate.evaluate(evidences, self.matrix_evidence())
        self.assertFalse(result.runtime_v0_2_ready)
        self.assertIn("independent_final_audit", result.failures)

    def test_final_gate_rejects_incomplete_spec_acceptance_matrix(self) -> None:
        gate = FinalAcceptanceGate(self.trace, self.required, commit_sha=self.commit, artifact_sha256=self.artifact, acceptance_matrix=self.matrix)
        evidences = [
            self.evidence("core"), self.evidence("desktop_e2e"), self.evidence("torture"),
            self.evidence("final_audit", independent=True),
        ]
        matrix_evidence = self.matrix_evidence()[:-1]
        result = gate.evaluate(evidences, matrix_evidence)
        self.assertFalse(result.runtime_v0_2_ready)
        self.assertIn("incomplete_spec_acceptance_matrix", result.failures)

    def test_final_gate_fails_closed_when_acceptance_matrix_is_not_bound(self) -> None:
        gate = FinalAcceptanceGate(
            self.trace,
            self.required,
            commit_sha=self.commit,
            artifact_sha256=self.artifact,
        )
        evidences = [
            self.evidence("core"), self.evidence("desktop_e2e"), self.evidence("torture"),
            self.evidence("final_audit", independent=True),
        ]
        result = gate.evaluate(evidences)
        self.assertFalse(result.runtime_v0_2_ready)
        self.assertIn("missing_spec_acceptance_matrix", result.failures)

    def test_final_gate_can_emit_ready_only_with_complete_fresh_bound_proof(self) -> None:
        gate = FinalAcceptanceGate(self.trace, self.required, commit_sha=self.commit, artifact_sha256=self.artifact, acceptance_matrix=self.matrix)
        evidences = [
            self.evidence("core"),
            self.evidence("desktop_e2e"),
            self.evidence("torture"),
            self.evidence("final_audit", independent=True),
        ]
        result = gate.evaluate(evidences, self.matrix_evidence())
        self.assertTrue(result.runtime_v0_2_ready)
        self.assertEqual(result.missing_or_invalid_evidence, ())
        self.assertEqual(result.failures, ())


if __name__ == "__main__":
    unittest.main()
