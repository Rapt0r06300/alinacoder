from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from alinacoder.desktop.workbench import DesktopWorkbench


class _TraceFabric:
    def complete(self, messages, requirement, *, mode):
        return SimpleNamespace(
            text="fixed",
            provider_id="kilo_gateway",
            model_id="example/free:free",
            quota_remaining=42,
            metadata={
                "task_class": "debug",
                "route_reason": "best verified debugging LCB among available zero-cost routes",
                "zero_cost_verdict": "PROVEN_ZERO_COST",
                "billing_class": "ZERO_PRICE_MODEL",
                "chain_of_thought": "must never persist",
            },
        )


class CognitiveDesktopTraceTests(unittest.TestCase):
    def test_completed_run_exposes_safe_task_route_and_zero_cost_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with DesktopWorkbench(
                root,
                state_path=root / "state.sqlite",
                inference_fabric=_TraceFabric(),
                inference_mode="hybrid",
            ) as workbench:
                workbench.send_message("fix the parser traceback")
                run = workbench.current_run()
                self.assertIsNotNone(run)
                self.assertEqual(run["task_class"], "debug")
                self.assertEqual(run["zero_cost_verdict"], "PROVEN_ZERO_COST")
                self.assertIn("debugging LCB", run["route_reason"])
                serialized = str(workbench.snapshot())
                self.assertNotIn("must never persist", serialized)
                route_events = [event for event in workbench.activity() if event["kind"] == "route_selected"]
                self.assertEqual(len(route_events), 1)
                self.assertEqual(route_events[0]["details"]["provider_id"], "kilo_gateway")
                self.assertEqual(route_events[0]["details"]["task_class"], "debug")


if __name__ == "__main__":
    unittest.main()
