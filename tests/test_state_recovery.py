from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


class StateRecoveryTests(unittest.TestCase):
    def make_store(self, root: Path):
        from alinacoder.state.store import StateStore
        return StateStore(root / "state.db")

    def test_state_is_reconstructible_and_evidence_becomes_stale_after_change(self) -> None:
        from alinacoder.state.models import EvidenceReceipt
        with tempfile.TemporaryDirectory() as td:
            store = self.make_store(Path(td))
            state0 = store.create_session("s1", {"step": 0})
            epoch = store.acquire_writer("s1")
            state1 = store.commit_state("s1", state0.version, epoch, {"step": 1}, "advance")
            evidence = EvidenceReceipt.bind("ev1", state1, {"test": "pass"})
            self.assertEqual(store.reconstruct("s1"), state1)
            self.assertTrue(evidence.is_fresh(state1))
            state2 = store.commit_state("s1", state1.version, epoch, {"step": 2}, "advance")
            self.assertFalse(evidence.is_fresh(state2))

    def test_stale_writer_and_stale_version_are_rejected(self) -> None:
        from alinacoder.state.store import StaleStateError, StaleWriterError
        with tempfile.TemporaryDirectory() as td:
            store = self.make_store(Path(td))
            state = store.create_session("s1", {})
            epoch1 = store.acquire_writer("s1")
            epoch2 = store.acquire_writer("s1")
            with self.assertRaises(StaleWriterError):
                store.commit_state("s1", state.version, epoch1, {"x": 1}, "bad")
            state1 = store.commit_state("s1", state.version, epoch2, {"x": 1}, "ok")
            with self.assertRaises(StaleStateError):
                store.commit_state("s1", state.version, epoch2, {"x": 2}, "stale")
            self.assertEqual(store.get_state("s1"), state1)

    def test_restore_is_forward_only_and_keeps_event_history(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            store = self.make_store(Path(td))
            state = store.create_session("s1", {"value": "a"})
            epoch = store.acquire_writer("s1")
            store.checkpoint("s1", "good")
            changed = store.commit_state("s1", state.version, epoch, {"value": "b"}, "change")
            restored = store.restore_checkpoint("s1", "good", changed.version, epoch)
            self.assertEqual(restored.data, {"value": "a"})
            self.assertGreater(restored.version, changed.version)
            self.assertEqual([e.kind for e in store.list_events("s1")], ["session_created", "change", "checkpoint_restore"])

    def test_effect_intent_is_idempotent_and_pending_effects_recover(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            store = self.make_store(Path(td))
            store.create_session("s1", {})
            self.assertTrue(store.begin_effect("effect-1", "s1", {"op": "write"}))
            self.assertFalse(store.begin_effect("effect-1", "s1", {"op": "write"}))
            store.close()
            reopened = self.make_store(Path(td))
            self.assertEqual([i.effect_key for i in reopened.pending_effects("s1")], ["effect-1"])
            reopened.ack_effect("effect-1", {"ok": True})
            self.assertEqual(reopened.pending_effects("s1"), [])


if __name__ == "__main__":
    unittest.main()
