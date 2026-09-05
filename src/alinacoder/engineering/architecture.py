from __future__ import annotations


class ArchitectureFitnessGuard:
    def __init__(self, *, max_complexity_delta: int, max_dependency_delta: int) -> None:
        self.max_complexity_delta = max_complexity_delta
        self.max_dependency_delta = max_dependency_delta

    def check(self, *, complexity_delta: int, dependency_delta: int) -> None:
        if complexity_delta > self.max_complexity_delta:
            raise ValueError("complexity regression exceeds allowed budget")
        if dependency_delta > self.max_dependency_delta:
            raise ValueError("dependency growth exceeds allowed budget")
