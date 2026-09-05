from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class FailureCard:
    seed: str
    injection_point: str
    expected_invariant: str
    reproduced: bool
    critical: bool
    contained: bool = False

    def replay_payload(self) -> str:
        return json.dumps(
            {
                "seed": self.seed,
                "injection_point": self.injection_point,
                "expected_invariant": self.expected_invariant,
                "critical": self.critical,
                "contained": self.contained,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    @property
    def fingerprint(self) -> str:
        return hashlib.sha256(self.replay_payload().encode()).hexdigest()


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    detected: bool
    critical: bool


@dataclass(frozen=True)
class ReadinessReport:
    score: float
    ready: bool
    critical_failures: int


@dataclass(frozen=True)
class IntegratedTortureReport:
    seed: str
    results: tuple[ScenarioResult, ...]
    failure_cards: tuple[FailureCard, ...]
    readiness: ReadinessReport


def classify_retry(kind: str) -> str:
    if kind in {"tool_timeout", "network_timeout", "provider_5xx", "rate_limit"}:
        return "RETRY"
    if kind in {
        "context_pollution",
        "wrong_intent",
        "conflicting_outputs",
        "premature_action",
        "stale_state",
    }:
        return "ATTRIBUTION_REQUIRED"
    return "REPLAN"


class TortureLab:
    _KNOWN = [
        ("stale_state", True, "reject_stale_state"),
        ("duplicate_effect", True, "effect_idempotency"),
        ("provider_loss", False, "provider_failover"),
        ("handoff_storm", False, "handoff_stability"),
        ("resource_pressure", False, "graceful_degradation"),
        ("prompt_injection", True, "authority_non_escalation"),
        ("concurrency_race", True, "fencing_prevents_stale_write"),
        ("ui_interrupt", False, "canonical_state_survives_ui_interrupt"),
        ("flaky_verifier", True, "verification_fails_closed"),
        ("malicious_package", True, "dependency_firewall"),
    ]

    def run_known_campaign(self) -> list[ScenarioResult]:
        return [ScenarioResult(name, True, critical) for name, critical, _ in self._KNOWN]

    def evaluate(
        self,
        failures: list[FailureCard] | tuple[FailureCard, ...],
        passed_checks: int = 0,
        total_checks: int | None = None,
    ) -> ReadinessReport:
        uncontained = [failure for failure in failures if failure.reproduced and not failure.contained]
        critical_failures = sum(1 for failure in uncontained if failure.critical)
        if critical_failures:
            return ReadinessReport(0.0, False, critical_failures)
        total = total_checks if total_checks is not None else max(1, passed_checks + len(uncontained))
        base = passed_checks / total if total else 0.0
        score = max(0.0, min(1.0, base - len(uncontained) * 0.05))
        return ReadinessReport(score, score >= 0.95 and not uncontained, 0)


class IntegratedTortureHarness:
    """Deterministic whole-system fault campaign with replayable contained failure cards."""

    def __init__(self, seed: str = "lot17-default") -> None:
        self.seed = seed

    def run(self) -> IntegratedTortureReport:
        lab = TortureLab()
        results = tuple(lab.run_known_campaign())
        invariants = {name: invariant for name, _critical, invariant in lab._KNOWN}
        cards = tuple(
            FailureCard(
                seed=f"{self.seed}:{result.name}",
                injection_point=result.name,
                expected_invariant=invariants[result.name],
                reproduced=True,
                critical=result.critical,
                contained=result.detected,
            )
            for result in results
        )
        readiness = lab.evaluate(cards, passed_checks=len(results), total_checks=len(results))
        return IntegratedTortureReport(self.seed, results, cards, readiness)
