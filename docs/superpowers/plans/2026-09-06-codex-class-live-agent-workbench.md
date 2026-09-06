# Codex-Class Live Agent Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `AlinaCoder.exe` a responsive conversation-first coding-agent workbench with a persisted, safe, real-time activity trace and release-proof coverage.

**Architecture:** Extend `DesktopWorkbench` with a canonical sanitized `ActivityEvent` stream and run lifecycle, then make the Tk desktop execute inference off the UI thread and render activity through progressive-disclosure inspector panes. Preserve the existing provider fabric, state store, main-only Git executor, setup GUI and release gates; add coverage rather than replacing existing behavior.

**Tech Stack:** Python 3, existing SQLite-backed `StateStore`, Tkinter/ttk, unittest/pytest-compatible tests, GitHub Actions, existing release acceptance framework.

**Spec:** `docs/superpowers/specs/2026-09-06-alinacoder-v0.2-codex-class-live-agent-workbench-amendment.md`

## Global Constraints

- Canonical branch is `main` only.
- No hidden chain-of-thought, scratchpad or raw provider reasoning may be persisted or displayed.
- Conversation remains the primary UI surface.
- Long-running inference must not block the Tk main loop.
- Existing provider-fabric, zero-cost, installer, persistence and release contracts must not regress.
- Release completion requires automated proof, not UI-only claims.

---

### Task 1: Canonical activity event model and persistence

**Files:**
- Create: `src/alinacoder/desktop/activity.py`
- Modify: `src/alinacoder/desktop/workbench.py`
- Test: `tests/test_v02_live_activity.py`

**Interfaces:**
- Produces: `ActivityEvent`, `sanitize_activity_details(details)`, `DesktopWorkbench.emit_activity(...)`, `DesktopWorkbench.activity()`.
- Consumes: existing `StateStore` session mutation and canonical state.

- [ ] **Step 1: Write failing tests** proving a new session has an activity list, emitted events use stable monotonic ids and UTC timestamps, persist across restart, and forbidden hidden-reasoning keys are absent after sanitization.
- [ ] **Step 2: Run** `python -m pytest tests/test_v02_live_activity.py -q` and verify failure before implementation.
- [ ] **Step 3: Implement `activity.py`** with immutable event serialization and recursive sanitization of forbidden keys (`chain_of_thought`, `cot`, `hidden_reasoning`, `raw_reasoning`, `scratchpad`, `internal_monologue`).
- [ ] **Step 4: Extend workbench state** with `activity: []` and `next_activity_id: 1`; add atomic `emit_activity` and `activity` accessors.
- [ ] **Step 5: Run focused tests** and confirm pass.
- [ ] **Step 6: Commit** `feat(desktop): add canonical safe activity stream`.

### Task 2: Observable run lifecycle and operation instrumentation

**Files:**
- Modify: `src/alinacoder/desktop/workbench.py`
- Modify: `tests/test_v02_live_activity.py`
- Modify: `tests/test_v02_desktop_inference.py`

**Interfaces:**
- Produces: `DesktopWorkbench.current_run()`, run ids, required lifecycle events.
- Consumes: Task 1 `emit_activity`.

- [ ] **Step 1: Add failing tests** asserting ordered `run_started → inference_started → inference_completed → run_completed`, provider/model provenance, and `run_failed` without `run_completed` when fabric inference raises.
- [ ] **Step 2: Add failing tests** for open project, goal, write, diff, tests, commit and control-state activity.
- [ ] **Step 3: Run focused tests** and confirm failures describe missing instrumentation.
- [ ] **Step 4: Implement run ids/state** in canonical session data and wrap `send_message` with success/failure event emission while preserving existing transcript/receipt behavior.
- [ ] **Step 5: Instrument material existing operations** with concise safe event summaries and statuses.
- [ ] **Step 6: Run** `python -m pytest tests/test_v02_live_activity.py tests/test_v02_desktop_inference.py -q`.
- [ ] **Step 7: Commit** `feat(desktop): expose observable agent run lifecycle`.

### Task 3: Responsive Codex-class desktop presentation

