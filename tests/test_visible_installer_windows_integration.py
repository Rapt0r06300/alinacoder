from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


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

    def test_interrupted_maintenance_copy_never_corrupts_previous_setup(self) -> None:
        from alinacoder.product import windows_integration as integration

        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "AlinaCoder"
            root.mkdir(parents=True)
            (root / "AlinaCoder.exe").write_bytes(b"app")
            maintenance = root / "AlinaCoderSetup.exe"
            maintenance.write_bytes(b"LAST-HEALTHY-SETUP")
            source = Path(td) / "new-setup.exe"
            source.write_bytes(b"NEW-SETUP")

            def interrupted_copy(src, dst, *args, **kwargs):
                Path(dst).write_bytes(b"PARTIAL")
                raise OSError("simulated interrupted maintenance copy")

            with patch.object(integration.shutil, "copy2", side_effect=interrupted_copy):
                with self.assertRaises(OSError):
                    integration.install_windows_integration(
                        root,
                        source,
                        create_shortcuts=False,
                        register_uninstall=False,
                        retry_attempts=1,
                        sleep=lambda _: None,
                    )

            self.assertEqual(maintenance.read_bytes(), b"LAST-HEALTHY-SETUP")

    def test_transient_shortcut_failure_is_repaired_automatically(self) -> None:
        from alinacoder.product import windows_integration as integration

        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "AlinaCoder"
            root.mkdir(parents=True)
            (root / "AlinaCoder.exe").write_bytes(b"app")
            source = Path(td) / "setup.exe"
            source.write_bytes(b"setup")
            calls = 0

            def flaky_shortcut(path: Path, target: Path, working_dir: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise OSError("temporary shell integration failure")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"shortcut")

            with patch.object(integration.os, "name", "nt"), patch.object(
                integration,
                "_create_shortcut",
                side_effect=flaky_shortcut,
            ):
                plan = integration.install_windows_integration(
                    root,
                    source,
                    create_desktop_shortcut=False,
                    register_uninstall=False,
                    retry_attempts=3,
                    sleep=lambda _: None,
                )

            self.assertEqual(calls, 2)
            self.assertTrue(plan.start_menu_shortcut.is_file())


if __name__ == "__main__":
    unittest.main()
