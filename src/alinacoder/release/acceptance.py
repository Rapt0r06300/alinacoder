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
    _DOMAIN_BY_FAMILY = {
        "COST": "provider_fabric", "GIT": "tools", "INTENT": "conversation",
        "STATE": "state_recovery", "EFFECT": "security", "VERIFY": "verification",
        "MEMORY": "memory_repo", "PROVIDER": "provider_fabric", "RECOVERY": "state_recovery",
        "SPEC": "bootstrap",
    }
    _EVIDENCE_BY_DOMAIN = {
        "bootstrap": "core", "state_recovery": "core", "security": "core", "memory_repo": "core",
        "conversation": "desktop_e2e", "provider_fabric": "core", "tools": "desktop_e2e",
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
            rows.append(TraceabilityRow(rule_id, domain, code_path, test_path, self._EVIDENCE_BY_DOMAIN[domain]))
        return RuleTraceabilityReport(tuple(rows), tuple(sorted(unknown)))


@dataclass(frozen=True)
class AcceptanceCaseEvidence:
    case_id: str
    verdict: str
    fresh: bool
    source: str


@dataclass(frozen=True)
class SpecAcceptanceMatrixReport:
    passed: bool
    missing: tuple[str, ...]
    invalid: tuple[str, ...]
    unknown: tuple[str, ...]
    passed_cases: int
    required_cases: int


class SpecAcceptanceMatrix:
    families: dict[str, tuple[str, ...]] = {
        "conversation": (
            "evolving_intent", "correction_negation", "branch_isolation", "deictic_visible_references",
            "clarification_stopping", "user_preference_revision", "repeated_correction_no_repeat_violation",
            "french_noisy_hesitant_input",
        ),
        "repository_engineering": (
            "multi_file_bug_repair", "feature_addition", "dependency_sensitive_refactor",
            "implicit_requirement_recovery", "test_generation_use", "regression_detection",
            "partial_failure_recovery", "long_horizon_no_premature_stop",
        ),
        "control_safety": (
            "stale_response_rejection", "cancellation_fencing", "stale_patch_rejection", "effect_idempotency",
            "untrusted_repo_instructions_are_data", "memory_promotion_governance", "exact_main_enforcement",
        ),
        "provider_fabric": (
            "free_route_disappears", "quota_exhausted", "model_alias_changes", "provider_timeout",
            "same_lineage_failover", "cognitive_failover", "no_eligible_cloud_route", "local_only_fallback",
            "zero_paid_calls",
        ),
        "continuity": (
            "process_crash", "restart_during_mission", "model_switch", "user_correction_in_flight",
            "partial_stream_failure", "recovery_without_duplicate_effect",
        ),
        "desktop_ux": (
            "clean_first_run", "ordinary_chat_without_advanced_panels", "pause_resume", "all_stop",
            "plan_artifact_selection", "targeted_edit_continue", "verification_visibility", "low_idle_resource_use",
        ),
    }

    def required_case_ids(self) -> tuple[str, ...]:
        return tuple(f"{family}.{case}" for family, cases in self.families.items() for case in cases)

    def evaluate(self, evidences: list[AcceptanceCaseEvidence] | tuple[AcceptanceCaseEvidence, ...]) -> SpecAcceptanceMatrixReport:
        required = self.required_case_ids()
        required_set = set(required)
        by_case: dict[str, AcceptanceCaseEvidence] = {}
        unknown: set[str] = set()
        for evidence in evidences:
            if evidence.case_id not in required_set:
                unknown.add(evidence.case_id)
                continue
            by_case[evidence.case_id] = evidence
        missing = tuple(case_id for case_id in required if case_id not in by_case)
        invalid = tuple(
            case_id for case_id in required
            if case_id in by_case and (
                by_case[case_id].verdict != "PASS" or not by_case[case_id].fresh or not by_case[case_id].source
            )
        )
        passed_cases = sum(
            1 for case_id in required
            if case_id in by_case and by_case[case_id].verdict == "PASS" and by_case[case_id].fresh and by_case[case_id].source
        )
        unknown_tuple = tuple(sorted(unknown))
        return SpecAcceptanceMatrixReport(
            passed=not missing and not invalid and not unknown_tuple,
            missing=missing, invalid=invalid, unknown=unknown_tuple,
            passed_cases=passed_cases, required_cases=len(required),
        )


@dataclass(frozen=True)
class AcceptanceCoverageRow:
    case_id: str
    path: str
    test_name: str = ""
    evidence_key: str = ""


@dataclass(frozen=True)
class AcceptanceCoverageReport:
    complete: bool
    rows: tuple[AcceptanceCoverageRow, ...]
    gaps: tuple[str, ...]
    unknown: tuple[str, ...]
    duplicates: tuple[str, ...]
    covered_cases: int


class AcceptanceCoverageCatalog:
    def __init__(self, repo_root: Path | str, relative_path: str = "docs/release/acceptance-coverage-v0.2.json") -> None:
        self.repo_root = Path(repo_root)
        self.path = self.repo_root / relative_path

    def _rows(self) -> tuple[AcceptanceCoverageRow, ...]:
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return tuple(
            AcceptanceCoverageRow(
                case_id=str(item["case_id"]), path=str(item["path"]),
                test_name=str(item.get("test_name", "")), evidence_key=str(item.get("evidence_key", "")),
            )
            for item in payload.get("cases", [])
        )

    def validate(self, matrix: SpecAcceptanceMatrix) -> AcceptanceCoverageReport:
        rows = self._rows()
        required = set(matrix.required_case_ids())
        counts: dict[str, int] = {}
        invalid: set[str] = set()
        for row in rows:
            counts[row.case_id] = counts.get(row.case_id, 0) + 1
            target = self.repo_root / row.path
            if not target.exists() or not (row.test_name or row.evidence_key):
                invalid.add(row.case_id)
                continue
            if row.test_name:
                try:
                    text = target.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    invalid.add(row.case_id)
                    continue
                if f"def {row.test_name}(" not in text:
                    invalid.add(row.case_id)
        known = {row.case_id for row in rows}
        gaps = tuple(sorted((required - known) | invalid))
        unknown = tuple(sorted(known - required))
        duplicates = tuple(sorted(case_id for case_id, count in counts.items() if count > 1))
        complete = not gaps and not unknown and not duplicates and len(known) == len(required)
        return AcceptanceCoverageReport(complete, rows, gaps, unknown, duplicates, len(known & required))


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
    def __init__(
        self,
        traceability: RuleTraceabilityReport,
        required: tuple[str, ...] | set[str],
        *,
        commit_sha: str,
        artifact_sha256: str,
        acceptance_matrix: SpecAcceptanceMatrix | None = None,
    ) -> None:
        self.traceability = traceability
        self.required = tuple(required)
        self.commit_sha = commit_sha
        self.artifact_sha256 = artifact_sha256
        self.acceptance_matrix = acceptance_matrix

    def evaluate(
        self,
        evidences: list[AcceptanceEvidence] | tuple[AcceptanceEvidence, ...],
        acceptance_case_evidences: list[AcceptanceCaseEvidence] | tuple[AcceptanceCaseEvidence, ...] = (),
    ) -> FinalAcceptanceResult:
        by_name = {evidence.name: evidence for evidence in evidences}
        missing: list[str] = []
        failures: list[str] = []
        if not self.traceability.complete:
            failures.append("incomplete_rule_traceability")
        for name in self.required:
            evidence = by_name.get(name)
            valid = bool(
                evidence and evidence.verdict == "PASS" and evidence.fresh
                and evidence.commit_sha == self.commit_sha and evidence.artifact_sha256 == self.artifact_sha256
            )
            if not valid:
                missing.append(name)
        final_audit = by_name.get("final_audit")
        if not final_audit or not final_audit.independent:
            failures.append("independent_final_audit")
        if self.acceptance_matrix is None:
            failures.append("missing_spec_acceptance_matrix")
        else:
            matrix_report = self.acceptance_matrix.evaluate(acceptance_case_evidences)
            if not matrix_report.passed:
                failures.append("incomplete_spec_acceptance_matrix")
        ready = not missing and not failures
        return FinalAcceptanceResult(ready, tuple(missing), tuple(failures))


class ReleaseBundle:
    REQUIRED = {
        "AlinaCoder.exe", "AlinaCoderSetup.exe", "release-manifest.json", "sbom.spdx.json",
        "USER_GUIDE.md", "OPERATIONS.md",
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
    matrix = SpecAcceptanceMatrix()
    coverage = AcceptanceCoverageCatalog(args.repo_root).validate(matrix)
    report = {
        "runtime_v0_2_ready": False,
        "bundle_complete": bundle.complete(), "traceability_complete": traceability.complete,
        "acceptance_coverage_complete": coverage.complete, "acceptance_cases": len(matrix.required_case_ids()),
        "rule_count": traceability.rule_count, "unknown_rule_families": list(traceability.unknown_families),
        "artifact_exists": artifact.exists(), "setup_exists": setup.exists(), "commit_sha": args.commit_sha,
    }
    if artifact.exists() and bundle.complete():
        report["artifact_sha256"] = sha256_file(artifact)
    print(json.dumps(report, sort_keys=True))
    return 0 if bundle.complete() and artifact.exists() and setup.exists() and traceability.complete and coverage.complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
