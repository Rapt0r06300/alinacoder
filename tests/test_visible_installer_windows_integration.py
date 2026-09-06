from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


class VisibleInstallerWindowsIntegrationTests(unittest.TestCase):
    def test_plan_targets_per_user_shortcuts_and_uninstall_entry(self) -> None:
        from alinacoder.product.windows_integration import build_windows_integration_plan

        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "AlinaCoder"
            setup = Path(td) / "AlinaCoderSetup.exe"
            plan = build_windows_integration_plan(root, setup, appdata=Path(td)/"AppData", userprofile=Path(td)/"User")
            self.assertEqual(plan.app_exe, root / "AlinaCoder.exe")
            self.assertEqual(plan.maintenance_setup, root / "AlinaCoderSetup.exe")
            self.assertTrue(plan.start_menu_shortcut.name.endswith(".lnk"))
            self.assertTrue(plan.desktop_shortcut.name.endswith(".lnk"))
            self.assertIn("Uninstall\\AlinaCoder", plan.uninstall_key.replace("/", "\\"))
            self.assertIn("--uninstall", plan.uninstall_command)
            self.assertIn(str(root), plan.uninstall_command)

    def test_apply_requires_ready_application_before_creating_integration(self) -> None:
        from alinacoder.product.windows_integration import install_windows_integration

        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "AlinaCoder"
            setup = Path(td) / "AlinaCoderSetup.exe"
            setup.write_bytes(b"setup")
            with self.assertRaises(FileNotFoundError):
                install_windows_integration(root, setup, create_shortcuts=False, register_uninstall=False)

    def test_maintenance_setup_is_copied_only_after_app_exists(self) -> None:
        from alinacoder.product.windows_integration import install_windows_integration

        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "AlinaCoder"
            root.mkdir(parents=True)
            (root / "AlinaCoder.exe").write_bytes(b"app")
            setup = Path(td) / "AlinaCoderSetup.exe"
            setup.write_bytes(b"setup")
            result = install_windows_integration(root, setup, create_shortcuts=False, register_uninstall=False)
            self.assertTrue((root / "AlinaCoderSetup.exe").is_file())
            self.assertEqual(result.maintenance_setup, root / "AlinaCoderSetup.exe")


if __name__ == "__main__":
    unittest.main()
