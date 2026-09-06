from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProviderSafetyClass(str, Enum):
    ZERO_PRICE_MODEL = "ZERO_PRICE_MODEL"
    HARD_STOP_FREE_QUOTA = "HARD_STOP_FREE_QUOTA"
    NO_PAYMENT_METHOD_FREE_TIER = "NO_PAYMENT_METHOD_FREE_TIER"
    FREE_MODE_PAYG_DISABLED = "FREE_MODE_PAYG_DISABLED"
    LOCAL_NO_API_BILLING = "LOCAL_NO_API_BILLING"


@dataclass(frozen=True, slots=True)
class ProviderDefinition:
    provider_id: str
    label: str
    protocol: str
    base_url: str | None
    discovery_url: str | None
    auth_env: str | None
    safe_classes: tuple[ProviderSafetyClass, ...]
    account_proof_required: bool = True
    structurally_auto_admissible: bool = False
    aggregator: bool = False
    zero_cost_requalification_required: bool = True
    https_only: bool = True
    lifecycle_state: str = "ACTIVE"
    retired: bool = False
    source_urls: tuple[str, ...] = ()
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.provider_id:
            raise ValueError("provider_id is required")
        if self.protocol not in {"openai_chat", "gemini", "ollama", "custom"}:
            raise ValueError(f"unsupported provider protocol: {self.protocol}")
        if self.retired and self.lifecycle_state not in {"RETIRED", "TOMBSTONED"}:
            raise ValueError("retired provider must be RETIRED or TOMBSTONED")
        if self.https_only:
            for value in (self.base_url, self.discovery_url):
                if value and not value.startswith("https://"):
                    raise ValueError(f"remote provider URL must be HTTPS: {value}")


class ProviderAtlas:
    def __init__(self, entries: tuple[ProviderDefinition, ...]) -> None:
        by_id = {entry.provider_id: entry for entry in entries}
        if len(by_id) != len(entries):
            raise ValueError("duplicate provider_id in provider atlas")
        self._entries = entries
        self._by_id = by_id

    def entries(self) -> tuple[ProviderDefinition, ...]:
        return self._entries

    def get(self, provider_id: str) -> ProviderDefinition:
        return self._by_id[provider_id]

    def active(self) -> tuple[ProviderDefinition, ...]:
        return tuple(entry for entry in self._entries if not entry.retired)


_ZERO = (ProviderSafetyClass.ZERO_PRICE_MODEL,)
_HARD = (ProviderSafetyClass.HARD_STOP_FREE_QUOTA,)
_NO_CARD = (ProviderSafetyClass.NO_PAYMENT_METHOD_FREE_TIER,)
_PAYG_OFF = (ProviderSafetyClass.FREE_MODE_PAYG_DISABLED,)
_LOCAL = (ProviderSafetyClass.LOCAL_NO_API_BILLING,)


