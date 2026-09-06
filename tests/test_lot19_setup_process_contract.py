from __future__ import annotations

import re
import unittest
from pathlib import Path


class Lot19SetupProcessBoundaryTests(unittest.TestCase):
    def _workflow(self, name: str) -> str:
        return (Path(__file__).parents[1] / ".github" / "workflows" / name).read_text(encoding="utf-8")

    def test_windowed_setup_is_always_waited_in_lot19(self) -> None:
        workflow = self._workflow("ci.yml")
        self.assertNotRegex(
            workflow,
            re.compile(r"(?m)^\s*&\s+\.\\dist\\AlinaCoderSetup\.exe\b"),
            "windowed AlinaCoderSetup.exe must never be invoked as a synchronous console command",
        )
        waited = [
            line
            for line in workflow.splitlines()
            if "Start-Process" in line and "AlinaCoderSetup.exe" in line
        ]
        self.assertGreaterEqual(len(waited), 9, "every LOT19 setup lifecycle invocation must wait for the GUI process")
        for line in waited:
            self.assertIn("-Wait", line)
            self.assertIn("-PassThru", line)

    def test_setup_exit_codes_are_read_from_waited_process_objects(self) -> None:
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
            for line in workflow.splitlines()
            if "Start-Process" in line
            and "AlinaCoderSetup.exe" in line
            and "--installer-ui-smoke" in line
        ]
        self.assertEqual(len(waited), 1)
        self.assertIn("-Wait", waited[0])
        self.assertIn("-PassThru", waited[0])
        self.assertIn("$visibleSetup.ExitCode", workflow)


if __name__ == "__main__":
    unittest.main()
