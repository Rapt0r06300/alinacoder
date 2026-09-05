from __future__ import annotations

import unittest

from alinacoder.evaluation.torture import IntegratedTortureHarness


class Lot17RealFaultInjectionTests(unittest.TestCase):
    def test_every_integrated_scenario_records_real_probe_evidence(self) -> None:
        report = IntegratedTortureHarness(seed="real-probes").run()
        self.assertGreaterEqual(len(report.results), 10)
        for result in report.results:
            self.assertTrue(result.detected, result.name)
            self.assertTrue(result.probe, result.name)
            self.assertTrue(result.evidence, result.name)
            self.assertNotEqual(result.probe, "synthetic", result.name)

    def test_campaign_exercises_multiple_real_subsystem_boundaries(self) -> None:
        report = IntegratedTortureHarness(seed="boundaries").run()
        probes = {result.probe for result in report.results}
        self.assertTrue({"state_store", "authority_firewall", "provider_control", "resource_controller", "dependency_firewall"}.issubset(probes))


if __name__ == "__main__":
    unittest.main()
