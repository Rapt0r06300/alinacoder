from __future__ import annotations

from datetime import datetime, timedelta, timezone
import time
from typing import Callable, Iterable

from .catalog import ProviderCatalog
from .models import CapabilityRequirement, CostProofReceipt, ModelRoute, RouteUnavailableError
from .profiles import CapabilityProfileStore
from .provider_atlas import ProviderSafetyClass
from .providers import ProviderError, ProviderModel, ProviderResponse, ZeroCostProvider
from .qualification import QualificationRegistry, SponsoredCreditQualification
from .quota import QuotaLedger
from .routing import FrontierRouter
from .tasks import TaskClass, TaskClassifier


class InferenceFabric:
    """Fail-closed free/sponsored inference orchestrator with evidence-aware failover."""

    def __init__(
        self,
        providers: Iterable[ZeroCostProvider],
        qualification_registry: QualificationRegistry,
        *,
        now_fn: Callable[[], datetime] | None = None,
        profile_store: CapabilityProfileStore | None = None,
        quota_ledger: QuotaLedger | None = None,
        task_classifier: TaskClassifier | None = None,
        owns_runtime_stores: bool = False,
    ) -> None:
        self._providers = list(providers)
        self._registry = qualification_registry
        self._now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self._router = FrontierRouter()
        self._depleted: set[tuple[str, str]] = set()
        self._profiles = profile_store
        self._quota = quota_ledger
        self._task_classifier = task_classifier or TaskClassifier()
        self._owns_runtime_stores = bool(owns_runtime_stores)

    def close(self) -> None:
        if not self._owns_runtime_stores:
            return
        if self._profiles is not None:
            self._profiles.close()
            self._profiles = None
        if self._quota is not None:
            self._quota.close()
            self._quota = None

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
            return None
        return proof

    def _quota_allows(self, provider_id: str, model_id: str) -> bool:
        if self._quota is None:
            return (provider_id, model_id) not in self._depleted
        self._quota.ensure_route(provider_id, model_id)
        return self._quota.eligible(provider_id, model_id)

    def _remote_admissible(self, provider: ZeroCostProvider, model: ProviderModel, now: datetime) -> bool:
        definition = provider.definition
        if definition.retired or not self._quota_allows(definition.provider_id, model.model_id):
            return False
        if model.quota_remaining is not None and model.quota_remaining <= 0:
            return False

        sponsored = self._sponsored_proof(provider, model, now)
        if sponsored is not None:
            return True
        if self._has_nonzero_known_price(model):
            return False
        if definition.structurally_auto_admissible and model.zero_price and not definition.account_proof_required:
            return True
        proof = self._registry.get(definition.provider_id, model.model_id)
        return bool(proof and proof.admissible(now))

    def _local_admissible(self, provider: ZeroCostProvider, model: ProviderModel) -> bool:
        return (
            not provider.definition.retired
            and self._quota_allows(provider.definition.provider_id, model.model_id)
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

    def _quality_for(self, model: ProviderModel, task_class: TaskClass) -> float:
        if self._profiles is None:
            return float(model.quality_hint)
        lineage = str(model.metadata.get("lineage") or model.model_id)
        return self._profiles.quality_lcb(
            model.provider_id,
            model.model_id,
            task_class.value,
            seed_prior=float(model.quality_hint),
        )

    def _capabilities_for(self, model: ProviderModel) -> dict[str, float]:
        capabilities = dict(model.capabilities)
        if self._profiles is None:
            return capabilities
        # Once enough direct observations exist for a mandatory dimension,
        # measured evidence supersedes static provider hints. Cold-start data
        # informs ranking but does not prematurely make a route incapable.
        for name, seed in list(capabilities.items()):
            observation = self._profiles.observation(model.provider_id, model.model_id, name)
            if observation is not None and observation.trials >= 5:
                capabilities[name] = self._profiles.quality_lcb(
                    model.provider_id, model.model_id, name, seed_prior=float(seed)
                )
        return capabilities

    def _discover_phase(
        self,
        providers: list[ZeroCostProvider],
        *,
        now: datetime,
        attempted: set[tuple[str, str]],
        task_class: TaskClass,
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
                    capabilities=self._capabilities_for(model),
                    cost_proof=receipt,
                    quality_lcb=self._quality_for(model, task_class),
                    quota_remaining=max(1, int(quota)),
                    healthy=True,
                    metadata={
                        "protocol": provider.definition.protocol,
                        "billing_class": receipt.billing_class,
                        "task_class": task_class.value,
                    },
                )
                routes.append(route)
                owners[key] = provider
        catalog.refresh(routes)
        return catalog, owners

    @staticmethod
    def _retry_seconds(exc: ProviderError) -> float | None:
        value = exc.metadata.get("retry_after") if isinstance(exc.metadata, dict) else None
        try:
            return None if value is None else max(0.0, float(value))
        except (TypeError, ValueError):
            return None

    def _observe_error(self, route: ModelRoute, exc: ProviderError) -> None:
        if self._quota is not None:
            self._quota.observe_error(
                route.provider_id,
                route.model_id,
                code=exc.code,
                retry_after_seconds=self._retry_seconds(exc),
            )
        elif exc.code in {"QUOTA_EXHAUSTED", "BILLING_BLOCKED"}:
            self._depleted.add(route.key)

    def _observe_success(self, route: ModelRoute, response: ProviderResponse, elapsed_ms: float) -> None:
        if self._quota is not None:
            self._quota.observe_response(
                route.provider_id,
                route.model_id,
                remaining_requests=response.quota_remaining,
                latency_ms=elapsed_ms,
                cost_proof_expires_at=route.cost_proof.expires_at,
            )
        elif response.quota_remaining is not None and response.quota_remaining <= 0:
            self._depleted.add(route.key)

    def _run_phase(
        self,
        providers: list[ZeroCostProvider],
        messages: list[dict[str, str]],
        requirement: CapabilityRequirement,
        task_class: TaskClass,
    ) -> ProviderResponse:
        attempted: set[tuple[str, str]] = set()
        current_route: ModelRoute | None = None
        while True:
            now = self._now_fn()
            catalog, owners = self._discover_phase(
                providers, now=now, attempted=attempted, task_class=task_class
            )
            route = self._router.select(requirement, catalog, current_route=current_route, now=now)
            key = route.key
            provider = owners[key]
            attempted.add(key)
            started = time.monotonic()
            try:
                response = provider.complete(route.model_id, [dict(item) for item in messages])
            except ProviderError as exc:
                self._observe_error(route, exc)
                current_route = route
                continue
            elapsed_ms = (time.monotonic() - started) * 1000.0
            if response.provider_id != route.provider_id or response.model_id != route.model_id:
                mismatch = ProviderError(
                    "INVALID_RESPONSE",
                    provider_id=route.provider_id,
                    model_id=route.model_id,
                    retryable=False,
                    metadata={"reason": "provider/model identity mismatch"},
                )
                self._observe_error(route, mismatch)
                current_route = route
                continue
            self._observe_success(route, response, elapsed_ms)
            metadata = dict(response.metadata)
            metadata.update(
                {
                    "task_class": task_class.value,
                    "quality_lcb": route.quality_lcb,
                    "route_reason": f"best verified {task_class.value} LCB among available admissible routes",
                    "zero_cost_verdict": route.cost_proof.verdict,
                    "billing_class": route.cost_proof.billing_class,
                }
            )
            return ProviderResponse(
                text=response.text,
                provider_id=response.provider_id,
                model_id=response.model_id,
                quota_remaining=response.quota_remaining,
                metadata=metadata,
            )

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
        task_class = self._task_classifier.classify(messages, requirement)
        remote = [provider for provider in self._providers if not self._is_local(provider)]
        local = [provider for provider in self._providers if self._is_local(provider)]
        if normalized == "local-only":
            return self._run_phase(local, messages, requirement, task_class)
        if normalized == "free-cloud":
            return self._run_phase(remote, messages, requirement, task_class)
        try:
            return self._run_phase(remote, messages, requirement, task_class)
        except RouteUnavailableError:
            return self._run_phase(local, messages, requirement, task_class)
