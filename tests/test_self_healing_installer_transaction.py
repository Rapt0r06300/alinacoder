from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product import installer
from alinacoder.product.prerequisites import BootstrapError, BootstrapReport


class _Bootstrapper:
    def __init__(self, report: BootstrapReport) -> None:
        self.adapter = object()
        self._report = report

    def run(self, *, online: bool, model_override: str | None = None) -> BootstrapReport:
        return self._report


class SelfHealingInstallerTransactionTests(unittest.TestCase):
    @staticmethod
    def _write(path: Path, payload: bytes) -> Path:
        path.write_bytes(payload)
        return path

    def test_bootstrap_failure_never_replaces_previous_healthy_binary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = self._write(root / "source.exe", b"NEW-VERSION")
            target = self._write(root / "AlinaCoder.exe", b"LAST-HEALTHY")
            bootstrapper = _Bootstrapper(BootstrapReport(False, "qwen", (), ("model_pull",), None))

            with self.assertRaises(BootstrapError):
                installer.install(root, source_exe=source, bootstrapper=bootstrapper)

            self.assertEqual(target.read_bytes(), b"LAST-HEALTHY")

    def test_copy_failure_can_only_damage_staging_not_active_target(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = self._write(root / "source.exe", b"NEW-VERSION")
            target = self._write(root / "AlinaCoder.exe", b"LAST-HEALTHY")
            real_copy2 = installer.shutil.copy2

            def fail_after_partial_copy(src, dst, *args, **kwargs):
                destination = Path(dst)
                destination.write_bytes(b"PARTIAL")
                raise OSError("simulated interrupted application copy")

            with patch.object(installer.shutil, "copy2", side_effect=fail_after_partial_copy):
                with self.assertRaises(OSError):
                    installer.install(root, source_exe=source, bootstrapper=None)

            self.assertEqual(target.read_bytes(), b"LAST-HEALTHY")
            self.assertTrue((root / "AlinaCoder.exe.staging").exists())
            self.assertEqual(real_copy2, installer.shutil.copy2.__wrapped__ if hasattr(installer.shutil.copy2, "__wrapped__") else real_copy2)

    def test_failure_after_promotion_restores_previous_binary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = self._write(root / "source.exe", b"NEW-VERSION")
            target = self._write(root / "AlinaCoder.exe", b"LAST-HEALTHY")
            bootstrapper = _Bootstrapper(BootstrapReport(True, "qwen", (), (), None))

            with patch.object(installer, "_write_metadata", side_effect=OSError("metadata disk failure")):
                with self.assertRaises(OSError):
                    installer.install(root, source_exe=source, bootstrapper=bootstrapper)

            self.assertEqual(target.read_bytes(), b"LAST-HEALTHY")

    def test_success_promotes_verified_binary_and_cleans_backup(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = self._write(root / "source.exe", b"NEW-VERSION")
            target = self._write(root / "AlinaCoder.exe", b"LAST-HEALTHY")
            bootstrapper = _Bootstrapper(BootstrapReport(True, "qwen", (), (), None))

            installed = installer.install(root, source_exe=source, bootstrapper=bootstrapper)

            self.assertEqual(installed, target)
            self.assertEqual(target.read_bytes(), b"NEW-VERSION")
            self.assertFalse((root / "AlinaCoder.exe.staging").exists())
            self.assertFalse((root / "AlinaCoder.exe.backup").exists())
            self.assertTrue((root / "install.json").is_file())


if __name__ == "__main__":
    unittest.main()
