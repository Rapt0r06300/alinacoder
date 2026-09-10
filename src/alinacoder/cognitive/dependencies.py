from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DependencyNode:
    node_id: str
    kind: str
    depends_on: set[str] = field(default_factory=set)
    status: str = "ACTIVE"
    stale_reason: str | None = None


class DependencyGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, DependencyNode] = {}

    def add(self, node_id: str, kind: str, *, depends_on: tuple[str, ...] | list[str] | set[str] = ()) -> DependencyNode:
        node_id = str(node_id).strip()
        kind = str(kind).strip()
        if not node_id or not kind:
            raise ValueError("node_id and kind are required")
        deps = {str(item) for item in depends_on}
        missing = deps - self._nodes.keys()
        if missing:
            raise ValueError(f"unknown dependencies: {sorted(missing)}")
        if node_id in deps:
            raise ValueError("node cannot depend on itself")
        node = DependencyNode(node_id, kind, deps)
        self._nodes[node_id] = node
        return node

    def get(self, node_id: str) -> DependencyNode:
        try:
            return self._nodes[node_id]
        except KeyError as exc:
            raise KeyError(node_id) from exc

    def descendants(self, roots: tuple[str, ...] | list[str] | set[str]) -> set[str]:
        affected = {str(item) for item in roots}
        missing = affected - self._nodes.keys()
        if missing:
            raise KeyError(sorted(missing)[0])
        changed = True
        while changed:
            changed = False
            for node in self._nodes.values():
                if node.node_id not in affected and node.depends_on & affected:
                    affected.add(node.node_id)
                    changed = True
        return affected

    def invalidate_descendants(
        self,
        changed: tuple[str, ...] | list[str] | set[str],
        reason: str,
    ) -> set[str]:
        affected = self.descendants(changed)
        for node_id in affected:
            node = self._nodes[node_id]
            node.status = "STALE"
            node.stale_reason = str(reason)
        return affected

    def activate(self, node_id: str) -> None:
        node = self.get(node_id)
        node.status = "ACTIVE"
        node.stale_reason = None
