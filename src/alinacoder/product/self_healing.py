from __future__ import annotations

import json
from pathlib import Path
import time
from typing import Any, Callable

from .prerequisites import BootstrapError
from .recovery import (
    RecoveryDecision,
    RecoveryJournal,
    RecoveryPolicy,
    backoff_seconds,
    classify_failure,
    cleanup_transients,
)
from .setup_events import CancellationToken, SetupEvent, SetupEventSink


BootstrapperFactory = Callable[[], Any]
Sleep = Callable[[float], None]


def _emit(
    sink: SetupEventSink | None,
    *,
    kind: str,
    message: str,
    detail: str = "",
    current: int | None = None,
    total: int | None = None,
) -> None:
    if sink is None:
        return
    sink(
        SetupEvent(
            phase="repair",
            kind=kind,
            message=message,
            detail=detail,
            current=current,
            total=total,
        )
    )


def _validate_full_install(install_dir: Path, target: Path, *, deferred_prerequisites: bool) -> None:
    if not target.is_file() or target.stat().st_size <= 0:
        raise BootstrapError("AlinaCoder.exe is missing after installation")
    metadata_path = install_dir / "install.json"
    if not metadata_path.is_file():
        raise BootstrapError("install metadata is missing after installation")
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise BootstrapError("install metadata is unreadable after installation") from exc
    if not isinstance(metadata, dict):
        raise BootstrapError("install metadata is invalid after installation")
    if not deferred_prerequisites and not bool(metadata.get("bootstrap_ready", False)):
        blockers = metadata.get("bootstrap_blockers", [])
        if isinstance(blockers, list):
            detail = ", ".join(str(item) for item in blockers)
        else:
            detail = str(blockers)
        raise BootstrapError("prerequisite bootstrap incomplete after installation: " + detail)


def _run_once(
    install_dir: Path,
    *,
    operation: str,
    source_exe: Path | None,
    bootstrapper: Any | None,
    deferred_prerequisites: bool,
    online: bool,
    model: str | None,
) -> Path:
    # Lazy import avoids circular initialization while preserving installer.py as
    # the canonical operation boundary.
    from . import installer

    if operation == "install":
        return installer.install(
            install_dir,
            source_exe=source_exe,
            operation="install",
            bootstrapper=bootstrapper,
            deferred_prerequisites=deferred_prerequisites,
            online=online,
            model=model,
        )
    if operation == "repair":
        return installer.repair(
            install_dir,
            source_exe=source_exe,
            bootstrapper=bootstrapper,
            deferred_prerequisites=deferred_prerequisites,
            online=online,
            model=model,
        )
    if operation == "upgrade":
        return installer.upgrade(
            install_dir,
            source_exe=source_exe,
            bootstrapper=bootstrapper,
            deferred_prerequisites=deferred_prerequisites,
            online=online,
            model=model,
        )
    raise ValueError(f"unsupported self-healing operation: {operation}")


def _effective_decision(exc: BaseException, *, online: bool) -> RecoveryDecision:
    decision = classify_failure(exc)
    if not online and decision.recoverable:
        # Offline mode is an explicit user constraint. Repeating an operation that
        # requires network access cannot repair it and only wastes time.
        return RecoveryDecision("offline_blocked", False, decision.remediations)
    return decision


def run_self_healing_operation(
    install_dir: Path | str,
    *,
    operation: str,
    source_exe: Path | None = None,
    bootstrapper_factory: BootstrapperFactory | None = None,
    deferred_prerequisites: bool = False,
    online: bool = True,
    model: str | None = None,
    policy: RecoveryPolicy | None = None,
    event_sink: SetupEventSink | None = None,
    cancellation_token: CancellationToken | None = None,
    sleep: Sleep = time.sleep,
) -> Path:
    """Converge install/repair/upgrade toward one verified healthy state.

    Recoverable failures are diagnosed, journaled, cleaned at safe transient
    boundaries and retried with bounded backoff. Fatal trust failures and user
    cancellation are never bypassed.
    """

    if operation not in {"install", "repair", "upgrade"}:
        raise ValueError(f"unsupported self-healing operation: {operation}")

    root = Path(install_dir)
    root.mkdir(parents=True, exist_ok=True)
    selected_policy = policy or RecoveryPolicy()
    journal = RecoveryJournal(root, sleep=sleep)
    token = cancellation_token or CancellationToken()

    for attempt in range(1, selected_policy.max_attempts + 1):
        token.raise_if_cancelled()
        cleanup_transients(root, sleep=sleep)
        journal.record_running(
            operation=operation,
            attempt=attempt,
            max_attempts=selected_policy.max_attempts,
        )
        _emit(
            event_sink,
            kind="start" if attempt == 1 else "retrying",
            message=(
                "Vérification et installation d’AlinaCoder"
                if attempt == 1
                else "Nouvelle tentative de réparation automatique"
            ),
            detail=f"tentative {attempt}/{selected_policy.max_attempts}",
            current=attempt,
            total=selected_policy.max_attempts,
        )

        try:
            if deferred_prerequisites:
                bootstrapper = None
            elif bootstrapper_factory is not None:
                bootstrapper = bootstrapper_factory()
            else:
                from . import installer

                bootstrapper = installer.build_bootstrapper(root)

            target = _run_once(
                root,
                operation=operation,
                source_exe=source_exe,
                bootstrapper=bootstrapper,
                deferred_prerequisites=deferred_prerequisites,
                online=online,
                model=model,
            )
            _validate_full_install(root, target, deferred_prerequisites=deferred_prerequisites)
            journal.record_ready(
                operation=operation,
                attempt=attempt,
                max_attempts=selected_policy.max_attempts,
                installed_path=target,
            )
            _emit(
                event_sink,
                kind="complete",
                message="AlinaCoder est entièrement installé et vérifié",
                detail=str(target),
                current=selected_policy.max_attempts,
                total=selected_policy.max_attempts,
            )
            return target
        except BaseException as exc:
            # KeyboardInterrupt/SystemExit must keep their process semantics.
            if not isinstance(exc, Exception):
                raise
            decision = _effective_decision(exc, online=online)
            journal.record_failure(
                operation=operation,
                attempt=attempt,
                max_attempts=selected_policy.max_attempts,
                exc=exc,
                decision=decision,
            )
            exhausted = attempt >= selected_policy.max_attempts
            if not decision.recoverable or exhausted:
                _emit(
                    event_sink,
                    kind="error",
                    message="La réparation automatique ne peut pas continuer en sécurité",
                    detail=f"{decision.category}: {exc}",
                    current=attempt,
                    total=selected_policy.max_attempts,
                )
                raise

            removed = cleanup_transients(root, sleep=sleep)
            _emit(
                event_sink,
                kind="retry",
                message="Problème détecté — AlinaCoder se répare automatiquement",
                detail=(
                    f"{decision.category}; remédiations={','.join(decision.remediations)}; "
                    f"nettoyés={len(removed)}"
                ),
                current=attempt,
                total=selected_policy.max_attempts,
            )
            token.raise_if_cancelled()
            delay = backoff_seconds(selected_policy, attempt)
            if delay > 0:
                sleep(delay)

    raise AssertionError("unreachable self-healing loop exit")


def bind_self_healing_installer() -> None:
    """Expose the runner on the canonical installer module without import cycles."""

    from . import installer

    installer.run_self_healing_operation = run_self_healing_operation  # type: ignore[attr-defined]


__all__ = ["bind_self_healing_installer", "run_self_healing_operation"]
