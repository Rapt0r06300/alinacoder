from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class ReplayCase:
    case_id: str
    category: str
    turns: tuple[str, ...]
    expected: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ReplayReport:
    total: int
    passed: int
    failed: int
    category_counts: dict[str, int]
    failure_ids: tuple[str, ...]


class ConversationReplayCorpus:
    CATEGORIES = (
        "correction",
        "pronoun_reference",
        "multi_selection_ambiguity",
        "continuation",
        "negation",
        "scope_priority",
        "interruption",
        "partial_asr",
        "noisy_french",
        "mixed_technical_language",
        "stale_reference",
        "restart",
        "message_during_work",
        "stop_scope",
        "undo",
        "long_constraint_retention",
        "false_memory_rejection",
        "causal_invalidation",
    )

    @staticmethod
    def _id(seed: str, category: str, index: int) -> str:
        digest = hashlib.sha256(f"{seed}:{category}:{index}".encode("utf-8")).hexdigest()[:16]
        return f"replay:{category}:{index:03d}:{digest}"

    @classmethod
    def _case(cls, seed: str, category: str, index: int) -> ReplayCase:
        marker = f"R{index:03d}"
        if category == "correction":
            turns = (f"Répare l'installer {marker}", "Non, je parle du model bridge.")
            expected = {"old_target": "installer", "new_target": "model bridge", "preserve_unrelated": True}
        elif category == "pronoun_reference":
            turns = (f"Sélectionne artifact-{marker}", "Corrige ça.")
            expected = {"reference": f"artifact-{marker}"}
        elif category == "multi_selection_ambiguity":
            turns = (f"Sélectionne a-{marker} et b-{marker}", "Supprime ça.")
            expected = {"ambiguous": True, "reference_count": 2}
        elif category == "continuation":
            turns = (f"Commence la tâche {marker}", "Continue sans t'arrêter.")
            expected = {"continuation": True}
        elif category == "negation":
            turns = (f"Utilise provider-{marker}", f"N'utilise plus provider-{marker}.")
            expected = {"negated": f"provider-{marker}"}
        elif category == "scope_priority":
            turns = (f"Répare A puis B {marker}", "Priorité à B, A ensuite.")
            expected = {"priority": "B"}
        elif category == "interruption":
            turns = (f"Explique le plan {marker}", "STOP", "Reprends à partir du dernier état vérifié.")
            expected = {"interrupt": True, "resume": True}
        elif category == "partial_asr":
            turns = (f"power chell gitub {marker}", "[ASR_PARTIAL] commi", "[USER_COMMITTED] commit")
            expected = {"stable_authority": "commit"}
        elif category == "noisy_french":
            turns = (f"euh stp repare le ficher power chell {marker}",)
            expected = {"normalized_terms": ("fichier", "powershell")}
        elif category == "mixed_technical_language":
            turns = (f"Fix le failing test puis commit sur main {marker}",)
            expected = {"technical_terms": ("failing test", "commit", "main")}
        elif category == "stale_reference":
            turns = (f"Lis src/a-{marker}.py", f"Modifie src/a-{marker}.py", "Utilise l'ancien read.")
            expected = {"stale_after_mutation": True}
        elif category == "restart":
            turns = (f"Contrainte {marker}: main only", "[RESTART]", "Continue.")
            expected = {"constraint": "main only", "survives_restart": True}
        elif category == "message_during_work":
            turns = (f"Lance analyse {marker}", "[WORKING]", "Ajoute aussi les tests de quota.")
            expected = {"new_requirement": "tests de quota"}
        elif category == "stop_scope":
            turns = (f"Tâches A et B {marker}", "Stop seulement B.")
            expected = {"stop": "B", "preserve": "A"}
        elif category == "undo":
            turns = (f"Change timeout à {index + 10}", "Annule uniquement ce dernier changement.")
            expected = {"undo_last_only": True}
        elif category == "long_constraint_retention":
            constraint = f"constraint-{marker}: no-paid-spillover"
            middle = tuple(f"Tour de travail {marker}-{step:03d}" for step in range(99))
            turns = (constraint,) + middle + ("Continue en respectant la contrainte initiale.",)
            expected = {"constraint": constraint, "minimum_turns": 101}
        elif category == "false_memory_rejection":
            turns = (f"Je n'ai jamais validé provider-{marker}", "Tu te souviens que je l'ai validé ?")
            expected = {"reject_false_memory": True}
        elif category == "causal_invalidation":
            turns = (f"Cible installer-{marker}", "Inspecte provider atlas", "Correction: cible model bridge.")
            expected = {"invalidate": f"installer-{marker}", "preserve": "provider atlas"}
        else:
            raise ValueError(category)
        return ReplayCase(cls._id(seed, category, index), category, turns, expected)

    @classmethod
    def generate(cls, *, seed: str = "release-v2", per_category: int = 60) -> tuple[ReplayCase, ...]:
        count = max(56, int(per_category))  # 18 * 56 = 1008 minimum release cases.
        return tuple(
            cls._case(str(seed), category, index)
            for category in cls.CATEGORIES
            for index in range(count)
        )


