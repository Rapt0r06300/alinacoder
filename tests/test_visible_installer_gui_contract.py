from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from alinacoder.product.setup_events import SetupEvent


class VisibleInstallerGuiContractTests(unittest.TestCase):
    def test_default_double_click_selects_gui_and_quiet_stays_cli(self) -> None:
        from alinacoder.product.setup_gui import select_setup_mode

        self.assertEqual(select_setup_mode([]), "gui")
        self.assertEqual(select_setup_mode(["--quiet"]), "cli")
        self.assertEqual(select_setup_mode(["--repair", "--quiet"]), "cli")
        self.assertEqual(select_setup_mode(["--installer-ui-smoke"]), "smoke")

    def test_view_model_keeps_error_visible_and_exposes_recovery_actions(self) -> None:
        from alinacoder.product.setup_gui import SetupViewModel

        view = SetupViewModel()
        view.apply_event(SetupEvent("ollama", "start", "Installation d'Ollama"))
        view.apply_event(SetupEvent("download", "progress", "Téléchargement Ollama", current=50, total=100))
        view.mark_error("Réseau indisponible", "TimeoutError: timed out")

        self.assertEqual(view.state, "error")
        self.assertEqual(view.progress_percent, 50)
        self.assertIn("Réessayer", view.actions)
        self.assertIn("Copier le diagnostic", view.actions)
        self.assertIn("Ouvrir les logs", view.actions)
        self.assertIn("TimeoutError", view.diagnostics)

    def test_success_exposes_launch_and_all_human_phases(self) -> None:
        from alinacoder.product.setup_gui import PHASES, SetupViewModel

        keys = [key for key, _label in PHASES]
        self.assertEqual(keys, ["preparation", "analyse", "git", "ollama", "model", "validation", "alinacoder", "integration", "complete"])
        view = SetupViewModel()
        for key, label in PHASES:
            view.apply_event(SetupEvent(key, "complete", label))
        view.mark_success("qwen3:0.6b")
        self.assertEqual(view.state, "success")
        self.assertIn("Lancer AlinaCoder", view.actions)
        self.assertTrue(all(item.state == "done" for item in view.phases))

    def test_smoke_evidence_proves_persistent_error_and_success_contract(self) -> None:
        from alinacoder.product.setup_gui import run_ui_smoke

        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "evidence.json"
            payload = run_ui_smoke(out, commit_sha="abc123", setup_sha256="f" * 64)
            self.assertTrue(payload["ok"])
            self.assertTrue(payload["visible_installer_e2e"])
            self.assertTrue(payload["no_console_default"])
            self.assertTrue(payload["error_persistent"])
            self.assertTrue(payload["retry_available"])
            self.assertEqual(payload["phase_count"], 9)
            self.assertTrue(out.is_file())


if __name__ == "__main__":
    unittest.main()
