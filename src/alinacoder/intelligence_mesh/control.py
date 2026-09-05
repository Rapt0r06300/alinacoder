from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 2) -> None:
        self.failure_threshold = max(1, failure_threshold)
        self.failures = 0
        self.state = CircuitState.CLOSED

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def probe(self) -> None:
        if self.state == CircuitState.OPEN:
            self.state = CircuitState.HALF_OPEN

    def record_success(self) -> None:
        self.failures = 0
        self.state = CircuitState.CLOSED


class QuotaPortfolio:
    def __init__(self) -> None:
        self._remaining: dict[tuple[str, str], int] = {}
        self._reserved: dict[tuple[str, str], int] = {}

    def set_quota(self, provider_id: str, model_id: str, remaining: int) -> None:
        self._remaining[(provider_id, model_id)] = max(0, remaining)

    def reserve(self, provider_id: str, model_id: str, units: int = 1) -> bool:
        key = (provider_id, model_id)
        units = max(1, units)
        available = self._remaining.get(key, 0) - self._reserved.get(key, 0)
        if available < units:
            return False
        self._reserved[key] = self._reserved.get(key, 0) + units
        return True

    def release(self, provider_id: str, model_id: str, units: int = 1, *, consumed: bool = False) -> None:
        key = (provider_id, model_id)
        units = min(max(1, units), self._reserved.get(key, 0))
        self._reserved[key] = self._reserved.get(key, 0) - units
        if consumed:
            self._remaining[key] = max(0, self._remaining.get(key, 0) - units)

    def available(self, provider_id: str, model_id: str) -> int:
        key = (provider_id, model_id)
        return max(0, self._remaining.get(key, 0) - self._reserved.get(key, 0))


@dataclass(frozen=True)
class TaskAffinityLease:
    task_id: str
    lineage: str
    started_tick: int
    minimum_dwell: int = 2

    def dwell_satisfied(self, current_tick: int) -> bool:
        return current_tick - self.started_tick >= self.minimum_dwell


@dataclass(frozen=True)
class SwitchHysteresis:
    minimum_gain_margin: float = 0.1
    consecutive_evidence_required: int = 2

    def permits(self, *, expected_gain: float, consecutive_evidence: int, hard_ineligible: bool = False) -> bool:
        if hard_ineligible:
            return True
        return expected_gain >= self.minimum_gain_margin and consecutive_evidence >= self.consecutive_evidence_required


class EnrollmentState(str, Enum):
    UNENROLLED = "UNENROLLED"
    CONNECTED = "CONNECTED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


@dataclass
class ProviderEnrollment:
    provider_id: str
    auth_method: str
    state: EnrollmentState = EnrollmentState.UNENROLLED

    def connect(self) -> None:
        if self.auth_method not in {"NO_AUTH", "API_KEY", "OAUTH", "DEVICE_FLOW", "PKCE"}:
            raise ValueError("unsupported official auth method")
        self.state = EnrollmentState.CONNECTED

    def revoke(self) -> None:
        self.state = EnrollmentState.REVOKED


@dataclass(frozen=True)
class ProtocolAdapter:
    protocol: str

    def normalize_request(self, messages: list[dict[str, str]]) -> dict[str, object]:
        if self.protocol not in {"openai_chat", "responses", "gemini", "anthropic_messages", "ollama"}:
            raise ValueError("unsupported protocol")
        if not messages:
            raise ValueError("messages required")
        return {"protocol": self.protocol, "messages": list(messages)}
