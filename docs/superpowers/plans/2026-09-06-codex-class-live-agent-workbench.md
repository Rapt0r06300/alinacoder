# Codex-Class Live Agent Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task in this session. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `AlinaCoder.exe` a responsive, conversation-first coding-agent workbench with a persisted safe live activity trace, inspectable execution evidence, responsive controls, and release-blocking acceptance coverage.

**Architecture:** Preserve the existing `DesktopWorkbench`, provider fabric, SQLite-backed canonical state, Tkinter shell, main-only Git executor, installer and release verification. Add one focused `desktop/activity.py` contract, instrument the workbench with safe observable run events, move inference off the Tk UI thread through a queue-backed worker boundary, render Activity as progressive disclosure, and extend release acceptance so v0.2 cannot be declared ready without these proofs.

**Tech Stack:** Python 3.12/3.13, `StateStore`/SQLite, Tkinter/ttk, standard-library `threading` + `queue`, unittest/pytest-compatible tests, GitHub Actions, existing AlinaCoder release acceptance framework.

**Spec:** `docs/superpowers/specs/2026-09-06-alinacoder-v0.2-codex-class-live-agent-workbench-amendment.md`

## Global Constraints

- Canonical branch is `main` only; the user explicitly authorized direct execution on `main`.
- Do not create or leave an additional Git branch as the final state.
- No hidden chain-of-thought, scratchpad, raw provider reasoning, `chain_of_thought`, `cot`, `hidden_reasoning`, `raw_reasoning`, `scratchpad`, or `internal_monologue` may be persisted or displayed.
- Conversation remains the primary UI surface; advanced details use progressive disclosure.
- Long-running inference must not block the Tk main loop.
- Stop/Pause/Resume/Takeover must remain responsive during active inference.
- Existing provider-fabric, zero-cost, setup, persistence, main-only Git, installer, packaged desktop and release contracts must not regress.
- No fake progress. UI progress must come from canonical observable events.
- Release completion requires automated proof on the final HEAD, not UI-only claims.
- The current GitHub connector does not expose a native/local worktree execution surface; because the user explicitly requires `main` only, execution is in-place on `main` with atomic commits and CI verification.

## Current execution state

- [x] Spec committed: `f5d10343e6cadf00597c53711a936c35cb4d12a2`.
- [x] Initial plan committed: `74efc09f56cfd500f8c6a53705b39f72c5e9646c`.
- [x] RED tests committed: `22a5bf351eda25eaacdd2cbc1d996e8e0ad7dc74`.
- [x] RED proved in GitHub Actions on Python 3.12 and 3.13: `Run tests` failed while compilation passed.
- [x] Minimal `ActivityEvent`/sanitizer production file started after RED: `24a0b6a1ca6964f05b2710cf9563452650dbb25b`.

---

## File map

- `src/alinacoder/desktop/activity.py` — immutable safe user-visible activity event contract and recursive redaction.
- `src/alinacoder/desktop/workbench.py` — canonical activity persistence, run lifecycle, operation instrumentation, current-run projection.
- `src/alinacoder/desktop/app.py` — conversation-first Tk UI, background message worker, activity polling/rendering, responsive controls.
- `src/alinacoder/desktop/core.py` — semantic UI capability/action registry.
- `tests/test_v02_live_activity.py` — persistence, redaction, inference lifecycle, error and control-event behavior.
- `tests/test_v02_live_activity_ui_contract.py` — static/semantic contract for non-blocking dispatch and inspector ordering.
- `tests/test_v02_desktop_inference.py` — non-regression of provider routing and canonical transcript continuity.
- `tests/test_lot14_desktop.py` — desktop capability/action compatibility.
- `src/alinacoder/release/acceptance.py` — release acceptance families/cases.
- `docs/release/acceptance-coverage-v0.2.json` — exact acceptance test mapping.
- `docs/release/traceability-v0.2.json` — code/test traceability.
- `.github/workflows/ci.yml` and `.github/workflows/publish-v0.2.0.yml` — enforcement path.
- `docs/audits/2026-09-06-v0.2-live-agent-workbench-release-audit.md` — final evidence-backed release audit.

