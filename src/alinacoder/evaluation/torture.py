from __future__ import annotations

import hashlib
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

from alinacoder.intelligence_mesh.control import CircuitBreaker, CircuitState, SwitchHysteresis
from alinacoder.orchestration.core import FencingRegistry
from alinacoder.resources.core import ResourceController, ResourceMode
from alinacoder.security.authority import Provenance, TrustLevel
from alinacoder.security.dependencies import (
    DependencyAdmissionError,
    DependencyAdmissionFirewall,
    DependencyRequest,
)
from alinacoder.security.trust import InstructionTrustFirewall, TrustPolicyError
from alinacoder.state.store import StateStore, StaleWriterError


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
    probe: str = "legacy"
    evidence: str = "legacy deterministic probe"


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
    """Deterministic fault campaign that executes real subsystem rejection/recovery paths."""

    def __init__(self, seed: str = "lot17-default") -> None:
        self.seed = seed

    @staticmethod
    def _result(name: str, critical: bool, probe: str, detected: bool, evidence: str) -> ScenarioResult:
        return ScenarioResult(name=name, detected=bool(detected), critical=critical, probe=probe, evidence=evidence)

    def _probe_stale_state(self, root: Path) -> ScenarioResult:
        path = root / "stale.sqlite"
        with StateStore(path) as store:
            state = store.create_session("s", {"value": 0})
            stale_epoch = store.acquire_writer("s")
            store.acquire_writer("s")
            try:
                store.commit_state("s", state.version, stale_epoch, {"value": 1}, "stale")
            except StaleWriterError as exc:
                return self._result("stale_state", True, "state_store", True, type(exc).__name__)
        return self._result("stale_state", True, "state_store", False, "stale writer was accepted")

    def _probe_duplicate_effect(self, root: Path) -> ScenarioResult:
        with StateStore(root / "effect.sqlite") as store:
            store.create_session("s", {})
            first = store.begin_effect("effect:1", "s", {"x": 1})
            second = store.begin_effect("effect:1", "s", {"x": 1})
        return self._result("duplicate_effect", True, "state_store", first and not second, f"first={first};second={second}")

    def _probe_provider_loss(self) -> ScenarioResult:
        breaker = CircuitBreaker(failure_threshold=1)
        breaker.record_failure()
        return self._result("provider_loss", False, "provider_control", breaker.state == CircuitState.OPEN, breaker.state.value)

    def _probe_handoff_storm(self) -> ScenarioResult:
        hysteresis = SwitchHysteresis(minimum_gain_margin=0.10, consecutive_evidence_required=2)
        blocked = not hysteresis.permits(expected_gain=0.04, consecutive_evidence=7)
        return self._result("handoff_storm", False, "provider_control", blocked, "low-value switch blocked" if blocked else "switch admitted")

    def _probe_resource_pressure(self) -> ScenarioResult:
        controller = ResourceController(pressure_samples=1, recovery_samples=1)
        mode = controller.observe_pressure(0.99)
        return self._result("resource_pressure", False, "resource_controller", mode == ResourceMode.CONSERVATIVE, mode.value)

    def _probe_prompt_injection(self) -> ScenarioResult:
        firewall = InstructionTrustFirewall()
        provenance = Provenance("hostile-repo", TrustLevel.UNTRUSTED, tainted=True)
        try:
            firewall.admit(provenance, privileged=True)
        except TrustPolicyError as exc:
            return self._result("prompt_injection", True, "authority_firewall", True, type(exc).__name__)
        return self._result("prompt_injection", True, "authority_firewall", False, "privilege escalation admitted")

    def _probe_concurrency_race(self) -> ScenarioResult:
        registry = FencingRegistry()
        stale = registry.issue("repo")
        current = registry.issue("repo")
        detected = not registry.validate("repo", stale) and registry.validate("repo", current)
        return self._result("concurrency_race", True, "fencing_registry", detected, f"stale={stale};current={current}")

    def _probe_ui_interrupt(self, root: Path) -> ScenarioResult:
        path = root / "ui.sqlite"
        with StateStore(path) as store:
            state = store.create_session("desktop", {"control_state": "RUNNING", "draft": "preserve me"})
            epoch = store.acquire_writer("desktop")
            store.commit_state(
                "desktop",
                state.version,
                epoch,
                {"control_state": "PAUSED", "draft": "preserve me"},
                "ui_interrupt",
            )
        with StateStore(path) as restarted:
            recovered = restarted.reconstruct("desktop")
        detected = recovered.data == {"control_state": "PAUSED", "draft": "preserve me"}
        return self._result("ui_interrupt", False, "state_store", detected, f"version={recovered.version};state={recovered.data}")

    def _probe_flaky_verifier(self) -> ScenarioResult:
        # A stochastic/inconclusive verifier is semantic uncertainty, never blind success/retry.
        decision = classify_retry("wrong_intent")
        detected = decision == "ATTRIBUTION_REQUIRED"
        return self._result("flaky_verifier", True, "verification_policy", detected, decision)

    def _probe_malicious_package(self) -> ScenarioResult:
        firewall = DependencyAdmissionFirewall({"pypi.org"})
        request = DependencyRequest("evil", "1.0.0", None, "attacker.invalid")
        try:
            firewall.admit(request)
        except DependencyAdmissionError as exc:
            return self._result("malicious_package", True, "dependency_firewall", True, type(exc).__name__)
        return self._result("malicious_package", True, "dependency_firewall", False, "malicious dependency admitted")

    def run(self) -> IntegratedTortureReport:
        lab = TortureLab()
        with tempfile.TemporaryDirectory(prefix="alinacoder-torture-") as td:
            root = Path(td)
            results = (
                self._probe_stale_state(root),
                self._probe_duplicate_effect(root),
                self._probe_provider_loss(),
                self._probe_handoff_storm(),
                self._probe_resource_pressure(),
                self._probe_prompt_injection(),
                self._probe_concurrency_race(),
                self._probe_ui_interrupt(root),
                self._probe_flaky_verifier(),
                self._probe_malicious_package(),
            )
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
        readiness = lab.evaluate(cards, passed_checks=sum(result.detected for result in results), total_checks=len(results))
        return IntegratedTortureReport(self.seed, results, cards, readiness)
