import unittest
from alinacoder.self_improvement.core import BlackBoxRecorder,CandidateMetrics,CorrectionRuleFactory,EvolutionCandidate,EvolutionGate,GovernanceSupervisor
class Lot12SelfImprovementTests(unittest.TestCase):
 def test_hidden_holdout_regression_blocks_promotion(self):
  g=EvolutionGate(.01);c=EvolutionCandidate('c1','router','improve');self.assertEqual(g.evaluate(c,CandidateMetrics(.7,.8,.75),CandidateMetrics(.85,.9,.6)),'REJECT_HIDDEN_REGRESSION')
 def test_protected_governance_surface_cannot_self_modify(self):
  s=GovernanceSupervisor(('src/alinacoder/security/','docs/superpowers/specs/'));self.assertFalse(s.mutation_allowed(['src/alinacoder/security/policy.py']));self.assertTrue(s.mutation_allowed(['src/alinacoder/orchestration/router.py']))
 def test_promotion_and_rollback_preserve_version_lineage(self):
  g=EvolutionGate(.01);c=EvolutionCandidate('c2','skill','better');self.assertEqual(g.evaluate(c,CandidateMetrics(.6,.65,.61),CandidateMetrics(.72,.71,.70)),'PROMOTE');g.promote(c,previous_version='v1');self.assertEqual(g.active_version,'c2');g.rollback();self.assertEqual(g.active_version,'v1')
 def test_runtime_rule_requires_user_provenance_and_is_revocable(self):
  f=CorrectionRuleFactory();
  with self.assertRaises(ValueError):f.create('r1','always main',source='assistant',scope='git')
  r=f.create('r1','always main',source='user',scope='git');self.assertTrue(r.active);f.revoke('r1');self.assertFalse(f.get('r1').active)
 def test_black_box_replay_is_deterministic(self):
  r=BlackBoxRecorder();r.record('tool',{'name':'git','result':'ok'});r.record('verify',{'status':'PASS'});self.assertEqual(r.digest(),r.replay().digest())
if __name__=='__main__':unittest.main()
