from __future__ import annotations

from .models import UnknownResultError


class GitMainExecutor:
    def validate_target(self, branch: str) -> None:
        if branch != "main":
            raise ValueError("AlinaCoder v0.2 may mutate Git main only")

    def reconcile_after_unknown_result(self, *, expected_head: str, observed_head: str) -> str:
        if observed_head == expected_head:
            return "COMMITTED"
        raise UnknownResultError("mutation outcome unknown; reconcile state before retry")
