from __future__ import annotations

import unittest

from alinacoder.conversation import (
    ArtifactAnchor,
    ClarificationPolicy,
    ConversationEngine,
    Perspective,
    PlaybackLedger,
    PreferenceOriginError,
    ReferenceAmbiguityError,
    TurnInput,
)


class Lot06ConversationTests(unittest.TestCase):
    def test_twenty_turn_repairs_preserve_latest_intent_and_unrelated_verified_work(self) -> None:
        engine = ConversationEngine()
        engine.ingest(TurnInput("u1", "Crée le parser et garde le cache", meaning="create parser; keep cache"))
        engine.mark_verified("cache", "cache-proof")
        for index in range(2, 20):
            engine.ingest(TurnInput(f"u{index}", f"continue étape {index}", meaning=f"continue step {index}"))
        contract = engine.correct("u20", target="parser", replacement="Crée le parser JSON strict")
        self.assertEqual(contract.active_requirements["parser"], "Crée le parser JSON strict")
        self.assertEqual(contract.verified_work["cache"], "cache-proof")
        self.assertEqual(contract.turn_count, 20)

    def test_artifact_anchor_resolves_that_and_ambiguity_requires_clarification(self) -> None:
        engine = ConversationEngine()
        engine.register_anchor(ArtifactAnchor("diff-1", "diff", "src/a.py", selected=True))
        self.assertEqual(engine.resolve_reference("ça").artifact_id, "diff-1")
        engine.register_anchor(ArtifactAnchor("diff-2", "diff", "src/b.py", selected=True))
        with self.assertRaises(ReferenceAmbiguityError):
            engine.resolve_reference("ça")

    def test_preference_can_only_be_promoted_from_user_origin(self) -> None:
        engine = ConversationEngine()
        engine.record_preference("style", "concis", origin="user", evidence_id="turn-1")
        self.assertEqual(engine.preferences()["style"].value, "concis")
        with self.assertRaises(PreferenceOriginError):
            engine.record_preference("editor", "vim", origin="assistant", evidence_id="assistant-guess")

    def test_playback_interrupt_commits_only_heard_prefix_to_common_ground(self) -> None:
        ledger = PlaybackLedger()
        playback = ledger.start("p1", "Je vais modifier trois fichiers puis lancer les tests")
        ledger.commit_heard(playback.playback_id, 18)
        ledger.interrupt(playback.playback_id)
        heard = ledger.heard_text(playback.playback_id)
        self.assertEqual(heard, "Je vais modifier tr")
        self.assertNotIn("tests", ledger.common_ground_text())

    def test_common_ground_keeps_user_and_assistant_perspectives_distinct(self) -> None:
        engine = ConversationEngine()
        engine.believe(Perspective.USER, "target", "main.py", confidence=1.0, source="turn-1")
        engine.believe(Perspective.ASSISTANT, "target", "app.py", confidence=0.4, source="inference")
        self.assertEqual(engine.belief(Perspective.USER, "target").value, "main.py")
        self.assertEqual(engine.belief(Perspective.ASSISTANT, "target").value, "app.py")
        self.assertTrue(engine.has_perspective_conflict("target"))

    def test_clarification_regret_asks_only_when_expected_error_cost_dominates(self) -> None:
        policy = ClarificationPolicy(question_cost=0.2)
        self.assertTrue(policy.should_ask(ambiguity_probability=0.8, wrong_action_cost=1.0, inference_confidence=0.4))
        self.assertFalse(policy.should_ask(ambiguity_probability=0.05, wrong_action_cost=0.3, inference_confidence=0.95))

    def test_raw_and_meaning_are_both_preserved_for_noisy_french(self) -> None:
        engine = ConversationEngine()
        contract = engine.ingest(TurnInput("voice-1", "corrige le ficher la", meaning="corrige le fichier sélectionné"))
        last_turn = engine.turns[-1]
        self.assertEqual(last_turn.raw, "corrige le ficher la")
        self.assertEqual(last_turn.meaning, "corrige le fichier sélectionné")
        self.assertEqual(contract.last_turn_id, "voice-1")


if __name__ == "__main__":
    unittest.main()
