# AlinaCoder v0.2 — Codex-Class Live Agent Workbench Amendment

Date: 2026-09-06  
Status: **APPROVED USER DIRECTION — NORMATIVE V0.2 ADDITIVE AMENDMENT**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment is additive to the existing AlinaCoder v0.2 conversational, desktop, activity-timeline, verification, release and setup contracts. It does not replace or weaken any prior requirement.

The user-facing target is a simple coding-agent interface comparable in interaction quality to modern Codex/Claude-style workbenches: conversation remains the primary surface while the user can see what AlinaCoder is doing in real time, inspect evidence, redirect work, and review changes without leaving `AlinaCoder.exe`.

Where this amendment is stricter about desktop observability, responsiveness, run-state presentation, progress evidence, or release validation, the stricter requirement wins.

## 2. Product contract

`AlinaCoder.exe` SHALL provide one coherent desktop surface with:

- a conversation-first central workspace;
- a compact persistent project/model/run status area;
- a live, append-only activity stream for material agent actions;
- inspectable Plan, Activity/Timeline, Diff, Tests, Git, Receipts and Diagnostics views;
- pause, resume, stop and user-takeover controls that remain usable while work is running;
- project and session continuity across restart;
- evidence-backed completion rather than unsupported progress claims;
- progressive disclosure: advanced details stay available without making the default UI complex.

## 3. No hidden chain-of-thought exposure

The UI MUST NOT expose private model chain-of-thought, hidden scratchpad content, raw internal reasoning tokens, or provider-private reasoning traces.

Instead it SHALL expose an **Explainable Activity Trace** made only from observable or deliberately summarized execution facts, for example:

- `run_started` / `run_completed` / `run_failed`;
- `phase_changed` with short user-facing status;
- provider/model route selected;
- repository/project inspection started/completed;
- search/tool invocation and its public query/target when safe;
- file read/write target and outcome;
- command/test started and completed with exit status;
- diff refreshed;
- goal/criterion state changed;
- git status/commit action;
- pause/resume/stop/takeover;
- warnings, blockers and recoverable failures.

Activity payloads MUST be sanitized before persistence/display. Reserved forbidden keys include at minimum:

`chain_of_thought`, `cot`, `hidden_reasoning`, `raw_reasoning`, `scratchpad`, `internal_monologue`.

## 4. Canonical ActivityEvent

The workbench SHALL use a structured event contract:

```text
ActivityEvent
- event_id: stable monotonic session-local identifier
- timestamp: UTC ISO-8601
- run_id: optional run identifier
- kind: stable machine-readable event type
- phase: optional high-level phase
- summary: concise user-facing explanation
- status: info | running | success | warning | error | stopped
- details: sanitized JSON object
```

Events SHALL be append-only in canonical session state and survive desktop restart.

## 5. Run lifecycle

A user turn that invokes inference SHALL visibly traverse a run lifecycle. Minimum lifecycle:

```text
run_started
→ inference_started
→ inference_completed OR run_failed
→ run_completed (on success)
```

Provider/model provenance SHALL be included after routing completes.

Existing workbench operations SHALL emit corresponding activity events where material: open project, goal creation/completion, file writes, diff inspection, tests/commands, git commit, pause/resume/stop/takeover.

## 6. Responsive desktop requirement

Long-running inference or execution MUST NOT freeze the Tk main loop.

The GUI SHALL execute message work outside the UI thread and marshal display updates back onto the Tk event loop. While a run is active:

- transcript remains scrollable;
- the activity view refreshes;
- Stop/Pause/Resume/Takeover controls remain responsive;
- the composer can accept a correction/next instruction for subsequent handling;
- the user sees an explicit running state.

No fake progress animation may substitute for real workbench events.

## 7. Simple Codex-class layout

The default visual hierarchy SHALL remain deliberately simple:

1. Header: AlinaCoder, current project, inference route, run/control state.
2. Main area: conversation transcript.
3. Composer: one primary text input plus send/voice controls.
4. Compact execution controls.
5. Secondary inspector: Activity first, then Plan, Diff, Tests, Git, Receipts, Diagnostics and deeper context/run inspector views.

Advanced panes MAY be collapsed/secondary. The chat must not become a dashboard wall.

## 8. Activity presentation

The Activity/Timeline view SHALL render newest canonical events with readable timestamps, status, summary and compact details. It SHALL not dump the entire canonical state for ordinary viewing.

The Run Inspector SHALL show structured current-run facts such as run id, state, provider/model, active goal, last action, latest evidence and error/blocker if any.

The transcript MAY include concise high-signal system notices, but duplicate verbose logs should stay in Activity/Diagnostics.

## 9. Evidence and verification

The UI SHALL distinguish:

- claimed intent/status;
- observable action event;
- verification receipt;
- final completion.

A run MUST NOT visually transition to completed if its execution raised an exception. Failures SHALL create `run_failed` with a sanitized public error summary.

## 10. Release acceptance gates

v0.2 publication SHALL be blocked unless automated tests prove at minimum:

1. activity events are persisted and survive restart;
2. inference emits the required lifecycle in order;
3. provider/model provenance appears in activity after inference;
4. failed inference emits `run_failed` and not `run_completed`;
5. workbench material operations emit activity;
6. forbidden hidden-reasoning keys are rejected/sanitized;
7. existing conversation/provider continuity tests still pass;
8. existing visible-installer/release gates still pass;
9. desktop capability contract advertises live activity and responsive agent workbench support.

## 11. Non-goals for this amendment

This amendment does not require exposing internal model reasoning, replacing Tkinter, adding a browser/IDE clone, adding mandatory cloud services, changing the main-only Git policy, or weakening the zero-cost/provider safety rules.

## 12. Done Contract

This amendment is Done only when:

- code, tests and release metadata are committed on `main`;
- CI/release verification is green for the affected gates;
- the desktop shows persisted live activity during a real workbench run;
- controls remain usable while the run executes;
- no private reasoning trace is exposed;
- existing setup and packaged desktop behavior remain non-regressed;
- release evidence explicitly covers this amendment.
