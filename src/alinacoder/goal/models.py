from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CriterionStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    STALE = "STALE"
    CONTRADICTED = "CONTRADICTED"


class GoalStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"
    BLOCKED = "BLOCKED"


@dataclass(slots=True)
class GoalCriterion:
    criterion_id: str
    description: str
    status: CriterionStatus = CriterionStatus.UNVERIFIED
    evidence: dict[str, Any] = field(default_factory=dict)
    stale_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"criterion_id": self.criterion_id, "description": self.description, "status": self.status.value, "evidence": self.evidence, "stale_reason": self.stale_reason}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GoalCriterion":
        return cls(data["criterion_id"], data["description"], CriterionStatus(data.get("status", "UNVERIFIED")), dict(data.get("evidence", {})), data.get("stale_reason"))


@dataclass(slots=True)
class GoalContract:
    goal_id: str
    objective: str
    criteria: list[GoalCriterion]
    prohibitions: list[str] = field(default_factory=list)
    status: GoalStatus = GoalStatus.ACTIVE
    plan_revision: int = 0
    plan_steps: list[str] = field(default_factory=list)
    attempted_strategies: list[dict[str, str]] = field(default_factory=list)
    blockers: list[dict[str, Any]] = field(default_factory=list)
    cancel_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"goal_id": self.goal_id, "objective": self.objective, "criteria": [c.to_dict() for c in self.criteria], "prohibitions": list(self.prohibitions), "status": self.status.value, "plan_revision": self.plan_revision, "plan_steps": list(self.plan_steps), "attempted_strategies": list(self.attempted_strategies), "blockers": list(self.blockers), "cancel_reason": self.cancel_reason}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GoalContract":
        return cls(data["goal_id"], data["objective"], [GoalCriterion.from_dict(c) for c in data.get("criteria", [])], list(data.get("prohibitions", [])), GoalStatus(data.get("status", "ACTIVE")), int(data.get("plan_revision", 0)), list(data.get("plan_steps", [])), list(data.get("attempted_strategies", [])), list(data.get("blockers", [])), data.get("cancel_reason"))
