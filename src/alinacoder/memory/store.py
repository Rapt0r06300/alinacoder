from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Any
import uuid

_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+", re.UNICODE)


def file_sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _tokens(text: str) -> set[str]:
    return {m.group(0).lower() for m in _TOKEN_RE.finditer(text)}


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    project_id: str
    kind: str
    content: str
    source: str
    source_hash: str | None
    authority: int
    stale: bool
    stale_reason: str | None
    superseded_by: str | None
    metadata: dict[str, Any]
    score: float = 0.0


class MemoryStore:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=FULL")
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories(memory_id TEXT PRIMARY KEY,project_id TEXT NOT NULL,kind TEXT NOT NULL,content TEXT NOT NULL,source TEXT NOT NULL,source_hash TEXT,authority INTEGER NOT NULL,stale INTEGER NOT NULL DEFAULT 0,stale_reason TEXT,superseded_by TEXT,metadata_json TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project_id,stale,superseded_by);
        """)

    def close(self) -> None:
        self._conn.close()

    def put(self, project_id: str, kind: str, content: str, source: str, *, source_hash: str | None = None, authority: int = 0, metadata: dict[str, Any] | None = None) -> str:
        if not project_id or not content.strip() or not source:
            raise ValueError("project_id, content and source are required")
        memory_id = uuid.uuid4().hex
        self._conn.execute("INSERT INTO memories(memory_id,project_id,kind,content,source,source_hash,authority,stale,stale_reason,superseded_by,metadata_json) VALUES(?,?,?,?,?,?,?,0,NULL,NULL,?)", (memory_id,project_id,kind,content,source,source_hash,int(authority),json.dumps(metadata or {}, sort_keys=True)))
        return memory_id

    def supersede(self, project_id: str, old_memory_id: str, new_memory_id: str) -> None:
        cur = self._conn.execute("UPDATE memories SET superseded_by=? WHERE project_id=? AND memory_id=?", (new_memory_id,project_id,old_memory_id))
        if cur.rowcount != 1:
            raise KeyError(old_memory_id)

    def _record(self, row: sqlite3.Row, score: float = 0.0) -> MemoryRecord:
        return MemoryRecord(row["memory_id"],row["project_id"],row["kind"],row["content"],row["source"],row["source_hash"],int(row["authority"]),bool(row["stale"]),row["stale_reason"],row["superseded_by"],json.loads(row["metadata_json"]),score)

    def active(self, project_id: str) -> list[MemoryRecord]:
        rows = self._conn.execute("SELECT * FROM memories WHERE project_id=? AND stale=0 AND superseded_by IS NULL", (project_id,)).fetchall()
        return [self._record(row) for row in rows]

    def search(self, project_id: str, query: str, limit: int = 8) -> list[MemoryRecord]:
        q = _tokens(query)
        if not q or limit <= 0:
            return []
        scored: list[MemoryRecord] = []
        for record in self.active(project_id):
            t = _tokens(record.content)
            overlap = len(q & t)
            if overlap == 0:
                continue
            lexical = overlap / max(1, len(q))
            semantic_lite = overlap / max(1, len(q | t))
            authority_bonus = min(max(record.authority, 0), 100) / 1000.0
            score = lexical * 0.7 + semantic_lite * 0.2 + authority_bonus
            scored.append(MemoryRecord(record.memory_id, record.project_id, record.kind, record.content, record.source, record.source_hash, record.authority, record.stale, record.stale_reason, record.superseded_by, record.metadata, score))
        scored.sort(key=lambda item: (-item.score, -item.authority, item.memory_id))
        return scored[:limit]

    def refresh_source_freshness(self, project_id: str, repo_root: Path | str) -> list[str]:
        root = Path(repo_root).resolve()
        rows = self._conn.execute("SELECT memory_id,source,source_hash FROM memories WHERE project_id=? AND source_hash IS NOT NULL AND stale=0 AND superseded_by IS NULL", (project_id,)).fetchall()
        stale_ids: list[str] = []
        for row in rows:
            source = (root / row["source"]).resolve()
            try:
                source.relative_to(root)
            except ValueError:
                changed = True
            else:
                changed = not source.is_file() or file_sha256(source) != row["source_hash"]
            if changed:
                self._conn.execute("UPDATE memories SET stale=1,stale_reason=? WHERE memory_id=? AND project_id=?", ("source changed or missing",row["memory_id"],project_id))
                stale_ids.append(row["memory_id"])
        return stale_ids
