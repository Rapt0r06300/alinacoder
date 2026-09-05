from __future__ import annotations

from pathlib import Path


class SandboxPolicy:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root.resolve()

    def resolve(self, relative_path: str | Path) -> Path:
        candidate = (self.workspace_root / Path(relative_path)).resolve()
        try:
            candidate.relative_to(self.workspace_root)
        except ValueError as exc:
            raise PermissionError("path escapes sandbox workspace") from exc
        return candidate
