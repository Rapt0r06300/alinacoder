from __future__ import annotations

from dataclasses import dataclass


class SemanticRegressionDetector:
    def compare(self, before: dict[str, object], after: dict[str, object], *, protected_keys: set[str]) -> set[str]:
        return {key for key in protected_keys if before.get(key) != after.get(key)}


@dataclass(frozen=True)
class DependencyMigrationEvidence:
    package: str
    from_version: str
    to_version: str
    upstream_source: str
    source_hash: str
    breaking_changes: tuple[str, ...] = ()

    def is_admissible(self) -> bool:
        return bool(self.package and self.from_version and self.to_version and self.upstream_source and len(self.source_hash) >= 16)


class SelfCorrectionPolicy:
    def decide(self, *, repeated_fingerprint: bool, evidence_changed: bool, plan_invalidated: bool) -> str:
        if plan_invalidated:
            return "REPLAN_AFFECTED"
        if repeated_fingerprint and not evidence_changed:
            return "NEW_PROBE"
        if evidence_changed:
            return "REASSESS_HYPOTHESES"
        return "PATCH"


@dataclass(frozen=True)
class BehavioralContract:
    name: str
    required: dict[str, object]


class BehavioralContractEvaluator:
    def evaluate(self, contract: BehavioralContract, observed: dict[str, object]) -> bool:
        return all(observed.get(key) == value for key, value in contract.required.items())
