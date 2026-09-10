from __future__ import annotations

from copy import deepcopy
from dataclasses import fields
from typing import Any

from alinacoder.state.store import StateStore
from .models import CognitiveState


class CognitiveStateStore:
    """Event-backed cognitive subdocument layered onto the canonical StateStore."""

    def __init__(self, store: StateStore, session_id: str) -> None:
        self.store = store
        self.session_id = str(session_id)
        # Fail early for unknown sessions without rewriting legacy state merely
        # because a reader constructed this facade.
        self.store.get_state(self.session_id)

    def snapshot(self) -> CognitiveState:
        state = self.store.get_state(self.session_id)
        raw = state.data.get("cognitive", {})
        cognitive = CognitiveState.from_dict(raw if isinstance(raw, dict) else {})
        return CognitiveState.from_dict({**cognitive.to_dict(), "state_version": state.version})

    def update(self, **changes: Any) -> CognitiveState:
        allowed = {field.name for field in fields(CognitiveState)} - {"state_version"}
        unknown = set(changes) - allowed
        if unknown:
            raise ValueError(f"unknown cognitive fields: {sorted(unknown)}")
        state = self.store.get_state(self.session_id)
        current = CognitiveState.from_dict(state.data.get("cognitive", {}))
        payload = current.to_dict()
        payload.update(deepcopy(changes))
        payload["state_version"] = state.version + 1
        updated = CognitiveState.from_dict(payload)
        data = deepcopy(state.data)
        data["cognitive"] = updated.to_dict()
        epoch = self.store.acquire_writer(self.session_id)
        committed = self.store.commit_state(
            self.session_id,
            state.version,
            epoch,
            data,
            "cognitive_state_updated",
            {
                "changed_fields": sorted(changes),
                "intent_revision": updated.intent_revision,
                "plan_revision": updated.plan_revision,
                "current_phase": updated.current_phase,
            },
        )
        return CognitiveState.from_dict({**updated.to_dict(), "state_version": committed.version})
