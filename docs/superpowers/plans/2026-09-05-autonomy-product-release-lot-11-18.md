# AlinaCoder v0.2 — LOT 11–18 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use Superpowers executing-plans/TDD. Direct work on `main` is explicitly approved by the owner for this project.

**Goal:** Implement the remaining AlinaCoder v0.2 runtime from multi-agent orchestration through a proven Windows release candidate.

**Architecture:** Extend the existing stdlib-first Python 3.12+ runtime with eight isolated subsystems: orchestration, governed self-improvement, resources/local inference, desktop workbench, optional Supabase mirror, Windows productization, torture/evaluation lab, and final acceptance/release. Canonical local state, owner policy, effect mediation, zero-cost routing and independent verification from LOT 01–10 remain authoritative.

**Tech Stack:** Python 3.12+, stdlib-first runtime, Tk/Tkinter-compatible desktop shell, SQLite/local state, HTTP via urllib, optional Supabase SQL/REST, PyInstaller only in packaging CI, GitHub Actions Windows runners.

**Spec:** `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md` plus the normative manifest and active amendments.

## Global Constraints

- Repository: `Rapt0r06300/alinacoder`; branch: `main` only.
- Python >= 3.12.
- Autonomous paid spend remains exactly EUR 0.00.
- Supabase is optional and never canonical.
- No model/agent can grant itself authority or modify the sealed acceptance boundary.
- `RUNTIME_V0_2_READY` remains false until LOT 18 evidence is fresh and complete.
- Each lot uses RED → GREEN → REFACTOR → full CI → Agiflow Testing/Review/Done.

---

### LOT 11 — Multi-Agent Orchestration

**Files:** create `src/alinacoder/orchestration/` and `tests/test_lot11_orchestration.py`.

Implement capability-scoped specialists, topology routing from dependency/coupling, fencing tokens, read/write/resource leases, semantic conflict detection, failure-domain-aware vote aggregation, council value-of-information gating, conflict notifications, and zombie-agent rejection.

Acceptance: no silent stale overwrite; same lineage != independent vote; semantic API conflicts detected; debate only when expected terminal value exceeds latency/resource cost.

### LOT 12 — Governed Self-Improvement

**Files:** create `src/alinacoder/self_improvement/` and `tests/test_lot12_self_improvement.py`.

Implement immutable governance digest, black-box event recorder, replay corpus, evolution proposals, BEFORE/AFTER measurements, sealed exogenous acceptance gate, hidden holdout interface, shadow candidate, promotion/rollback lineage, correction-derived runtime rules with user provenance/scope/revocation, and architecture-immune protected surfaces.

Acceptance: candidate failing hidden holdout is rejected; protected governance cannot self-edit; promoted candidate rolls back exactly; self-authored verifier cannot be sole promotion authority.

### LOT 13 — Resource Controller & Local Inference

**Files:** create `src/alinacoder/resources/` and `tests/test_lot13_resources.py`.

Implement HardwareProfile, DynamicLoadSnapshot, resource modes, hysteresis/dwell/cooldown controller, local runtime discovery adapters (Ollama/llama.cpp/LM Studio/vLLM-compatible endpoints), HardwareFitProfile, local model selection, load/unload decisions, provider-offline fallback, performance baselines and regression gates.

Acceptance: pressure causes controlled downgrade without state loss; offline local-only remains coherent; unsuitable models are rejected; anti-oscillation is deterministic.

### LOT 14 — Desktop Workbench

**Files:** create `src/alinacoder/desktop/`, desktop entrypoint, tests `tests/test_lot14_desktop.py`.

Implement a conversation-first desktop application model and Tk-based shell with stable automation IDs, onboarding, project/session state, `/goal` controls, text composer, voice-state adapter hooks, plan/context/diff/test/Git inspectors, action/evidence receipts, RunInspector, LiveDiffTimeline, STOP/Pause/Resume/Takeover, crash-safe persisted window/session model, keyboard navigation contract and DPI-aware startup.

