from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys


def _bundled_exe() -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    candidates = [base / "AlinaCoder.exe", Path(sys.executable).with_name("AlinaCoder.exe")]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("bundled AlinaCoder.exe not found")


def default_install_dir() -> Path:
    local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(local) / "AlinaCoder"


def _write_metadata(install_dir: Path, *, operation: str) -> None:
    (install_dir / "install.json").write_text(
        json.dumps(
            {
                "version": "0.2.0",
                "preserve_user_data_on_uninstall": True,
                "last_operation": operation,
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def install(install_dir: Path, source_exe: Path | None = None, *, operation: str = "install") -> Path:
    install_dir = Path(install_dir)
    install_dir.mkdir(parents=True, exist_ok=True)
    source = Path(source_exe) if source_exe is not None else _bundled_exe()
    target = install_dir / "AlinaCoder.exe"
    shutil.copy2(source, target)
    _write_metadata(install_dir, operation=operation)
    return target


def repair(install_dir: Path, source_exe: Path | None = None) -> Path:
    install_dir = Path(install_dir)
    if not install_dir.exists():
        install_dir.mkdir(parents=True, exist_ok=True)
    return install(install_dir, source_exe=source_exe, operation="repair")


def upgrade(install_dir: Path, source_exe: Path | None = None) -> Path:
    return install(Path(install_dir), source_exe=source_exe, operation="upgrade")


def uninstall(install_dir: Path, *, purge_user_data: bool = False) -> None:
    install_dir = Path(install_dir)
    for name in ["AlinaCoder.exe", "install.json"]:
        path = install_dir / name
        if path.exists():
            path.unlink()
    if purge_user_data and install_dir.exists():
        shutil.rmtree(install_dir, ignore_errors=True)
    elif install_dir.exists() and not any(install_dir.iterdir()):
        install_dir.rmdir()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="AlinaCoderSetup")
    parser.add_argument("--install-dir", type=Path, default=default_install_dir())
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--uninstall", action="store_true")
    actions.add_argument("--repair", action="store_true")
    actions.add_argument("--upgrade", action="store_true")
    parser.add_argument("--purge-user-data", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    if args.uninstall:
        uninstall(args.install_dir, purge_user_data=args.purge_user_data)
        if not args.quiet:
            print(f"Uninstalled AlinaCoder from {args.install_dir}")
    elif args.repair:
        target = repair(args.install_dir)
        if not args.quiet:
            print(f"Repaired AlinaCoder at {target}")
    elif args.upgrade:
        target = upgrade(args.install_dir)
        if not args.quiet:
            print(f"Upgraded AlinaCoder at {target}")
    else:
        operation = "upgrade" if (args.install_dir / "AlinaCoder.exe").exists() else "install"
        target = install(args.install_dir, operation=operation)
        if not args.quiet:
            print(f"Installed AlinaCoder to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
