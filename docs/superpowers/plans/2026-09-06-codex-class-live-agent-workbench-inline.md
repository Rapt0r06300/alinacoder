# Codex-Class Live Agent Workbench — Thread-Safe Inline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish AlinaCoder v0.2 with a simple Codex/Claude-style conversation-first desktop that shows safe live execution activity, remains responsive while inference runs, and cannot be released without fresh automated proof.

**Architecture:** Keep the existing SQLite-backed `DesktopWorkbench` and Tkinter UI. Because `StateStore` creates a default thread-affine SQLite connection, **all canonical-state reads/writes remain on the Tk/main thread**; only the provider/model `complete(...)` call runs in a background worker. The workbench exposes a split message lifecycle (`begin_message` → `perform_inference` → `complete_message` / `fail_message`) while keeping synchronous `send_message` for existing tests/headless use.

**Tech Stack:** Python 3.12/3.13, SQLite `StateStore`, Tkinter/ttk, standard-library `threading` and `queue`, existing inference fabric, unittest/pytest, GitHub Actions, existing v0.2 release acceptance framework.

**Spec:** `docs/superpowers/specs/2026-09-06-alinacoder-v0.2-codex-class-live-agent-workbench-amendment.md`

## Global Constraints

- Work directly on `main`; the user explicitly authorized this and does not want a final extra branch.
- Do not expose private chain-of-thought, scratchpads, raw hidden reasoning or provider-private reasoning traces.
- Conversation remains primary; Activity/Plan/Diff/Tests/Git are progressive-disclosure secondary views.
- No fake progress: every visible execution event must come from a real workbench state transition or observable operation.
- SQLite `StateStore` access stays on its creating thread in the desktop GUI.
- Background worker performs provider inference only; it does not mutate Tk widgets or canonical state.
- Pause/Resume/STOP/Takeover controls remain usable while provider inference is active.
- Existing provider-fabric, zero-cost, persistence, Git-main-only, installer and release gates must not regress.
- Do not claim v0.2 ready until final `main` HEAD has fresh green CI/release evidence.

## Current TDD state

- [x] Spec: `f5d10343e6cadf00597c53711a936c35cb4d12a2`.
- [x] RED tests: `22a5bf351eda25eaacdd2cbc1d996e8e0ad7dc74`.
- [x] RED observed on GitHub Actions Python 3.12 and 3.13 (`Run tests` failed; compile passed).
- [x] `src/alinacoder/desktop/activity.py` created after RED: `24a0b6a1ca6964f05b2710cf9563452650dbb25b`.
- [x] Initial strict plan: `985822c2d807c8f6b12720515fa1084a1d9bd4fa`.

---

### Task 1: Canonical safe activity persistence

**Files:**
- Existing/create: `src/alinacoder/desktop/activity.py`
- Modify: `src/alinacoder/desktop/workbench.py`
- Test: `tests/test_v02_live_activity.py`

**Interfaces:**
- `sanitize_activity_details(value: Any) -> Any`
- `ActivityEvent.to_dict() -> dict[str, Any]`
- `DesktopWorkbench.emit_activity(kind: str, summary: str, *, status: str = "info", run_id: str | None = None, phase: str | None = None, details: dict[str, Any] | None = None) -> dict[str, Any]`
- `DesktopWorkbench.activity() -> list[dict[str, Any]]`

- [x] **Step 1: RED test exists.** It requires monotonic `activity:1`, `activity:2`, UTC `Z` timestamps, persistence across restart and recursive removal of forbidden reasoning keys.

- [ ] **Step 2: Add backward-compatible session fields.** New sessions include:

```python
"activity": [],
"next_activity_id": 1,
"next_run_id": 1,
"current_run": None,
```

Every `_mutate` first calls:

```python
def _ensure_state_shape(data: dict[str, Any]) -> None:
    data.setdefault("activity", [])
    data.setdefault("next_activity_id", 1)
    data.setdefault("next_run_id", 1)
    data.setdefault("current_run", None)
```

- [ ] **Step 3: Implement `emit_activity`.** Timestamp with:

```python
datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
```

Allocate id inside the same `_mutate` transaction and append only the sanitized `ActivityEvent.to_dict()` payload.

- [ ] **Step 4: Implement `activity()`.** Return a deep copy of `snapshot().get("activity", [])`.

