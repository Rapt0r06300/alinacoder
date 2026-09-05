import unittest
from alinacoder.orchestration.core import AgentSpec,CouncilPolicy,FencingRegistry,IndependentVoteAggregator,ProposedChange,SemanticConflictDetector,TopologyRouter
class Lot11OrchestrationTests(unittest.TestCase):
 def test_zombie_agent_is_rejected_after_new_fence(self):
  f=FencingRegistry();a=f.issue('repo');b=f.issue('repo');self.assertFalse(f.validate('repo',a));self.assertTrue(f.validate('repo',b))
 def test_same_lineage_is_one_cognitive_vote(self):
  votes=[(AgentSpec('a','verify','lineage-x','p1'),'PASS',.8),(AgentSpec('b','verify','lineage-x','p2'),'PASS',.9),(AgentSpec('c','security','lineage-y','p3'),'FAIL',.95)];r=IndependentVoteAggregator().aggregate(votes);self.assertEqual(r.independent_votes,2);self.assertEqual(r.verdict,'FAIL')
 def test_semantic_api_conflict_is_detected_across_files(self):
  c=[ProposedChange('a','src/api.py',exports={'foo':'foo(x: int)'}),ProposedChange('b','src/client.py',requires={'foo':'foo(x: str)'})];r=SemanticConflictDetector().detect(c);self.assertEqual(len(r),1);self.assertEqual(r[0].symbol,'foo')
 def test_council_runs_only_when_expected_value_exceeds_cost(self):
  p=CouncilPolicy(.05);self.assertTrue(p.should_debate(expected_terminal_gain=.25,criticality=1,latency_cost=.05,resource_cost=.05));self.assertFalse(p.should_debate(expected_terminal_gain=.05,criticality=1,latency_cost=.03,resource_cost=.03))
 def test_topology_router_uses_parallel_only_for_low_coupling_independent_work(self):
  r=TopologyRouter();self.assertEqual(r.route(nodes=['a','b'],edges=[],coupling=.1),'parallel');self.assertEqual(r.route(nodes=['a','b'],edges=[],coupling=.9),'sequential');self.assertEqual(r.route(nodes=['a','b'],edges=[('a','b')],coupling=.2),'sequential')
if __name__=='__main__':unittest.main()
