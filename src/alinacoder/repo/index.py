from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import sqlite3


@dataclass(frozen=True, slots=True)
class SymbolRecord:
    path: str
    name: str
    kind: str
    line: int


class RepositoryIndex:
    def __init__(self, path: Path | str, project_id: str) -> None:
        self.path = Path(path)
        self.project_id = project_id
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS files(project_id TEXT NOT NULL,path TEXT NOT NULL,sha256 TEXT NOT NULL,PRIMARY KEY(project_id,path));
            CREATE TABLE IF NOT EXISTS symbols(project_id TEXT NOT NULL,path TEXT NOT NULL,name TEXT NOT NULL,kind TEXT NOT NULL,line INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS edges(project_id TEXT NOT NULL,path TEXT NOT NULL,target TEXT NOT NULL,kind TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS idx_symbols_project_name ON symbols(project_id,name);
        """)

    def close(self) -> None:
        self._conn.close()

    def index_file(self, path: Path | str, repo_root: Path | str) -> bool:
        file_path = Path(path).resolve(); root = Path(repo_root).resolve(); relative = file_path.relative_to(root).as_posix()
        data = file_path.read_bytes(); digest = hashlib.sha256(data).hexdigest()
        row = self._conn.execute("SELECT sha256 FROM files WHERE project_id=? AND path=?", (self.project_id,relative)).fetchone()
        if row and row["sha256"] == digest:
            return False
        tree = ast.parse(data.decode("utf-8"), filename=relative)
        symbols: list[tuple[str,str,int]] = []; edges: list[tuple[str,str]] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)): symbols.append((node.name,"function",node.lineno))
            elif isinstance(node, ast.ClassDef): symbols.append((node.name,"class",node.lineno))
            elif isinstance(node, ast.Import):
                for alias in node.names: edges.append((alias.name,"import"))
            elif isinstance(node, ast.ImportFrom) and node.module: edges.append((node.module,"import"))
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name): edges.append((node.func.id,"call"))
                elif isinstance(node.func, ast.Attribute): edges.append((node.func.attr,"call"))
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            self._conn.execute("DELETE FROM symbols WHERE project_id=? AND path=?", (self.project_id,relative)); self._conn.execute("DELETE FROM edges WHERE project_id=? AND path=?", (self.project_id,relative))
            self._conn.execute("INSERT INTO files(project_id,path,sha256) VALUES(?,?,?) ON CONFLICT(project_id,path) DO UPDATE SET sha256=excluded.sha256", (self.project_id,relative,digest))
            self._conn.executemany("INSERT INTO symbols(project_id,path,name,kind,line) VALUES(?,?,?,?,?)", [(self.project_id,relative,n,k,l) for n,k,l in symbols])
            self._conn.executemany("INSERT INTO edges(project_id,path,target,kind) VALUES(?,?,?,?)", [(self.project_id,relative,t,k) for t,k in edges])
        except Exception:
            self._conn.execute("ROLLBACK"); raise
        else:
            self._conn.execute("COMMIT")
        return True

    def symbols(self, path: str | None = None) -> list[SymbolRecord]:
        if path is None: rows = self._conn.execute("SELECT path,name,kind,line FROM symbols WHERE project_id=? ORDER BY path,line,name", (self.project_id,)).fetchall()
        else: rows = self._conn.execute("SELECT path,name,kind,line FROM symbols WHERE project_id=? AND path=? ORDER BY line,name", (self.project_id,path)).fetchall()
        return [SymbolRecord(r["path"],r["name"],r["kind"],int(r["line"])) for r in rows]

    def search_symbols(self, query: str, limit: int = 20) -> list[SymbolRecord]:
        q = query.lower().strip()
        if not q: return []
        rows = self._conn.execute("SELECT path,name,kind,line FROM symbols WHERE project_id=? AND lower(name) LIKE ? ORDER BY name LIMIT ?", (self.project_id,f"%{q}%",limit)).fetchall()
        return [SymbolRecord(r["path"],r["name"],r["kind"],int(r["line"])) for r in rows]

    def edges(self, path: str | None = None) -> list[tuple[str,str,str]]:
        if path is None: rows = self._conn.execute("SELECT path,target,kind FROM edges WHERE project_id=? ORDER BY path,target", (self.project_id,)).fetchall()
        else: rows = self._conn.execute("SELECT path,target,kind FROM edges WHERE project_id=? AND path=? ORDER BY target", (self.project_id,path)).fetchall()
        return [(r["path"],r["target"],r["kind"]) for r in rows]
