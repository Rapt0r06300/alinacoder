from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .core import CouncilPolicy

_PRIVATE_KEYS = frozenset({
    "chain_of_thought", "cot", "hidden_reasoning", "raw_reasoning", "scratchpad", "internal_monologue"
})


def _safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _safe(item) for key, item in value.items() if str(key).lower() not in _PRIVATE_KEYS}
    if isinstance(value, (list, tuple)):
        return [_safe(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class CriticPacket:
    task_contract: dict[str, Any]
    evidence: dict[str, Any]
    proposed_result: dict[str, Any]
    primary_lineage: str

    def to_dict(self) -> dict[str, Any]:
        return _safe(asdict(self))

    def admits_critic_lineage(self, critic_lineage: str) -> bool:
        return bool(critic_lineage and critic_lineage != self.primary_lineage)


class CriticPolicy:
    """Spend independent review only when expected terminal value justifies it."""

    def __init__(self, council_policy: CouncilPolicy | None = None) -> None:
        self._council = council_policy or CouncilPolicy(minimum_margin=0.05)

    def should_call(
        self,
        *,
        criticality: float,
        uncertainty: float,
        repeated_failures: int,
        blast_radius: float,
        expected_terminal_gain: float,
        latency_cost: float,
        quota_cost: float,
    ) -> bool:
        criticality = max(0.0, min(1.0, float(criticality)))
        uncertainty = max(0.0, min(1.0, float(uncertainty)))
        blast_radius = max(0.0, min(1.0, float(blast_radius)))
        failure_pressure = min(1.0, max(0, int(repeated_failures)) / 3.0)
        effective_criticality = min(
            1.0,
            criticality * 0.45 + uncertainty * 0.25 + blast_radius * 0.20 + failure_pressure * 0.10,
        )
        return self._council.should_debate(
            expected_terminal_gain=max(0.0, float(expected_terminal_gain)),
            criticality=effective_criticality,
            latency_cost=max(0.0, float(latency_cost)),
            resource_cost=max(0.0, float(quota_cost)),
        )
