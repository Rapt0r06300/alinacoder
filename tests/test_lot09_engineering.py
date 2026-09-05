from __future__ import annotations

import unittest

from alinacoder.engineering import (
    ArchitectureFitnessGuard,
    CandidatePatch,
    CausalDebugger,
    ChangeImpactSimulator,
    Hypothesis,
    PlanDAG,
    RepairAttemptGraph,
    RequirementRecoveryGraph,
)


class Lot09EngineeringTests(unittest.TestCase):
    def test_requirement_graph_separates_requirements_assumptions_and_unknowns(self):
        graph = RequirementRecoveryGraph()
        graph.require("R1", "must preserve public API", source="user", explicit=True)
        graph.assume("A1", "database is sqlite", source="repo")
        graph.unknown("U1", "migration policy")
        self.assertEqual(graph.requirements["R1"].text, "must preserve public API")
        self.assertFalse(graph.assumptions["A1"].verified)
        self.assertIn("U1", graph.unresolved_unknowns())

    def test_plan_dag_replans_only_affected_descendants(self):
        dag = PlanDAG()
        dag.add("A")
        dag.add("B", depends_on={"A"})
        dag.add("C")
        dag.add("D", depends_on={"B"})
        self.assertEqual(dag.replan_affected({"A"}), {"A","B","D"})
        self.assertEqual(dag.replan_affected({"C"}), {"C"})

    def test_causal_debugger_prioritizes_falsifiable_trace_supported_hypothesis(self):
        debugger = CausalDebugger()
        ranked = debugger.rank_hypotheses([
            Hypothesis("h1", evidence_matches=1, discriminating_probe=False, falsifiable=True),
            Hypothesis("h2", evidence_matches=3, discriminating_probe=True, falsifiable=True),
            Hypothesis("h3", evidence_matches=5, discriminating_probe=False, falsifiable=False),
        ])
        self.assertEqual(ranked[0].hypothesis_id, "h2")

    def test_change_impact_simulator_computes_transitive_blast_radius_and_tests(self):
        sim = ChangeImpactSimulator(
            dependencies={"a.py":{"b.py"}, "b.py":{"c.py"}},
            tests_by_file={"b.py":{"test_b"}, "c.py":{"test_c"}},
        )
        impact = sim.analyze({"a.py"})
        self.assertEqual(impact.files, {"a.py","b.py","c.py"})
        self.assertEqual(impact.tests, {"test_b","test_c"})

    def test_repair_attempt_graph_blocks_repeating_known_failed_patch(self):
        attempts = RepairAttemptGraph()
        attempts.record("deadbeef", outcome="failed", reason="same assertion")
        self.assertFalse(attempts.may_retry("deadbeef"))
        self.assertTrue(attempts.may_retry("newfingerprint"))

    def test_candidate_patch_and_architecture_fitness_fail_closed(self):
        patch = CandidatePatch({"src/a.py"}, behavioral_contracts={"parser":"strict-json"}, required_tests={"test_parser"})
        self.assertTrue(patch.ready_for_verification(executed_tests={"test_parser"}))
        self.assertFalse(patch.ready_for_verification(executed_tests=set()))
        guard = ArchitectureFitnessGuard(max_complexity_delta=2, max_dependency_delta=1)
        guard.check(complexity_delta=2, dependency_delta=1)
        with self.assertRaises(ValueError):
            guard.check(complexity_delta=3, dependency_delta=0)


if __name__ == "__main__":
    unittest.main()
