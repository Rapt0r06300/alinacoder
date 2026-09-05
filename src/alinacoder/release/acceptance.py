from __future__ import annotations
import argparse,hashlib,json
from dataclasses import dataclass
from pathlib import Path
class TraceabilityMatrix:
    def __init__(self,*,required_domains:set[str])->None:self.required_domains=set(required_domains);self.entries={}
    def cover(self,domain:str,code_path:str,test_path:str)->None:
        if not code_path or not test_path:raise ValueError('traceability requires code and test')
        self.entries[domain]=(code_path,test_path)
    def complete(self)->bool:return self.required_domains.issubset(self.entries)
    def gaps(self)->set[str]:return self.required_domains-self.entries.keys()
@dataclass(frozen=True)
class AcceptanceEvidence:name:str;verdict:str;commit_sha:str;artifact_sha256:str;fresh:bool
class AcceptanceGate:
    def __init__(self,*,required:set[str],commit_sha:str,artifact_sha256:str)->None:self.required=set(required);self.commit_sha=commit_sha;self.artifact_sha256=artifact_sha256;self._evidence={}
    def add(self,evidence:AcceptanceEvidence)->None:self._evidence[evidence.name]=evidence
    def runtime_v0_2_ready(self)->bool:
        for name in self.required:
            e=self._evidence.get(name)
            if not e or e.verdict!='PASS' or not e.fresh:return False
            if e.commit_sha!=self.commit_sha or e.artifact_sha256!=self.artifact_sha256:return False
        return True
class ReleaseBundle:
    REQUIRED={'AlinaCoder.exe','AlinaCoderSetup.exe','release-manifest.json','sbom.spdx.json','USER_GUIDE.md','OPERATIONS.md'}
    def __init__(self,files:set[str])->None:self.files=set(files)
    def complete(self)->bool:return self.REQUIRED.issubset(self.files)
def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,default=Path.cwd());p.add_argument('--artifact-dir',type=Path,required=True);p.add_argument('--commit-sha',default='');a=p.parse_args(argv);artifact=a.artifact_dir/'AlinaCoder.exe';setup=a.artifact_dir/'AlinaCoderSetup.exe';files={x.name for x in a.artifact_dir.iterdir()} if a.artifact_dir.exists() else set()
    for doc in ['USER_GUIDE.md','OPERATIONS.md']:
        if (a.repo_root/'docs'/doc).exists():files.add(doc)
    bundle=ReleaseBundle(files);report={'runtime_v0_2_ready':False,'bundle_complete':bundle.complete(),'artifact_exists':artifact.exists(),'setup_exists':setup.exists()}
    if artifact.exists() and bundle.complete():report['artifact_sha256']=sha256_file(artifact)
    print(json.dumps(report,sort_keys=True));return 0 if report['bundle_complete'] and artifact.exists() and setup.exists() else 2
if __name__=='__main__':raise SystemExit(main())
