from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Callable, Iterable

from .catalog import ProviderCatalog
from .models import CapabilityRequirement, CostProofReceipt, ModelRoute, RouteUnavailableError
from .provider_atlas import ProviderSafetyClass
from .providers import ProviderError, ProviderModel, ProviderResponse, ZeroCostProvider
from .qualification import QualificationRegistry, SponsoredCreditQualification
from .routing import FrontierRouter


class InferenceFabric:
    """Fail-closed free/sponsored inference orchestrator with provider/model failover."""

    def __init__(
        self,
        providers: Iterable[ZeroCostProvider],
        qualification_registry: QualificationRegistry,
        *,
        now_fn: Callable[[], datetime] | None = None,
    ) -> None:
        self._providers = list(providers)
        self._registry = qualification_registry
        self._now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self._router = FrontierRouter()
        self._depleted: set[tuple[str, str]] = set()

    def provider_ids(self) -> tuple[str, ...]:
        """Return instantiated providers in deterministic runtime order."""

        return tuple(provider.definition.provider_id for provider in self._providers)

    def _is_local(self, provider: ZeroCostProvider) -> bool:
        return provider.definition.provider_id == "ollama_local" or provider.definition.protocol == "ollama"

    @staticmethod
    def _known_prices(model: ProviderModel) -> tuple[float | None, float | None, float | None]:
        return (model.prompt_price, model.completion_price, model.request_price)

    @staticmethod
    def _has_nonzero_known_price(model: ProviderModel) -> bool:
        return any(value is not None and float(value) != 0.0 for value in InferenceFabric._known_prices(model))

    @staticmethod
    def _all_prices_known_zero(model: ProviderModel) -> bool:
        values = InferenceFabric._known_prices(model)
        return all(value is not None and float(value) == 0.0 for value in values)

    @staticmethod
    def _sponsored_prices_match(model: ProviderModel, proof: SponsoredCreditQualification) -> bool:
        observed = InferenceFabric._known_prices(model)
        proven = (proof.list_prompt_price, proof.list_completion_price, proof.list_request_price)
        for actual, expected in zip(observed, proven):
            if actual is not None and float(actual) != float(expected):
                return False
        return True

    def _sponsored_proof(
        self,
        provider: ZeroCostProvider,
        model: ProviderModel,
        now: datetime,
    ) -> SponsoredCreditQualification | None:
        definition = provider.definition
        if ProviderSafetyClass.SPONSORED_CREDIT_HARD_STOP not in definition.safe_classes:
            return None
        proof = self._registry.get_sponsored(definition.provider_id, model.model_id)
        if not proof or not proof.admissible(now):
            return None
        if not self._sponsored_prices_match(model, proof):
            return None
        if self._all_prices_known_zero(model):
            # Exact zero-price models remain governed by the existing zero-cost
            # proof contract rather than being re-labelled as sponsored.
            return None
        return proof

    def _remote_admissible(self, provider: ZeroCostProvider, model: ProviderModel, now: datetime) -> bool:
        definition = provider.definition
        if definition.retired or (definition.provider_id, model.model_id) in self._depleted:
            return False
        if model.quota_remaining is not None and model.quota_remaining <= 0:
            return False

        sponsored = self._sponsored_proof(provider, model, now)
        if sponsored is not None:
            return True

        # A live paid model row always loses unless the complete sponsored-credit
        # contract above is proven for the exact route.
        if self._has_nonzero_known_price(model):
            return False
        if definition.structurally_auto_admissible and model.zero_price and not definition.account_proof_required:
            return True
        proof = self._registry.get(definition.provider_id, model.model_id)
        return bool(proof and proof.admissible(now))

    def _local_admissible(self, provider: ZeroCostProvider, model: ProviderModel) -> bool:
        return (
            not provider.definition.retired
            and (provider.definition.provider_id, model.model_id) not in self._depleted
            and (model.quota_remaining is None or model.quota_remaining > 0)
            and ProviderSafetyClass.LOCAL_NO_API_BILLING in provider.definition.safe_classes
            and model.zero_price
        )

    def _cost_receipt(self, provider: ZeroCostProvider, model: ProviderModel, now: datetime) -> CostProofReceipt:
        definition = provider.definition
        sponsored = None if self._is_local(provider) else self._sponsored_proof(provider, model, now)
        if sponsored is not None:
            return CostProofReceipt(
                definition.provider_id,
                model.model_id,
                sponsored.list_prompt_price,
                sponsored.list_completion_price,
                sponsored.list_request_price,
                "SPONSORED_CREDIT_HARD_STOP",
                sponsored.verified_at,
                sponsored.expires_at,
                hard_overage_block=sponsored.hard_quota_stop,
                billing_class="SPONSORED_CREDIT_HARD_STOP",
                sponsored_credit_remaining_usd=sponsored.credit_remaining_usd,
                auto_recharge_disabled=sponsored.auto_recharge_disabled,
                byok_fallback_disabled=sponsored.byok_fallback_disabled,
                paid_fallback_disabled=sponsored.paid_fallback_disabled,
            )

        if self._is_local(provider):
            expires = now + timedelta(minutes=5)
        else:
            registered = self._registry.get(definition.provider_id, model.model_id)
            expires = registered.expires_at if registered and registered.admissible(now) else now + timedelta(minutes=1)
        return CostProofReceipt(
            definition.provider_id,
            model.model_id,
            0.0,
            0.0,
            0.0,
            "PROVEN_ZERO_COST",
            now,
            expires,
            hard_overage_block=True,
        )

    def _discover_phase(
        self,
        providers: list[ZeroCostProvider],
        *,
        now: datetime,
        attempted: set[tuple[str, str]],
    ) -> tuple[ProviderCatalog, dict[tuple[str, str], ZeroCostProvider]]:
        catalog = ProviderCatalog()
        routes: list[ModelRoute] = []
        owners: dict[tuple[str, str], ZeroCostProvider] = {}
        for provider in providers:
            try:
                models = provider.discover()
            except ProviderError:
                continue
            for model in models:
                key = (provider.definition.provider_id, model.model_id)
                if key in attempted:
                    continue
                admissible = self._local_admissible(provider, model) if self._is_local(provider) else self._remote_admissible(provider, model, now)
                if not admissible:
                    continue
                quota = model.quota_remaining if model.quota_remaining is not None else 1
                receipt = self._cost_receipt(provider, model, now)
                route = ModelRoute(
                    provider_id=provider.definition.provider_id,
                    model_id=model.model_id,
                    lineage=str(model.metadata.get("lineage") or model.model_id),
                    capabilities=dict(model.capabilities),
                    cost_proof=receipt,
                    quality_lcb=float(model.quality_hint),
                    quota_remaining=max(1, int(quota)),
                    healthy=True,
                    metadata={
                        "protocol": provider.definition.protocol,
                        "billing_class": receipt.billing_class,
                    },
                )
                routes.append(route)
                owners[key] = provider
        catalog.refresh(routes)
        return catalog, owners

    def _run_phase(
        self,
        providers: list[ZeroCostProvider],
        messages: list[dict[str, str]],
        requirement: CapabilityRequirement,
    ) -> ProviderResponse:
        attempted: set[tuple[str, str]] = set()
        current_route: ModelRoute | None = None
        while True:
            now = self._now_fn()
            catalog, owners = self._discover_phase(providers, now=now, attempted=attempted)
            route = self._router.select(requirement, catalog, current_route=current_route, now=now)
            key = route.key
            provider = owners[key]
            attempted.add(key)
            try:
                response = provider.complete(route.model_id, [dict(item) for item in messages])
            except ProviderError as exc:
                if exc.code in {"QUOTA_EXHAUSTED", "BILLING_BLOCKED"}:
                    self._depleted.add(key)
                current_route = route
                continue
            if response.provider_id != route.provider_id or response.model_id != route.model_id:
                current_route = route
                continue
            if response.quota_remaining is not None and response.quota_remaining <= 0:
                self._depleted.add(key)
            return response

    def complete(
        self,
        messages: list[dict[str, str]],
        requirement: CapabilityRequirement,
        *,
        mode: str,
    ) -> ProviderResponse:
        normalized = str(mode).strip().lower()
        if normalized not in {"local-only", "free-cloud", "hybrid"}:
            raise ValueError("mode must be local-only, free-cloud, or hybrid")
        if not messages:
            raise ValueError("messages are required")

        remote = [provider for provider in self._providers if not self._is_local(provider)]
        local = [provider for provider in self._providers if self._is_local(provider)]
        if normalized == "local-only":
            return self._run_phase(local, messages, requirement)
        if normalized == "free-cloud":
            return self._run_phase(remote, messages, requirement)
        try:
            return self._run_phase(remote, messages, requirement)
        except RouteUnavailableError:
            return self._run_phase(local, messages, requirement)
