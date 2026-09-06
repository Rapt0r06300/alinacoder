from __future__ import annotations

import unittest

from alinacoder.intelligence_mesh.runtime import build_default_inference_fabric


class FakeVault:
    def __init__(self, values: dict[str, str]) -> None:
        self.values = dict(values)

    def get(self, provider_id: str) -> str | None:
        return self.values.get(provider_id)


class RuntimeBuilderTests(unittest.TestCase):
    def test_hybrid_builds_configured_dynamic_cloud_routes_plus_local_ollama(self) -> None:
        fabric = build_default_inference_fabric(
            FakeVault({"openrouter": "or-key", "kilo_gateway": "kilo-key", "gemini": "gem-key"}),
            mode="hybrid",
        )
        provider_ids = set(fabric.provider_ids())
        self.assertIn("openrouter", provider_ids)
        self.assertIn("kilo_gateway", provider_ids)
        self.assertIn("gemini", provider_ids)
        self.assertIn("ollama_local", provider_ids)
        self.assertNotIn("github_models", provider_ids)

    def test_local_only_never_builds_remote_provider_even_when_keys_exist(self) -> None:
        fabric = build_default_inference_fabric(FakeVault({"openrouter": "or-key"}), mode="local-only")
        self.assertEqual(fabric.provider_ids(), ("ollama_local",))

    def test_free_cloud_does_not_include_local_fallback(self) -> None:
        fabric = build_default_inference_fabric(FakeVault({"openrouter": "or-key"}), mode="free-cloud")
        self.assertIn("openrouter", fabric.provider_ids())
        self.assertNotIn("ollama_local", fabric.provider_ids())

    def test_missing_credentials_skip_remote_candidate_without_blocking_other_routes(self) -> None:
        fabric = build_default_inference_fabric(FakeVault({}), mode="hybrid")
        self.assertEqual(fabric.provider_ids(), ("ollama_local",))


if __name__ == "__main__":
    unittest.main()
