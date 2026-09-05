from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable

from .models import EffectReceipt, ToolCall
from .runtime import ToolRuntime


class GovernedToolExecutor:
    def __init__(self, runtime: ToolRuntime) -> None:
        self.runtime = runtime

    def invoke(
        self,
        call: ToolCall,
        executor: Callable[[dict[str, Any]], dict[str, Any]],
        *,
        precondition: Callable[[dict[str, Any]], bool] | None = None,
        postcondition: Callable[[dict[str, Any]], bool] | None = None,
    ) -> EffectReceipt:
        if precondition is not None and not precondition(call.arguments):
            raise PermissionError("tool precondition failed")
        receipt = self.runtime.invoke(call, executor)
        if postcondition is not None and not postcondition(receipt.result):
            raise RuntimeError("tool postcondition failed")
        if not receipt.verified:
            raise RuntimeError("mutating effect is not verified")
        return receipt


@dataclass(frozen=True)
class MCPManifest:
    server_id: str
    tools: dict[str, dict[str, object]]

    @property
    def fingerprint(self) -> str:
        payload = json.dumps(self.tools, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


class MCPLifecycle:
    def __init__(self) -> None:
        self._approved_fingerprints: dict[str, str] = {}

    def approve(self, manifest: MCPManifest) -> None:
        self._approved_fingerprints[manifest.server_id] = manifest.fingerprint

    def validate(self, manifest: MCPManifest) -> bool:
        return self._approved_fingerprints.get(manifest.server_id) == manifest.fingerprint


@dataclass(frozen=True)
class CapabilityProjection:
    filesystem_roots: tuple[str, ...] = ()
    egress_hosts: tuple[str, ...] = ()
    secret_names: tuple[str, ...] = ()

    def allows_secret(self, name: str) -> bool:
        return name in self.secret_names

    def allows_egress(self, host: str) -> bool:
        return host in self.egress_hosts


class DeterministicReplayLedger:
    def __init__(self) -> None:
        self._events: list[tuple[str, str]] = []

    def append(self, invocation_id: str, result_hash: str) -> None:
        self._events.append((invocation_id, result_hash))

    def replay(self) -> tuple[tuple[str, str], ...]:
        return tuple(self._events)
