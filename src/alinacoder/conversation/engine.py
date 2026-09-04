from __future__ import annotations

from dataclasses import replace

from .models import ArtifactAnchor, Belief, GroundedIntentContract, Perspective, Preference, TurnInput, TurnRecord


class ReferenceAmbiguityError(RuntimeError):
    pass


class PreferenceOriginError(RuntimeError):
    pass


class ClarificationPolicy:
    def __init__(self, question_cost: float = 0.2) -> None:
        self.question_cost = question_cost

    def should_ask(self, *, ambiguity_probability: float, wrong_action_cost: float, inference_confidence: float) -> bool:
        expected_error_cost = max(0.0, ambiguity_probability) * max(0.0, wrong_action_cost) * max(0.0, 1.0 - inference_confidence)
        return expected_error_cost > self.question_cost


class ConversationEngine:
    """Deterministic conversational state outside the LLM.

    The engine preserves RAW+MEANING turns, current intent/constraints, verified work,
    user-vs-assistant beliefs, artifact anchors and user-originated preferences.
    Corrections supersede only the targeted requirement.
    """

    def __init__(self) -> None:
        self.turns: list[TurnRecord] = []
        self._requirements: dict[str, str] = {}
        self._constraints: dict[str, str] = {}
        self._verified: dict[str, str] = {}
        self._superseded: list[tuple[str, str]] = []
        self._anchors: list[ArtifactAnchor] = []
        self._beliefs: dict[tuple[Perspective, str], Belief] = {}
        self._preferences: dict[str, Preference] = {}
        self._last_turn_id = ""

    def ingest(self, turn: TurnInput) -> GroundedIntentContract:
        meaning = turn.meaning if turn.meaning is not None else turn.raw
        self.turns.append(TurnRecord(turn.turn_id, turn.raw, meaning))
        self._last_turn_id = turn.turn_id
        return self.contract()

    def set_requirement(self, key: str, value: str) -> GroundedIntentContract:
        self._requirements[key] = value
        return self.contract()

    def set_constraint(self, key: str, value: str) -> GroundedIntentContract:
        self._constraints[key] = value
        return self.contract()

    def correct(self, turn_id: str, *, target: str, replacement: str) -> GroundedIntentContract:
        old = self._requirements.get(target)
        if old is not None:
            self._superseded.append((target, old))
        self._requirements[target] = replacement
        self.turns.append(TurnRecord(turn_id, replacement, replacement))
        self._last_turn_id = turn_id
        return self.contract()

    def mark_verified(self, key: str, proof: str) -> None:
        self._verified[key] = proof

    def contract(self) -> GroundedIntentContract:
        return GroundedIntentContract(
            last_turn_id=self._last_turn_id,
            turn_count=len(self.turns),
            active_requirements=dict(self._requirements),
            constraints=dict(self._constraints),
            verified_work=dict(self._verified),
            superseded=list(self._superseded),
        )

    def register_anchor(self, anchor: ArtifactAnchor) -> None:
        self._anchors.append(anchor)

    def resolve_reference(self, text: str) -> ArtifactAnchor:
        normalized = text.strip().lower()
        if normalized in {"ça", "ca", "celui-là", "celui la", "celle-là", "celle la", "this", "that"}:
            selected = [a for a in self._anchors if a.selected]
            if len(selected) == 1:
                return selected[0]
            if len(selected) > 1:
                raise ReferenceAmbiguityError("multiple selected artifact anchors")
        direct = [a for a in self._anchors if a.artifact_id == text or a.locator == text]
        if len(direct) == 1:
            return direct[0]
        if len(direct) > 1:
            raise ReferenceAmbiguityError("multiple matching artifact anchors")
        raise ReferenceAmbiguityError(f"unresolved reference: {text}")

    def believe(self, perspective: Perspective, key: str, value: str, *, confidence: float, source: str) -> Belief:
        belief = Belief(perspective, key, value, max(0.0, min(1.0, confidence)), source)
        self._beliefs[(perspective, key)] = belief
        return belief

    def belief(self, perspective: Perspective, key: str) -> Belief:
        return self._beliefs[(perspective, key)]

    def has_perspective_conflict(self, key: str) -> bool:
        user = self._beliefs.get((Perspective.USER, key))
        assistant = self._beliefs.get((Perspective.ASSISTANT, key))
        return bool(user and assistant and user.value != assistant.value)

    def record_preference(self, key: str, value: str, *, origin: str, evidence_id: str) -> Preference:
        if origin != "user":
            raise PreferenceOriginError("durable preference requires user-originated evidence")
        pref = Preference(key, value, evidence_id)
        self._preferences[key] = pref
        return pref

    def preferences(self) -> dict[str, Preference]:
        return dict(self._preferences)
