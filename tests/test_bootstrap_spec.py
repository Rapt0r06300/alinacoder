from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path


def git_blob_sha(text: str) -> str:
    data = text.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class BootstrapSpecTests(unittest.TestCase):
    def test_constitutional_defaults_are_fail_closed(self) -> None:
        from alinacoder.config import AlinaConfig
        cfg = AlinaConfig()
        self.assertEqual(cfg.max_paid_spend_eur, 0.0)
        self.assertFalse(cfg.allow_pay_as_you_go)
        self.assertFalse(cfg.allow_automatic_credit_purchase)
        self.assertFalse(cfg.allow_automatic_plan_upgrade)
        self.assertFalse(cfg.allow_paid_fallback)
        self.assertFalse(cfg.allow_auto_reload)
        self.assertEqual(cfg.canonical_branch, "main")

    def test_spec_compiler_validates_manifest_and_git_blob_hash(self) -> None:
        from alinacoder.spec.compiler import SpecCompiler
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            spec_path = root / "spec.md"
            spec = "# Spec\nALINA.COST.ZERO.001\nALINA.GIT.MAIN_ONLY.001\n"
            spec_path.write_text(spec, encoding="utf-8")
            manifest = {"current_spec": {"path": "spec.md", "source_hash": git_blob_sha(spec)}, "constitutional_invariants": ["ALINA.COST.ZERO.001", "ALINA.GIT.MAIN_ONLY.001"], "active_documents": [], "resolution_policy": {"unresolved_conflicts": []}}
            (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            result = SpecCompiler(root).compile(root / "manifest.json")
            self.assertTrue(result.valid)
            self.assertEqual(result.current_spec_path, spec_path)
            self.assertEqual(result.invariants, tuple(manifest["constitutional_invariants"]))

    def test_spec_compiler_fails_closed_on_hash_mismatch(self) -> None:
        from alinacoder.spec.compiler import SpecCompileError, SpecCompiler
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "spec.md").write_text("# changed", encoding="utf-8")
            manifest = {"current_spec": {"path": "spec.md", "source_hash": "0" * 40}, "constitutional_invariants": [], "active_documents": []}
            (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaises(SpecCompileError):
                SpecCompiler(root).compile(root / "manifest.json")

    def test_spec_compiler_fails_closed_when_invariant_missing(self) -> None:
        from alinacoder.spec.compiler import SpecCompileError, SpecCompiler
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            spec = "# Spec\nALINA.COST.ZERO.001\n"
            (root / "spec.md").write_text(spec, encoding="utf-8")
            manifest = {"current_spec": {"path": "spec.md", "source_hash": git_blob_sha(spec)}, "constitutional_invariants": ["ALINA.COST.ZERO.001", "ALINA.GIT.MAIN_ONLY.001"], "active_documents": []}
            (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaises(SpecCompileError):
                SpecCompiler(root).compile(root / "manifest.json")

    def test_cli_imports(self) -> None:
        from alinacoder.cli import build_parser
        self.assertEqual(build_parser().prog, "alinacoder")


if __name__ == "__main__":
    unittest.main()