class ConversationReplayRunner:
    """Structural deterministic oracle for replay fixtures; no network/model dependency."""

    @staticmethod
    def _validate(case: ReplayCase) -> bool:
        if not case.case_id or not case.turns or not case.category:
            return False
        joined = " ".join(case.turns).lower()
        expected = case.expected
        category = case.category
        if category == "correction":
            return "non, je parle" in joined and expected["new_target"] in joined
        if category == "pronoun_reference":
            return expected["reference"].lower() in joined and "ça" in joined
        if category == "multi_selection_ambiguity":
            return bool(expected.get("ambiguous")) and " et " in joined and "ça" in joined
        if category == "continuation":
            return bool(expected.get("continuation")) and "continue" in joined
        if category == "negation":
            return expected["negated"].lower() in joined and ("n'utilise plus" in joined or "ne " in joined)
        if category == "scope_priority":
            return f"priorité à {expected['priority'].lower()}" in joined
        if category == "interruption":
            return "stop" in joined and "reprends" in joined
        if category == "partial_asr":
            return "[asr_partial]" in joined and "[user_committed]" in joined
        if category == "noisy_french":
            return "ficher" in joined and "power chell" in joined
        if category == "mixed_technical_language":
            return all(term in joined for term in expected["technical_terms"])
        if category == "stale_reference":
            return bool(expected.get("stale_after_mutation")) and "modifie" in joined and "ancien read" in joined
        if category == "restart":
            return bool(expected.get("survives_restart")) and expected["constraint"] in joined and "[restart]" in joined
        if category == "message_during_work":
            return "[working]" in joined and expected["new_requirement"] in joined
        if category == "stop_scope":
            return f"stop seulement {expected['stop'].lower()}" in joined and expected["preserve"].lower() in joined
        if category == "undo":
            return bool(expected.get("undo_last_only")) and "annule uniquement" in joined
        if category == "long_constraint_retention":
            return len(case.turns) >= int(expected.get("minimum_turns", 101)) and expected["constraint"].lower() in joined
        if category == "false_memory_rejection":
            return bool(expected.get("reject_false_memory")) and "jamais validé" in joined
        if category == "causal_invalidation":
            return expected["invalidate"].lower() in joined and expected["preserve"] in joined and "correction" in joined
        return False

    def run(self, cases: Iterable[ReplayCase]) -> ReplayReport:
        materialized = tuple(cases)
        failures: list[str] = []
        category_counts: dict[str, int] = {}
        for case in materialized:
            category_counts[case.category] = category_counts.get(case.category, 0) + 1
            if not self._validate(case):
                failures.append(case.case_id)
        return ReplayReport(
            total=len(materialized),
            passed=len(materialized) - len(failures),
            failed=len(failures),
            category_counts=category_counts,
            failure_ids=tuple(failures),
        )
