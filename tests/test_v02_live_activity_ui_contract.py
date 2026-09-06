from __future__ import annotations

import inspect
import unittest
from pathlib import Path

from alinacoder.desktop.app import product_capabilities
from alinacoder.desktop.core import WorkbenchModel


class LiveActivityUiContractTests(unittest.TestCase):
    def test_product_declares_live_responsive_safe_activity_capabilities(self) -> None:
        self.assertTrue(
            {
                "live_activity_stream",
                "responsive_agent_workbench",
                "safe_explainable_activity_trace",
            }.issubset(product_capabilities())
        )
        self.assertIn("view_activity", WorkbenchModel().available_actions())

    def test_activity_is_first_secondary_inspector(self) -> None:
        source = Path(inspect.getsourcefile(product_capabilities)).read_text(encoding="utf-8")
        self.assertIn('"Activity"', source)
        self.assertIn('"Plan"', source)
        self.assertLess(source.index('"Activity"'), source.index('"Plan"'))
        self.assertNotIn('"Timeline", "Diagnostics"', source)

    def test_gui_uses_inference_only_background_worker_and_tk_polling(self) -> None:
        source = Path(inspect.getsourcefile(product_capabilities)).read_text(encoding="utf-8")
        self.assertIn("import queue", source)
        self.assertIn("import threading", source)
        self.assertIn("root.after(100, poll_agent_ui)", source)
        self.assertIn("workbench.begin_message(text)", source)
        self.assertIn("workbench.perform_inference(request)", source)
        self.assertIn("workbench.complete_message(run_id, response)", source)
        self.assertIn("workbench.fail_message(run_id, error)", source)
        worker_start = source.index("def inference_worker")
        worker_end = source.index("def poll_agent_ui", worker_start)
        worker = source[worker_start:worker_end]
        self.assertIn("perform_inference", worker)
        self.assertNotIn("complete_message", worker)
        self.assertNotIn("fail_message", worker)
        self.assertNotIn("snapshot(", worker)
        self.assertNotIn("transcript.insert", worker)
        self.assertNotIn("status.set", worker)
        self.assertNotIn("set_view", worker)


if __name__ == "__main__":
    unittest.main()
