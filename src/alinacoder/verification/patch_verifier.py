from __future__ import annotations

from .models import PatchVerificationReport


class BidirectionalPatchVerifier:
    def verify(self, *, intended_obligations: set[str], reconstructed_obligations: set[str]) -> PatchVerificationReport:
        missing = set(intended_obligations) - set(reconstructed_obligations)
        unexpected = set(reconstructed_obligations) - set(intended_obligations)
        return PatchVerificationReport(not missing, missing, unexpected)
