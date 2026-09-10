from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from .retrieval import HybridHit, HybridRetriever

_TOKEN = re.compile(r"[A-Za-z0-9_./:-]+", re.UNICODE)


def _tokens(text: str) -> set[str]:
    return {match.group(0).lower() for match in _TOKEN.finditer(str(text))}


@dataclass(frozen=True, slots=True)
class RetrievalContext:
    goal: str
    phase: str
    subtask: str
    paths: tuple[str, ...]
    failures: tuple[str, ...]
    constraints: tuple[str, ...]
    repo_state: str


@dataclass(frozen=True, slots=True)
class RankingCandidate:
    ref: str
    text: str
    base_score: float
    authority: int = 0
    fresh: bool = True
    evidence_valid: bool = True
    source: str = "memory"
    estimated_chars: int = 0


class PhaseAwareRanker:
    """Deterministic value score layered over existing retrieval safeguards."""

    def score(self, candidate: RankingCandidate, context: RetrievalContext) -> float:
        if not candidate.fresh or not candidate.evidence_valid:
            return -1.0
        text = _tokens(candidate.text + " " + candidate.ref)
        phase = _tokens(context.phase + " " + context.subtask)
        goal = _tokens(context.goal)
        paths = _tokens(" ".join(context.paths))
        failures = _tokens(" ".join(context.failures))
        constraints = _tokens(" ".join(context.constraints))
        phase_overlap = len(text & phase) / max(1, len(phase))
        goal_overlap = len(text & goal) / max(1, len(goal))
        path_overlap = len(text & paths) / max(1, len(paths))
        failure_overlap = len(text & failures) / max(1, len(failures))
        constraint_overlap = len(text & constraints) / max(1, len(constraints))
        authority = min(100, max(0, int(candidate.authority))) / 100.0
        size = candidate.estimated_chars or len(candidate.text)
        context_cost = min(1.0, size / 8000.0)
        return (
            float(candidate.base_score) * 0.30
            + phase_overlap * 0.18
            + goal_overlap * 0.12
            + path_overlap * 0.14
            + failure_overlap * 0.16
            + constraint_overlap * 0.04
            + authority * 0.08
            - context_cost * 0.02
        )


class PhaseAwareRetriever:
    def __init__(self, retriever: HybridRetriever, ranker: PhaseAwareRanker | None = None) -> None:
        self.retriever = retriever
        self.ranker = ranker or PhaseAwareRanker()

    def search(self, project_id: str, query: str, context: RetrievalContext, limit: int = 16) -> list[HybridHit]:
        base = self.retriever.retrieve(project_id, query, max(limit * 2, limit))
        scored: list[HybridHit] = []
        for hit in base:
            authority = 80 if hit.source == "repo" else 60 if hit.source == "memory" else 50
            value = self.ranker.score(
                RankingCandidate(hit.ref, hit.text, hit.score, authority=authority, fresh=True, source=hit.source),
                context,
            )
            if value >= 0:
                scored.append(HybridHit(hit.source, hit.ref, hit.text, value))
        # Diversity: round-robin through source families after relevance sort,
        # preserving strong hits while preventing one source from consuming the
        # entire prompt budget.
        scored.sort(key=lambda item: (-item.score, item.source, item.ref))
        selected: list[HybridHit] = []
        source_counts: dict[str, int] = {}
        per_source_soft_cap = max(2, limit // 2)
        for hit in scored:
            if len(selected) >= limit:
                break
            if source_counts.get(hit.source, 0) >= per_source_soft_cap:
                continue
            selected.append(hit)
            source_counts[hit.source] = source_counts.get(hit.source, 0) + 1
        if len(selected) < limit:
            used = {(hit.source, hit.ref) for hit in selected}
            selected.extend(hit for hit in scored if (hit.source, hit.ref) not in used) 
            selected = selected[:limit]
        return selected


@dataclass(frozen=True, slots=True)
class FoldedContext:
    decision: str
    evidence: tuple[str, ...]
    files: tuple[str, ...]
    rejected_hypotheses: tuple[str, ...]
    open_questions: tuple[str, ...]
    verification_state: str
    source_event_ids: tuple[str, ...]
    summary: str


class ContextFolder:
    """Create an actionable phase summary without mutating/deleting history."""

    def fold(
        self,
        history: Iterable[dict],
        *,
        decision: str,
        evidence: tuple[str, ...] | list[str],
        files: tuple[str, ...] | list[str],
        rejected_hypotheses: tuple[str, ...] | list[str],
        open_questions: tuple[str, ...] | list[str],
        verification_state: str,
    ) -> FoldedContext:
        events = [dict(item) for item in history]
        source_ids = tuple(str(item.get("event_id")) for item in events if item.get("event_id"))
        evidence_t = tuple(str(x) for x in evidence)
        files_t = tuple(str(x) for x in files)
        rejected_t = tuple(str(x) for x in rejected_hypotheses)
        questions_t = tuple(str(x) for x in open_questions)
        parts = [f"Decision: {decision}", f"Verification: {verification_state}"]
        if files_t:
            parts.append("Files: " + ", ".join(files_t))
        if evidence_t:
            parts.append("Evidence: " + ", ".join(evidence_t))
        if rejected_t:
            parts.append("Rejected: " + ", ".join(rejected_t))
        if questions_t:
            parts.append("Open: " + ", ".join(questions_t))
        return FoldedContext(
            str(decision), evidence_t, files_t, rejected_t, questions_t,
            str(verification_state), source_ids, "\n".join(parts),
        )
