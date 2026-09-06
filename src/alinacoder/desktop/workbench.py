from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any, Sequence

from alinacoder.desktop.activity import ActivityEvent, sanitize_activity_details
from alinacoder.goal.engine import GoalEngine
from alinacoder.goal.models import GoalContract
from alinacoder.intelligence_mesh import CapabilityRequirement
from alinacoder.state.store import SessionNotFoundError, StateStore
from alinacoder.tools.git import GitMainExecutor
from alinacoder.tools.process import ManagedProcessRunner


class DesktopWorkbench:
    """Canonical desktop control surface shared by GUI, headless UI tests and packaged E2E."""

    def __init__(
        self,
        workspace: Path | str,
        *,
        state_path: Path | str,
        session_id: str = "desktop",
        inference_fabric: Any | None = None,
        inference_mode: str = "local-only",
    ) -> None:
        self.workspace = Path(workspace).resolve()
        self.store = StateStore(state_path)
        self.session_id = session_id
        mode = str(inference_mode).strip().lower()
        if mode not in {"local-only", "free-cloud", "hybrid"}:
            raise ValueError("inference_mode must be local-only, free-cloud, or hybrid")
        self.inference_fabric = inference_fabric
        self.inference_mode = mode
        try:
            self.store.get_state(session_id)
        except SessionNotFoundError:
            self.store.create_session(
                session_id,
                {
                    "project": {},
                    "transcript": [],
                    "active_goal_id": None,
                    "receipts": [],
                    "control_state": "RUNNING",
                    "activity": [],
                    "next_activity_id": 1,
                    "next_run_id": 1,
                    "current_run": None,
                },
            )
        self.goals = GoalEngine(self.store, session_id)
        self.git = GitMainExecutor()
        self.runner = ManagedProcessRunner()

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _ensure_state_shape(data: dict[str, Any]) -> None:
        data.setdefault("project", {})
        data.setdefault("transcript", [])
        data.setdefault("active_goal_id", None)
        data.setdefault("receipts", [])
        data.setdefault("control_state", "RUNNING")
        data.setdefault("activity", [])
        data.setdefault("next_activity_id", 1)
        data.setdefault("next_run_id", 1)
        data.setdefault("current_run", None)

    def close(self) -> None:
        self.store.close()

    def __enter__(self) -> "DesktopWorkbench":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _mutate(self, event_kind: str, mutate, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        state = self.store.get_state(self.session_id)
        data = deepcopy(state.data)
        self._ensure_state_shape(data)
        mutate(data)
        epoch = self.store.acquire_writer(self.session_id)
        committed = self.store.commit_state(
            self.session_id,
            state.version,
            epoch,
            data,
            event_kind,
            sanitize_activity_details(metadata or {}),
        )
        return committed.data

    def _receipt(self, action: str, ok: bool, details: dict[str, Any]) -> dict[str, Any]:
        receipt = {"action": action, "ok": bool(ok), "details": sanitize_activity_details(details)}
        self._mutate(
            "desktop_receipt",
            lambda data: data.setdefault("receipts", []).append(receipt),
            {"action": action, "ok": bool(ok)},
        )
        return deepcopy(receipt)

    def snapshot(self) -> dict[str, Any]:
        data = deepcopy(self.store.get_state(self.session_id).data)
        self._ensure_state_shape(data)
        return data

    def emit_activity(
        self,
        kind: str,
        summary: str,
        *,
        status: str = "info",
        run_id: str | None = None,
        phase: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        holder: dict[str, Any] = {}

        def mutate(data: dict[str, Any]) -> None:
            sequence = int(data.setdefault("next_activity_id", 1))
            event = ActivityEvent(
                event_id=f"activity:{sequence}",
                timestamp=self._utc_now(),
                kind=str(kind),
                summary=str(summary),
                status=str(status),
                run_id=str(run_id) if run_id is not None else None,
                phase=str(phase) if phase is not None else None,
                details=sanitize_activity_details(details or {}),
            ).to_dict()
            data["next_activity_id"] = sequence + 1
            data.setdefault("activity", []).append(event)
            holder.update(event)

        self._mutate(
            "desktop_activity",
            mutate,
            {"kind": str(kind), "status": str(status), "run_id": run_id},
        )
        return deepcopy(holder)

    def activity(self) -> list[dict[str, Any]]:
        return deepcopy(list(self.snapshot().get("activity", [])))

    def current_run(self) -> dict[str, Any] | None:
        current = self.snapshot().get("current_run")
        return deepcopy(current) if isinstance(current, dict) else None

    def open_project(self) -> dict[str, Any]:
        if not (self.workspace / ".git").exists():
            raise ValueError("workspace must be a Git repository")
        branch = self.git.current_branch(self.workspace)
        self.git.validate_target(branch)
        project = {
            "path": str(self.workspace),
            "branch": branch,
            "head": self.git.head(self.workspace),
        }
        self._mutate("desktop_project_opened", lambda data: data.__setitem__("project", project), project)
        self._receipt("open_project", True, project)
        self.emit_activity(
            "project_opened",
            f"Opened project on {branch}",
            status="success",
            details={"path": project["path"], "branch": branch, "head": project["head"]},
        )
        return project

    @staticmethod
    def _canonical_messages(transcript: list[dict[str, Any]]) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        for item in transcript:
            role = str(item.get("role", ""))
            text = str(item.get("text", ""))
            if role in {"user", "assistant"} and text:
                messages.append({"role": role, "content": text})
        return messages

    def _append_user_message(self, text: str) -> None:
        message = {"role": "user", "text": str(text)}
        self._mutate(
            "desktop_message",
            lambda data: data.setdefault("transcript", []).append(message),
            {"role": "user"},
        )

    def _allocate_run(self, text: str) -> dict[str, Any]:
        holder: dict[str, Any] = {}

        def mutate(data: dict[str, Any]) -> None:
            sequence = int(data.setdefault("next_run_id", 1))
            run_id = f"run:{sequence}"
            data["next_run_id"] = sequence + 1
            run = {
                "run_id": run_id,
                "status": "running",
                "phase": "inference",
                "provider_id": None,
                "model_id": None,
                "error": None,
                "started_at": self._utc_now(),
                "finished_at": None,
                "request_preview": str(text)[:240],
            }
            data["current_run"] = run
            holder.update(run)

        self._mutate("desktop_run_started", mutate, {"status": "running", "phase": "inference"})
        self.emit_activity(
            "run_started",
            "Started agent run",
            status="running",
            run_id=str(holder["run_id"]),
            phase="inference",
            details={"request_preview": holder["request_preview"]},
        )
        return deepcopy(holder)

    def begin_message(self, text: str) -> dict[str, Any]:
        if self.inference_fabric is None:
            raise RuntimeError("inference fabric is not configured")
        self._append_user_message(text)
        run = self._allocate_run(text)
        messages = self._canonical_messages(list(self.snapshot().get("transcript", [])))
        request = {
            "run_id": run["run_id"],
            "messages": messages,
            "requirement": CapabilityRequirement({"reasoning": 0.3, "code": 0.3}),
            "mode": self.inference_mode,
        }
        self.emit_activity(
            "inference_started",
            "Selecting model and generating response",
            status="running",
            run_id=str(run["run_id"]),
            phase="inference",
            details={"mode": self.inference_mode, "message_count": len(messages)},
        )
        return request

    def perform_inference(self, request: dict[str, Any]) -> Any:
        """Perform only provider inference. Safe for a GUI worker thread: no StateStore/Tk access."""
        if self.inference_fabric is None:
            raise RuntimeError("inference fabric is not configured")
        return self.inference_fabric.complete(
            request["messages"],
            request["requirement"],
            mode=request["mode"],
        )

    def complete_message(self, run_id: str, response: Any) -> dict[str, Any]:
        provider_id = str(response.provider_id)
        model_id = str(response.model_id)
        assistant_text = str(response.text)
        assistant = {
            "role": "assistant",
            "text": assistant_text,
            "provider_id": provider_id,
            "model_id": model_id,
        }
        self._mutate(
            "desktop_assistant_message",
            lambda data: data.setdefault("transcript", []).append(assistant),
            {"role": "assistant", "provider_id": provider_id, "model_id": model_id},
        )
        self.emit_activity(
            "inference_completed",
            "Model response received",
            status="success",
            run_id=run_id,
            phase="inference",
            details={"provider_id": provider_id, "model_id": model_id},
        )

        finished_at = self._utc_now()

        def mutate_run(data: dict[str, Any]) -> None:
            current = data.get("current_run")
            if not isinstance(current, dict) or current.get("run_id") != run_id:
                raise RuntimeError(f"run is not current: {run_id}")
            current.update(
                {
                    "status": "completed",
                    "phase": "complete",
                    "provider_id": provider_id,
                    "model_id": model_id,
                    "error": None,
                    "finished_at": finished_at,
                }
            )

        self._mutate(
            "desktop_run_completed",
            mutate_run,
            {"run_id": run_id, "provider_id": provider_id, "model_id": model_id},
        )
        self.emit_activity(
            "run_completed",
            "Agent run completed",
            status="success",
            run_id=run_id,
            phase="complete",
            details={"provider_id": provider_id, "model_id": model_id},
        )
        details = {
            "assistant_text": assistant_text,
            "provider_id": provider_id,
            "model_id": model_id,
            "quota_remaining": response.quota_remaining,
            "metadata": sanitize_activity_details(response.metadata),
            "run_id": run_id,
        }
        return self._receipt("send_message", True, details)

    def fail_message(self, run_id: str, error: BaseException | str) -> None:
        public_error = str(error)[:1000]
        finished_at = self._utc_now()

        def mutate_run(data: dict[str, Any]) -> None:
            current = data.get("current_run")
            if not isinstance(current, dict) or current.get("run_id") != run_id:
                raise RuntimeError(f"run is not current: {run_id}")
            current.update(
                {
                    "status": "failed",
                    "phase": "failed",
                    "error": public_error,
                    "finished_at": finished_at,
                }
            )

        self._mutate("desktop_run_failed", mutate_run, {"run_id": run_id, "error": public_error})
        self.emit_activity(
            "run_failed",
            "Agent run failed",
            status="error",
            run_id=run_id,
            phase="failed",
            details={"error": public_error},
        )

    def send_message(self, text: str) -> dict[str, Any]:
        if self.inference_fabric is None:
            self._append_user_message(text)
            return self._receipt("send_message", True, {"text": text})
        request = self.begin_message(text)
        try:
            response = self.perform_inference(request)
        except Exception as exc:
            self.fail_message(str(request["run_id"]), exc)
            raise
        return self.complete_message(str(request["run_id"]), response)

    def start_goal(self, objective: str, criteria: list[str]) -> GoalContract:
        goal = self.goals.create_goal(objective, criteria)
        self._mutate(
            "desktop_goal_selected",
            lambda data: data.__setitem__("active_goal_id", goal.goal_id),
            {"goal_id": goal.goal_id},
        )
        self._receipt("start_goal", True, {"goal_id": goal.goal_id, "objective": objective})
        self.emit_activity(
            "goal_started",
            "Goal created and persisted",
            status="success",
            details={"goal_id": goal.goal_id, "objective": objective},
        )
        return goal

    def _safe_path(self, relative_path: str) -> Path:
        target = (self.workspace / relative_path).resolve()
        try:
            target.relative_to(self.workspace)
        except ValueError as exc:
            raise ValueError("workspace mutation escaped project root") from exc
        return target

    def write_text(self, relative_path: str, content: str) -> dict[str, Any]:
        branch = self.git.current_branch(self.workspace)
        self.git.validate_target(branch)
        target = self._safe_path(relative_path)
        effect_key = "desktop-write:" + hashlib.sha256(
            f"{self.workspace}:{relative_path}:{content}".encode()
        ).hexdigest()
        admitted = self.store.begin_effect(
            effect_key,
            self.session_id,
            {"path": relative_path, "sha256": hashlib.sha256(content.encode()).hexdigest()},
        )
        if admitted:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            self.git.mark_intent_to_add(self.workspace, relative_path)
            self.store.ack_effect(effect_key, {"written": True, "path": relative_path})
        details = {"path": relative_path, "effect_key": effect_key, "admitted": admitted}
        receipt = self._receipt("write_text", True, details)
        self.emit_activity(
            "file_written",
            f"Updated {relative_path}",
            status="success",
            details={"path": relative_path, "admitted": admitted},
        )
        return receipt

    def diff(self) -> str:
        value = self.git.diff(self.workspace)
        self._receipt("view_diff", True, {"bytes": len(value.encode())})
        self.emit_activity(
            "diff_inspected",
            "Refreshed Git diff",
            status="success",
            details={"bytes": len(value.encode())},
        )
        return value

    def run_tests(self, argv: Sequence[str]) -> dict[str, Any]:
        command = list(argv)
        self.emit_activity(
            "tests_started",
            "Started verification command",
            status="running",
            phase="verification",
            details={"argv": command},
        )
        process = self.runner.run(argv, timeout_seconds=120, cwd=str(self.workspace))
        details = {
            "argv": list(process.argv),
            "returncode": process.returncode,
            "timed_out": process.timed_out,
            "stdout": process.stdout[-4000:],
            "stderr": process.stderr[-4000:],
        }
        ok = process.returncode == 0 and not process.timed_out
        receipt = self._receipt("run_tests", ok, details)
        self.emit_activity(
            "tests_completed",
            "Verification command passed" if ok else "Verification command failed",
            status="success" if ok else "error",
            phase="verification",
            details={"argv": command, "returncode": process.returncode, "timed_out": process.timed_out},
        )
        return receipt

    def verify_goal_criterion(self, goal_id: str, criterion_id: str, evidence: dict[str, Any]) -> GoalContract:
        goal = self.goals.verify_criterion(goal_id, criterion_id, evidence)
        self._receipt(
            "verify_goal_criterion",
            True,
            {"goal_id": goal_id, "criterion_id": criterion_id},
        )
        self.emit_activity(
            "goal_criterion_verified",
            "Goal criterion verified",
            status="success",
            phase="verification",
            details={"goal_id": goal_id, "criterion_id": criterion_id},
        )
        return goal

    def complete_goal(self, goal_id: str) -> GoalContract:
        goal = self.goals.complete(goal_id)
        self._receipt("complete_goal", True, {"goal_id": goal_id})
        self.emit_activity(
            "goal_completed",
            "Goal completed",
            status="success",
            details={"goal_id": goal_id},
        )
        return goal

    def commit_main(self, message: str) -> dict[str, Any]:
        self.emit_activity(
            "git_commit_started",
            "Committing verified changes on main",
            status="running",
            phase="git",
            details={"message": message},
        )
        result = self.git.commit_all(self.workspace, message)
        ok = bool(result.get("ok"))
        self._receipt("commit_main", ok, result)
        self.emit_activity(
            "git_commit_completed",
            "Git commit completed" if ok else "Git commit failed",
            status="success" if ok else "error",
            phase="git",
            details={"branch": result.get("branch"), "head": result.get("head"), "ok": ok},
        )
        return dict(result)

    def status(self) -> dict[str, Any]:
        branch = self.git.current_branch(self.workspace)
        return {
            "branch": branch,
            "head": self.git.head(self.workspace),
            "dirty": bool(self.git.status_porcelain(self.workspace).strip()),
        }

    def _set_control(self, state: str) -> dict[str, Any]:
        data = self._mutate(
            "desktop_control_changed",
            lambda current: current.__setitem__("control_state", state),
            {"state": state},
        )
        self._receipt(state.lower(), True, {"state": state})
        kind_by_state = {
            "PAUSED": "control_paused",
            "RUNNING": "control_resumed",
            "STOPPED": "control_stopped",
            "USER_TAKEOVER": "control_takeover",
        }
        self.emit_activity(
            kind_by_state[state],
            f"Control state changed to {state}",
            status="stopped" if state == "STOPPED" else "info",
            details={"state": state},
        )
        return data

    def pause(self) -> None:
        self._set_control("PAUSED")

    def resume(self) -> None:
        self._set_control("RUNNING")

    def stop(self) -> None:
        self._set_control("STOPPED")

    def takeover(self) -> None:
        self._set_control("USER_TAKEOVER")


def run_acceptance_e2e(workspace: Path | str, *, evidence_out: Path | str | None = None) -> dict[str, Any]:
    workspace = Path(workspace).resolve()
    with tempfile.TemporaryDirectory(prefix="alinacoder-acceptance-") as td:
        state_path = Path(td) / "canonical.sqlite"
        workbench = DesktopWorkbench(workspace, state_path=state_path, session_id="packaged-e2e")
        baseline = workbench.status()
        project = workbench.open_project()
        workbench.send_message("/goal Add a deterministic acceptance marker and prove it")
        goal = workbench.start_goal(
            "Add a deterministic acceptance marker and prove it",
            ["artifact written", "tests pass", "main branch ready"],
        )
        workbench.write_text("acceptance.txt", "ALINACODER_ACCEPTANCE=PASS\n")
        diff = workbench.diff()
        test_receipt = workbench.run_tests(["git", "diff", "--check"])
        workbench.verify_goal_criterion(goal.goal_id, "c1", {"path": "acceptance.txt", "present_in_diff": "acceptance.txt" in diff})
        workbench.verify_goal_criterion(goal.goal_id, "c2", {"receipt": test_receipt})
        workbench.verify_goal_criterion(goal.goal_id, "c3", {"branch": project["branch"]})
        completed = workbench.complete_goal(goal.goal_id)
        committed = workbench.commit_main("acceptance: AlinaCoder packaged end-to-end mission")
        workbench.pause()
        paused_snapshot = workbench.snapshot()
        workbench.close()

        restarted = DesktopWorkbench(workspace, state_path=state_path, session_id="packaged-e2e")
        recovered = restarted.snapshot()
        restarted.resume()
        final_status = restarted.status()
        receipts = restarted.snapshot().get("receipts", [])
        restarted.close()

        report = {
            "ok": all(
                [
                    baseline["branch"] == "main",
                    project["branch"] == "main",
                    "acceptance.txt" in diff,
                    test_receipt["ok"],
                    completed.status.value == "COMPLETE",
                    committed["branch"] == "main",
                    committed["head"] != baseline["head"],
                    paused_snapshot.get("control_state") == "PAUSED",
                    recovered.get("control_state") == "PAUSED",
                    final_status["branch"] == "main",
                    not final_status["dirty"],
                ]
            ),
            "workspace": str(workspace),
            "head_before": baseline["head"],
            "head_after": final_status["head"],
            "goal_id": goal.goal_id,
            "goal_status": completed.status.value,
            "canonical_recovery": recovered.get("control_state") == "PAUSED",
            "receipts": len(receipts),
            "test_ok": bool(test_receipt["ok"]),
            "branch": final_status["branch"],
            "dirty": final_status["dirty"],
        }
        if evidence_out is not None:
            target = Path(evidence_out)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        return report
