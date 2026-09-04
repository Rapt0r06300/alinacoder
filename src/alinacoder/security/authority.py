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

    def allows(self, capability: str) -> bool:
        return capability in self.capabilities


class AuthorityError(RuntimeError):
    pass


class AuthorityBroker:
    def __init__(self, policy: OwnerPolicy) -> None:
        self.policy = policy
        self._epoch = 0

    @property
    def epoch(self) -> int:
        return self._epoch

    def issue(self, subject: str, requested: set[str] | frozenset[str]) -> CapabilityToken:
        requested_caps = frozenset(requested)
        if not requested_caps.issubset(self.policy.allowed_capabilities):
            extra = sorted(requested_caps - self.policy.allowed_capabilities)
            raise AuthorityError(f"Requested capabilities exceed owner policy: {extra}")
        return CapabilityToken(secrets.token_hex(16), subject, requested_caps, self._epoch)

    def revoke_all(self) -> int:
        self._epoch += 1
        return self._epoch

    def validate(self, token: CapabilityToken, capability: str) -> None:
        if token.policy_epoch != self._epoch:
            raise AuthorityError("Stale/revoked capability token")
        if not token.allows(capability):
            raise AuthorityError(f"Capability not granted: {capability}")
