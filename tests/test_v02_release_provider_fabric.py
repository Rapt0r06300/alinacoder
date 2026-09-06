from __future__ import annotations

from pathlib import Path
import unittest


class ProviderFabricReleaseGateTests(unittest.TestCase):
    def test_ci_requires_same_artifact_provider_fabric_evidence(self) -> None:
        workflow = Path('.github/workflows/ci.yml').read_text(encoding='utf-8')
        self.assertIn('Verify v0.2 provider fabric E2E', workflow)
        self.assertIn('scripts/verify_v02_provider_fabric.py', workflow)
        self.assertIn("AcceptanceEvidence('provider_fabric_e2e'", workflow)
        self.assertIn("'provider_fabric_e2e'", workflow)
        self.assertIn('dist/provider-fabric-evidence.json', workflow)


if __name__ == '__main__':
    unittest.main()
