from __future__ import annotations

from pathlib import Path
import unittest


class ReleasePublicationWorkflowTests(unittest.TestCase):
    def test_successful_ci_republishes_exact_verified_v020_artifacts(self) -> None:
        path = Path('.github/workflows/publish-v0.2.0.yml')
        self.assertTrue(path.is_file())
        workflow = path.read_text(encoding='utf-8')
        for required in (
            'workflow_run:',
            'contents: write',
            'gh run download',
            'final-acceptance-evidence.json',
            'provider-fabric-evidence.json',
            "runtime_v0_2_ready",
            "provider_fabric_e2e",
            'git/refs/tags/v0.2.0',
            'gh release upload v0.2.0',
            '--clobber',
            'AlinaCoder-v0.2.0.zip',
        ):
            self.assertIn(required, workflow)


if __name__ == '__main__':
    unittest.main()
