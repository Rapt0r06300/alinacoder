from __future__ import annotations
import argparse,json,os,shutil,sys
from pathlib import Path
def _bundled_exe()->Path:
    base=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent));candidates=[base/'AlinaCoder.exe',Path(sys.executable).with_name('AlinaCoder.exe')]
    for candidate in candidates:
        if candidate.exists():return candidate
    raise FileNotFoundError('bundled AlinaCoder.exe not found')
def default_install_dir()->Path:
    local=os.environ.get('LOCALAPPDATA') or str(Path.home()/'AppData'/'Local');return Path(local)/'AlinaCoder'
def install(install_dir:Path,source_exe:Path|None=None)->Path:
    install_dir.mkdir(parents=True,exist_ok=True);source=source_exe or _bundled_exe();target=install_dir/'AlinaCoder.exe';shutil.copy2(source,target);(install_dir/'install.json').write_text(json.dumps({'version':'0.2.0','preserve_user_data_on_uninstall':True},sort_keys=True),encoding='utf-8');return target
def uninstall(install_dir:Path,*,purge_user_data:bool=False)->None:
    for name in ['AlinaCoder.exe','install.json']:
        path=install_dir/name
        if path.exists():path.unlink()
    if purge_user_data and install_dir.exists():shutil.rmtree(install_dir,ignore_errors=True)
    elif install_dir.exists() and not any(install_dir.iterdir()):install_dir.rmdir()
def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(prog='AlinaCoderSetup');p.add_argument('--install-dir',type=Path,default=default_install_dir());p.add_argument('--uninstall',action='store_true');p.add_argument('--purge-user-data',action='store_true');p.add_argument('--quiet',action='store_true');a=p.parse_args(argv)
    if a.uninstall:
        uninstall(a.install_dir,purge_user_data=a.purge_user_data)
        if not a.quiet:print(f'Uninstalled AlinaCoder from {a.install_dir}')
    else:
        target=install(a.install_dir)
        if not a.quiet:print(f'Installed AlinaCoder to {target}')
    return 0
if __name__=='__main__':raise SystemExit(main())
