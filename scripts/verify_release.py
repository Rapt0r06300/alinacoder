from __future__ import annotations
import argparse,json
from pathlib import Path
from alinacoder.release.acceptance import ReleaseBundle,sha256_file
def main(argv=None)->int:
 p=argparse.ArgumentParser();p.add_argument('--dist',type=Path,default=Path('dist'));p.add_argument('--commit',required=True);a=p.parse_args(argv);manifest=json.loads((a.dist/'release-manifest.json').read_text(encoding='utf-8'));app=a.dist/'AlinaCoder.exe';bundle=ReleaseBundle({x.name for x in a.dist.iterdir()});ok=bundle.complete() and app.exists() and manifest.get('commit_sha')==a.commit and manifest.get('sha256')==sha256_file(app);print(json.dumps({'ok':ok,'bundle_complete':bundle.complete(),'commit':manifest.get('commit_sha'),'artifact_sha256':sha256_file(app) if app.exists() else None},sort_keys=True));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