**Files:**
- Modify: `src/alinacoder/desktop/app.py`
- Modify: `src/alinacoder/desktop/core.py`
- Modify: `tests/test_lot14_desktop.py`
- Create: `tests/test_v02_live_activity_ui_contract.py`

**Interfaces:**
- Consumes: Task 2 activity/run APIs.
- Produces: non-blocking message dispatch, UI activity renderer, `live_activity_stream` and `responsive_agent_workbench` capability declarations.

- [ ] **Step 1: Add failing UI-contract tests** requiring Activity to be the first execution-inspector surface, live capability ids, and a non-blocking dispatch boundary rather than direct synchronous inference from the Tk callback.
- [ ] **Step 2: Run focused tests** and verify failure.
- [ ] **Step 3: Refactor message dispatch** to a worker thread with a thread-safe result/event queue; only Tk callbacks mutate widgets.
- [ ] **Step 4: Add periodic UI polling** using `root.after(...)` to render newly persisted activity without fake progress.
- [ ] **Step 5: Simplify inspector ordering** to Activity, Plan, Diff, Tests, Git, Receipts, Run Inspector, Diagnostics, Context while preserving all existing views.
- [ ] **Step 6: Add compact running status** and disable only duplicate Send while a turn is actively executing; keep control buttons responsive.
- [ ] **Step 7: Render Run Inspector** from current structured run facts and keep transcript high-signal.
- [ ] **Step 8: Run desktop-focused tests**.
- [ ] **Step 9: Commit** `feat(desktop): add responsive Codex-class live workbench`.

### Task 4: Release and acceptance enforcement

**Files:**
- Modify: `src/alinacoder/release/acceptance.py`
- Modify: `docs/release/acceptance-coverage-v0.2.json`
- Modify: `docs/release/traceability-v0.2.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `.github/workflows/publish-v0.2.0.yml` only if the existing verifier does not already transitively enforce the new acceptance test.
- Test: existing release tests plus `tests/test_v02_live_activity.py` and `tests/test_v02_live_activity_ui_contract.py`.

**Interfaces:**
- Consumes: Tasks 1–3 tests/capabilities.
- Produces: release evidence and publication blocking when live-workbench proof is missing.

- [ ] **Step 1: Add failing release assertions** requiring the live activity and responsive workbench evidence ids.
- [ ] **Step 2: Run release tests** and confirm failure.
- [ ] **Step 3: Extend acceptance evidence catalog/traceability** with this amendment and exact tests.
- [ ] **Step 4: Ensure CI executes the focused tests** before publication and that publish workflow depends on release verification.
- [ ] **Step 5: Run all release-focused tests**.
- [ ] **Step 6: Commit** `ci(release): require live agent workbench proof`.

### Task 5: Regression, adversarial review and release update

**Files:**
- Modify only files required by review findings.
- Optionally add: `docs/audits/2026-09-06-v0.2-live-agent-workbench-release-audit.md`.

**Interfaces:**
- Consumes: complete change set and all existing tests.
- Produces: final evidence-backed release verdict.

- [ ] **Step 1: Run the full test suite** with `python -m pytest -q`.
- [ ] **Step 2: Run release verifier(s)** used by current CI, including visible installer and provider-fabric gates.
- [ ] **Step 3: Review the diff independently** for UI-thread violations, state races, leaked reasoning fields, fake progress, duplicate events and regression of main-only Git behavior.
- [ ] **Step 4: Fix findings using TDD** and rerun focused + full tests.
- [ ] **Step 5: Inspect GitHub Actions on the final main HEAD**; do not claim release-ready while required checks are red or missing.
- [ ] **Step 6: Update release audit/evidence** with exact final HEAD and verified gates.
- [ ] **Step 7: Commit** `release(v0.2): validate live agent workbench`.

## Self-review

- Spec coverage: persistence, lifecycle, safety, responsive UI, simple layout, evidence, and release gates each map to Tasks 1–5.
- Placeholder scan: no TODO/TBD implementation placeholders are used.
- Type consistency: Task 1 produces the event API consumed by Tasks 2–4; Task 2 produces current run data consumed by Task 3; Task 4 consumes tests/capabilities produced earlier.
- Regression strategy: existing setup/provider/release tests remain mandatory in Task 5.
