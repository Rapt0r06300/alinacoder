from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RepairOp(str, Enum):
    REPLACE = "REPLACE"
    CANCEL = "CANCEL"
    NARROW = "NARROW"
    EXTEND = "EXTEND"
    REORDER = "REORDER"
    NEGATE = "NEGATE"
    CONFIRM = "CONFIRM"


@dataclass
class ContextBranch:
    branch_id: str
    parent_id: str | None = None
    facts: dict[str, str] = field(default_factory=dict)
    active: bool = True


class ConversationContextGraph:
    def __init__(self) -> None:
        self.branches: dict[str, ContextBranch] = {"main": ContextBranch("main")}

    def fork(self, branch_id: str, *, parent_id: str = "main") -> ContextBranch:
        if branch_id in self.branches or parent_id not in self.branches:
            raise ValueError("invalid branch")
        branch = ContextBranch(branch_id, parent_id, dict(self.branches[parent_id].facts))
        self.branches[branch_id] = branch
        return branch

    def set_fact(self, branch_id: str, key: str, value: str) -> None:
        self.branches[branch_id].facts[key] = value

    def apply_repair(self, branch_id: str, op: RepairOp, key: str, value: str | None = None) -> None:
        branch = self.branches[branch_id]
        if op in {RepairOp.REPLACE, RepairOp.CONFIRM}:
            if value is None:
                raise ValueError("value required")
            branch.facts[key] = value
        elif op in {RepairOp.CANCEL, RepairOp.NEGATE}:
            branch.facts.pop(key, None)
        elif op == RepairOp.EXTEND:
            if value is None:
                raise ValueError("value required")
            current = branch.facts.get(key, "")
            branch.facts[key] = f"{current}; {value}".strip("; ")
        elif op == RepairOp.NARROW:
            if value is None:
                raise ValueError("value required")
            branch.facts[key] = value
        elif op == RepairOp.REORDER:
            if value is None:
                raise ValueError("value required")
            branch.facts[key] = value


@dataclass(frozen=True)
class MicroTurn:
    text: str
    stable: bool
    source: str = "asr"

    @property
    def may_authorize_mutation(self) -> bool:
        return self.stable and self.source == "user_committed"


class MicroTurnStream:
    def __init__(self) -> None:
        self._turns: list[MicroTurn] = []

    def push(self, text: str, *, stable: bool = False, source: str = "asr") -> MicroTurn:
        turn = MicroTurn(text, stable, source)
        self._turns.append(turn)
        return turn

    def commit_user_turn(self, text: str) -> MicroTurn:
        return self.push(text, stable=True, source="user_committed")


class SemanticPrefetchPolicy:
    SAFE_EFFECTS = {"read", "search", "index_lookup", "git_show", "stat"}

    def may_prefetch(self, effect_kind: str, *, turn_stable: bool) -> bool:
        if effect_kind in self.SAFE_EFFECTS:
            return True
        return bool(turn_stable)


class TechnicalFrenchNormalizer:
    _REPLACEMENTS = {
        "ficher": "fichier",
        "gitub": "github",
        "power chell": "powershell",
        "commite": "commit",
    }

    def normalize(self, text: str) -> str:
        normalized = text
        lowered = normalized.lower()
        for wrong, right in self._REPLACEMENTS.items():
            if wrong in lowered:
                start = lowered.index(wrong)
                normalized = normalized[:start] + right + normalized[start + len(wrong):]
                lowered = normalized.lower()
        return normalized


@dataclass(frozen=True)
class ConversationFailure:
    turn_id: str
    category: str
    raw: str
    corrected_meaning: str


class ConversationFailureReplay:
    def __init__(self) -> None:
        self._failures: list[ConversationFailure] = []

    def record(self, failure: ConversationFailure) -> None:
        self._failures.append(failure)

    def cases(self, category: str | None = None) -> tuple[ConversationFailure, ...]:
        items = self._failures if category is None else [f for f in self._failures if f.category == category]
        return tuple(items)
