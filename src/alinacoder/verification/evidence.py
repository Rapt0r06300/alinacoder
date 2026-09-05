from __future__ import annotations

from .models import DoneContractResult, EvidenceReceipt


class StochasticVerdict:
    @staticmethod
    def from_samples(samples: list[bool], *, min_samples: int = 5, pass_threshold: float = 0.8) -> str:
        if len(samples) < min_samples:
            return "INCONCLUSIVE"
        rate = sum(1 for x in samples if x) / len(samples)
        return "PASS" if rate >= pass_threshold else "FAIL"


class DoneContractEngine:
    def evaluate(
        self,
        obligations: set[str],
        evidence_by_obligation: dict[str, list[EvidenceReceipt]],
        *,
        current_state_hash: str,
        now: float,
    ) -> DoneContractResult:
        missing: set[str] = set()
        for obligation in obligations:
            receipts = evidence_by_obligation.get(obligation, [])
            satisfied = any(receipt.passed and receipt.is_fresh(current_state_hash=current_state_hash, now=now) for receipt in receipts)
            if not satisfied:
                missing.add(obligation)
        total = len(obligations)
        score = 1.0 if total == 0 else (total - len(missing)) / total
        return DoneContractResult(not missing, missing, score)
