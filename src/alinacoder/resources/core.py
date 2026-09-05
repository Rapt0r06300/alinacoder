from __future__ import annotations

import statistics
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class ResourceMode(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    PERFORMANCE = "PERFORMANCE"


@dataclass(frozen=True)
class HardwareProfile:
    ram_gb: float
    vram_gb: float
    cpu_cores: int
    gpu_name: str = ""


@dataclass(frozen=True)
class DynamicLoadSnapshot:
    ram_pressure: float
    vram_pressure: float
    cpu_pressure: float
    gpu_pressure: float
    thermal_pressure: float = 0.0

    @property
    def max_pressure(self) -> float:
        return max(
            self.ram_pressure,
            self.vram_pressure,
            self.cpu_pressure,
            self.gpu_pressure,
            self.thermal_pressure,
        )


@dataclass(frozen=True)
class LocalModel:
    name: str
    required_ram_gb: float
    required_vram_gb: float
    capability: float
    context_tokens: int = 8192
    runtime: str = "ollama"


class HardwareFitProfile:
    def __init__(self, hardware: HardwareProfile, headroom_ratio: float = 0.9) -> None:
        self.hardware = hardware
        self.headroom_ratio = headroom_ratio

    def fits(self, model: LocalModel) -> bool:
        return (
            model.required_ram_gb <= self.hardware.ram_gb * self.headroom_ratio
            and model.required_vram_gb <= self.hardware.vram_gb * self.headroom_ratio
        )

    def select(self, models: Iterable[LocalModel]) -> LocalModel:
        eligible = [model for model in models if self.fits(model)]
        if not eligible:
            raise RuntimeError("no local model fits current hardware")
        return max(
            eligible,
            key=lambda model: (model.capability, model.context_tokens, -model.required_vram_gb),
        )


class LocalModelDiscovery:
    @staticmethod
    def from_ollama_payload(payload: dict) -> list[LocalModel]:
        discovered: list[LocalModel] = []
        for raw in payload.get("models", []):
            size = float(raw.get("size", 0))
            gb = max(0.5, size / 1_000_000_000)
            discovered.append(
                LocalModel(
                    str(raw["name"]),
                    gb * 1.25,
                    gb,
                    float(raw.get("capability", 0.5)),
                    runtime="ollama",
                )
            )
        return discovered

    @staticmethod
    def normalize_openai_compatible(runtime: str, payload: dict) -> list[LocalModel]:
        return [
            LocalModel(
                str(item.get("id")),
                4,
                4,
                float(item.get("capability", 0.5)),
                runtime=runtime,
            )
            for item in payload.get("data", [])
        ]


class ResourceController:
    def __init__(
        self,
        *,
        mode: ResourceMode = ResourceMode.BALANCED,
        pressure_samples: int = 3,
        recovery_samples: int = 3,
        high_threshold: float = 0.90,
        low_threshold: float = 0.45,
        cooldown_samples: int = 0,
    ) -> None:
        self.mode = mode
        self.pressure_samples = max(1, pressure_samples)
        self.recovery_samples = max(1, recovery_samples)
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold
        self.cooldown_samples = max(0, cooldown_samples)
        self._cooldown_remaining = 0
        self._high_count = 0
        self._low_count = 0

    def _transition(self, mode: ResourceMode) -> None:
        if mode != self.mode:
            self.mode = mode
            self._cooldown_remaining = self.cooldown_samples
            self._high_count = 0
            self._low_count = 0

    def observe_pressure(self, pressure: float) -> ResourceMode:
        if self._cooldown_remaining > 0:
            self._cooldown_remaining -= 1
            if self._cooldown_remaining > 0:
                return self.mode

        if pressure >= self.high_threshold:
            self._high_count += 1
            self._low_count = 0
            if self._high_count >= self.pressure_samples:
                self._transition(ResourceMode.CONSERVATIVE)
        elif pressure <= self.low_threshold:
            self._low_count += 1
            self._high_count = 0
            if self._low_count >= self.recovery_samples:
                self._transition(ResourceMode.BALANCED)
        else:
            self._high_count = 0
            self._low_count = 0
        return self.mode

    def observe_snapshot(self, snapshot: DynamicLoadSnapshot) -> ResourceMode:
        return self.observe_pressure(snapshot.max_pressure)

    def execution_strategy(self, *, internet_available: bool, local_models_available: bool) -> str:
        if not internet_available and local_models_available:
            return "LOCAL_ONLY"
        if not internet_available:
            return "DEGRADED_NO_INFERENCE"
        return "HYBRID"


class PerformanceGate:
    def __init__(self, max_regression_ratio: float = 1.20) -> None:
        self.max_regression_ratio = max_regression_ratio

    def passes(self, baseline: list[float], candidate: list[float]) -> bool:
        if not baseline or not candidate:
            return False
        baseline_median = statistics.median(baseline)
        candidate_median = statistics.median(candidate)
        return (
            candidate_median <= baseline_median
            if baseline_median <= 0
            else candidate_median / baseline_median <= self.max_regression_ratio
        )


@dataclass(frozen=True)
class PerformanceBudget:
    version: str
    startup_ms: float
    idle_ram_mb: float
    idle_cpu_percent: float
    ui_action_p95_ms: float


@dataclass(frozen=True)
class PerformanceSnapshot:
    startup_ms: float
    idle_ram_mb: float
    idle_cpu_percent: float
    ui_action_p95_ms: float


@dataclass(frozen=True)
class RuntimePerformanceReport:
    passed: bool
    violations: tuple[str, ...]
    budget_version: str


class RuntimePerformanceAudit:
    def __init__(self, budget: PerformanceBudget) -> None:
        self.budget = budget

    def evaluate(self, snapshot: PerformanceSnapshot) -> RuntimePerformanceReport:
        violations: list[str] = []
        if snapshot.startup_ms > self.budget.startup_ms:
            violations.append("startup_ms")
        if snapshot.idle_ram_mb > self.budget.idle_ram_mb:
            violations.append("idle_ram_mb")
        if snapshot.idle_cpu_percent > self.budget.idle_cpu_percent:
            violations.append("idle_cpu_percent")
        if snapshot.ui_action_p95_ms > self.budget.ui_action_p95_ms:
            violations.append("ui_action_p95_ms")
        return RuntimePerformanceReport(not violations, tuple(violations), self.budget.version)

    def audit_model_fit(
        self,
        hardware: HardwareProfile,
        model: LocalModel,
        *,
        headroom_ratio: float = 0.9,
    ) -> RuntimePerformanceReport:
        fits = HardwareFitProfile(hardware, headroom_ratio=headroom_ratio).fits(model)
        violations = () if fits else ("model_fit",)
        return RuntimePerformanceReport(fits, violations, self.budget.version)


class WorkloadScheduler:
    def __init__(self, controller: ResourceController) -> None:
        self.controller = controller

    def max_parallelism(self, hardware: HardwareProfile) -> int:
        if self.controller.mode == ResourceMode.CONSERVATIVE:
            return 1
        if self.controller.mode == ResourceMode.PERFORMANCE:
            return max(1, min(8, hardware.cpu_cores // 2))
        return max(1, min(4, hardware.cpu_cores // 4 or 1))
