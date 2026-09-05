from __future__ import annotations


class FormalEscalationPolicy:
    def should_escalate(self, *, criticality: str, irreversible: bool, invariant_bearing: bool) -> bool:
        return criticality.lower() == "high" and irreversible and invariant_bearing
