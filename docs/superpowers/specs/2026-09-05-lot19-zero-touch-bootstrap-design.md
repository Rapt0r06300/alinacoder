# LOT 19 — Zero-Touch Windows Bootstrap Design

## Goal

`AlinaCoderSetup.exe` must transform a supported clean Windows machine into an immediately usable AlinaCoder installation without requiring the user to manually install Ollama, Git, a local model, Python, or development tooling.

## Product contract

The installer owns orchestration, not external software. It must detect what already exists, install only missing/incompatible prerequisites, verify every downloaded executable before execution, retain durable ownership receipts, and never remove user-owned prerequisite installations.

A successful bootstrap means all required prerequisite gates are proven on the same installation transaction: supported Windows, enough disk for the selected model, Git available, Ollama available and healthy, a hardware-fit local model present, and a real local inference smoke test passed. If the network is unavailable or a prerequisite cannot be proven, the application may be copied in deferred mode but bootstrap readiness remains false.

## Architecture

### Versioned manifest

`packaging/prerequisites-v0.2.json` is the declarative source for prerequisite policy. It contains official release API endpoints, allowed repository owners/names, minimum compatible versions, asset selectors, the Ollama endpoint, and model profiles. The installer never executes a remote script as its installation mechanism.

### Pure planning layer

`src/alinacoder/product/prerequisites.py` contains immutable data objects for machine profile, installed-component inventory, release asset, bootstrap action, bootstrap plan, component receipt, and bootstrap report. `DependencyPlanner` consumes the manifest plus detected state and produces a deterministic action plan without side effects. `ModelSelector` picks the strongest profile that fits RAM/VRAM/disk limits while preserving a CPU-only fallback.

### Windows adapter

`WindowsBootstrapAdapter` performs the side effects behind a narrow interface: hardware/inventory detection, HTTPS JSON/download, SHA-256 verification, Authenticode verification for downloaded Windows executables, process execution, Ollama API health/model/pull/generate calls, and atomic receipt persistence. Tests use a fake adapter so scenario coverage is deterministic.

Official release discovery uses GitHub's release API for `ollama/ollama` and `git-for-windows/git`. The chosen asset must come from the allow-listed repository and include a GitHub asset digest matching the downloaded SHA-256. Ollama's official Windows installer is executed silently; Git is installed only when no compatible Git executable is available.

### Ownership and lifecycle

Every prerequisite is recorded as either `pre_existing` or `managed_by_alinacoder`. Ordinary uninstall removes AlinaCoder only and preserves external prerequisites. An explicit managed-prerequisite purge may remove only components installed by AlinaCoder; pre-existing components are immutable from the uninstaller's perspective.

Repair re-runs detection and repairs missing/broken managed components. Upgrade is anti-downgrade and records prior verified release metadata. Rollback may restore an AlinaCoder-managed prerequisite only when the previous exact asset URL and digest were recorded; otherwise it preserves the newer prerequisite instead of performing an unsafe blind downgrade.

### Model policy

The model catalog is manifest-driven and may evolve independently of installer code. Initial profiles are:

- low/CPU-only: `qwen3:0.6b`, 523 MB class, 40K context;
- balanced: `qwen3:4b`, 2.5 GB class, long context;
- performance: `qwen3:8b`, 5.2 GB class;
- workstation coding: `qwen3-coder:30b`, 19 GB class, 256K context.

Selection uses conservative headroom: model disk requirement plus reserve, RAM threshold, and optional VRAM threshold. Pull runs through Ollama's local API/CLI with retry and resumes through Ollama's content-addressed blob store. Completion requires the model to appear in the local inventory and return a non-empty answer to a deterministic smoke prompt.

### Installer integration

`src/alinacoder/product/installer.py` installs the application binary first, then invokes the prerequisite bootstrap unless `--deferred-prerequisites` was explicitly requested. New flags support `--bootstrap-only`, `--model`, `--offline`, `--rollback`, and explicit purge of AlinaCoder-managed prerequisites. `install.json` records `bootstrap_ready`, selected model, bootstrap receipt path, and pending blockers.

No successful zero-touch install exits with code 0 when a required prerequisite is unproven. Deferred/offline installation is explicitly reported as incomplete and remains resumable.

## Release and readiness

LOT 19 adds `bootstrap_e2e` to the final release evidence set. `RUNTIME_V0_2_READY` is false unless bootstrap evidence is fresh and bound to the same commit and `AlinaCoder.exe` digest as all other final evidence.

SBOM/release metadata records external runtime prerequisites and model policy as downloaded-at-install-time components, distinct from bundled build dependencies.

## Test matrix

Unit/integration tests cover deterministic planning, pre-existing ownership preservation, compatible/incompatible Ollama versions, hardware-fit model choice, low-resource CPU-only fallback, offline/deferred behavior, interrupted pull/resume, digest/signature rejection, anti-downgrade and rollback rules, idempotent repair, and safe uninstall.

The Windows release job runs a scenario probe and a live bootstrap proof. The live proof installs/uses official Ollama on the runner, pulls the low-resource model selected for that machine (or an explicit CI-safe low profile), performs a real localhost inference, records receipts, then exercises repair and uninstall while verifying that pre-existing external components are preserved. Simulated scenario cases cover states that cannot be reliably recreated on a hosted runner, including an old incompatible Ollama and network interruption.

## Security constraints

- HTTPS only; allow-listed release repositories/hosts only.
- No `irm ... | iex`, arbitrary PowerShell, or unverified remote scripts.
- Downloaded release assets require SHA-256 digest validation; Windows executable signature is checked when present/required.
- No secret is stored in bootstrap state.
- No driver is installed automatically. Driver gaps are reported as advisory blockers/degraded-performance notices only.
- UAC is never bypassed. Per-user installation is preferred and elevation refusal yields an explicit degraded/deferred state.
