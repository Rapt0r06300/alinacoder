from __future__ import annotations

import json
import unittest
from unittest.mock import MagicMock, patch

from scripts.verify_lot19_bootstrap import post_generate


class Lot19IndependentVerifierTests(unittest.TestCase):
    def test_real_inference_probe_disables_thinking_and_reserves_answer_tokens(self) -> None:
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"response":"OK","done":true}'

        with patch("scripts.verify_lot19_bootstrap.urllib.request.urlopen", return_value=response) as urlopen:
            result = post_generate("http://127.0.0.1:11434", "qwen3:0.6b")

        self.assertTrue(result["done"])
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertIs(payload["think"], False)
        self.assertIs(payload["stream"], False)
        self.assertGreaterEqual(payload["options"]["num_predict"], 16)


if __name__ == "__main__":
    unittest.main()
