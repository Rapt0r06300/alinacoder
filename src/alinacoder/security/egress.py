from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class EgressPolicy:
    allowed_domains: frozenset[str]

    def allows(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return False
        host = parsed.hostname.lower().rstrip(".")
        return any(host == allowed or host.endswith("." + allowed) for allowed in self.allowed_domains)
