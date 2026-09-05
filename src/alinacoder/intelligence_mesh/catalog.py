from __future__ import annotations

from dataclasses import dataclass

from .models import ModelRoute


@dataclass(frozen=True)
class CatalogDrift:
    key: tuple[str, str]
    kind: str


class ProviderCatalog:
    def __init__(self) -> None:
        self._routes: dict[tuple[str, str], ModelRoute] = {}
        self._drift: list[CatalogDrift] = []
        self._generation = 0

    @property
    def generation(self) -> int:
        return self._generation

    @property
    def drift(self) -> tuple[CatalogDrift, ...]:
        return tuple(self._drift)

    def refresh(self, snapshot: list[ModelRoute]) -> None:
        incoming = {route.key: route for route in snapshot}
        previous = self._routes
        drift: list[CatalogDrift] = []
        for key in previous.keys() - incoming.keys():
            drift.append(CatalogDrift(key, "MODEL_REMOVED"))
        for key in incoming.keys() - previous.keys():
            drift.append(CatalogDrift(key, "MODEL_ADDED"))
        for key in incoming.keys() & previous.keys():
            before = previous[key]
            after = incoming[key]
            if before.cost_proof.verdict != after.cost_proof.verdict or (
                before.cost_proof.prompt_price,
                before.cost_proof.completion_price,
                before.cost_proof.request_price,
            ) != (
                after.cost_proof.prompt_price,
                after.cost_proof.completion_price,
                after.cost_proof.request_price,
            ):
                drift.append(CatalogDrift(key, "FREE_STATUS_CHANGED"))
            if before.capabilities != after.capabilities:
                drift.append(CatalogDrift(key, "CAPABILITY_CHANGED"))
            if before.healthy != after.healthy:
                drift.append(CatalogDrift(key, "HEALTH_CHANGED"))
        self._routes = incoming
        self._drift = drift
        self._generation += 1

    def routes(self) -> list[ModelRoute]:
        return list(self._routes.values())

    def get(self, provider_id: str, model_id: str) -> ModelRoute:
        return self._routes[(provider_id, model_id)]
