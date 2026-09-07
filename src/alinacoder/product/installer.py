from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
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
from .self_healing import run_self_healing_operation
from .windows_fs import replace_with_retry, unlink_with_retry


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


def _sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stage_application_binary(source: Path | str, install_dir: Path | str) -> tuple[Path, str]:
    """Copy the application into a sibling staging file and verify it fully."""

    source_path = Path(source)
    root = Path(install_dir)
    root.mkdir(parents=True, exist_ok=True)
    if not source_path.is_file() or source_path.stat().st_size <= 0:
        raise BootstrapError("bundled AlinaCoder.exe is missing or empty")

    staging = root / "AlinaCoder.exe.staging"
    unlink_with_retry(staging, missing_ok=True)
    expected = _sha256_file(source_path)
    shutil.copy2(source_path, staging)
    if not staging.is_file() or staging.stat().st_size <= 0:
        raise BootstrapError("staged AlinaCoder.exe is missing or empty")
    if _sha256_file(staging) != expected:
        raise BootstrapError("staged AlinaCoder.exe failed SHA-256 verification")
    return staging, expected


def _prepare_application_backup(target: Path) -> Path | None:
    """Persist the last known application binary before promotion."""

    backup = target.with_name("AlinaCoder.exe.backup")
    if backup.is_file():
        return backup
    if not target.is_file():
        return None

    temporary = target.with_name("AlinaCoder.exe.backup.tmp")
    unlink_with_retry(temporary, missing_ok=True)
    expected = _sha256_file(target)
    shutil.copy2(target, temporary)
    if not temporary.is_file() or temporary.stat().st_size <= 0 or _sha256_file(temporary) != expected:
        unlink_with_retry(temporary, missing_ok=True)
        raise BootstrapError("could not preserve the previous AlinaCoder.exe")
    replace_with_retry(temporary, backup)
    return backup


def _restore_application_backup(target: Path, backup: Path | None) -> None:
    """Restore the previous application or remove an uncommitted fresh install."""

    if backup is not None and backup.is_file():
        replace_with_retry(backup, target)
        return
    unlink_with_retry(target, missing_ok=True)


def _promote_application_binary(staging: Path, target: Path, expected_sha256: str) -> Path | None:
    """Atomically promote a verified stage, restoring the old target on failure."""

    backup = _prepare_application_backup(target)
    promoted = False
    try:
        replace_with_retry(staging, target)
        promoted = True
        if not target.is_file() or target.stat().st_size <= 0:
            raise BootstrapError("promoted AlinaCoder.exe is missing or empty")
        if _sha256_file(target) != expected_sha256:
            raise BootstrapError("promoted AlinaCoder.exe failed SHA-256 verification")
        return backup
    except Exception:
        if promoted:
            _restore_application_backup(target, backup)
        raise


def _finalize_application_promotion(backup: Path | None) -> None:
    if backup is not None:
        unlink_with_retry(backup, missing_ok=True)


def _commit_application_install(
    install_dir: Path,
    staging: Path,
    expected_sha256: str,
    *,
    operation: str,
    report: BootstrapReport | None = None,
    deferred: bool = False,
) -> Path:
    """Commit application + metadata as one recoverable application transaction."""

    target = install_dir / "AlinaCoder.exe"
    backup = _promote_application_binary(staging, target, expected_sha256)
    try:
        _write_metadata(install_dir, operation=operation, report=report, deferred=deferred)
    except Exception:
        _restore_application_backup(target, backup)
        raise
    _finalize_application_promotion(backup)
    return target


