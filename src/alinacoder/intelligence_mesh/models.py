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
    billing_class: str = "ZERO_PRICE_MODEL"
    sponsored_credit_remaining_usd: float = 0.0
    auto_recharge_disabled: bool = False
    byok_fallback_disabled: bool = False
    paid_fallback_disabled: bool = False

    def is_admissible(self, now: datetime) -> bool:
        fresh = self.verified_at <= now <= self.expires_at
        if not fresh or not self.hard_overage_block:
            return False
        if self.verdict == "PROVEN_ZERO_COST":
            return (
                self.prompt_price == 0.0
                and self.completion_price == 0.0
                and self.request_price == 0.0
            )
        if self.verdict == "SPONSORED_CREDIT_HARD_STOP":
            return (
                self.billing_class == "SPONSORED_CREDIT_HARD_STOP"
                and self.prompt_price >= 0.0
                and self.completion_price >= 0.0
                and self.request_price >= 0.0
                and self.sponsored_credit_remaining_usd > 0.0
                and self.auto_recharge_disabled
                and self.byok_fallback_disabled
                and self.paid_fallback_disabled
            )
        return False


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
