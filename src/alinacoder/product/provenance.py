from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProvenanceEvidence:
    commit_sha: str
    artifact_sha256: str
    provenance_verified: bool
    sbom_verified: bool
    signer_identity: str
    authenticode_verified: bool = False

    def as_dict(self) -> dict:
        return asdict(self)


class ReleaseAdmissionPolicy:
    """Fail-closed policy for RC and production release channels."""

    def __init__(self, *, channel: str) -> None:
        normalized = channel.strip().lower()
        if normalized not in {"rc", "production"}:
            raise ValueError("release channel must be rc or production")
        self.channel = normalized

    def admit(
        self,
        evidence: ProvenanceEvidence,
        *,
        expected_commit: str,
        expected_artifact_sha256: str,
    ) -> bool:
        if not expected_commit or not expected_artifact_sha256:
            return False
        if evidence.commit_sha != expected_commit:
            return False
        if evidence.artifact_sha256 != expected_artifact_sha256:
            return False
        if not evidence.provenance_verified or not evidence.sbom_verified:
            return False
        if not evidence.signer_identity.strip():
            return False
        if self.channel == "production" and not evidence.authenticode_verified:
            return False
        return True
