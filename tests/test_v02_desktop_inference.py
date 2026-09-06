from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from alinacoder.desktop.workbench import DesktopWorkbench
from alinacoder.intelligence_mesh.providers import ProviderResponse


class FakeFabric:
    def __init__(self, responses: list[ProviderResponse]) -> None:
        self.responses = list(responses)
        self.calls: list[dict[str, object]] = []

    def complete(self, messages, requirement, *, mode):
        self.calls.append({"messages": [dict(item) for item in messages], "minimums": dict(requirement.minimums), "mode": mode})
        return self.responses.pop(0)


class DesktopInferenceIntegrationTests(unittest.TestCase):
    def test_send_message_calls_fabric_and_persists_assistant_route_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fabric = FakeFabric([ProviderResponse("Bonjour depuis le cloud", "openrouter", "strong:free", quota_remaining=4)])
            workbench = DesktopWorkbench(
                Path(td),
                state_path=Path(td) / "state.sqlite",
                inference_fabric=fabric,
                inference_mode="hybrid",
            )
            receipt = workbench.send_message("Bonjour")
            snapshot = workbench.snapshot()
            workbench.close()

        self.assertEqual(fabric.calls[0]["mode"], "hybrid")
        self.assertEqual(fabric.calls[0]["messages"], [{"role": "user", "content": "Bonjour"}])
        self.assertEqual(snapshot["transcript"][0], {"role": "user", "text": "Bonjour"})
        self.assertEqual(snapshot["transcript"][1]["role"], "assistant")
        self.assertEqual(snapshot["transcript"][1]["text"], "Bonjour depuis le cloud")
        self.assertEqual(snapshot["transcript"][1]["provider_id"], "openrouter")
        self.assertEqual(snapshot["transcript"][1]["model_id"], "strong:free")
        self.assertEqual(receipt["details"]["assistant_text"], "Bonjour depuis le cloud")
        self.assertEqual(receipt["details"]["provider_id"], "openrouter")

    def test_provider_switch_receives_complete_canonical_conversation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fabric = FakeFabric(
                [
                    ProviderResponse("Réponse A", "openrouter", "a:free", quota_remaining=0),
                    ProviderResponse("Réponse B", "zai", "glm-4.7-flash", quota_remaining=10),
                ]
            )
            workbench = DesktopWorkbench(
                Path(td),
                state_path=Path(td) / "state.sqlite",
                inference_fabric=fabric,
                inference_mode="free-cloud",
            )
            workbench.send_message("Premier tour")
            workbench.send_message("Deuxième tour")
            snapshot = workbench.snapshot()
            workbench.close()

        self.assertEqual(
            fabric.calls[1]["messages"],
            [
                {"role": "user", "content": "Premier tour"},
                {"role": "assistant", "content": "Réponse A"},
                {"role": "user", "content": "Deuxième tour"},
            ],
        )
        self.assertEqual(snapshot["transcript"][-1]["provider_id"], "zai")
        self.assertEqual(snapshot["transcript"][-1]["model_id"], "glm-4.7-flash")

    def test_legacy_headless_workbench_remains_non_inferencing_when_no_fabric_is_supplied(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workbench = DesktopWorkbench(Path(td), state_path=Path(td) / "state.sqlite")
            receipt = workbench.send_message("Headless acceptance")
            snapshot = workbench.snapshot()
            workbench.close()
        self.assertEqual(snapshot["transcript"], [{"role": "user", "text": "Headless acceptance"}])
        self.assertEqual(receipt["details"], {"text": "Headless acceptance"})


if __name__ == "__main__":
    unittest.main()
