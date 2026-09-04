from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterator

from .models import CanonicalSessionState, EffectRecord, EventRecord, canonical_json


class StateStoreError(RuntimeError):
    pass


class StaleStateError(StateStoreError):
    pass


class StaleWriterError(StateStoreError):
    pass


class SessionNotFoundError(StateStoreError):
    pass


class StateStore:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=FULL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._init_schema()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "StateStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            yield self._conn
        except Exception:
            self._conn.execute("ROLLBACK")
            raise
        else:
            self._conn.execute("COMMIT")

    def _init_schema(self) -> None:
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions(session_id TEXT PRIMARY KEY, version INTEGER NOT NULL, state_json TEXT NOT NULL, checksum TEXT NOT NULL, fencing_epoch INTEGER NOT NULL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS events(sequence INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL, version INTEGER NOT NULL, kind TEXT NOT NULL, state_json TEXT NOT NULL, checksum TEXT NOT NULL, metadata_json TEXT NOT NULL, UNIQUE(session_id, version));
            CREATE TABLE IF NOT EXISTS checkpoints(session_id TEXT NOT NULL, label TEXT NOT NULL, source_version INTEGER NOT NULL, state_json TEXT NOT NULL, checksum TEXT NOT NULL, PRIMARY KEY(session_id, label));
            CREATE TABLE IF NOT EXISTS effects(effect_key TEXT PRIMARY KEY, session_id TEXT NOT NULL, status TEXT NOT NULL, payload_json TEXT NOT NULL, result_json TEXT);
        """)

    def _state_from_row(self, row: sqlite3.Row) -> CanonicalSessionState:
        return CanonicalSessionState(row["session_id"], int(row["version"]), json.loads(row["state_json"]), row["checksum"], int(row["fencing_epoch"]))

    def create_session(self, session_id: str, initial_data: dict[str, Any] | None = None) -> CanonicalSessionState:
        state = CanonicalSessionState.build(session_id, 0, initial_data or {}, 0)
        with self._transaction() as conn:
            if conn.execute("SELECT 1 FROM sessions WHERE session_id=?", (session_id,)).fetchone():
                raise StateStoreError(f"Session already exists: {session_id}")
            conn.execute("INSERT INTO sessions(session_id,version,state_json,checksum,fencing_epoch) VALUES(?,?,?,?,?)", (session_id,0,canonical_json(state.data),state.checksum,0))
            conn.execute("INSERT INTO events(session_id,version,kind,state_json,checksum,metadata_json) VALUES(?,?,?,?,?,?)", (session_id,0,"session_created",canonical_json(state.data),state.checksum,"{}"))
        return state

    def get_state(self, session_id: str) -> CanonicalSessionState:
        row = self._conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if row is None:
            raise SessionNotFoundError(session_id)
        return self._state_from_row(row)

    def acquire_writer(self, session_id: str) -> int:
        with self._transaction() as conn:
            row = conn.execute("SELECT fencing_epoch FROM sessions WHERE session_id=?", (session_id,)).fetchone()
            if row is None:
                raise SessionNotFoundError(session_id)
            epoch = int(row["fencing_epoch"]) + 1
            conn.execute("UPDATE sessions SET fencing_epoch=? WHERE session_id=?", (epoch,session_id))
        return epoch

    def commit_state(self, session_id: str, expected_version: int, fencing_epoch: int, new_data: dict[str, Any], event_kind: str, metadata: dict[str, Any] | None = None) -> CanonicalSessionState:
        with self._transaction() as conn:
            row = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
            if row is None:
                raise SessionNotFoundError(session_id)
            current_version = int(row["version"])
            current_epoch = int(row["fencing_epoch"])
            if fencing_epoch != current_epoch:
                raise StaleWriterError(f"Writer epoch {fencing_epoch} != current {current_epoch}")
            if expected_version != current_version:
                raise StaleStateError(f"Expected version {expected_version} != current {current_version}")
            state = CanonicalSessionState.build(session_id, current_version + 1, new_data, current_epoch)
            state_json = canonical_json(state.data)
            conn.execute("UPDATE sessions SET version=?,state_json=?,checksum=? WHERE session_id=?", (state.version,state_json,state.checksum,session_id))
            conn.execute("INSERT INTO events(session_id,version,kind,state_json,checksum,metadata_json) VALUES(?,?,?,?,?,?)", (session_id,state.version,event_kind,state_json,state.checksum,canonical_json(metadata or {})))
        return state

    def list_events(self, session_id: str) -> list[EventRecord]:
        rows = self._conn.execute("SELECT sequence,session_id,version,kind,checksum,metadata_json FROM events WHERE session_id=? ORDER BY version", (session_id,)).fetchall()
        return [EventRecord(int(r["sequence"]),r["session_id"],int(r["version"]),r["kind"],r["checksum"],json.loads(r["metadata_json"])) for r in rows]

    def reconstruct(self, session_id: str) -> CanonicalSessionState:
        row = self._conn.execute("SELECT e.session_id,e.version,e.state_json,e.checksum,s.fencing_epoch FROM events e JOIN sessions s ON s.session_id=e.session_id WHERE e.session_id=? ORDER BY e.version DESC LIMIT 1", (session_id,)).fetchone()
        if row is None:
            raise SessionNotFoundError(session_id)
        state = self._state_from_row(row)
        expected = CanonicalSessionState.build(state.session_id,state.version,state.data,state.fencing_epoch).checksum
        if state.checksum != expected:
            raise StateStoreError("Event log checksum mismatch")
        return state

    def checkpoint(self, session_id: str, label: str) -> None:
        state = self.get_state(session_id)
        with self._transaction() as conn:
            conn.execute("INSERT OR REPLACE INTO checkpoints(session_id,label,source_version,state_json,checksum) VALUES(?,?,?,?,?)", (session_id,label,state.version,canonical_json(state.data),state.checksum))

    def restore_checkpoint(self, session_id: str, label: str, expected_version: int, fencing_epoch: int) -> CanonicalSessionState:
        row = self._conn.execute("SELECT state_json,source_version FROM checkpoints WHERE session_id=? AND label=?", (session_id,label)).fetchone()
        if row is None:
            raise StateStoreError(f"Unknown checkpoint: {label}")
        return self.commit_state(session_id, expected_version, fencing_epoch, json.loads(row["state_json"]), "checkpoint_restore", {"checkpoint": label, "source_version": int(row["source_version"])})

    def begin_effect(self, effect_key: str, session_id: str, payload: dict[str, Any]) -> bool:
        try:
            with self._transaction() as conn:
                conn.execute("INSERT INTO effects(effect_key,session_id,status,payload_json,result_json) VALUES(?,?,?,?,NULL)", (effect_key,session_id,"pending",canonical_json(payload)))
            return True
        except sqlite3.IntegrityError:
            return False

    def ack_effect(self, effect_key: str, result: dict[str, Any]) -> None:
        with self._transaction() as conn:
            cur = conn.execute("UPDATE effects SET status='acked', result_json=? WHERE effect_key=? AND status='pending'", (canonical_json(result),effect_key))
            if cur.rowcount != 1:
                raise StateStoreError(f"Effect is not pending: {effect_key}")

    def pending_effects(self, session_id: str) -> list[EffectRecord]:
        rows = self._conn.execute("SELECT * FROM effects WHERE session_id=? AND status='pending' ORDER BY effect_key", (session_id,)).fetchall()
        return [EffectRecord(r["effect_key"],r["session_id"],r["status"],json.loads(r["payload_json"]),json.loads(r["result_json"]) if r["result_json"] else None) for r in rows]
