from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from alinacoder.product import installer
from alinacoder.product.prerequisites import BootstrapError, BootstrapState, ComponentReceipt


class _Adapter:
    def __init__(self, root: Path, state: BootstrapState) -> None:
        self.state_path = root / "bootstrap-state.json"
        self.receipt_path = root / "bootstrap-receipt.json"
        self._state = state

    def load_state(self) -> BootstrapState:
        return self._state

    def ollama_ready(self, endpoint: str) -> bool:
        return True

    def persist_report(self, report) -> None:
        self._state = report.state


class _Bootstrapper:
    class _Manifest:
        class _Ollama:
            endpoint = "http://127.0.0.1:11434"
        ollama = _Ollama()

    def __init__(self, adapter: _Adapter) -> None:
        self.adapter = adapter
        self.manifest = self._Manifest()


class Lot19RollbackIdempotenceTests(unittest.TestCase):
    def test_same_version_upgrade_allows_verified_noop_rollback(self) -> None:
        state = BootstrapState(
            components={
                "ollama": ComponentReceipt(
                    "ollama",
                    "0.15.0",
                    "managed_by_alinacoder",
                    "https://github.com/ollama/ollama/releases/download/v0.15.0/OllamaSetup.exe",
                    "a" * 64,
                    True,
                )
            },
            selected_model="qwen3:0.6b",
            ready=True,
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            restored = installer.rollback(root, bootstrapper=_Bootstrapper(_Adapter(root, state)))
        self.assertEqual(restored, ())

    def test_partial_previous_provenance_is_never_treated_as_noop(self) -> None:
        state = BootstrapState(
            components={
                "ollama": ComponentReceipt(
                    "ollama",
                    "0.15.0",
                    "managed_by_alinacoder",
                    "https://github.com/ollama/ollama/releases/download/v0.15.0/OllamaSetup.exe",
                    "a" * 64,
                    True,
                    previous_version="0.14.0",
                    previous_source_url="https://github.com/ollama/ollama/releases/download/v0.14.0/OllamaSetup.exe",
                    previous_sha256="",
                )
            },
            selected_model="qwen3:0.6b",
            ready=True,
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(BootstrapError):
                installer.rollback(root, bootstrapper=_Bootstrapper(_Adapter(root, state)))


if __name__ == "__main__":
    unittest.main()
