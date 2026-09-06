from __future__ import annotations

import argparse
import json
from pathlib import Path

from alinacoder.intelligence_mesh.credentials import ProviderCredentialVault
from alinacoder.intelligence_mesh.provider_atlas import normative_provider_atlas

from .core import DesktopControlPlane, DesktopStateStore, WorkbenchModel, self_test
from .experience import FirstRunOnboarding, VoiceInputAdapter
from .workbench import DesktopWorkbench, run_acceptance_e2e


_PRODUCT_CAPABILITIES = frozenset(
    {
        "conversation_first_workbench",
        "first_run_onboarding",
        "voice_input",
        "provider_configuration",
        "secure_provider_credentials",
        "provider_settings_ui",
        "real_zero_cost_provider_fabric",
        "local_runtime_configuration",
        "persistent_project_session",
        "goal_controls",
        "diff_test_git_inspectors",
        "stop_pause_resume_takeover",
        "semantic_ui_oracle",
    }
)


def product_capabilities() -> set[str]:
    return set(_PRODUCT_CAPABILITIES)


def _default_state_path() -> Path:
    return Path.home() / ".alinacoder" / "desktop-state.json"


def _default_runtime_state_path() -> Path:
    return Path.home() / ".alinacoder" / "canonical.sqlite"


def _default_credential_path() -> Path:
    return Path.home() / ".alinacoder" / "provider-credentials.json"


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
    onboarding = FirstRunOnboarding.from_dict(state.get("onboarding"))
    voice = VoiceInputAdapter()
    credential_vault = ProviderCredentialVault(_default_credential_path())
    provider_atlas = normative_provider_atlas()
    workbench: DesktopWorkbench | None = None

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    header = ttk.Frame(root)
    header.grid(row=0, column=0, sticky="ew")
    status = tk.StringVar(value=state.get("control_state", legacy_control.state))
    project_text = tk.StringVar(value=state.get("project", "No project"))
    inference_text = tk.StringVar(
        value=(
            f"{onboarding.provider_mode}/{onboarding.local_runtime or '-'}"
            if onboarding.provider_mode
            else "Inference not configured"
        )
    )
    ttk.Label(header, text="AlinaCoder", name="title").pack(side="left", padx=8)
    ttk.Label(header, textvariable=project_text, name="project_status").pack(side="left", padx=8)
    ttk.Label(header, textvariable=inference_text, name="inference_status").pack(side="left", padx=8)
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
    transcript.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=8, pady=8)
    composer = ttk.Entry(chat, name="composer")
    composer.grid(row=1, column=0, sticky="ew", padx=(8, 4), pady=(0, 8))
    composer.insert(0, state.get("draft", ""))
    voice_button = ttk.Button(chat, text="Voice", name="voice")
    voice_button.grid(row=1, column=1, sticky="ew", padx=4, pady=(0, 8))
    send_button = ttk.Button(chat, text="Send", name="send")
    send_button.grid(row=1, column=2, sticky="ew", padx=(4, 8), pady=(0, 8))

    controls = ttk.Frame(chat)
    controls.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 8))

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
                "onboarding": onboarding.to_dict(),
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

    def configure_providers() -> None:
        candidates = [entry for entry in provider_atlas.active() if entry.auth_env]
        window = tk.Toplevel(root)
        window.title("Zero-cost Provider Settings")
        window.geometry("760x440")
        window.transient(root)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(1, weight=1)
        ttk.Label(
            window,
            text="Provider keys are encrypted with Windows DPAPI. A key alone never enables paid usage: zero-cost/account safety is re-proven before routing.",
            wraplength=720,
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=10)
        listing = tk.Listbox(window, exportselection=False)
        listing.grid(row=1, column=0, sticky="nsew", padx=12)
        status_text = tk.StringVar(value="Select a provider")
        notes_text = tk.StringVar(value="")
        ttk.Label(window, textvariable=status_text).grid(row=2, column=0, sticky="w", padx=12, pady=(8, 0))
        ttk.Label(window, textvariable=notes_text, wraplength=720).grid(row=3, column=0, sticky="ew", padx=12, pady=(2, 8))
        for entry in candidates:
            listing.insert("end", f"{entry.label} ({entry.provider_id})")

        def selected_entry():
            selection = listing.curselection()
            if not selection:
                return None
            return candidates[int(selection[0])]

        def refresh_provider_status(_event=None) -> None:
            entry = selected_entry()
            if entry is None:
                status_text.set("Select a provider")
                notes_text.set("")
                return
            connected = credential_vault.has(entry.provider_id)
            status_text.set(f"{entry.label}: {'credential stored' if connected else 'credential not configured'}")
            notes_text.set(entry.notes or "Exact zero-cost qualification is required before use.")

        def save_provider_key() -> None:
            entry = selected_entry()
            if entry is None:
                return
            value = simpledialog.askstring(
                f"{entry.label} credential",
                "Paste the provider API key/token. It will be encrypted locally with Windows DPAPI.",
                show="*",
                parent=window,
            )
            if value:
                credential_vault.put(entry.provider_id, value)
                refresh_provider_status()

        def remove_provider_key() -> None:
            entry = selected_entry()
            if entry is None:
                return
            credential_vault.delete(entry.provider_id)
            refresh_provider_status()

        listing.bind("<<ListboxSelect>>", refresh_provider_status)
        actions = ttk.Frame(window)
        actions.grid(row=4, column=0, sticky="ew", padx=12, pady=10)
        ttk.Button(actions, text="Add / Replace Key", command=save_provider_key).pack(side="left", padx=(0, 6))
        ttk.Button(actions, text="Remove Key", command=remove_provider_key).pack(side="left", padx=6)
        ttk.Button(actions, text="Close", command=window.destroy).pack(side="right")
        if candidates:
            listing.selection_set(0)
            refresh_provider_status()

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
            onboarding.configure_project(project["path"])
            project_text.set(project["path"])
            status.set(workbench.snapshot().get("control_state", "RUNNING"))
            transcript.insert("end", f"\n[system] Opened {project['path']} on {project['branch']}\n")
            persist()
            refresh_views()
        except Exception as exc:
            workbench = None
            messagebox.showerror("Open project failed", str(exc))

    def configure_first_run() -> None:
        selected = onboarding.project_path
        if not selected or not Path(selected).joinpath(".git").exists():
            selected = filedialog.askdirectory(title="AlinaCoder first run — choose your Git project")
            if not selected:
                return
        provider_mode = simpledialog.askstring(
            "Inference mode",
            "Choose: local-only, free-cloud, or hybrid",
            initialvalue=onboarding.provider_mode or "local-only",
        )
        if provider_mode is None:
            return
        provider_mode = provider_mode.strip().lower()
        local_runtime = onboarding.local_runtime
        if provider_mode in {"local-only", "hybrid"}:
            local_runtime_value = simpledialog.askstring(
                "Local runtime",
                "Local runtime (ollama, llama.cpp, lm-studio, vllm)",
                initialvalue=local_runtime or "ollama",
            )
            if local_runtime_value is None:
                return
            local_runtime = local_runtime_value
        try:
            onboarding.configure_project(selected)
            onboarding.configure_inference(provider_mode=provider_mode, local_runtime=local_runtime)
            onboarding.enable_input_mode("text")
            onboarding.enable_input_mode("voice")
            onboarding.finish()
            inference_text.set(f"{onboarding.provider_mode}/{onboarding.local_runtime or '-'}")
            persist()
            open_project(selected)
            transcript.insert("end", "[system] First-run onboarding complete. Text and Voice are available.\n")
        except Exception as exc:
            messagebox.showerror("Onboarding failed", str(exc))

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

    def capture_voice() -> None:
        if not onboarding.complete:
            messagebox.showinfo("Setup required", "Complete First-run Setup before using Voice.")
            return
        previous = status.get()
        status.set("LISTENING")
        root.update_idletasks()
        try:
            spoken = voice.capture_once()
            composer.delete(0, "end")
            composer.insert(0, spoken)
            transcript.insert("end", f"\n[voice] {spoken}\n")
            persist()
        except Exception as exc:
            messagebox.showerror("Voice input failed", str(exc))
        finally:
            if workbench is not None:
                status.set(workbench.snapshot().get("control_state", previous))
            else:
                status.set(previous)

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

    ttk.Button(controls, text="First-run Setup", command=configure_first_run, name="setup").pack(side="left", padx=2)
    ttk.Button(controls, text="Providers", command=configure_providers, name="provider_settings").pack(side="left", padx=2)
    ttk.Button(controls, text="Open Project", command=open_project, name="open_project").pack(side="left", padx=2)
    for label, action in [("Pause", "pause"), ("Resume", "resume"), ("STOP", "stop"), ("Takeover", "takeover")]:
        ttk.Button(controls, text=label, command=lambda action=action: set_control(action), name=label.lower()).pack(side="left", padx=2)
    ttk.Button(controls, text="Run Tests", command=run_tests, name="run_tests").pack(side="left", padx=2)
    ttk.Button(controls, text="Commit main", command=commit_main, name="commit_main").pack(side="left", padx=2)
    voice_button.configure(command=capture_voice)
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

    last_project = onboarding.project_path or state.get("project")
    if onboarding.complete and last_project and Path(last_project).joinpath(".git").exists():
        root.after(50, lambda: open_project(last_project))
    elif not onboarding.complete:
        root.after(150, configure_first_run)

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
        result["product_capabilities"] = sorted(product_capabilities())
        print(json.dumps(result, sort_keys=True))
        return 0 if result["ok"] else 2
    if args.semantic_ui:
        result = WorkbenchModel().semantic_ui_snapshot()
        result["product_capabilities"] = sorted(product_capabilities())
        print(json.dumps(result, sort_keys=True))
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
