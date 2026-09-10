from __future__ import annotations

from dataclasses import dataclass

from .models import EvidenceReceipt


@dataclass(slots=True)
class VerificationEntry:
    key: str
    receipt: EvidenceReceipt
    paths: tuple[str, ...]
    valid: bool = True
    stale_reason: str | None = None


class VerificationKernel:
    """Deterministic authority over fresh, state-bound completion evidence."""

    def __init__(self) -> None:
        self._entries: dict[str, list[VerificationEntry]] = {}

    def add(self, key: str, receipt: EvidenceReceipt, *, paths: tuple[str, ...] | list[str] = ()) -> None:
        if not key or not receipt.verifier_id:
            raise ValueError("verification key and verifier are required")
        self._entries.setdefault(str(key), []).append(
            VerificationEntry(str(key), receipt, tuple(dict.fromkeys(str(path) for path in paths)))
        )

    def certify(self, key: str, *, current_state_hash: str, now: float) -> bool:
        return any(
            entry.valid
            and entry.receipt.passed
            and entry.receipt.is_fresh(current_state_hash=current_state_hash, now=now)
            for entry in self._entries.get(str(key), ())
        )

    def invalidate_for_paths(self, paths: tuple[str, ...] | list[str], reason: str) -> tuple[str, ...]:
        affected_paths = {str(path) for path in paths}
        invalidated: set[str] = set()
        for key, entries in self._entries.items():
            for entry in entries:
                if entry.valid and affected_paths.intersection(entry.paths):
                    entry.valid = False
                    entry.stale_reason = str(reason)
                    invalidated.add(key)
        return tuple(sorted(invalidated))

    def invalidate_state(self, state_hash: str, reason: str) -> tuple[str, ...]:
        invalidated: set[str] = set()
        for key, entries in self._entries.items():
            for entry in entries:
                if entry.valid and entry.receipt.state_hash == state_hash:
                    entry.valid = False
                    entry.stale_reason = str(reason)
                    invalidated.add(key)
        return tuple(sorted(invalidated))
