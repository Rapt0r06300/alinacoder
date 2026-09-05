from __future__ import annotations

from datetime import datetime

from .catalog import ProviderCatalog
from .models import CapabilityRequirement, ModelRoute, RouteUnavailableError


class FrontierRouter:
    def _eligible(self, route: ModelRoute, requirement: CapabilityRequirement, now: datetime) -> bool:
        return (
            route.healthy
            and route.quota_remaining > 0
            and route.cost_proof.is_admissible(now)
            and route.covers(requirement)
        )

    def select(
        self,
        requirement: CapabilityRequirement,
        catalog: ProviderCatalog,
        *,
        current_route: ModelRoute | None = None,
        now: datetime,
    ) -> ModelRoute:
        eligible = [r for r in catalog.routes() if self._eligible(r, requirement, now)]
        if not eligible:
            raise RouteUnavailableError("no eligible zero-cost route")

        if current_route is not None:
            if self._eligible(current_route, requirement, now):
                current_match = next((r for r in eligible if r.key == current_route.key), None)
                if current_match is not None:
                    return current_match
            same_lineage = [r for r in eligible if r.lineage == current_route.lineage]
            if same_lineage:
                return max(same_lineage, key=lambda r: (r.quality_lcb, r.quota_remaining))

        return max(eligible, key=lambda r: (r.quality_lcb, r.quota_remaining))
