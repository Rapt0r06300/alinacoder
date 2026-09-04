from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any


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
