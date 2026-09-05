from __future__ import annotations
import json,os
from pathlib import Path
class AutomationRegistry:
    @staticmethod
    def default_ids()->dict[str,str]:
        names=['composer','send','voice','goal','pause','resume','stop','takeover','project','sessions','plan','context','diff','tests','git','receipts','run_inspector','timeline','provider_status','resource_status','diagnostics'];return {n:f'alinacoder.{n}' for n in names}
class DesktopControlPlane:
    def __init__(self)->None:self.state='RUNNING';self.epoch=0
    def _set(self,state:str)->None:self.state=state;self.epoch+=1
    def pause(self)->None:self._set('PAUSED')
    def resume(self)->None:self._set('RUNNING')
    def stop(self)->None:self._set('STOPPED')
    def takeover(self)->None:self._set('USER_TAKEOVER')
class DesktopStateStore:
    def __init__(self,path:Path)->None:self.path=Path(path)
    def save(self,state:dict)->None:
        self.path.parent.mkdir(parents=True,exist_ok=True);tmp=self.path.with_suffix(self.path.suffix+'.tmp');tmp.write_text(json.dumps(state,sort_keys=True,ensure_ascii=False),encoding='utf-8');os.replace(tmp,self.path)
    def load(self)->dict:return {} if not self.path.exists() else json.loads(self.path.read_text(encoding='utf-8'))
class WorkbenchModel:
    _ACTIONS=frozenset({'open_project','send_message','start_goal','pause','resume','stop','takeover','view_plan','edit_plan','view_context','view_diff','run_tests','commit_main','view_git','view_receipts','view_run_inspector','view_timeline','configure_provider','configure_local_model','open_diagnostics','select_artifact','voice_input'})
    def available_actions(self)->set[str]:return set(self._ACTIONS)
    def semantic_ui_snapshot(self)->dict:return {'automation_ids':AutomationRegistry.default_ids(),'actions':sorted(self._ACTIONS)}
def self_test()->dict:
    ids=AutomationRegistry.default_ids();actions=WorkbenchModel().available_actions();required={'send_message','start_goal','stop','commit_main'};return {'ok':len(ids.values())==len(set(ids.values())) and required.issubset(actions),'automation_ids':ids,'actions':sorted(actions)}
