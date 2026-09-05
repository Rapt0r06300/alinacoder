from __future__ import annotations
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
def run(*args:str)->None:subprocess.run(args,cwd=ROOT,check=True)
def main()->int:
 if os.name!='nt':raise SystemExit('Windows packaging must run on Windows')
 DIST.mkdir(exist_ok=True);run(sys.executable,'-m','PyInstaller','--noconfirm','--clean','--onefile','--windowed','--name','AlinaCoder','--paths','src','packaging/alinacoder_entry.py');app=DIST/'AlinaCoder.exe'
 if not app.exists():raise RuntimeError('AlinaCoder.exe was not produced')
 run(sys.executable,'-m','PyInstaller','--noconfirm','--clean','--onefile','--name','AlinaCoderSetup','--paths','src','--add-binary',f'{app}{os.pathsep}.','packaging/setup_entry.py')
 if not (DIST/'AlinaCoderSetup.exe').exists():raise RuntimeError('AlinaCoderSetup.exe was not produced')
 return 0
if __name__=='__main__':raise SystemExit(main())
