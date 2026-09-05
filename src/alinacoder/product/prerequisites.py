from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse


class BootstrapError(RuntimeError):
    pass


class ManifestError(BootstrapError):
    pass


class ProvenanceError(BootstrapError):
    pass


def version_tuple(value: str) -> tuple[int, ...]:
    match = re.search(r"(\d+(?:\.\d+)+)", str(value))
    if not match:
        raise ValueError(f"unsupported version: {value}")
    return tuple(int(part) for part in match.group(1).split("."))


def version_at_least(value: str, minimum: str) -> bool:
    left = version_tuple(value)
    right = version_tuple(minimum)
    width = max(len(left), len(right))
    return left + (0,) * (width - len(left)) >= right + (0,) * (width - len(right))


@dataclass(frozen=True)
class ComponentPolicy:
    minimum_version: str
    release_api: str
    allowed_repository: str
    asset_name: str = ""
    asset_regex: str = ""
    endpoint: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ComponentPolicy":
        policy = cls(
            minimum_version=str(payload["minimum_version"]),
            release_api=str(payload["release_api"]),
            allowed_repository=str(payload["allowed_repository"]),
            asset_name=str(payload.get("asset_name", "")),
            asset_regex=str(payload.get("asset_regex", "")),
            endpoint=str(payload.get("endpoint", "")),
        )
        parsed = urlparse(policy.release_api)
        if parsed.scheme != "https" or parsed.hostname != "api.github.com":
            raise ManifestError("release APIs must use https://api.github.com")
        if "/" not in policy.allowed_repository:
            raise ManifestError("allowed_repository must be owner/repository")
        if not policy.asset_name and not policy.asset_regex:
            raise ManifestError("component policy requires an asset selector")
        return policy


@dataclass(frozen=True)
class ModelProfile:
    name: str
    model: str
    minimum_ram_gb: float
    minimum_vram_gb: float
    minimum_free_disk_gb: float
    estimated_download_gb: float
    context_tokens: int

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ModelProfile":
        return cls(
            name=str(payload["name"]),
            model=str(payload["model"]),
            minimum_ram_gb=float(payload["minimum_ram_gb"]),
            minimum_vram_gb=float(payload["minimum_vram_gb"]),
            minimum_free_disk_gb=float(payload["minimum_free_disk_gb"]),
            estimated_download_gb=float(payload["estimated_download_gb"]),
            context_tokens=int(payload["context_tokens"]),
        )


