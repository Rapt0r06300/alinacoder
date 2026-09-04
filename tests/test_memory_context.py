from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


class MemoryContextTests(unittest.TestCase):
    def test_project_memory_isolation_and_persistence(self) -> None:
        from alinacoder.memory.store import MemoryStore
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "memory.db"; store = MemoryStore(db)
            store.put("p1","semantic","alpha architecture rule","user",authority=100); store.put("p2","semantic","alpha secret from other project","user",authority=100)
            self.assertEqual(len(store.search("p1","alpha",10)),1); self.assertEqual(store.search("p1","secret",10),[]); store.close()
            reopened = MemoryStore(db); self.assertEqual(reopened.search("p1","architecture",10)[0].project_id,"p1"); reopened.close()

    def test_stale_memory_cannot_override_current_repo(self) -> None:
        from alinacoder.memory.context import ContextCompiler
        from alinacoder.memory.store import MemoryStore, file_sha256
        from alinacoder.repo.index import RepositoryIndex
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); src = root / "app.py"; src.write_text("MODE = 'new'\n",encoding="utf-8")
            store = MemoryStore(root/"memory.db"); old_hash=file_sha256(src); memory_id=store.put("p1","semantic","MODE is old","app.py",source_hash=old_hash,authority=50)
            src.write_text("MODE = 'newer'\n",encoding="utf-8"); self.assertIn(memory_id,store.refresh_source_freshness("p1",root))
            index=RepositoryIndex(root/"repo.db","p1"); index.index_file(src,root)
            compiled=ContextCompiler(store,index).compile("p1","MODE",repo_root=root,required_constraints=["MODE follows repo"],max_chars=500)
            self.assertIn("MODE follows repo",compiled.text); self.assertNotIn("MODE is old",compiled.text); store.close(); index.close()

    def test_incremental_ast_index_replaces_renamed_symbol(self) -> None:
        from alinacoder.repo.index import RepositoryIndex
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); src=root/"module.py"; src.write_text("def foo():\n    return 1\n",encoding="utf-8"); index=RepositoryIndex(root/"repo.db","p1")
            self.assertTrue(index.index_file(src,root)); self.assertEqual([s.name for s in index.symbols("module.py")],["foo"]); self.assertFalse(index.index_file(src,root))
            src.write_text("def bar():\n    return 2\n",encoding="utf-8"); self.assertTrue(index.index_file(src,root)); self.assertEqual([s.name for s in index.symbols("module.py")],["bar"]); index.close()

    def test_context_is_bounded_but_preserves_constraints_and_evidence(self) -> None:
        from alinacoder.memory.context import ContextCompiler
        from alinacoder.memory.store import MemoryStore
        from alinacoder.repo.index import RepositoryIndex
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); store=MemoryStore(root/"memory.db"); index=RepositoryIndex(root/"repo.db","p1")
            for i in range(30): store.put("p1","episodic",f"memory {i} "+("x"*80),"conversation",authority=20)
            compiled=ContextCompiler(store,index).compile("p1","memory",required_constraints=["NEVER SPEND MONEY","MAIN ONLY"],evidence=["HEAD=abc123"],max_chars=420)
            self.assertLessEqual(len(compiled.text),420); self.assertIn("NEVER SPEND MONEY",compiled.text); self.assertIn("MAIN ONLY",compiled.text); self.assertIn("HEAD=abc123",compiled.text); store.close(); index.close()

    def test_forgetting_detector_reports_changed_sources(self) -> None:
        from alinacoder.memory.store import MemoryStore, file_sha256
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); src=root/"config.py"; src.write_text("VALUE=1\n",encoding="utf-8"); store=MemoryStore(root/"memory.db")
            memory_id=store.put("p1","semantic","VALUE is 1","config.py",source_hash=file_sha256(src),authority=50); self.assertEqual(store.refresh_source_freshness("p1",root),[])
            src.write_text("VALUE=2\n",encoding="utf-8"); self.assertEqual(store.refresh_source_freshness("p1",root),[memory_id]); self.assertEqual(store.search("p1","VALUE",10),[]); store.close()


if __name__ == "__main__":
    unittest.main()
