from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PREREQUISITE_MANIFEST = ROOT / "packaging" / "prerequisites-v0.2.json"
WINDOWS_MANIFEST = ROOT / "packaging" / "alinacoder-windows.manifest"


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> int:
    if os.name != "nt":
        raise SystemExit("Windows packaging must run on Windows")
    if not PREREQUISITE_MANIFEST.exists():
        raise SystemExit("missing packaging/prerequisites-v0.2.json")
    if not WINDOWS_MANIFEST.exists():
        raise SystemExit("missing packaging/alinacoder-windows.manifest")
    DIST.mkdir(exist_ok=True)
    run(
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
        "--manifest", str(WINDOWS_MANIFEST),
        "--name", "AlinaCoder", "--paths", "src", "packaging/alinacoder_entry.py",
    )
    app = DIST / "AlinaCoder.exe"
    if not app.exists():
        raise RuntimeError("AlinaCoder.exe was not produced")
    run(
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
        "--manifest", str(WINDOWS_MANIFEST),
        "--name", "AlinaCoderSetup", "--paths", "src",
        "--add-binary", f"{app}{os.pathsep}.",
        "--add-data", f"{PREREQUISITE_MANIFEST}{os.pathsep}packaging",
        "packaging/setup_entry.py",
    )
    if not (DIST / "AlinaCoderSetup.exe").exists():
        raise RuntimeError("AlinaCoderSetup.exe was not produced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
