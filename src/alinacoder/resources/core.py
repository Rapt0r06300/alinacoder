from __future__ import annotations
import statistics
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

class ResourceMode(str,Enum): CONSERVATIVE='CONSERVATIVE'; BALANCED='BALANCED'; PERFORMANCE='PERFORMANCE'
@dataclass(frozen=True)
class HardwareProfile: ram_gb:float; vram_gb:float; cpu_cores:int; gpu_name:str=''
@dataclass(frozen=True)
class DynamicLoadSnapshot:
    ram_pressure:float; vram_pressure:float; cpu_pressure:float; gpu_pressure:float; thermal_pressure:float=0.0
    @property
    def max_pressure(self)->float:return max(self.ram_pressure,self.vram_pressure,self.cpu_pressure,self.gpu_pressure,self.thermal_pressure)
@dataclass(frozen=True)
class LocalModel: name:str; required_ram_gb:float; required_vram_gb:float; capability:float; context_tokens:int=8192; runtime:str='ollama'
class HardwareFitProfile:
    def __init__(self,hardware:HardwareProfile,headroom_ratio:float=0.9)->None:self.hardware=hardware;self.headroom_ratio=headroom_ratio
    def fits(self,model:LocalModel)->bool:return model.required_ram_gb<=self.hardware.ram_gb*self.headroom_ratio and model.required_vram_gb<=self.hardware.vram_gb*self.headroom_ratio
    def select(self,models:Iterable[LocalModel])->LocalModel:
        eligible=[m for m in models if self.fits(m)]
        if not eligible:raise RuntimeError('no local model fits current hardware')
        return max(eligible,key=lambda m:(m.capability,m.context_tokens,-m.required_vram_gb))
class LocalModelDiscovery:
    @staticmethod
    def from_ollama_payload(payload:dict)->list[LocalModel]:
        out=[]
        for raw in payload.get('models',[]):
            size=float(raw.get('size',0));gb=max(0.5,size/1_000_000_000);out.append(LocalModel(str(raw['name']),gb*1.25,gb,float(raw.get('capability',0.5)),runtime='ollama'))
        return out
    @staticmethod
    def normalize_openai_compatible(runtime:str,payload:dict)->list[LocalModel]:return [LocalModel(str(i.get('id')),4,4,float(i.get('capability',0.5)),runtime=runtime) for i in payload.get('data',[])]
class ResourceController:
    def __init__(self,*,mode:ResourceMode=ResourceMode.BALANCED,pressure_samples:int=3,recovery_samples:int=3,high_threshold:float=0.90,low_threshold:float=0.45)->None:
        self.mode=mode;self.pressure_samples=max(1,pressure_samples);self.recovery_samples=max(1,recovery_samples);self.high_threshold=high_threshold;self.low_threshold=low_threshold;self._high_count=0;self._low_count=0
    def observe_pressure(self,pressure:float)->ResourceMode:
        if pressure>=self.high_threshold:
            self._high_count+=1;self._low_count=0
            if self._high_count>=self.pressure_samples:self.mode=ResourceMode.CONSERVATIVE;self._high_count=0
        elif pressure<=self.low_threshold:
            self._low_count+=1;self._high_count=0
            if self._low_count>=self.recovery_samples:self.mode=ResourceMode.BALANCED;self._low_count=0
        else:self._high_count=self._low_count=0
        return self.mode
    def observe_snapshot(self,snapshot:DynamicLoadSnapshot)->ResourceMode:return self.observe_pressure(snapshot.max_pressure)
    def execution_strategy(self,*,internet_available:bool,local_models_available:bool)->str:
        if not internet_available and local_models_available:return 'LOCAL_ONLY'
        if not internet_available:return 'DEGRADED_NO_INFERENCE'
        return 'HYBRID'
class PerformanceGate:
    def __init__(self,max_regression_ratio:float=1.20)->None:self.max_regression_ratio=max_regression_ratio
    def passes(self,baseline:list[float],candidate:list[float])->bool:
        if not baseline or not candidate:return False
        b=statistics.median(baseline);c=statistics.median(candidate);return c<=b if b<=0 else c/b<=self.max_regression_ratio
class WorkloadScheduler:
    def __init__(self,controller:ResourceController)->None:self.controller=controller
    def max_parallelism(self,hardware:HardwareProfile)->int:
        if self.controller.mode==ResourceMode.CONSERVATIVE:return 1
        if self.controller.mode==ResourceMode.PERFORMANCE:return max(1,min(8,hardware.cpu_cores//2))
        return max(1,min(4,hardware.cpu_cores//4 or 1))
