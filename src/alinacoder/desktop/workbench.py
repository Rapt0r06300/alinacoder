from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any, Sequence

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
                },
            )
        self.goals = GoalEngine(self.store, session_id)
        self.git = GitMainExecutor()
        self.runner = ManagedProcessRunner()

    def close(self) -> None:
        self.store.close()

    def __enter__(self) -> "DesktopWorkbench":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _mutate(self, event_kind: str, mutate, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        state = self.store.get_state(self.session_id)
        data = deepcopy(state.data)
        mutate(data)
        epoch = self.store.acquire_writer(self.session_id)
        committed = self.store.commit_state(
            self.session_id,
            state.version,
            epoch,
            data,
            event_kind,
            metadata or {},
        )
        return committed.data

    def _receipt(self, action: str, ok: bool, details: dict[str, Any]) -> dict[str, Any]:
        receipt = {"action": action, "ok": bool(ok), "details": deepcopy(details)}
        self._mutate(
            "desktop_receipt",
            lambda data: data.setdefault("receipts", []).append(receipt),
            {"action": action, "ok": bool(ok)},
        )
        return receipt

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.store.get_state(self.session_id).data)

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

    def send_message(self, text: str) -> dict[str, Any]:
        message = {"role": "user", "text": text}
        self._mutate(
            "desktop_message",
            lambda data: data.setdefault("transcript", []).append(message),
            {"role": "user"},
        )
        if self.inference_fabric is None:
            return self._receipt("send_message", True, {"text": text})

        transcript = self.snapshot().get("transcript", [])
        messages = self._canonical_messages(list(transcript))
        requirement = CapabilityRequirement({"reasoning": 0.3, "code": 0.3})
        response = self.inference_fabric.complete(messages, requirement, mode=self.inference_mode)
        assistant = {
            "role": "assistant",
            "text": str(response.text),
            "provider_id": str(response.provider_id),
            "model_id": str(response.model_id),
        }
        self._mutate(
            "desktop_assistant_message",
            lambda data: data.setdefault("transcript", []).append(assistant),
            {"role": "assistant", "provider_id": response.provider_id, "model_id": response.model_id},
        )
        details = {
            "text": text,
            "assistant_text": str(response.text),
            "provider_id": str(response.provider_id),
            "model_id": str(response.model_id),
            "quota_remaining": response.quota_remaining,
            "metadata": deepcopy(response.metadata),
        }
        return self._receipt("send_message", True, details)

    def start_goal(self, objective: str, criteria: list[str]) -> GoalContract:
        goal = self.goals.create_goal(objective, criteria)
        self._mutate(
            "desktop_goal_selected",
            lambda data: data.__setitem__("active_goal_id", goal.goal_id),
            {"goal_id": goal.goal_id},
        )
        self._receipt("start_goal", True, {"goal_id": goal.goal_id, "objective": objective})
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
        return self._receipt("write_text", True, details)

    def diff(self) -> str:
        value = self.git.diff(self.workspace)
        self._receipt("view_diff", True, {"bytes": len(value.encode())})
        return value

    def run_tests(self, argv: Sequence[str]) -> dict[str, Any]:
        process = self.runner.run(argv, timeout_seconds=120, cwd=str(self.workspace))
        details = {
            "argv": list(process.argv),
            "returncode": process.returncode,
            "timed_out": process.timed_out,
            "stdout": process.stdout[-4000:],
            "stderr": process.stderr[-4000:],
        }
        return self._receipt("run_tests", process.returncode == 0 and not process.timed_out, details)

    def verify_goal_criterion(self, goal_id: str, criterion_id: str, evidence: dict[str, Any]) -> GoalContract:
        goal = self.goals.verify_criterion(goal_id, criterion_id, evidence)
        self._receipt(
            "verify_goal_criterion",
            True,
            {"goal_id": goal_id, "criterion_id": criterion_id},
        )
        return goal

    def complete_goal(self, goal_id: str) -> GoalContract:
        goal = self.goals.complete(goal_id)
        self._receipt("complete_goal", True, {"goal_id": goal_id})
        return goal

    def commit_main(self, message: str) -> dict[str, Any]:
        result = self.git.commit_all(self.workspace, message)
        self._receipt("commit_main", bool(result.get("ok")), result)
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
