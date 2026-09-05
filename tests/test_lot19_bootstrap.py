from __future__ import annotations

import importlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_NAME = "alinacoder.product.prerequisites"
MODULE_AVAILABLE = importlib.util.find_spec(MODULE_NAME) is not None


def api():
    return importlib.import_module(MODULE_NAME)


class Lot19BootstrapContractTests(unittest.TestCase):
    def test_contract_module_exists(self) -> None:
        self.assertTrue(MODULE_AVAILABLE, "LOT 19 prerequisite bootstrap module is missing")


@unittest.skipUnless(MODULE_AVAILABLE, "LOT 19 prerequisite bootstrap module is not implemented yet")
class Lot19BootstrapBehaviorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.m = api()
        self.manifest_path = Path(__file__).resolve().parents[1] / "packaging" / "prerequisites-v0.2.json"
        self.manifest = self.m.PrerequisiteManifest.load(self.manifest_path)

    def machine(self, *, ram: float = 16, vram: float = 8, disk: float = 30):
        return self.m.MachineProfile(
            windows_major=11,
            architecture="AMD64",
            ram_gb=ram,
            vram_gb=vram,
            disk_free_gb=disk,
            gpu_vendor="NVIDIA" if vram else "CPU",
        )

    def component(self, name: str, version: str, *, origin: str = "pre_existing"):
        return self.m.InstalledComponent(name=name, version=version, origin=origin, path=f"C:/{name}/{name}.exe")

    def test_manifest_uses_only_https_official_release_apis_and_local_ollama_endpoint(self) -> None:
        self.assertEqual(self.manifest.ollama.allowed_repository, "ollama/ollama")
        self.assertEqual(self.manifest.git.allowed_repository, "git-for-windows/git")
        self.assertTrue(self.manifest.ollama.release_api.startswith("https://api.github.com/"))
        self.assertTrue(self.manifest.git.release_api.startswith("https://api.github.com/"))
        self.assertEqual(self.manifest.ollama.endpoint, "http://127.0.0.1:11434")
        self.assertGreaterEqual(len(self.manifest.model_profiles), 4)

    def test_model_selector_uses_cpu_safe_fallback_on_low_resource_machine(self) -> None:
        selected = self.m.ModelSelector(self.manifest).select(self.machine(ram=4, vram=0, disk=4))
        self.assertEqual(selected.name, "cpu-low")
        self.assertEqual(selected.model, "qwen3:0.6b")

    def test_model_selector_chooses_strongest_profile_that_fits(self) -> None:
        selected = self.m.ModelSelector(self.manifest).select(self.machine(ram=32, vram=24, disk=64))
        self.assertEqual(selected.name, "workstation-coding")
        self.assertEqual(selected.model, "qwen3-coder:30b")

    def test_clean_machine_plan_installs_git_ollama_and_model(self) -> None:
        inventory = self.m.ComponentInventory(git=None, ollama=None, models=frozenset())
        plan = self.m.DependencyPlanner(self.manifest).plan(self.machine(ram=8, vram=0, disk=10), inventory, online=True)
        kinds = [(a.kind, a.component) for a in plan.actions]
        self.assertIn(("install", "git"), kinds)
        self.assertIn(("install", "ollama"), kinds)
        self.assertIn(("pull", "model"), kinds)
        self.assertTrue(plan.ready_possible)

    def test_preexisting_compatible_components_are_preserved(self) -> None:
        inventory = self.m.ComponentInventory(
            git=self.component("git", "2.51.0"),
            ollama=self.component("ollama", "0.33.3"),
            models=frozenset({"qwen3:4b"}),
        )
        plan = self.m.DependencyPlanner(self.manifest).plan(self.machine(ram=8, vram=0, disk=10), inventory, online=True)
        destructive = [a for a in plan.actions if a.kind in {"install", "upgrade", "remove"}]
        self.assertEqual(destructive, [])
        self.assertIn("qwen3:4b", plan.selected_model.model)

    def test_old_ollama_is_upgraded_but_never_downgraded(self) -> None:
        old = self.m.ComponentInventory(
            git=self.component("git", "2.51.0"),
            ollama=self.component("ollama", "0.10.0"),
            models=frozenset(),
        )
        plan = self.m.DependencyPlanner(self.manifest).plan(self.machine(), old, online=True)
        self.assertTrue(any(a.kind == "upgrade" and a.component == "ollama" for a in plan.actions))
        newer = self.m.ComponentInventory(
            git=self.component("git", "2.51.0"),
            ollama=self.component("ollama", "99.0.0"),
            models=frozenset(),
        )
        newer_plan = self.m.DependencyPlanner(self.manifest).plan(self.machine(), newer, online=True)
        self.assertFalse(any(a.kind == "upgrade" and a.component == "ollama" for a in newer_plan.actions))

    def test_offline_plan_is_explicitly_deferred_and_not_ready(self) -> None:
        inventory = self.m.ComponentInventory(git=None, ollama=None, models=frozenset())
        plan = self.m.DependencyPlanner(self.manifest).plan(self.machine(), inventory, online=False)
        self.assertFalse(plan.ready_possible)
        self.assertTrue(plan.blockers)
        self.assertTrue(all(a.kind == "defer" for a in plan.actions))

    def test_release_resolver_rejects_wrong_repo_or_missing_digest(self) -> None:
        resolver = self.m.OfficialReleaseResolver(self.manifest)
        wrong_repo = {
            "html_url": "https://github.com/evil/ollama/releases/tag/v1",
            "tag_name": "v1.0.0",
            "assets": [{"name": "OllamaSetup.exe", "browser_download_url": "https://github.com/evil/ollama/x.exe", "digest": "sha256:" + "a" * 64}],
        }
        with self.assertRaises(self.m.ProvenanceError):
            resolver.select_asset(wrong_repo, component="ollama")
        missing_digest = {
            "html_url": "https://github.com/ollama/ollama/releases/tag/v0.33.3",
            "tag_name": "v0.33.3",
            "assets": [{"name": "OllamaSetup.exe", "browser_download_url": "https://github.com/ollama/ollama/releases/download/v0.33.3/OllamaSetup.exe", "digest": None}],
        }
        with self.assertRaises(self.m.ProvenanceError):
            resolver.select_asset(missing_digest, component="ollama")

    def test_bootstrap_requires_real_model_smoke_before_ready(self) -> None:
        class FakeAdapter:
            def __init__(self):
                self.saved = None
            def detect_machine(self): return self_outer.machine(ram=4, vram=0, disk=5)
            def detect_inventory(self): return self_outer.m.ComponentInventory(
                git=self_outer.component("git", "2.51.0"),
                ollama=self_outer.component("ollama", "0.33.3"),
                models=frozenset({"qwen3:0.6b"}),
            )
            def ollama_ready(self, endpoint): return True
            def smoke_model(self, endpoint, model): return ""
            def persist_report(self, report): self.saved = report
        self_outer = self
        adapter = FakeAdapter()
        report = self.m.PrerequisiteBootstrapper(self.manifest, adapter).run(online=True)
        self.assertFalse(report.ready)
        self.assertIn("model_smoke", report.blockers)
        self.assertIsNotNone(adapter.saved)

    def test_interrupted_model_pull_can_resume_without_reinstalling_prerequisites(self) -> None:
        class FakeAdapter:
            def __init__(self): self.pull_calls = 0; self.installs = []
            def detect_machine(self): return self_outer.machine(ram=4, vram=0, disk=5)
            def detect_inventory(self):
                models = frozenset({"qwen3:0.6b"}) if self.pull_calls > 0 else frozenset()
                return self_outer.m.ComponentInventory(
                    git=self_outer.component("git", "2.51.0"),
                    ollama=self_outer.component("ollama", "0.33.3"), models=models)
            def ollama_ready(self, endpoint): return True
            def pull_model(self, endpoint, model): self.pull_calls += 1; return self.pull_calls > 1
            def smoke_model(self, endpoint, model): return "ok" if self.pull_calls > 1 else ""
            def persist_report(self, report): pass
        self_outer = self
        adapter = FakeAdapter()
        first = self.m.PrerequisiteBootstrapper(self.manifest, adapter).run(online=True)
        second = self.m.PrerequisiteBootstrapper(self.manifest, adapter).run(online=True)
        self.assertFalse(first.ready)
        self.assertTrue(second.ready)
        self.assertEqual(adapter.pull_calls, 2)
        self.assertEqual(adapter.installs, [])

    def test_uninstall_policy_never_removes_preexisting_dependencies(self) -> None:
        state = self.m.BootstrapState(
            components={
                "ollama": self.m.ComponentReceipt("ollama", "0.33.3", "pre_existing", "", "", True),
                "git": self.m.ComponentReceipt("git", "2.51.0", "managed_by_alinacoder", "https://example.invalid/git.exe", "a" * 64, True),
            },
            selected_model="qwen3:0.6b",
            ready=True,
        )
        actions = self.m.managed_uninstall_actions(state, purge_managed=True)
        self.assertNotIn("ollama", {a.component for a in actions})
        self.assertIn("git", {a.component for a in actions})

    def test_state_round_trip_is_atomic_json_contract(self) -> None:
        state = self.m.BootstrapState(components={}, selected_model="qwen3:0.6b", ready=False, pending=("network",))
        payload = state.as_dict()
        rebuilt = self.m.BootstrapState.from_dict(json.loads(json.dumps(payload)))
        self.assertEqual(rebuilt.selected_model, state.selected_model)
        self.assertEqual(rebuilt.pending, ("network",))


if __name__ == "__main__":
    unittest.main()
