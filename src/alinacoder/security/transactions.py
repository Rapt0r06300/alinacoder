from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any


class TransactionError(RuntimeError):
    pass


@dataclass(slots=True)
class _Step:
    key: str
    apply: Callable[[], Any]
    compensate: Callable[[], Any]


class SemanticTransaction:
    def __init__(self, transaction_id: str) -> None:
        if not transaction_id:
            raise ValueError("transaction_id is required")
        self.transaction_id = transaction_id
        self.status = "OPEN"
        self._steps: list[_Step] = []
        self._executed: list[_Step] = []

    @property
    def pending_keys(self) -> tuple[str, ...]:
        return tuple(step.key for step in self._steps[len(self._executed):])

    def stage(self, key: str, apply: Callable[[], Any], compensate: Callable[[], Any]) -> None:
        if self.status != "OPEN":
            raise TransactionError("Cannot stage after transaction closes")
        if not key or any(step.key == key for step in self._steps):
            raise TransactionError("Effect keys must be unique and non-empty")
        self._steps.append(_Step(key, apply, compensate))

    def commit(self) -> tuple[Any, ...]:
        if self.status != "OPEN":
            raise TransactionError(f"Transaction is already {self.status}")
        results: list[Any] = []
        try:
            for step in self._steps:
                result = step.apply()
                self._executed.append(step)
                results.append(result)
        except Exception as exc:
            compensation_errors: list[BaseException] = []
            for step in reversed(self._executed):
                try:
                    step.compensate()
                except BaseException as comp_exc:
                    compensation_errors.append(comp_exc)
            self.status = "ABORTED"
            suffix = f"; compensation errors={len(compensation_errors)}" if compensation_errors else ""
            raise TransactionError(f"Transaction {self.transaction_id} aborted{suffix}") from exc
        self.status = "COMMITTED"
        return tuple(results)

    def abort(self) -> None:
        if self.status != "OPEN":
            raise TransactionError(f"Transaction is already {self.status}")
        self._steps.clear()
        self.status = "ABORTED"
