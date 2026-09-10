from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .experiential import ExperientialProvider
from .fabric import InferenceFabric
from .profiles import CapabilityProfileStore
from .provider_atlas import ProviderDefinition, normative_provider_atlas
from .providers import GeminiProvider, OllamaProvider, OpenAICompatibleProvider, ZeroCostProvider
from .qualification import QualificationRegistry
from .quota import QuotaLedger


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
        if not definition.base_url:
            return None
        return OpenAICompatibleProvider(definition, api_key=api_key or None)
    return None


def _runtime_state_dir(vault: CredentialReader, explicit: Path | str | None) -> Path | None:
    if explicit is not None:
        return Path(explicit)
    vault_path = getattr(vault, "path", None)
    if vault_path is None:
        return None
    return Path(vault_path).parent / "runtime-intelligence"


def build_default_inference_fabric(
    vault: CredentialReader,
    *,
    mode: str = "hybrid",
    qualification_registry: QualificationRegistry | None = None,
    runtime_state_dir: Path | str | None = None,
) -> InferenceFabric:
    """Build executable routes plus persistent capability/quota intelligence.

    Missing credentials leave ordinary remote providers inactive. Providers
    with explicitly documented anonymous free access may be constructed without
    a credential, but individual models still pass exact cost admission. When a
    filesystem-backed vault is used, model outcomes and quota/health state are
    stored beside (not inside) the credential vault; no secret is copied there.
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

    state_dir = _runtime_state_dir(vault, runtime_state_dir)
    profiles = None
    quota = None
    owns_stores = False
    if state_dir is not None:
        state_dir.mkdir(parents=True, exist_ok=True)
        profiles = CapabilityProfileStore(state_dir / "capability-profiles.sqlite")
        quota = QuotaLedger(state_dir / "quota-ledger.sqlite")
        owns_stores = True

    return InferenceFabric(
        providers,
        qualification_registry or QualificationRegistry(),
        profile_store=profiles,
        quota_ledger=quota,
        owns_runtime_stores=owns_stores,
    )
