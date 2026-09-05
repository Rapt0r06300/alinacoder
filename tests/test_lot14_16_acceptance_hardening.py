from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from alinacoder.desktop.workbench import DesktopWorkbench
from alinacoder.product.installer import install, repair
from alinacoder.supabase.core import MigrationContract, SupabaseMirror


class GitFixtureMixin:
    def make_repo(self, root: Path) -> Path:
        repo = root / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "alinacoder@example.invalid"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "AlinaCoder Acceptance"], cwd=repo, check=True)
        (repo / "README.md").write_text("# Fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-m", "fixture baseline"], cwd=repo, check=True, capture_output=True, text=True)
        return repo


class Lot14IntegratedWorkbenchTests(GitFixtureMixin, unittest.TestCase):
    def test_conversation_goal_diff_tests_commit_and_restart_use_canonical_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = self.make_repo(root)
            state_path = root / "state.sqlite"
            workbench = DesktopWorkbench(repo, state_path=state_path, session_id="desktop-e2e")
            try:
                project = workbench.open_project()
                self.assertEqual(project["branch"], "main")
                workbench.send_message("/goal Add a verified acceptance marker")
                goal = workbench.start_goal(
                    "Add a verified acceptance marker",
                    ["artifact written", "tests pass", "main branch ready"],
                )
                workbench.write_text("acceptance.txt", "ALINACODER_ACCEPTANCE=PASS\n")
                self.assertIn("acceptance.txt", workbench.diff())
                test_receipt = workbench.run_tests(["git", "diff", "--check"])
                self.assertTrue(test_receipt["ok"])
                workbench.verify_goal_criterion(goal.goal_id, "c1", {"path": "acceptance.txt"})
                workbench.verify_goal_criterion(goal.goal_id, "c2", {"test": test_receipt})
                workbench.verify_goal_criterion(goal.goal_id, "c3", {"branch": "main"})
                self.assertEqual(workbench.complete_goal(goal.goal_id).status.value, "COMPLETE")
                committed = workbench.commit_main("acceptance: prove desktop workbench e2e")
                self.assertTrue(committed["ok"])
                self.assertEqual(committed["branch"], "main")
                self.assertFalse(workbench.status()["dirty"])
            finally:
                workbench.close()

            restarted = DesktopWorkbench(repo, state_path=state_path, session_id="desktop-e2e")
            try:
                snapshot = restarted.snapshot()
                self.assertEqual(snapshot["project"]["path"], str(repo.resolve()))
                self.assertEqual(snapshot["active_goal_id"], goal.goal_id)
                self.assertGreaterEqual(len(snapshot["receipts"]), 4)
            finally:
                restarted.close()

    def test_pause_resume_stop_takeover_are_canonical_and_survive_restart(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = self.make_repo(root)
            state_path = root / "state.sqlite"
            workbench = DesktopWorkbench(repo, state_path=state_path, session_id="controls")
            try:
                workbench.pause()
                self.assertEqual(workbench.snapshot()["control_state"], "PAUSED")
            finally:
                workbench.close()
            restarted = DesktopWorkbench(repo, state_path=state_path, session_id="controls")
            try:
                self.assertEqual(restarted.snapshot()["control_state"], "PAUSED")
                restarted.resume()
                restarted.takeover()
                self.assertEqual(restarted.snapshot()["control_state"], "USER_TAKEOVER")
                restarted.stop()
                self.assertEqual(restarted.snapshot()["control_state"], "STOPPED")
            finally:
                restarted.close()


class Lot15MigrationContractTests(unittest.TestCase):
    def test_optional_mirror_has_versioned_up_and_down_contracts(self) -> None:
        root = Path(__file__).parents[1]
        contract = MigrationContract(root / "supabase" / "migrations")
        report = contract.validate()
        self.assertTrue(report["valid"])
        self.assertIn("0001_optional_mirror.sql", report["up"])
        self.assertIn("0001_optional_mirror.down.sql", report["down"])
        self.assertTrue(report["rls_authenticated"])
        self.assertTrue(report["pgmq_idempotency_warning"])

    def test_supabase_outage_never_changes_canonical_mode(self) -> None:
        mirror = SupabaseMirror(True, "project", "tenant")
        self.assertEqual(mirror.mode, "MIRROR")
        mirror.mark_unhealthy("network")
        self.assertEqual(mirror.mode, "LOCAL_ONLY")
        self.assertEqual(mirror.write_non_secret({"kind": "memory", "secret": False}), "LOCAL_ONLY")


class Lot16InstallerLifecycleTests(unittest.TestCase):
    def test_repair_replaces_binary_but_preserves_user_data(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            install_dir = root / "AlinaCoder"
            v1 = root / "v1.exe"
            v2 = root / "v2.exe"
            v1.write_bytes(b"v1")
            v2.write_bytes(b"v2")
            install(install_dir, source_exe=v1)
            (install_dir / "user-state.json").write_text('{"keep":true}', encoding="utf-8")
            repair(install_dir, source_exe=v2)
            self.assertEqual((install_dir / "AlinaCoder.exe").read_bytes(), b"v2")
            self.assertTrue((install_dir / "user-state.json").exists())
            metadata = json.loads((install_dir / "install.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["last_operation"], "repair")
            self.assertTrue(metadata["preserve_user_data_on_uninstall"])


if __name__ == "__main__":
    unittest.main()