---

### Task 1: Canonical safe ActivityEvent stream

**Files:**
- Create: `src/alinacoder/desktop/activity.py`
- Modify: `src/alinacoder/desktop/workbench.py`
- Test: `tests/test_v02_live_activity.py`

**Interfaces:**
- Produces: `ActivityEvent.to_dict() -> dict[str, Any]`.
- Produces: `sanitize_activity_details(value: Any) -> Any`.
- Produces: `DesktopWorkbench.emit_activity(kind: str, summary: str, *, status: str = "info", run_id: str | None = None, phase: str | None = None, details: dict[str, Any] | None = None) -> dict[str, Any]`.
- Produces: `DesktopWorkbench.activity() -> list[dict[str, Any]]`.
- Consumes: existing `DesktopWorkbench._mutate(...)` and `StateStore` canonical state.

- [x] **Step 1: Write the failing persistence/redaction test.**

```python
def test_activity_is_persisted_with_monotonic_ids_and_safe_details(self):
    first = workbench.emit_activity(
        "tool_started",
        "Inspecting repository",
        status="running",
        details={"path": "src", "chain_of_thought": "must never persist"},
    )
    second = workbench.emit_activity(
        "tool_completed",
        "Repository inspected",
        status="success",
        details={"nested": {"raw_reasoning": "private", "files": 3}},
    )
    assert first["event_id"] == "activity:1"
    assert second["event_id"] == "activity:2"
    assert "chain_of_thought" not in first["details"]
    assert "raw_reasoning" not in second["details"]["nested"]
```

- [x] **Step 2: Prove RED in CI.**

Run: `python -m pytest tests/test_v02_live_activity.py -q`

Expected before implementation: FAIL because `DesktopWorkbench.emit_activity` / `activity` do not exist. GitHub Actions already proved the test step fails on Python 3.12 and 3.13 at `22a5bf3...`.

- [x] **Step 3: Add the minimal immutable event/redaction module.**

Required implementation shape:

```python
_FORBIDDEN_REASONING_KEYS = frozenset({...})


def sanitize_activity_details(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): sanitize_activity_details(item)
            for key, item in value.items()
            if str(key).strip().lower() not in _FORBIDDEN_REASONING_KEYS
        }
    ...


@dataclass(frozen=True)
class ActivityEvent:
    event_id: str
    timestamp: str
    kind: str
    summary: str
    status: str = "info"
    run_id: str | None = None
    phase: str | None = None
    details: dict[str, Any] | None = None
```

- [ ] **Step 4: Extend canonical session state.**

On new session creation add exactly:

```python
"activity": [],
"next_activity_id": 1,
"next_run_id": 1,
"current_run": None,
```

For old persisted sessions, accessors must use `setdefault` during mutation so migration is backward-compatible.

- [ ] **Step 5: Implement atomic activity emission.**

Use one `_mutate("desktop_activity", mutate, metadata)` transaction. Inside `mutate`:

```python
sequence = int(data.setdefault("next_activity_id", 1))
event_id = f"activity:{sequence}"
data["next_activity_id"] = sequence + 1
data.setdefault("activity", []).append(event)
```

Timestamp format: `datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")`.

- [ ] **Step 6: Implement `activity()`.**

```python
def activity(self) -> list[dict[str, Any]]:
    return deepcopy(list(self.snapshot().get("activity", [])))
```

- [ ] **Step 7: Run focused tests.**

Run: `python -m pytest tests/test_v02_live_activity.py::LiveActivityTests::test_activity_is_persisted_with_monotonic_ids_and_safe_details -q`

Expected: PASS.

- [ ] **Step 8: Commit Task 1.**

```bash
git add src/alinacoder/desktop/activity.py src/alinacoder/desktop/workbench.py tests/test_v02_live_activity.py
git commit -m "feat(desktop): add canonical safe activity stream"
```

