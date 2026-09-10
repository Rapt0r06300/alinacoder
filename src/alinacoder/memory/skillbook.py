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
    problem_signature: str = ""
    scope: str = ""
    strategy: str = ""
    failed_alternatives: tuple[str, ...] = ()
    commit_binding: str = ""
    revalidation_policy: str = "on_source_or_state_change"


@dataclass(frozen=True, slots=True)
class SkillRecord:
    skill_id: str
    project_id: str
    key: str
    lesson: str
    evidence: tuple[str, ...]
    score: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    quarantined: bool = False
    metadata: dict[str, object] | None = None


class SkillBook:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=FULL")
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS skills(skill_id TEXT PRIMARY KEY,project_id TEXT NOT NULL,key TEXT NOT NULL,lesson TEXT NOT NULL,evidence_json TEXT NOT NULL, UNIQUE(project_id,key,lesson))"
        )
        columns = {str(row["name"]) for row in self._conn.execute("PRAGMA table_info(skills)").fetchall()}
        migrations = {
            "success_count": "ALTER TABLE skills ADD COLUMN success_count INTEGER NOT NULL DEFAULT 0",
            "failure_count": "ALTER TABLE skills ADD COLUMN failure_count INTEGER NOT NULL DEFAULT 0",
            "quarantined": "ALTER TABLE skills ADD COLUMN quarantined INTEGER NOT NULL DEFAULT 0",
            "metadata_json": "ALTER TABLE skills ADD COLUMN metadata_json TEXT NOT NULL DEFAULT '{}'",
        }
        for name, statement in migrations.items():
            if name not in columns:
                self._conn.execute(statement)
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_skills_project ON skills(project_id,key)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_skills_active ON skills(project_id,quarantined)")

    def close(self) -> None:
        self._conn.close()

    def _metadata(self, card: ExperienceCard) -> dict[str, object]:
        return {
            "problem_signature": card.problem_signature,
            "scope": card.scope,
            "strategy": card.strategy,
            "failed_alternatives": list(card.failed_alternatives),
            "commit_binding": card.commit_binding,
            "revalidation_policy": card.revalidation_policy,
        }

    def promote(self, card: ExperienceCard) -> str:
        if not card.project_id or not card.key.strip() or not card.lesson.strip():
            raise SkillPromotionError("Project, key and lesson are required")
        if not card.verified or not card.evidence:
            raise SkillPromotionError("Only verified experience with evidence can become a skill")
        skill_id = uuid.uuid4().hex
        try:
            self._conn.execute(
                "INSERT INTO skills(skill_id,project_id,key,lesson,evidence_json,metadata_json) VALUES(?,?,?,?,?,?)",
                (skill_id, card.project_id, card.key, card.lesson, json.dumps(card.evidence), json.dumps(self._metadata(card), sort_keys=True)),
            )
        except sqlite3.IntegrityError:
            row = self._conn.execute(
                "SELECT skill_id FROM skills WHERE project_id=? AND key=? AND lesson=?",
                (card.project_id, card.key, card.lesson),
            ).fetchone()
            assert row is not None
            return str(row["skill_id"])
        return skill_id

    def _record(self, row: sqlite3.Row, score: float = 0.0) -> SkillRecord:
        metadata_raw = row["metadata_json"] if "metadata_json" in row.keys() else "{}"
        try:
            metadata = json.loads(metadata_raw or "{}")
        except json.JSONDecodeError:
            metadata = {}
        return SkillRecord(
            str(row["skill_id"]), str(row["project_id"]), str(row["key"]), str(row["lesson"]),
            tuple(json.loads(row["evidence_json"])), score,
            int(row["success_count"]) if "success_count" in row.keys() else 0,
            int(row["failure_count"]) if "failure_count" in row.keys() else 0,
            bool(row["quarantined"]) if "quarantined" in row.keys() else False,
            metadata if isinstance(metadata, dict) else {},
        )

    def get(self, skill_id: str) -> SkillRecord:
        row = self._conn.execute("SELECT * FROM skills WHERE skill_id=?", (skill_id,)).fetchone()
        if row is None:
            raise KeyError(skill_id)
        return self._record(row)

    def observe_outcome(self, skill_id: str, success: bool) -> SkillRecord:
        row = self._conn.execute("SELECT success_count,failure_count FROM skills WHERE skill_id=?", (skill_id,)).fetchone()
        if row is None:
            raise KeyError(skill_id)
        success_count = int(row["success_count"]) + int(bool(success))
        failure_count = int(row["failure_count"]) + int(not bool(success))
        total = success_count + failure_count
        success_rate = success_count / total if total else 1.0
        quarantined = total >= 3 and failure_count >= 3 and success_rate < 0.35
        self._conn.execute(
            "UPDATE skills SET success_count=?,failure_count=?,quarantined=? WHERE skill_id=?",
            (success_count, failure_count, int(quarantined), skill_id),
        )
        return self.get(skill_id)

    def quarantine(self, skill_id: str) -> SkillRecord:
        cur = self._conn.execute("UPDATE skills SET quarantined=1 WHERE skill_id=?", (skill_id,))
        if cur.rowcount != 1:
            raise KeyError(skill_id)
        return self.get(skill_id)

    def revalidate(self, skill_id: str) -> SkillRecord:
        cur = self._conn.execute(
            "UPDATE skills SET quarantined=0,success_count=0,failure_count=0 WHERE skill_id=?", (skill_id,)
        )
        if cur.rowcount != 1:
            raise KeyError(skill_id)
        return self.get(skill_id)

    def search(self, project_id: str, query: str, limit: int = 8) -> list[SkillRecord]:
        q = _tokens(query)
        if not q or limit <= 0:
            return []
        rows = self._conn.execute(
            "SELECT * FROM skills WHERE project_id=? AND quarantined=0", (project_id,)
        ).fetchall()
        scored: list[SkillRecord] = []
        for row in rows:
            terms = _tokens(row["key"] + " " + row["lesson"])
            overlap = len(q & terms)
            if not overlap:
                continue
            score = overlap / max(1, len(q | terms))
            scored.append(self._record(row, score))
        scored.sort(key=lambda item: (-item.score, item.key, item.skill_id))
        return scored[:limit]
