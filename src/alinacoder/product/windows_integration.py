from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess


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
    appdata_root = Path(appdata) if appdata is not None else Path(os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming")))
    user_root = Path(userprofile) if userprofile is not None else Path(os.environ.get("USERPROFILE", str(Path.home())))
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
) -> WindowsIntegrationPlan:
    plan = build_windows_integration_plan(install_dir, setup_exe)
    if not plan.app_exe.is_file():
        raise FileNotFoundError("AlinaCoder.exe must be installed and verified before Windows integration")
    if not plan.source_setup.is_file():
        raise FileNotFoundError("AlinaCoderSetup.exe source is missing")

    plan.install_dir.mkdir(parents=True, exist_ok=True)
    if plan.source_setup.resolve() != plan.maintenance_setup.resolve():
        shutil.copy2(plan.source_setup, plan.maintenance_setup)

    if create_shortcuts:
        if os.name != "nt":
            raise OSError("shortcut creation requires Windows")
        _create_shortcut(plan.start_menu_shortcut, plan.app_exe, plan.install_dir)
        if create_desktop_shortcut:
            _create_shortcut(plan.desktop_shortcut, plan.app_exe, plan.install_dir)
    if register_uninstall:
        _register_uninstall(plan)
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
