from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product import installer
from alinacoder.product.setup_controller import SetupController


class SelfHealingEntrypointTests(unittest.TestCase):
    def test_visible_setup_delegates_to_self_healing_runner(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "AlinaCoder.exe"
            target.write_bytes(b"app")
            controller = SetupController(root)
            calls = []

            def fake_runner(install_dir, **kwargs):
                calls.append((Path(install_dir), kwargs))
                factory = kwargs["bootstrapper_factory"]
                bootstrapper = factory()
                self.assertIsNotNone(getattr(bootstrapper, "adapter", None))
                return target

            with patch.object(installer, "run_self_healing_operation", side_effect=fake_runner), patch.object(
                installer, "install", side_effect=AssertionError("visible setup bypassed self-healing runner")
            ), patch.object(
                installer, "upgrade", side_effect=AssertionError("visible setup bypassed self-healing runner")
            ):
                snapshot = controller.run_install("qwen3:0.6b")

            self.assertEqual(snapshot.state, "success")
            self.assertTrue(snapshot.can_launch)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][0], root)
            self.assertEqual(calls[0][1]["operation"], "upgrade")
            self.assertEqual(calls[0][1]["model"], "qwen3:0.6b")
            self.assertIs(calls[0][1]["event_sink"], controller._sink)
            self.assertIs(calls[0][1]["cancellation_token"], controller.cancellation_token)

    def test_cli_repair_uses_self_healing_runner(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "AlinaCoder.exe"
            target.write_bytes(b"app")
            calls = []

            def fake_runner(install_dir, **kwargs):
                calls.append((Path(install_dir), kwargs))
                return target

            with patch.object(installer, "run_self_healing_operation", side_effect=fake_runner), patch.object(
                installer, "repair", side_effect=AssertionError("CLI repair bypassed self-healing runner")
            ):
                code = installer.main(["--quiet", "--repair", "--install-dir", str(root), "--model", "qwen3:0.6b"])

            self.assertEqual(code, 0)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1]["operation"], "repair")
            self.assertEqual(calls[0][1]["model"], "qwen3:0.6b")

    def test_cli_upgrade_uses_self_healing_runner(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "AlinaCoder.exe"
            target.write_bytes(b"old")
            calls = []

            def fake_runner(install_dir, **kwargs):
                calls.append((Path(install_dir), kwargs))
                return target

            with patch.object(installer, "run_self_healing_operation", side_effect=fake_runner), patch.object(
                installer, "upgrade", side_effect=AssertionError("CLI upgrade bypassed self-healing runner")
            ):
                code = installer.main(["--quiet", "--upgrade", "--install-dir", str(root)])

            self.assertEqual(code, 0)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1]["operation"], "upgrade")

    def test_cli_default_install_uses_self_healing_runner(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "AlinaCoder.exe"
            calls = []

            def fake_runner(install_dir, **kwargs):
                calls.append((Path(install_dir), kwargs))
                target.write_bytes(b"new")
                return target

            with patch.object(installer, "run_self_healing_operation", side_effect=fake_runner), patch.object(
                installer, "install", side_effect=AssertionError("CLI install bypassed self-healing runner")
            ):
                code = installer.main(["--quiet", "--install-dir", str(root)])

            self.assertEqual(code, 0)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1]["operation"], "install")


if __name__ == "__main__":
    unittest.main()
