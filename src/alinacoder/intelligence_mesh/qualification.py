from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .provider_atlas import ProviderSafetyClass


@dataclass(frozen=True, slots=True)
class ZeroCostQualification:
    provider_id: str
    model_id: str
    safe_class: ProviderSafetyClass
    verified_at: datetime
    expires_at: datetime
    prompt_price: float
    completion_price: float
    request_price: float
    hard_overage_block: bool
    account_safe: bool
    source: str

    def admissible(self, now: datetime) -> bool:
        return (
            bool(self.provider_id)
            and bool(self.model_id)
            and bool(self.source)
            and self.verified_at <= now <= self.expires_at
            and float(self.prompt_price) == 0.0
            and float(self.completion_price) == 0.0
            and float(self.request_price) == 0.0
            and bool(self.hard_overage_block)
            and bool(self.account_safe)
        )


@dataclass(frozen=True, slots=True)
class SponsoredCreditQualification:
    provider_id: str
    model_id: str
    verified_at: datetime
    expires_at: datetime
    list_prompt_price: float
    list_completion_price: float
    list_request_price: float
    credit_remaining_usd: float
    platform_funded_lane: bool
    auto_recharge_disabled: bool
    hard_quota_stop: bool
    byok_fallback_disabled: bool
    paid_fallback_disabled: bool
    account_safe: bool
    source: str
    zdr_satisfied: bool = True
    no_training_satisfied: bool = True

    def admissible(self, now: datetime) -> bool:
        return (
            bool(self.provider_id)
            and bool(self.model_id)
            and bool(self.source)
            and self.verified_at <= now <= self.expires_at
            and float(self.list_prompt_price) >= 0.0
            and float(self.list_completion_price) >= 0.0
            and float(self.list_request_price) >= 0.0
            and float(self.credit_remaining_usd) > 0.0
            and bool(self.platform_funded_lane)
            and bool(self.auto_recharge_disabled)
            and bool(self.hard_quota_stop)
            and bool(self.byok_fallback_disabled)
            and bool(self.paid_fallback_disabled)
            and bool(self.account_safe)
            and bool(self.zdr_satisfied)
            and bool(self.no_training_satisfied)
        )


class QualificationRegistry:
    def __init__(self) -> None:
        self._proofs: dict[tuple[str, str], ZeroCostQualification] = {}
        self._sponsored_proofs: dict[tuple[str, str], SponsoredCreditQualification] = {}

    def upsert(self, proof: ZeroCostQualification) -> None:
        if not proof.provider_id or not proof.model_id:
            raise ValueError("qualification must identify an exact provider/model route")
        self._proofs[(proof.provider_id, proof.model_id)] = proof

    def get(self, provider_id: str, model_id: str) -> ZeroCostQualification | None:
        return self._proofs.get((provider_id, model_id))

    def remove(self, provider_id: str, model_id: str) -> None:
        self._proofs.pop((provider_id, model_id), None)

    def admissible(self, provider_id: str, model_id: str, now: datetime) -> bool:
        proof = self.get(provider_id, model_id)
        return bool(proof and proof.admissible(now))

    def upsert_sponsored(self, proof: SponsoredCreditQualification) -> None:
        if not proof.provider_id or not proof.model_id:
            raise ValueError("sponsored qualification must identify an exact provider/model route")
        self._sponsored_proofs[(proof.provider_id, proof.model_id)] = proof

    def get_sponsored(self, provider_id: str, model_id: str) -> SponsoredCreditQualification | None:
        return self._sponsored_proofs.get((provider_id, model_id))

    def remove_sponsored(self, provider_id: str, model_id: str) -> None:
        self._sponsored_proofs.pop((provider_id, model_id), None)

    def sponsored_admissible(self, provider_id: str, model_id: str, now: datetime) -> bool:
        proof = self.get_sponsored(provider_id, model_id)
        return bool(proof and proof.admissible(now))
