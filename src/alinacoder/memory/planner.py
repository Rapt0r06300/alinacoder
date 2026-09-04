from __future__ import annotations
from dataclasses import dataclass
import hashlib, json

@dataclass(frozen=True, slots=True)
class ContextPlan:
    project_id: str
    query: str
    state_version: int
    cache_key: str
    mandatory_text: str

class ContextQueryPlanner:
    def __init__(self, max_chars: int = 4000) -> None:
        if max_chars <= 0: raise ValueError('max_chars must be positive')
        self.max_chars=max_chars; self._cache:dict[str,ContextPlan]={}
    def plan(self, project_id:str, query:str, *, state_version:int, constraints:list[str]|tuple[str,...]=(), evidence:list[str]|tuple[str,...]=()) -> ContextPlan:
        payload={"project_id":project_id,"query":query,"state_version":state_version,"constraints":list(constraints),"evidence":list(evidence)}
        key=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        if key in self._cache:return self._cache[key]
        lines=[f'[CONSTRAINT] {x}' for x in constraints]+[f'[EVIDENCE] {x}' for x in evidence]; mandatory='\n'.join(lines)
        if len(mandatory)>self.max_chars: raise ValueError('Mandatory context exceeds budget')
        plan=ContextPlan(project_id,query,state_version,key,mandatory); self._cache[key]=plan; return plan
    def invalidate_project(self,project_id:str)->None:
        self._cache={k:v for k,v in self._cache.items() if v.project_id!=project_id}
