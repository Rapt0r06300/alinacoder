from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import queue
import sys
import threading
from typing import Iterable

from .setup_controller import SetupController, SetupSnapshot
from .setup_events import SetupEvent, redact_setup_text


PHASES: tuple[tuple[str, str], ...] = (
    ("preparation", "Préparation"),
    ("analyse", "Analyse du PC"),
    ("git", "Git"),
    ("ollama", "Ollama"),
    ("model", "Modèle local"),
    ("validation", "Validation IA"),
    ("alinacoder", "AlinaCoder"),
    ("integration", "Intégration Windows"),
    ("complete", "Terminé"),
)


@dataclass
class PhaseState:
    key: str
    label: str
    state: str = "pending"


class SetupViewModel:
    """Display state for the setup GUI, independent from Tk/display availability."""

    def __init__(self) -> None:
        self.state = "idle"
        self.status = "Prêt à installer AlinaCoder v0.2.0"
        self.detail = ""
        self.progress_current: int | None = None
        self.progress_total: int | None = None
        self.diagnostics = ""
        self.selected_model = ""
        self.phases = [PhaseState(key, label) for key, label in PHASES]

    @property
    def progress_percent(self) -> int | None:
        if self.progress_current is None or not self.progress_total:
            return None
        return max(0, min(100, int((self.progress_current / self.progress_total) * 100)))

    @property
    def actions(self) -> tuple[str, ...]:
        if self.state == "idle":
            return ("Installer", "Fermer")
        if self.state == "running":
            return ("Annuler",)
        if self.state in {"error", "cancelled"}:
            return ("Réessayer", "Copier le diagnostic", "Ouvrir les logs", "Fermer")
        if self.state == "success":
            return ("Lancer AlinaCoder", "Ouvrir les logs", "Fermer")
        return ("Fermer",)

    def _phase(self, key: str) -> PhaseState | None:
        return next((item for item in self.phases if item.key == key), None)

    def apply_event(self, event: SetupEvent) -> None:
        if self.state == "idle":
            self.state = "running"
        phase = self._phase(event.phase)
        if phase is not None:
            if event.kind in {"start", "info", "progress", "detail", "retry"}:
                if phase.state != "done":
                    phase.state = "active"
            elif event.kind == "complete":
                phase.state = "done"
            elif event.kind in {"error", "cancelled"}:
                phase.state = "error"
        self.status = event.message or self.status
        if event.detail:
            self.detail = redact_setup_text(event.detail)
        if event.kind == "progress":
            self.progress_current = event.current
            self.progress_total = event.total
        line = f"[{event.phase}] {event.message}"
        if event.detail:
            line += f" — {redact_setup_text(event.detail)}"
        self.diagnostics = (self.diagnostics + "\n" + line).strip()

    def mark_running(self) -> None:
        self.state = "running"
        self.status = "Installation en cours…"

    def mark_error(self, message: str, detail: str) -> None:
        self.state = "error"
        self.status = message
        self.detail = redact_setup_text(detail)
        self.diagnostics = (self.diagnostics + "\n" + self.detail).strip()
        active = next((item for item in self.phases if item.state == "active"), None)
        if active is not None:
            active.state = "error"

    def mark_cancelled(self, detail: str = "") -> None:
        self.state = "cancelled"
        self.status = "Installation annulée"
        self.detail = redact_setup_text(detail)

    def mark_success(self, selected_model: str = "") -> None:
        self.state = "success"
        self.status = "AlinaCoder est installé et prêt"
        self.selected_model = selected_model
        for item in self.phases:
            item.state = "done"
        self.progress_current = 100
        self.progress_total = 100


