# LOT 19 Zero-Touch Windows Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `AlinaCoderSetup.exe` install and verify Ollama, a hardware-fit local model, Git, and only the prerequisite closure actually required by AlinaCoder on a clean Windows machine.

**Architecture:** A manifest-driven pure planner determines actions from detected machine/inventory state. A Windows adapter performs official-release discovery, verified downloads, process execution, Ollama API operations, and atomic receipts. Installer lifecycle and final release readiness consume the same bootstrap report.

**Tech Stack:** Python 3.12+ stdlib, Windows APIs/PowerShell only for OS-native inspection/signature verification, GitHub Releases API, Ollama localhost API, PyInstaller, unittest, GitHub Actions Windows runner.

**Spec:** `docs/superpowers/specs/2026-09-05-lot19-zero-touch-bootstrap-design.md`

## Global Constraints

- Work directly on GitHub `main` only, per explicit user instruction.
- Keep LOT 19 as one Agiflow task and create no new work unit/subtasks.
- Never execute unverified remote scripts.
- Preserve every pre-existing Ollama/Git installation and user model on ordinary uninstall.
- `RUNTIME_V0_2_READY` must remain false until fresh LOT 19 evidence is sealed on the same SHA/artifact.

---

### Task 1: Define executable bootstrap contracts and RED tests

**Files:**
- Create: `tests/test_lot19_bootstrap.py`
- Create: `packaging/prerequisites-v0.2.json`

**Interfaces:**
- Produces expected public API from `alinacoder.product.prerequisites`: `PrerequisiteManifest`, `MachineProfile`, `ComponentInventory`, `DependencyPlanner`, `ModelSelector`, `OfficialReleaseResolver`, `PrerequisiteBootstrapper`, `BootstrapReport`.

- [ ] Write tests for manifest validation and HTTPS/allow-list rules.
- [ ] Write tests for clean machine, pre-existing compatible Ollama/Git, incompatible Ollama, low-resource CPU-only model selection, offline/deferred state, interrupted/resumed pull, ownership-safe uninstall, upgrade/rollback and digest mismatch rejection.
- [ ] Run Windows core CI and verify LOT 19 tests fail because the module/contracts do not exist.
- [ ] Commit the RED contract.

### Task 2: Implement deterministic manifest/planner/model selection

**Files:**
- Create: `src/alinacoder/product/prerequisites.py`
- Test: `tests/test_lot19_bootstrap.py`

**Interfaces:**
- `PrerequisiteManifest.load(path) -> PrerequisiteManifest`
- `ModelSelector.select(machine, manifest, override=None) -> ModelProfile`
- `DependencyPlanner.plan(machine, inventory, online=True, model_override=None) -> BootstrapPlan`

- [ ] Implement typed dataclasses and strict manifest validation.
- [ ] Implement version comparison and ownership state.
- [ ] Implement conservative RAM/VRAM/disk model fit and CPU-only fallback.
- [ ] Implement idempotent plan generation for install/upgrade/keep/pull/health/deferred.
- [ ] Run LOT 19 tests and commit GREEN planner/model-selection code.

### Task 3: Implement official release resolution and Windows side-effect adapter

**Files:**
- Modify: `src/alinacoder/product/prerequisites.py`
- Test: `tests/test_lot19_bootstrap.py`

**Interfaces:**
- `OfficialReleaseResolver.latest(owner, repo, asset_predicate) -> ReleaseAsset`
- `WindowsBootstrapAdapter.detect_machine() -> MachineProfile`
- `WindowsBootstrapAdapter.detect_inventory() -> ComponentInventory`
- `WindowsBootstrapAdapter.download_verified(asset, destination) -> Path`
- `WindowsBootstrapAdapter.verify_authenticode(path) -> bool`

- [ ] Resolve releases only through allow-listed GitHub repositories and require asset `sha256:` digests.
- [ ] Stream HTTPS downloads to temporary files, hash while downloading, atomically rename only after digest validation.
- [ ] Verify downloaded Windows executable Authenticode status via an OS-native check when a signed executable is required.
- [ ] Detect Windows version/architecture/RAM/disk/GPU/VRAM, Git, Ollama version and model inventory.
- [ ] Run tests and commit.

### Task 4: Implement Ollama bootstrap, model pull/resume and real health proof

