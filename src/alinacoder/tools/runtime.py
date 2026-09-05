from __future__ import annotations

import hashlib
import json
from typing import Any, Callable

from .models import EffectReceipt, ToolCall, ToolSchema, ToolValidationError


class ToolRuntime:
    def __init__(self) -> None:
        self._schemas: dict[str, ToolSchema] = {}
        self._receipts: dict[str, EffectReceipt] = {}

    def register(self, schema: ToolSchema) -> None:
        self._schemas[schema.name] = schema

    def _validate(self, call: ToolCall) -> ToolSchema:
        if call.tool_name not in self._schemas:
            raise ToolValidationError(f"unknown tool: {call.tool_name}")
        schema = self._schemas[call.tool_name]
        for key, expected_type in schema.required.items():
            if key not in call.arguments:
                raise ToolValidationError(f"missing required argument: {key}")
            if not isinstance(call.arguments[key], expected_type):
                raise ToolValidationError(f"invalid type for {key}")
        if not schema.allow_extra:
            unknown = set(call.arguments) - set(schema.required)
            if unknown:
                raise ToolValidationError(f"unknown arguments: {sorted(unknown)}")
        return schema

    def invoke(self, call: ToolCall, executor: Callable[[dict[str, Any]], dict[str, Any]]) -> EffectReceipt:
        if call.invocation_id in self._receipts:
            return self._receipts[call.invocation_id]
        self._validate(call)
        result = executor(dict(call.arguments))
        if not isinstance(result, dict):
            raise ToolValidationError("tool executor must return a dict")
        payload = json.dumps(result, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        receipt = EffectReceipt(
            invocation_id=call.invocation_id,
            tool_name=call.tool_name,
            result=result,
            verified=bool(result.get("ok", False)),
            result_hash=hashlib.sha256(payload).hexdigest(),
        )
        self._receipts[call.invocation_id] = receipt
        return receipt

    def receipt(self, invocation_id: str) -> EffectReceipt | None:
        return self._receipts.get(invocation_id)
