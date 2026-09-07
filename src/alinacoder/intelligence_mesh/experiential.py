from __future__ import annotations

from .provider_atlas import ProviderDefinition
from .providers import (
    HttpTransport,
    OpenAICompatibleProvider,
    ProviderError,
    ProviderModel,
    _decode_json,
    _int_or_none,
)


def _micro_usd_per_million_to_usd(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return None
    if amount < 0:
        return None
    return amount / 1_000_000.0


class ExperientialProvider(OpenAICompatibleProvider):
    """Experiential-specific catalog parser over the OpenAI-compatible wire API.

    Experiential's `/v1/models` pricing extension is expressed in micro-USD
    per million tokens. AlinaCoder normalizes it to USD per million tokens so
    sponsored-credit proof can preserve and compare the real list price.
    """

    def __init__(
        self,
        definition: ProviderDefinition,
        *,
        api_key: str,
        transport: HttpTransport | None = None,
        timeout: float = 45.0,
    ) -> None:
        if definition.provider_id != "experiential_gateway":
            raise ValueError("ExperientialProvider requires experiential_gateway definition")
        super().__init__(definition, api_key=api_key, transport=transport, timeout=timeout)

    def discover(self) -> list[ProviderModel]:
        if not self.definition.discovery_url:
            return []
        result = self._transport.request(
            "GET",
            self.definition.discovery_url,
            headers=self._headers(),
            payload=None,
            timeout=self._timeout,
        )
        if result.status >= 400:
            from .providers import _error_from_result

            raise _error_from_result(result, self.definition.provider_id, None)

        payload = _decode_json(result, self.definition.provider_id)
        rows = payload.get("data", payload.get("models", []))
        if not isinstance(rows, list):
            return []

        models: list[ProviderModel] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            model_id = str(row.get("id") or row.get("name") or "").strip()
            if not model_id:
                continue
            pricing = row.get("pricing") if isinstance(row.get("pricing"), dict) else {}
            prompt = _micro_usd_per_million_to_usd(pricing.get("input_micro_usd_per_million_tokens"))
            completion = _micro_usd_per_million_to_usd(pricing.get("output_micro_usd_per_million_tokens"))
            request_price = 0.0 if pricing and (prompt is not None or completion is not None) else None
            context = (
                _int_or_none(row.get("context_window_tokens"))
                or _int_or_none(row.get("context_window"))
                or _int_or_none(row.get("context_length"))
                or 0
            )
            lineage = str(row.get("canonical_slug") or row.get("model_lineage") or model_id).strip() or model_id
            models.append(
                ProviderModel(
                    provider_id=self.definition.provider_id,
                    model_id=model_id,
                    prompt_price=prompt,
                    completion_price=completion,
                    request_price=request_price,
                    context_tokens=context,
                    metadata={
                        "lineage": lineage,
                        "pricing_source": str(row.get("pricing_source") or "experiential-catalog"),
                        "retention": str(row.get("retention") or ""),
                    },
                )
            )
        return models
