from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import secrets


class TrustLevel(IntEnum):
    UNTRUSTED = 0
    OBSERVED = 10
    PROJECT = 50
    USER = 100


@dataclass(frozen=True, slots=True)
class Provenance:
    source: str
    trust: TrustLevel
    tainted: bool = False

    @classmethod
    def user(cls) -> "Provenance":
        return cls("user", TrustLevel.USER, False)


@dataclass(frozen=True, slots=True)
class OwnerPolicy:
    allowed_capabilities: frozenset[str]


@dataclass(frozen=True, slots=True)
class CapabilityToken:
    token_id: str
    subject: str
    capabilities: frozenset[str]
    policy_epoch: int
    parent_token_id: str | None = None

    def allows(self, capability: str) -> bool:
        return capability in self.capabilities


class AuthorityError(RuntimeError):
    pass


class AuthorityBroker:
    def __init__(self, policy: OwnerPolicy) -> None:
        self.policy = policy
        self._epoch = 0
        self._parents: dict[str, str | None] = {}
        self._revoked: set[str] = set()

    @property
    def epoch(self) -> int:
        return self._epoch

    def issue(self, subject: str, requested: set[str] | frozenset[str]) -> CapabilityToken:
        requested_caps = frozenset(requested)
        if not requested_caps.issubset(self.policy.allowed_capabilities):
            extra = sorted(requested_caps - self.policy.allowed_capabilities)
            raise AuthorityError(f"Requested capabilities exceed owner policy: {extra}")
        token = CapabilityToken(secrets.token_hex(16), subject, requested_caps, self._epoch, None)
        self._parents[token.token_id] = None
        return token

    def delegate(self, parent: CapabilityToken, subject: str, requested: set[str] | frozenset[str]) -> CapabilityToken:
        self._validate_live(parent)
        requested_caps = frozenset(requested)
        if not requested_caps.issubset(parent.capabilities):
            extra = sorted(requested_caps - parent.capabilities)
            raise AuthorityError(f"Delegation cannot expand parent authority: {extra}")
        token = CapabilityToken(secrets.token_hex(16), subject, requested_caps, self._epoch, parent.token_id)
        self._parents[token.token_id] = parent.token_id
        return token

    def revoke(self, token_id: str) -> None:
        if token_id not in self._parents:
            raise AuthorityError(f"Unknown capability token: {token_id}")
        self._revoked.add(token_id)

    def revoke_all(self) -> int:
        self._epoch += 1
        self._revoked.clear()
        return self._epoch

    def _validate_live(self, token: CapabilityToken) -> None:
        if token.policy_epoch != self._epoch:
            raise AuthorityError("Stale/revoked capability token")
        if token.token_id not in self._parents:
            raise AuthorityError("Unknown capability token")
        current: str | None = token.token_id
        seen: set[str] = set()
        while current is not None:
            if current in seen:
                raise AuthorityError("Invalid delegation cycle")
            seen.add(current)
            if current in self._revoked:
                raise AuthorityError("Capability token or ancestor was revoked")
            current = self._parents.get(current)

    def validate(self, token: CapabilityToken, capability: str) -> None:
        self._validate_live(token)
        if not token.allows(capability):
            raise AuthorityError(f"Capability not granted: {capability}")