---

### Task 2: Observable run lifecycle and material-operation instrumentation

**Files:**
- Modify: `src/alinacoder/desktop/workbench.py`
- Modify: `tests/test_v02_live_activity.py`
- Test non-regression: `tests/test_v02_desktop_inference.py`

**Interfaces:**
- Consumes: Task 1 `emit_activity()`.
- Produces: `DesktopWorkbench.current_run() -> dict[str, Any] | None`.
- Produces run state fields: `run_id`, `status`, `phase`, `provider_id`, `model_id`, `error`, `started_at`, `finished_at`.

- [x] **Step 1: Write RED success lifecycle test.**

```python
kinds = [item["kind"] for item in workbench.activity()]
assert kinds[-4:] == [
    "run_started",
    "inference_started",
    "inference_completed",
    "run_completed",
]
assert workbench.current_run()["status"] == "completed"
```

- [x] **Step 2: Write RED failure lifecycle test.**

```python
with self.assertRaisesRegex(RuntimeError, "provider unavailable"):
    workbench.send_message("Salut")
kinds = [item["kind"] for item in workbench.activity()]
assert "run_failed" in kinds
assert "run_completed" not in kinds
assert workbench.current_run()["status"] == "failed"
```

- [x] **Step 3: Write RED control instrumentation test.**

```python
workbench.pause(); workbench.resume(); workbench.takeover(); workbench.stop()
assert [item["kind"] for item in workbench.activity()] == [
    "control_paused", "control_resumed", "control_takeover", "control_stopped"
]
```

- [ ] **Step 4: Implement run allocation.**

Add helper:

```python
def _start_run(self, text: str) -> str:
    # allocate `run:{next_run_id}` atomically, persist current_run running state,
    # emit run_started, return run id
```

The persisted user-visible `current_run` must contain only observable facts; do not persist model hidden reasoning.

- [ ] **Step 5: Wrap `send_message()` lifecycle.**

Required order for inference-enabled turns:

```python
run_id = self._start_run(text)
self.emit_activity("inference_started", "Selecting model and generating response", status="running", run_id=run_id, phase="inference")
try:
    response = self.inference_fabric.complete(...)
except Exception as exc:
    self._finish_run_failed(run_id, exc)
    raise
self.emit_activity("inference_completed", "Model response received", status="success", run_id=run_id, phase="inference", details={"provider_id": ..., "model_id": ...})
# persist assistant transcript exactly as before
self._finish_run_completed(run_id, provider_id=..., model_id=...)
```

- [ ] **Step 6: Preserve headless behavior.**

When `inference_fabric is None`, `send_message()` must preserve the existing legacy test contract: user transcript + receipt only; no fake model completion is manufactured.

- [ ] **Step 7: Instrument material workbench operations.**

Emit exactly these stable event kinds after real outcomes:

```text
project_opened
goal_started
file_written
diff_inspected
tests_started
tests_completed
goal_criterion_verified
goal_completed
git_commit_started
git_commit_completed
control_paused
control_resumed
control_stopped
control_takeover
```

For tests, include command/returncode/timed_out but keep stdout/stderr in receipts/Diagnostics rather than duplicating large logs into Activity.

- [ ] **Step 8: Run focused lifecycle + inference regression tests.**

Run:

```bash
python -m pytest tests/test_v02_live_activity.py tests/test_v02_desktop_inference.py -q
```

Expected: PASS.

- [ ] **Step 9: Commit Task 2.**

```bash
git add src/alinacoder/desktop/workbench.py tests/test_v02_live_activity.py tests/test_v02_desktop_inference.py
git commit -m "feat(desktop): expose observable agent run lifecycle"
```

---

### Task 3: Responsive Codex-class desktop UI

**Files:**
- Modify: `src/alinacoder/desktop/app.py`
- Modify: `src/alinacoder/desktop/core.py`
- Modify: `tests/test_lot14_desktop.py`
- Create: `tests/test_v02_live_activity_ui_contract.py`

