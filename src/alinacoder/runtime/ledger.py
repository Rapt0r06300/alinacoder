from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import sqlite3
import uuid


@dataclass(frozen=True, slots=True)
class LedgerObservation:
    observation_id: str
    repo_state: str
    path: str
    selector: str
    result_digest: str
    valid: bool
    invalidation_cause: str | None


@dataclass(frozen=True, slots=True)
class LedgerCommand:
    command_id: str
    repo_state: str
    command: str
    arguments: tuple[str, ...]
    effect_class: str
    result_digest: str
    success: bool
    failure_class: str | None
    strategy_key: str | None


@dataclass(frozen=True, slots=True)
class LedgerSummary:
    repo_state: str
    valid_observation_count: int
    observed_paths: tuple[str, ...]
    failure_classes: tuple[str, ...]
    failed_strategies: tuple[str, ...]
    recent_commands: tuple[str, ...]


class ExecutionLedger:
    """Mechanically derived execution facts; no model reasoning is persisted."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=FULL")
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS observations(
                observation_id TEXT PRIMARY KEY,
                repo_state TEXT NOT NULL,
                path TEXT NOT NULL,
                selector TEXT NOT NULL,
                result_digest TEXT NOT NULL,
                valid INTEGER NOT NULL DEFAULT 1,
                invalidation_cause TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_ledger_observation_path ON observations(path, valid);
            CREATE TABLE IF NOT EXISTS modifications(
                modification_id TEXT PRIMARY KEY,
                repo_state_before TEXT NOT NULL,
                repo_state_after TEXT NOT NULL,
                paths_json TEXT NOT NULL,
                before_json TEXT NOT NULL,
                after_json TEXT NOT NULL,
                origin TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS commands(
                command_id TEXT PRIMARY KEY,
                repo_state TEXT NOT NULL,
                command TEXT NOT NULL,
                arguments_json TEXT NOT NULL,
                effect_class TEXT NOT NULL,
                result_digest TEXT NOT NULL,
                success INTEGER NOT NULL,
                failure_class TEXT,
                strategy_key TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_ledger_command_reuse
                ON commands(repo_state, command, effect_class, success);
            CREATE INDEX IF NOT EXISTS idx_ledger_strategy
                ON commands(repo_state, strategy_key, success);
            """
        )

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "ExecutionLedger":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def record_observation(self, *, repo_state: str, path: str, selector: str, result_digest: str) -> str:
        if not repo_state or not path or not result_digest:
            raise ValueError("repo_state, path and result_digest are required")
        observation_id = "obs:" + uuid.uuid4().hex
        self._conn.execute(
            "INSERT INTO observations VALUES(?,?,?,?,?,1,NULL)",
            (observation_id, str(repo_state), str(path), str(selector), str(result_digest)),
        )
        return observation_id

    def get_observation(self, observation_id: str) -> LedgerObservation:
        row = self._conn.execute("SELECT * FROM observations WHERE observation_id=?", (observation_id,)).fetchone()
        if row is None:
            raise KeyError(observation_id)
        return LedgerObservation(
            str(row["observation_id"]), str(row["repo_state"]), str(row["path"]), str(row["selector"]),
            str(row["result_digest"]), bool(row["valid"]), row["invalidation_cause"],
        )

    def invalidate_paths(self, paths: tuple[str, ...] | list[str], cause: str) -> tuple[str, ...]:
        normalized = tuple(dict.fromkeys(str(path) for path in paths if str(path)))
        invalidated: list[str] = []
        for path in normalized:
            rows = self._conn.execute(
                "SELECT observation_id FROM observations WHERE path=? AND valid=1", (path,)
            ).fetchall()
            invalidated.extend(str(row["observation_id"]) for row in rows)
            self._conn.execute(
                "UPDATE observations SET valid=0,invalidation_cause=? WHERE path=? AND valid=1",
                (str(cause), path),
            )
        return tuple(invalidated)

    def record_modification(
        self,
        *,
        repo_state_before: str,
        repo_state_after: str,
        paths: tuple[str, ...] | list[str],
        before_digests: dict[str, str],
        after_digests: dict[str, str],
        origin: str,
    ) -> tuple[str, ...]:
        normalized = tuple(dict.fromkeys(str(path) for path in paths if str(path)))
        modification_id = "mod:" + uuid.uuid4().hex
        self._conn.execute(
            "INSERT INTO modifications VALUES(?,?,?,?,?,?,?)",
            (
                modification_id, str(repo_state_before), str(repo_state_after), json.dumps(normalized),
                json.dumps(before_digests, sort_keys=True), json.dumps(after_digests, sort_keys=True), str(origin),
            ),
        )
        changed = tuple(
            path for path in normalized
            if str(before_digests.get(path, "")) != str(after_digests.get(path, ""))
        )
        return self.invalidate_paths(changed, f"modified by {origin}; repo {repo_state_before}->{repo_state_after}")

    def record_command(
        self,
        *,
        repo_state: str,
        command: str,
        arguments: tuple[str, ...] | list[str],
        effect_class: str,
        result_digest: str,
        success: bool,
        failure_class: str | None = None,
        strategy_key: str | None = None,
    ) -> str:
        if not repo_state or not command or effect_class not in {"read", "write", "external", "verify"}:
            raise ValueError("valid repo_state, command and effect_class are required")
        command_id = "cmd:" + uuid.uuid4().hex
        self._conn.execute(
            "INSERT INTO commands VALUES(?,?,?,?,?,?,?,?,?)",
            (
                command_id, str(repo_state), str(command), json.dumps(tuple(str(x) for x in arguments)),
                str(effect_class), str(result_digest), int(bool(success)),
                str(failure_class) if failure_class else None,
                str(strategy_key) if strategy_key else None,
            ),
        )
        return command_id

    @staticmethod
    def _command(row: sqlite3.Row) -> LedgerCommand:
        return LedgerCommand(
            str(row["command_id"]), str(row["repo_state"]), str(row["command"]),
            tuple(str(x) for x in json.loads(row["arguments_json"])), str(row["effect_class"]),
            str(row["result_digest"]), bool(row["success"]), row["failure_class"], row["strategy_key"],
        )

    def reusable_read(self, command: str, arguments: tuple[str, ...] | list[str], repo_state: str) -> LedgerCommand | None:
        encoded = json.dumps(tuple(str(x) for x in arguments))
        row = self._conn.execute(
            """
            SELECT * FROM commands WHERE repo_state=? AND command=? AND arguments_json=?
              AND effect_class='read' AND success=1 ORDER BY rowid DESC LIMIT 1
            """,
            (repo_state, command, encoded),
        ).fetchone()
        return None if row is None else self._command(row)

    def repeated_failed_strategy(self, strategy_key: str, repo_state: str) -> bool:
        if not strategy_key:
            return False
        row = self._conn.execute(
            "SELECT 1 FROM commands WHERE repo_state=? AND strategy_key=? AND success=0 LIMIT 1",
            (repo_state, strategy_key),
        ).fetchone()
        return row is not None

    def inform(self, repo_state: str, limit: int = 8) -> LedgerSummary:
        observations = self._conn.execute(
            "SELECT path FROM observations WHERE valid=1 ORDER BY rowid DESC LIMIT ?", (max(1, int(limit)),)
        ).fetchall()
        commands = self._conn.execute(
            "SELECT * FROM commands WHERE repo_state=? ORDER BY rowid DESC LIMIT ?", (repo_state, max(1, int(limit)))
        ).fetchall()
        failures = tuple(dict.fromkeys(str(row["failure_class"]) for row in commands if row["failure_class"]))
        strategies = tuple(dict.fromkeys(str(row["strategy_key"]) for row in commands if not row["success"] and row["strategy_key"]))
        return LedgerSummary(
            str(repo_state),
            int(self._conn.execute("SELECT COUNT(*) FROM observations WHERE valid=1").fetchone()[0]),
            tuple(dict.fromkeys(str(row["path"]) for row in observations)),
            failures,
            strategies,
            tuple(str(row["command"]) for row in commands),
        )
