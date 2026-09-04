from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any


class SpecCompileError(RuntimeError):
    pass


def git_blob_sha_bytes(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


@dataclass(frozen=True, slots=True)
class SpecCompileResult:
    valid: bool
    manifest_path: Path
    current_spec_path: Path
    invariants: tuple[str, ...]
    validated_documents: tuple[Path, ...]


class SpecCompiler:
    def __init__(self, repository_root: Path | str) -> None:
        self.root = Path(repository_root).resolve()

    def _safe_path(self, relative: str) -> Path:
        candidate = (self.root / relative).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise SpecCompileError(f"Manifest path escapes repository root: {relative}") from exc
        return candidate

    def _verify_document(self, item: dict[str, Any]) -> Path:
        relative = item.get("path")
        expected = item.get("source_hash")
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise SpecCompileError("Document entry requires path and source_hash")
        path = self._safe_path(relative)
        if not path.is_file():
            raise SpecCompileError(f"Missing normative document: {relative}")
        actual = git_blob_sha_bytes(path.read_bytes())
        if actual != expected:
            raise SpecCompileError(f"Normative document hash mismatch for {relative}: expected {expected}, got {actual}")
        return path

    def compile(self, manifest_path: Path | str) -> SpecCompileResult:
        manifest_path = Path(manifest_path)
        if not manifest_path.is_absolute():
            manifest_path = (self.root / manifest_path).resolve()
        if not manifest_path.is_file():
            raise SpecCompileError(f"Missing manifest: {manifest_path}")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeError) as exc:
            raise SpecCompileError("Invalid normative manifest") from exc
        policy = manifest.get("resolution_policy", {})
        unresolved = policy.get("unresolved_conflicts", manifest.get("unresolved_conflicts", []))
        if unresolved:
            raise SpecCompileError(f"Unresolved normative conflicts: {unresolved}")
        current_item = manifest.get("current_spec")
        if not isinstance(current_item, dict):
            raise SpecCompileError("Manifest requires current_spec")
        current_path = self._verify_document(current_item)
        current_text = current_path.read_text(encoding="utf-8")
        invariants = tuple(manifest.get("constitutional_invariants", ()))
        missing = [rule for rule in invariants if not isinstance(rule, str) or rule not in current_text]
        if missing:
            raise SpecCompileError(f"Consolidated spec omits constitutional invariants: {missing}")
        validated: list[Path] = [current_path]
        for item in manifest.get("active_documents", []):
            if not isinstance(item, dict):
                raise SpecCompileError("Invalid active document entry")
            validated.append(self._verify_document(item))
        return SpecCompileResult(True, manifest_path, current_path, invariants, tuple(dict.fromkeys(validated)))