**Files:**
- Modify: `src/alinacoder/product/prerequisites.py`
- Test: `tests/test_lot19_bootstrap.py`

**Interfaces:**
- `PrerequisiteBootstrapper.run(...) -> BootstrapReport`
- `OllamaClient.wait_ready()`, `pull(model)`, `list_models()`, `smoke_generate(model) -> str`

- [ ] Install official `OllamaSetup.exe` silently only when needed; install official Git for Windows only when Git is missing/incompatible.
- [ ] Wait for `http://127.0.0.1:11434` health with bounded retry/backoff.
- [ ] Pull selected model with progress/retry and rely on Ollama content-addressed resume semantics.
- [ ] Require model inventory plus non-empty deterministic local generation before readiness.
- [ ] Persist atomic `bootstrap-state.json`/`bootstrap-receipt.json` with component origin, exact version, URL, digest, action and health proof.
- [ ] Run tests and commit.

### Task 5: Integrate zero-touch behavior into AlinaCoderSetup lifecycle

**Files:**
- Modify: `src/alinacoder/product/installer.py`
- Modify: `packaging/setup_entry.py` only if entrypoint wiring is required
- Test: `tests/test_lot19_bootstrap.py`

**Interfaces:**
- Default install/repair/upgrade invokes prerequisite bootstrap.
- CLI flags: `--deferred-prerequisites`, `--offline`, `--bootstrap-only`, `--model`, `--rollback`, `--purge-managed-prerequisites`.

- [ ] Make normal install fail closed when required bootstrap cannot be proven.
- [ ] Make deferred/offline state explicit, resumable, and non-ready.
- [ ] Preserve external prerequisites on ordinary uninstall.
- [ ] Permit explicit purge only for components whose receipt origin is `managed_by_alinacoder`.
- [ ] Implement repair/upgrade/rollback semantics without blind external downgrade.
- [ ] Run regression suite and commit.

### Task 6: Bind release metadata and final readiness to LOT 19

**Files:**
- Modify: `src/alinacoder/product/core.py`
- Modify: `scripts/generate_release_metadata.py`
- Modify: `scripts/verify_release.py`
- Modify: `src/alinacoder/release/acceptance.py`
- Modify: `docs/USER_GUIDE.md`
- Modify: `docs/OPERATIONS.md`
- Test: `tests/test_lot19_bootstrap.py`

**Interfaces:**
- Release manifest/SBOM records prerequisite policy and model catalog.
- Final gate requires `bootstrap_e2e` evidence bound to exact commit/artifact digest.

- [ ] Add external prerequisite/model descriptors to release metadata/SBOM.
- [ ] Require prerequisite manifest in release bundle verification.
- [ ] Add LOT 19 evidence to final readiness fail-closed path.
- [ ] Document installation, offline/deferred behavior, ownership and recovery.
- [ ] Run tests and commit.

### Task 7: Add clean-Windows scenario probe and live CI proof

**Files:**
- Create: `scripts/verify_lot19_bootstrap.py`
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Script emits `dist/lot19-bootstrap-evidence.json` and exits non-zero on any required scenario failure.

- [ ] Execute deterministic simulated scenarios: clean/no deps, compatible pre-existing, incompatible Ollama, CPU-only/low RAM, interrupted/offline/resume, repair/upgrade/rollback/uninstall ownership.
- [ ] On Windows push CI, run a live official Ollama bootstrap path, force/select the low CI-safe `qwen3:0.6b` profile, perform a real localhost prompt, and archive proof.
- [ ] Re-run repair/uninstall and verify pre-existing ownership is preserved.
- [ ] Bind `bootstrap_e2e` evidence into final seal and upload the evidence file.
- [ ] Verify core 3.12, core 3.13 and package-windows all pass.
- [ ] Commit final CI integration.

### Task 8: Final independent review and Agiflow closure

**Files:**
- Review all LOT 19 changes and final GitHub Actions evidence.

- [ ] Compare final diff against all six Agiflow acceptance criteria and six test cases.
- [ ] Verify final artifact provenance, SBOM, release manifest, setup executable, bootstrap evidence and `RUNTIME_V0_2_READY=true` on one SHA.
- [ ] Update A—T-19 acceptance criteria/test cases and devInfo with exact run/artifact/digests.
- [ ] Move `In Progress → Testing → Review → Done` only after the fresh final run is green.
