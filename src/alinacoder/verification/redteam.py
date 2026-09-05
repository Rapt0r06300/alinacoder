from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum


class EvidenceType(str, Enum):
    VISIBLE = "visible"
    HIDDEN = "hidden"
    COMPOSITIONAL = "compositional"
    MUTATION = "mutation"
    METAMORPHIC = "metamorphic"
    DIFFERENTIAL = "differential"
    FORMAL = "formal"


class EvidenceGapMiner:
    def missing(self, required: set[EvidenceType], observed: set[EvidenceType]) -> set[EvidenceType]:
        return set(required) - set(observed)


class VerifierIntegrityGuard:
    def __init__(self, expected_hash: str) -> None:
        self.expected_hash = expected_hash

    @staticmethod
    def hash_source(source: str) -> str:
        return hashlib.sha256(source.encode("utf-8")).hexdigest()

    def verify(self, source: str) -> bool:
        return self.hash_source(source) == self.expected_hash


@dataclass(frozen=True)
class RedTeamOutcome:
    accepted: bool
    reason: str


class RedTeamVerifierLoop:
    """Deterministic hacker→fixer→solver admission checks.

    A candidate is rejected if it changed verifier integrity or relies only on
    visible tests. This keeps the generator from gaming its own evaluator.
    """

    def assess(
        self,
        *,
        visible_passed: bool,
        hidden_passed: bool,
        compositional_passed: bool,
        verifier_integrity: bool,
    ) -> RedTeamOutcome:
        if not verifier_integrity:
            return RedTeamOutcome(False, "verifier_tampering")
        if visible_passed and not hidden_passed:
            return RedTeamOutcome(False, "visible_only_gaming")
        if not compositional_passed:
            return RedTeamOutcome(False, "composition_gap")
        if visible_passed and hidden_passed and compositional_passed:
            return RedTeamOutcome(True, "independent_gates_passed")
        return RedTeamOutcome(False, "insufficient_evidence")
