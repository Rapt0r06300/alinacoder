from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlaybackTurn:
    playback_id: str
    text: str
    heard_chars: int = 0
    interrupted: bool = False


class PlaybackLedger:
    """Playback-aligned common ground.

    Generated-but-unheard assistant output stays speculative and revocable. This
    mirrors the PACE-style playback boundary and prevents post-interruption state
    from being grounded in words the user never heard.
    """

    def __init__(self) -> None:
        self._turns: dict[str, PlaybackTurn] = {}
        self._order: list[str] = []

    def start(self, playback_id: str, text: str) -> PlaybackTurn:
        if playback_id in self._turns:
            raise ValueError("duplicate playback id")
        turn = PlaybackTurn(playback_id, text)
        self._turns[playback_id] = turn
        self._order.append(playback_id)
        return turn

    def commit_heard(self, playback_id: str, heard_chars: int) -> None:
        turn = self._turns[playback_id]
        turn.heard_chars = max(turn.heard_chars, min(len(turn.text), max(0, heard_chars)))

    def interrupt(self, playback_id: str) -> None:
        self._turns[playback_id].interrupted = True

    def heard_text(self, playback_id: str) -> str:
        turn = self._turns[playback_id]
        return turn.text[: turn.heard_chars]

    def unheard_text(self, playback_id: str) -> str:
        turn = self._turns[playback_id]
        return turn.text[turn.heard_chars :]

    def common_ground_text(self) -> str:
        return "\n".join(self.heard_text(pid) for pid in self._order if self._turns[pid].heard_chars)


class TurnContinuationForecast:
    def __init__(self, pause_threshold_ms: int = 900) -> None:
        self.pause_threshold_ms = pause_threshold_ms

    def should_wait(self, *, pause_ms: int, unfinished_syntax: bool, recent_filler: bool = False) -> bool:
        if unfinished_syntax or recent_filler:
            return True
        return pause_ms < self.pause_threshold_ms


class InterruptionClassifier:
    TYPES = {"correction", "question", "topic_switch", "filler", "pushback", "stop", "repeat", "normal"}

    def classify(self, text: str) -> str:
        t = text.strip().lower()
        if not t or t in {"mhm", "mm-hm", "oui", "ok", "d'accord"}:
            return "filler"
        if any(k in t for k in ("stop", "arrête", "tais-toi")):
            return "stop"
        if any(k in t for k in ("non attends", "en fait", "plutôt", "corrige")):
            return "correction"
        if any(k in t for k in ("répète", "j'ai pas entendu")):
            return "repeat"
        if "?" in t or t.startswith(("pourquoi", "comment", "est-ce")):
            return "question"
        return "normal"
