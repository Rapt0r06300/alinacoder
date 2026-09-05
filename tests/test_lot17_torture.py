import unittest
from alinacoder.evaluation.torture import FailureCard,TortureLab,classify_retry
class Lot17TortureTests(unittest.TestCase):
 def test_critical_failure_prevents_readiness(self):
  r=TortureLab().evaluate([FailureCard('seed1','prompt_injection','authority_non_escalation',True,True)]);self.assertFalse(r.ready);self.assertEqual(r.score,0.0)
 def test_failure_card_replay_payload_is_deterministic(self):
  c=FailureCard('42','stale_state','reject_stale',True,False);self.assertEqual(c.replay_payload(),c.replay_payload())
 def test_semantic_fault_is_not_blindly_retried(self):self.assertEqual(classify_retry('tool_timeout'),'RETRY');self.assertEqual(classify_retry('context_pollution'),'ATTRIBUTION_REQUIRED')
 def test_known_safety_scenarios_are_caught(self):
  r=TortureLab().run_known_campaign();self.assertTrue(all(x.detected for x in r));self.assertGreaterEqual(len(r),8)
if __name__=='__main__':unittest.main()
