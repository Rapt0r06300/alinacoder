from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import DesktopControlPlane, DesktopStateStore, WorkbenchModel, self_test
from .workbench import DesktopWorkbench, run_acceptance_e2e


def _default_state_path() -> Path:
    return Path.home() / ".alinacoder" / "desktop-state.json"


def _default_runtime_state_path() -> Path:
    return Path.home() / ".alinacoder" / "canonical.sqlite"


def run_gui() -> int:
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog, ttk

    root = tk.Tk()
    root.title("AlinaCoder v0.2")
    try:
        root.tk.call("tk", "scaling", root.winfo_fpixels("1i") / 72.0)
    except Exception:
        pass

    legacy_control = DesktopControlPlane()
    store = DesktopStateStore(_default_state_path())
    state = store.load()
    workbench: DesktopWorkbench | None = None

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    header = ttk.Frame(root)
    header.grid(row=0, column=0, sticky="ew")
    status = tk.StringVar(value=state.get("control_state", legacy_control.state))
    project_text = tk.StringVar(value=state.get("project", "No project"))
    ttk.Label(header, text="AlinaCoder", name="title").pack(side="left", padx=8)
    ttk.Label(header, textvariable=project_text, name="project_status").pack(side="left", padx=8)
    ttk.Label(header, textvariable=status, name="status").pack(side="right", padx=8)

    body = ttk.Panedwindow(root, orient="horizontal")
    body.grid(row=1, column=0, sticky="nsew")
    chat = ttk.Frame(body)
    inspector = ttk.Notebook(body)
    body.add(chat, weight=3)
    body.add(inspector, weight=2)
    chat.columnconfigure(0, weight=1)
    chat.rowconfigure(0, weight=1)

    transcript = tk.Text(chat, wrap="word", name="transcript")
    transcript.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=8, pady=8)
    composer = ttk.Entry(chat, name="composer")
    composer.grid(row=1, column=0, sticky="ew", padx=(8, 4), pady=(0, 8))
    composer.insert(0, state.get("draft", ""))
    send_button = ttk.Button(chat, text="Send", name="send")
    send_button.grid(row=1, column=1, sticky="ew", padx=(4, 8), pady=(0, 8))

    controls = ttk.Frame(chat)
    controls.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8))

    inspector_frames: dict[str, tk.Text] = {}
    for name in ["Plan", "Context", "Diff", "Tests", "Git", "Receipts", "Run Inspector", "Timeline", "Diagnostics"]:
        frame = ttk.Frame(inspector)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        inspector.add(frame, text=name)
        view = tk.Text(frame, wrap="word", height=8, name=name.lower().replace(" ", "_"))
        view.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        view.insert("1.0", f"{name} — canonical state view")
        view.configure(state="disabled")
        inspector_frames[name] = view

    def set_view(name: str, value: str) -> None:
        view = inspector_frames[name]
        view.configure(state="normal")
        view.delete("1.0", "end")
        view.insert("1.0", value)
        view.configure(state="disabled")

    def persist() -> None:
        store.save(
            {
                "draft": composer.get(),
                "control_state": status.get(),
                "project": project_text.get() if project_text.get() != "No project" else "",
            }
        )

    def refresh_views() -> None:
        if workbench is None:
            return
        snap = workbench.snapshot()
        set_view("Context", json.dumps(snap, indent=2, ensure_ascii=False, sort_keys=True))
        try:
            set_view("Diff", workbench.git.diff(workbench.workspace))
            set_view("Git", json.dumps(workbench.status(), indent=2, sort_keys=True))
        except Exception as exc:
            set_view("Diagnostics", f"Git refresh failed: {exc}")
        set_view("Receipts", json.dumps(snap.get("receipts", []), indent=2, ensure_ascii=False))
        goal_id = snap.get("active_goal_id")
        if goal_id:
            try:
                goal = workbench.goals.get_goal(goal_id)
                set_view("Plan", json.dumps(goal.to_dict(), indent=2, ensure_ascii=False))
            except Exception:
                pass

    def open_project(path: str | None = None) -> None:
        nonlocal workbench
        selected = path or filedialog.askdirectory(title="Open Git project")
        if not selected:
            return
        try:
            if workbench is not None:
                workbench.close()
            workbench = DesktopWorkbench(selected, state_path=_default_runtime_state_path(), session_id="desktop")
            project = workbench.open_project()
            project_text.set(project["path"])
            status.set(workbench.snapshot().get("control_state", "RUNNING"))
            transcript.insert("end", f"\n[system] Opened {project['path']} on {project['branch']}\n")
            persist()
            refresh_views()
        except Exception as exc:
            workbench = None
            messagebox.showerror("Open project failed", str(exc))

    def send_message() -> None:
        if workbench is None:
            messagebox.showinfo("Project required", "Open a Git project first.")
            return
        text = composer.get().strip()
        if not text:
            return
        try:
            workbench.send_message(text)
            transcript.insert("end", f"\nYou: {text}\n")
            if text.startswith("/goal "):
                objective = text[6:].strip()
                goal = workbench.start_goal(
                    objective,
                    ["requested change implemented", "verification passes", "main commit ready"],
                )
                transcript.insert("end", f"AlinaCoder: Goal {goal.goal_id} created and persisted.\n")
            composer.delete(0, "end")
            persist()
            refresh_views()
        except Exception as exc:
            messagebox.showerror("Action failed", str(exc))

    def set_control(action: str) -> None:
        try:
            if workbench is not None:
                getattr(workbench, action)()
                status.set(workbench.snapshot()["control_state"])
            else:
                getattr(legacy_control, action)()
                status.set(legacy_control.state)
            persist()
            refresh_views()
        except Exception as exc:
            messagebox.showerror("Control failed", str(exc))

    def run_tests() -> None:
        if workbench is None:
            return
        receipt = workbench.run_tests(["git", "diff", "--check"])
        set_view("Tests", json.dumps(receipt, indent=2, ensure_ascii=False))
        refresh_views()

    def commit_main() -> None:
        if workbench is None:
            return
        message = simpledialog.askstring("Commit on main", "Commit message:", initialvalue="AlinaCoder: verified change")
        if not message:
            return
        try:
            receipt = workbench.commit_main(message)
            transcript.insert("end", f"\n[git] {json.dumps(receipt, sort_keys=True)}\n")
            refresh_views()
        except Exception as exc:
            messagebox.showerror("Commit failed", str(exc))

    ttk.Button(controls, text="Open Project", command=open_project, name="open_project").pack(side="left", padx=2)
    for label, action in [("Pause", "pause"), ("Resume", "resume"), ("STOP", "stop"), ("Takeover", "takeover")]:
        ttk.Button(controls, text=label, command=lambda action=action: set_control(action), name=label.lower()).pack(side="left", padx=2)
    ttk.Button(controls, text="Run Tests", command=run_tests, name="run_tests").pack(side="left", padx=2)
    ttk.Button(controls, text="Commit main", command=commit_main, name="commit_main").pack(side="left", padx=2)
    send_button.configure(command=send_message)
    composer.bind("<Return>", lambda _event: send_message())

    def on_close() -> None:
        persist()
        if workbench is not None:
            workbench.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.geometry("1200x760")
    composer.focus_set()

    last_project = state.get("project")
    if last_project and Path(last_project).joinpath(".git").exists():
        root.after(50, lambda: open_project(last_project))

    root.mainloop()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="AlinaCoder")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--semantic-ui", action="store_true")
    parser.add_argument("--acceptance-e2e", action="store_true")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--evidence-out", type=Path)
    args = parser.parse_args(argv)
    if args.self_test:
        result = self_test()
        print(json.dumps(result, sort_keys=True))
        return 0 if result["ok"] else 2
    if args.semantic_ui:
        print(json.dumps(WorkbenchModel().semantic_ui_snapshot(), sort_keys=True))
        return 0
    if args.acceptance_e2e:
        if args.workspace is None:
            parser.error("--acceptance-e2e requires --workspace")
        result = run_acceptance_e2e(args.workspace, evidence_out=args.evidence_out)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["ok"] else 2
    return run_gui()


if __name__ == "__main__":
    raise SystemExit(main())
