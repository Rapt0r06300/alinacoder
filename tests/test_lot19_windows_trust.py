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

    def test_product_adapter_is_bound_to_native_wintrust(self) -> None:
        self.assertEqual(self.adapter.__class__.__module__, "alinacoder.product.windows_trust")
        self.assertEqual(self.adapter.__class__.__name__, "NativeWindowsBootstrapAdapter")

    def test_unsigned_fake_executable_is_rejected(self) -> None:
        unsigned = Path(self.temp.name) / "unsigned.exe"
        unsigned.write_bytes(b"MZ" + b"not-a-signed-pe")
        self.assertFalse(self.adapter.verify_authenticode(unsigned))


if __name__ == "__main__":
    unittest.main()
