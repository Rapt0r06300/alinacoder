from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path


class Lot04CompletionTests(unittest.TestCase):
    def test_delegation_cannot_expand_authority_and_revocation_invalidates_descendant(self) -> None:
        from alinacoder.security.authority import AuthorityBroker, AuthorityError, OwnerPolicy

        broker = AuthorityBroker(OwnerPolicy(frozenset({"fs.read", "fs.write"})))
        parent = broker.issue("planner", {"fs.read", "fs.write"})
        child = broker.delegate(parent, "reader", {"fs.read"})
        broker.validate(child, "fs.read")
        with self.assertRaises(AuthorityError):
            broker.delegate(child, "bad-child", {"fs.write"})
        broker.revoke(parent.token_id)
        with self.assertRaises(AuthorityError):
            broker.validate(child, "fs.read")

    def test_semantic_transaction_stages_effects_and_compensates_reverse_order(self) -> None:
        from alinacoder.security.transactions import SemanticTransaction, TransactionError

        events: list[str] = []
        tx = SemanticTransaction("tx-1")
        tx.stage("a", lambda: events.append("do-a"), lambda: events.append("undo-a"))

        def fail() -> None:
            events.append("do-b")
            raise RuntimeError("boom")

        tx.stage("b", fail, lambda: events.append("undo-b"))
        self.assertEqual(events, [])
        with self.assertRaises(TransactionError):
            tx.commit()
        self.assertEqual(events, ["do-a", "do-b", "undo-a"])
        self.assertEqual(tx.status, "ABORTED")

    @unittest.skipUnless(os.name == "nt", "DPAPI is Windows-only")
    def test_dpapi_protector_round_trips_without_plaintext_storage(self) -> None:
        from alinacoder.security.platform_secrets import DPAPIProtector

        protector = DPAPIProtector()
        protected = protector.protect(b"very-secret-value")
        self.assertNotIn(b"very-secret-value", protected)
        self.assertEqual(protector.unprotect(protected), b"very-secret-value")

    def test_dependency_firewall_rejects_unpinned_or_untrusted_dependency(self) -> None:
        from alinacoder.security.dependencies import DependencyAdmissionError, DependencyAdmissionFirewall, DependencyRequest

        firewall = DependencyAdmissionFirewall(allowed_sources={"pypi.org"})
        firewall.admit(DependencyRequest("example", "1.2.3", "sha256:" + "a" * 64, "pypi.org"))
        with self.assertRaises(DependencyAdmissionError):
            firewall.admit(DependencyRequest("example", "*", "sha256:" + "a" * 64, "pypi.org"))
        with self.assertRaises(DependencyAdmissionError):
            firewall.admit(DependencyRequest("example", "1.2.3", None, "evil.example"))

    def test_tool_schema_validation_rejects_missing_and_unknown_arguments(self) -> None:
        from alinacoder.security.tools import ToolInvocationError, ToolManifest, ToolRegistry

        manifest = ToolManifest(
            "write_file",
            {"type": "object", "required": ["path", "content"], "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "additionalProperties": False},
            "local",
        )
        registry = ToolRegistry()
        registry.approve(manifest)
        registry.validate_invocation(manifest, {"path": "x", "content": "ok"})
        with self.assertRaises(ToolInvocationError):
            registry.validate_invocation(manifest, {"path": "x"})
        with self.assertRaises(ToolInvocationError):
            registry.validate_invocation(manifest, {"path": "x", "content": "ok", "force": True})


class Lot05CompletionTests(unittest.TestCase):
    def test_skillbook_is_project_scoped_and_promotes_only_verified_experience(self) -> None:
        from alinacoder.memory.skillbook import ExperienceCard, SkillBook, SkillPromotionError

        with tempfile.TemporaryDirectory() as td:
            book = SkillBook(Path(td) / "skills.db")
            card = ExperienceCard("p1", "fix-import", "repair missing import", verified=True, evidence=("test:green",))
            skill_id = book.promote(card)
            self.assertEqual(len(book.search("p1", "import")), 1)
            self.assertEqual(book.search("p2", "import"), [])
            self.assertEqual(book.get(skill_id).project_id, "p1")
            with self.assertRaises(SkillPromotionError):
                book.promote(ExperienceCard("p1", "guess", "unverified guess", verified=False, evidence=()))
            book.close()

    def test_memory_graph_retrieval_follows_explicit_relationships_without_cross_project_leak(self) -> None:
        from alinacoder.memory.graph import MemoryGraph

        with tempfile.TemporaryDirectory() as td:
            graph = MemoryGraph(Path(td) / "graph.db")
            a = graph.add("p1", "requirement", "goal mode must resume")
            b = graph.add("p1", "decision", "persist goal contract")
            graph.link("p1", a, b, "supports")
            graph.add("p2", "secret", "goal mode secret")
            results = graph.retrieve("p1", "goal", hops=1)
            self.assertEqual({r.node_id for r in results}, {a, b})
            self.assertTrue(all(r.project_id == "p1" for r in results))
            graph.close()

    def test_project_twin_updates_after_symbol_rename(self) -> None:
        from alinacoder.repo.index import RepositoryIndex
        from alinacoder.repo.twin import ProjectTwin

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "app.py"
            source.write_text("def old_name():\n    return 1\n", encoding="utf-8")
            index = RepositoryIndex(root / "index.db", "p1")
            index.index_file(source, root)
            twin = ProjectTwin(index)
            first = twin.snapshot()
            self.assertIn("old_name", first.symbols)
            source.write_text("def new_name():\n    return 1\n", encoding="utf-8")
            index.index_file(source, root)
            second = twin.snapshot()
            self.assertNotIn("old_name", second.symbols)
            self.assertIn("new_name", second.symbols)
            self.assertNotEqual(first.fingerprint, second.fingerprint)
            index.close()

    def test_data_flow_and_test_impact_are_available_from_repository_graph(self) -> None:
        from alinacoder.repo.analysis import RepositoryAnalyzer

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "calc.py").write_text("def total(x):\n    y = x + 1\n    return y\n", encoding="utf-8")
            (root / "test_calc.py").write_text("from calc import total\n\ndef test_total():\n    assert total(1) == 2\n", encoding="utf-8")
            analyzer = RepositoryAnalyzer(root)
            flow = analyzer.data_flow("calc.py", "y")
            self.assertTrue(any(edge.kind == "define" for edge in flow))
            self.assertTrue(any(edge.kind == "read" for edge in flow))
            self.assertIn("test_calc.py", analyzer.impacted_tests({"calc.py"}))

    def test_context_query_planner_cache_is_versioned_and_invalidates_on_new_state(self) -> None:
        from alinacoder.memory.planner import ContextQueryPlanner

        planner = ContextQueryPlanner(max_chars=500)
        first = planner.plan("p1", "fix parser", state_version=7, constraints=["main only"], evidence=["test:red"])
        second = planner.plan("p1", "fix parser", state_version=7, constraints=["main only"], evidence=["test:red"])
        third = planner.plan("p1", "fix parser", state_version=8, constraints=["main only"], evidence=["test:red"])
        self.assertEqual(first.cache_key, second.cache_key)
        self.assertNotEqual(first.cache_key, third.cache_key)
        self.assertIn("main only", first.mandatory_text)
        self.assertIn("test:red", first.mandatory_text)


if __name__ == "__main__":
    unittest.main()
