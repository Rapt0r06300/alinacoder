import tempfile,unittest
from pathlib import Path
from alinacoder.desktop.core import AutomationRegistry,DesktopControlPlane,DesktopStateStore,WorkbenchModel,self_test
class Lot14DesktopTests(unittest.TestCase):
 def test_stop_pause_resume_takeover_change_backend_control_state(self):
  c=DesktopControlPlane();c.pause();self.assertEqual(c.state,'PAUSED');c.resume();self.assertEqual(c.state,'RUNNING');c.takeover();self.assertEqual(c.state,'USER_TAKEOVER');c.stop();self.assertEqual(c.state,'STOPPED')
 def test_automation_ids_are_stable_and_unique(self):
  ids=AutomationRegistry.default_ids();self.assertEqual(ids['composer'],'alinacoder.composer');self.assertEqual(len(ids.values()),len(set(ids.values())))
 def test_desktop_state_survives_restart(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'desktop.json';s=DesktopStateStore(p);s.save({'project':'repo','session':'s1','goal':'finish'});self.assertEqual(DesktopStateStore(p).load()['goal'],'finish')
 def test_essential_actions_do_not_require_external_terminal(self):
  a=WorkbenchModel().available_actions();self.assertTrue({'open_project','send_message','start_goal','pause','resume','stop','takeover','view_diff','run_tests','commit_main'}.issubset(a));self.assertNotIn('open_external_terminal',a)
 def test_packaged_self_test_contract(self):
  r=self_test();self.assertTrue(r['ok']);self.assertIn('automation_ids',r)
if __name__=='__main__':unittest.main()
