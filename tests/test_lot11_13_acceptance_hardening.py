from __future__ import annotations

import unittest

from alinacoder.orchestration.core import (
    AgentSpec,
    SpecialistRegistry,
    TopologyValueAudit,
)
from alinacoder.resources.core import (
    HardwareProfile,
    LocalModel,
    PerformanceBudget,
    PerformanceSnapshot,
    ResourceController,
    ResourceMode,
    RuntimePerformanceAudit,
)
from alinacoder.self_improvement.core import (
    CandidateMetrics,
    CorrectionRuleFactory,
    EvaluationPartitions,
    EvolutionCandidate,
    EvolutionGate,
    VerifierEvidence,
)


class Lot11AcceptanceHardeningTests(unittest.TestCase):
    def test_specialist_selection_prefers_independent_failure_domains(self) -> None:
        registry = SpecialistRegistry(
            [
                AgentSpec("a", "code", "lineage-a", "provider-a", frozenset({"code"}), "fd-a"),
                AgentSpec("b", "code", "lineage-b", "provider-b", frozenset({"code"}), "fd-b"),
                AgentSpec("c", "code", "lineage-a", "provider-c", frozenset({"code"}), "fd-c"),
            ]
        )
        selected = registry.select_diverse("code", desired=2)
        self.assertEqual(len(selected), 2)
        self.assertEqual(len({agent.lineage for agent in selected}), 2)
        self.assertEqual(len({agent.failure_domain for agent in selected}), 2)

    def test_topology_without_proven_terminal_gain_is_disabled(self) -> None:
        audit = TopologyValueAudit(min_terminal_gain=0.03)
        result = audit.observe(
            topology="parallel",
            baseline_terminal_success=0.80,
            topology_terminal_success=0.82,
            latency_penalty=0.01,
            resource_penalty=0.01,
        )
        self.assertFalse(result.enabled)
        self.assertEqual(result.verdict, "DISABLE_NO_PROVEN_VALUE")
        self.assertFalse(audit.is_enabled("parallel"))

    def test_topology_with_measured_net_gain_remains_enabled(self) -> None:
        audit = TopologyValueAudit(min_terminal_gain=0.03)
        result = audit.observe(
            topology="council",
            baseline_terminal_success=0.60,
            topology_terminal_success=0.78,
            latency_penalty=0.03,
            resource_penalty=0.02,
        )
        self.assertTrue(result.enabled)
        self.assertEqual(result.verdict, "KEEP_PROVEN_VALUE")


class Lot12AcceptanceHardeningTests(unittest.TestCase):
    def test_evaluation_partitions_reject_holdout_contamination(self) -> None:
        with self.assertRaises(ValueError):
            EvaluationPartitions(
                visible_ids=frozenset({"case-1", "case-2"}),
                validation_ids=frozenset({"case-3"}),
                hidden_ids=frozenset({"case-2", "case-4"}),
            )

    def test_self_authored_verifier_cannot_be_sole_promotion_authority(self) -> None:
        gate = EvolutionGate(0.01)
        candidate = EvolutionCandidate("candidate-1", "router", "reduce routing failures", lineage="lineage-x")
        before = CandidateMetrics(0.60, 0.60, 0.60)
        after = CandidateMetrics(0.80, 0.80, 0.80)
        evidence = [VerifierEvidence("self-check", "lineage-x", sealed=False, verdict="PASS")]
        self.assertEqual(
            gate.evaluate_certified(candidate, before, after, evidence),
            "REJECT_CIRCULAR_AUTHORITY",
        )

    def test_independent_sealed_verifier_can_certify_proven_candidate(self) -> None:
        gate = EvolutionGate(0.01)
        candidate = EvolutionCandidate("candidate-2", "skill", "improve deterministic replay", lineage="lineage-x")
        before = CandidateMetrics(0.60, 0.60, 0.60)
        after = CandidateMetrics(0.75, 0.75, 0.75)
        evidence = [VerifierEvidence("sealed-acceptance", "lineage-y", sealed=True, verdict="PASS")]
        self.assertEqual(gate.evaluate_certified(candidate, before, after, evidence), "PROMOTE")

    def test_durable_correction_rule_requires_evidence_and_test_proof(self) -> None:
        factory = CorrectionRuleFactory()
        with self.assertRaises(ValueError):
            factory.create_validated(
                "rule-1",
                "always target main",
                source="user",
                scope="git",
                evidence=(),
                tests_passed=True,
            )
        rule = factory.create_validated(
            "rule-1",
            "always target main",
            source="user",
            scope="git",
            evidence=("conversation:user-correction", "test:test_git_main"),
            tests_passed=True,
        )
        self.assertTrue(rule.active)
        factory.revoke("rule-1")
        self.assertFalse(factory.get("rule-1").active)


class Lot13AcceptanceHardeningTests(unittest.TestCase):
    def test_resource_controller_cooldown_prevents_mode_flapping(self) -> None:
        controller = ResourceController(
            mode=ResourceMode.BALANCED,
            pressure_samples=1,
            recovery_samples=1,
            cooldown_samples=2,
        )
        self.assertEqual(controller.observe_pressure(0.95), ResourceMode.CONSERVATIVE)
        self.assertEqual(controller.observe_pressure(0.10), ResourceMode.CONSERVATIVE)
        self.assertEqual(controller.observe_pressure(0.10), ResourceMode.BALANCED)

    def test_versioned_performance_budget_rejects_runtime_regression(self) -> None:
        budget = PerformanceBudget(
            version="v0.2",
            startup_ms=1500,
            idle_ram_mb=350,
            idle_cpu_percent=5.0,
            ui_action_p95_ms=150,
        )
        audit = RuntimePerformanceAudit(budget)
        good = PerformanceSnapshot(1200, 300, 3.0, 100)
        bad = PerformanceSnapshot(1800, 300, 3.0, 100)
        self.assertTrue(audit.evaluate(good).passed)
        report = audit.evaluate(bad)
        self.assertFalse(report.passed)
        self.assertIn("startup_ms", report.violations)

    def test_hardware_stress_audit_rejects_model_that_exceeds_headroom(self) -> None:
        budget = PerformanceBudget("v0.2", 1500, 350, 5.0, 150)
        audit = RuntimePerformanceAudit(budget)
        hardware = HardwareProfile(ram_gb=16, vram_gb=8, cpu_cores=8, gpu_name="GPU")
        oversized = LocalModel("too-big", required_ram_gb=30, required_vram_gb=16, capability=1.0)
        result = audit.audit_model_fit(hardware, oversized, headroom_ratio=0.9)
        self.assertFalse(result.passed)
        self.assertIn("model_fit", result.violations)


if __name__ == "__main__":
    unittest.main()
