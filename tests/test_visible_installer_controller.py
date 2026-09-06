from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from alinacoder.product.setup_events import SetupCancelled, SetupEvent


class VisibleInstallerControllerTests(unittest.TestCase):
    def test_success_keeps_ordered_state_and_enables_launch(self) -> None:
        from alinacoder.product.setup_controller import SetupController

        events: list[SetupEvent] = []
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "AlinaCoder.exe"

            def operation(model, event_sink, cancellation_token):
                event_sink(SetupEvent("analyse", "complete", "PC analysé"))
                event_sink(SetupEvent("model", "complete", "Modèle prêt"))
                target.write_bytes(b"app")
                return target, "qwen3:0.6b"

            controller = SetupController(root, operation=operation, event_sink=events.append)
            snapshot = controller.run_install()
            self.assertEqual(snapshot.state, "success")
            self.assertTrue(snapshot.can_launch)
            self.assertFalse(snapshot.can_retry)
            self.assertEqual(snapshot.selected_model, "qwen3:0.6b")
            self.assertTrue(any(e.phase == "preparation" for e in events))
            self.assertTrue(controller.log_path.exists())

    def test_error_stays_available_and_retry_reuses_install_state(self) -> None:
        from alinacoder.product.setup_controller import SetupController

        attempts = 0
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)

            def operation(model, event_sink, cancellation_token):
                nonlocal attempts
                attempts += 1
                if attempts == 1:
                    raise RuntimeError("ollama download failed: network unavailable")
                target = root / "AlinaCoder.exe"
                target.write_bytes(b"app")
                return target, "qwen3:0.6b"

            controller = SetupController(root, operation=operation)
            failed = controller.run_install(model="qwen3:0.6b")
            self.assertEqual(failed.state, "error")
            self.assertTrue(failed.can_retry)
            self.assertIn("network unavailable", failed.last_error)
            self.assertTrue(controller.log_path.exists())

            recovered = controller.retry()
            self.assertEqual(recovered.state, "success")
            self.assertEqual(attempts, 2)

    def test_cancelled_state_is_not_success(self) -> None:
        from alinacoder.product.setup_controller import SetupController

        with tempfile.TemporaryDirectory() as td:
            def operation(model, event_sink, cancellation_token):
                raise SetupCancelled("cancelled")

            controller = SetupController(Path(td), operation=operation)
            snapshot = controller.run_install()
            self.assertEqual(snapshot.state, "cancelled")
            self.assertFalse(snapshot.can_launch)
            self.assertTrue(snapshot.can_retry)


if __name__ == "__main__":
    unittest.main()
