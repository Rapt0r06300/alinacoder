from __future__ import annotations

import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alinacoder.product.prerequisites import (
    PrerequisiteManifest,
    ProvenanceError,
    ReleaseAsset,
    WindowsBootstrapAdapter,
)


class Lot19PrerequisitePrefetchCacheTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.manifest = PrerequisiteManifest.load(root / "packaging" / "prerequisites-v0.2.json")

    def _asset(self, payload: bytes, *, name: str = "OllamaSetup.exe") -> ReleaseAsset:
        return ReleaseAsset(
            component="ollama",
            repository="ollama/ollama",
            version="0.33.3",
            name=name,
            url=f"https://github.com/ollama/ollama/releases/download/v0.33.3/{name}",
            sha256=hashlib.sha256(payload).hexdigest(),
        )

    def test_matching_explicit_prefetch_cache_is_rehashed_and_avoids_network(self) -> None:
        payload = b"verified-official-release-bytes"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prefetch = root / "prefetch"
            prefetch.mkdir()
            (prefetch / "OllamaSetup.exe").write_bytes(payload)

            def network_should_not_run(_url: str) -> bytes:
                raise AssertionError("network fallback must not run for an exact cached asset")

            adapter = WindowsBootstrapAdapter(
                root / "state",
                self.manifest,
                download_bytes=network_should_not_run,
            )
            with patch.dict(os.environ, {"ALINACODER_PREREQ_CACHE_DIR": str(prefetch)}, clear=False):
                resolved = adapter.download_verified(self._asset(payload), require_authenticode=False)

            self.assertEqual(resolved.read_bytes(), payload)
            self.assertEqual(resolved.parent, adapter.cache_dir)

    def test_tampered_explicit_prefetch_cache_fails_closed_without_network_fallback(self) -> None:
        expected = b"expected-official-release-bytes"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prefetch = root / "prefetch"
            prefetch.mkdir()
            (prefetch / "OllamaSetup.exe").write_bytes(b"tampered")

            def network_should_not_run(_url: str) -> bytes:
                raise AssertionError("tampered explicit cache must fail closed, not hide behind network fallback")

            adapter = WindowsBootstrapAdapter(
                root / "state",
                self.manifest,
                download_bytes=network_should_not_run,
            )
            with patch.dict(os.environ, {"ALINACODER_PREREQ_CACHE_DIR": str(prefetch)}, clear=False):
                with self.assertRaises(ProvenanceError):
                    adapter.download_verified(self._asset(expected), require_authenticode=False)

    def test_unsafe_asset_name_is_rejected_before_cache_lookup(self) -> None:
        payload = b"payload"
        asset = self._asset(payload, name="../OllamaSetup.exe")
        with tempfile.TemporaryDirectory() as td:
            adapter = WindowsBootstrapAdapter(Path(td) / "state", self.manifest, download_bytes=lambda _url: payload)
            with patch.dict(os.environ, {"ALINACODER_PREREQ_CACHE_DIR": str(Path(td) / "prefetch")}, clear=False):
                with self.assertRaises(ProvenanceError):
                    adapter.download_verified(asset, require_authenticode=False)


if __name__ == "__main__":
    unittest.main()
