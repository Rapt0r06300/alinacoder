from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from alinacoder.intelligence_mesh import CapabilityRequirement
from alinacoder.intelligence_mesh.fabric import InferenceFabric
from alinacoder.intelligence_mesh.provider_atlas import ProviderDefinition, ProviderSafetyClass, normative_provider_atlas
from alinacoder.intelligence_mesh.providers import ProviderError, ProviderModel, ProviderResponse
from alinacoder.intelligence_mesh.qualification import QualificationRegistry, ZeroCostQualification
from alinacoder.intelligence_mesh.models import RouteUnavailableError


NOW = datetime(2026, 9, 6, 13, 0, tzinfo=timezone.utc)


class FakeProvider:
    def __init__(self, definition: ProviderDefinition, models: list[ProviderModel], outcomes: list[object] | None = None) -> None:
        self.definition = definition
        self.models = list(models)
        self.outcomes = list(outcomes or [])
        self.calls: list[tuple[str, list[dict[str, str]]]] = []

    def discover(self) -> list[ProviderModel]:
        return list(self.models)

    def complete(self, model_id: str, messages: list[dict[str, str]]) -> ProviderResponse:
        self.calls.append((model_id, [dict(item) for item in messages]))
        if self.outcomes:
            outcome = self.outcomes.pop(0)
            if isinstance(outcome, BaseException):
                raise outcome
            if isinstance(outcome, ProviderResponse):
                return outcome
        return ProviderResponse(f"answer:{self.definition.provider_id}:{model_id}", self.definition.provider_id, model_id, quota_remaining=5)


def free_model(provider_id: str, model_id: str, *, quality: float, code: float = 1.0, quota: int | None = 10) -> ProviderModel:
    return ProviderModel(
        provider_id=provider_id,
        model_id=model_id,
        prompt_price=0.0,
        completion_price=0.0,
        request_price=0.0,
        capabilities={"code": code, "reasoning": quality},
        quality_hint=quality,
        quota_remaining=quota,
    )


def paid_model(provider_id: str, model_id: str, *, quality: float = 1.0) -> ProviderModel:
    return ProviderModel(
        provider_id=provider_id,
        model_id=model_id,
        prompt_price=0.01,
        completion_price=0.02,
        request_price=0.0,
        capabilities={"code": 1.0, "reasoning": quality},
        quality_hint=quality,
        quota_remaining=10,
    )


def proof(provider_id: str, model_id: str, *, safe: bool = True, stale: bool = False) -> ZeroCostQualification:
    return ZeroCostQualification(
        provider_id=provider_id,
        model_id=model_id,
        safe_class=ProviderSafetyClass.HARD_STOP_FREE_QUOTA,
        verified_at=NOW - timedelta(minutes=10),
        expires_at=(NOW - timedelta(seconds=1) if stale else NOW + timedelta(minutes=20)),
        prompt_price=0.0,
        completion_price=0.0,
        request_price=0.0,
        hard_overage_block=True,
        account_safe=safe,
        source="test-proof",
    )


class QualificationTests(unittest.TestCase):
    def test_exact_fresh_zero_cost_safe_account_is_admissible(self) -> None:
        self.assertTrue(proof("groq", "gpt-oss-120b").admissible(NOW))

    def test_paid_stale_or_unsafe_account_proof_is_rejected(self) -> None:
        self.assertFalse(proof("groq", "m", stale=True).admissible(NOW))
        self.assertFalse(proof("groq", "m", safe=False).admissible(NOW))
        paid = replace(proof("groq", "m"), prompt_price=0.001)
        self.assertFalse(paid.admissible(NOW))


