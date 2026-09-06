from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from alinacoder.desktop.workbench import DesktopWorkbench
from alinacoder.intelligence_mesh.providers import ProviderResponse


class FakeFabric:
    def __init__(self, response: ProviderResponse | Exception) -> None:
        self.response = response

    def complete(self, messages, requirement, *, mode):
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class LiveActivityTests(unittest.TestCase):
    def test_activity_is_persisted_with_monotonic_ids_and_safe_details(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            state = Path(td) / "state.sqlite"
            workbench = DesktopWorkbench(Path(td), state_path=state, session_id="activity")
            first = workbench.emit_activity(
                "tool_started",
                "Inspecting repository",
                status="running",
                details={"path": "src", "chain_of_thought": "must never persist"},
            )
            second = workbench.emit_activity(
                "tool_completed",
                "Repository inspected",
                status="success",
                details={"nested": {"raw_reasoning": "private", "files": 3}},
            )
            workbench.close()

            restarted = DesktopWorkbench(Path(td), state_path=state, session_id="activity")
            events = restarted.activity()
            restarted.close()

        self.assertEqual([item["event_id"] for item in events], [first["event_id"], second["event_id"]])
        self.assertEqual(first["event_id"], "activity:1")
        self.assertEqual(second["event_id"], "activity:2")
        self.assertTrue(first["timestamp"].endswith("Z"))
        self.assertNotIn("chain_of_thought", first["details"])
        self.assertNotIn("raw_reasoning", second["details"]["nested"])
        self.assertEqual(events, [first, second])

    def test_successful_inference_emits_required_run_lifecycle_and_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workbench = DesktopWorkbench(
                Path(td),
                state_path=Path(td) / "state.sqlite",
                session_id="success",
                inference_fabric=FakeFabric(ProviderResponse("Bonjour", "openrouter", "model:free", quota_remaining=7)),
                inference_mode="hybrid",
            )
            receipt = workbench.send_message("Salut")
            events = workbench.activity()
            current = workbench.current_run()
            workbench.close()

        kinds = [item["kind"] for item in events]
        self.assertEqual(kinds[-4:], ["run_started", "inference_started", "inference_completed", "run_completed"])
        self.assertEqual(events[-2]["details"]["provider_id"], "openrouter")
        self.assertEqual(events[-2]["details"]["model_id"], "model:free")
        self.assertEqual(current["status"], "completed")
        self.assertEqual(receipt["details"]["assistant_text"], "Bonjour")

    def test_failed_inference_emits_run_failed_and_never_run_completed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workbench = DesktopWorkbench(
                Path(td),
                state_path=Path(td) / "state.sqlite",
                session_id="failure",
                inference_fabric=FakeFabric(RuntimeError("provider unavailable")),
                inference_mode="free-cloud",
            )
            with self.assertRaisesRegex(RuntimeError, "provider unavailable"):
                workbench.send_message("Salut")
            events = workbench.activity()
            current = workbench.current_run()
            workbench.close()

        kinds = [item["kind"] for item in events]
        self.assertIn("run_failed", kinds)
        self.assertNotIn("run_completed", kinds)
        self.assertEqual(current["status"], "failed")
        self.assertIn("provider unavailable", current["error"])

    def test_material_controls_emit_activity(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workbench = DesktopWorkbench(Path(td), state_path=Path(td) / "state.sqlite", session_id="controls")
            workbench.pause()
            workbench.resume()
            workbench.takeover()
            workbench.stop()
            kinds = [item["kind"] for item in workbench.activity()]
            workbench.close()

        self.assertEqual(kinds, ["control_paused", "control_resumed", "control_takeover", "control_stopped"])


if __name__ == "__main__":
    unittest.main()
