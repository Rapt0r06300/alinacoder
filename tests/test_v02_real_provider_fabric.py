from __future__ import annotations

import json
import unittest

from alinacoder.intelligence_mesh.provider_atlas import (
    ProviderSafetyClass,
    normative_provider_atlas,
)
from alinacoder.intelligence_mesh.providers import (
    GeminiProvider,
    HttpResult,
    OllamaProvider,
    OpenAICompatibleProvider,
    ProviderError,
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


class QueueTransport:
    def __init__(self, *results: HttpResult) -> None:
        self.results = list(results)
        self.calls: list[dict[str, object]] = []

    def request(self, method: str, url: str, *, headers: dict[str, str], payload: dict | None, timeout: float) -> HttpResult:
        self.calls.append({"method": method, "url": url, "headers": dict(headers), "payload": payload, "timeout": timeout})
        if not self.results:
            raise AssertionError("unexpected transport call")
        return self.results.pop(0)


def result(status: int, body: dict, headers: dict[str, str] | None = None) -> HttpResult:
    return HttpResult(status=status, headers=headers or {}, body=json.dumps(body).encode("utf-8"))


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


class ProviderAdapterTests(unittest.TestCase):
    def test_openai_discovery_preserves_exact_price_and_completion_parses_quota(self) -> None:
        definition = normative_provider_atlas().get("openrouter")
        transport = QueueTransport(
            result(
                200,
                {
                    "data": [
                        {"id": "strong:free", "pricing": {"prompt": "0", "completion": "0", "request": "0"}, "context_length": 262144},
                        {"id": "paid", "pricing": {"prompt": "0.1", "completion": "0.2", "request": "0"}, "context_length": 131072},
                    ]
                },
            ),
            result(
                200,
                {"choices": [{"message": {"content": "done"}}]},
                {"x-ratelimit-remaining-requests": "17", "x-ratelimit-reset": "42"},
            ),
        )
        provider = OpenAICompatibleProvider(definition, api_key="secret", transport=transport)

        models = provider.discover()
        self.assertEqual([model.model_id for model in models], ["strong:free", "paid"])
        self.assertTrue(models[0].zero_price)
        self.assertFalse(models[1].zero_price)
        self.assertEqual(models[0].context_tokens, 262144)

        response = provider.complete("strong:free", [{"role": "user", "content": "hi"}])
        self.assertEqual(response.text, "done")
        self.assertEqual(response.provider_id, "openrouter")
        self.assertEqual(response.model_id, "strong:free")
        self.assertEqual(response.quota_remaining, 17)
        # The credential must cross the HTTP Authorization boundary, but it must
        # never escape into the persistable provider response/metadata.
        self.assertNotIn("secret", json.dumps({"text": response.text, "metadata": response.metadata}))

    def test_openai_429_is_classified_as_quota_exhaustion(self) -> None:
        definition = normative_provider_atlas().get("groq")
        transport = QueueTransport(result(429, {"error": {"message": "rate limit"}}, {"retry-after": "3"}))
        provider = OpenAICompatibleProvider(definition, api_key="secret", transport=transport)

        with self.assertRaises(ProviderError) as caught:
            provider.complete("model", [{"role": "user", "content": "hi"}])
        self.assertEqual(caught.exception.code, "QUOTA_EXHAUSTED")
        self.assertTrue(caught.exception.retryable)
        self.assertEqual(caught.exception.metadata.get("retry_after"), "3")

    def test_gemini_adapter_parses_native_response_and_quota_error(self) -> None:
        definition = normative_provider_atlas().get("gemini")
        success = QueueTransport(result(200, {"candidates": [{"content": {"parts": [{"text": "gemini answer"}]}}]}))
        provider = GeminiProvider(definition, api_key="g-key", transport=success)
        response = provider.complete("gemini-flash", [{"role": "user", "content": "hello"}])
        self.assertEqual(response.text, "gemini answer")
        self.assertEqual(response.provider_id, "gemini")

        limited = GeminiProvider(definition, api_key="g-key", transport=QueueTransport(result(429, {"error": {"message": "quota"}})))
        with self.assertRaises(ProviderError) as caught:
            limited.complete("gemini-flash", [{"role": "user", "content": "hello"}])
        self.assertEqual(caught.exception.code, "QUOTA_EXHAUSTED")

    def test_ollama_adapter_discovers_local_models_and_completes_chat(self) -> None:
        definition = normative_provider_atlas().get("ollama_local")
        transport = QueueTransport(
            result(200, {"models": [{"name": "qwen3:4b", "size": 2500000000}]}),
            result(200, {"message": {"role": "assistant", "content": "local answer"}}),
        )
        provider = OllamaProvider(definition, transport=transport)
        models = provider.discover()
        self.assertEqual(models[0].model_id, "qwen3:4b")
        self.assertTrue(models[0].zero_price)
        response = provider.complete("qwen3:4b", [{"role": "user", "content": "hello"}])
        self.assertEqual(response.text, "local answer")
        self.assertEqual(response.provider_id, "ollama_local")


if __name__ == "__main__":
    unittest.main()
