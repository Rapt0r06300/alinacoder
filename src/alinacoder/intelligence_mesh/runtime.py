from __future__ import annotations

from typing import Protocol

from .experiential import ExperientialProvider
from .fabric import InferenceFabric
from .provider_atlas import ProviderDefinition, normative_provider_atlas
from .providers import GeminiProvider, OllamaProvider, OpenAICompatibleProvider, ZeroCostProvider
from .qualification import QualificationRegistry


class CredentialReader(Protocol):
    def get(self, provider_id: str) -> str | None: ...


def _remote_provider(definition: ProviderDefinition, api_key: str) -> ZeroCostProvider | None:
    if definition.retired:
        return None
    has_credential = bool(api_key)
    if not has_credential and not definition.anonymous_free_allowed:
        return None
    if definition.provider_id == "experiential_gateway":
        if not has_credential:
            return None
        return ExperientialProvider(definition, api_key=api_key)
    if definition.protocol == "gemini":
        if not definition.base_url or not has_credential:
            return None
        return GeminiProvider(definition, api_key=api_key)
    if definition.protocol == "openai_chat":
        # Anonymous construction is intentionally limited by the provider
        # definition. The fabric still admits only exact current zero-price
        # routes, so this cannot create a paid anonymous fallback.
        if not definition.base_url:
            return None
        return OpenAICompatibleProvider(definition, api_key=api_key or None)
    return None


def build_default_inference_fabric(
    vault: CredentialReader,
    *,
    mode: str = "hybrid",
    qualification_registry: QualificationRegistry | None = None,
) -> InferenceFabric:
    """Build the executable provider set for the selected inference mode.

    The atlas is discovery/qualification policy; this builder only instantiates
    routes that can actually be called. Missing credentials leave ordinary
    remote providers inactive. Providers with explicitly documented anonymous
    free access may be constructed without a credential, but their individual
    models still pass the fabric's exact zero-cost admission policy. Local
    Ollama never requires an API credential.
    """

    normalized = str(mode).strip().lower()
    if normalized not in {"local-only", "free-cloud", "hybrid"}:
        raise ValueError("mode must be local-only, free-cloud, or hybrid")

    atlas = normative_provider_atlas()
    providers: list[ZeroCostProvider] = []

    if normalized in {"free-cloud", "hybrid"}:
        for definition in atlas.active():
            if definition.provider_id == "ollama_local":
                continue
            secret = vault.get(definition.provider_id)
            provider = _remote_provider(definition, secret or "")
            if provider is not None:
                providers.append(provider)

    if normalized in {"local-only", "hybrid"}:
        providers.append(OllamaProvider(atlas.get("ollama_local")))

    return InferenceFabric(providers, qualification_registry or QualificationRegistry())
