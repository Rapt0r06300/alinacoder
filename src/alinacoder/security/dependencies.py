from __future__ import annotations

from dataclasses import dataclass
import re


class DependencyAdmissionError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class DependencyRequest:
    name: str
    version: str
    integrity: str | None
    source: str


_EXACT_VERSION = re.compile(r"^[0-9]+(?:\.[0-9A-Za-z._-]+)+$")
_SHA256 = re.compile(r"^sha256:[0-9a-fA-F]{64}$")


class DependencyAdmissionFirewall:
    def __init__(self, allowed_sources: set[str] | frozenset[str]) -> None:
        self.allowed_sources = frozenset(s.lower().rstrip(".") for s in allowed_sources)

    def admit(self, request: DependencyRequest) -> None:
        if not request.name.strip():
            raise DependencyAdmissionError("Dependency name is required")
        if request.source.lower().rstrip(".") not in self.allowed_sources:
            raise DependencyAdmissionError(f"Dependency source is not approved: {request.source}")
        if not _EXACT_VERSION.fullmatch(request.version) or any(ch in request.version for ch in "*<>=~^ "):
            raise DependencyAdmissionError("Dependency version must be exact and pinned")
        if request.integrity is None or not _SHA256.fullmatch(request.integrity):
            raise DependencyAdmissionError("Dependency requires a sha256 integrity pin")
