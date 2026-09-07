from __future__ import annotations

from dataclasses import dataclass, replace
import os
from pathlib import Path
import subprocess
from typing import Callable

from .setup_events import (
    CancellationToken,
    SetupCancelled,
    SetupEvent,
    SetupEventSink,
    SetupLogger,
    combine_event_sinks,
    default_setup_log_path,
)


@dataclass(frozen=True)
class SetupSnapshot:
    state: str = "idle"
    phase: str = "preparation"
    message: str = "Prêt à installer AlinaCoder"
    detail: str = ""
    selected_model: str = ""
    installed_path: str = ""
    last_error: str = ""
    log_path: str = ""
    can_retry: bool = False
    can_launch: bool = False


SetupOperation = Callable[[str | None, SetupEventSink, CancellationToken], tuple[Path, str]]


class SetupController:
    """UI-neutral orchestration for the visible Windows installer."""

    def __init__(
        self,
        install_dir: Path | str,
        *,
        operation: SetupOperation | None = None,
        event_sink: SetupEventSink | None = None,
        cancellation_token: CancellationToken | None = None,
        log_path: Path | str | None = None,
        launcher: Callable[[Path], None] | None = None,
    ) -> None:
        self.install_dir = Path(install_dir)
        self.log_path = Path(log_path) if log_path is not None else default_setup_log_path()
        self._logger = SetupLogger(self.log_path)
        self._sink = combine_event_sinks(self._logger, event_sink, self._capture_event)
        self._token = cancellation_token or CancellationToken()
        self._operation = operation or self._default_operation
        self._launcher = launcher or self._default_launcher
        self._last_model: str | None = None
        self._snapshot = SetupSnapshot(log_path=str(self.log_path))

    @property
    def snapshot(self) -> SetupSnapshot:
        return self._snapshot

    @property
    def cancellation_token(self) -> CancellationToken:
        return self._token

    def _capture_event(self, event: SetupEvent) -> None:
        self._snapshot = replace(
            self._snapshot,
            phase=event.phase or self._snapshot.phase,
            message=event.message or self._snapshot.message,
            detail=event.detail or self._snapshot.detail,
        )

    def notify(self, event: SetupEvent) -> None:
        """Publish one setup event to both durable log and graphical observers."""
        self._sink(event)

    def _default_operation(
        self,
        model: str | None,
        event_sink: SetupEventSink,
        cancellation_token: CancellationToken,
    ) -> tuple[Path, str]:
        from . import installer
        from .windows_trust import ObservableWindowsBootstrapAdapter
        from .prerequisites import PrerequisiteBootstrapper, PrerequisiteManifest

        manifest = PrerequisiteManifest.load(installer._bundled_manifest())
        last_adapter: dict[str, ObservableWindowsBootstrapAdapter] = {}

        def bootstrapper_factory() -> PrerequisiteBootstrapper:
            adapter = ObservableWindowsBootstrapAdapter(
                self.install_dir,
                manifest,
                event_sink=event_sink,
                cancellation_token=cancellation_token,
            )
            last_adapter["value"] = adapter
            return PrerequisiteBootstrapper(manifest, adapter)

        operation = "upgrade" if (self.install_dir / "AlinaCoder.exe").exists() else "install"
        target = installer.run_self_healing_operation(
            self.install_dir,
            operation=operation,
            bootstrapper_factory=bootstrapper_factory,
            online=True,
            model=model,
            event_sink=event_sink,
            cancellation_token=cancellation_token,
        )

        adapter = last_adapter.get("value")
        state = adapter.load_state() if adapter is not None else None
        selected = state.selected_model if state is not None else (model or "")
        return target, selected

    @staticmethod
    def _default_launcher(path: Path) -> None:
        kwargs = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
        if os.name == "nt":
            kwargs["creationflags"] = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.Popen([str(path)], **kwargs)  # type: ignore[arg-type]

    def run_install(self, model: str | None = None) -> SetupSnapshot:
        self._last_model = model
        if self._token.cancelled:
            self._token = CancellationToken()
        self._snapshot = SetupSnapshot(
            state="running",
            phase="preparation",
            message="Préparation de l'installation",
            log_path=str(self.log_path),
        )
        self.notify(SetupEvent("preparation", "start", "Préparation de l'installation", str(self.install_dir)))
        try:
            target, selected_model = self._operation(model, self._sink, self._token)
            self._token.raise_if_cancelled()
            self._snapshot = replace(
                self._snapshot,
                state="success",
                phase="alinacoder",
                message="AlinaCoder est installé",
                selected_model=selected_model,
                installed_path=str(target),
                last_error="",
                can_retry=False,
                can_launch=Path(target).is_file(),
            )
            self.notify(SetupEvent("alinacoder", "complete", "AlinaCoder installé", str(target)))
        except SetupCancelled as exc:
            self._snapshot = replace(
                self._snapshot,
                state="cancelled",
                message="Installation annulée",
                detail=str(exc),
                last_error=str(exc),
                can_retry=True,
                can_launch=False,
            )
            self.notify(SetupEvent("cancel", "cancelled", "Installation annulée", str(exc)))
        except Exception as exc:
            detail = f"{type(exc).__name__}: {exc}"
            self._snapshot = replace(
                self._snapshot,
                state="error",
                message="L'installation a rencontré une erreur après réparation automatique",
                detail=detail,
                last_error=detail,
                can_retry=True,
                can_launch=False,
            )
            self.notify(
                SetupEvent(
                    "error",
                    "error",
                    "La réparation automatique n'a pas pu terminer l'installation",
                    detail,
                )
            )
        return self._snapshot

    def retry(self) -> SetupSnapshot:
        if self._snapshot.state not in {"error", "cancelled"}:
            return self._snapshot
        self._token = CancellationToken()
        return self.run_install(self._last_model)

    def cancel(self) -> None:
        self._token.cancel()
        self.notify(SetupEvent(self._snapshot.phase, "info", "Annulation demandée"))

    def launch_installed(self) -> bool:
        if not self._snapshot.can_launch or not self._snapshot.installed_path:
            return False
        path = Path(self._snapshot.installed_path)
        if not path.is_file():
            return False
        self._launcher(path)
        return True
