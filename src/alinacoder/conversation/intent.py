from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any

from .advanced import TechnicalFrenchNormalizer


@dataclass(frozen=True, slots=True)
class IntentEnvelope:
    raw: str
    meaning: str
    primary_intent: str
    alternatives: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    requirements_added: tuple[str, ...] = ()
    requirements_changed: tuple[str, ...] = ()
    requirements_cancelled: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    prohibitions: tuple[str, ...] = ()
    desired_result: str = ""
    continuation: bool = False
    correction: bool = False
    confidence: str = "MEDIUM"
    uncertainty_causes: tuple[str, ...] = ()
    source_turn_ids: tuple[str, ...] = ()
    model_proposal: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key in (
            "alternatives", "references", "requirements_added", "requirements_changed",
            "requirements_cancelled", "constraints", "prohibitions", "uncertainty_causes", "source_turn_ids",
        ):
            value[key] = list(value[key])
        return value


class IntentCompiler:
    """Deterministic-first intent envelope builder.

    Model output, when supplied, is retained as proposal metadata only; it does
    not directly mutate canonical requirements or permissions.
    """

    _CORRECTION = re.compile(
        r"(?:^|[.!?]\s*)(?:non\b|no\b|je (?:parle|veux dire)|i mean\b|plut[oô]t\b|correction\b)",
        re.IGNORECASE,
    )
    _CONTINUE = re.compile(
        r"\b(?:continue|continuer|poursuis|poursuivre|vas[- ]?y|go on|keep going|ne t['’]?arr[eê]te pas)\b",
        re.IGNORECASE,
    )
    _CANCEL = re.compile(
        r"\b(?:annule|annuler|cancel|supprime cette demande|ignore cette demande|laisse tomber)\b",
        re.IGNORECASE,
    )
    _PROHIBITION = re.compile(
        r"\b(?:ne|n['’])\s+([^.!?]{2,120}?)\s+(?:pas|plus)\b|\b(?:sans)\s+([^.!?]{2,120})",
        re.IGNORECASE,
    )
    _REFERENCE = re.compile(r"\b(?:ça|cela|ceci|this|that|celui[- ]?ci|celle[- ]?ci)\b", re.IGNORECASE)

    def __init__(self, normalizer: TechnicalFrenchNormalizer | None = None) -> None:
        self._normalizer = normalizer or TechnicalFrenchNormalizer()

    def compile(
        self,
        raw: str,
        *,
        source_turn_ids: tuple[str, ...] | list[str] = (),
        selected_artifacts: tuple[str, ...] | list[str] = (),
        model_proposal: dict[str, Any] | None = None,
    ) -> IntentEnvelope:
        raw_text = str(raw)
        if not raw_text.strip():
            raise ValueError("intent input cannot be empty")
        meaning = self._normalizer.normalize(raw_text).strip()
        correction = bool(self._CORRECTION.search(meaning))
        continuation = bool(self._CONTINUE.search(meaning))
        cancelled = bool(self._CANCEL.search(meaning))
        references = tuple(str(item) for item in selected_artifacts if str(item))
        if self._REFERENCE.search(meaning) and not references:
            references = ("UNRESOLVED_DEICTIC_REFERENCE",)
        prohibitions: list[str] = []
        for match in self._PROHIBITION.finditer(meaning):
            value = next((part for part in match.groups() if part), "")
            if value.strip():
                prohibitions.append(value.strip())
        requirements_cancelled = (meaning,) if cancelled else ()
        requirements_changed = (meaning,) if correction else ()
        requirements_added = () if (correction or cancelled) else (meaning,)
        uncertainties: list[str] = []
        if references == ("UNRESOLVED_DEICTIC_REFERENCE",):
            uncertainties.append("unresolved_reference")
        confidence = "HIGH" if not uncertainties else "MEDIUM"
        return IntentEnvelope(
            raw=raw_text,
            meaning=meaning,
            primary_intent=meaning,
            alternatives=(),
            references=references,
            requirements_added=requirements_added,
            requirements_changed=requirements_changed,
            requirements_cancelled=requirements_cancelled,
            constraints=(),
            prohibitions=tuple(prohibitions),
            desired_result=meaning,
            continuation=continuation,
            correction=correction,
            confidence=confidence,
            uncertainty_causes=tuple(uncertainties),
            source_turn_ids=tuple(str(item) for item in source_turn_ids),
            model_proposal=dict(model_proposal) if isinstance(model_proposal, dict) else None,
        )
