from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlinaConfig:
    max_paid_spend_eur: float = 0.0
    allow_pay_as_you_go: bool = False
    allow_automatic_credit_purchase: bool = False
    allow_automatic_plan_upgrade: bool = False
    allow_paid_fallback: bool = False
    allow_auto_reload: bool = False
    canonical_branch: str = "main"

    def validate(self) -> None:
        if self.max_paid_spend_eur != 0.0:
            raise ValueError("AlinaCoder v0.2 requires MAX_PAID_SPEND_EUR=0.00")
        if any((self.allow_pay_as_you_go, self.allow_automatic_credit_purchase, self.allow_automatic_plan_upgrade, self.allow_paid_fallback, self.allow_auto_reload)):
            raise ValueError("Autonomous paid/billing escalation is forbidden")
        if self.canonical_branch != "main":
            raise ValueError("Canonical branch must be main")