@dataclass(frozen=True)
class PrerequisiteManifest:
    schema_version: int
    product_version: str
    minimum_windows_major: int
    ollama: ComponentPolicy
    git: ComponentPolicy
    model_profiles: tuple[ModelProfile, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "PrerequisiteManifest":
        profiles = tuple(ModelProfile.from_dict(item) for item in payload.get("model_profiles", []))
        if not profiles:
            raise ManifestError("at least one model profile is required")
        if len({profile.name for profile in profiles}) != len(profiles):
            raise ManifestError("model profile names must be unique")
        return cls(
            schema_version=int(payload["schema_version"]),
            product_version=str(payload["product_version"]),
            minimum_windows_major=int(payload["minimum_windows_major"]),
            ollama=ComponentPolicy.from_dict(dict(payload["ollama"])),
            git=ComponentPolicy.from_dict(dict(payload["git"])),
            model_profiles=profiles,
        )

    @classmethod
    def load(cls, path: Path | str) -> "PrerequisiteManifest":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


@dataclass(frozen=True)
class MachineProfile:
    windows_major: int
    architecture: str
    ram_gb: float
    vram_gb: float
    disk_free_gb: float
    gpu_vendor: str = "unknown"


@dataclass(frozen=True)
class InstalledComponent:
    name: str
    version: str
    origin: str
    path: str


@dataclass(frozen=True)
class ComponentInventory:
    git: InstalledComponent | None
    ollama: InstalledComponent | None
    models: frozenset[str] = frozenset()


@dataclass(frozen=True)
class BootstrapAction:
    kind: str
    component: str
    reason: str = ""


@dataclass(frozen=True)
class BootstrapPlan:
    actions: tuple[BootstrapAction, ...]
    selected_model: ModelProfile
    ready_possible: bool
    blockers: tuple[str, ...] = ()


class ModelSelector:
    def __init__(self, manifest: PrerequisiteManifest) -> None:
        self.manifest = manifest

    @staticmethod
    def _fits(machine: MachineProfile, profile: ModelProfile) -> bool:
        return (
            machine.ram_gb >= profile.minimum_ram_gb
            and machine.vram_gb >= profile.minimum_vram_gb
            and machine.disk_free_gb >= profile.minimum_free_disk_gb
        )

    def select(self, machine: MachineProfile, override: str | None = None) -> ModelProfile:
        if machine.windows_major < self.manifest.minimum_windows_major:
            raise BootstrapError(f"Windows {self.manifest.minimum_windows_major}+ is required")
        if override:
            for profile in self.manifest.model_profiles:
                if override in {profile.name, profile.model}:
                    if not self._fits(machine, profile):
                        raise BootstrapError(f"requested model does not fit hardware: {override}")
                    return profile
            raise BootstrapError(f"unknown model profile: {override}")
        fits = [profile for profile in self.manifest.model_profiles if self._fits(machine, profile)]
        if not fits:
            raise BootstrapError("no local model profile fits available RAM/VRAM/disk")
        return max(
            fits,
            key=lambda profile: (
                profile.minimum_ram_gb,
                profile.minimum_vram_gb,
                profile.estimated_download_gb,
            ),
        )


class DependencyPlanner:
    def __init__(self, manifest: PrerequisiteManifest) -> None:
        self.manifest = manifest
        self.models = ModelSelector(manifest)

    def plan(
        self,
        machine: MachineProfile,
        inventory: ComponentInventory,
        *,
        online: bool,
        model_override: str | None = None,
    ) -> BootstrapPlan:
        selected = self.models.select(machine, model_override)
        required: list[BootstrapAction] = []
        if inventory.git is None:
            required.append(BootstrapAction("install", "git", "missing"))
        elif not version_at_least(inventory.git.version, self.manifest.git.minimum_version):
            required.append(BootstrapAction("upgrade", "git", "below minimum"))
        if inventory.ollama is None:
            required.append(BootstrapAction("install", "ollama", "missing"))
        elif not version_at_least(inventory.ollama.version, self.manifest.ollama.minimum_version):
            required.append(BootstrapAction("upgrade", "ollama", "below minimum"))
        if selected.model not in inventory.models:
            required.append(BootstrapAction("pull", "model", selected.model))
        required.append(BootstrapAction("health", "ollama", self.manifest.ollama.endpoint))
        required.append(BootstrapAction("smoke", "model", selected.model))
        if not online:
            blockers = tuple(
                f"offline:{action.component}:{action.kind}"
                for action in required
                if action.kind in {"install", "upgrade", "pull"}
            )
            if blockers:
                return BootstrapPlan(
                    actions=tuple(BootstrapAction("defer", item.split(":")[1], item) for item in blockers),
                    selected_model=selected,
                    ready_possible=False,
                    blockers=blockers,
                )
        return BootstrapPlan(tuple(required), selected, True, ())


@dataclass(frozen=True)
class ReleaseAsset:
    component: str
    repository: str
    version: str
    name: str
    url: str
    sha256: str


class OfficialReleaseResolver:
    def __init__(self, manifest: PrerequisiteManifest) -> None:
        self.manifest = manifest

    def _policy(self, component: str) -> ComponentPolicy:
        if component == "ollama":
            return self.manifest.ollama
        if component == "git":
            return self.manifest.git
        raise ProvenanceError(f"unsupported component: {component}")

    def select_asset(self, release: dict[str, Any], *, component: str) -> ReleaseAsset:
        policy = self._policy(component)
        expected_prefix = f"https://github.com/{policy.allowed_repository}/releases/"
        if not str(release.get("html_url", "")).startswith(expected_prefix):
            raise ProvenanceError("release repository does not match allow-list")
        assets = list(release.get("assets") or [])
        selected: dict[str, Any] | None = None
        for asset in assets:
            name = str(asset.get("name", ""))
            if policy.asset_name and name == policy.asset_name:
                selected = asset
                break
            if policy.asset_regex and re.fullmatch(policy.asset_regex, name):
                selected = asset
                break
        if selected is None:
            raise ProvenanceError(f"official release asset not found for {component}")
        digest = str(selected.get("digest") or "")
        if not re.fullmatch(r"sha256:[0-9a-fA-F]{64}", digest):
            raise ProvenanceError("release asset is missing a SHA-256 digest")
        url = str(selected.get("browser_download_url", ""))
        parsed = urlparse(url)
        expected_path = f"/{policy.allowed_repository}/releases/download/"
        if parsed.scheme != "https" or parsed.hostname != "github.com" or not parsed.path.startswith(expected_path):
            raise ProvenanceError("release asset URL is outside the allow-listed repository")
        tag = str(release.get("tag_name", ""))
        try:
            version = ".".join(str(part) for part in version_tuple(tag))
        except ValueError as exc:
            raise ProvenanceError("release tag does not contain a version") from exc
        return ReleaseAsset(component, policy.allowed_repository, version, str(selected["name"]), url, digest.split(":", 1)[1].lower())


@dataclass(frozen=True)
class ComponentReceipt:
    name: str
    version: str
    origin: str
    source_url: str
    sha256: str
    healthy: bool


@dataclass(frozen=True)
class BootstrapState:
    components: dict[str, ComponentReceipt]
    selected_model: str
    ready: bool
    pending: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "components": {name: asdict(receipt) for name, receipt in sorted(self.components.items())},
            "selected_model": self.selected_model,
            "ready": self.ready,
            "pending": list(self.pending),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "BootstrapState":
        return cls(
            components={name: ComponentReceipt(**dict(receipt)) for name, receipt in dict(payload.get("components", {})).items()},
            selected_model=str(payload.get("selected_model", "")),
            ready=bool(payload.get("ready", False)),
            pending=tuple(str(item) for item in payload.get("pending", [])),
        )


@dataclass(frozen=True)
class BootstrapReport:
    ready: bool
    selected_model: str
    actions: tuple[BootstrapAction, ...]
    blockers: tuple[str, ...] = ()
    state: BootstrapState | None = None


class BootstrapAdapter(Protocol):
    def detect_machine(self) -> MachineProfile: ...
    def detect_inventory(self) -> ComponentInventory: ...
    def ollama_ready(self, endpoint: str) -> bool: ...
    def smoke_model(self, endpoint: str, model: str) -> str: ...
    def persist_report(self, report: BootstrapReport) -> None: ...


class PrerequisiteBootstrapper:
    def __init__(self, manifest: PrerequisiteManifest, adapter: BootstrapAdapter) -> None:
        self.manifest = manifest
        self.adapter = adapter
        self.planner = DependencyPlanner(manifest)
        self._pending_pull_model: str | None = None

    def run(self, *, online: bool, model_override: str | None = None) -> BootstrapReport:
        machine = self.adapter.detect_machine()
        inventory = self.adapter.detect_inventory()
        plan = self.planner.plan(machine, inventory, online=online, model_override=model_override)
        blockers = list(plan.blockers)
        executed: list[BootstrapAction] = []
        if not plan.ready_possible:
            report = BootstrapReport(False, plan.selected_model.model, plan.actions, tuple(blockers))
            self.adapter.persist_report(report)
            return report
        pull_requested = any(action.kind == "pull" for action in plan.actions) or self._pending_pull_model == plan.selected_model.model
        if pull_requested:
            pull = getattr(self.adapter, "pull_model", None)
            if not callable(pull) or not bool(pull(self.manifest.ollama.endpoint, plan.selected_model.model)):
                self._pending_pull_model = plan.selected_model.model
                blockers.append("model_pull")
            else:
                self._pending_pull_model = None
                executed.append(BootstrapAction("pull", "model", plan.selected_model.model))
        ready_fn = getattr(self.adapter, "ollama_ready", None)
        if not callable(ready_fn) or not bool(ready_fn(self.manifest.ollama.endpoint)):
            blockers.append("ollama_health")
        smoke_fn = getattr(self.adapter, "smoke_model", None)
        smoke = str(smoke_fn(self.manifest.ollama.endpoint, plan.selected_model.model)) if callable(smoke_fn) else ""
        if not smoke.strip():
            blockers.append("model_smoke")
        ready = not blockers
        report = BootstrapReport(ready, plan.selected_model.model, tuple(executed or plan.actions), tuple(dict.fromkeys(blockers)))
        self.adapter.persist_report(report)
        return report


def managed_uninstall_actions(state: BootstrapState, *, purge_managed: bool) -> tuple[BootstrapAction, ...]:
    if not purge_managed:
        return ()
    return tuple(
        BootstrapAction("remove", name, "explicit managed prerequisite purge")
        for name, receipt in sorted(state.components.items())
        if receipt.origin == "managed_by_alinacoder"
    )
