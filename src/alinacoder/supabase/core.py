from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


def reciprocal_rank_fusion(rankings: list[list[str]], *, k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, item in enumerate(ranking, start=1):
            scores[item] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))


class IdempotentQueueConsumer:
    def __init__(self) -> None:
        self._seen: dict[str, int] = {}

    def admit(self, message_id: str, *, fence: int, minimum_fence: int = 0) -> bool:
        if fence < minimum_fence:
            return False
        previous = self._seen.get(message_id)
        if previous is not None and fence <= previous:
            return False
        self._seen[message_id] = fence
        return True


@dataclass
class SupabaseMirror:
    enabled: bool
    project_id: str
    tenant_id: str
    healthy: bool = True
    last_error: str | None = None

    @property
    def mode(self) -> str:
        return "MIRROR" if self.enabled and self.healthy else "LOCAL_ONLY"

    def mark_unhealthy(self, reason: str) -> None:
        self.healthy = False
        self.last_error = reason

    def mark_healthy(self) -> None:
        self.healthy = True
        self.last_error = None

    def validate_scope(self, *, project_id: str, tenant_id: str) -> None:
        if project_id != self.project_id or tenant_id != self.tenant_id:
            raise PermissionError("cross-project/tenant mirror access denied")

    def write_non_secret(self, record: dict) -> str:
        if record.get("secret") is True or any(
            key.lower() in {"token", "password", "api_key"} and bool(value)
            for key, value in record.items()
        ):
            raise PermissionError("secrets may not be mirrored")
        return self.mode

    def private_channel(self, suffix: str) -> str:
        return f"private:{self.tenant_id}:{self.project_id}:{suffix}"


class MigrationContract:
    """Static, deterministic validation for the optional Supabase migration pair."""

    def __init__(self, migrations_dir: Path | str) -> None:
        self.migrations_dir = Path(migrations_dir)

    def validate(self) -> dict:
        up_paths = sorted(
            path
            for path in self.migrations_dir.glob("*.sql")
            if not path.name.endswith(".down.sql")
        )
        down_paths = sorted(self.migrations_dir.glob("*.down.sql"))
        up_names = [path.name for path in up_paths]
        down_names = [path.name for path in down_paths]
        paired = all(
            self.migrations_dir.joinpath(path.name.removesuffix(".sql") + ".down.sql").exists()
            for path in up_paths
        )
        up_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in up_paths)
        down_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in down_paths)
        rls_authenticated = (
            "enable row level security" in up_text
            and "to authenticated" in up_text
            and "auth.jwt()" in up_text
        )
        queue_warning = (
            "at-least-once" in up_text
            and "idempot" in up_text
            and "fencing" in up_text
        )
        rollback_drops_mirror = "drop table if exists public.alinacoder_memory_mirror" in down_text
        valid = bool(up_paths) and paired and rls_authenticated and queue_warning and rollback_drops_mirror
        return {
            "valid": valid,
            "up": up_names,
            "down": down_names,
            "paired": paired,
            "rls_authenticated": rls_authenticated,
            "pgmq_idempotency_warning": queue_warning,
            "rollback_drops_mirror": rollback_drops_mirror,
        }
