from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from alinacoder.state.store import StateStore
from .authority import AuthorityBroker, AuthorityError, CapabilityToken, Provenance, TrustLevel


class EffectDenied(RuntimeError):
    pass

class DuplicateEffectError(EffectDenied):
    pass


@dataclass(frozen=True, slots=True)
class EffectAdmissionReceipt:
    effect_key: str
    capability: str
    state_version: int
    policy_epoch: int


class ExternalEffectGate:
    def __init__(self, store: StateStore, authority: AuthorityBroker) -> None:
        self.store = store
        self.authority = authority

    def admit(self, effect_key: str, session_id: str, capability: str, token: CapabilityToken, expected_state_version: int, instruction_provenance: Provenance, payload: dict[str, Any]) -> EffectAdmissionReceipt:
        try:
            self.authority.validate(token, capability)
        except AuthorityError as exc:
            raise EffectDenied(str(exc)) from exc
        current = self.store.get_state(session_id)
        if current.version != expected_state_version:
            raise EffectDenied(f"Stale state: expected {expected_state_version}, current {current.version}")
        if instruction_provenance.tainted or instruction_provenance.trust < TrustLevel.USER:
            raise EffectDenied("Untrusted/tainted instruction cannot authorize a durable privileged effect")
        if not self.store.begin_effect(effect_key, session_id, {"capability": capability, "payload": payload}):
            raise DuplicateEffectError(f"Effect already recorded: {effect_key}")
        return EffectAdmissionReceipt(effect_key, capability, current.version, token.policy_epoch)