Acceptance: all essential commands exposed in the application model without external terminal; STOP/Pause/Resume/Takeover change canonical backend control state; stable automation IDs are testable headlessly; `--self-test` works in packaged binary.

### LOT 15 — Optional Supabase Mirror

**Files:** create `src/alinacoder/supabase/`, versioned SQL migrations under `supabase/migrations/`, tests `tests/test_lot15_supabase.py`.

Implement disabled-by-default adapter, health/degradation state, non-secret mirror records, project/tenant scoping, RRF utility for lexical/vector ranks, durable-message idempotency/fencing wrapper, private-channel naming contract, migration manifest/rollback metadata, and local-only fallback. SQL enables pgvector/pgmq only as optional extensions and defines RLS policies.

Acceptance: outage never blocks local runtime; duplicate queue delivery cannot duplicate effect; cross-project isolation is explicit; no alpha feature is required.

### LOT 16 — Windows Productization

**Files:** create `src/alinacoder/product/`, `src/alinacoder/installer.py`, packaging scripts, SBOM/provenance generator, update verifier, and CI packaging job.

Build `AlinaCoder.exe` and `AlinaCoderSetup.exe` via pinned PyInstaller in Windows CI. Installer defaults per-user, supports quiet install/repair/uninstall and explicit data retention policy. Generate SHA-256 manifest, source commit provenance and SPDX-like SBOM. Update verifier rejects downgrade, hash mismatch, stale/tampered metadata and requires trusted signature/Authenticode policy for production channels. Signing step is conditional on owner-provided certificate.

Acceptance: clean Windows runner builds both executables; setup installs executable to an empty temp destination; installed executable passes `--self-test`; uninstall contract is verified; artifacts are uploaded with manifest/SBOM.

### LOT 17 — Whole-System Torture Lab

**Files:** create `src/alinacoder/evaluation/torture.py`, scenario corpus and `tests/test_lot17_torture.py`.

Implement deterministic fault campaigns over stale state, duplicate effects, provider loss, handoff storms, resource pressure, malicious instruction provenance, concurrency races, crash boundaries, flaky evidence, UI interruption and long-horizon goal progression. Every reproducible failure emits a FailureCard with seed, injection point, expected invariant and replay payload. OperationalReadinessScore is security-adjusted and fails closed.

Acceptance: known critical faults are caught; retries do not mask semantic faults; FailureCards replay deterministically; readiness cannot pass with a critical invariant failure.

### LOT 18 — Final Acceptance & Proven Delivery

**Files:** create `src/alinacoder/release/`, `tests/test_lot18_acceptance.py`, operator/user docs, and final CI acceptance job.

Implement a traceability matrix from normative domains/rules to code/tests/evidence, final acceptance gate, release-evidence bundle, clean-Windows install/self-test/uninstall flow, smoke orchestration of conversation→goal→verification→Git-main contract using a fixture repository, local-only mode, provider failover simulation, self-improvement promotion/rejection simulation, Supabase ON/OFF, update anti-downgrade, and security/recovery gates.

`RUNTIME_V0_2_READY=true` may be emitted only by the acceptance gate when every mandatory requirement has fresh PASS evidence bound to the current source commit and packaged artifact hashes.

## Final Verification

Run on Windows CI:

```powershell
python -m compileall -q src tests
python -m unittest discover -s tests -v
python -m alinacoder.spec_compiler --repo-root .
python -m pip install pyinstaller==6.16.0
python scripts/build_windows.py
.\dist\AlinaCoder.exe --self-test
.\dist\AlinaCoderSetup.exe --quiet --install-dir "$env:RUNNER_TEMP\AlinaCoderTest"
& "$env:RUNNER_TEMP\AlinaCoderTest\AlinaCoder.exe" --self-test
.\dist\AlinaCoderSetup.exe --uninstall --quiet --install-dir "$env:RUNNER_TEMP\AlinaCoderTest"
python -m alinacoder.release.acceptance --repo-root . --artifact-dir dist
```

No LOT is `Done` until its tests, the complete regression suite and relevant packaging/integration gates pass.