**Interfaces:**
- Consumes: Task 2 `activity()` and `current_run()`.
- Produces: `dispatch_message_async(text: str) -> bool` nested GUI boundary or equivalent named top-level helper testable by source contract.
- Produces capability ids: `live_activity_stream`, `responsive_agent_workbench`, `safe_explainable_activity_trace`.

- [ ] **Step 1: Write RED capability tests.**

```python
caps = product_capabilities()
assert {
    "live_activity_stream",
    "responsive_agent_workbench",
    "safe_explainable_activity_trace",
}.issubset(caps)
```

Also assert `WorkbenchModel.available_actions()` contains `view_activity`.

- [ ] **Step 2: Write RED UI source-contract tests.**

Read `src/alinacoder/desktop/app.py` as text and assert all of:

```python
assert "import threading" in source
assert "import queue" in source
assert '"Activity"' in source
assert source.index('"Activity"') < source.index('"Plan"')
assert "root.after(" in source
assert "workbench.send_message(text)" not in synchronous_callback_body
```

The test should isolate the `send_message` callback body rather than banning the call globally because the worker must still invoke it.

- [ ] **Step 3: Prove RED.**

Run:

```bash
python -m pytest tests/test_v02_live_activity_ui_contract.py tests/test_lot14_desktop.py -q
```

Expected: FAIL because current app is synchronous and has no Activity-first capability contract.

- [ ] **Step 4: Add queue/thread imports and GUI run state.**

Use only standard library:

```python
import queue
import threading
```

Inside `run_gui()` create:

```python
ui_events: queue.Queue[tuple[str, object]] = queue.Queue()
message_worker: threading.Thread | None = None
last_activity_count = 0
```

- [ ] **Step 5: Implement worker boundary.**

`send_message()` must capture text, render `You: ...`, clear composer, set status to `WORKING`, disable duplicate Send, then start one daemon worker:

```python
def worker() -> None:
    try:
        receipt = workbench.send_message(text)
        ui_events.put(("message_complete", (text, receipt)))
    except Exception as exc:
        ui_events.put(("message_error", (text, str(exc))))
```

No Tk widget may be mutated from `worker()`.

- [ ] **Step 6: Poll queue and canonical activity from Tk thread.**

Use `root.after(100, poll_agent_ui)`; `poll_agent_ui()` drains `ui_events`, updates transcript/status/send-button, calls `refresh_views()`, and renders only new activity events since `last_activity_count`.

- [ ] **Step 7: Make inspector conversation-first and Activity-first.**

Exact secondary view order:

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

Do not remove any existing information; `Timeline` semantics are absorbed by `Activity` because both represent the append-only observable activity stream.

- [ ] **Step 8: Render compact activity text.**

Format each event as one readable line plus optional compact JSON details:

```text
14:52:01  RUNNING  Selecting model and generating response
14:52:03  SUCCESS  Model response received  {"provider_id":"...","model_id":"..."}
```

Do not render forbidden keys even if old/corrupt state contains them; sanitize again at display boundary.

- [ ] **Step 9: Render Run Inspector.**

```python
set_view("Run Inspector", json.dumps(workbench.current_run() or {}, indent=2, ensure_ascii=False, sort_keys=True))
```

- [ ] **Step 10: Preserve responsive controls.**

Do not disable Pause/Resume/STOP/Takeover while worker is alive. Only duplicate Send is disabled for the active turn.

- [ ] **Step 11: Run focused desktop tests.**

```bash
python -m pytest tests/test_v02_live_activity_ui_contract.py tests/test_lot14_desktop.py tests/test_v02_desktop_inference.py -q
```

Expected: PASS.

- [ ] **Step 12: Commit Task 3.**

```bash
git add src/alinacoder/desktop/app.py src/alinacoder/desktop/core.py tests/test_lot14_desktop.py tests/test_v02_live_activity_ui_contract.py
git commit -m "feat(desktop): add responsive Codex-class live workbench"
```

