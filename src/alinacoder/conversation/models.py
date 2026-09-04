from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Perspective(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class TurnInput:
    turn_id: str
    raw: str
    meaning: str | None = None


@dataclass(frozen=True)
class TurnRecord:
    turn_id: str
    raw: str
    meaning: str


@dataclass(frozen=True)
class ArtifactAnchor:
    artifact_id: str
    kind: str
    locator: str
    selected: bool = False


@dataclass(frozen=True)
class Belief:
    perspective: Perspective
    key: str
    value: str
    confidence: float
    source: str


@dataclass(frozen=True)
class Preference:
    key: str
    value: str
    evidence_id: str


@dataclass
class GroundedIntentContract:
    last_turn_id: str
    turn_count: int
    active_requirements: dict[str, str] = field(default_factory=dict)
    constraints: dict[str, str] = field(default_factory=dict)
    verified_work: dict[str, str] = field(default_factory=dict)
    superseded: list[tuple[str, str]] = field(default_factory=list)