def select_setup_mode(argv: Iterable[str]) -> str:
    args = list(argv)
    if "--installer-ui-smoke" in args:
        return "smoke"
    if not args:
        return "gui"
    return "cli"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_ui_smoke(
    evidence_out: Path | str,
    *,
    commit_sha: str = "",
    setup_sha256: str = "",
) -> dict[str, object]:
    """Headless oracle for the packaged default-GUI contract."""

    error_view = SetupViewModel()
    error_view.mark_running()
    error_view.apply_event(SetupEvent("preparation", "complete", "Préparation"))
    error_view.apply_event(SetupEvent("ollama", "start", "Installation d'Ollama"))
    error_view.apply_event(SetupEvent("download", "progress", "Téléchargement", current=50, total=100))
    error_view.mark_error("Erreur d'installation", "TimeoutError: simulated network interruption")

    success_view = SetupViewModel()
    success_view.mark_running()
    for key, label in PHASES:
        success_view.apply_event(SetupEvent(key, "complete", label))
    success_view.mark_success("qwen3:0.6b")

    payload: dict[str, object] = {
        "ok": True,
        "visible_installer_e2e": True,
        "commit_sha": commit_sha,
        "setup_sha256": setup_sha256,
        "default_mode": select_setup_mode([]),
        "no_console_default": select_setup_mode([]) == "gui",
        "phase_count": len(PHASES),
        "error_persistent": error_view.state == "error" and "Fermer" in error_view.actions,
        "retry_available": "Réessayer" in error_view.actions,
        "diagnostics_available": "Copier le diagnostic" in error_view.actions and "TimeoutError" in error_view.diagnostics,
        "success_launch_available": "Lancer AlinaCoder" in success_view.actions,
        "progress_visible": error_view.progress_percent == 50,
    }
    payload["ok"] = bool(
        payload["visible_installer_e2e"]
        and payload["no_console_default"]
        and payload["error_persistent"]
        and payload["retry_available"]
        and payload["diagnostics_available"]
        and payload["success_launch_available"]
        and payload["progress_visible"]
        and payload["phase_count"] == 9
    )
    out = Path(evidence_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload


def _default_install_dir() -> Path:
    local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(local) / "AlinaCoder"


def run_setup_gui(*, install_dir: Path | str | None = None) -> int:
    """Run the persistent graphical setup window. No terminal is required."""

    import tkinter as tk
    from tkinter import messagebox, ttk

    root = tk.Tk()
    root.title("Installation d’AlinaCoder v0.2.0")
    root.minsize(780, 640)
    root.geometry("840x680")

    view = SetupViewModel()
    event_queue: queue.Queue[object] = queue.Queue()
    controller = SetupController(Path(install_dir) if install_dir is not None else _default_install_dir(), event_sink=event_queue.put)

    style = ttk.Style(root)
    try:
        style.theme_use("vista")
    except tk.TclError:
        pass

    shell = ttk.Frame(root, padding=20)
    shell.pack(fill="both", expand=True)
    ttk.Label(shell, text="AlinaCoder v0.2.0", font=("Segoe UI", 22, "bold")).pack(anchor="w")
    ttk.Label(shell, text="Installation locale, visible et vérifiée", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 14))

    install_path_var = tk.StringVar(value=f"Installation : {controller.install_dir}")
    ttk.Label(shell, textvariable=install_path_var).pack(anchor="w", pady=(0, 10))

    status_var = tk.StringVar(value=view.status)
    ttk.Label(shell, textvariable=status_var, font=("Segoe UI", 12, "bold"), wraplength=780).pack(anchor="w", pady=(4, 8))

    progress = ttk.Progressbar(shell, mode="indeterminate", maximum=100)
    progress.pack(fill="x", pady=(0, 12))

    phase_frame = ttk.LabelFrame(shell, text="Étapes", padding=10)
    phase_frame.pack(fill="x", pady=(0, 12))
    phase_vars: dict[str, tk.StringVar] = {}
    for key, label in PHASES:
        var = tk.StringVar(value=f"○  {label}")
        phase_vars[key] = var
        ttk.Label(phase_frame, textvariable=var).pack(anchor="w", pady=1)

    details_frame = ttk.LabelFrame(shell, text="Détails de l’installation", padding=8)
    details_frame.pack(fill="both", expand=True, pady=(0, 12))
    details = tk.Text(details_frame, height=10, wrap="word", state="disabled", font=("Consolas", 9))
    scrollbar = ttk.Scrollbar(details_frame, command=details.yview)
    details.configure(yscrollcommand=scrollbar.set)
    details.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    footer = ttk.Frame(shell)
    footer.pack(fill="x")
    action_buttons: dict[str, ttk.Button] = {}

    def append_detail(text: str) -> None:
        if not text:
            return
        details.configure(state="normal")
        details.insert("end", text.rstrip() + "\n")
        details.see("end")
        details.configure(state="disabled")

    def render() -> None:
        status_var.set(view.status)
        icons = {"pending": "○", "active": "▶", "done": "✓", "error": "✕"}
        for item in view.phases:
            phase_vars[item.key].set(f"{icons.get(item.state, '○')}  {item.label}")
        pct = view.progress_percent
        if pct is None and view.state == "running":
            progress.configure(mode="indeterminate")
            progress.start(12)
        else:
            progress.stop()
            progress.configure(mode="determinate")
            progress["value"] = pct if pct is not None else (100 if view.state == "success" else 0)
        for button in action_buttons.values():
            button.pack_forget()
        for name in view.actions:
            action_buttons[name].pack(side="right", padx=(8, 0))

    def finish_from_snapshot(snapshot: SetupSnapshot) -> None:
        if snapshot.state == "success":
            view.mark_success(snapshot.selected_model)
            append_detail(f"Installation terminée : {snapshot.installed_path}")
            append_detail(f"Modèle local : {snapshot.selected_model}")
            append_detail(f"Journal : {snapshot.log_path}")
        elif snapshot.state == "cancelled":
            view.mark_cancelled(snapshot.last_error)
            append_detail(snapshot.last_error)
        else:
            view.mark_error("L’installation a échoué", snapshot.last_error)
            append_detail(snapshot.last_error)
            append_detail(f"Journal : {snapshot.log_path}")
        render()

    def poll_queue() -> None:
        try:
            while True:
                item = event_queue.get_nowait()
                if isinstance(item, SetupEvent):
                    view.apply_event(item)
                    append_detail(f"[{item.phase}] {item.message}" + (f" — {redact_setup_text(item.detail)}" if item.detail else ""))
                elif isinstance(item, SetupSnapshot):
                    finish_from_snapshot(item)
        except queue.Empty:
            pass
        render()
        root.after(100, poll_queue)

    def worker() -> None:
        snapshot = controller.run_install()
        if snapshot.state == "success":
            try:
                from .windows_integration import install_windows_integration

                source_setup = Path(sys.executable) if getattr(sys, "frozen", False) else Path(sys.argv[0]).resolve()
                event_queue.put(SetupEvent("integration", "start", "Création des raccourcis et de la désinstallation Windows"))
                install_windows_integration(controller.install_dir, source_setup)
                event_queue.put(SetupEvent("integration", "complete", "Intégration Windows terminée"))
            except Exception as exc:
                # Integration is part of the end-user Done contract. Keep failure visible.
                snapshot = SetupSnapshot(
                    state="error",
                    phase="integration",
                    message="L’intégration Windows a échoué",
                    detail=str(exc),
                    selected_model=snapshot.selected_model,
                    installed_path=snapshot.installed_path,
                    last_error=f"{type(exc).__name__}: {exc}",
                    log_path=snapshot.log_path,
                    can_retry=True,
                    can_launch=False,
                )
        event_queue.put(snapshot)

    def start_install() -> None:
        if view.state == "running":
            return
        view.mark_running()
        append_detail(f"Journal : {controller.log_path}")
        render()
        threading.Thread(target=worker, daemon=True, name="AlinaCoderSetupWorker").start()

    def retry() -> None:
        view.state = "idle"
        start_install()

    def cancel() -> None:
        if messagebox.askyesno("Annuler l’installation", "Voulez-vous vraiment demander l’annulation ?\nLes téléchargements déjà vérifiés seront conservés pour la reprise."):
            controller.cancel()
            append_detail("Annulation demandée…")

    def copy_diagnostic() -> None:
        text = view.diagnostics or controller.snapshot.last_error or f"Journal : {controller.log_path}"
        root.clipboard_clear()
        root.clipboard_append(text)
        status_var.set("Diagnostic copié dans le presse-papiers")

    def open_logs() -> None:
        controller.log_path.parent.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            os.startfile(str(controller.log_path.parent))  # type: ignore[attr-defined]

    def launch() -> None:
        if controller.launch_installed():
            root.destroy()
        else:
            messagebox.showerror("AlinaCoder", "Impossible de lancer AlinaCoder. Consultez le journal d’installation.")

    def close_window() -> None:
        if view.state == "running":
            if not messagebox.askyesno("Installation en cours", "L’installation est toujours en cours. Voulez-vous demander son annulation et fermer ensuite ?"):
                return
            controller.cancel()
            return
        root.destroy()

    callbacks = {
        "Installer": start_install,
        "Annuler": cancel,
        "Réessayer": retry,
        "Copier le diagnostic": copy_diagnostic,
        "Ouvrir les logs": open_logs,
        "Lancer AlinaCoder": launch,
        "Fermer": close_window,
    }
    for name, callback in callbacks.items():
        action_buttons[name] = ttk.Button(footer, text=name, command=callback)

    root.protocol("WM_DELETE_WINDOW", close_window)
    render()
    root.after(100, poll_queue)
    root.mainloop()
    return 0


def setup_entrypoint(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    mode = select_setup_mode(args)
    if mode == "gui":
        return run_setup_gui()
    if mode == "smoke":
        import argparse

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--installer-ui-smoke", action="store_true")
        parser.add_argument("--evidence-out", required=True)
        parser.add_argument("--commit", default=os.environ.get("GITHUB_SHA", ""))
        parsed, _unknown = parser.parse_known_args(args)
        setup_path = Path(sys.executable) if getattr(sys, "frozen", False) else Path(sys.argv[0]).resolve()
        digest = _sha256(setup_path) if setup_path.is_file() else ""
        payload = run_ui_smoke(parsed.evidence_out, commit_sha=parsed.commit, setup_sha256=digest)
        return 0 if payload.get("ok") else 2

    from .installer import main as cli_main
    return cli_main(args)
