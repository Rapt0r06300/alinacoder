from __future__ import annotations

import unittest

from alinacoder.verification import (
    BidirectionalPatchVerifier,
    CompletionFirewall,
    DoneContractEngine,
    EvidenceReceipt,
    FormalEscalationPolicy,
    StochasticVerdict,
    VerificationBundle,
)


class Lot10VerificationTests(unittest.TestCase):
    def test_evidence_is_bound_to_exact_state_and_expires(self):
        ev = EvidenceReceipt("tests","verifier-A","state-1","artifact-1",passed=True,observed_at=100.0,expires_at=200.0)
        self.assertTrue(ev.is_fresh(current_state_hash="state-1", now=150.0))
        self.assertFalse(ev.is_fresh(current_state_hash="state-2", now=150.0))
        self.assertFalse(ev.is_fresh(current_state_hash="state-1", now=201.0))

    def test_stochastic_evidence_can_be_inconclusive(self):
        self.assertEqual(StochasticVerdict.from_samples([True, False], min_samples=5), "INCONCLUSIVE")
        self.assertEqual(StochasticVerdict.from_samples([True]*9+[False], min_samples=5, pass_threshold=0.8), "PASS")
        self.assertEqual(StochasticVerdict.from_samples([True,False,False,False,False], min_samples=5, pass_threshold=0.8), "FAIL")

    def test_visible_tests_alone_never_cross_completion_firewall(self):
        bundle = VerificationBundle(visible_tests=True, hidden_tests=False, compositional_tests=False, mutation_tests=True, verifier_integrity=True)
        decision = CompletionFirewall().decide(bundle, generator_id="model-A", verifier_id="model-B")
        self.assertFalse(decision.allowed)
        self.assertIn("hidden", decision.reasons)

    def test_same_generator_and_verifier_is_rejected(self):
        bundle = VerificationBundle(True, True, True, True, True)
        decision = CompletionFirewall().decide(bundle, generator_id="same", verifier_id="same")
        self.assertFalse(decision.allowed)
        self.assertIn("independent", decision.reasons)

    def test_bidirectional_patch_verifier_detects_wrong_problem(self):
        report = BidirectionalPatchVerifier().verify(
            intended_obligations={"parse-json","preserve-cache"},
            reconstructed_obligations={"parse-json"},
        )
        self.assertFalse(report.accepted)
        self.assertEqual(report.missing, {"preserve-cache"})

    def test_done_contract_requires_fresh_passed_evidence_per_obligation(self):
        engine = DoneContractEngine()
        evidence = {
            "R1":[EvidenceReceipt("hidden","v1","state","a1",True,100,200)],
            "R2":[EvidenceReceipt("composition","v2","state","a2",True,100,200)],
        }
        result = engine.evaluate({"R1","R2"}, evidence, current_state_hash="state", now=150)
        self.assertTrue(result.ready)
        self.assertEqual(result.readiness_score, 1.0)
        stale = engine.evaluate({"R1","R2"}, evidence, current_state_hash="changed", now=150)
        self.assertFalse(stale.ready)
        self.assertEqual(stale.missing, {"R1","R2"})

    def test_formal_escalation_for_irreversible_high_criticality_invariant(self):
        policy = FormalEscalationPolicy()
        self.assertTrue(policy.should_escalate(criticality="high", irreversible=True, invariant_bearing=True))
        self.assertFalse(policy.should_escalate(criticality="low", irreversible=False, invariant_bearing=False))


if __name__ == "__main__":
    unittest.main()
