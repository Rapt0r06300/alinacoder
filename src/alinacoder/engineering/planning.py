from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlanNode:
    node_id: str
    depends_on: set[str] = field(default_factory=set)


class PlanDAG:
    def __init__(self) -> None:
        self.nodes: dict[str, PlanNode] = {}

    def add(self, node_id: str, *, depends_on: set[str] | None = None) -> None:
        deps = set(depends_on or set())
        missing = deps - self.nodes.keys()
        if missing:
            raise ValueError(f"unknown dependencies: {sorted(missing)}")
        self.nodes[node_id] = PlanNode(node_id, deps)

    def replan_affected(self, changed: set[str]) -> set[str]:
        affected = set(changed)
        progressed = True
        while progressed:
            progressed = False
            for node in self.nodes.values():
                if node.node_id not in affected and node.depends_on & affected:
                    affected.add(node.node_id)
                    progressed = True
        return affected
