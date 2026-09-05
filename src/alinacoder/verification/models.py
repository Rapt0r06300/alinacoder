from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceReceipt:
    evidence_type: str
    verifier_id: str
    state_hash: str
    artifact_hash: str
    passed: bool
    observed_at: float
    expires_at: float

    def is_fresh(self, *, current_state_hash: str, now: float) -> bool:
        return self.state_hash == current_state_hash and self.observed_at <= now <= self.expires_at


@dataclass(frozen=True)
class VerificationBundle:
    visible_tests: bool
    hidden_tests: bool
    compositional_tests: bool
    mutation_tests: bool
    verifier_integrity: bool


@dataclass(frozen=True)
class CompletionDecision:
    allowed: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class PatchVerificationReport:
    accepted: bool
    missing: set[str]
    unexpected: set[str]


@dataclass(frozen=True)
class DoneContractResult:
    ready: bool
    missing: set[str]
    readiness_score: float