- [ ] **Step 5: Verify focused behavior.**

Run: `python -m pytest tests/test_v02_live_activity.py::LiveActivityTests::test_activity_is_persisted_with_monotonic_ids_and_safe_details -q`

Expected: PASS.

- [ ] **Step 6: Commit.**

```bash
git add src/alinacoder/desktop/activity.py src/alinacoder/desktop/workbench.py tests/test_v02_live_activity.py
git commit -m "feat(desktop): add canonical safe activity stream"
```

---

### Task 2: Split observable message lifecycle without cross-thread SQLite

**Files:**
- Modify: `src/alinacoder/desktop/workbench.py`
- Test: `tests/test_v02_live_activity.py`
- Regression: `tests/test_v02_desktop_inference.py`

**Interfaces:**
- `DesktopWorkbench.begin_message(text: str) -> dict[str, Any]`
- `DesktopWorkbench.perform_inference(request: dict[str, Any]) -> ProviderResponse-like object`
- `DesktopWorkbench.complete_message(run_id: str, response: Any) -> dict[str, Any]`
- `DesktopWorkbench.fail_message(run_id: str, error: BaseException | str) -> None`
- `DesktopWorkbench.current_run() -> dict[str, Any] | None`
- Existing `send_message(text)` remains synchronous and composes these methods.

- [x] **Step 1: RED lifecycle tests exist.** Success requires:

```text
run_started → inference_started → inference_completed → run_completed
```

Failure requires `run_failed` and forbids `run_completed`.

- [ ] **Step 2: Implement `_allocate_run(text)`.** Atomically allocate `run:{n}`, persist observable current-run facts, then emit `run_started`.

Current-run schema:

```python
{
    "run_id": run_id,
    "status": "running",
    "phase": "inference",
    "provider_id": None,
    "model_id": None,
    "error": None,
    "started_at": timestamp,
    "finished_at": None,
}
```

Do not persist hidden reasoning.

- [ ] **Step 3: Implement `begin_message`.** On the caller thread:

```python
# persist user transcript
run_id = self._allocate_run(text)
messages = self._canonical_messages(self.snapshot()["transcript"])
request = {
    "run_id": run_id,
    "messages": messages,
    "requirement": CapabilityRequirement({"reasoning": 0.3, "code": 0.3}),
    "mode": self.inference_mode,
}
self.emit_activity("inference_started", "Selecting model and generating response", status="running", run_id=run_id, phase="inference")
return request
```

- [ ] **Step 4: Implement `perform_inference`.** This is the only method intended for the GUI worker thread:

```python
def perform_inference(self, request):
    if self.inference_fabric is None:
        raise RuntimeError("inference fabric is not configured")
    return self.inference_fabric.complete(
        request["messages"],
        request["requirement"],
        mode=request["mode"],
    )
```

It must not touch `self.store`, `snapshot`, `_mutate`, Tk, files, Git or process runner.

- [ ] **Step 5: Implement `complete_message`.** On caller/UI thread: persist assistant transcript, sanitize response metadata before receipt persistence, emit `inference_completed` with provider/model, set current run completed with `finished_at`, then emit `run_completed`.

- [ ] **Step 6: Implement `fail_message`.** On caller/UI thread: store a short public error string, set current run status `failed`, `finished_at`, and emit exactly one `run_failed` event.

- [ ] **Step 7: Rebuild synchronous `send_message`.** Preserve legacy no-fabric behavior:

```python
if self.inference_fabric is None:
    # append user + legacy receipt, no fake inference completion
    return self._receipt("send_message", True, {"text": text})
request = self.begin_message(text)
try:
    response = self.perform_inference(request)
except Exception as exc:
    self.fail_message(request["run_id"], exc)
    raise
return self.complete_message(request["run_id"], response)
```

Ensure the user message is appended exactly once.

- [ ] **Step 8: Instrument controls.** `pause/resume/stop/takeover` emit stable kinds `control_paused`, `control_resumed`, `control_stopped`, `control_takeover` after state change.

- [ ] **Step 9: Instrument other material operations.** Emit stable events after observable outcomes: `project_opened`, `goal_started`, `file_written`, `diff_inspected`, `tests_started`, `tests_completed`, `goal_criterion_verified`, `goal_completed`, `git_commit_started`, `git_commit_completed`.

