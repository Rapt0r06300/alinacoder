from __future__ import annotations

import importlib
import importlib.util
import unittest


def _load(testcase: unittest.TestCase):
    name = "alinacoder.evaluation.conversation_replay"
    try:
        spec = importlib.util.find_spec(name)
    except ModuleNotFoundError:
        spec = None
    testcase.assertIsNotNone(spec, f"missing module: {name}")
    return importlib.import_module(name)


class ConversationReplayV2Tests(unittest.TestCase):
    def test_corpus_contains_at_least_one_thousand_deterministic_unique_cases(self) -> None:
        replay = _load(self)
        first = replay.ConversationReplayCorpus.generate(seed="release-v2")
        second = replay.ConversationReplayCorpus.generate(seed="release-v2")
        self.assertGreaterEqual(len(first), 1000)
        self.assertEqual([case.case_id for case in first], [case.case_id for case in second])
        self.assertEqual(len(first), len({case.case_id for case in first}))

    def test_corpus_covers_required_failure_families(self) -> None:
        replay = _load(self)
        cases = replay.ConversationReplayCorpus.generate(seed="release-v2")
        categories = {case.category for case in cases}
        required = {
            "correction",
            "pronoun_reference",
            "multi_selection_ambiguity",
            "continuation",
            "negation",
            "scope_priority",
            "interruption",
            "partial_asr",
            "noisy_french",
            "mixed_technical_language",
            "stale_reference",
            "restart",
            "message_during_work",
            "stop_scope",
            "undo",
            "long_constraint_retention",
            "false_memory_rejection",
            "causal_invalidation",
        }
        self.assertTrue(required.issubset(categories), required - categories)

    def test_runner_passes_structural_release_corpus_and_reports_categories(self) -> None:
        replay = _load(self)
        cases = replay.ConversationReplayCorpus.generate(seed="release-v2")
        report = replay.ConversationReplayRunner().run(cases)
        self.assertEqual(report.total, len(cases))
        self.assertEqual(report.failed, 0)
        self.assertEqual(report.passed, report.total)
        self.assertGreaterEqual(len(report.category_counts), 18)
        self.assertEqual(report.failure_ids, ())

    def test_long_constraint_cases_have_over_one_hundred_turns(self) -> None:
        replay = _load(self)
        cases = replay.ConversationReplayCorpus.generate(seed="release-v2")
        long_cases = [case for case in cases if case.category == "long_constraint_retention"]
        self.assertTrue(long_cases)
        self.assertTrue(all(len(case.turns) >= 101 for case in long_cases[:5]))
        self.assertTrue(all(case.expected.get("constraint") for case in long_cases[:5]))


if __name__ == "__main__":
    unittest.main()
