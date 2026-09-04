from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re, sqlite3, uuid
_TOKEN=re.compile(r"[A-Za-z0-9_]+")
def _tokens(s:str)->set[str]: return {m.group(0).lower() for m in _TOKEN.finditer(s)}
@dataclass(frozen=True,slots=True)
class MemoryNode: node_id:str; project_id:str; kind:str; content:str
class MemoryGraph:
    def __init__(self,path:Path|str)->None:
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self._conn=sqlite3.connect(self.path,isolation_level=None); self._conn.row_factory=sqlite3.Row; self._conn.execute("PRAGMA journal_mode=WAL"); self._conn.executescript("CREATE TABLE IF NOT EXISTS nodes(node_id TEXT PRIMARY KEY,project_id TEXT,kind TEXT,content TEXT); CREATE TABLE IF NOT EXISTS edges(project_id TEXT,src TEXT,dst TEXT,kind TEXT,UNIQUE(project_id,src,dst,kind));")
    def close(self)->None:self._conn.close()
    def add(self,project_id:str,kind:str,content:str)->str:
        nid=uuid.uuid4().hex; self._conn.execute("INSERT INTO nodes VALUES(?,?,?,?)",(nid,project_id,kind,content)); return nid
    def link(self,project_id:str,src:str,dst:str,kind:str)->None:
        rows=self._conn.execute("SELECT node_id FROM nodes WHERE project_id=? AND node_id IN (?,?)",(project_id,src,dst)).fetchall()
        if len(rows)!=2: raise ValueError("Graph links must remain inside one project")
        self._conn.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)",(project_id,src,dst,kind))
    def retrieve(self,project_id:str,query:str,hops:int=1)->list[MemoryNode]:
        q=_tokens(query); rows=self._conn.execute("SELECT * FROM nodes WHERE project_id=?",(project_id,)).fetchall(); seeds=[r["node_id"] for r in rows if q & _tokens(r["content"])]; seen=set(seeds); frontier=set(seeds)
        for _ in range(max(0,hops)):
            if not frontier: break
            nxt=set()
            for nid in frontier:
                erows=self._conn.execute("SELECT src,dst FROM edges WHERE project_id=? AND (src=? OR dst=?)",(project_id,nid,nid)).fetchall()
                for e in erows: nxt.update((e["src"],e["dst"]))
            nxt-=seen; seen|=nxt; frontier=nxt
        if not seen:return []
        out=[]
        for r in rows:
            if r["node_id"] in seen: out.append(MemoryNode(r["node_id"],r["project_id"],r["kind"],r["content"]))
        return out
