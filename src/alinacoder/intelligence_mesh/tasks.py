from __future__ import annotations

from enum import Enum
from typing import Any


class TaskClass(str, Enum):
    CONVERSATION = "conversation"
    INTENT = "intent"
    PLANNING = "planning"
    REPOSITORY = "repository"
    ARCHITECTURE = "architecture"
    CODE = "code"
    DEBUG = "debug"
    REVIEW = "review"
    VERIFICATION = "verification"
    SUMMARIZATION = "summarization"
    RESEARCH = "research"


class TaskClassifier:
    """Cheap deterministic first-pass classifier for inference routing."""

    _KEYWORDS: tuple[tuple[TaskClass, tuple[str, ...]], ...] = (
        (TaskClass.DEBUG, ("traceback", "failing test", "bug", "debug", "exception", "crash", "fix this error", "répare", "erreur")),
        (TaskClass.ARCHITECTURE, ("architecture", "design", "system design", "technical design", "conception")),
        (TaskClass.PLANNING, ("implementation plan", "plan d'implémentation", "roadmap", "plan the", "planifier")),
        (TaskClass.REVIEW, ("code review", "review this", "audit this patch", "relire", "revue de code")),
        (TaskClass.VERIFICATION, ("verify", "verification", "prove", "test evidence", "vérifie", "preuve")),
        (TaskClass.RESEARCH, ("research", "search the web", "documentation", "recherche", "cherche sur")),
        (TaskClass.SUMMARIZATION, ("summarize", "summary", "résume", "synthèse")),
        (TaskClass.REPOSITORY, ("repository", "repo", "git", "file tree", "symbol", "codebase", "dépôt")),
        (TaskClass.CODE, ("implement", "write code", "function", "class ", "refactor", "code", "implémente")),
        (TaskClass.INTENT, ("what do i mean", "interpret", "clarify intent", "intention", "comprends ma demande")),
    )

    def classify(self, messages: list[dict[str, str]], requirement: Any | None) -> TaskClass:
        text = " ".join(str(item.get("content", "")) for item in messages[-4:]).lower()
        # Architecture wins over planning when both are explicitly requested;
        # debugging wins over generic coding words because it is more specific.
        for task, keywords in self._KEYWORDS:
            if any(keyword in text for keyword in keywords):
                return task
        minimums = getattr(requirement, "minimums", {}) if requirement is not None else {}
        if isinstance(minimums, dict):
            if float(minimums.get("code", 0.0)) >= 0.7:
                return TaskClass.CODE
            if float(minimums.get("reasoning", 0.0)) >= 0.8:
                return TaskClass.PLANNING
        return TaskClass.CONVERSATION
