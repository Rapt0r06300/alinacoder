from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import tempfile
from typing import Protocol

from alinacoder.security.platform_secrets import DPAPIProtector


class SecretProtector(Protocol):
    def protect(self, plaintext: bytes) -> bytes: ...
    def unprotect(self, ciphertext: bytes) -> bytes: ...


class ProviderCredentialVault:
    """Small local provider-key vault; persisted JSON contains ciphertext only."""

    def __init__(self, path: Path | str, *, protector: SecretProtector | None = None) -> None:
        self.path = Path(path)
        if protector is None:
            if os.name != "nt":
                raise OSError("provider credential vault requires Windows DPAPI unless a protector is injected")
            protector = DPAPIProtector(machine_scope=False)
        self._protector = protector

    def _load(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("provider credential vault is unreadable") from exc
        if not isinstance(payload, dict) or int(payload.get("schema_version", 0)) != 1:
            raise ValueError("unsupported provider credential vault schema")
        providers = payload.get("providers", {})
        if not isinstance(providers, dict):
            raise ValueError("provider credential vault providers must be an object")
        return {str(key): str(value) for key, value in providers.items() if str(key) and str(value)}

    def _write(self, providers: dict[str, str]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version": 1, "providers": dict(sorted(providers.items()))}
        encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        fd, temp_name = tempfile.mkstemp(prefix=self.path.name + ".", suffix=".tmp", dir=str(self.path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, self.path)
        finally:
            try:
                Path(temp_name).unlink(missing_ok=True)
            except OSError:
                pass

    def put(self, provider_id: str, secret: str) -> None:
        provider = str(provider_id).strip()
        value = str(secret).strip()
        if not provider or not value:
            raise ValueError("provider_id and secret are required")
        protected = self._protector.protect(value.encode("utf-8"))
        providers = self._load()
        providers[provider] = base64.b64encode(protected).decode("ascii")
        self._write(providers)

    def get(self, provider_id: str) -> str | None:
        encoded = self._load().get(str(provider_id).strip())
        if not encoded:
            return None
        try:
            protected = base64.b64decode(encoded.encode("ascii"), validate=True)
            plaintext = self._protector.unprotect(protected)
            return plaintext.decode("utf-8")
        except Exception as exc:
            raise ValueError("provider credential cannot be decrypted") from exc

    def delete(self, provider_id: str) -> None:
        providers = self._load()
        providers.pop(str(provider_id).strip(), None)
        self._write(providers)

    def has(self, provider_id: str) -> bool:
        return str(provider_id).strip() in self._load()

    def providers(self) -> tuple[str, ...]:
        return tuple(sorted(self._load()))
