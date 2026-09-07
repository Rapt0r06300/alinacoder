from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from alinacoder.intelligence_mesh import (
    CapabilityRequirement,
    CostProofReceipt,
    HttpResult,
    InferenceFabric,
    OpenAICompatibleProvider,
    ProviderError,
    ProviderModel,
    ProviderResponse,
    ProviderSafetyClass,
    QualificationRegistry,
    SponsoredCreditQualification,
    normative_provider_atlas,
)


class _FakeProvider:
    def __init__(self, definition, models, *, response_text="ok", errors=None):
        self.definition = definition
        self._models = list(models)
        self._response_text = response_text
        self._errors = list(errors or [])
        self.calls = []

    def discover(self):
        return list(self._models)

    def complete(self, model_id, messages):
        self.calls.append((model_id, list(messages)))
        if self._errors:
            raise self._errors.pop(0)
        return ProviderResponse(self._response_text, self.definition.provider_id, model_id, quota_remaining=1)


class _CaptureTransport:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def request(self, method, url, *, headers, payload, timeout):
        self.calls.append((method, url, dict(headers), payload, timeout))
        return self.result


class ExperientialFrontierGatewayTests(unittest.TestCase):
    def _now(self):
        return datetime(2026, 9, 7, 18, 30, tzinfo=timezone.utc)

    def _sponsored(self, **overrides):
        now = self._now()
        values = {
            "provider_id": "experiential_gateway",
            "model_id": "gpt-6-astra",
            "verified_at": now - timedelta(minutes=1),
            "expires_at": now + timedelta(minutes=10),
            "list_prompt_price": 10.0,
            "list_completion_price": 50.0,
            "list_request_price": 0.0,
            "credit_remaining_usd": 5.0,
            "platform_funded_lane": True,
            "auto_recharge_disabled": True,
            "hard_quota_stop": True,
            "byok_fallback_disabled": True,
            "paid_fallback_disabled": True,
            "account_safe": True,
            "source": "experiential-account-proof",
            "zdr_satisfied": True,
            "no_training_satisfied": True,
        }
        values.update(overrides)
        return SponsoredCreditQualification(**values)

    def test_new_safety_class_is_distinct_from_exact_zero_price(self):
        self.assertEqual(
            ProviderSafetyClass.SPONSORED_CREDIT_HARD_STOP.value,
            "SPONSORED_CREDIT_HARD_STOP",
        )

    def test_sponsored_qualification_requires_complete_hard_stop_contract(self):
        now = self._now()
        self.assertTrue(self._sponsored().admissible(now))
        for field, unsafe in (
            ("credit_remaining_usd", 0.0),
            ("platform_funded_lane", False),
            ("auto_recharge_disabled", False),
            ("hard_quota_stop", False),
            ("byok_fallback_disabled", False),
            ("paid_fallback_disabled", False),
            ("account_safe", False),
            ("zdr_satisfied", False),
            ("no_training_satisfied", False),
        ):
            with self.subTest(field=field):
                self.assertFalse(self._sponsored(**{field: unsafe}).admissible(now))
        self.assertFalse(self._sponsored(expires_at=now - timedelta(seconds=1)).admissible(now))

    def test_cost_receipt_preserves_positive_list_price_for_sponsored_route(self):
        now = self._now()
        receipt = CostProofReceipt(
            "experiential_gateway",
            "gpt-6-astra",
            10.0,
            50.0,
            0.0,
            "SPONSORED_CREDIT_HARD_STOP",
            now - timedelta(minutes=1),
            now + timedelta(minutes=10),
            hard_overage_block=True,
            billing_class="SPONSORED_CREDIT_HARD_STOP",
            sponsored_credit_remaining_usd=5.0,
            auto_recharge_disabled=True,
            byok_fallback_disabled=True,
            paid_fallback_disabled=True,
        )
        self.assertTrue(receipt.is_admissible(now))
        self.assertEqual((receipt.prompt_price, receipt.completion_price), (10.0, 50.0))

    def test_positive_price_receipt_is_not_admissible_without_sponsored_guards(self):
        now = self._now()
        receipt = CostProofReceipt(
            "experiential_gateway",
            "gpt-6-astra",
            10.0,
            50.0,
            0.0,
            "SPONSORED_CREDIT_HARD_STOP",
            now,
            now + timedelta(minutes=10),
            hard_overage_block=True,
        )
        self.assertFalse(receipt.is_admissible(now))

    def test_atlas_registers_experiential_as_guarded_aggregator(self):
        entry = normative_provider_atlas().get("experiential_gateway")
        self.assertEqual(entry.base_url, "https://api.experientiallabs.ai/v1")
        self.assertEqual(entry.discovery_url, "https://api.experientiallabs.ai/v1/models")
        self.assertEqual(entry.auth_env, "EXPERIENTIAL_API_KEY")
        self.assertTrue(entry.aggregator)
        self.assertTrue(entry.account_proof_required)
        self.assertFalse(entry.structurally_auto_admissible)
        self.assertIn(ProviderSafetyClass.SPONSORED_CREDIT_HARD_STOP, entry.safe_classes)

    def test_positive_price_experiential_route_requires_sponsored_proof(self):
        now = self._now()
        definition = normative_provider_atlas().get("experiential_gateway")
        model = ProviderModel(
            "experiential_gateway",
            "gpt-6-astra",
            prompt_price=10.0,
            completion_price=50.0,
            request_price=0.0,
            capabilities={"code": 1.0},
            quality_hint=0.99,
        )
        provider = _FakeProvider(definition, [model])
        registry = QualificationRegistry()
        fabric = InferenceFabric([provider], registry, now_fn=lambda: now)
        with self.assertRaises(Exception):
            fabric.complete([{"role": "user", "content": "fix it"}], CapabilityRequirement({"code": 0.8}), mode="free-cloud")

        registry.upsert_sponsored(self._sponsored())
        response = fabric.complete([{"role": "user", "content": "fix it"}], CapabilityRequirement({"code": 0.8}), mode="free-cloud")
        self.assertEqual(response.model_id, "gpt-6-astra")

    def test_quota_and_billing_errors_fail_over_without_reusing_blocked_route(self):
        now = self._now()
        atlas = normative_provider_atlas()
        exp = atlas.get("experiential_gateway")
        backup = atlas.get("openrouter")
        primary_model = ProviderModel(
            "experiential_gateway", "gpt-6-astra", 10.0, 50.0, 0.0,
            capabilities={"code": 1.0}, quality_hint=0.99,
        )
        backup_model = ProviderModel(
            "openrouter", "qwen-free", 0.0, 0.0, 0.0,
            capabilities={"code": 1.0}, quality_hint=0.8,
        )
        primary = _FakeProvider(
            exp,
            [primary_model],
            errors=[ProviderError("QUOTA_EXHAUSTED", provider_id="experiential_gateway", model_id="gpt-6-astra", retryable=True, status=429)],
        )
        secondary = _FakeProvider(backup, [backup_model], response_text="backup")
        registry = QualificationRegistry()
        registry.upsert_sponsored(self._sponsored())
        fabric = InferenceFabric([primary, secondary], registry, now_fn=lambda: now)
        response = fabric.complete([{"role": "user", "content": "fix"}], CapabilityRequirement({"code": 0.5}), mode="free-cloud")
        self.assertEqual(response.text, "backup")
        self.assertEqual(len(primary.calls), 1)

    def test_generic_adapter_never_exposes_bearer_secret_in_response_metadata(self):
        definition = normative_provider_atlas().get("experiential_gateway")
        transport = _CaptureTransport(
            HttpResult(
                200,
                {},
                b'{"choices":[{"message":{"content":"ok"}}]}',
            )
        )
        secret = "xpl_supersecretvalue"
        provider = OpenAICompatibleProvider(definition, api_key=secret, transport=transport)
        response = provider.complete("gpt-6-astra", [{"role": "user", "content": "hi"}])
        self.assertEqual(response.text, "ok")
        self.assertNotIn(secret, repr(response.metadata))
        self.assertEqual(transport.calls[0][2]["Authorization"], f"Bearer {secret}")


if __name__ == "__main__":
    unittest.main()
