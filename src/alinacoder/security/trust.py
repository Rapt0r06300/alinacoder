from __future__ import annotations

from dataclasses import dataclass

from .authority import Provenance, TrustLevel


class TrustPolicyError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class InstructionTrustFirewall:
    minimum_privileged_trust: TrustLevel = TrustLevel.USER

    def admit(self, provenance: Provenance, *, privileged: bool) -> None:
        if provenance.tainted:
            raise TrustPolicyError("Tainted instructions cannot authorize privileged execution")
        if privileged and provenance.trust < self.minimum_privileged_trust:
            raise TrustPolicyError("Instruction provenance is below privileged trust threshold")