def normative_provider_atlas() -> ProviderAtlas:
    """Return the v0.2 provider discovery atlas.

    The atlas describes candidates and their qualification boundary.  It does
    not mark remote providers as free forever: every remote route is still
    requalified immediately before dispatch by the runtime fabric.
    """

    entries = (
        ProviderDefinition(
            "kilo_gateway",
            "Kilo Gateway",
            "openai_chat",
            "https://api.kilo.ai/api/gateway",
            "https://api.kilo.ai/api/gateway/models",
            "KILO_API_KEY",
            _ZERO,
            account_proof_required=False,
            structurally_auto_admissible=True,
            aggregator=True,
            source_urls=(
                "https://kilo.ai/docs/gateway/models-and-providers",
                "https://kilo.ai/docs/gateway/usage-and-billing",
            ),
            notes="Only exact current zero-price/free routes; provider-side paid fallback is forbidden.",
        ),
        ProviderDefinition(
            "zai",
            "Z.AI",
            "openai_chat",
            "https://api.z.ai/api/paas/v4",
            None,
            "ZAI_API_KEY",
            _ZERO,
            account_proof_required=False,
            structurally_auto_admissible=True,
            source_urls=("https://docs.z.ai/guides/overview/pricing",),
            notes="Only exact models whose current Z.AI pricing row is Free are eligible.",
        ),
        ProviderDefinition(
            "sambanova",
            "SambaNova Cloud",
            "openai_chat",
            "https://api.sambanova.ai/v1",
            "https://api.sambanova.ai/v1/models",
            "SAMBANOVA_API_KEY",
            _NO_CARD,
            source_urls=("https://docs.sambanova.ai/",),
            notes="Requires proof that the account remains Free Tier with no payment method.",
        ),
        ProviderDefinition(
            "groq",
            "Groq",
            "openai_chat",
            "https://api.groq.com/openai/v1",
            "https://api.groq.com/openai/v1/models",
            "GROQ_API_KEY",
            _HARD,
            source_urls=("https://console.groq.com/docs/rate-limits",),
            notes="Free-plan quotas are organization scoped; current account plan must be proven safe.",
        ),
        ProviderDefinition(
            "cloudflare_workers_ai",
            "Cloudflare Workers AI",
            "openai_chat",
            None,
            None,
            "CLOUDFLARE_API_TOKEN",
            _HARD,
            source_urls=(
                "https://developers.cloudflare.com/workers-ai/platform/pricing/",
                "https://developers.cloudflare.com/workers-ai/platform/limits/",
            ),
            notes="Only Workers Free plan is hard-safe; Workers Paid can bill above the daily allocation.",
        ),
        ProviderDefinition(
            "openrouter",
            "OpenRouter",
            "openai_chat",
            "https://openrouter.ai/api/v1",
            "https://openrouter.ai/api/v1/models",
            "OPENROUTER_API_KEY",
            _ZERO,
            account_proof_required=False,
            structurally_auto_admissible=True,
            aggregator=True,
            source_urls=("https://openrouter.ai/docs/api_reference/limits",),
            notes="Only exact current zero-price/:free routes; AlinaCoder owns failover and never supplies paid fallbacks.",
        ),
        ProviderDefinition(
            "gemini",
            "Google Gemini API",
            "gemini",
            "https://generativelanguage.googleapis.com/v1beta",
            None,
            "GEMINI_API_KEY",
            _HARD,
            source_urls=("https://ai.google.dev/gemini-api/docs/rate-limits",),
            notes="Free-tier project must be proven unlinked from billing for autonomous use.",
        ),
        ProviderDefinition(
            "mistral",
            "Mistral",
            "openai_chat",
            "https://api.mistral.ai/v1",
            "https://api.mistral.ai/v1/models",
            "MISTRAL_API_KEY",
            _PAYG_OFF,
            source_urls=(
                "https://docs.mistral.ai/admin/billing-usage/usage-limits",
                "https://docs.mistral.ai/admin/billing-usage/subscriptions",
            ),
            notes="Free mode is eligible only while pay-as-you-go is proven disabled.",
        ),
        ProviderDefinition(
            "huggingface",
            "Hugging Face Inference Providers",
            "openai_chat",
            "https://router.huggingface.co/v1",
            None,
            "HF_TOKEN",
            _HARD,
            aggregator=True,
            source_urls=("https://huggingface.co/docs/inference-providers/pricing",),
            notes="Monthly credits can coexist with extra usage; requires hard-stop/account proof.",
        ),
        ProviderDefinition(
            "tencent_hunyuan",
            "Tencent Hunyuan",
            "openai_chat",
            None,
            None,
            "TENCENT_HUNYUAN_API_KEY",
            _HARD,
            notes="Eligible only when post-payment is disabled and free entitlement remains.",
        ),
        ProviderDefinition(
            "alibaba_model_studio",
            "Alibaba Model Studio",
            "openai_chat",
            "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            None,
            "DASHSCOPE_API_KEY",
            _HARD,
            notes="Requires current Free Quota Only / hard-stop proof for the exact region and account.",
        ),
        ProviderDefinition(
            "siliconflow",
            "SiliconFlow",
            "openai_chat",
            "https://api.siliconflow.cn/v1",
            "https://api.siliconflow.cn/v1/models",
            "SILICONFLOW_API_KEY",
            _ZERO,
            notes="Only exact live zero-price models are eligible; signup credits are not standing free capacity.",
        ),
        ProviderDefinition(
            "scaleway",
            "Scaleway Generative APIs",
            "openai_chat",
            "https://api.scaleway.ai/v1",
            None,
            "SCALEWAY_API_KEY",
            _HARD,
            notes="Trial/free allowance is blocked unless independent hard zero-spend control is proven.",
        ),
        ProviderDefinition(
            "ollama_local",
            "Ollama Local",
            "ollama",
            "http://127.0.0.1:11434",
            "http://127.0.0.1:11434/api/tags",
            None,
            _LOCAL,
            account_proof_required=False,
            structurally_auto_admissible=True,
            zero_cost_requalification_required=False,
            https_only=False,
            notes="Foundational local zero-API-billing fallback.",
        ),
        ProviderDefinition(
            "ollama_cloud",
            "Ollama Cloud",
            "openai_chat",
            "https://ollama.com/v1",
            None,
            "OLLAMA_API_KEY",
            _HARD,
            notes="Free usage may coexist with purchased credits; account behavior must prove no paid spillover.",
        ),
        ProviderDefinition(
            "nvidia_nim",
            "NVIDIA NIM",
            "openai_chat",
            "https://integrate.api.nvidia.com/v1",
            "https://integrate.api.nvidia.com/v1/models",
            "NVIDIA_API_KEY",
            _HARD,
            source_urls=("https://docs.api.nvidia.com/nim/",),
            notes="Hosted access may be trial/evaluation scoped; use-scope and zero-spend proof are mandatory.",
        ),
        ProviderDefinition(
            "cerebras",
            "Cerebras",
            "openai_chat",
            "https://api.cerebras.ai/v1",
            "https://api.cerebras.ai/v1/models",
            "CEREBRAS_API_KEY",
            _HARD,
            notes="Current account entitlement must prove hard-stop free capacity; trial/payment-gated access is not auto-admitted.",
        ),
        ProviderDefinition(
            "opencode_zen",
            "OpenCode Zen",
            "openai_chat",
            None,
            None,
            "OPENCODE_ZEN_API_KEY",
            _ZERO,
            aggregator=True,
            notes="Zero-priced model rows still require proof that auto-reload and paid fallback are impossible.",
        ),
        ProviderDefinition(
            "github_models",
            "GitHub Models",
            "openai_chat",
            None,
            None,
            None,
            (),
            account_proof_required=True,
            structurally_auto_admissible=False,
            lifecycle_state="TOMBSTONED",
            retired=True,
            notes="Normative v0.2 tombstone: do not rediscover without new authoritative GitHub restoration evidence.",
        ),
    )
    return ProviderAtlas(entries)