---

### Task 4: Release acceptance and traceability enforcement

**Files:**
- Modify: `src/alinacoder/release/acceptance.py`
- Modify: `docs/release/acceptance-coverage-v0.2.json`
- Modify: `docs/release/traceability-v0.2.json`
- Modify: `.github/workflows/ci.yml` only if current `pytest` invocation or final acceptance runner does not already cover the new tests.
- Modify: `.github/workflows/publish-v0.2.0.yml` only if publication can bypass final acceptance.
- Test: existing release tests plus new live activity tests.

**Interfaces:**
- Extends `SpecAcceptanceMatrix.families["desktop_ux"]` with exact cases:
  - `live_activity_persistence`
  - `safe_activity_redaction`
  - `observable_run_lifecycle`
  - `responsive_message_execution`
  - `activity_first_progressive_disclosure`
- Maps every case to one exact test function in `acceptance-coverage-v0.2.json`.

- [ ] **Step 1: Inspect current CI/publish commands and catalog schema.**

Fetch the exact current workflow and release JSON files before editing. Preserve pinning/security and unrelated gates.

- [ ] **Step 2: Write RED release test.**

Add/extend a release test to assert the five new desktop cases are in `SpecAcceptanceMatrix().required_case_ids()` and have valid coverage rows.

Example assertion:

```python
required = set(SpecAcceptanceMatrix().required_case_ids())
assert {
    "desktop_ux.live_activity_persistence",
    "desktop_ux.safe_activity_redaction",
    "desktop_ux.observable_run_lifecycle",
    "desktop_ux.responsive_message_execution",
    "desktop_ux.activity_first_progressive_disclosure",
}.issubset(required)
```

- [ ] **Step 3: Prove RED.**

Run the exact existing release-test module plus the new assertion. Expected: FAIL because the new cases are not yet in acceptance.py/catalog.

- [ ] **Step 4: Extend `SpecAcceptanceMatrix`.**

Append the five exact case ids under `desktop_ux`; do not rename/remove existing cases.

- [ ] **Step 5: Extend acceptance coverage JSON.**

Map cases to real tests only, for example:

```json
{
  "case_id": "desktop_ux.live_activity_persistence",
  "path": "tests/test_v02_live_activity.py",
  "test_name": "test_activity_is_persisted_with_monotonic_ids_and_safe_details"
}
```

Use `test_v02_live_activity_ui_contract.py` for responsive/Activity-first cases.

- [ ] **Step 6: Extend traceability.**

Ensure the desktop/conversation domain points to code paths that now include `desktop/activity.py`, `desktop/workbench.py`, and the exact tests. Follow existing JSON schema; do not invent a new incompatible schema.

- [ ] **Step 7: Verify CI transitively runs new tests.**

If CI already runs `python -m pytest` over the full suite, no workflow change is needed. If it selects modules, add the new modules explicitly.

- [ ] **Step 8: Verify publish cannot bypass release verifier.**

If already enforced, leave workflow unchanged and record evidence in the audit. Otherwise add the smallest dependency/gate required.

- [ ] **Step 9: Run release-focused tests.**

Run current release acceptance tests plus:

```bash
python -m pytest tests/test_v02_live_activity.py tests/test_v02_live_activity_ui_contract.py -q
```

Expected: PASS.

- [ ] **Step 10: Commit Task 4.**

```bash
git add src/alinacoder/release/acceptance.py docs/release/acceptance-coverage-v0.2.json docs/release/traceability-v0.2.json .github/workflows/ci.yml .github/workflows/publish-v0.2.0.yml tests/
git commit -m "ci(release): require live agent workbench proof"
```

Only stage workflow files if actually changed.

---

### Task 5: Full regression, adversarial review, fixes, and final v0.2 release update

**Files:**
- Create: `docs/audits/2026-09-06-v0.2-live-agent-workbench-release-audit.md`
- Modify only implementation/test/release files required by verified findings.

