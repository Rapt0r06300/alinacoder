from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import sqlite3
import uuid

_TOKEN = re.compile(r"[A-Za-z0-9_]+", re.UNICODE)


def _tokens(text: str) -> set[str]:
    return {m.group(0).lower() for m in _TOKEN.finditer(text)}


class SkillPromotionError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ExperienceCard:
    project_id: str
    key: str
    lesson: str
    verified: bool
    evidence: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SkillRecord:
    skill_id: str
    project_id: str
    key: str
    lesson: str
    evidence: tuple[str, ...]
    score: float = 0.0


class SkillBook:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=FULL")
        self._conn.execute("CREATE TABLE IF NOT EXISTS skills(skill_id TEXT PRIMARY KEY,project_id TEXT NOT NULL,key TEXT NOT NULL,lesson TEXT NOT NULL,evidence_json TEXT NOT NULL, UNIQUE(project_id,key,lesson))")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_skills_project ON skills(project_id,key)")

    def close(self) -> None:
        self._conn.close()

    def promote(self, card: ExperienceCard) -> str:
        if not card.project_id or not card.key.strip() or not card.lesson.strip():
            raise SkillPromotionError("Project, key and lesson are required")
        if not card.verified or not card.evidence:
            raise SkillPromotionError("Only verified experience with evidence can become a skill")
        skill_id = uuid.uuid4().hex
        try:
            self._conn.execute("INSERT INTO skills(skill_id,project_id,key,lesson,evidence_json) VALUES(?,?,?,?,?)", (skill_id, card.project_id, card.key, card.lesson, json.dumps(card.evidence)))
        except sqlite3.IntegrityError:
            row = self._conn.execute("SELECT skill_id FROM skills WHERE project_id=? AND key=? AND lesson=?", (card.project_id, card.key, card.lesson)).fetchone()
            assert row is not None
            return str(row["skill_id"])
        return skill_id

    def get(self, skill_id: str) -> SkillRecord:
        row = self._conn.execute("SELECT * FROM skills WHERE skill_id=?", (skill_id,)).fetchone()
        if row is None:
            raise KeyError(skill_id)
        return SkillRecord(row["skill_id"], row["project_id"], row["key"], row["lesson"], tuple(json.loads(row["evidence_json"])))

    def search(self, project_id: str, query: str, limit: int = 8) -> list[SkillRecord]:
        q = _tokens(query)
        if not q:
            return []
        rows = self._conn.execute("SELECT * FROM skills WHERE project_id=?", (project_id,)).fetchall()
        scored: list[SkillRecord] = []
        for row in rows:
            terms = _tokens(row["key"] + " " + row["lesson"])
            overlap = len(q & terms)
            if not overlap:
                continue
            score = overlap / max(1, len(q | terms))
            scored.append(SkillRecord(row["skill_id"], row["project_id"], row["key"], row["lesson"], tuple(json.loads(row["evidence_json"])), score))
        scored.sort(key=lambda item: (-item.score, item.key, item.skill_id))
        return scored[:limit]
