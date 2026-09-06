# Fast Windows 10/11 Release Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the v0.2.0 Windows release gate fail fast and observably instead of allowing LOT19 prerequisite operations to consume tens of minutes, while preserving the stronger production/user installer timeouts.

**Architecture:** Keep production bootstrap defaults unchanged. Add environment-controlled timeout budgets to the native Windows bootstrap adapter, clamp them to safe values, and set shorter budgets only in GitHub Actions LOT19. Add an outer setup-process timeout/diagnostic helper in the workflow so a hung GUI setup is terminated with a useful failure instead of blocking the release silently.

**Tech Stack:** Python 3.12/3.13, PyInstaller, PowerShell 7, GitHub Actions, Ollama local runtime.

**Spec:** `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-codex-class-live-agent-workbench-amendment.md`

## Global Constraints

- Work directly on `main`; no release branch.
- Preserve fail-closed release behavior and same-SHA evidence.
- Preserve the real local Ollama inference gate; do not replace it with mocks.
- Production installer defaults remain tolerant; only CI opts into shorter budgets.
- Windows 10 and Windows 11 compatibility proof remains mandatory for both packaged executables.

---

### Task 1: Configurable bounded bootstrap subprocess budgets

**Files:**
- Modify: `src/alinacoder/product/windows_trust.py`
- Test: `tests/test_lot19_pull_resilience.py`

**Interfaces:**
- Consumes: `NativeWindowsBootstrapAdapter._run(args, timeout=...)`
- Produces: `_timeout_seconds(env_name: str, default: int, minimum: int, maximum: int) -> int`

- [ ] **Step 1: Write the failing test**

Add a test that sets `ALINACODER_MODEL_PULL_TIMEOUT_SECONDS=180`, invokes `pull_model`, and asserts every pull attempt receives timeout `180`. Add malformed/out-of-range cases proving fallback/clamping.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_lot19_pull_resilience -v`
Expected: FAIL because pull timeout is hard-coded to 600.

- [ ] **Step 3: Write minimal implementation**

Add a small integer environment parser and use it for model pull. Keep default `600`, clamp to a safe interval, and leave non-CI behavior unchanged.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_lot19_pull_resilience -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `fix(bootstrap): make model pull timeout CI-bounded`

### Task 2: Observable outer timeout for every windowed setup invocation

**Files:**
- Modify: `.github/workflows/ci.yml`
- Test: `tests/test_lot19_setup_process_contract.py`

**Interfaces:**
- Consumes: `AlinaCoderSetup.exe` windowed process
- Produces: PowerShell helper `Invoke-AlinaCoderSetup` returning the process exit code or throwing after a bounded timeout with setup log tail.

- [ ] **Step 1: Write the failing test**

Require the LOT19 script to define `Invoke-AlinaCoderSetup`, require `WaitForExit`, `Kill`, and setup-log tail diagnostics, and require the clean bootstrap call to pass a bounded timeout.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_lot19_setup_process_contract -v`
Expected: FAIL because direct `Start-Process -Wait` calls have no outer timeout or diagnostics.

- [ ] **Step 3: Write minimal implementation**

Define the helper inside LOT19, launch the GUI setup with `Start-Process -PassThru`, poll `HasExited` with a deadline, print the newest `%LOCALAPPDATA%/AlinaCoder/logs/setup-*.log` tail on timeout/failure, terminate the process tree, and return its actual exit code. Set `ALINACODER_MODEL_PULL_TIMEOUT_SECONDS=180` only for LOT19.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_lot19_setup_process_contract -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `fix(ci): make LOT19 setup fail fast with diagnostics`

### Task 3: Full release verification and publication

**Files:**
- Create after green CI: `docs/audits/2026-09-06-v0.2-windows10-11-release-final-audit.md`

**Interfaces:**
- Consumes: successful CI artifact for the exact final SHA
- Produces: v0.2.0 tag/release and published assets bound to the same SHA/digests.

- [ ] **Step 1: Verify core and package gates**

Require core 3.12, core 3.13, Windows packaging, embedded Win10/11 manifest evidence, provenance, packaged smoke, LOT19, provider fabric, release bundle verification, final acceptance, and artifact upload all PASS.

- [ ] **Step 2: Verify publisher**

Require `publish-v0.2.0` to complete successfully for the same final SHA.

- [ ] **Step 3: Verify release object**

Fetch `releases/tags/v0.2.0`; require `target_commitish` equals final SHA, `draft=false`, `prerelease=false`, and exactly one current asset for each published file.

- [ ] **Step 4: Verify published digests and Windows proof**

Require published release-manifest Windows compatibility values to prove Windows 10 and 11, and require GitHub asset digests to match the CI-built files.

- [ ] **Step 5: Commit audit only if needed**

If an audit commit is created, rerun the entire same-SHA CI + publish chain on that audit HEAD before declaring Done.
