from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any, Mapping


_FORBIDDEN_REASONING_KEYS = frozenset(
    {
        "chain_of_thought",
        "cot",
        "hidden_reasoning",
        "raw_reasoning",
        "scratchpad",
        "internal_monologue",
    }
)

_ALLOWED_STATUSES = frozenset({"info", "running", "success", "warning", "error", "stopped"})


def sanitize_activity_details(value: Any) -> Any:
    """Return a JSON-friendly copy with private-reasoning fields removed recursively."""
    if isinstance(value, Mapping):
        return {
            str(key): sanitize_activity_details(item)
            for key, item in value.items()
            if str(key).strip().lower() not in _FORBIDDEN_REASONING_KEYS
        }
    if isinstance(value, list):
        return [sanitize_activity_details(item) for item in value]
    if isinstance(value, tuple):
        return [sanitize_activity_details(item) for item in value]
    if isinstance(value, set):
        return [sanitize_activity_details(item) for item in sorted(value, key=repr)]
    return deepcopy(value)


@dataclass(frozen=True)
class ActivityEvent:
    event_id: str
    timestamp: str
    kind: str
    summary: str
    status: str = "info"
    run_id: str | None = None
    phase: str | None = None
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        if self.status not in _ALLOWED_STATUSES:
            raise ValueError(f"invalid activity status: {self.status}")
        payload = asdict(self)
        payload["details"] = sanitize_activity_details(payload.get("details") or {})
        return payload
