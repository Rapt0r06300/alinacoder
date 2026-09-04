from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


class SecurityKernelTests(unittest.TestCase):
    def make_state(self, root: Path):
        from alinacoder.state.store import StateStore
        store = StateStore(root / "state.db")
        state = store.create_session("s1", {})
        return store, state

    def test_untrusted_prompt_cannot_escalate_to_privileged_effect(self) -> None:
        from alinacoder.security.authority import AuthorityBroker, OwnerPolicy, Provenance, TrustLevel
        from alinacoder.security.effects import EffectDenied, ExternalEffectGate
        with tempfile.TemporaryDirectory() as td:
            store, state = self.make_state(Path(td))
            broker = AuthorityBroker(OwnerPolicy(frozenset({"fs.write"})))
            token = broker.issue("worker", {"fs.write"})
            gate = ExternalEffectGate(store, broker)
            hostile = Provenance("web:https://evil.example", TrustLevel.UNTRUSTED, tainted=True)
            with self.assertRaises(EffectDenied): gate.admit("effect-1", "s1", "fs.write", token, state.version, hostile, {"path": "x"})
            store.close()

    def test_stale_approval_is_rejected_after_revocation_epoch_changes(self) -> None:
        from alinacoder.security.authority import AuthorityBroker, OwnerPolicy, Provenance
        from alinacoder.security.effects import EffectDenied, ExternalEffectGate
        with tempfile.TemporaryDirectory() as td:
            store, state = self.make_state(Path(td))
            broker = AuthorityBroker(OwnerPolicy(frozenset({"fs.write"})))
            token = broker.issue("worker", {"fs.write"})
            broker.revoke_all()
            with self.assertRaises(EffectDenied): ExternalEffectGate(store, broker).admit("effect-1", "s1", "fs.write", token, state.version, Provenance.user(), {"path": "x"})
            store.close()

    def test_effect_key_prevents_duplicate_effect(self) -> None:
        from alinacoder.security.authority import AuthorityBroker, OwnerPolicy, Provenance
        from alinacoder.security.effects import DuplicateEffectError, ExternalEffectGate
        with tempfile.TemporaryDirectory() as td:
            store, state = self.make_state(Path(td))
            broker = AuthorityBroker(OwnerPolicy(frozenset({"fs.write"})))
            token = broker.issue("worker", {"fs.write"})
            gate = ExternalEffectGate(store, broker)
            self.assertEqual(gate.admit("effect-1", "s1", "fs.write", token, state.version, Provenance.user(), {"path": "x"}).effect_key, "effect-1")
            with self.assertRaises(DuplicateEffectError): gate.admit("effect-1", "s1", "fs.write", token, state.version, Provenance.user(), {"path": "x"})
            store.close()

    def test_secret_redaction_prevents_plaintext_logging(self) -> None:
        from alinacoder.security.secrets import InMemorySecretStore, SecretBroker, redact_secrets
        store = InMemorySecretStore()
        handle = store.put("github", "super-secret-token")
        broker = SecretBroker(store)
        self.assertEqual(str(handle), "secret://github")
        self.assertEqual(redact_secrets("token=super-secret-token", ["super-secret-token"]), "token=[REDACTED]")
        self.assertEqual(broker.use(handle, lambda secret: len(secret)), len("super-secret-token"))
        with self.assertRaises(ValueError): broker.use(handle, lambda secret: f"leak:{secret}")

    def test_tool_manifest_drift_requires_reapproval(self) -> None:
        from alinacoder.security.tools import ToolManifest, ToolRegistry
        registry = ToolRegistry()
        original = ToolManifest("write_file", {"path": "str"}, "local")
        registry.approve(original)
        self.assertTrue(registry.is_approved(original))
        self.assertFalse(registry.is_approved(ToolManifest("write_file", {"path": "str", "force": "bool"}, "local")))

    def test_egress_is_deny_by_default(self) -> None:
        from alinacoder.security.egress import EgressPolicy
        policy = EgressPolicy(frozenset({"api.github.com"}))
        self.assertTrue(policy.allows("https://api.github.com/repos/x/y"))
        self.assertFalse(policy.allows("https://evil.example/upload"))
        self.assertFalse(policy.allows("file:///tmp/x"))


if __name__ == "__main__":
    unittest.main()
