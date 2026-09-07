from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import time
from typing import Callable, TypeVar

from .windows_fs import replace_with_retry, unlink_with_retry


T = TypeVar("T")
Sleep = Callable[[float], None]


@dataclass(frozen=True)
class WindowsIntegrationPlan:
    install_dir: Path
    app_exe: Path
    source_setup: Path
    maintenance_setup: Path
    start_menu_shortcut: Path
    desktop_shortcut: Path
    uninstall_key: str
    uninstall_command: str


def build_windows_integration_plan(
    install_dir: Path | str,
    setup_exe: Path | str,
    *,
    appdata: Path | str | None = None,
    userprofile: Path | str | None = None,
) -> WindowsIntegrationPlan:
    root = Path(install_dir)
    source = Path(setup_exe)
    appdata_root = Path(appdata) if appdata is not None else Path(
        os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
    )
    user_root = Path(userprofile) if userprofile is not None else Path(
        os.environ.get("USERPROFILE", str(Path.home()))
    )
    start_menu = appdata_root / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "AlinaCoder.lnk"
    desktop = user_root / "Desktop" / "AlinaCoder.lnk"
    maintenance = root / "AlinaCoderSetup.exe"
    uninstall = f'"{maintenance}" --uninstall --install-dir "{root}"'
    return WindowsIntegrationPlan(
        install_dir=root,
        app_exe=root / "AlinaCoder.exe",
        source_setup=source,
        maintenance_setup=maintenance,
        start_menu_shortcut=start_menu,
        desktop_shortcut=desktop,
        uninstall_key=r"Software\Microsoft\Windows\CurrentVersion\Uninstall\AlinaCoder",
        uninstall_command=uninstall,
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _retry(
    action: Callable[[], T],
    *,
    attempts: int,
    sleep: Sleep,
) -> T:
    """Retry one recoverable Windows integration operation with a bounded budget."""

    if attempts < 1:
        raise ValueError("retry_attempts must be at least 1")
    for attempt in range(1, attempts + 1):
        try:
            return action()
        except FileNotFoundError:
            # Missing required artifacts are structural, not transient.
            raise
        except OSError:
            if attempt >= attempts:
                raise
            sleep(min(0.25 * (2 ** (attempt - 1)), 2.0))
    raise AssertionError("unreachable retry loop exit")


def _copy_verified(source: Path, destination: Path) -> str:
    expected = _sha256_file(source)
    shutil.copy2(source, destination)
    if not destination.is_file() or destination.stat().st_size <= 0:
        raise OSError(f"copied file is missing or empty: {destination}")
    if _sha256_file(destination) != expected:
        raise OSError(f"copied file failed SHA-256 verification: {destination}")
    return expected


def _install_maintenance_setup_atomic(plan: WindowsIntegrationPlan, *, sleep: Sleep) -> None:
    """Transactionally replace the maintenance setup while preserving the last healthy copy."""

    source = plan.source_setup
    target = plan.maintenance_setup
    if source.resolve() == target.resolve():
        return

    staging = target.with_name("AlinaCoderSetup.exe.staging")
    backup = target.with_name("AlinaCoderSetup.exe.backup")
    backup_tmp = target.with_name("AlinaCoderSetup.exe.backup.tmp")

    unlink_with_retry(staging, missing_ok=True, sleep=sleep)
    expected = _copy_verified(source, staging)

    backup_available = backup.is_file()
    if target.is_file() and not backup_available:
        unlink_with_retry(backup_tmp, missing_ok=True, sleep=sleep)
        current_digest = _sha256_file(target)
        shutil.copy2(target, backup_tmp)
        if (
            not backup_tmp.is_file()
            or backup_tmp.stat().st_size <= 0
            or _sha256_file(backup_tmp) != current_digest
        ):
            unlink_with_retry(backup_tmp, missing_ok=True, sleep=sleep)
            raise OSError("could not preserve the previous AlinaCoderSetup.exe")
        replace_with_retry(backup_tmp, backup, sleep=sleep)
        backup_available = True

    promoted = False
    try:
        replace_with_retry(staging, target, sleep=sleep)
        promoted = True
        if not target.is_file() or target.stat().st_size <= 0 or _sha256_file(target) != expected:
            raise OSError("promoted AlinaCoderSetup.exe failed verification")
    except Exception:
        if promoted and backup_available and backup.is_file():
            replace_with_retry(backup, target, sleep=sleep)
        raise
    else:
        if backup_available:
            unlink_with_retry(backup, missing_ok=True, sleep=sleep)
        unlink_with_retry(backup_tmp, missing_ok=True, sleep=sleep)


def _create_shortcut(shortcut: Path, target: Path, working_dir: Path) -> None:
    shortcut.parent.mkdir(parents=True, exist_ok=True)
    escaped_shortcut = str(shortcut).replace("'", "''")
    escaped_target = str(target).replace("'", "''")
    escaped_working = str(working_dir).replace("'", "''")
    script = (
        "$w=New-Object -ComObject WScript.Shell;"
        f"$s=$w.CreateShortcut('{escaped_shortcut}');"
        f"$s.TargetPath='{escaped_target}';"
        f"$s.WorkingDirectory='{escaped_working}';"
        f"$s.IconLocation='{escaped_target},0';"
        "$s.Save()"
    )
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    if completed.returncode != 0 or not shortcut.exists():
        raise OSError(f"could not create shortcut: {shortcut}")


def _register_uninstall(plan: WindowsIntegrationPlan) -> None:
    if os.name != "nt":
        return
    import winreg

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, plan.uninstall_key) as key:
        values: dict[str, object] = {
            "DisplayName": "AlinaCoder",
            "DisplayVersion": "0.2.0",
            "Publisher": "AlinaCoder",
            "InstallLocation": str(plan.install_dir),
            "DisplayIcon": str(plan.app_exe),
            "UninstallString": plan.uninstall_command,
            "QuietUninstallString": plan.uninstall_command + " --quiet",
            "NoModify": 1,
        }
        for name, value in values.items():
            kind = winreg.REG_DWORD if isinstance(value, int) else winreg.REG_SZ
            winreg.SetValueEx(key, name, 0, kind, value)


