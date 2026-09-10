from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

from alinacoder.intelligence_mesh.provider_atlas import normative_provider_atlas
from alinacoder.intelligence_mesh.runtime import build_default_inference_fabric


class _EmptyVault:
    def get(self, provider_id: str) -> str | None:
        return None


def _load(testcase: unittest.TestCase, module_name: str):
    try:
        spec = importlib.util.find_spec(module_name)
    except ModuleNotFoundError:
        spec = None
    testcase.assertIsNotNone(spec, f"missing module: {module_name}")
    return importlib.import_module(module_name)


class FrontierMeshV2Tests(unittest.TestCase):
    def test_kilo_definition_explicitly_allows_anonymous_free_access(self) -> None:
        kilo = normative_provider_atlas().get("kilo_gateway")
        self.assertTrue(getattr(kilo, "anonymous_free_allowed", False))
        self.assertTrue(kilo.structurally_auto_admissible)
        self.assertFalse(kilo.account_proof_required)

    def test_default_hybrid_runtime_constructs_anonymous_kilo_without_key(self) -> None:
        fabric = build_default_inference_fabric(_EmptyVault(), mode="hybrid")
        try:
            self.assertIn("kilo_gateway", fabric.provider_ids())
            self.assertIn("ollama_local", fabric.provider_ids())
        finally:
            close = getattr(fabric, "close", None)
            if callable(close):
                close()

    def test_wilson_lower_bound_is_conservative_and_monotonic(self) -> None:
        profiles = _load(self, "alinacoder.intelligence_mesh.profiles")
        wilson = getattr(profiles, "wilson_lower_bound", None)
        self.assertTrue(callable(wilson), "profiles.wilson_lower_bound is required")
        self.assertEqual(wilson(0, 0), 0.0)
        self.assertGreater(wilson(10, 10), wilson(8, 10))
        self.assertGreater(wilson(8, 10), wilson(4, 10))
        self.assertLess(wilson(10, 10), 1.0)

    def test_profile_store_penalizes_cold_start_below_proven_route(self) -> None:
        profiles = _load(self, "alinacoder.intelligence_mesh.profiles")
        with tempfile.TemporaryDirectory() as td:
            store = profiles.CapabilityProfileStore(Path(td) / "profiles.sqlite")
            try:
                for _ in range(8):
                    store.record("p", "proven", "lineage-a", "debug", True, benchmark_version="v1")
                for _ in range(2):
                    store.record("p", "cold", "lineage-b", "debug", True, benchmark_version="v1")
                proven = store.quality_lcb("p", "proven", "debug", seed_prior=0.70)
                cold = store.quality_lcb("p", "cold", "debug", seed_prior=0.95)
                self.assertGreater(proven, cold)
            finally:
                store.close()

    def test_task_classifier_detects_debug_and_architecture(self) -> None:
        tasks = _load(self, "alinacoder.intelligence_mesh.tasks")
        classifier = tasks.TaskClassifier()
        debug = classifier.classify([{"role": "user", "content": "Fix this traceback and failing test"}], None)
        architecture = classifier.classify([{"role": "user", "content": "Design the architecture and implementation plan"}], None)
        self.assertEqual(debug.value, "debug")
        self.assertEqual(architecture.value, "architecture")

    def test_quota_ledger_persists_429_cooldown_until_reset(self) -> None:
        quota = _load(self, "alinacoder.intelligence_mesh.quota")
        clock = [datetime(2026, 9, 10, 20, 0, tzinfo=timezone.utc)]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "quota.sqlite"
            ledger = quota.QuotaLedger(path, now_fn=lambda: clock[0])
            ledger.ensure_route("p", "m")
            ledger.observe_error("p", "m", code="QUOTA_EXHAUSTED", retry_after_seconds=60)
            self.assertFalse(ledger.eligible("p", "m"))
            ledger.close()

            reopened = quota.QuotaLedger(path, now_fn=lambda: clock[0])
            try:
                self.assertFalse(reopened.eligible("p", "m"))
                clock[0] += timedelta(seconds=61)
                self.assertTrue(reopened.eligible("p", "m"))
            finally:
                reopened.close()

    def test_quota_ledger_hard_blocks_billing_and_auth_errors(self) -> None:
        quota = _load(self, "alinacoder.intelligence_mesh.quota")
        with tempfile.TemporaryDirectory() as td:
            ledger = quota.QuotaLedger(Path(td) / "quota.sqlite")
            try:
                ledger.ensure_route("p", "bill")
                ledger.observe_error("p", "bill", code="BILLING_BLOCKED")
                self.assertEqual(ledger.get("p", "bill").state.value, "billing_blocked")
                self.assertFalse(ledger.eligible("p", "bill"))

                ledger.ensure_route("p", "auth")
                ledger.observe_error("p", "auth", code="AUTH_REQUIRED")
                self.assertEqual(ledger.get("p", "auth").state.value, "auth_blocked")
                self.assertFalse(ledger.eligible("p", "auth"))
            finally:
                ledger.close()


if __name__ == "__main__":
    unittest.main()
