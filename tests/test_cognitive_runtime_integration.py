from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest

from alinacoder.desktop.workbench import DesktopWorkbench


class _Fabric:
    def __init__(self) -> None:
        self.calls = []
        self.verified = []

    def complete(self, messages, requirement, *, mode):
        self.calls.append((messages, requirement, mode))
        return SimpleNamespace(
            text="ok",
            provider_id="kilo_gateway",
            model_id="free-model:free",
            quota_remaining=12,
            metadata={
                "task_class": "debug",
                "route_reason": "best verified debug LCB among available admissible routes",
                "zero_cost_verdict": "PROVEN_ZERO_COST",
                "billing_class": "ZERO_PRICE_MODEL",
                "quality_lcb": 0.72,
            },
        )

    def observe_verified_outcome(self, **payload):
        self.verified.append(dict(payload))


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True)
    return completed.stdout.strip()


def _repo(root: Path) -> None:
    _git(root, "init", "-b", "main")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "Test")
    (root / "a.txt").write_text("one\n", encoding="utf-8")
    (root / "b.txt").write_text("two\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "baseline")


class CognitiveRuntimeIntegrationTests(unittest.TestCase):
    def test_begin_message_compiles_intent_updates_cognitive_state_and_emits_trace(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fabric = _Fabric()
            with DesktopWorkbench(root, state_path=root / "state.sqlite", inference_fabric=fabric, inference_mode="hybrid") as wb:
                request = wb.begin_message("Non, je parle du model bridge. Continue sans t'arrêter.")
                snapshot = wb.snapshot()
                cognitive = snapshot.get("cognitive", {})
                self.assertEqual(cognitive.get("intent_revision"), 1)
                self.assertIn("model bridge", cognitive.get("active_requirements", [""])[-1])
                self.assertTrue(request.get("intent", {}).get("correction"))
                self.assertTrue(request.get("intent", {}).get("continuation"))
                self.assertIn("intent_updated", [event["kind"] for event in wb.activity()])

    def test_user_correction_stales_prior_intent_dependencies_but_preserves_unrelated_fact(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fabric = _Fabric()
            with DesktopWorkbench(root, state_path=root / "state.sqlite", inference_fabric=fabric, inference_mode="hybrid") as wb:
                wb.begin_message("Répare l'installer")
                first = wb.snapshot()["cognitive"]
                prior_node = first["active_intent_node"]
                wb.record_cognitive_dependency("plan:installer", "plan", depends_on=(prior_node,))
                wb.record_cognitive_dependency("fact:provider-atlas", "fact")
                wb.begin_message("Non, je parle du model bridge")
                deps = wb.cognitive_dependencies()
                self.assertEqual(deps[prior_node]["status"], "STALE")
                self.assertEqual(deps["plan:installer"]["status"], "STALE")
                self.assertEqual(deps["fact:provider-atlas"]["status"], "ACTIVE")

    def test_workspace_write_invalidates_only_changed_path_observation_in_execution_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _repo(root)
            with DesktopWorkbench(root, state_path=root / "state.sqlite") as wb:
                wb.open_project()
                obs_a = wb.observe_path("a.txt")
                obs_b = wb.observe_path("b.txt")
                wb.write_text("a.txt", "changed\n")
                self.assertFalse(wb.execution_ledger.get_observation(obs_a).valid)
                self.assertTrue(wb.execution_ledger.get_observation(obs_b).valid)
                summary = wb.execution_ledger.inform(wb.repo_state_fingerprint())
                self.assertGreaterEqual(summary.valid_observation_count, 1)

    def test_test_execution_records_verification_command_and_can_train_route_only_from_execution_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _repo(root)
            fabric = _Fabric()
            with DesktopWorkbench(root, state_path=root / "state.sqlite", inference_fabric=fabric, inference_mode="hybrid") as wb:
                wb.open_project()
                wb.send_message("debug the repository")
                receipt = wb.run_tests(["git", "diff", "--check"])
                self.assertTrue(receipt["ok"])
                summary = wb.execution_ledger.inform(wb.repo_state_fingerprint())
                self.assertIn("git", " ".join(summary.recent_commands))
                self.assertEqual(len(fabric.verified), 1)
                self.assertTrue(fabric.verified[0]["success"])
                self.assertEqual(fabric.verified[0]["provider_id"], "kilo_gateway")
                self.assertEqual(fabric.verified[0]["task_class"], "debug")

    def test_cognitive_and_execution_state_survive_restart(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _repo(root)
            state = root / "state.sqlite"
            fabric = _Fabric()
            wb = DesktopWorkbench(root, state_path=state, inference_fabric=fabric, inference_mode="hybrid")
            wb.open_project()
            wb.begin_message("Fix the parser bug")
            observation = wb.observe_path("a.txt")
            wb.close()

            restarted = DesktopWorkbench(root, state_path=state, inference_fabric=fabric, inference_mode="hybrid")
            try:
                self.assertEqual(restarted.snapshot()["cognitive"]["intent_revision"], 1)
                self.assertTrue(restarted.execution_ledger.get_observation(observation).valid)
            finally:
                restarted.close()


if __name__ == "__main__":
    unittest.main()
