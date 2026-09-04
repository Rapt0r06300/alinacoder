from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def checksum_for(session_id: str, version: int, data: dict[str, Any]) -> str:
    payload = canonical_json({"session_id": session_id, "version": version, "data": data})
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class CanonicalSessionState:
    session_id: str
    version: int
    data: dict[str, Any]
    checksum: str
    fencing_epoch: int = 0

    @classmethod
    def build(cls, session_id: str, version: int, data: dict[str, Any], fencing_epoch: int = 0) -> "CanonicalSessionState":
        copied = json.loads(canonical_json(data))
        return cls(session_id, version, copied, checksum_for(session_id, version, copied), fencing_epoch)


@dataclass(frozen=True, slots=True)
class EvidenceReceipt:
    evidence_id: str
    state_checksum: str
    state_version: int
    payload: dict[str, Any]

    @classmethod
    def bind(cls, evidence_id: str, state: CanonicalSessionState, payload: dict[str, Any]) -> "EvidenceReceipt":
        return cls(evidence_id, state.checksum, state.version, json.loads(canonical_json(payload)))

    def is_fresh(self, state: CanonicalSessionState) -> bool:
        return self.state_checksum == state.checksum and self.state_version == state.version


@dataclass(frozen=True, slots=True)
class EventRecord:
    sequence: int
    session_id: str
    version: int
    kind: str
    state_checksum: str
    metadata: dict[str, Any]


@dataclass(frozen=True, slots=True)
class EffectRecord:
    effect_key: str
    session_id: str
    status: str
    payload: dict[str, Any]
    result: dict[str, Any] | None
