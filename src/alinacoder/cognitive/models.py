from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CognitiveState:
    state_version: int = 0
    active_goal_id: str | None = None
    intent_revision: int = 0
    active_intent_node: str | None = None
    plan_revision: int = 0
    current_phase: str = ""
    current_subtask_id: str | None = None
    active_requirements: tuple[str, ...] = ()
    active_constraints: tuple[str, ...] = ()
    prohibitions: tuple[str, ...] = ()
    open_questions: tuple[str, ...] = ()
    uncertainties: tuple[dict[str, Any], ...] = ()
    selected_artifacts: tuple[str, ...] = ()
    verified_facts: tuple[dict[str, Any], ...] = ()
    stale_facts: tuple[dict[str, Any], ...] = ()
    recent_failures: tuple[dict[str, Any], ...] = ()
    execution_ledger_version: int = 0
    memory_snapshot_version: int = 0
    current_model_route: dict[str, Any] = field(default_factory=dict)
    last_verified_repo_state: str | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key in (
            "active_requirements", "active_constraints", "prohibitions", "open_questions",
            "uncertainties", "selected_artifacts", "verified_facts", "stale_facts", "recent_failures",
        ):
            value[key] = list(value[key])
        return value

    @classmethod
    def from_dict(cls, value: dict[str, Any] | None) -> "CognitiveState":
        data = dict(value or {})
        return cls(
            state_version=int(data.get("state_version", 0)),
            active_goal_id=data.get("active_goal_id"),
            intent_revision=int(data.get("intent_revision", 0)),
            active_intent_node=data.get("active_intent_node"),
            plan_revision=int(data.get("plan_revision", 0)),
            current_phase=str(data.get("current_phase", "")),
            current_subtask_id=data.get("current_subtask_id"),
            active_requirements=tuple(str(x) for x in data.get("active_requirements", ())),
            active_constraints=tuple(str(x) for x in data.get("active_constraints", ())),
            prohibitions=tuple(str(x) for x in data.get("prohibitions", ())),
            open_questions=tuple(str(x) for x in data.get("open_questions", ())),
            uncertainties=tuple(dict(x) for x in data.get("uncertainties", ()) if isinstance(x, dict)),
            selected_artifacts=tuple(str(x) for x in data.get("selected_artifacts", ())),
            verified_facts=tuple(dict(x) for x in data.get("verified_facts", ()) if isinstance(x, dict)),
            stale_facts=tuple(dict(x) for x in data.get("stale_facts", ()) if isinstance(x, dict)),
            recent_failures=tuple(dict(x) for x in data.get("recent_failures", ()) if isinstance(x, dict)),
            execution_ledger_version=int(data.get("execution_ledger_version", 0)),
            memory_snapshot_version=int(data.get("memory_snapshot_version", 0)),
            current_model_route=dict(data.get("current_model_route", {})),
            last_verified_repo_state=data.get("last_verified_repo_state"),
        )