**Interfaces:**
- Consumes: all prior tasks and existing v0.2 release machinery.
- Produces: exact final HEAD, test/CI evidence, remaining blockers or `READY` verdict.

- [ ] **Step 1: Run full suite.**

```bash
python -m pytest -q
```

Expected: all tests PASS on supported Python versions in CI.

- [ ] **Step 2: Run canonical spec/release verifier commands from current CI.**

Do not guess commands: fetch `.github/workflows/ci.yml` and execute exactly the verifier commands it uses for canonical spec, release acceptance, installer/provider gates.

- [ ] **Step 3: Perform independent diff review.**

Review against this checklist:

```text
[ ] no Tk widget mutation from worker thread
[ ] no hidden-reasoning key can persist or render
[ ] no fake activity/progress
[ ] activity ids remain monotonic across restart
[ ] failed inference never emits run_completed
[ ] provider/model provenance survives provider switch
[ ] headless no-fabric behavior remains compatible
[ ] stop/pause/resume/takeover controls remain available
[ ] no regression of main-only Git enforcement
[ ] no removal/weakening of zero-cost provider rules
[ ] no installer/release-gate regression
[ ] Activity is secondary/progressive disclosure, chat stays primary
```

- [ ] **Step 4: For every finding, use TDD.**

Before each fix: add a failing regression test, observe failure in CI/local test execution, make the minimal change, rerun focused test, then rerun full suite.

- [ ] **Step 5: Create release audit.**

Audit must contain:

```text
Spec amendment path
Implementation plan path
Final main HEAD
Changed components
New acceptance cases
Full-suite result
Python 3.12 CI result
Python 3.13 CI result
Windows package job result
Release/publish gate result
Known limitations
Final verdict: READY or BLOCKED with exact blockers
```

- [ ] **Step 6: Commit final audit/fixes.**

```bash
git add docs/audits/2026-09-06-v0.2-live-agent-workbench-release-audit.md <verified-fix-files>
git commit -m "release(v0.2): validate live agent workbench"
```

- [ ] **Step 7: Wait only for observable CI completion by polling GitHub in this same turn.**

Do not ask the user to come back later. Inspect Actions for the exact final HEAD until the current run has a terminal conclusion available within the tool session.

- [ ] **Step 8: Apply verification-before-completion discipline.**

Do not say “finished”, “release-ready”, “béton”, or “all green” unless the final HEAD has fresh passing evidence for required gates. If a gate is red, diagnose and fix it in this same inline execution flow when feasible; otherwise report `BLOCKED` with the exact failing gate and evidence.

---

## Self-review required by writing-plans

### 1. Spec coverage

- Safe explainable trace → Tasks 1–3.
- Persistent append-only events → Task 1.
- Run lifecycle/provenance/failure truthfulness → Task 2.
- Responsive desktop/no Tk freeze → Task 3.
- Simple conversation-first layout/progressive disclosure → Task 3.
- Pause/resume/stop/takeover during work → Task 3.
- Release blocking evidence → Task 4.
- Full regression/adversarial review/final HEAD proof → Task 5.

No uncovered normative requirement identified.

### 2. Placeholder scan

No `TODO`, `TBD`, “implement later”, “similar to Task N”, or unspecified “add tests/error handling” placeholders remain. Every code-changing task specifies concrete APIs, exact event/case names, test intent and verification command.

### 3. Type/name consistency

- `ActivityEvent.to_dict()` and `sanitize_activity_details()` are defined in Task 1 and consumed unchanged later.
- `DesktopWorkbench.emit_activity()` and `activity()` are defined in Task 1 and consumed by Tasks 2–3.
- `DesktopWorkbench.current_run()` is defined in Task 2 and consumed by Task 3.
- Capability ids and acceptance case ids are exact and stable across Tasks 3–5.

## Execution handoff

The user explicitly selected **Inline Execution** and explicitly instructed not to pause for another choice. Continue immediately with `superpowers:executing-plans`, task-by-task, using TDD and final verification skills.