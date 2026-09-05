import unittest
from alinacoder.resources.core import HardwareFitProfile,HardwareProfile,LocalModel,LocalModelDiscovery,PerformanceGate,ResourceController,ResourceMode
class Lot13ResourceTests(unittest.TestCase):
 def test_pressure_requires_hysteresis_before_downgrade(self):
  c=ResourceController(mode=ResourceMode.BALANCED,pressure_samples=2,recovery_samples=2);self.assertEqual(c.observe_pressure(.95),ResourceMode.BALANCED);self.assertEqual(c.observe_pressure(.95),ResourceMode.CONSERVATIVE);self.assertEqual(c.observe_pressure(.2),ResourceMode.CONSERVATIVE);self.assertEqual(c.observe_pressure(.2),ResourceMode.BALANCED)
 def test_hardware_fit_rejects_model_that_cannot_fit(self):
  p=HardwareFitProfile(HardwareProfile(32,8,8,'GPU'));self.assertFalse(p.fits(LocalModel('huge',40,16,.95)));self.assertTrue(p.fits(LocalModel('small',8,6,.7)))
 def test_selects_strongest_local_model_that_fits(self):
  p=HardwareFitProfile(HardwareProfile(32,12,8,'GPU'));models=[LocalModel('m1',8,4,.6),LocalModel('m2',16,10,.9),LocalModel('m3',48,24,.99)];self.assertEqual(p.select(models).name,'m2')
 def test_ollama_payload_discovery_is_local_and_deterministic(self):self.assertEqual(LocalModelDiscovery.from_ollama_payload({'models':[{'name':'qwen:test','size':8000000000}]})[0].name,'qwen:test')
 def test_performance_gate_detects_median_regression(self):
  g=PerformanceGate(1.2);self.assertTrue(g.passes([1,1.1,1],[1.1,1.2,1.1]));self.assertFalse(g.passes([1,1,1],[1.5,1.6,1.5]))
if __name__=='__main__':unittest.main()
