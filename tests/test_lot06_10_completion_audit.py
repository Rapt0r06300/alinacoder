from __future__ import annotations

import unittest

from alinacoder.conversation.advanced import (
    ConversationContextGraph,
    ConversationFailure,
    ConversationFailureReplay,
    MicroTurnStream,
    RepairOp,
    SemanticPrefetchPolicy,
    TechnicalFrenchNormalizer,
)
from alinacoder.engineering.assurance import (
    BehavioralContract,
    BehavioralContractEvaluator,
    DependencyMigrationEvidence,
    SelfCorrectionPolicy,
    SemanticRegressionDetector,
)
from alinacoder.intelligence_mesh.control import (
    CircuitBreaker,
    CircuitState,
    EnrollmentState,
    ProtocolAdapter,
    ProviderEnrollment,
    QuotaPortfolio,
    SwitchHysteresis,
    TaskAffinityLease,
)
from alinacoder.tools.control import (
    CapabilityProjection,
    DeterministicReplayLedger,
    GovernedToolExecutor,
    MCPManifest,
    MCPLifecycle,
)
from alinacoder.tools import ToolCall, ToolRuntime, ToolSchema
from alinacoder.verification.redteam import (
    EvidenceGapMiner,
    EvidenceType,
    RedTeamVerifierLoop,
    VerifierIntegrityGuard,
)


class Lot06CompletionAuditTests(unittest.TestCase):
    def test_context_branches_and_repairs_do_not_pollute_main(self) -> None:
        graph = ConversationContextGraph()
        graph.set_fact("main", "target", "a.py")
        graph.fork("aside")
        graph.apply_repair("aside", RepairOp.REPLACE, "target", "b.py")
        graph.apply_repair("aside", RepairOp.EXTEND, "constraint", "preserve API")
        self.assertEqual(graph.branches["main"].facts["target"], "a.py")
        self.assertEqual(graph.branches["aside"].facts["target"], "b.py")
        self.assertEqual(graph.branches["aside"].facts["constraint"], "preserve API")

    def test_partial_stream_never_authorizes_mutation_and_prefetch_stays_read_only(self) -> None:
        stream = MicroTurnStream()
        partial = stream.push("supprime le...", stable=False)
        committed = stream.commit_user_turn("supprime le cache")
        self.assertFalse(partial.may_authorize_mutation)
        self.assertTrue(committed.may_authorize_mutation)
        policy = SemanticPrefetchPolicy()
        self.assertTrue(policy.may_prefetch("read", turn_stable=False))
        self.assertFalse(policy.may_prefetch("write", turn_stable=False))
        self.assertTrue(policy.may_prefetch("write", turn_stable=True))

    def test_technical_french_normalization_and_failure_replay(self) -> None:
        self.assertEqual(TechnicalFrenchNormalizer().normalize("ouvre le ficher Gitub"), "ouvre le fichier github")
        replay = ConversationFailureReplay()
        replay.record(ConversationFailure("t1", "reference", "corrige ça", "corrige diff-7"))
        self.assertEqual(replay.cases("reference")[0].corrected_meaning, "corrige diff-7")


class Lot07CompletionAuditTests(unittest.TestCase):
    def test_quota_reservation_is_atomic_from_router_perspective(self) -> None:
        portfolio = QuotaPortfolio()
        portfolio.set_quota("p", "m", 2)
        self.assertTrue(portfolio.reserve("p", "m"))
        self.assertEqual(portfolio.available("p", "m"), 1)
        self.assertTrue(portfolio.reserve("p", "m"))
        self.assertFalse(portfolio.reserve("p", "m"))
        portfolio.release("p", "m", consumed=True)
        self.assertEqual(portfolio.available("p", "m"), 0)

    def test_circuit_breaker_and_switch_hysteresis_prevent_thrashing(self) -> None:
        breaker = CircuitBreaker(failure_threshold=2)
        breaker.record_failure()
        self.assertEqual(breaker.state, CircuitState.CLOSED)
        breaker.record_failure()
        self.assertEqual(breaker.state, CircuitState.OPEN)
        breaker.probe()
        self.assertEqual(breaker.state, CircuitState.HALF_OPEN)
        breaker.record_success()
        self.assertEqual(breaker.state, CircuitState.CLOSED)
        lease = TaskAffinityLease("task", "family", 10, minimum_dwell=3)
        self.assertFalse(lease.dwell_satisfied(12))
        self.assertTrue(lease.dwell_satisfied(13))
        hysteresis = SwitchHysteresis(0.2, 2)
        self.assertFalse(hysteresis.permits(expected_gain=0.3, consecutive_evidence=1))
        self.assertTrue(hysteresis.permits(expected_gain=0.3, consecutive_evidence=2))

    def test_official_enrollment_and_protocols_are_explicit(self) -> None:
        enrollment = ProviderEnrollment("p", "OAUTH")
        enrollment.connect()
        self.assertEqual(enrollment.state, EnrollmentState.CONNECTED)
        enrollment.revoke()
        self.assertEqual(enrollment.state, EnrollmentState.REVOKED)
        request = ProtocolAdapter("gemini").normalize_request([{"role":"user","content":"hello"}])
        self.assertEqual(request["protocol"], "gemini")


