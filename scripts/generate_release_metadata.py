from __future__ import annotations
import json,os,shutil
from pathlib import Path
from alinacoder.product.core import ReleaseManifest,SBOMBuilder
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
def main()->int:
 app=DIST/'AlinaCoder.exe'
 if not app.exists():raise SystemExit('missing dist/AlinaCoder.exe')
 commit=os.environ.get('GITHUB_SHA','LOCAL-UNVERIFIED');manifest=ReleaseManifest.from_bytes('0.2.0',commit,app.name,app.read_bytes()).as_dict();manifest['channel']='v0.2-rc';manifest['signature']='UNSIGNED_NO_CERTIFICATE';(DIST/'release-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding='utf-8');sbom=SBOMBuilder().build(['python-stdlib','pyinstaller==6.16.0']);sbom['documentNamespace']=f'https://github.com/Rapt0r06300/alinacoder/{commit}';(DIST/'sbom.spdx.json').write_text(json.dumps(sbom,indent=2,sort_keys=True),encoding='utf-8')
 for name in ['USER_GUIDE.md','OPERATIONS.md']:shutil.copy2(ROOT/'docs'/name,DIST/name)
 return 0
if __name__=='__main__':raise SystemExit(main())
