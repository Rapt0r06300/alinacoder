from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PlanNodeV2:
    node_id: str
    phase: str
    subtask: str = ""
    depends_on: tuple[str, ...] = ()
    required_evidence: tuple[str, ...] = ()
    completion_predicate: str = ""
    affected_files: tuple[str, ...] = ()
    affected_symbols: tuple[str, ...] = ()
    expected_tools: tuple[str, ...] = ()
    status: str = "PENDING"
    attempts: int = 0
    failure_reasons: list[str] = field(default_factory=list)
    memory_query_intent: str = ""
    stale_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class PlanGraph:
    _VALID_STATUSES = {"PENDING", "ACTIVE", "COMPLETED", "FAILED", "STALE", "BLOCKED"}

    def __init__(self) -> None:
        self._nodes: dict[str, PlanNodeV2] = {}

    def add(self, node: PlanNodeV2) -> None:
        if not node.node_id.strip() or not node.phase.strip():
            raise ValueError("plan node requires node_id and phase")
        if node.node_id in self._nodes:
            raise ValueError(f"duplicate plan node: {node.node_id}")
        missing = set(node.depends_on) - self._nodes.keys()
        if missing:
            raise ValueError(f"unknown plan dependencies: {sorted(missing)}")
        if node.status not in self._VALID_STATUSES:
            raise ValueError(f"invalid plan status: {node.status}")
        self._nodes[node.node_id] = node

    def get(self, node_id: str) -> PlanNodeV2:
        try:
            return self._nodes[node_id]
        except KeyError as exc:
            raise KeyError(node_id) from exc

    def mark_active(self, node_id: str) -> None:
        node = self.get(node_id)
        node.status = "ACTIVE"
        node.attempts += 1
        node.stale_reason = None

    def mark_completed(self, node_id: str) -> None:
        node = self.get(node_id)
        node.status = "COMPLETED"
        node.stale_reason = None

    def record_failure(self, node_id: str, reason: str) -> None:
        node = self.get(node_id)
        node.status = "FAILED"
        node.attempts += 1
        node.failure_reasons.append(str(reason))

    def descendants(self, changed: tuple[str, ...] | list[str] | set[str]) -> set[str]:
        affected = {str(item) for item in changed}
        missing = affected - self._nodes.keys()
        if missing:
            raise KeyError(sorted(missing)[0])
        progressed = True
        while progressed:
            progressed = False
            for node in self._nodes.values():
                if node.node_id not in affected and set(node.depends_on) & affected:
                    affected.add(node.node_id)
                    progressed = True
        return affected

    def replan_affected(
        self,
        changed: tuple[str, ...] | list[str] | set[str],
        *,
        reason: str,
    ) -> set[str]:
        affected = self.descendants(changed)
        for node_id in affected:
            node = self._nodes[node_id]
            node.status = "STALE"
            node.stale_reason = str(reason)
        return affected

    def ready(self) -> tuple[PlanNodeV2, ...]:
        return tuple(
            node
            for node in self._nodes.values()
            if node.status == "PENDING"
            and all(self._nodes[dep].status == "COMPLETED" for dep in node.depends_on)
        )

    def nodes(self) -> tuple[PlanNodeV2, ...]:
        return tuple(self._nodes.values())
