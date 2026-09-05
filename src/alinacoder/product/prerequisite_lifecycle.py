from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from .prerequisites import BootstrapState, ProvenanceError, ReleaseAsset


@dataclass(frozen=True)
class RollbackAction:
    component: str
    target_version: str
    source_url: str
    sha256: str


def managed_rollback_actions(state: BootstrapState) -> tuple[RollbackAction, ...]:
    actions: list[RollbackAction] = []
    for name, receipt in sorted(state.components.items()):
        if receipt.origin != "managed_by_alinacoder" or name.startswith("model:"):
            continue
        if not receipt.previous_version or not receipt.previous_source_url:
            continue
        if not re.fullmatch(r"[0-9a-fA-F]{64}", receipt.previous_sha256 or ""):
            continue
        parsed = urlparse(receipt.previous_source_url)
        if parsed.scheme != "https" or parsed.hostname != "github.com" or "/releases/download/" not in parsed.path:
            continue
        actions.append(
            RollbackAction(
                component=name,
                target_version=receipt.previous_version,
                source_url=receipt.previous_source_url,
                sha256=receipt.previous_sha256.lower(),
            )
        )
    return tuple(actions)


def rollback_managed(adapter, state: BootstrapState) -> tuple[str, ...]:
    restored: list[str] = []
    for action in managed_rollback_actions(state):
        policy = adapter._policy(action.component)
        name = policy.asset_name or f"{action.component}-{action.target_version}.exe"
        asset = ReleaseAsset(
            component=action.component,
            repository=policy.allowed_repository,
            version=action.target_version,
            name=name,
            url=action.source_url,
            sha256=action.sha256,
        )
        installer = adapter.download_verified(asset, require_authenticode=True)
        if action.component == "git":
            args = [str(installer), "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CURRENTUSER"]
        else:
            args = [str(installer), "/VERYSILENT", "/NORESTART"]
        code, _ = adapter._run(args, timeout=1800)
        if code not in (0, 3010):
            raise ProvenanceError(f"rollback failed for {action.component}: exit {code}")
        restored.append(action.component)
    return tuple(restored)
