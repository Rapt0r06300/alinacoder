from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

from alinacoder.memory.skillbook import ExperienceCard, SkillBook
from alinacoder.state.store import StateStore
from alinacoder.verification.models import EvidenceReceipt


def _load(testcase: unittest.TestCase, module_name: str):
    try:
        spec = importlib.util.find_spec(module_name)
    except ModuleNotFoundError:
        spec = None
    testcase.assertIsNotNone(spec, f"missing module: {module_name}")
    return importlib.import_module(module_name)


class CognitiveKernelTests(unittest.TestCase):
    def test_cognitive_state_is_backward_compatible_and_persistent(self) -> None:
        state_mod = _load(self, "alinacoder.cognitive.state")
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "state.sqlite"
            with StateStore(path) as store:
                store.create_session("s", {"legacy": {"keep": True}})
                cognitive = state_mod.CognitiveStateStore(store, "s")
                initial = cognitive.snapshot()
                self.assertEqual(initial.intent_revision, 0)
                cognitive.update(
                    active_goal_id="g1",
                    intent_revision=1,
                    active_requirements=("preserve main",),
                    prohibitions=("no paid spillover",),
                    current_phase="understand",
                )
            with StateStore(path) as restarted:
                persisted = state_mod.CognitiveStateStore(restarted, "s").snapshot()
                self.assertEqual(persisted.active_goal_id, "g1")
                self.assertEqual(persisted.intent_revision, 1)
                self.assertIn("preserve main", persisted.active_requirements)
                self.assertTrue(restarted.get_state("s").data["legacy"]["keep"])

    def test_dependency_graph_invalidates_descendants_only(self) -> None:
        deps = _load(self, "alinacoder.cognitive.dependencies")
        graph = deps.DependencyGraph()
        graph.add("intent:installer", "intent")
        graph.add("plan:inspect-installer", "plan", depends_on=("intent:installer",))
        graph.add("evidence:installer-test", "evidence", depends_on=("plan:inspect-installer",))
        graph.add("observation:provider-atlas", "observation")
        affected = graph.invalidate_descendants(("intent:installer",), "user corrected target")
        self.assertEqual(
            affected,
            {"intent:installer", "plan:inspect-installer", "evidence:installer-test"},
        )
        self.assertEqual(graph.get("evidence:installer-test").status, "STALE")
        self.assertEqual(graph.get("observation:provider-atlas").status, "ACTIVE")

    def test_intent_compiler_detects_correction_and_continuation_without_losing_raw(self) -> None:
        intent_mod = _load(self, "alinacoder.conversation.intent")
        compiler = intent_mod.IntentCompiler()
        raw = "Non, je parle du model bridge. Continue sans t'arrêter."
        envelope = compiler.compile(raw, source_turn_ids=("turn:7",))
        self.assertEqual(envelope.raw, raw)
        self.assertTrue(envelope.correction)
        self.assertTrue(envelope.continuation)
        self.assertEqual(envelope.source_turn_ids, ("turn:7",))
        self.assertTrue(envelope.primary_intent)

    def test_uncertainty_controller_prefers_safe_information_before_question(self) -> None:
        control = _load(self, "alinacoder.conversation.control")
        controller = control.UncertaintyController()
        inspect = controller.decide(
            ambiguity=0.9,
            wrong_action_cost=0.9,
            reversible=False,
            safe_inspection_available=True,
            sandbox_probe_available=False,
        )
        self.assertEqual(inspect.action.value, "inspect")
        probe = controller.decide(
            ambiguity=0.9,
            wrong_action_cost=0.8,
            reversible=True,
            safe_inspection_available=False,
            sandbox_probe_available=True,
        )
        self.assertEqual(probe.action.value, "sandbox_probe")
        ask = controller.decide(
            ambiguity=0.9,
            wrong_action_cost=0.95,
            reversible=False,
            safe_inspection_available=False,
            sandbox_probe_available=False,
        )
        self.assertEqual(ask.action.value, "ask_user")
        act = controller.decide(
            ambiguity=0.6,
            wrong_action_cost=0.1,
            reversible=True,
            safe_inspection_available=False,
            sandbox_probe_available=False,
        )
        self.assertEqual(act.action.value, "act")

    def test_plan_graph_replans_only_affected_descendants(self) -> None:
        planning = _load(self, "alinacoder.cognitive.planning")
        graph = planning.PlanGraph()
        graph.add(planning.PlanNodeV2("understand", phase="understand"))
        graph.add(planning.PlanNodeV2("provider", phase="localize", depends_on=("understand",)))
        graph.add(planning.PlanNodeV2("installer", phase="localize", depends_on=("understand",)))
        graph.add(planning.PlanNodeV2("provider-fix", phase="implement", depends_on=("provider",)))
        graph.mark_completed("installer")
        affected = graph.replan_affected(("provider",), reason="target corrected")
        self.assertEqual(affected, {"provider", "provider-fix"})
        self.assertEqual(graph.get("installer").status, "COMPLETED")

    def test_phase_aware_ranking_prefers_current_phase_and_failure_relevance(self) -> None:
        adaptive = _load(self, "alinacoder.memory.adaptive")
        context = adaptive.RetrievalContext(
            goal="fix parser",
            phase="debug",
            subtask="reproduce traceback",
            paths=("src/parser.py",),
            failures=("ValueError parse",),
            constraints=("no dependency changes",),
            repo_state="abc",
        )
        relevant = adaptive.RankingCandidate(
            ref="a",
            text="parser ValueError traceback debug src/parser.py",
            base_score=0.5,
            authority=80,
            fresh=True,
        )
        generic = adaptive.RankingCandidate(
            ref="b",
            text="general architecture notes",
            base_score=0.5,
            authority=80,
            fresh=True,
        )
        ranker = adaptive.PhaseAwareRanker()
        self.assertGreater(ranker.score(relevant, context), ranker.score(generic, context))

    def test_context_folder_preserves_source_event_ids_without_mutating_history(self) -> None:
        adaptive = _load(self, "alinacoder.memory.adaptive")
        history = [
            {"event_id": "e1", "kind": "read", "text": "inspected parser"},
            {"event_id": "e2", "kind": "test", "text": "reproduced ValueError"},
        ]
        original = [dict(item) for item in history]
        folded = adaptive.ContextFolder().fold(
            history,
            decision="patch parser",
            evidence=("e2",),
            files=("src/parser.py",),
            rejected_hypotheses=("network",),
            open_questions=(),
            verification_state="reproduced",
        )
        self.assertEqual(history, original)
        self.assertEqual(folded.source_event_ids, ("e1", "e2"))
        self.assertEqual(folded.decision, "patch parser")

    def test_verification_kernel_invalidates_state_bound_evidence_by_path(self) -> None:
        kernel_mod = _load(self, "alinacoder.verification.kernel")
        kernel = kernel_mod.VerificationKernel()
        receipt = EvidenceReceipt("tests", "pytest", "s1", "artifact", True, 1.0, 10.0)
        kernel.add("criterion:parser", receipt, paths=("src/parser.py",))
        self.assertTrue(kernel.certify("criterion:parser", current_state_hash="s1", now=2.0))
        invalidated = kernel.invalidate_for_paths(("src/parser.py",), "file changed")
        self.assertIn("criterion:parser", invalidated)
        self.assertFalse(kernel.certify("criterion:parser", current_state_hash="s1", now=2.0))

    def test_critic_policy_is_value_gated_and_packet_redacts_private_reasoning(self) -> None:
        critic = _load(self, "alinacoder.orchestration.critic")
        packet = critic.CriticPacket(
            task_contract={"goal": "fix parser"},
            evidence={"test": "failed"},
            proposed_result={"patch": "x", "chain_of_thought": "private"},
            primary_lineage="model-a",
        )
        self.assertNotIn("chain_of_thought", str(packet.to_dict()))
        policy = critic.CriticPolicy()
        self.assertTrue(
            policy.should_call(
                criticality=0.9,
                uncertainty=0.8,
                repeated_failures=2,
                blast_radius=0.8,
                expected_terminal_gain=0.3,
                latency_cost=0.02,
                quota_cost=0.02,
            )
        )
        self.assertFalse(
            policy.should_call(
                criticality=0.1,
                uncertainty=0.1,
                repeated_failures=0,
                blast_radius=0.1,
                expected_terminal_gain=0.01,
                latency_cost=0.05,
                quota_cost=0.05,
            )
        )

    def test_skillbook_quarantines_poor_verified_skill_without_deleting_it(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            book = SkillBook(Path(td) / "skills.sqlite")
            try:
                skill_id = book.promote(
                    ExperienceCard(
                        "project",
                        "parser/value-error",
                        "validate token before indexing",
                        True,
                        ("test:parser",),
                    )
                )
                observe = getattr(book, "observe_outcome", None)
                self.assertTrue(callable(observe), "SkillBook.observe_outcome is required")
                observe(skill_id, False)
                observe(skill_id, False)
                observe(skill_id, False)
                self.assertTrue(book.get(skill_id).quarantined)
                self.assertEqual(book.search("project", "parser value error"), [])
                self.assertEqual(book.get(skill_id).skill_id, skill_id)
            finally:
                book.close()


if __name__ == "__main__":
    unittest.main()
