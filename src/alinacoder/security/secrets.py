from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class SecretHandle:
    name: str

    def __str__(self) -> str:
        return f"secret://{self.name}"


class InMemorySecretStore:
    def __init__(self) -> None:
        self._secrets: dict[str, str] = {}

    def put(self, name: str, secret: str) -> SecretHandle:
        if not name or not secret:
            raise ValueError("Secret name/value cannot be empty")
        self._secrets[name] = secret
        return SecretHandle(name)

    def _get(self, handle: SecretHandle) -> str:
        try:
            return self._secrets[handle.name]
        except KeyError as exc:
            raise KeyError(f"Unknown secret handle: {handle}") from exc


class SecretBroker:
    def __init__(self, store: InMemorySecretStore) -> None:
        self._store = store

    def use(self, handle: SecretHandle, operation: Callable[[str], T]) -> T:
        secret = self._store._get(handle)
        result = operation(secret)
        if isinstance(result, str) and secret in result:
            raise ValueError("Secret-bearing result cannot leave SecretBroker")
        return result


def redact_secrets(text: str, secrets: list[str] | tuple[str, ...]) -> str:
    redacted = text
    for secret in sorted((s for s in secrets if s), key=len, reverse=True):
        redacted = redacted.replace(secret, "[REDACTED]")
    return redacted
