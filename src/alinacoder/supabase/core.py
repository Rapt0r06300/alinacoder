from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
def reciprocal_rank_fusion(rankings:list[list[str]],*,k:int=60)->list[tuple[str,float]]:
    scores=defaultdict(float)
    for ranking in rankings:
        for rank,item in enumerate(ranking,start=1):scores[item]+=1.0/(k+rank)
    return sorted(scores.items(),key=lambda item:(-item[1],item[0]))
class IdempotentQueueConsumer:
    def __init__(self)->None:self._seen={}
    def admit(self,message_id:str,*,fence:int,minimum_fence:int=0)->bool:
        if fence<minimum_fence:return False
        previous=self._seen.get(message_id)
        if previous is not None and fence<=previous:return False
        self._seen[message_id]=fence;return True
@dataclass
class SupabaseMirror:
    enabled:bool;project_id:str;tenant_id:str;healthy:bool=True;last_error:str|None=None
    @property
    def mode(self)->str:return 'MIRROR' if self.enabled and self.healthy else 'LOCAL_ONLY'
    def mark_unhealthy(self,reason:str)->None:self.healthy=False;self.last_error=reason
    def mark_healthy(self)->None:self.healthy=True;self.last_error=None
    def validate_scope(self,*,project_id:str,tenant_id:str)->None:
        if project_id!=self.project_id or tenant_id!=self.tenant_id:raise PermissionError('cross-project/tenant mirror access denied')
    def write_non_secret(self,record:dict)->str:
        if record.get('secret') is True or any(k.lower() in {'token','password','api_key'} and bool(v) for k,v in record.items()):raise PermissionError('secrets may not be mirrored')
        return self.mode
    def private_channel(self,suffix:str)->str:return f'private:{self.tenant_id}:{self.project_id}:{suffix}'
