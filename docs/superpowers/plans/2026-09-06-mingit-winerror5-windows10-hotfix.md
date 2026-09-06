# Windows 10 MinGit WinError 5 Hotfix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the v0.2 Windows installer robust when Windows 10 temporarily denies renaming the verified MinGit staging directory after `git.exe --version` validation, then republish `v0.2.0` from the exact verified hotfix SHA.

**Architecture:** Keep the existing verified MinGit staging/backup/rollback design. Add one narrowly-scoped Windows filesystem helper that retries transient directory replacement failures (`PermissionError` / sharing-access errors) with bounded backoff, while preserving fail-closed behavior for persistent errors. Use it for the staging→managed and managed→backup/rollback directory moves so no admin privilege is required and rollback remains exact.

**Tech Stack:** Python 3.12/3.13, pathlib/shutil, unittest, GitHub Actions Windows runners, PyInstaller.

**Spec:** `packaging/prerequisites-v0.2.json` and the existing LOT19 Windows bootstrap contract.

## Global Constraints

- Work directly on `main` only; no PR branch.
- Preserve verified official MinGit ZIP selection and SHA-256 validation.
- Preserve per-user install root under `%LOCALAPPDATA%\Programs\AlinaCoder\Git`.
- Do not require administrator elevation.
- Keep rollback/fail-closed semantics; never report success if the final managed Git executable is not verified.
- Preserve Windows 10 and Windows 11 release compatibility gates.
- Republish `v0.2.0` only from a fully green same-SHA CI artifact.

---

### Task 1: Reproduce the Windows transient rename failure

**Files:**
- Modify: `tests/test_lot19_mingit_bootstrap.py`
- Production behavior under test: `src/alinacoder/product/windows_trust.py`

**Interfaces:**
- Consumes: `NativeWindowsBootstrapAdapter.install_component("git", operation="install")`
- Produces: regression coverage proving a first transient `PermissionError(winerror=5)` during staging→managed promotion is retried and eventually succeeds without losing rollback safety.

- [ ] **Step 1: Write the failing test**

Add a test that uses the existing in-memory MinGit ZIP and command runner, patches `Path.replace` only for the `Git.alinacoder-staging -> Git` transition, raises a synthetic `PermissionError` with `winerror = 5` on the first attempt, then delegates to the real `Path.replace` on the second attempt. Assert installation succeeds, the managed `cmd/git.exe` exists, and at least two promotion attempts occurred.

```python
def test_transient_windows_access_denied_promoting_staging_is_retried(self) -> None:
    archive_bytes = self._mingit_zip()
    # build official release fixture exactly like the existing MinGit test
    # patch Path.replace so only staging -> Git fails once with winerror 5
    # then call install_component("git", operation="install")
    # assert receipt is healthy and managed git exists
```

- [ ] **Step 2: Verify RED**

Run via GitHub Actions core suite on the RED commit.
Expected: the new test fails because `_install_mingit` currently calls `staging.replace(root)` exactly once and immediately propagates the `PermissionError`.

- [ ] **Step 3: Commit RED**

Commit only the regression test.

---

### Task 2: Add bounded Windows directory-promotion retry

**Files:**
- Modify: `src/alinacoder/product/windows_trust.py`
- Test: `tests/test_lot19_mingit_bootstrap.py`

**Interfaces:**
- Produces: `NativeWindowsBootstrapAdapter._replace_directory_with_retry(source: Path, destination: Path, *, attempts: int = 8) -> None`
- Semantics: retry only transient access/sharing failures, with existing injected `_sleep`; immediately propagate unrelated filesystem errors; after the final transient failure, raise the original error.

- [ ] **Step 1: Implement the minimal helper**

```python
def _replace_directory_with_retry(self, source: Path, destination: Path, *, attempts: int = 8) -> None:
    for attempt in range(attempts):
        try:
            source.replace(destination)
            return
        except PermissionError:
            if attempt + 1 >= attempts:
                raise
            self._sleep(min(0.15 * (2 ** attempt), 2.0))
```

If Windows sharing violations surface as `OSError` with `winerror` 5 or 32 rather than `PermissionError`, include only those two winerrors in the retry set and re-raise all other `OSError` values immediately.

- [ ] **Step 2: Use the helper at MinGit directory promotion boundaries**

Replace the direct `root.replace(backup)`, `staging.replace(root)`, and rollback `backup.replace(root)` calls in `_install_mingit` with the bounded helper. Do not alter download, extraction, version verification, receipt, or ownership semantics.

- [ ] **Step 3: Verify GREEN**

Run the full Python 3.12 and 3.13 core suites. Expected: the new WinError 5 regression passes and all existing MinGit/bootstrap tests stay green.

- [ ] **Step 4: Commit GREEN**

Commit only `windows_trust.py` after the RED test is proven.

---

### Task 3: Rebuild, prove on Windows, and republish v0.2.0

**Files:**
- No product source changes unless a new failing gate identifies a separate root cause.
- Release workflows: `.github/workflows/ci.yml`, `.github/workflows/publish-v0.2.0.yml` remain unchanged unless a gate itself is defective.

**Interfaces:**
- Consumes: exact `main` hotfix SHA.
- Produces: same-SHA Windows artifacts and updated public `v0.2.0` release.

- [ ] **Step 1: Wait for exact hotfix HEAD CI**

Require success for Python 3.12, Python 3.13, Windows executable build, manifest/SBOM, provenance attestations, packaged smoke, verified Ollama cache, LOT19 clean Windows bootstrap/lifecycle, provider fabric E2E, release provenance, final acceptance sealing, and artifact upload.

- [ ] **Step 2: Verify automatic publisher**

Require `publish-v0.2.0` success for the exact current `main` SHA: same-SHA artifact validation, double-click setup window, visible installer smoke, archive build, tag move, asset replacement, digest verification.

- [ ] **Step 3: Independently verify public release**

Confirm through GitHub API:
- `refs/tags/v0.2.0` equals the hotfix HEAD;
- release `target_commitish` equals the same SHA;
- `draft == false` and `prerelease == false`;
- all 9 expected assets exist with non-empty SHA-256 digests;
- `AlinaCoderSetup.exe` and `AlinaCoder.exe` are newly uploaded from the hotfix publisher run.

- [ ] **Step 4: Report completion only after those checks pass**

Do not claim the Windows 10 installer hotfix is released before the public tag/release/assets are independently verified.