class InferenceFabricTests(unittest.TestCase):
    def test_selects_strongest_eligible_zero_cost_model_not_highest_paid_model(self) -> None:
        atlas = normative_provider_atlas()
        openrouter = FakeProvider(
            atlas.get("openrouter"),
            [free_model("openrouter", "good:free", quality=0.85), paid_model("openrouter", "best-paid", quality=1.0)],
        )
        zai = FakeProvider(atlas.get("zai"), [free_model("zai", "glm-4.7-flash", quality=0.92)])
        fabric = InferenceFabric([openrouter, zai], QualificationRegistry(), now_fn=lambda: NOW)

        response = fabric.complete([{"role": "user", "content": "code"}], CapabilityRequirement({"code": 0.8}), mode="free-cloud")

        self.assertEqual((response.provider_id, response.model_id), ("zai", "glm-4.7-flash"))
        self.assertFalse(any(model_id == "best-paid" for model_id, _ in openrouter.calls))

    def test_account_proof_provider_is_blocked_until_fresh_safe_proof_exists(self) -> None:
        atlas = normative_provider_atlas()
        groq = FakeProvider(atlas.get("groq"), [free_model("groq", "gpt-oss-120b", quality=0.99)])
        registry = QualificationRegistry()
        fabric = InferenceFabric([groq], registry, now_fn=lambda: NOW)
        with self.assertRaises(RouteUnavailableError):
            fabric.complete([{"role": "user", "content": "hi"}], CapabilityRequirement({"code": 0.5}), mode="free-cloud")

        registry.upsert(proof("groq", "gpt-oss-120b"))
        response = fabric.complete([{"role": "user", "content": "hi"}], CapabilityRequirement({"code": 0.5}), mode="free-cloud")
        self.assertEqual(response.provider_id, "groq")

    def test_http_429_fails_over_across_provider_boundary_without_retrying_failed_route(self) -> None:
        atlas = normative_provider_atlas()
        first = FakeProvider(
            atlas.get("openrouter"),
            [free_model("openrouter", "top:free", quality=0.99)],
            [ProviderError("QUOTA_EXHAUSTED", provider_id="openrouter", model_id="top:free", retryable=True, status=429)],
        )
        second = FakeProvider(atlas.get("zai"), [free_model("zai", "glm-4.7-flash", quality=0.90)])
        messages = [{"role": "user", "content": "preserve me"}]
        fabric = InferenceFabric([first, second], QualificationRegistry(), now_fn=lambda: NOW)

        response = fabric.complete(messages, CapabilityRequirement({"code": 0.5}), mode="free-cloud")

        self.assertEqual(response.provider_id, "zai")
        self.assertEqual(len(first.calls), 1)
        self.assertEqual(second.calls[0][1], messages)

    def test_response_with_zero_remaining_quota_switches_model_on_next_request(self) -> None:
        atlas = normative_provider_atlas()
        provider = FakeProvider(
            atlas.get("openrouter"),
            [free_model("openrouter", "a:free", quality=0.99), free_model("openrouter", "b:free", quality=0.80)],
            [ProviderResponse("first", "openrouter", "a:free", quota_remaining=0), ProviderResponse("second", "openrouter", "b:free", quota_remaining=3)],
        )
        fabric = InferenceFabric([provider], QualificationRegistry(), now_fn=lambda: NOW)
        req = CapabilityRequirement({"code": 0.5})

        first = fabric.complete([{"role": "user", "content": "one"}], req, mode="free-cloud")
        second = fabric.complete([{"role": "user", "content": "two"}], req, mode="free-cloud")

        self.assertEqual(first.model_id, "a:free")
        self.assertEqual(second.model_id, "b:free")

    def test_hybrid_exhaustion_falls_back_to_local_ollama_but_free_cloud_fails_closed(self) -> None:
        atlas = normative_provider_atlas()
        dead_cloud = FakeProvider(
            atlas.get("openrouter"),
            [free_model("openrouter", "dead:free", quality=0.99)],
            [ProviderError("QUOTA_EXHAUSTED", provider_id="openrouter", model_id="dead:free", retryable=True, status=429)],
        )
        local = FakeProvider(atlas.get("ollama_local"), [free_model("ollama_local", "qwen3:4b", quality=0.60)])
        fabric = InferenceFabric([dead_cloud, local], QualificationRegistry(), now_fn=lambda: NOW)
        req = CapabilityRequirement({"code": 0.5})

        response = fabric.complete([{"role": "user", "content": "hi"}], req, mode="hybrid")
        self.assertEqual(response.provider_id, "ollama_local")

        dead_cloud_2 = FakeProvider(
            atlas.get("openrouter"),
            [free_model("openrouter", "dead:free", quality=0.99)],
            [ProviderError("QUOTA_EXHAUSTED", provider_id="openrouter", model_id="dead:free", retryable=True, status=429)],
        )
        local_2 = FakeProvider(atlas.get("ollama_local"), [free_model("ollama_local", "qwen3:4b", quality=0.60)])
        cloud_only = InferenceFabric([dead_cloud_2, local_2], QualificationRegistry(), now_fn=lambda: NOW)
        with self.assertRaises(RouteUnavailableError):
            cloud_only.complete([{"role": "user", "content": "hi"}], req, mode="free-cloud")
        self.assertEqual(len(local_2.calls), 0)


if __name__ == "__main__":
    unittest.main()
