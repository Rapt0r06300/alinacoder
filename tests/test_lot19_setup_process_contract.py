from __future__ import annotations

import re
import unittest
from pathlib import Path


class Lot19SetupProcessBoundaryTests(unittest.TestCase):
    def test_windowed_setup_is_always_waited_in_lot19(self) -> None:
        workflow = (Path(__file__).parents[1] / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
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
        workflow = (Path(__file__).parents[1] / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("$offlineExit = $offlineSetup.ExitCode", workflow)
        self.assertNotIn("$offlineExit = $LASTEXITCODE", workflow)


if __name__ == "__main__":
    unittest.main()
