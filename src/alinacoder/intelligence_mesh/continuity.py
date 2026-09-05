from __future__ import annotations

from dataclasses import dataclass

from .models import StaleResponseError


@dataclass(frozen=True)
class ContinuityEnvelope:
    session_id: str
    state_version: int
    state_checksum: str
    repo_head: str
    intent_version: str

    def verify(self, *, session_id: str, state_version: int, state_checksum: str, repo_head: str, intent_version: str) -> bool:
        return (
            self.session_id == session_id
            and self.state_version == state_version
            and self.state_checksum == state_checksum
            and self.repo_head == repo_head
            and self.intent_version == intent_version
        )

    def admit_response(self, *, current_state_version: int, current_checksum: str, response_state_version: int, response_checksum: str) -> None:
        if response_state_version != current_state_version or response_checksum != current_checksum:
            raise StaleResponseError("response was computed from stale canonical state")