class Lot08CompletionAuditTests(unittest.TestCase):
    def test_tool_pre_and_postconditions_are_mandatory_when_supplied(self) -> None:
        runtime = ToolRuntime()
        runtime.register(ToolSchema("write", {"path": str}, mutating=True))
        governed = GovernedToolExecutor(runtime)
        with self.assertRaises(PermissionError):
            governed.invoke(ToolCall("i0", "write", {"path":"a"}), lambda _: {"ok":True}, precondition=lambda _: False)
        receipt = governed.invoke(
            ToolCall("i1", "write", {"path":"a"}),
            lambda _: {"ok":True,"head":"abc"},
            precondition=lambda _: True,
            postcondition=lambda result: result.get("head") == "abc",
        )
        self.assertTrue(receipt.verified)

    def test_mcp_manifest_drift_capability_projection_and_replay(self) -> None:
        lifecycle = MCPLifecycle()
        original = MCPManifest("server", {"read":{"args":["path"]}})
        lifecycle.approve(original)
        self.assertTrue(lifecycle.validate(original))
        changed = MCPManifest("server", {"read":{"args":["path"]}, "shell":{"args":["cmd"]}})
        self.assertFalse(lifecycle.validate(changed))
        projection = CapabilityProjection(filesystem_roots=("repo",), egress_hosts=("github.com",), secret_names=())
        self.assertTrue(projection.allows_egress("github.com"))
        self.assertFalse(projection.allows_secret("OPENAI_API_KEY"))
        replay = DeterministicReplayLedger()
        replay.append("i1", "hash")
        self.assertEqual(replay.replay(), (("i1","hash"),))


class Lot09CompletionAuditTests(unittest.TestCase):
    def test_semantic_regression_migration_evidence_and_self_correction(self) -> None:
        detector = SemanticRegressionDetector()
        regressions = detector.compare({"api":"v1","cache":True}, {"api":"v2","cache":True}, protected_keys={"api","cache"})
        self.assertEqual(regressions, {"api"})
        migration = DependencyMigrationEvidence("pkg", "1", "2", "https://upstream/docs", "0123456789abcdef", ("rename x",))
        self.assertTrue(migration.is_admissible())
        policy = SelfCorrectionPolicy()
        self.assertEqual(policy.decide(repeated_fingerprint=True, evidence_changed=False, plan_invalidated=False), "NEW_PROBE")
        self.assertEqual(policy.decide(repeated_fingerprint=False, evidence_changed=False, plan_invalidated=True), "REPLAN_AFFECTED")

    def test_behavioral_contract_is_checked_against_observed_behavior(self) -> None:
        contract = BehavioralContract("parser", {"strict":True,"format":"json"})
        evaluator = BehavioralContractEvaluator()
        self.assertTrue(evaluator.evaluate(contract, {"strict":True,"format":"json","latency":1}))
        self.assertFalse(evaluator.evaluate(contract, {"strict":False,"format":"json"}))


class Lot10CompletionAuditTests(unittest.TestCase):
    def test_evidence_gap_miner_requires_composition_and_mutation_evidence(self) -> None:
        required = {EvidenceType.VISIBLE, EvidenceType.HIDDEN, EvidenceType.COMPOSITIONAL, EvidenceType.MUTATION}
        observed = {EvidenceType.VISIBLE, EvidenceType.HIDDEN}
        self.assertEqual(EvidenceGapMiner().missing(required, observed), {EvidenceType.COMPOSITIONAL, EvidenceType.MUTATION})

    def test_verifier_integrity_and_redteam_reject_test_gaming(self) -> None:
        source = "def verify(): return True"
        expected = VerifierIntegrityGuard.hash_source(source)
        guard = VerifierIntegrityGuard(expected)
        self.assertTrue(guard.verify(source))
        self.assertFalse(guard.verify(source + " # weakened"))
        loop = RedTeamVerifierLoop()
        self.assertEqual(loop.assess(visible_passed=True, hidden_passed=False, compositional_passed=True, verifier_integrity=True).reason, "visible_only_gaming")
        self.assertEqual(loop.assess(visible_passed=True, hidden_passed=True, compositional_passed=True, verifier_integrity=False).reason, "verifier_tampering")
        self.assertTrue(loop.assess(visible_passed=True, hidden_passed=True, compositional_passed=True, verifier_integrity=True).accepted)


if __name__ == "__main__":
    unittest.main()
