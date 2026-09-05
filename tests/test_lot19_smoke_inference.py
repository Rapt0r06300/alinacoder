from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product.prerequisites import PrerequisiteManifest
from alinacoder.product.windows_trust import NativeWindowsBootstrapAdapter


class Lot19SmokeInferenceTests(unittest.TestCase):
    def test_qwen_smoke_disables_default_thinking_and_reserves_answer_tokens(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")

        with tempfile.TemporaryDirectory() as td:
            adapter = NativeWindowsBootstrapAdapter(Path(td), manifest)
            with patch("alinacoder.product.prerequisites._json_bytes", return_value={"response": "OK"}) as request:
                response = adapter.smoke_model("http://127.0.0.1:11434", "qwen3:0.6b")

        self.assertEqual(response, "OK")
        payload = request.call_args.args[1]
        self.assertIs(payload["think"], False)
        self.assertIs(payload["stream"], False)
        self.assertGreaterEqual(payload["options"]["num_predict"], 16)


if __name__ == "__main__":
    unittest.main()
