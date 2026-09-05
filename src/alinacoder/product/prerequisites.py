from __future__ import annotations

import ctypes
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Protocol
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
    path: str = ""
    previous_version: str = ""
    previous_source_url: str = ""
    previous_sha256: str = ""


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
    def install_component(self, component: str, *, operation: str) -> ComponentReceipt: ...
    def ollama_ready(self, endpoint: str) -> bool: ...
    def pull_model(self, endpoint: str, model: str) -> bool: ...
    def smoke_model(self, endpoint: str, model: str) -> str: ...
    def persist_report(self, report: BootstrapReport) -> None: ...


def _json_bytes(url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": "AlinaCoder/0.2", "Content-Type": "application/json"},
        method="GET" if payload is None else "POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


class WindowsBootstrapAdapter:
    """Windows side-effect boundary for verified prerequisite bootstrap.

    Pure planning remains outside this class. All remote installers are resolved from
    allow-listed GitHub release APIs and validated against the release asset SHA-256.
    """

    def __init__(
        self,
        state_dir: Path | str,
        manifest: PrerequisiteManifest,
        *,
        download_bytes: Callable[[str], bytes] | None = None,
        command_runner: Callable[..., tuple[int, str]] | None = None,
        json_loader: Callable[[str], dict[str, Any]] | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir = self.state_dir / ".bootstrap-cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.manifest = manifest
        self.resolver = OfficialReleaseResolver(manifest)
        self._download_bytes = download_bytes
        self._command_runner = command_runner or self._default_command_runner
        self._json_loader = json_loader or (lambda url: _json_bytes(url))
        self._sleep = sleep
        self._last_install_receipts: dict[str, ComponentReceipt] = {}

    @property
    def state_path(self) -> Path:
        return self.state_dir / "bootstrap-state.json"

    @property
    def receipt_path(self) -> Path:
        return self.state_dir / "bootstrap-receipt.json"

    def _policy(self, component: str) -> ComponentPolicy:
        if component == "ollama":
            return self.manifest.ollama
        if component == "git":
            return self.manifest.git
        raise BootstrapError(f"unsupported prerequisite component: {component}")

    def _default_command_runner(self, args: list[str], *, timeout: int = 300) -> tuple[int, str]:
        completed = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return completed.returncode, completed.stdout or ""

    def _run(self, args: list[str], *, timeout: int = 300) -> tuple[int, str]:
        try:
            return self._command_runner(args, timeout=timeout)
        except TypeError:
            return self._command_runner(args)

    def latest_asset(self, component: str) -> ReleaseAsset:
        policy = self._policy(component)
        return self.resolver.select_asset(self._json_loader(policy.release_api), component=component)

    def download_verified(self, asset: ReleaseAsset, *, require_authenticode: bool = True) -> Path:
        target = self.cache_dir / asset.name
        temporary = target.with_suffix(target.suffix + ".partial")
        temporary.unlink(missing_ok=True)
        digest = hashlib.sha256()
        if self._download_bytes is not None:
            data = self._download_bytes(asset.url)
            digest.update(data)
            temporary.write_bytes(data)
        else:
            parsed = urlparse(asset.url)
            if parsed.scheme != "https" or parsed.hostname != "github.com":
                raise ProvenanceError("downloads are restricted to HTTPS GitHub release assets")
            request = urllib.request.Request(asset.url, headers={"User-Agent": "AlinaCoder/0.2"})
            with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as handle:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    handle.write(chunk)
        actual = digest.hexdigest()
        if actual.lower() != asset.sha256.lower():
            temporary.unlink(missing_ok=True)
            raise ProvenanceError(f"SHA-256 mismatch for {asset.name}")
        if require_authenticode and asset.name.lower().endswith(".exe") and os.name == "nt":
            if not self.verify_authenticode(temporary):
                temporary.unlink(missing_ok=True)
                raise ProvenanceError(f"Authenticode validation failed for {asset.name}")
        temporary.replace(target)
        return target

    def verify_authenticode(self, path: Path | str) -> bool:
        escaped = str(Path(path)).replace("'", "''")
        command = [
            "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
            f"(Get-AuthenticodeSignature -LiteralPath '{escaped}').Status.ToString()",
        ]
        code, output = self._run(command, timeout=60)
        return code == 0 and output.strip().lower() == "valid"

    def _ignore_component(self, name: str) -> bool:
        ignored = {item.strip().lower() for item in os.environ.get("ALINACODER_BOOTSTRAP_IGNORE_EXISTING", "").split(",") if item.strip()}
        return name.lower() in ignored

    def _candidate_executables(self, name: str) -> tuple[Path, ...]:
        candidates: list[Path] = []
        discovered = shutil.which(name)
        if discovered:
            candidates.append(Path(discovered))
        local = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
        program_files = Path(os.environ.get("ProgramFiles", "C:/Program Files"))
        if name == "ollama":
            candidates.extend((local / "Programs" / "Ollama" / "ollama.exe", program_files / "Ollama" / "ollama.exe"))
        elif name == "git":
            candidates.extend((program_files / "Git" / "cmd" / "git.exe", local / "Programs" / "Git" / "cmd" / "git.exe"))
        unique: list[Path] = []
        for candidate in candidates:
            if candidate not in unique:
                unique.append(candidate)
        return tuple(unique)

    def _find_executable(self, name: str) -> Path | None:
        if self._ignore_component(name):
            return None
        for candidate in self._candidate_executables(name):
            if candidate.exists():
                return candidate
        return None

    def _component_version(self, name: str, path: Path) -> str:
        args = [str(path), "--version"]
        code, output = self._run(args, timeout=30)
        if code != 0:
            return "0.0.0"
        try:
            return ".".join(str(item) for item in version_tuple(output))
        except ValueError:
            return "0.0.0"

    def load_state(self) -> BootstrapState | None:
        if not self.state_path.exists():
            return None
        try:
            return BootstrapState.from_dict(json.loads(self.state_path.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return None

    def _origin_for(self, name: str, version: str) -> str:
        state = self.load_state()
        receipt = state.components.get(name) if state else None
        if receipt and receipt.origin == "managed_by_alinacoder" and receipt.version == version:
            return "managed_by_alinacoder"
        return "pre_existing"

    def detect_inventory(self) -> ComponentInventory:
        git_path = self._find_executable("git")
        ollama_path = self._find_executable("ollama")
        git = None
        ollama = None
        if git_path:
            version = self._component_version("git", git_path)
            git = InstalledComponent("git", version, self._origin_for("git", version), str(git_path))
        if ollama_path:
            version = self._component_version("ollama", ollama_path)
            ollama = InstalledComponent("ollama", version, self._origin_for("ollama", version), str(ollama_path))
        models: set[str] = set()
        if ollama_path:
            code, output = self._run([str(ollama_path), "list"], timeout=60)
            if code == 0:
                for line in output.splitlines()[1:]:
                    parts = line.split()
                    if parts:
                        models.add(parts[0])
        return ComponentInventory(git, ollama, frozenset(models))

    def _ram_gb(self) -> float:
        if os.name != "nt":
            return 8.0
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        status = MemoryStatus()
        status.dwLength = ctypes.sizeof(MemoryStatus)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return 8.0
        return round(status.ullTotalPhys / (1024 ** 3), 2)

    def _gpu_profile(self) -> tuple[str, float]:
        nvidia = shutil.which("nvidia-smi")
        if nvidia:
            code, output = self._run([nvidia, "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], timeout=30)
            if code == 0 and output.strip():
                first = output.splitlines()[0]
                name, _, memory = first.rpartition(",")
                try:
                    return name.strip() or "NVIDIA", round(float(memory.strip()) / 1024, 2)
                except ValueError:
                    pass
        return "CPU", 0.0

    def detect_machine(self) -> MachineProfile:
        if os.name == "nt" and hasattr(sys, "getwindowsversion"):
            windows_major = int(sys.getwindowsversion().major)
        else:
            windows_major = self.manifest.minimum_windows_major
        try:
            disk = shutil.disk_usage(self.state_dir).free / (1024 ** 3)
        except OSError:
            disk = 0.0
        gpu, vram = self._gpu_profile()
        return MachineProfile(
            windows_major=windows_major,
            architecture=platform.machine() or "unknown",
            ram_gb=self._ram_gb(),
            vram_gb=vram,
            disk_free_gb=round(disk, 2),
            gpu_vendor=gpu,
        )

    def install_component(self, component: str, *, operation: str) -> ComponentReceipt:
        policy = self._policy(component)
        asset = self.latest_asset(component)
        if not version_at_least(asset.version, policy.minimum_version):
            raise ProvenanceError(f"latest {component} release is below required minimum")
        previous_inventory = self.detect_inventory()
        previous = previous_inventory.git if component == "git" else previous_inventory.ollama
        installer = self.download_verified(asset, require_authenticode=True)
        if component == "git":
            args = [str(installer), "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CURRENTUSER"]
        else:
            args = [str(installer), "/VERYSILENT", "/NORESTART"]
        code, output = self._run(args, timeout=1800)
        if code not in (0, 3010):
            raise BootstrapError(f"{component} {operation} failed with exit code {code}: {output[-500:]}")
        receipt = ComponentReceipt(
            name=component,
            version=asset.version,
            origin="managed_by_alinacoder",
            source_url=asset.url,
            sha256=asset.sha256,
            healthy=True,
            previous_version=previous.version if previous else "",
        )
        self._last_install_receipts[component] = receipt
        return receipt

    def _ollama_executable(self) -> Path | None:
        return self._find_executable("ollama")

    def start_ollama(self) -> bool:
        executable = self._ollama_executable()
        if executable is None:
            return False
        try:
            subprocess.Popen(
                [str(executable), "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0),
            )
            return True
        except OSError:
            return False

    def ollama_ready(self, endpoint: str) -> bool:
        try:
            payload = _json_bytes(endpoint.rstrip("/") + "/api/tags")
            return isinstance(payload.get("models", []), list)
        except (OSError, ValueError, urllib.error.URLError, TimeoutError):
            return False

    def wait_ollama(self, endpoint: str, *, attempts: int = 30) -> bool:
        if self.ollama_ready(endpoint):
            return True
        self.start_ollama()
        for attempt in range(attempts):
            if self.ollama_ready(endpoint):
                return True
            self._sleep(min(0.25 * (attempt + 1), 2.0))
        return False

    def pull_model(self, endpoint: str, model: str) -> bool:
        executable = self._ollama_executable()
        if executable is None:
            return False
        code, _ = self._run([str(executable), "pull", model], timeout=7200)
        if code != 0:
            return False
        inventory = self.detect_inventory()
        return model in inventory.models

    def smoke_model(self, endpoint: str, model: str) -> str:
        try:
            payload = _json_bytes(
                endpoint.rstrip("/") + "/api/generate",
                {"model": model, "prompt": "Reply only with OK.", "stream": False, "options": {"num_predict": 8}},
            )
            return str(payload.get("response", "")).strip()
        except (OSError, ValueError, urllib.error.URLError, TimeoutError):
            return ""

    def _atomic_write_json(self, path: Path, payload: dict[str, Any]) -> None:
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        temporary.replace(path)

    def persist_report(self, report: BootstrapReport) -> None:
        state = report.state or BootstrapState({}, report.selected_model, report.ready, report.blockers)
        self._atomic_write_json(self.state_path, state.as_dict())
        self._atomic_write_json(
            self.receipt_path,
            {
                "ready": report.ready,
                "selected_model": report.selected_model,
                "blockers": list(report.blockers),
                "actions": [asdict(action) for action in report.actions],
                "state": state.as_dict(),
            },
        )

    def managed_uninstall(self, *, purge: bool = False) -> tuple[str, ...]:
        state = self.load_state()
        if not state or not purge:
            return ()
        removed: list[str] = []
        for action in managed_uninstall_actions(state, purge_managed=True):
            executable = self._find_executable(action.component)
            if executable is None:
                continue
            directory = executable.parent.parent if executable.parent.name.lower() == "cmd" else executable.parent
            uninstallers = list(directory.glob("unins*.exe")) + [directory / "uninstall.exe"]
            uninstaller = next((item for item in uninstallers if item.exists()), None)
            if uninstaller is None:
                continue
            code, _ = self._run([str(uninstaller), "/VERYSILENT", "/NORESTART"], timeout=900)
            if code in (0, 3010):
                removed.append(action.component)
        return tuple(removed)


class PrerequisiteBootstrapper:
    def __init__(self, manifest: PrerequisiteManifest, adapter: BootstrapAdapter) -> None:
        self.manifest = manifest
        self.adapter = adapter
        self.planner = DependencyPlanner(manifest)

    @staticmethod
    def _preexisting_receipt(component: InstalledComponent | None) -> ComponentReceipt | None:
        if component is None:
            return None
        return ComponentReceipt(component.name, component.version, component.origin, "", "", True, path=component.path)

    def run(self, *, online: bool, model_override: str | None = None) -> BootstrapReport:
        machine = self.adapter.detect_machine()
        initial = self.adapter.detect_inventory()
        plan = self.planner.plan(machine, initial, online=online, model_override=model_override)
        blockers = list(plan.blockers)
        executed: list[BootstrapAction] = []
        receipts: dict[str, ComponentReceipt] = {}
        git_receipt = self._preexisting_receipt(initial.git)
        ollama_receipt = self._preexisting_receipt(initial.ollama)
        if git_receipt:
            receipts["git"] = git_receipt
        if ollama_receipt:
            receipts["ollama"] = ollama_receipt
        if not plan.ready_possible:
            state = BootstrapState(receipts, plan.selected_model.model, False, tuple(blockers))
            report = BootstrapReport(False, plan.selected_model.model, plan.actions, tuple(blockers), state)
            self.adapter.persist_report(report)
            return report
        for action in plan.actions:
            if action.kind not in {"install", "upgrade"}:
                continue
            installer = getattr(self.adapter, "install_component", None)
            if not callable(installer):
                blockers.append(f"{action.component}_{action.kind}")
                continue
            try:
                receipt = installer(action.component, operation=action.kind)
            except BootstrapError:
                blockers.append(f"{action.component}_{action.kind}")
                continue
            receipts[action.component] = receipt
            executed.append(action)
        current = self.adapter.detect_inventory()
        if current.git is None or not version_at_least(current.git.version, self.manifest.git.minimum_version):
            blockers.append("git_health")
        if current.ollama is None or not version_at_least(current.ollama.version, self.manifest.ollama.minimum_version):
            blockers.append("ollama_version")
        wait = getattr(self.adapter, "wait_ollama", None)
        if callable(wait):
            healthy = bool(wait(self.manifest.ollama.endpoint))
        else:
            healthy = bool(self.adapter.ollama_ready(self.manifest.ollama.endpoint))
        if not healthy:
            blockers.append("ollama_health")
        needs_pull = plan.selected_model.model not in current.models
        pulled_by_us = False
        if needs_pull:
            pull = getattr(self.adapter, "pull_model", None)
            if not callable(pull) or not bool(pull(self.manifest.ollama.endpoint, plan.selected_model.model)):
                blockers.append("model_pull")
            else:
                pulled_by_us = True
                executed.append(BootstrapAction("pull", "model", plan.selected_model.model))
        smoke_fn = getattr(self.adapter, "smoke_model", None)
        smoke = str(smoke_fn(self.manifest.ollama.endpoint, plan.selected_model.model)) if callable(smoke_fn) else ""
        if not smoke.strip():
            blockers.append("model_smoke")
        refreshed = self.adapter.detect_inventory()
        for name, component in (("git", refreshed.git), ("ollama", refreshed.ollama)):
            if name not in receipts and component:
                receipt = self._preexisting_receipt(component)
                if receipt:
                    receipts[name] = receipt
        receipts[f"model:{plan.selected_model.model}"] = ComponentReceipt(
            name=f"model:{plan.selected_model.model}",
            version=plan.selected_model.model,
            origin="managed_by_alinacoder" if pulled_by_us else "pre_existing",
            source_url=self.manifest.ollama.endpoint,
            sha256="",
            healthy=bool(smoke.strip()),
        )
        unique_blockers = tuple(dict.fromkeys(blockers))
        ready = not unique_blockers
        state = BootstrapState(receipts, plan.selected_model.model, ready, unique_blockers)
        report = BootstrapReport(ready, plan.selected_model.model, tuple(executed or plan.actions), unique_blockers, state)
        self.adapter.persist_report(report)
        return report

    def managed_uninstall(self, *, purge: bool = False) -> tuple[str, ...]:
        action = getattr(self.adapter, "managed_uninstall", None)
        return tuple(action(purge=purge)) if callable(action) else ()


def managed_uninstall_actions(state: BootstrapState, *, purge_managed: bool) -> tuple[BootstrapAction, ...]:
    if not purge_managed:
        return ()
    return tuple(
        BootstrapAction("remove", name, "explicit managed prerequisite purge")
        for name, receipt in sorted(state.components.items())
        if receipt.origin == "managed_by_alinacoder" and not name.startswith("model:")
    )