def install_windows_integration(
    install_dir: Path | str,
    setup_exe: Path | str,
    *,
    create_desktop_shortcut: bool = True,
    create_shortcuts: bool = True,
    register_uninstall: bool = True,
    retry_attempts: int = 4,
    sleep: Sleep = time.sleep,
) -> WindowsIntegrationPlan:
    """Install the final per-user Windows integration with bounded self-repair."""

    if retry_attempts < 1:
        raise ValueError("retry_attempts must be at least 1")

    plan = build_windows_integration_plan(install_dir, setup_exe)
    if not plan.app_exe.is_file():
        raise FileNotFoundError("AlinaCoder.exe must be installed and verified before Windows integration")
    if not plan.source_setup.is_file():
        raise FileNotFoundError("AlinaCoderSetup.exe source is missing")

    plan.install_dir.mkdir(parents=True, exist_ok=True)
    _retry(
        lambda: _install_maintenance_setup_atomic(plan, sleep=sleep),
        attempts=retry_attempts,
        sleep=sleep,
    )

    if create_shortcuts:
        if os.name != "nt":
            raise OSError("shortcut creation requires Windows")
        _retry(
            lambda: _create_shortcut(plan.start_menu_shortcut, plan.app_exe, plan.install_dir),
            attempts=retry_attempts,
            sleep=sleep,
        )
        if create_desktop_shortcut:
            _retry(
                lambda: _create_shortcut(plan.desktop_shortcut, plan.app_exe, plan.install_dir),
                attempts=retry_attempts,
                sleep=sleep,
            )
    if register_uninstall:
        _retry(lambda: _register_uninstall(plan), attempts=retry_attempts, sleep=sleep)
    return plan


def remove_windows_integration(install_dir: Path | str) -> None:
    root = Path(install_dir)
    plan = build_windows_integration_plan(root, root / "AlinaCoderSetup.exe")
    for shortcut in (plan.start_menu_shortcut, plan.desktop_shortcut):
        try:
            shortcut.unlink(missing_ok=True)
        except OSError:
            pass
    if os.name == "nt":
        import winreg

        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, plan.uninstall_key)
        except FileNotFoundError:
            pass
