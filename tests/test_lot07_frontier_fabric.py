from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from alinacoder.intelligence_mesh import (
    CapabilityRequirement,
    ContinuityEnvelope,
    CostProofReceipt,
    FrontierRouter,
    ModelRoute,
    ProviderCatalog,
    RouteUnavailableError,
    StaleResponseError,
)


class Lot07FrontierFabricTests(unittest.TestCase):
    def _now(self):
        return datetime(2026, 9, 5, tzinfo=timezone.utc)

    def _free(self, provider: str, model: str, ttl_minutes: int = 30):
        now = self._now()
        return CostProofReceipt(provider, model, 0.0, 0.0, 0.0, "PROVEN_ZERO_COST", now, now + timedelta(minutes=ttl_minutes), hard_overage_block=True)

    def test_only_exact_fresh_proven_zero_cost_route_is_admissible(self):
        now = self._now()
        self.assertTrue(self._free("p", "m").is_admissible(now))
        paid = CostProofReceipt("p", "m", 0.01, 0, 0, "PAID", now, now + timedelta(hours=1), True)
        self.assertFalse(paid.is_admissible(now))
        expired = self._free("p", "m", ttl_minutes=-1)
        self.assertFalse(expired.is_admissible(now))

    def test_router_matches_capability_not_model_name(self):
        cat = ProviderCatalog()
        cat.refresh([
            ModelRoute("p1", "small", "fam-a", {"reasoning":0.7,"code":0.95}, self._free("p1","small"), quality_lcb=0.8),
            ModelRoute("p2", "huge", "fam-b", {"reasoning":0.99,"code":0.5}, self._free("p2","huge"), quality_lcb=0.95),
        ])
        route = FrontierRouter().select(CapabilityRequirement({"code":0.9}), cat, now=self._now())
        self.assertEqual(route.model_id, "small")

    def test_price_change_quarantines_route_before_next_call(self):
        cat = ProviderCatalog()
        cat.refresh([ModelRoute("p", "m", "fam", {"code":1.0}, self._free("p","m"), quality_lcb=0.9)])
        cat.refresh([ModelRoute("p", "m", "fam", {"code":1.0}, CostProofReceipt("p","m",0.01,0,0,"PAID",self._now(),self._now()+timedelta(hours=1),True), quality_lcb=0.9)])
        with self.assertRaises(RouteUnavailableError):
            FrontierRouter().select(CapabilityRequirement({"code":0.5}), cat, now=self._now())

    def test_quota_exhaustion_fails_over(self):
        cat = ProviderCatalog()
        cat.refresh([
            ModelRoute("p1","m1","fam",{"code":1.0},self._free("p1","m1"),quality_lcb=0.95,quota_remaining=0),
            ModelRoute("p2","m2","fam2",{"code":1.0},self._free("p2","m2"),quality_lcb=0.9,quota_remaining=3),
        ])
        route = FrontierRouter().select(CapabilityRequirement({"code":0.5}), cat, now=self._now())
        self.assertEqual(route.provider_id, "p2")

    def test_same_lineage_host_failover_is_preferred_when_current_host_unhealthy(self):
        cat = ProviderCatalog()
        cat.refresh([
            ModelRoute("dead","m","fam",{"code":1.0},self._free("dead","m"),quality_lcb=0.95,healthy=False),
            ModelRoute("mirror","m","fam",{"code":1.0},self._free("mirror","m"),quality_lcb=0.8),
            ModelRoute("other","x","fam-x",{"code":1.0},self._free("other","x"),quality_lcb=0.99),
        ])
        current = cat.get("dead","m")
        route = FrontierRouter().select(CapabilityRequirement({"code":0.5}), cat, current_route=current, now=self._now())
        self.assertEqual((route.provider_id, route.lineage), ("mirror","fam"))

    def test_continuity_envelope_and_stale_response_gate(self):
        env = ContinuityEnvelope("session", 7, "abc", "head", "intent-v2")
        self.assertTrue(env.verify(session_id="session", state_version=7, state_checksum="abc", repo_head="head", intent_version="intent-v2"))
        with self.assertRaises(StaleResponseError):
            env.admit_response(current_state_version=8, current_checksum="def", response_state_version=7, response_checksum="abc")


if __name__ == "__main__":
    unittest.main()
