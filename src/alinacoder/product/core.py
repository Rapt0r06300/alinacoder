from __future__ import annotations
import hashlib
from dataclasses import asdict,dataclass
from pathlib import Path
def _version_tuple(version:str)->tuple[int,...]:
    try:return tuple(int(p) for p in version.split('+')[0].split('-')[0].split('.'))
    except ValueError as exc:raise ValueError(f'unsupported version: {version}') from exc
@dataclass(frozen=True)
class ReleaseManifest:
    version:str;commit_sha:str;artifact_name:str;sha256:str
    @classmethod
    def from_bytes(cls,version:str,commit_sha:str,artifact_name:str,data:bytes)->'ReleaseManifest':return cls(version,commit_sha,artifact_name,hashlib.sha256(data).hexdigest())
    def verify(self,data:bytes)->bool:return hashlib.sha256(data).hexdigest()==self.sha256
    def as_dict(self)->dict:return asdict(self)
class UpdateVerifier:
    def __init__(self,*,current_version:str,require_signature:bool=True)->None:self.current_version=current_version;self.require_signature=require_signature
    def accepts(self,manifest:dict,*,artifact:bytes)->bool:
        try:
            if _version_tuple(str(manifest['version']))<=_version_tuple(self.current_version):return False
        except (KeyError,ValueError):return False
        if manifest.get('sha256')!=hashlib.sha256(artifact).hexdigest():return False
        if self.require_signature and manifest.get('signature')!='TRUSTED':return False
        return True
@dataclass(frozen=True)
class InstallPlan:version:str;install_dir:Path;executable:Path;preserve_user_data:bool
def build_install_plan(*,version:str,install_dir:Path,preserve_user_data:bool)->InstallPlan:
    install_dir=Path(install_dir);return InstallPlan(version,install_dir,install_dir/'AlinaCoder.exe',preserve_user_data)
class SBOMBuilder:
    def build(self,components:list[str])->dict:
        packages=[{'name':c.split('==')[0],'versionInfo':c.split('==',1)[1] if '==' in c else 'builtin'} for c in components];return {'spdxVersion':'SPDX-2.3','dataLicense':'CC0-1.0','SPDXID':'SPDXRef-DOCUMENT','name':'AlinaCoder-v0.2','packages':packages}
