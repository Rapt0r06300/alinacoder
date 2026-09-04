from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .store import MemoryStore
from alinacoder.repo.index import RepositoryIndex


class ContextBudgetError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class CompiledContext:
    text: str
    memory_ids: tuple[str, ...]
    symbol_refs: tuple[str, ...]


class ContextCompiler:
    def __init__(self, memories: MemoryStore, repo_index: RepositoryIndex) -> None:
        self.memories = memories
        self.repo_index = repo_index

    def compile(self, project_id: str, query: str, *, repo_root: Path | str | None = None, required_constraints: list[str] | None = None, evidence: list[str] | None = None, max_chars: int = 4000) -> CompiledContext:
        if max_chars <= 0:
            raise ContextBudgetError("Context budget must be positive")
        if repo_root is not None:
            self.memories.refresh_source_freshness(project_id, repo_root)
        mandatory = [f"[CONSTRAINT] {x}" for x in (required_constraints or [])]
        mandatory += [f"[EVIDENCE] {x}" for x in (evidence or [])]
        mandatory_text = "\n".join(mandatory)
        if len(mandatory_text) > max_chars:
            raise ContextBudgetError("Mandatory constraints/evidence exceed context budget")
        lines = list(mandatory)
        used = len(mandatory_text)
        memory_ids: list[str] = []
        symbol_refs: list[str] = []
        for symbol in self.repo_index.search_symbols(query, 12):
            line = f"[REPO] {symbol.path}:{symbol.line} {symbol.kind} {symbol.name}"
            extra = len(line) + (1 if lines else 0)
            if used + extra <= max_chars:
                lines.append(line); used += extra; symbol_refs.append(f"{symbol.path}:{symbol.line}:{symbol.name}")
        for memory in self.memories.search(project_id, query, 24):
            line = f"[MEMORY:{memory.kind}|authority={memory.authority}|source={memory.source}] {memory.content}"
            extra = len(line) + (1 if lines else 0)
            if used + extra <= max_chars:
                lines.append(line); used += extra; memory_ids.append(memory.memory_id)
        return CompiledContext("\n".join(lines), tuple(memory_ids), tuple(symbol_refs))