- [ ] **Step 10: Verify focused + regression.**

```bash
python -m pytest tests/test_v02_live_activity.py tests/test_v02_desktop_inference.py -q
```

Expected: PASS.

- [ ] **Step 11: Commit.**

```bash
git add src/alinacoder/desktop/workbench.py tests/test_v02_live_activity.py tests/test_v02_desktop_inference.py
git commit -m "feat(desktop): expose observable thread-safe run lifecycle"
```

---

### Task 3: Responsive Tk desktop with inference-only background worker

**Files:**
- Modify: `src/alinacoder/desktop/app.py`
- Modify: `src/alinacoder/desktop/core.py`
- Modify: `tests/test_lot14_desktop.py`
- Create: `tests/test_v02_live_activity_ui_contract.py`

**Interfaces:**
- Capability ids: `live_activity_stream`, `responsive_agent_workbench`, `safe_explainable_activity_trace`.
- Semantic action: `view_activity`.
- GUI worker receives only the request from `begin_message()` and calls `perform_inference()`.
- Tk polling callback calls `complete_message()` or `fail_message()` on the Tk thread.

- [ ] **Step 1: Write RED UI/capability tests.** Assert capability ids, `view_activity`, `import threading`, `import queue`, Activity before Plan, and `root.after(` polling.

- [ ] **Step 2: Add a thread-safety source contract.** Assert the worker function contains `perform_inference` but does not contain `_mutate(`, `snapshot(`, `complete_message(` or Tk widget mutation (`transcript.insert`, `status.set`, `set_view`).

- [ ] **Step 3: Prove RED.**

```bash
python -m pytest tests/test_v02_live_activity_ui_contract.py tests/test_lot14_desktop.py -q
```

Expected: FAIL against current synchronous UI.

- [ ] **Step 4: Add standard-library worker plumbing.** At module top:

```python
import queue
import threading
```

Inside `run_gui()`:

```python
ui_events: queue.Queue[tuple[str, object]] = queue.Queue()
message_worker: threading.Thread | None = None
last_activity_count = 0
```

- [ ] **Step 5: Refactor Send on Tk thread.** `send_message()` validates text, appends `You: ...`, clears composer, calls `request = workbench.begin_message(text)`, sets status `WORKING`, disables only Send, then starts worker.

- [ ] **Step 6: Worker performs inference only.**

```python
def worker() -> None:
    try:
        response = workbench.perform_inference(request)
    except Exception as exc:
        ui_events.put(("inference_error", (request["run_id"], str(exc))))
    else:
        ui_events.put(("inference_complete", (request["run_id"], response)))
```

No SQLite or Tk access from worker.

- [ ] **Step 7: Poll on Tk thread.** `poll_agent_ui()` drains `ui_events`; for success call `workbench.complete_message(run_id, response)`, render assistant text, restore Send; for failure call `workbench.fail_message(run_id, error)`, show Diagnostics/status and restore Send. Reschedule with `root.after(100, poll_agent_ui)`.

- [ ] **Step 8: Activity-first secondary panes.** Exact order:

```python
[
    "Activity",
    "Plan",
    "Diff",
    "Tests",
    "Git",
    "Receipts",
    "Run Inspector",
    "Diagnostics",
    "Context",
]
```

- [ ] **Step 9: Render Activity from canonical events.** Display timestamp/status/summary and compact sanitized details. Do not dump full canonical state into Activity.

- [ ] **Step 10: Render current run.** `Run Inspector` gets `workbench.current_run() or {}`.

- [ ] **Step 11: Preserve controls.** Do not disable Pause/Resume/STOP/Takeover while inference worker runs.

- [ ] **Step 12: Verify desktop tests.**

```bash
python -m pytest tests/test_v02_live_activity_ui_contract.py tests/test_lot14_desktop.py tests/test_v02_desktop_inference.py tests/test_v02_live_activity.py -q
```

Expected: PASS.

- [ ] **Step 13: Commit.**

```bash
git add src/alinacoder/desktop/app.py src/alinacoder/desktop/core.py tests/test_lot14_desktop.py tests/test_v02_live_activity_ui_contract.py
git commit -m "feat(desktop): add responsive Codex-class live workbench"
```

---

### Task 4: Release acceptance enforcement

