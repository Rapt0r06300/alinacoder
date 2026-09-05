from __future__ import annotations

from .models import CompletionDecision, VerificationBundle


class CompletionFirewall:
    def decide(self, bundle: VerificationBundle, *, generator_id: str, verifier_id: str) -> CompletionDecision:
        reasons: list[str] = []
        if generator_id == verifier_id:
            reasons.append("independent")
        if not bundle.hidden_tests:
            reasons.append("hidden")
        if not bundle.compositional_tests:
            reasons.append("compositional")
        if not bundle.mutation_tests:
            reasons.append("mutation")
        if not bundle.verifier_integrity:
            reasons.append("verifier_integrity")
        if not bundle.visible_tests:
            reasons.append("visible")
        return CompletionDecision(not reasons, tuple(reasons))
