from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Requirement:
    requirement_id: str
    text: str
    source: str
    explicit: bool = True


@dataclass
class Assumption:
    assumption_id: str
    text: str
    source: str
    verified: bool = False


class RequirementRecoveryGraph:
    def __init__(self) -> None:
        self.requirements: dict[str, Requirement] = {}
        self.assumptions: dict[str, Assumption] = {}
        self.unknowns: set[str] = set()

    def require(self, requirement_id: str, text: str, *, source: str, explicit: bool = True) -> None:
        self.requirements[requirement_id] = Requirement(requirement_id, text, source, explicit)

    def assume(self, assumption_id: str, text: str, *, source: str) -> None:
        self.assumptions[assumption_id] = Assumption(assumption_id, text, source, False)

    def verify_assumption(self, assumption_id: str) -> None:
        self.assumptions[assumption_id].verified = True

    def unknown(self, unknown_id: str, text: str) -> None:
        self.unknowns.add(unknown_id)

    def resolve_unknown(self, unknown_id: str) -> None:
        self.unknowns.discard(unknown_id)

    def unresolved_unknowns(self) -> set[str]:
        return set(self.unknowns)
