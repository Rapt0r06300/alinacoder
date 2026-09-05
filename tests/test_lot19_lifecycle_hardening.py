from __future__ import annotations

import unittest

from alinacoder.product import installer
from alinacoder.product import prerequisites as p


class Lot19RollbackHardeningTests(unittest.TestCase):
    def test_rollback_is_allowed_only_for_managed_component_with_exact_previous_provenance(self) -> None:
        state = p.BootstrapState(
            components={
                "ollama": p.ComponentReceipt(
                    "ollama", "0.33.3", "managed_by_alinacoder",
                    "https://github.com/ollama/ollama/releases/download/v0.33.3/OllamaSetup.exe",
                    "a" * 64, True,
                    previous_version="0.32.0",
                    previous_source_url="https://github.com/ollama/ollama/releases/download/v0.32.0/OllamaSetup.exe",
                    previous_sha256="b" * 64,
                ),
                "git": p.ComponentReceipt(
                    "git", "2.55.0", "pre_existing", "", "", True,
                    previous_version="2.54.0",
                    previous_source_url="https://github.com/git-for-windows/git/releases/download/v2.54.0.windows.1/Git-2.54.0-64-bit.exe",
                    previous_sha256="c" * 64,
                ),
            },
            selected_model="qwen3:0.6b",
            ready=True,
        )
        actions = p.managed_rollback_actions(state)
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].component, "ollama")
        self.assertEqual(actions[0].target_version, "0.32.0")
        self.assertEqual(actions[0].sha256, "b" * 64)

    def test_rollback_refuses_managed_component_without_exact_previous_digest(self) -> None:
        state = p.BootstrapState(
            components={
                "ollama": p.ComponentReceipt(
                    "ollama", "0.33.3", "managed_by_alinacoder", "https://example.invalid/current", "a" * 64, True,
                    previous_version="0.32.0", previous_source_url="https://example.invalid/old", previous_sha256="",
                )
            },
            selected_model="qwen3:0.6b",
            ready=True,
        )
        self.assertEqual(p.managed_rollback_actions(state), ())

    def test_installer_exposes_explicit_rollback_lifecycle(self) -> None:
        self.assertTrue(hasattr(installer, "rollback"))


if __name__ == "__main__":
    unittest.main()
