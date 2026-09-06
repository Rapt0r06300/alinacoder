from __future__ import annotations

import re
import unittest
from pathlib import Path


class Lot19SetupProcessBoundaryTests(unittest.TestCase):
    def _workflow(self, name: str) -> str:
        return (Path(__file__).parents[1] / ".github" / "workflows" / name).read_text(encoding="utf-8")

    @staticmethod
    def _start_process_invocations(workflow: str, binary: str) -> list[str]:
        pattern = re.compile(r"^\s*\$[A-Za-z_][A-Za-z0-9_]*\s*=\s*Start-Process\b")
        return [line for line in workflow.splitlines() if pattern.search(line) and binary in line]

    def test_lot19_waits_for_setup_process_only_not_persistent_children(self) -> None:
        workflow = self._workflow("ci.yml")
        self.assertNotRegex(
            workflow,
            re.compile(r"(?m)^\s*&\s+\.\\dist\\AlinaCoderSetup\.exe\b"),
            "windowed AlinaCoderSetup.exe must never be invoked through the console call operator",
        )
        self.assertIn("function Invoke-Lot19Setup", workflow)
        invocations = self._start_process_invocations(workflow, "AlinaCoderSetup.exe")
        self.assertEqual(len(invocations), 1, "LOT19 must centralize setup launch in one bounded helper")
        self.assertIn("-PassThru", invocations[0])
        self.assertNotIn("-Wait", invocations[0], "Start-Process -Wait waits persistent Ollama descendants")
        self.assertIn("$process.WaitForExit($TimeoutSeconds * 1000)", workflow)
        self.assertGreaterEqual(workflow.count("Invoke-Lot19Setup -Label"), 9)

    def test_lot19_timeout_emits_process_and_receipt_diagnostics(self) -> None:
        workflow = self._workflow("ci.yml")
        self.assertIn("Get-CimInstance Win32_Process", workflow)
        self.assertIn('"install.json"', workflow)
        self.assertIn('"bootstrap-state.json"', workflow)
        self.assertIn('"bootstrap-receipt.json"', workflow)
        self.assertRegex(
            workflow,
            re.compile(
                r"LOT 19 clean Windows bootstrap E2E and lifecycle matrix\s*\n\s*timeout-minutes:\s*30",
                re.MULTILINE,
            ),
        )

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
            for line in self._start_process_invocations(workflow, "AlinaCoderSetup.exe")
            if "--installer-ui-smoke" in line
        ]
        self.assertEqual(len(waited), 1)
        self.assertIn("-Wait", waited[0])
        self.assertIn("-PassThru", waited[0])
        self.assertIn("$visibleSetup.ExitCode", workflow)


if __name__ == "__main__":
    unittest.main()
