from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolSchema:
    name: str
    required: dict[str, type]
    mutating: bool = False
    allow_extra: bool = False


@dataclass(frozen=True)
class ToolCall:
    invocation_id: str
    tool_name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class EffectReceipt:
    invocation_id: str
    tool_name: str
    result: dict[str, Any]
    verified: bool
    result_hash: str


class ToolValidationError(RuntimeError):
    pass


class UnknownResultError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProcessReceipt:
    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False
