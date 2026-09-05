from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Any

from .prerequisite_lifecycle import bind_previous_provenance, rollback_managed
from .prerequisites import (
    BootstrapError,
    BootstrapReport,
    BootstrapState,
    PrerequisiteBootstrapper,
    PrerequisiteManifest,
    WindowsBootstrapAdapter,
)


def _bundled_exe() -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    candidates = [base / "AlinaCoder.exe", Path(sys.executable).with_name("AlinaCoder.exe")]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("bundled AlinaCoder.exe not found")


def _bundled_manifest() -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    root = Path(__file__).resolve().parents[3]
    candidates = [
        base / "packaging" / "prerequisites-v0.2.json",
        base / "prerequisites-v0.2.json",
        root / "packaging" / "prerequisites-v0.2.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("bundled prerequisite manifest not found")


def default_install_dir() -> Path:
    local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(local) / "AlinaCoder"


def build_bootstrapper(install_dir: Path) -> PrerequisiteBootstrapper:
    manifest = PrerequisiteManifest.load(_bundled_manifest())
    return PrerequisiteBootstrapper(manifest, WindowsBootstrapAdapter(Path(install_dir), manifest))


def _metadata_payload(*, operation: str, report: BootstrapReport | None, deferred: bool) -> dict[str, Any]:
    if report is not None:
        ready = report.ready
        selected_model = report.selected_model
        blockers = list(report.blockers)
    elif deferred:
        ready = False
        selected_model = ""
        blockers = ["deferred"]
    else:
        ready = False
        selected_model = ""
        blockers = ["bootstrap_not_run"]
    return {
        "version": "0.2.0",
        "preserve_user_data_on_uninstall": True,
        "last_operation": operation,
        "bootstrap_ready": ready,
        "selected_model": selected_model,
        "bootstrap_blockers": blockers,
        "bootstrap_state": "bootstrap-state.json",
        "bootstrap_receipt": "bootstrap-receipt.json",
    }


def _write_metadata(
    install_dir: Path,
    *,
    operation: str,
    report: BootstrapReport | None = None,
    deferred: bool = False,
) -> None:
    install_dir.mkdir(parents=True, exist_ok=True)
    temporary = install_dir / "install.json.tmp"
    temporary.write_text(
        json.dumps(_metadata_payload(operation=operation, report=report, deferred=deferred), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    temporary.replace(install_dir / "install.json")


def install(
    install_dir: Path,
    source_exe: Path | None = None,
    *,
    operation: str = "install",
    bootstrapper: Any | None = None,
    deferred_prerequisites: bool = False,
    online: bool = True,
    model: str | None = None,
) -> Path:
    install_dir = Path(install_dir)
    install_dir.mkdir(parents=True, exist_ok=True)
    source = Path(source_exe) if source_exe is not None else _bundled_exe()
    target = install_dir / "AlinaCoder.exe"
    shutil.copy2(source, target)
    if deferred_prerequisites:
        _write_metadata(install_dir, operation=operation, deferred=True)
        return target
    if bootstrapper is None:
        _write_metadata(install_dir, operation=operation)
        return target
    report = bootstrapper.run(online=online, model_override=model)
    _write_metadata(install_dir, operation=operation, report=report)
    if not report.ready:
        raise BootstrapError("prerequisite bootstrap incomplete: " + ", ".join(report.blockers))
    return target


def repair(
    install_dir: Path,
    source_exe: Path | None = None,
    *,
    bootstrapper: Any | None = None,
    deferred_prerequisites: bool = False,
    online: bool = True,
    model: str | None = None,
) -> Path:
    install_dir = Path(install_dir)
    install_dir.mkdir(parents=True, exist_ok=True)
    return install(
        install_dir,
        source_exe=source_exe,
        operation="repair",
        bootstrapper=bootstrapper,
        deferred_prerequisites=deferred_prerequisites,
        online=online,
        model=model,
    )


def _load_bootstrap_state(bootstrapper: Any | None) -> BootstrapState | None:
    adapter = getattr(bootstrapper, "adapter", None)
    load_state = getattr(adapter, "load_state", None)
    if not callable(load_state):
        return None
    return load_state()


def upgrade(
    install_dir: Path,
    source_exe: Path | None = None,
    *,
    bootstrapper: Any | None = None,
    deferred_prerequisites: bool = False,
    online: bool = True,
    model: str | None = None,
) -> Path:
    previous_state = _load_bootstrap_state(bootstrapper)
    target = install(
        Path(install_dir),
        source_exe=source_exe,
        operation="upgrade",
        bootstrapper=bootstrapper,
        deferred_prerequisites=deferred_prerequisites,
        online=online,
        model=model,
    )
    adapter = getattr(bootstrapper, "adapter", None)
    if adapter is not None and previous_state is not None:
        bind_previous_provenance(adapter, previous_state)
    return target


def rollback(
    install_dir: Path,
    *,
    bootstrapper: Any | None = None,
) -> tuple[str, ...]:
    install_dir = Path(install_dir)
    bootstrapper = bootstrapper or build_bootstrapper(install_dir)
    adapter = getattr(bootstrapper, "adapter", None)
    if adapter is None:
        raise BootstrapError("rollback requires a Windows bootstrap adapter")
    state = _load_bootstrap_state(bootstrapper)
    if state is None:
        raise BootstrapError("no bootstrap state available for rollback")
    restored = rollback_managed(adapter, state)
    if not restored:
        raise BootstrapError("no provenance-bound managed prerequisite rollback target is available")
    inventory = adapter.detect_inventory()
    components = dict(state.components)
    for name in restored:
        current = inventory.git if name == "git" else inventory.ollama
        previous = components.get(name)
        if current is None or previous is None:
            raise BootstrapError(f"rollback verification failed for {name}")
        components[name] = type(previous)(
            name=name,
            version=current.version,
            origin="managed_by_alinacoder",
            source_url=previous.previous_source_url,
            sha256=previous.previous_sha256,
            healthy=True,
            path=current.path,
        )
    ready = bool(adapter.ollama_ready(bootstrapper.manifest.ollama.endpoint))
    rebound = BootstrapState(components, state.selected_model, ready, () if ready else ("ollama_health",))
    adapter._atomic_write_json(adapter.state_path, rebound.as_dict())
    report = BootstrapReport(ready, rebound.selected_model, (), rebound.pending, rebound)
    adapter.persist_report(report)
    _write_metadata(install_dir, operation="rollback", report=report)
    if not ready:
        raise BootstrapError("rollback completed but Ollama health check failed")
    return restored


def uninstall(
    install_dir: Path,
    *,
    purge_user_data: bool = False,
    bootstrapper: Any | None = None,
    purge_managed_prerequisites: bool = False,
) -> None:
    install_dir = Path(install_dir)
    if bootstrapper is not None:
        action = getattr(bootstrapper, "managed_uninstall", None)
        if callable(action):
            action(purge=purge_managed_prerequisites)
    for name in ["AlinaCoder.exe", "install.json"]:
        path = install_dir / name
        if path.exists():
            path.unlink()
    if purge_user_data and install_dir.exists():
        shutil.rmtree(install_dir, ignore_errors=True)
    elif install_dir.exists() and not any(install_dir.iterdir()):
        install_dir.rmdir()


def _run_bootstrap_only(install_dir: Path, *, online: bool, model: str | None) -> BootstrapReport:
    bootstrapper = build_bootstrapper(install_dir)
    report = bootstrapper.run(online=online, model_override=model)
    _write_metadata(install_dir, operation="bootstrap", report=report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="AlinaCoderSetup")
    parser.add_argument("--install-dir", type=Path, default=default_install_dir())
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--uninstall", action="store_true")
    actions.add_argument("--repair", action="store_true")
    actions.add_argument("--upgrade", action="store_true")
    actions.add_argument("--rollback", action="store_true")
    actions.add_argument("--bootstrap-only", action="store_true")
    parser.add_argument("--purge-user-data", action="store_true")
    parser.add_argument("--purge-managed-prerequisites", action="store_true")
    parser.add_argument("--deferred-prerequisites", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    try:
        bootstrapper = None if args.deferred_prerequisites else build_bootstrapper(args.install_dir)
        if args.uninstall:
            uninstall(
                args.install_dir,
                purge_user_data=args.purge_user_data,
                bootstrapper=bootstrapper,
                purge_managed_prerequisites=args.purge_managed_prerequisites,
            )
            if not args.quiet:
                print(f"Uninstalled AlinaCoder from {args.install_dir}")
        elif args.rollback:
            restored = rollback(args.install_dir, bootstrapper=bootstrapper)
            if not args.quiet:
                print("Rolled back managed prerequisites: " + ", ".join(restored))
        elif args.bootstrap_only:
            report = _run_bootstrap_only(args.install_dir, online=not args.offline, model=args.model)
            if not report.ready:
                if not args.quiet:
                    print("Bootstrap incomplete: " + ", ".join(report.blockers))
                return 2
            if not args.quiet:
                print(f"Bootstrap ready with {report.selected_model}")
        elif args.repair:
            target = repair(
                args.install_dir,
                bootstrapper=bootstrapper,
                deferred_prerequisites=args.deferred_prerequisites,
                online=not args.offline,
                model=args.model,
            )
            if not args.quiet:
                print(f"Repaired AlinaCoder at {target}")
        elif args.upgrade:
            target = upgrade(
                args.install_dir,
                bootstrapper=bootstrapper,
                deferred_prerequisites=args.deferred_prerequisites,
                online=not args.offline,
                model=args.model,
            )
            if not args.quiet:
                print(f"Upgraded AlinaCoder at {target}")
        else:
            operation = "upgrade" if (args.install_dir / "AlinaCoder.exe").exists() else "install"
            if operation == "upgrade":
                target = upgrade(
                    args.install_dir,
                    bootstrapper=bootstrapper,
                    deferred_prerequisites=args.deferred_prerequisites,
                    online=not args.offline,
                    model=args.model,
                )
            else:
                target = install(
                    args.install_dir,
                    operation=operation,
                    bootstrapper=bootstrapper,
                    deferred_prerequisites=args.deferred_prerequisites,
                    online=not args.offline,
                    model=args.model,
                )
            if not args.quiet:
                print(f"Installed AlinaCoder to {target}")
        return 0
    except (BootstrapError, FileNotFoundError, OSError) as exc:
        if not args.quiet:
            print(f"AlinaCoder setup failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
