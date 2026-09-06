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


class QualificationRegistry:
    def __init__(self) -> None:
        self._proofs: dict[tuple[str, str], ZeroCostQualification] = {}

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
