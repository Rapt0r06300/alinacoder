from __future__ import annotations

from typing import Protocol

from .fabric import InferenceFabric
from .provider_atlas import ProviderDefinition, normative_provider_atlas
from .providers import GeminiProvider, OllamaProvider, OpenAICompatibleProvider, ZeroCostProvider
from .qualification import QualificationRegistry


class CredentialReader(Protocol):
    def get(self, provider_id: str) -> str | None: ...


def _remote_provider(definition: ProviderDefinition, api_key: str) -> ZeroCostProvider | None:
    if definition.retired or not api_key:
        return None
    if definition.protocol == "gemini":
        if not definition.base_url:
            return None
        return GeminiProvider(definition, api_key=api_key)
    if definition.protocol == "openai_chat":
        # A route without a concrete API base cannot be executed safely by the
        # generic adapter. Keep it in the normative atlas, but do not construct
        # a runtime provider until a provider-specific adapter exists.
        if not definition.base_url:
            return None
        return OpenAICompatibleProvider(definition, api_key=api_key)
    return None


def build_default_inference_fabric(
    vault: CredentialReader,
    *,
    mode: str = "hybrid",
    qualification_registry: QualificationRegistry | None = None,
) -> InferenceFabric:
    """Build the executable provider set for the selected inference mode.

    The atlas is discovery/qualification policy; this builder only instantiates
    routes that can actually be called. Missing credentials simply leave a
    remote provider inactive. Local Ollama never requires an API credential.
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
