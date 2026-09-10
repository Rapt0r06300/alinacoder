from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import math
from pathlib import Path
import sqlite3
from typing import Callable


def wilson_lower_bound(successes: int, trials: int, z: float = 1.959963984540054) -> float:
    """Return the Wilson lower confidence bound for Bernoulli outcomes."""
    n = int(trials)
    s = int(successes)
    if n <= 0:
        return 0.0
    if s < 0 or s > n:
        raise ValueError("successes must satisfy 0 <= successes <= trials")
    if z <= 0:
        raise ValueError("z must be positive")
    p = s / n
    z2 = z * z
    denominator = 1.0 + z2 / n
    centre = p + z2 / (2.0 * n)
    radius = z * math.sqrt((p * (1.0 - p) + z2 / (4.0 * n)) / n)
    return max(0.0, min(1.0, (centre - radius) / denominator))


@dataclass(frozen=True, slots=True)
class CapabilityObservation:
    successes: int
    trials: int
    benchmark_version: str
    observed_at: str


@dataclass(frozen=True, slots=True)
class ModelCapabilityProfile:
    provider_id: str
    model_id: str
    lineage: str
    dimensions: dict[str, CapabilityObservation]
    context_tokens: int = 0
    benchmark_version: str = ""


class CapabilityProfileStore:
    """Persistent measured capability outcomes used by the runtime router."""

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
            CREATE TABLE IF NOT EXISTS capability_observations(
                provider_id TEXT NOT NULL,
                model_id TEXT NOT NULL,
                lineage TEXT NOT NULL,
                capability TEXT NOT NULL,
                benchmark_version TEXT NOT NULL,
                successes INTEGER NOT NULL DEFAULT 0,
                trials INTEGER NOT NULL DEFAULT 0,
                observed_at TEXT NOT NULL,
                PRIMARY KEY(provider_id, model_id, capability, benchmark_version)
            );
            CREATE INDEX IF NOT EXISTS idx_capability_model
                ON capability_observations(provider_id, model_id, capability);
            """
        )

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "CapabilityProfileStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def record(
        self,
        provider_id: str,
        model_id: str,
        lineage: str,
        capability: str,
        success: bool,
        *,
        benchmark_version: str,
    ) -> None:
        values = (str(provider_id).strip(), str(model_id).strip(), str(lineage).strip(), str(capability).strip(), str(benchmark_version).strip())
        if not all(values):
            raise ValueError("provider, model, lineage, capability and benchmark_version are required")
        observed_at = self._now_fn().astimezone(timezone.utc).isoformat()
        self._conn.execute(
            """
            INSERT INTO capability_observations(
                provider_id,model_id,lineage,capability,benchmark_version,successes,trials,observed_at
            ) VALUES(?,?,?,?,?,?,1,?)
            ON CONFLICT(provider_id,model_id,capability,benchmark_version) DO UPDATE SET
                lineage=excluded.lineage,
                successes=capability_observations.successes + excluded.successes,
                trials=capability_observations.trials + 1,
                observed_at=excluded.observed_at
            """,
            (*values, 1 if success else 0, observed_at),
        )

    def _latest(self, provider_id: str, model_id: str, capability: str) -> sqlite3.Row | None:
        return self._conn.execute(
            """
            SELECT * FROM capability_observations
            WHERE provider_id=? AND model_id=? AND capability=?
            ORDER BY observed_at DESC, benchmark_version DESC LIMIT 1
            """,
            (provider_id, model_id, capability),
        ).fetchone()

    def quality_lcb(
        self,
        provider_id: str,
        model_id: str,
        capability: str,
        *,
        seed_prior: float = 0.5,
    ) -> float:
        row = self._latest(provider_id, model_id, capability)
        prior = max(0.0, min(1.0, float(seed_prior)))
        if row is None:
            return prior * 0.20
        trials = int(row["trials"])
        successes = int(row["successes"])
        if trials < 5:
            # Strong cold-start penalty: a tiny perfect sample must not outrank
            # a route with enough real evidence solely because of a seed prior.
            observed = successes / trials if trials else 0.0
            sample_fraction = trials / 5.0
            return min(prior, observed) * 0.50 * sample_fraction
        return wilson_lower_bound(successes, trials)

    def observation(self, provider_id: str, model_id: str, capability: str) -> CapabilityObservation | None:
        row = self._latest(provider_id, model_id, capability)
        if row is None:
            return None
        return CapabilityObservation(
            int(row["successes"]),
            int(row["trials"]),
            str(row["benchmark_version"]),
            str(row["observed_at"]),
        )

    def capabilities(
        self,
        provider_id: str,
        model_id: str,
        names: tuple[str, ...] | list[str],
        *,
        seed: dict[str, float] | None = None,
    ) -> dict[str, float]:
        seed = dict(seed or {})
        return {
            name: self.quality_lcb(provider_id, model_id, name, seed_prior=seed.get(name, 0.5))
            for name in names
        }
