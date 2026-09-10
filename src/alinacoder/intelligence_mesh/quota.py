from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
import sqlite3
from typing import Callable


class QuotaState(str, Enum):
    AVAILABLE = "available"
    DEPLETED_UNTIL_RESET = "depleted_until_reset"
    TEMP_UNHEALTHY = "temp_unhealthy"
    AUTH_BLOCKED = "auth_blocked"
    BILLING_BLOCKED = "billing_blocked"
    RETIRED = "retired"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class QuotaRecord:
    provider_id: str
    model_id: str
    state: QuotaState
    remaining_requests: int | None
    remaining_tokens: int | None
    reset_at: str | None
    cooldown_until: str | None
    consecutive_failures: int
    latency_ewma_ms: float | None
    success_count: int
    failure_count: int
    last_error: str | None
    cost_proof_expires_at: str | None
    reserved: int


class QuotaLedger:
    """Durable quota/health state. It records limits; it never attempts to evade them."""

    def __init__(self, path: Path | str, *, now_fn: Callable[[], datetime] | None = None) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self._conn = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=FULL")
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS quota_routes(
                provider_id TEXT NOT NULL,
                model_id TEXT NOT NULL,
                state TEXT NOT NULL,
                remaining_requests INTEGER,
                remaining_tokens INTEGER,
                reset_at TEXT,
                cooldown_until TEXT,
                consecutive_failures INTEGER NOT NULL DEFAULT 0,
                latency_ewma_ms REAL,
                success_count INTEGER NOT NULL DEFAULT 0,
                failure_count INTEGER NOT NULL DEFAULT 0,
                last_error TEXT,
                cost_proof_expires_at TEXT,
                reserved INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY(provider_id, model_id)
            );
            """
        )

    def close(self) -> None:
        self._conn.close()

    def _now(self) -> datetime:
        value = self._now_fn()
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)

    @staticmethod
    def _iso(value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.astimezone(timezone.utc).isoformat()

    @staticmethod
    def _dt(value: str | None) -> datetime | None:
        if not value:
            return None
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)

    def ensure_route(self, provider_id: str, model_id: str) -> None:
        provider_id, model_id = str(provider_id).strip(), str(model_id).strip()
        if not provider_id or not model_id:
            raise ValueError("provider_id and model_id are required")
        self._conn.execute(
            "INSERT OR IGNORE INTO quota_routes(provider_id,model_id,state) VALUES(?,?,?)",
            (provider_id, model_id, QuotaState.AVAILABLE.value),
        )

    def get(self, provider_id: str, model_id: str) -> QuotaRecord:
        self.ensure_route(provider_id, model_id)
        row = self._conn.execute(
            "SELECT * FROM quota_routes WHERE provider_id=? AND model_id=?",
            (provider_id, model_id),
        ).fetchone()
        assert row is not None
        return QuotaRecord(
            str(row["provider_id"]), str(row["model_id"]), QuotaState(str(row["state"])),
            row["remaining_requests"], row["remaining_tokens"], row["reset_at"], row["cooldown_until"],
            int(row["consecutive_failures"]), row["latency_ewma_ms"], int(row["success_count"]),
            int(row["failure_count"]), row["last_error"], row["cost_proof_expires_at"], int(row["reserved"]),
        )

    def eligible(self, provider_id: str, model_id: str) -> bool:
        record = self.get(provider_id, model_id)
        now = self._now()
        if record.state in {QuotaState.AUTH_BLOCKED, QuotaState.BILLING_BLOCKED, QuotaState.RETIRED, QuotaState.UNKNOWN}:
            return False
        until = self._dt(record.cooldown_until) or self._dt(record.reset_at)
        if record.state in {QuotaState.DEPLETED_UNTIL_RESET, QuotaState.TEMP_UNHEALTHY}:
            if until is None or now < until:
                return False
            self._conn.execute(
                "UPDATE quota_routes SET state=?,consecutive_failures=0,cooldown_until=NULL WHERE provider_id=? AND model_id=?",
                (QuotaState.AVAILABLE.value, provider_id, model_id),
            )
            record = self.get(provider_id, model_id)
        if record.remaining_requests is not None and record.remaining_requests - record.reserved <= 0:
            reset = self._dt(record.reset_at)
            if reset is None or now < reset:
                return False
        return True

    def reserve(self, provider_id: str, model_id: str, units: int = 1) -> bool:
        units = max(1, int(units))
        if not self.eligible(provider_id, model_id):
            return False
        record = self.get(provider_id, model_id)
        if record.remaining_requests is not None and record.remaining_requests - record.reserved < units:
            return False
        self._conn.execute(
            "UPDATE quota_routes SET reserved=reserved+? WHERE provider_id=? AND model_id=?",
            (units, provider_id, model_id),
        )
        return True

    def release(self, provider_id: str, model_id: str, units: int = 1, *, consumed: bool = False) -> None:
        record = self.get(provider_id, model_id)
        units = min(max(1, int(units)), record.reserved)
        remaining = record.remaining_requests
        if consumed and remaining is not None:
            remaining = max(0, remaining - units)
        self._conn.execute(
            "UPDATE quota_routes SET reserved=MAX(0,reserved-?),remaining_requests=? WHERE provider_id=? AND model_id=?",
            (units, remaining, provider_id, model_id),
        )

    def observe_response(
        self,
        provider_id: str,
        model_id: str,
        *,
        remaining_requests: int | None = None,
        remaining_tokens: int | None = None,
        reset_at: datetime | None = None,
        latency_ms: float | None = None,
        cost_proof_expires_at: datetime | None = None,
    ) -> None:
        record = self.get(provider_id, model_id)
        latency = record.latency_ewma_ms
        if latency_ms is not None:
            latency = float(latency_ms) if latency is None else latency * 0.8 + float(latency_ms) * 0.2
        state = QuotaState.AVAILABLE
        if remaining_requests is not None and int(remaining_requests) <= 0:
            state = QuotaState.DEPLETED_UNTIL_RESET
        self._conn.execute(
            """
            UPDATE quota_routes SET state=?,remaining_requests=COALESCE(?,remaining_requests),
                remaining_tokens=COALESCE(?,remaining_tokens),reset_at=COALESCE(?,reset_at),
                cooldown_until=NULL,consecutive_failures=0,latency_ewma_ms=?,success_count=success_count+1,
                last_error=NULL,cost_proof_expires_at=COALESCE(?,cost_proof_expires_at)
            WHERE provider_id=? AND model_id=?
            """,
            (state.value, remaining_requests, remaining_tokens, self._iso(reset_at), latency,
             self._iso(cost_proof_expires_at), provider_id, model_id),
        )

    def observe_error(
        self,
        provider_id: str,
        model_id: str,
        *,
        code: str,
        retry_after_seconds: float | int | None = None,
        reset_at: datetime | None = None,
    ) -> None:
        record = self.get(provider_id, model_id)
        normalized = str(code).upper()
        now = self._now()
        cooldown: datetime | None = None
        if retry_after_seconds is not None:
            cooldown = now + timedelta(seconds=max(0.0, float(retry_after_seconds)))
        if reset_at is not None and (cooldown is None or reset_at > cooldown):
            cooldown = reset_at
        failures = record.consecutive_failures + 1
        if normalized == "QUOTA_EXHAUSTED":
            state = QuotaState.DEPLETED_UNTIL_RESET
            cooldown = cooldown or (now + timedelta(minutes=5))
        elif normalized == "BILLING_BLOCKED":
            state = QuotaState.BILLING_BLOCKED
        elif normalized in {"AUTH_REQUIRED", "AUTH_BLOCKED"}:
            state = QuotaState.AUTH_BLOCKED
        elif normalized in {"RETIRED"}:
            state = QuotaState.RETIRED
        elif normalized in {"UNAVAILABLE", "NETWORK_ERROR", "TIMEOUT", "INVALID_RESPONSE"} and failures >= 2:
            state = QuotaState.TEMP_UNHEALTHY
            cooldown = cooldown or (now + timedelta(seconds=min(300, 15 * failures)))
        else:
            state = QuotaState.AVAILABLE
        self._conn.execute(
            """
            UPDATE quota_routes SET state=?,cooldown_until=?,reset_at=COALESCE(?,reset_at),
                consecutive_failures=?,failure_count=failure_count+1,last_error=?
            WHERE provider_id=? AND model_id=?
            """,
            (state.value, self._iso(cooldown), self._iso(reset_at), failures, normalized, provider_id, model_id),
        )
