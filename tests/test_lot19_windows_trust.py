from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from alinacoder.product.prerequisites import PrerequisiteManifest, WindowsBootstrapAdapter


@unittest.skipUnless(os.name == "nt", "Windows trust verification only applies on Windows")
class Lot19WindowsTrustTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.manifest = PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.adapter = WindowsBootstrapAdapter(Path(self.temp.name), self.manifest)

    def test_signed_windows_system_binary_is_trusted(self) -> None:
        signed = Path(os.environ["WINDIR"]) / "System32" / "notepad.exe"
        self.assertTrue(signed.exists())
        self.assertTrue(self.adapter.verify_authenticode(signed))

    def test_unsigned_fake_executable_is_rejected(self) -> None:
        unsigned = Path(self.temp.name) / "unsigned.exe"
        unsigned.write_bytes(b"MZ" + b"not-a-signed-pe")
        self.assertFalse(self.adapter.verify_authenticode(unsigned))


if __name__ == "__main__":
    unittest.main()
