from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any


class ToolInvocationError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ToolManifest:
    name: str
    schema: dict[str, Any]
    endpoint: str

    def fingerprint(self) -> str:
        payload = json.dumps({"name": self.name, "schema": self.schema, "endpoint": self.endpoint}, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


class ToolRegistry:
    def __init__(self) -> None:
        self._approved: dict[str, str] = {}

    def approve(self, manifest: ToolManifest) -> str:
        fingerprint = manifest.fingerprint()
        self._approved[manifest.name] = fingerprint
        return fingerprint

    def is_approved(self, manifest: ToolManifest) -> bool:
        return self._approved.get(manifest.name) == manifest.fingerprint()

    def validate_invocation(self, manifest: ToolManifest, arguments: dict[str, Any]) -> None:
        if not self.is_approved(manifest):
            raise ToolInvocationError("Tool manifest is not approved or has drifted")
        schema = manifest.schema
        if schema.get("type", "object") != "object":
            raise ToolInvocationError("Only object tool schemas are supported")
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        missing = sorted(required - arguments.keys())
        if missing:
            raise ToolInvocationError(f"Missing required arguments: {missing}")
        if schema.get("additionalProperties", True) is False:
            unknown = sorted(set(arguments) - set(properties))
            if unknown:
                raise ToolInvocationError(f"Unknown arguments are forbidden: {unknown}")
        for name, value in arguments.items():
            prop = properties.get(name)
            if not prop:
                continue
            expected = prop.get("type")
            if expected == "string" and not isinstance(value, str):
                raise ToolInvocationError(f"Argument {name} must be string")
            if expected == "boolean" and not isinstance(value, bool):
                raise ToolInvocationError(f"Argument {name} must be boolean")
            if expected == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
                raise ToolInvocationError(f"Argument {name} must be integer")
            if expected == "number" and (not isinstance(value, (int, float)) or isinstance(value, bool)):
                raise ToolInvocationError(f"Argument {name} must be number")
            if expected == "array" and not isinstance(value, list):
                raise ToolInvocationError(f"Argument {name} must be array")
            if expected == "object" and not isinstance(value, dict):
                raise ToolInvocationError(f"Argument {name} must be object")
            if "enum" in prop and value not in prop["enum"]:
                raise ToolInvocationError(f"Argument {name} is outside allowed enum")
