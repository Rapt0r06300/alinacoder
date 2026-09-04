from __future__ import annotations
from dataclasses import dataclass
import hashlib, json
from alinacoder.repo.index import RepositoryIndex
@dataclass(frozen=True,slots=True)
class TwinSnapshot:
    symbols: tuple[str,...]
    edges: tuple[tuple[str,str,str],...]
    fingerprint: str
class ProjectTwin:
    def __init__(self,index:RepositoryIndex)->None:self.index=index
    def snapshot(self)->TwinSnapshot:
        symbols=tuple(sorted({s.name for s in self.index.symbols()})); edges=tuple(sorted(self.index.edges())); payload=json.dumps({"symbols":symbols,"edges":edges},sort_keys=True,separators=(",",":")).encode(); return TwinSnapshot(symbols,edges,hashlib.sha256(payload).hexdigest())
