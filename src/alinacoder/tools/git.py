from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .models import ProcessReceipt, UnknownResultError
from .process import ManagedProcessRunner


class GitMainExecutor:
    def __init__(self, runner: ManagedProcessRunner | None = None) -> None:
        self.runner = runner or ManagedProcessRunner()

    def validate_target(self, branch: str) -> None:
        if branch != "main":
            raise ValueError("AlinaCoder v0.2 may mutate Git main only")

    def reconcile_after_unknown_result(self, *, expected_head: str, observed_head: str) -> str:
        if observed_head == expected_head:
            return "COMMITTED"
        raise UnknownResultError("mutation outcome unknown; reconcile state before retry")

    def _run(self, workspace: Path | str, argv: Sequence[str], *, timeout_seconds: float = 60) -> ProcessReceipt:
        receipt = self.runner.run(argv, timeout_seconds=timeout_seconds, cwd=str(Path(workspace)))
        if receipt.returncode != 0 or receipt.timed_out:
            raise RuntimeError(
                f"git command failed: {' '.join(argv)} rc={receipt.returncode} stderr={receipt.stderr.strip()}"
            )
        return receipt

    def current_branch(self, workspace: Path | str) -> str:
        return self._run(workspace, ["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()

    def head(self, workspace: Path | str) -> str:
        return self._run(workspace, ["git", "rev-parse", "HEAD"]).stdout.strip()

    def status_porcelain(self, workspace: Path | str) -> str:
        return self._run(workspace, ["git", "status", "--porcelain"]).stdout

    def diff(self, workspace: Path | str) -> str:
        return self._run(workspace, ["git", "diff", "--no-ext-diff", "--unified=3"]).stdout

    def mark_intent_to_add(self, workspace: Path | str, relative_path: str) -> None:
        self.validate_target(self.current_branch(workspace))
        self._run(workspace, ["git", "add", "-N", "--", relative_path])

    def commit_all(self, workspace: Path | str, message: str) -> dict[str, str | bool]:
        branch = self.current_branch(workspace)
        self.validate_target(branch)
        before = self.head(workspace)
        self._run(workspace, ["git", "add", "-A"])
        staged = self._run(workspace, ["git", "diff", "--cached", "--name-only"]).stdout.strip()
        if not staged:
            return {"ok": True, "branch": branch, "head": before, "changed": False}
        self._run(workspace, ["git", "commit", "-m", message], timeout_seconds=120)
        after = self.head(workspace)
        if after == before:
            raise UnknownResultError("commit reported success but HEAD did not advance")
        self.validate_target(self.current_branch(workspace))
        return {"ok": True, "branch": branch, "head": after, "changed": True}