**Files:**
- Modify: `src/alinacoder/release/acceptance.py`
- Modify: `docs/release/acceptance-coverage-v0.2.json`
- Modify: `docs/release/traceability-v0.2.json`
- Modify workflows only if current enforcement is insufficient.
- Test: existing release test modules plus live-workbench tests.

**Interfaces:**
Add these exact `desktop_ux` acceptance cases without removing existing cases:

```text
live_activity_persistence
safe_activity_redaction
observable_run_lifecycle
responsive_message_execution
activity_first_progressive_disclosure
```

- [ ] **Step 1: Fetch current CI, publish workflow, acceptance JSON and release tests.** Preserve exact existing schema and security pinning.

- [ ] **Step 2: Write RED release assertion.** Require all five new case ids and valid catalog mappings.

- [ ] **Step 3: Prove RED using the existing release test command/module.** Expected: FAIL before catalog/matrix update.

- [ ] **Step 4: Extend `SpecAcceptanceMatrix.families["desktop_ux"]`.** Append only; do not rename/remove old cases.

- [ ] **Step 5: Add exact coverage rows.** Map persistence/redaction/lifecycle to `tests/test_v02_live_activity.py`; map responsiveness/progressive disclosure to `tests/test_v02_live_activity_ui_contract.py`.

- [ ] **Step 6: Extend traceability using existing JSON schema.** Include new desktop activity/workbench code and tests without breaking old domain mappings.

- [ ] **Step 7: Verify CI full-suite coverage.** If CI already runs the whole test suite, leave it unchanged; otherwise add focused modules.

- [ ] **Step 8: Verify publish dependency.** If publish already depends on final acceptance/green package, leave unchanged; otherwise add the smallest blocking gate.

- [ ] **Step 9: Run release-focused verification.** Expected: PASS.

- [ ] **Step 10: Commit.**

```bash
git commit -m "ci(release): require live agent workbench proof"
```

---

### Task 5: Independent review, full regression, release audit and final CI proof

**Files:**
- Create: `docs/audits/2026-09-06-v0.2-live-agent-workbench-release-audit.md`
- Modify only files needed for proven review findings.

- [ ] **Step 1: Load `superpowers:requesting-code-review` and `verification-before-completion`.** Use their checklists before completion claims.

- [ ] **Step 2: Full test suite.** Run `python -m pytest -q` through the available execution/CI surface.

- [ ] **Step 3: Run canonical spec/release verifier commands exactly as current CI defines them.**

- [ ] **Step 4: Independent diff audit.** Check:

```text
no SQLite access from background worker
no Tk mutation from background worker
no hidden reasoning persisted/displayed
failed inference cannot emit run_completed
activity ids persist/advance correctly
provider/model provenance preserved
legacy no-fabric behavior preserved
controls remain usable during inference
main-only Git enforcement preserved
zero-cost/provider safety preserved
installer/release gates preserved
chat remains primary UI
```

- [ ] **Step 5: Fix every real finding with TDD.** New failing regression test first, then minimal fix, focused test, full rerun.

- [ ] **Step 6: Create release audit with exact final HEAD and evidence.** Include Python 3.12, Python 3.13, package-windows, acceptance/release verdicts and known limitations.

- [ ] **Step 7: Commit final release update.**

```bash
git commit -m "release(v0.2): validate live agent workbench"
```

- [ ] **Step 8: Poll GitHub Actions for the exact final HEAD in this same execution flow.** Do not ask the user to return later.

- [ ] **Step 9: Completion rule.** Say `READY`/“béton” only if all required final-HEAD gates are fresh and green; otherwise say `BLOCKED` and name the exact failing gate.

---

## writing-plans self-review

**Spec coverage:** Activity safety/persistence (Task 1), observable lifecycle (Task 2), responsive simple UI (Task 3), release blocking (Task 4), independent final proof (Task 5). No normative gap identified.

**Placeholder scan:** No TODO/TBD/“implement later” placeholders. Every task defines exact files, interfaces, test behavior, commands and commit boundary.

**Type/name consistency:** `emit_activity`, `activity`, `begin_message`, `perform_inference`, `complete_message`, `fail_message`, `current_run` are defined once and consumed consistently. Acceptance case ids and capability ids are exact.

**Critical architecture correction:** The GUI worker never calls `send_message()` because that would cross SQLite thread affinity. It calls `perform_inference()` only; state completion happens back on the Tk thread.