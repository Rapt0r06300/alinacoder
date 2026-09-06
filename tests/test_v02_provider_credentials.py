from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from alinacoder.desktop.app import product_capabilities
from alinacoder.intelligence_mesh.credentials import ProviderCredentialVault


class ReversibleProtector:
    def protect(self, plaintext: bytes) -> bytes:
        return b"vault:" + plaintext[::-1]

    def unprotect(self, ciphertext: bytes) -> bytes:
        if not ciphertext.startswith(b"vault:"):
            raise ValueError("bad ciphertext")
        return ciphertext[len(b"vault:"):][::-1]


class ProviderCredentialVaultTests(unittest.TestCase):
    def test_vault_persists_ciphertext_only_and_round_trips_secret(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "provider-credentials.json"
            vault = ProviderCredentialVault(path, protector=ReversibleProtector())
            vault.put("groq", "super-secret-key")

            raw = path.read_text(encoding="utf-8")
            self.assertNotIn("super-secret-key", raw)
            self.assertEqual(vault.get("groq"), "super-secret-key")
            self.assertEqual(vault.providers(), ("groq",))

    def test_delete_removes_secret_and_unknown_provider_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "provider-credentials.json"
            vault = ProviderCredentialVault(path, protector=ReversibleProtector())
            self.assertIsNone(vault.get("missing"))
            vault.put("gemini", "key")
            self.assertTrue(vault.has("gemini"))
            vault.delete("gemini")
            self.assertFalse(vault.has("gemini"))
            self.assertIsNone(vault.get("gemini"))
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["providers"], {})

    def test_desktop_product_explicitly_exposes_no_terminal_provider_settings(self) -> None:
        capabilities = product_capabilities()
        self.assertIn("secure_provider_credentials", capabilities)
        self.assertIn("provider_settings_ui", capabilities)
        self.assertIn("real_zero_cost_provider_fabric", capabilities)


if __name__ == "__main__":
    unittest.main()
