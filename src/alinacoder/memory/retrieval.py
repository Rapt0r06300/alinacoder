from __future__ import annotations
from dataclasses import dataclass
from alinacoder.memory.store import MemoryStore
from alinacoder.memory.graph import MemoryGraph
from alinacoder.repo.index import RepositoryIndex

@dataclass(frozen=True, slots=True)
class HybridHit:
    source: str
    ref: str
    text: str
    score: float

class HybridRetriever:
    def __init__(self, memories: MemoryStore, graph: MemoryGraph, repo: RepositoryIndex) -> None:
        self.memories=memories; self.graph=graph; self.repo=repo
    def retrieve(self, project_id: str, query: str, limit: int = 16) -> list[HybridHit]:
        hits:list[HybridHit]=[]
        for m in self.memories.search(project_id,query,limit): hits.append(HybridHit('memory',m.memory_id,m.content,m.score+0.20))
        for n in self.graph.retrieve(project_id,query,hops=1): hits.append(HybridHit('graph',n.node_id,n.content,0.55))
        for s in self.repo.search_symbols(query,limit): hits.append(HybridHit('repo',f'{s.path}:{s.line}:{s.name}',f'{s.kind} {s.name}',0.65))
        dedup:dict[tuple[str,str],HybridHit]={}
        for h in hits:
            key=(h.source,h.ref)
            if key not in dedup or h.score>dedup[key].score: dedup[key]=h
        return sorted(dedup.values(),key=lambda h:(-h.score,h.source,h.ref))[:limit]
