from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from alinacoder.tools import (
    GitMainExecutor,
    ResearchEvidence,
    SandboxPolicy,
    ToolCall,
    ToolRuntime,
    ToolSchema,
    ToolValidationError,
    UnknownResultError,
    ManagedProcessRunner,
)


class Lot08ToolRuntimeTests(unittest.TestCase):
    def test_schema_and_invocation_id_make_mutation_idempotent(self):
        runtime = ToolRuntime()
        runtime.register(ToolSchema("write", required={"path": str, "content": str}, mutating=True))
        calls = []
        def executor(args):
            calls.append(args.copy())
            return {"ok": True, "hash": "abc"}
        call = ToolCall("inv-1", "write", {"path":"a.txt","content":"x"})
        first = runtime.invoke(call, executor)
        second = runtime.invoke(call, executor)
        self.assertEqual(first, second)
        self.assertEqual(len(calls), 1)
        self.assertTrue(first.verified)

    def test_invalid_tool_arguments_fail_closed(self):
        runtime = ToolRuntime()
        runtime.register(ToolSchema("write", required={"path": str}, mutating=True))
        with self.assertRaises(ToolValidationError):
            runtime.invoke(ToolCall("x","write",{}), lambda args: {"ok":True})

    def test_git_executor_allows_main_only_and_reconciles_unknown_result(self):
        git = GitMainExecutor()
        git.validate_target("main")
        with self.assertRaises(ValueError):
            git.validate_target("feature/x")
        self.assertEqual(git.reconcile_after_unknown_result(expected_head="abc", observed_head="abc"), "COMMITTED")
        with self.assertRaises(UnknownResultError):
            git.reconcile_after_unknown_result(expected_head="abc", observed_head="def")

    def test_research_evidence_tracks_provenance_freshness_and_citation(self):
        ev = ResearchEvidence.from_document("https://example.test/doc", "hello world", observed_at=100.0, ttl_seconds=60.0)
        self.assertTrue(ev.is_fresh(150.0))
        self.assertFalse(ev.is_fresh(161.0))
        self.assertTrue(ev.content_hash)
        self.assertIn("example.test", ev.citation)

    def test_sandbox_rejects_escape_from_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = SandboxPolicy(Path(tmp))
            self.assertTrue(str(policy.resolve("sub/file.txt")).startswith(str(Path(tmp).resolve())))
            with self.assertRaises(PermissionError):
                policy.resolve("../escape.txt")

    def test_managed_process_runner_captures_success_and_timeout(self):
        runner = ManagedProcessRunner()
        ok = runner.run([sys.executable,"-c","print('ok')"], timeout_seconds=5)
        self.assertEqual(ok.returncode, 0)
        self.assertIn("ok", ok.stdout)
        slow = runner.run([sys.executable,"-c","import time; time.sleep(2)"], timeout_seconds=0.1)
        self.assertTrue(slow.timed_out)


if __name__ == "__main__":
    unittest.main()
