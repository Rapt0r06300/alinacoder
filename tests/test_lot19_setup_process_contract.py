from __future__ import annotations

import re
import unittest
from pathlib import Path


class Lot19SetupProcessBoundaryTests(unittest.TestCase):
    def _workflow(self, name: str) -> str:
        return (Path(__file__).parents[1] / ".github" / "workflows" / name).read_text(encoding="utf-8")

    @staticmethod
    def _waited_setup_invocations(workflow: str, binary: str) -> list[str]:
        pattern = re.compile(r"^\s*\$[A-Za-z_][A-Za-z0-9_]*\s*=\s*Start-Process\b")
        return [
            line
            for line in workflow.splitlines()
            if pattern.search(line) and binary in line
        ]

    def test_lot19_uses_observable_bounded_setup_process_boundary(self) -> None:
        workflow = self._workflow("ci.yml")
        self.assertNotRegex(
            workflow,
            re.compile(r"(?m)^\s*&\s+\.\\dist\\AlinaCoderSetup\.exe\b"),
            "windowed AlinaCoderSetup.exe must never be invoked as a synchronous console command",
        )
        self.assertIn("function Invoke-Lot19Setup", workflow)
        self.assertIn('Start-Process -FilePath ".\\dist\\AlinaCoderSetup.exe"', workflow)
        self.assertIn("-PassThru", workflow)
        self.assertIn(".WaitForExit($timeoutSeconds * 1000)", workflow)
        self.assertIn("Get-CimInstance Win32_Process", workflow)
        self.assertIn('"install.json"', workflow)
        self.assertIn('"bootstrap-state.json"', workflow)
        self.assertIn('"bootstrap-receipt.json"', workflow)
        self.assertGreaterEqual(workflow.count("Invoke-Lot19Setup -Label"), 9)

    def test_setup_exit_codes_are_read_from_process_objects(self) -> None:
        workflow = self._workflow("ci.yml")
        self.assertIn("$offlineExit = $offlineSetup.ExitCode", workflow)
        self.assertNotIn("$offlineExit = $LASTEXITCODE", workflow)

    def test_release_ui_smoke_waits_for_windowed_setup(self) -> None:
        workflow = self._workflow("publish-v0.2.0.yml")
        self.assertNotRegex(
            workflow,
            re.compile(r"(?m)^\s*&\s+\.\\release\\AlinaCoderSetup\.exe\b"),
            "release smoke must wait for the windowed setup process",
        )
        waited = [
            line
            for line in self._waited_setup_invocations(workflow, "AlinaCoderSetup.exe")
            if "--installer-ui-smoke" in line
        ]
        self.assertEqual(len(waited), 1)
        self.assertIn("-Wait", waited[0])
        self.assertIn("-PassThru", waited[0])
        self.assertIn("$visibleSetup.ExitCode", workflow)


if __name__ == "__main__":
    unittest.main()
