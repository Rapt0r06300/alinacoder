import unittest
from pathlib import Path
from alinacoder.supabase.core import IdempotentQueueConsumer,SupabaseMirror,reciprocal_rank_fusion
class Lot15SupabaseTests(unittest.TestCase):
 def test_rrf_combines_lexical_and_vector_without_alpha_dependency(self):self.assertEqual(reciprocal_rank_fusion([['a','b'],['b','c']])[0][0],'b')
 def test_duplicate_queue_delivery_cannot_duplicate_effect(self):
  c=IdempotentQueueConsumer();self.assertTrue(c.admit('m1',fence=2));self.assertFalse(c.admit('m1',fence=2));self.assertFalse(c.admit('m2',fence=1,minimum_fence=2))
 def test_disabled_or_unhealthy_supabase_falls_back_local(self):
  m=SupabaseMirror(False,'p1','t1');self.assertEqual(m.mode,'LOCAL_ONLY');self.assertEqual(m.write_non_secret({'kind':'memory','secret':False}),'LOCAL_ONLY');m.enabled=True;m.mark_unhealthy('network');self.assertEqual(m.mode,'LOCAL_ONLY')
 def test_cross_project_record_is_rejected(self):
  m=SupabaseMirror(True,'p1','t1')
  with self.assertRaises(PermissionError):m.validate_scope(project_id='p2',tenant_id='t1')
 def test_migration_contains_rls_vector_and_pgmq_contracts(self):
  t=(Path(__file__).parents[1]/'supabase'/'migrations'/'0001_optional_mirror.sql').read_text(encoding='utf-8').lower();self.assertIn('enable row level security',t);self.assertIn('vector',t);self.assertIn('pgmq',t)
if __name__=='__main__':unittest.main()
