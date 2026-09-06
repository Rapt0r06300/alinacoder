from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .provider_atlas import ProviderDefinition


@dataclass(frozen=True, slots=True)
class HttpResult:
    status: int
    headers: dict[str, str]
    body: bytes


class HttpTransport(Protocol):
    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        payload: dict | None,
        timeout: float,
    ) -> HttpResult: ...


class UrllibTransport:
    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        payload: dict | None,
        timeout: float,
    ) -> HttpResult:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(url, data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=timeout) as response:
                return HttpResult(
                    status=int(getattr(response, "status", 200)),
                    headers={str(k).lower(): str(v) for k, v in response.headers.items()},
                    body=response.read(),
                )
        except HTTPError as exc:
            return HttpResult(
                status=int(exc.code),
                headers={str(k).lower(): str(v) for k, v in exc.headers.items()},
                body=exc.read(),
            )
        except URLError as exc:
            raise ProviderError(
                "UNAVAILABLE",
                provider_id="transport",
                model_id=None,
                retryable=True,
                metadata={"detail": str(exc.reason)},
            ) from exc


@dataclass(frozen=True, slots=True)
class ProviderModel:
    provider_id: str
    model_id: str
    prompt_price: float | None = None
    completion_price: float | None = None
    request_price: float | None = None
    context_tokens: int = 0
    capabilities: dict[str, float] = field(default_factory=lambda: {"reasoning": 0.5, "code": 0.5})
    quality_hint: float = 0.5
    quota_remaining: int | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def zero_price(self) -> bool:
        prices = (self.prompt_price, self.completion_price, self.request_price)
        return all(value is not None and float(value) == 0.0 for value in prices)


@dataclass(frozen=True, slots=True)
class ProviderResponse:
    text: str
    provider_id: str
    model_id: str
    quota_remaining: int | None = None
    metadata: dict[str, object] = field(default_factory=dict)


class ProviderError(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        provider_id: str,
        model_id: str | None,
        retryable: bool,
        status: int | None = None,
        metadata: dict[str, object] | None = None,
    ) -> None:
        super().__init__(f"{provider_id}:{model_id or '-'}:{code}")
        self.code = code
        self.provider_id = provider_id
        self.model_id = model_id
        self.retryable = bool(retryable)
        self.status = status
        self.metadata = dict(metadata or {})


class ZeroCostProvider(Protocol):
    definition: ProviderDefinition

    def discover(self) -> list[ProviderModel]: ...

    def complete(self, model_id: str, messages: list[dict[str, str]]) -> ProviderResponse: ...


def _decode_json(result: HttpResult, provider_id: str, model_id: str | None = None) -> dict:
    try:
        value = json.loads(result.body.decode("utf-8", errors="replace") or "{}")
    except json.JSONDecodeError as exc:
        raise ProviderError(
            "INVALID_RESPONSE",
            provider_id=provider_id,
            model_id=model_id,
            retryable=result.status >= 500,
            status=result.status,
        ) from exc
    if not isinstance(value, dict):
        raise ProviderError(
            "INVALID_RESPONSE",
            provider_id=provider_id,
            model_id=model_id,
            retryable=False,
            status=result.status,
        )
    return value


