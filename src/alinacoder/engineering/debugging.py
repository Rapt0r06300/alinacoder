from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    evidence_matches: int
    discriminating_probe: bool
    falsifiable: bool


class CausalDebugger:
    def rank_hypotheses(self, hypotheses: list[Hypothesis]) -> list[Hypothesis]:
        def score(h: Hypothesis) -> tuple[int, int, int]:
            return (
                1 if h.falsifiable else -10,
                1 if h.discriminating_probe else 0,
                h.evidence_matches,
            )
        return sorted(hypotheses, key=score, reverse=True)


@dataclass(frozen=True)
class RepairAttempt:
    fingerprint: str
    outcome: str
    reason: str


class RepairAttemptGraph:
    def __init__(self) -> None:
        self._attempts: dict[str, RepairAttempt] = {}

    def record(self, fingerprint: str, *, outcome: str, reason: str) -> None:
        self._attempts[fingerprint] = RepairAttempt(fingerprint, outcome, reason)

    def may_retry(self, fingerprint: str) -> bool:
        previous = self._attempts.get(fingerprint)
        return previous is None or previous.outcome not in {"failed", "rejected"}
