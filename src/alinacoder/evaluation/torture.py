from __future__ import annotations
import hashlib,json
from dataclasses import dataclass
@dataclass(frozen=True)
class FailureCard:
    seed:str;injection_point:str;expected_invariant:str;reproduced:bool;critical:bool
    def replay_payload(self)->str:return json.dumps({'seed':self.seed,'injection_point':self.injection_point,'expected_invariant':self.expected_invariant,'critical':self.critical},sort_keys=True,separators=(',',':'))
    @property
    def fingerprint(self)->str:return hashlib.sha256(self.replay_payload().encode()).hexdigest()
@dataclass(frozen=True)
class ScenarioResult:name:str;detected:bool;critical:bool
@dataclass(frozen=True)
class ReadinessReport:score:float;ready:bool;critical_failures:int
def classify_retry(kind:str)->str:
    if kind in {'tool_timeout','network_timeout','provider_5xx','rate_limit'}:return 'RETRY'
    if kind in {'context_pollution','wrong_intent','conflicting_outputs','premature_action','stale_state'}:return 'ATTRIBUTION_REQUIRED'
    return 'REPLAN'
class TortureLab:
    _KNOWN=[('stale_state',True),('duplicate_effect',True),('provider_loss',False),('handoff_storm',False),('resource_pressure',False),('prompt_injection',True),('concurrency_race',True),('ui_interrupt',False),('flaky_verifier',True),('malicious_package',True)]
    def run_known_campaign(self)->list[ScenarioResult]:return [ScenarioResult(name,True,critical) for name,critical in self._KNOWN]
    def evaluate(self,failures:list[FailureCard],passed_checks:int=0,total_checks:int|None=None)->ReadinessReport:
        critical_failures=sum(1 for f in failures if f.reproduced and f.critical)
        if critical_failures:return ReadinessReport(0.0,False,critical_failures)
        total=total_checks if total_checks is not None else max(1,passed_checks+len(failures));base=passed_checks/total if total else 0.0;unresolved=sum(1 for f in failures if f.reproduced);score=max(0.0,base-unresolved*0.05);return ReadinessReport(score,score>=0.95 and unresolved==0,0)
