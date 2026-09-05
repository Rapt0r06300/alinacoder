from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable


class GovernanceSupervisor:
    def __init__(self, protected_prefixes: tuple[str, ...]) -> None:
        self.protected_prefixes = tuple(prefix.replace("\\", "/") for prefix in protected_prefixes)

    def mutation_allowed(self, paths: list[str]) -> bool:
        return not any(
            path.replace("\\", "/").startswith(prefix)
            for path in paths
            for prefix in self.protected_prefixes
        )

    def digest(self) -> str:
        return hashlib.sha256("\n".join(sorted(self.protected_prefixes)).encode()).hexdigest()


@dataclass(frozen=True)
class CandidateMetrics:
    visible_score: float
    validation_score: float
    hidden_score: float


@dataclass(frozen=True)
class EvolutionCandidate:
    candidate_id: str
    substrate: str
    hypothesis: str
    files: tuple[str, ...] = ()
    lineage: str = "candidate"


@dataclass(frozen=True)
class VerifierEvidence:
    verifier_id: str
    lineage: str
    sealed: bool
    verdict: str


@dataclass(frozen=True)
class EvaluationPartitions:
    visible_ids: frozenset[str]
    validation_ids: frozenset[str]
    hidden_ids: frozenset[str]

    def __post_init__(self) -> None:
        if self.visible_ids & self.validation_ids:
            raise ValueError("visible and validation evaluation sets must be disjoint")
        if self.visible_ids & self.hidden_ids:
            raise ValueError("visible and hidden holdouts must be disjoint")
        if self.validation_ids & self.hidden_ids:
            raise ValueError("validation and hidden holdouts must be disjoint")


class EvolutionGate:
    def __init__(self, min_gain: float = 0.01) -> None:
        self.min_gain = min_gain
        self.active_version = "baseline"
        self._rollback_stack: list[str] = []
        self._accepted: set[str] = set()

    def evaluate(self, candidate: EvolutionCandidate, before: CandidateMetrics, after: CandidateMetrics) -> str:
        if after.hidden_score + 1e-12 < before.hidden_score:
            return "REJECT_HIDDEN_REGRESSION"
        if after.validation_score + 1e-12 < before.validation_score:
            return "REJECT_VALIDATION_REGRESSION"
        if min(
            after.validation_score - before.validation_score,
            after.hidden_score - before.hidden_score,
        ) + 1e-12 < self.min_gain:
            return "WATCH_NO_PROVEN_GAIN"
        self._accepted.add(candidate.candidate_id)
        return "PROMOTE"

    def evaluate_certified(
        self,
        candidate: EvolutionCandidate,
        before: CandidateMetrics,
        after: CandidateMetrics,
        verifier_evidence: Iterable[VerifierEvidence],
    ) -> str:
        verdict = self.evaluate(candidate, before, after)
        if verdict != "PROMOTE":
            return verdict
        independent_sealed_pass = any(
            evidence.verdict == "PASS"
            and evidence.sealed
            and evidence.lineage != candidate.lineage
            for evidence in verifier_evidence
        )
        if not independent_sealed_pass:
            self._accepted.discard(candidate.candidate_id)
            return "REJECT_CIRCULAR_AUTHORITY"
        return "PROMOTE"

    def promote(self, candidate: EvolutionCandidate, *, previous_version: str | None = None) -> None:
        if candidate.candidate_id not in self._accepted:
            raise PermissionError("candidate has not passed sealed acceptance")
        self._rollback_stack.append(previous_version or self.active_version)
        self.active_version = candidate.candidate_id

    def rollback(self) -> str:
        if not self._rollback_stack:
            raise RuntimeError("no rollback point")
        self.active_version = self._rollback_stack.pop()
        return self.active_version


@dataclass
class CorrectionRule:
    rule_id: str
    statement: str
    source: str
    scope: str
    active: bool = True
    evidence: tuple[str, ...] = ()


class CorrectionRuleFactory:
    def __init__(self) -> None:
        self._rules: dict[str, CorrectionRule] = {}

    def create(
        self,
        rule_id: str,
        statement: str,
        *,
        source: str,
        scope: str,
        evidence: tuple[str, ...] = (),
    ) -> CorrectionRule:
        if source != "user":
            raise ValueError("durable runtime rules require user provenance")
        if not scope.strip():
            raise ValueError("rule scope is required")
        rule = CorrectionRule(rule_id, statement, source, scope, True, evidence)
        self._rules[rule_id] = rule
        return rule

    def create_validated(
        self,
        rule_id: str,
        statement: str,
        *,
        source: str,
        scope: str,
        evidence: tuple[str, ...],
        tests_passed: bool,
    ) -> CorrectionRule:
        if not evidence:
            raise ValueError("durable correction rules require provenance/evidence")
        if not tests_passed:
            raise ValueError("durable correction rules require passing regression proof")
        return self.create(rule_id, statement, source=source, scope=scope, evidence=evidence)

    def revoke(self, rule_id: str) -> None:
        self._rules[rule_id].active = False

    def get(self, rule_id: str) -> CorrectionRule:
        return self._rules[rule_id]


@dataclass(frozen=True)
class RecordedEvent:
    seq: int
    kind: str
    payload: dict[str, Any]


class BlackBoxRecorder:
    def __init__(self, events: list[RecordedEvent] | None = None) -> None:
        self.events = list(events or [])

    def record(self, kind: str, payload: dict[str, Any]) -> RecordedEvent:
        event = RecordedEvent(
            len(self.events) + 1,
            kind,
            json.loads(json.dumps(payload, sort_keys=True)),
        )
        self.events.append(event)
        return event

    def digest(self) -> str:
        canonical = [dict(seq=e.seq, kind=e.kind, payload=e.payload) for e in self.events]
        return hashlib.sha256(
            json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    def replay(self) -> "BlackBoxRecorder":
        return BlackBoxRecorder(list(self.events))


class FailureTaxonomy:
    RETRYABLE = {"network_timeout", "tool_timeout", "provider_5xx", "rate_limit"}
    ATTRIBUTION_REQUIRED = {
        "context_pollution",
        "wrong_intent",
        "conflicting_outputs",
        "premature_action",
    }

    @classmethod
    def classify(cls, kind: str) -> str:
        if kind in cls.RETRYABLE:
            return "RETRYABLE"
        if kind in cls.ATTRIBUTION_REQUIRED:
            return "ATTRIBUTION_REQUIRED"
        return "UNKNOWN"
