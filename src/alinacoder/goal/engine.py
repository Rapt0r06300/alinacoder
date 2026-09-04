from __future__ import annotations

from copy import deepcopy
import uuid
from typing import Any, Callable

from alinacoder.state.store import StateStore
from .models import CriterionStatus, GoalContract, GoalCriterion, GoalStatus


class GoalError(RuntimeError):
    pass

class GoalCompletionError(GoalError):
    pass

class GoalImpossibilityError(GoalError):
    pass


class GoalEngine:
    def __init__(self, store: StateStore, session_id: str) -> None:
        self.store = store
        self.session_id = session_id

    def _goals_from_state(self) -> dict[str, Any]:
        return deepcopy(self.store.get_state(self.session_id).data.get("goals", {}))

    def _persist(self, goals: dict[str, Any], event_kind: str, metadata: dict[str, Any] | None = None) -> None:
        state = self.store.get_state(self.session_id)
        epoch = self.store.acquire_writer(self.session_id)
        data = deepcopy(state.data)
        data["goals"] = goals
        self.store.commit_state(self.session_id, state.version, epoch, data, event_kind, metadata)

    def create_goal(self, objective: str, criteria: list[str], prohibitions: list[str] | None = None) -> GoalContract:
        if not objective.strip() or not criteria:
            raise GoalError("Goal requires objective and at least one criterion")
        goal_id = uuid.uuid4().hex
        contract = GoalContract(goal_id, objective.strip(), [GoalCriterion(f"c{i+1}", text.strip()) for i, text in enumerate(criteria)], list(prohibitions or []))
        goals = self._goals_from_state()
        goals[goal_id] = contract.to_dict()
        self._persist(goals, "goal_created", {"goal_id": goal_id})
        return contract

    def get_goal(self, goal_id: str) -> GoalContract:
        raw = self._goals_from_state().get(goal_id)
        if raw is None:
            raise GoalError(f"Unknown goal: {goal_id}")
        return GoalContract.from_dict(raw)

    def _update(self, goal_id: str, event_kind: str, mutate: Callable[[GoalContract], None]) -> GoalContract:
        goals = self._goals_from_state()
        raw = goals.get(goal_id)
        if raw is None:
            raise GoalError(f"Unknown goal: {goal_id}")
        goal = GoalContract.from_dict(raw)
        mutate(goal)
        goals[goal_id] = goal.to_dict()
        self._persist(goals, event_kind, {"goal_id": goal_id})
        return goal

    def replace_plan(self, goal_id: str, steps: list[str]) -> GoalContract:
        def mutate(goal: GoalContract) -> None:
            if goal.status in {GoalStatus.CANCELLED, GoalStatus.COMPLETE}:
                raise GoalError("Cannot replan a terminal goal")
            goal.plan_revision += 1
            goal.plan_steps = list(steps)
        return self._update(goal_id, "goal_replanned", mutate)

    def _criterion(self, goal: GoalContract, criterion_id: str) -> GoalCriterion:
        for criterion in goal.criteria:
            if criterion.criterion_id == criterion_id:
                return criterion
        raise GoalError(f"Unknown criterion: {criterion_id}")

    def verify_criterion(self, goal_id: str, criterion_id: str, evidence: dict[str, Any]) -> GoalContract:
        if not evidence:
            raise GoalError("Verification requires evidence")
        def mutate(goal: GoalContract) -> None:
            criterion = self._criterion(goal, criterion_id)
            criterion.status = CriterionStatus.VERIFIED
            criterion.evidence = deepcopy(evidence)
            criterion.stale_reason = None
        return self._update(goal_id, "goal_criterion_verified", mutate)

    def mark_criterion_stale(self, goal_id: str, criterion_id: str, reason: str) -> GoalContract:
        def mutate(goal: GoalContract) -> None:
            criterion = self._criterion(goal, criterion_id)
            criterion.status = CriterionStatus.STALE
            criterion.stale_reason = reason
        return self._update(goal_id, "goal_criterion_stale", mutate)

    def complete(self, goal_id: str) -> GoalContract:
        def mutate(goal: GoalContract) -> None:
            bad = [c.criterion_id for c in goal.criteria if c.status is not CriterionStatus.VERIFIED or not c.evidence]
            if bad:
                raise GoalCompletionError(f"Unverified/stale criteria: {bad}")
            if goal.status in {GoalStatus.CANCELLED, GoalStatus.BLOCKED}:
                raise GoalCompletionError(f"Goal cannot complete from {goal.status.value}")
            goal.status = GoalStatus.COMPLETE
        return self._update(goal_id, "goal_completed", mutate)

    def pause(self, goal_id: str) -> GoalContract:
        return self._update(goal_id, "goal_paused", lambda goal: setattr(goal, "status", GoalStatus.PAUSED))

    def resume(self, goal_id: str) -> GoalContract:
        def mutate(goal: GoalContract) -> None:
            if goal.status is not GoalStatus.PAUSED:
                raise GoalError("Only paused goals can resume")
            goal.status = GoalStatus.ACTIVE
        return self._update(goal_id, "goal_resumed", mutate)

    def cancel(self, goal_id: str, reason: str) -> GoalContract:
        def mutate(goal: GoalContract) -> None:
            goal.status = GoalStatus.CANCELLED
            goal.cancel_reason = reason
        return self._update(goal_id, "goal_cancelled", mutate)

    def edit_objective(self, goal_id: str, objective: str, invalidate_criterion_ids: list[str] | None = None) -> GoalContract:
        ids = set(invalidate_criterion_ids or [])
        def mutate(goal: GoalContract) -> None:
            goal.objective = objective.strip()
            goal.plan_revision += 1
            for criterion in goal.criteria:
                if criterion.criterion_id in ids:
                    criterion.status = CriterionStatus.UNVERIFIED
                    criterion.evidence = {}
                    criterion.stale_reason = "objective changed"
        return self._update(goal_id, "goal_edited", mutate)

    def record_strategy_failure(self, goal_id: str, strategy: str, reason: str) -> GoalContract:
        return self._update(goal_id, "goal_strategy_failed", lambda goal: goal.attempted_strategies.append({"strategy": strategy, "reason": reason}))

    def next_directive(self, goal_id: str) -> str:
        goal = self.get_goal(goal_id)
        if goal.status is GoalStatus.PAUSED:
            return "PAUSED"
        if goal.status in {GoalStatus.COMPLETE, GoalStatus.CANCELLED, GoalStatus.BLOCKED}:
            return goal.status.value
        if len(goal.attempted_strategies) >= 3:
            return "REPLAN"
        return "CONTINUE"

    def declare_impossible(self, goal_id: str, blocker: str, evidence: dict[str, Any], alternatives: list[str]) -> GoalContract:
        if not blocker.strip() or not evidence or len([a for a in alternatives if a.strip()]) < 2:
            raise GoalImpossibilityError("Impossibility requires concrete blocker evidence and at least two alternatives")
        def mutate(goal: GoalContract) -> None:
            goal.blockers.append({"blocker": blocker, "evidence": deepcopy(evidence), "alternatives": list(alternatives)})
            goal.status = GoalStatus.BLOCKED
        return self._update(goal_id, "goal_blocked_proven", mutate)
