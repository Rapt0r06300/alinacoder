from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CapabilityRequirement:
    minimums: dict[str, float]


@dataclass(frozen=True)
class CostProofReceipt:
    provider_id: str
    model_id: str
    prompt_price: float
    completion_price: float
    request_price: float
    verdict: str
    verified_at: datetime
    expires_at: datetime
    hard_overage_block: bool

    def is_admissible(self, now: datetime) -> bool:
        return (
            self.verdict == "PROVEN_ZERO_COST"
            and self.prompt_price == 0.0
            and self.completion_price == 0.0
            and self.request_price == 0.0
            and self.hard_overage_block
            and self.verified_at <= now <= self.expires_at
        )


@dataclass
class ModelRoute:
    provider_id: str
    model_id: str
    lineage: str
    capabilities: dict[str, float]
    cost_proof: CostProofReceipt
    quality_lcb: float
    quota_remaining: int = 1
    healthy: bool = True
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def key(self) -> tuple[str, str]:
        return (self.provider_id, self.model_id)

    def covers(self, requirement: CapabilityRequirement) -> bool:
        return all(self.capabilities.get(name, 0.0) >= level for name, level in requirement.minimums.items())


class RouteUnavailableError(RuntimeError):
    pass


class StaleResponseError(RuntimeError):
    pass
