from __future__ import annotations

import hashlib
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class ResearchEvidence:
    source_url: str
    content_hash: str
    observed_at: float
    expires_at: float
    citation: str

    @classmethod
    def from_document(cls, source_url: str, content: str, *, observed_at: float, ttl_seconds: float) -> "ResearchEvidence":
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        host = urlparse(source_url).netloc or source_url
        return cls(source_url, digest, observed_at, observed_at + max(0.0, ttl_seconds), f"source:{host}#{digest[:12]}")

    def is_fresh(self, now: float) -> bool:
        return self.observed_at <= now <= self.expires_at