def _float_or_none(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _int_or_none(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _lower_headers(headers: dict[str, str]) -> dict[str, str]:
    return {str(key).lower(): str(value) for key, value in headers.items()}


def _quota_remaining(headers: dict[str, str]) -> int | None:
    lowered = _lower_headers(headers)
    for key in (
        "x-ratelimit-remaining-requests",
        "x-ratelimit-remaining-requests-day",
        "ratelimit-remaining",
    ):
        if key in lowered:
            return _int_or_none(lowered[key])
    return None


def _error_from_result(result: HttpResult, provider_id: str, model_id: str | None) -> ProviderError:
    headers = _lower_headers(result.headers)
    metadata: dict[str, object] = {}
    if "retry-after" in headers:
        metadata["retry_after"] = headers["retry-after"]
    if result.status == 429:
        code, retryable = "QUOTA_EXHAUSTED", True
    elif result.status == 402:
        code, retryable = "BILLING_BLOCKED", False
    elif result.status in {401, 403}:
        code, retryable = "AUTH_REQUIRED", False
    elif result.status >= 500:
        code, retryable = "UNAVAILABLE", True
    else:
        code, retryable = "REQUEST_REJECTED", False
    return ProviderError(
        code,
        provider_id=provider_id,
        model_id=model_id,
        retryable=retryable,
        status=result.status,
        metadata=metadata,
    )


class OpenAICompatibleProvider:
    def __init__(
        self,
        definition: ProviderDefinition,
        *,
        api_key: str | None = None,
        transport: HttpTransport | None = None,
        timeout: float = 45.0,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        if definition.protocol != "openai_chat":
            raise ValueError("provider definition is not OpenAI-compatible")
        self.definition = definition
        self._api_key = str(api_key or "")
        self._transport = transport or UrllibTransport()
        self._timeout = max(1.0, float(timeout))
        self._extra_headers = dict(extra_headers or {})

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        headers.update(self._extra_headers)
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

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
            prompt = _float_or_none(pricing.get("prompt", pricing.get("input")))
            completion = _float_or_none(pricing.get("completion", pricing.get("output")))
            request_price = _float_or_none(pricing.get("request", 0 if pricing else None))
            context = _int_or_none(row.get("context_length", row.get("context_window"))) or 0
            models.append(
                ProviderModel(
                    provider_id=self.definition.provider_id,
                    model_id=model_id,
                    prompt_price=prompt,
                    completion_price=completion,
                    request_price=request_price,
                    context_tokens=context,
                    metadata={"raw_provider_id": row.get("canonical_slug") or row.get("owned_by") or ""},
                )
            )
        return models

    def complete(self, model_id: str, messages: list[dict[str, str]]) -> ProviderResponse:
        if not self.definition.base_url:
            raise ProviderError(
                "CONFIG_REQUIRED",
                provider_id=self.definition.provider_id,
                model_id=model_id,
                retryable=False,
            )
        result = self._transport.request(
            "POST",
            self.definition.base_url.rstrip("/") + "/chat/completions",
            headers=self._headers(),
            payload={"model": model_id, "messages": list(messages), "stream": False},
            timeout=self._timeout,
        )
        if result.status >= 400:
            raise _error_from_result(result, self.definition.provider_id, model_id)
        payload = _decode_json(result, self.definition.provider_id, model_id)
        try:
            content = payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(
                "INVALID_RESPONSE",
                provider_id=self.definition.provider_id,
                model_id=model_id,
                retryable=False,
                status=result.status,
            ) from exc
        if isinstance(content, list):
            text = "".join(str(part.get("text", "")) for part in content if isinstance(part, dict))
        else:
            text = str(content or "")
        if not text.strip():
            raise ProviderError(
                "EMPTY_RESPONSE",
                provider_id=self.definition.provider_id,
                model_id=model_id,
                retryable=False,
                status=result.status,
            )
        headers = _lower_headers(result.headers)
        metadata: dict[str, object] = {}
        for key in ("x-ratelimit-reset", "x-ratelimit-reset-requests", "x-ratelimit-reset-tokens"):
            if key in headers:
                metadata[key] = headers[key]
        return ProviderResponse(
            text=text,
            provider_id=self.definition.provider_id,
            model_id=model_id,
            quota_remaining=_quota_remaining(result.headers),
            metadata=metadata,
        )


class GeminiProvider:
    def __init__(
        self,
        definition: ProviderDefinition,
        *,
        api_key: str,
        transport: HttpTransport | None = None,
        timeout: float = 45.0,
    ) -> None:
        if definition.protocol != "gemini":
            raise ValueError("provider definition is not Gemini-native")
        self.definition = definition
        self._api_key = str(api_key or "")
        self._transport = transport or UrllibTransport()
        self._timeout = max(1.0, float(timeout))

    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json", "Accept": "application/json", "x-goog-api-key": self._api_key}

    def discover(self) -> list[ProviderModel]:
        if not self.definition.base_url:
            return []
        result = self._transport.request(
            "GET",
            self.definition.base_url.rstrip("/") + "/models",
            headers=self._headers(),
            payload=None,
            timeout=self._timeout,
        )
        if result.status >= 400:
            raise _error_from_result(result, self.definition.provider_id, None)
        payload = _decode_json(result, self.definition.provider_id)
        rows = payload.get("models", [])
        models: list[ProviderModel] = []
        if isinstance(rows, list):
            for row in rows:
                if not isinstance(row, dict):
                    continue
                raw_name = str(row.get("name", ""))
                model_id = raw_name.split("/", 1)[-1]
                methods = row.get("supportedGenerationMethods", [])
                if model_id and (not methods or "generateContent" in methods):
                    models.append(
                        ProviderModel(
                            provider_id=self.definition.provider_id,
                            model_id=model_id,
                            context_tokens=_int_or_none(row.get("inputTokenLimit")) or 0,
                            metadata={"output_token_limit": _int_or_none(row.get("outputTokenLimit")) or 0},
                        )
                    )
        return models

    def complete(self, model_id: str, messages: list[dict[str, str]]) -> ProviderResponse:
        if not self.definition.base_url:
            raise ProviderError("CONFIG_REQUIRED", provider_id=self.definition.provider_id, model_id=model_id, retryable=False)
        contents = []
        for message in messages:
            role = "model" if message.get("role") == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": str(message.get("content", ""))}]})
        result = self._transport.request(
            "POST",
            self.definition.base_url.rstrip("/") + f"/models/{model_id}:generateContent",
            headers=self._headers(),
            payload={"contents": contents},
            timeout=self._timeout,
        )
        if result.status >= 400:
            raise _error_from_result(result, self.definition.provider_id, model_id)
        payload = _decode_json(result, self.definition.provider_id, model_id)
        try:
            parts = payload["candidates"][0]["content"]["parts"]
            text = "".join(str(part.get("text", "")) for part in parts if isinstance(part, dict))
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("INVALID_RESPONSE", provider_id=self.definition.provider_id, model_id=model_id, retryable=False) from exc
        if not text.strip():
            raise ProviderError("EMPTY_RESPONSE", provider_id=self.definition.provider_id, model_id=model_id, retryable=False)
        return ProviderResponse(text=text, provider_id=self.definition.provider_id, model_id=model_id, quota_remaining=_quota_remaining(result.headers))


class OllamaProvider:
    def __init__(
        self,
        definition: ProviderDefinition,
        *,
        transport: HttpTransport | None = None,
        timeout: float = 120.0,
    ) -> None:
        if definition.protocol != "ollama":
            raise ValueError("provider definition is not Ollama-local")
        self.definition = definition
        self._transport = transport or UrllibTransport()
        self._timeout = max(1.0, float(timeout))

    def discover(self) -> list[ProviderModel]:
        url = self.definition.discovery_url or (str(self.definition.base_url).rstrip("/") + "/api/tags")
        result = self._transport.request("GET", url, headers={"Accept": "application/json"}, payload=None, timeout=self._timeout)
        if result.status >= 400:
            raise _error_from_result(result, self.definition.provider_id, None)
        payload = _decode_json(result, self.definition.provider_id)
        rows = payload.get("models", [])
        models: list[ProviderModel] = []
        if isinstance(rows, list):
            for row in rows:
                if not isinstance(row, dict):
                    continue
                model_id = str(row.get("name") or row.get("model") or "").strip()
                if model_id:
                    models.append(
                        ProviderModel(
                            provider_id=self.definition.provider_id,
                            model_id=model_id,
                            prompt_price=0.0,
                            completion_price=0.0,
                            request_price=0.0,
                            metadata={"size": row.get("size", 0)},
                        )
                    )
        return models

    def complete(self, model_id: str, messages: list[dict[str, str]]) -> ProviderResponse:
        if not self.definition.base_url:
            raise ProviderError("CONFIG_REQUIRED", provider_id=self.definition.provider_id, model_id=model_id, retryable=False)
        result = self._transport.request(
            "POST",
            self.definition.base_url.rstrip("/") + "/api/chat",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            payload={"model": model_id, "messages": list(messages), "stream": False, "think": False},
            timeout=self._timeout,
        )
        if result.status >= 400:
            raise _error_from_result(result, self.definition.provider_id, model_id)
        payload = _decode_json(result, self.definition.provider_id, model_id)
        try:
            text = str(payload["message"]["content"])
        except (KeyError, TypeError) as exc:
            raise ProviderError("INVALID_RESPONSE", provider_id=self.definition.provider_id, model_id=model_id, retryable=False) from exc
        if not text.strip():
            raise ProviderError("EMPTY_RESPONSE", provider_id=self.definition.provider_id, model_id=model_id, retryable=False)
        return ProviderResponse(text=text, provider_id=self.definition.provider_id, model_id=model_id)
