from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ControlAction(str, Enum):
    ACT = "act"
    INSPECT = "inspect"
    SANDBOX_PROBE = "sandbox_probe"
    VERIFY = "verify"
    ESCALATE_MODEL = "escalate_model"
    CALL_COUNCIL = "call_council"
    ASK_USER = "ask_user"
    BLOCK = "block"


@dataclass(frozen=True, slots=True)
class ControlDecision:
    action: ControlAction
    reason: str
    expected_error_cost: float


class UncertaintyController:
    """Convert uncertainty and reversibility into the least disruptive safe action."""

    def decide(
        self,
        *,
        ambiguity: float,
        wrong_action_cost: float,
        reversible: bool,
        safe_inspection_available: bool,
        sandbox_probe_available: bool,
        verification_available: bool = False,
        model_escalation_available: bool = False,
        council_available: bool = False,
        information_gain: float = 1.0,
    ) -> ControlDecision:
        ambiguity = max(0.0, min(1.0, float(ambiguity)))
        wrong_action_cost = max(0.0, min(1.0, float(wrong_action_cost)))
        information_gain = max(0.0, min(1.0, float(information_gain)))
        risk = ambiguity * wrong_action_cost
        if safe_inspection_available:
            return ControlDecision(ControlAction.INSPECT, "safe inspection can reduce uncertainty", risk)
        if sandbox_probe_available and reversible:
            return ControlDecision(ControlAction.SANDBOX_PROBE, "reversible probe can reduce uncertainty", risk)
        if risk <= 0.20 and reversible:
            return ControlDecision(ControlAction.ACT, "best-supported reversible interpretation is low risk", risk)
        if verification_available and risk <= 0.45:
            return ControlDecision(ControlAction.VERIFY, "verification can cheaply bound residual uncertainty", risk)
        if model_escalation_available and risk <= 0.60:
            return ControlDecision(ControlAction.ESCALATE_MODEL, "stronger interpretation may avoid interruption", risk)
        if council_available and risk > 0.60 and information_gain >= 0.5:
            return ControlDecision(ControlAction.CALL_COUNCIL, "independent review has positive information value", risk)
        if risk > 0.35 and information_gain > 0.0:
            return ControlDecision(ControlAction.ASK_USER, "high-cost ambiguity requires the highest-information user answer", risk)
        if risk > 0.35:
            return ControlDecision(ControlAction.BLOCK, "unsafe ambiguity cannot be resolved", risk)
        return ControlDecision(ControlAction.ACT, "residual ambiguity is bounded and action is recoverable", risk)
