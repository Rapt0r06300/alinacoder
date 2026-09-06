from __future__ import annotations

import unittest

from alinacoder.intelligence_mesh.provider_atlas import (
    ProviderSafetyClass,
    normative_provider_atlas,
)


EXPECTED_ACTIVE_PROVIDER_IDS = {
    "kilo_gateway",
    "zai",
    "sambanova",
    "groq",
    "cloudflare_workers_ai",
    "openrouter",
    "gemini",
    "mistral",
    "huggingface",
    "tencent_hunyuan",
    "alibaba_model_studio",
    "siliconflow",
    "scaleway",
    "ollama_local",
    "ollama_cloud",
    "nvidia_nim",
    "cerebras",
    "opencode_zen",
}


class ProviderAtlasTests(unittest.TestCase):
    def test_normative_atlas_contains_every_approved_provider_and_tombstones_github_models(self) -> None:
        atlas = normative_provider_atlas()
        entries = {entry.provider_id: entry for entry in atlas.entries()}

        self.assertTrue(EXPECTED_ACTIVE_PROVIDER_IDS.issubset(entries))
        self.assertIn("github_models", entries)
        self.assertTrue(entries["github_models"].retired)
        self.assertEqual(entries["github_models"].lifecycle_state, "TOMBSTONED")

    def test_every_remote_candidate_is_fail_closed_and_has_safety_metadata(self) -> None:
        atlas = normative_provider_atlas()
        for entry in atlas.entries():
            if entry.provider_id in {"ollama_local", "github_models"}:
                continue
            self.assertTrue(entry.https_only)
            self.assertTrue(entry.zero_cost_requalification_required)
            self.assertTrue(entry.safe_classes)
            self.assertTrue(all(isinstance(item, ProviderSafetyClass) for item in entry.safe_classes))

    def test_local_ollama_is_zero_api_billing_fallback(self) -> None:
        entry = normative_provider_atlas().get("ollama_local")
        self.assertFalse(entry.retired)
        self.assertEqual(entry.protocol, "ollama")
        self.assertIn(ProviderSafetyClass.LOCAL_NO_API_BILLING, entry.safe_classes)
        self.assertFalse(entry.account_proof_required)

    def test_trial_or_payment_gated_candidates_are_not_auto_admitted(self) -> None:
        atlas = normative_provider_atlas()
        guarded = {
            "huggingface",
            "scaleway",
            "nvidia_nim",
            "cerebras",
            "ollama_cloud",
            "opencode_zen",
        }
        for provider_id in guarded:
            entry = atlas.get(provider_id)
            self.assertTrue(entry.account_proof_required)
            self.assertFalse(entry.structurally_auto_admissible)


if __name__ == "__main__":
    unittest.main()
