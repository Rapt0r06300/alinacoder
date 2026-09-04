from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


class GoalEngineTests(unittest.TestCase):
    def make_engine(self, root: Path):
        from alinacoder.goal.engine import GoalEngine
        from alinacoder.state.store import StateStore
        store = StateStore(root / "state.db")
        try:
            store.get_state("s1")
        except Exception:
            store.create_session("s1", {})
        return store, GoalEngine(store, "s1")

    def test_goal_persists_across_restart_and_plan_replacement_preserves_progress(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            store, engine = self.make_engine(root)
            goal = engine.create_goal("Ship feature", ["tests pass", "artifact exists"])
            engine.verify_criterion(goal.goal_id, goal.criteria[0].criterion_id, {"suite": "green"})
            before = engine.get_goal(goal.goal_id)
            engine.replace_plan(goal.goal_id, ["try B", "verify B"])
            after = engine.get_goal(goal.goal_id)
            self.assertEqual(after.plan_revision, before.plan_revision + 1)
            self.assertEqual(after.criteria[0].status.value, "VERIFIED")
            store.close()
            reopened, engine2 = self.make_engine(root)
            loaded = engine2.get_goal(goal.goal_id)
            self.assertEqual(loaded.objective, "Ship feature")
            self.assertEqual(loaded.criteria[0].status.value, "VERIFIED")
            reopened.close()

    def test_complete_refuses_unverified_or_stale_criterion(self) -> None:
        from alinacoder.goal.engine import GoalCompletionError
        with tempfile.TemporaryDirectory() as td:
            store, engine = self.make_engine(Path(td))
            goal = engine.create_goal("Finish", ["A", "B"])
            engine.verify_criterion(goal.goal_id, goal.criteria[0].criterion_id, {"ok": True})
            with self.assertRaises(GoalCompletionError): engine.complete(goal.goal_id)
            engine.verify_criterion(goal.goal_id, goal.criteria[1].criterion_id, {"ok": True})
            engine.mark_criterion_stale(goal.goal_id, goal.criteria[1].criterion_id, "repo changed")
            with self.assertRaises(GoalCompletionError): engine.complete(goal.goal_id)
            engine.verify_criterion(goal.goal_id, goal.criteria[1].criterion_id, {"ok": True})
            self.assertEqual(engine.complete(goal.goal_id).status.value, "COMPLETE")
            store.close()

    def test_stagnation_triggers_replan_instead_of_repeat(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            store, engine = self.make_engine(Path(td))
            goal = engine.create_goal("Solve", ["done"])
            for strategy in ("a", "b", "c"): engine.record_strategy_failure(goal.goal_id, strategy, "failed")
            self.assertEqual(engine.next_directive(goal.goal_id), "REPLAN")
            self.assertEqual(len(engine.get_goal(goal.goal_id).attempted_strategies), 3)
            store.close()

    def test_pause_resume_edit_cancel_and_minimal_invalidation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            store, engine = self.make_engine(Path(td))
            goal = engine.create_goal("Original", ["A", "B"])
            for criterion in goal.criteria: engine.verify_criterion(goal.goal_id, criterion.criterion_id, {"ok": True})
            engine.pause(goal.goal_id)
            self.assertEqual(engine.get_goal(goal.goal_id).status.value, "PAUSED")
            engine.resume(goal.goal_id)
            engine.edit_objective(goal.goal_id, "Updated", invalidate_criterion_ids=[goal.criteria[1].criterion_id])
            edited = engine.get_goal(goal.goal_id)
            self.assertEqual(edited.criteria[0].status.value, "VERIFIED")
            self.assertEqual(edited.criteria[1].status.value, "UNVERIFIED")
            engine.cancel(goal.goal_id, "user")
            self.assertEqual(engine.get_goal(goal.goal_id).status.value, "CANCELLED")
            store.close()

    def test_impossibility_requires_external_blocker_evidence_and_alternatives(self) -> None:
        from alinacoder.goal.engine import GoalImpossibilityError
        with tempfile.TemporaryDirectory() as td:
            store, engine = self.make_engine(Path(td))
            goal = engine.create_goal("Reach external system", ["connected"])
            with self.assertRaises(GoalImpossibilityError): engine.declare_impossible(goal.goal_id, "service unavailable", {}, ["retry"])
            blocked = engine.declare_impossible(goal.goal_id, "service unavailable", {"status": 503, "observed": True}, ["retry alternate endpoint", "local fallback checked"])
            self.assertEqual(blocked.status.value, "BLOCKED")
            self.assertTrue(blocked.blockers)
            store.close()


if __name__ == "__main__":
    unittest.main()
