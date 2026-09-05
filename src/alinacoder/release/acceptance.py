from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


class TraceabilityMatrix:
    def __init__(self, *, required_domains: set[str]) -> None:
        self.required_domains = set(required_domains)
        self.entries: dict[str, tuple[str, str]] = {}

    def cover(self, domain: str, code_path: str, test_path: str) -> None:
        if not code_path or not test_path:
            raise ValueError("traceability requires code and test")
        self.entries[domain] = (code_path, test_path)

    def complete(self) -> bool:
        return self.required_domains.issubset(self.entries)

    def gaps(self) -> set[str]:
        return self.required_domains - self.entries.keys()


@dataclass(frozen=True)
class TraceabilityRow:
    rule_id: str
    domain: str
    code_path: str
    test_path: str
    evidence_name: str


@dataclass(frozen=True)
class RuleTraceabilityReport:
    rows: tuple[TraceabilityRow, ...]
    unknown_families: tuple[str, ...]

    @property
    def rule_count(self) -> int:
        return len(self.rows)

    @property
    def complete(self) -> bool:
        return bool(self.rows) and not self.unknown_families


class RuleTraceabilityBuilder:
    """Build traceability for the constitutional rules declared active by the normative manifest."""

    _DOMAIN_BY_FAMILY = {
        "COST": "provider_fabric",
        "GIT": "tools",
        "INTENT": "conversation",
        "STATE": "state_recovery",
        "EFFECT": "security",
        "VERIFY": "verification",
        "MEMORY": "memory_repo",
        "PROVIDER": "provider_fabric",
        "RECOVERY": "state_recovery",
        "SPEC": "bootstrap",
    }

    _EVIDENCE_BY_DOMAIN = {
        "bootstrap": "core",
        "state_recovery": "core",
        "security": "core",
        "memory_repo": "core",
        "conversation": "desktop_e2e",
        "provider_fabric": "core",
        "tools": "desktop_e2e",
        "verification": "final_audit",
    }

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root)

    def build(self) -> RuleTraceabilityReport:
        manifest_path = self.repo_root / "docs/superpowers/specs/2026-09-04-alinacoder-v0.2-normative-manifest.json"
        trace_path = self.repo_root / "docs/release/traceability-v0.2.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        domains = json.loads(trace_path.read_text(encoding="utf-8"))["domains"]
        rows: list[TraceabilityRow] = []
        unknown: set[str] = set()
        for rule_id in manifest.get("constitutional_invariants", []):
            parts = rule_id.split(".")
            family = parts[1] if len(parts) > 1 else ""
            domain = self._DOMAIN_BY_FAMILY.get(family)
            if not domain or domain not in domains:
                unknown.add(family or rule_id)
                continue
            code_path, test_path = domains[domain]
            rows.append(
                TraceabilityRow(
                    rule_id=rule_id,
                    domain=domain,
                    code_path=code_path,
                    test_path=test_path,
                    evidence_name=self._EVIDENCE_BY_DOMAIN[domain],
                )
            )
        return RuleTraceabilityReport(tuple(rows), tuple(sorted(unknown)))


@dataclass(frozen=True)
class AcceptanceEvidence:
    name: str
    verdict: str
    commit_sha: str
    artifact_sha256: str
    fresh: bool
    source: str = "runtime"
    independent: bool = False


class AcceptanceGate:
    def __init__(self, *, required: set[str], commit_sha: str, artifact_sha256: str) -> None:
        self.required = set(required)
        self.commit_sha = commit_sha
        self.artifact_sha256 = artifact_sha256
        self._evidence: dict[str, AcceptanceEvidence] = {}

    def add(self, evidence: AcceptanceEvidence) -> None:
        self._evidence[evidence.name] = evidence

    def runtime_v0_2_ready(self) -> bool:
        for name in self.required:
            evidence = self._evidence.get(name)
            if not evidence or evidence.verdict != "PASS" or not evidence.fresh:
                return False
            if evidence.commit_sha != self.commit_sha or evidence.artifact_sha256 != self.artifact_sha256:
                return False
        return True


@dataclass(frozen=True)
class FinalAcceptanceResult:
    runtime_v0_2_ready: bool
    missing_or_invalid_evidence: tuple[str, ...]
    failures: tuple[str, ...]


class FinalAcceptanceGate:
    """Fail-closed release gate requiring exact-state evidence and an independent final audit."""

    def __init__(
        self,
        traceability: RuleTraceabilityReport,
        required: tuple[str, ...] | set[str],
        *,
        commit_sha: str,
        artifact_sha256: str,
    ) -> None:
        self.traceability = traceability
        self.required = tuple(required)
        self.commit_sha = commit_sha
        self.artifact_sha256 = artifact_sha256

    def evaluate(self, evidences: list[AcceptanceEvidence] | tuple[AcceptanceEvidence, ...]) -> FinalAcceptanceResult:
        by_name = {evidence.name: evidence for evidence in evidences}
        missing: list[str] = []
        failures: list[str] = []
        if not self.traceability.complete:
            failures.append("incomplete_rule_traceability")
        for name in self.required:
            evidence = by_name.get(name)
            valid = bool(
                evidence
                and evidence.verdict == "PASS"
                and evidence.fresh
                and evidence.commit_sha == self.commit_sha
                and evidence.artifact_sha256 == self.artifact_sha256
            )
            if not valid:
                missing.append(name)
        final_audit = by_name.get("final_audit")
        if not final_audit or not final_audit.independent:
            failures.append("independent_final_audit")
        ready = not missing and not failures
        return FinalAcceptanceResult(ready, tuple(missing), tuple(failures))


class ReleaseBundle:
    REQUIRED = {
        "AlinaCoder.exe",
        "AlinaCoderSetup.exe",
        "release-manifest.json",
        "sbom.spdx.json",
        "USER_GUIDE.md",
        "OPERATIONS.md",
    }

    def __init__(self, files: set[str]) -> None:
        self.files = set(files)

    def complete(self) -> bool:
        return self.REQUIRED.issubset(self.files)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--commit-sha", default="")
    args = parser.parse_args(argv)
    artifact = args.artifact_dir / "AlinaCoder.exe"
    setup = args.artifact_dir / "AlinaCoderSetup.exe"
    files = {item.name for item in args.artifact_dir.iterdir()} if args.artifact_dir.exists() else set()
    for doc in ["USER_GUIDE.md", "OPERATIONS.md"]:
        if (args.repo_root / "docs" / doc).exists():
            files.add(doc)
    bundle = ReleaseBundle(files)
    traceability = RuleTraceabilityBuilder(args.repo_root).build()
    report = {
        "runtime_v0_2_ready": False,
        "bundle_complete": bundle.complete(),
        "traceability_complete": traceability.complete,
        "rule_count": traceability.rule_count,
        "unknown_rule_families": list(traceability.unknown_families),
        "artifact_exists": artifact.exists(),
        "setup_exists": setup.exists(),
        "commit_sha": args.commit_sha,
    }
    if artifact.exists() and bundle.complete():
        report["artifact_sha256"] = sha256_file(artifact)
    print(json.dumps(report, sort_keys=True))
    return 0 if bundle.complete() and artifact.exists() and setup.exists() and traceability.complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