def _normalize_bootstrap_state(
    report: BootstrapReport,
    initial_inventory: Any,
    previous_state: BootstrapState | None,
    adapter: Any,
) -> BootstrapReport:
    if report.state is None:
        return report
    components = dict(report.state.components)
    changed = False
    for name, initial in (("git", getattr(initial_inventory, "git", None)), ("ollama", getattr(initial_inventory, "ollama", None))):
        if initial is not None and getattr(initial, "origin", "") == "pre_existing" and name in components:
            current = components[name]
            if current.origin != "pre_existing":
                components[name] = replace(
                    current,
                    origin="pre_existing",
                    previous_version="",
                    previous_source_url="",
                    previous_sha256="",
                )
                changed = True
                continue
        prior = previous_state.components.get(name) if previous_state else None
        current = components.get(name)
        if (
            prior is not None and current is not None
            and prior.origin == "managed_by_alinacoder"
            and current.origin == "managed_by_alinacoder"
            and prior.version == current.version
            and prior.source_url and prior.sha256
            and (not current.source_url or not current.sha256)
        ):
            components[name] = replace(
                current,
                source_url=prior.source_url,
                sha256=prior.sha256,
                previous_version=prior.previous_version,
                previous_source_url=prior.previous_source_url,
                previous_sha256=prior.previous_sha256,
            )
            changed = True
    if not changed:
        return report
    state = BootstrapState(components, report.state.selected_model, report.state.ready, report.state.pending)
    corrected = BootstrapReport(report.ready, report.selected_model, report.actions, report.blockers, state)
    persist = getattr(adapter, "persist_report", None)
    if callable(persist):
        persist(corrected)
    return corrected


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
    staging, expected_sha256 = _stage_application_binary(source, install_dir)

    if deferred_prerequisites:
        return _commit_application_install(
            install_dir,
            staging,
            expected_sha256,
            operation=operation,
            deferred=True,
        )
    if bootstrapper is None:
        return _commit_application_install(
            install_dir,
            staging,
            expected_sha256,
            operation=operation,
        )

    adapter = getattr(bootstrapper, "adapter", None)
    detect = getattr(adapter, "detect_inventory", None)
    initial_inventory = detect() if callable(detect) else None
    load_state = getattr(adapter, "load_state", None)
    previous_state = load_state() if callable(load_state) else None
    report = bootstrapper.run(online=online, model_override=model)
    report = _normalize_bootstrap_state(report, initial_inventory, previous_state, adapter)
    if not report.ready:
        _write_metadata(install_dir, operation=operation, report=report)
        raise BootstrapError("prerequisite bootstrap incomplete: " + ", ".join(report.blockers))
    return _commit_application_install(
        install_dir,
        staging,
        expected_sha256,
        operation=operation,
        report=report,
    )


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
        has_previous_hint = any(
            receipt.origin == "managed_by_alinacoder"
            and not name.startswith("model:")
            and bool(receipt.previous_version or receipt.previous_source_url or receipt.previous_sha256)
            for name, receipt in state.components.items()
        )
        if has_previous_hint:
            raise BootstrapError("no valid provenance-bound managed prerequisite rollback target is available")
        ready = bool(state.ready and adapter.ollama_ready(bootstrapper.manifest.ollama.endpoint))
        if not ready:
            raise BootstrapError("rollback no-op refused because current bootstrap state is not healthy")
        report = BootstrapReport(True, state.selected_model, (), (), state)
        adapter.persist_report(report)
        _write_metadata(install_dir, operation="rollback", report=report)
        return ()

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


def _requested_operation(args: argparse.Namespace) -> str:
    if args.repair:
        return "repair"
    if args.upgrade:
        return "upgrade"
    if args.bootstrap_only:
        return "bootstrap"
    if args.rollback:
        return "rollback"
    if args.uninstall:
        return "uninstall"
    return "upgrade" if (args.install_dir / "AlinaCoder.exe").exists() else "install"


def _write_failure_receipt_if_missing(args: argparse.Namespace, exc: BaseException) -> None:
    """Leave a resumable fail-closed receipt even when setup fails before bootstrap."""

    if args.uninstall or args.rollback:
        return
    install_dir = Path(args.install_dir)
    if (install_dir / "install.json").exists():
        return
    blocker = f"setup_error:{type(exc).__name__}"
    report = BootstrapReport(False, str(args.model or ""), (), (blocker,))
    try:
        _write_metadata(install_dir, operation=_requested_operation(args), report=report)
    except OSError:
        pass


def _cli_self_healing_operation(args: argparse.Namespace, operation: str) -> Path:
    factory = None if args.deferred_prerequisites else (lambda: build_bootstrapper(args.install_dir))
    return run_self_healing_operation(
        args.install_dir,
        operation=operation,
        bootstrapper_factory=factory,
        deferred_prerequisites=args.deferred_prerequisites,
        online=not args.offline,
        model=args.model,
    )


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
        if args.uninstall:
            bootstrapper = None if args.deferred_prerequisites else build_bootstrapper(args.install_dir)
            uninstall(
                args.install_dir,
                purge_user_data=args.purge_user_data,
                bootstrapper=bootstrapper,
                purge_managed_prerequisites=args.purge_managed_prerequisites,
            )
            if not args.quiet:
                print(f"Uninstalled AlinaCoder from {args.install_dir}")
        elif args.rollback:
            bootstrapper = None if args.deferred_prerequisites else build_bootstrapper(args.install_dir)
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
        else:
            operation = _requested_operation(args)
            target = _cli_self_healing_operation(args, operation)
            if not args.quiet:
                verb = {"install": "Installed", "repair": "Repaired", "upgrade": "Upgraded"}.get(operation, "Installed")
                print(f"{verb} AlinaCoder at {target}")
        return 0
    except Exception as exc:
        _write_failure_receipt_if_missing(args, exc)
        if not args.quiet:
            print(f"AlinaCoder setup failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
