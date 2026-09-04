# AlinaCoder v0.1 — Design Specification

Date: 2026-09-04  
Status: Approved design specification  
Repository: `Rapt0r06300/alinacoder`  
Default branch: `main`

## 1. Purpose

AlinaCoder v0.1 is a local autonomous coding agent for Windows. It uses Ollama as its only LLM provider, works from a command-line interface, understands a Git repository and its roadmap, chooses or accepts development goals, edits code, runs commands and tests, reviews changes, commits and pushes directly to `main`, persists state, and recovers from failures or interruptions.

The goal is a reliable, inspectable developer agent with deterministic guardrails around an LLM—not a generic multi-agent platform.

## 2. Locked product decisions

1. CLI first; no GUI required for v0.1.
2. Autonomous operation: analyze, edit, test, commit, and push without approval when guardrails and Done Contracts pass.
3. Extended workspace with explicit writable-directory allowlist.
4. Windows only for v0.1.
5. Ollama only.
6. Hybrid goal selection: explicit goal when provided; otherwise inspect repo/roadmap/tests/Git and choose the next actionable task.
7. Direct work on `main`; no branch/PR workflow in v0.1.
8. Python 3.12+.
9. One selected Ollama model for planning, coding, debugging, and review.
10. Mixed memory: SQLite internally plus human-readable Markdown for durable project-facing state.
11. Autonomous PowerShell inside allowed workspaces, guarded by policy.
12. Controlled network access, not unrestricted internet.
13. Automatic diagnose → fix → retest → rollback/recover → continue behavior.
14. Continuous loop until no actionable work remains, a guardrail blocks progress, an external dependency is unavailable, or a human decision is genuinely required.
15. Automatic selection of the best suitable installed Ollama model, with config override.
16. Self-modification allowed only with stricter checkpoints, full validation, and rollback safety.
17. Hybrid CLI: structured commands plus conversational mode.
18. Modular service-oriented core with deterministic orchestration.

## 3. Architectural principles

### 3.1 Deterministic control around probabilistic reasoning

Ollama proposes reasoning summaries and structured actions. It never gets unchecked control of PowerShell, Git, filesystem writes, or network access.

`LLM proposal → schema validation → safety policy → execution → deterministic verification → state update`

A model claim such as “tests pass” is never evidence by itself; the runtime executes the tests and records actual results.

### 3.2 Deny by default

Actions are denied unless workspace, command, path, network destination, and operation category are allowed.

### 3.3 Real repository state wins

Filesystem and Git state override stale SQLite memory. Memory is durable context, not an authority allowed to contradict reality.

### 3.4 Small isolated components

Each module has one clear responsibility and communicates through explicit typed interfaces.

### 3.5 Continuous work with bounded failure

Autonomous work may span many tasks, but retries are progress-aware and bounded. Repetition without progress causes replan, rollback, block, or stop.

## 4. Canonical runtime loop

`Observe → Select Goal → Plan → Propose Action → Safety Gate → Execute → Verify → Review → Git → Memory → Next`

A successful task cycle:

1. Inspect repository/runtime state.
2. Select explicit goal or derive next roadmap task.
3. Create a bounded plan with measurable completion criteria.
4. Request the minimum action needed for the current plan step.
5. Validate action schema and policy.
6. Execute.
7. Run targeted deterministic verification.
8. Iterate until task Done Contract is satisfied.
9. Run broader validation and diff review.
10. Create a small descriptive commit on `main`.
11. Push only when all mandatory checks pass.
12. Persist task/files/tests/commit relationships.
13. Select next task if continuous mode remains active.

## 5. Proposed source layout

```text
alinacoder/
├─ src/alinacoder/
│  ├─ cli/
│  ├─ core/
│  │  ├─ orchestrator.py
│  │  └─ planner.py
│  ├─ providers/
│  │  └─ ollama.py
│  ├─ workspace/
│  │  └─ manager.py
│  ├─ tools/
│  │  ├─ shell.py
│  │  ├─ git.py
│  │  └─ tests.py
│  ├─ memory/
│  │  ├─ store.py
│  │  └─ project_state.py
│  ├─ safety/
│  │  └─ policy.py
│  ├─ network/
│  │  └─ policy.py
│  └─ recovery/
│     └─ manager.py
├─ tests/
├─ docs/
├─ pyproject.toml
├─ ALINACODER.toml
├─ ROADMAP.md
└─ README.md
```

Exact file count may evolve, but these responsibility boundaries are part of the design contract.

## 6. Core components

### 6.1 Orchestrator

Owns the deterministic state machine: initialize/reconcile runs, select goals, sequence plan/action/verification, enforce retry limits, trigger Git publication only after validation, and stop or hand off to recovery.

### 6.2 Planner

Turns an explicit or roadmap-derived goal into bounded steps plus a task-level Done Contract. Supports replanning when evidence invalidates assumptions.

### 6.3 Ollama provider

Discovers installed models, selects the best suitable coding model via deterministic scoring, supports a forced-model override, builds stable prompts, validates structured outputs, and retries malformed model responses without executing them. One selected model may be reused under planner/coder/debugger/reviewer prompt roles.

### 6.4 Workspace manager

Normalizes Windows paths, enforces writable allowlists, detects repo root, maps project structure, locates docs/roadmaps/dependency files/tests, provides bounded file access, and protects sensitive paths.

### 6.5 Shell tool

Executes PowerShell only after policy approval. It validates working directory, classifies risk, enforces time/output limits, captures exit code/stdout/stderr/duration, never silently elevates privileges, and never bypasses policy denial.

### 6.6 Git tool

Provides status, diff, HEAD/checkpoint capture, safe reconciliation, atomic commits, push after validation, and rollback to known checkpoints. No autonomous push is allowed with failing mandatory Done Contracts.

### 6.7 Test tool

Discovers common verification tools and honors explicit project configuration. Verification normally expands from targeted tests to relevant lint/type/build checks and broader regression tests.

### 6.8 SQLite memory store

Persists runs, goals, tasks/statuses, checkpoints, actions/results, failures/recovery attempts, durable decisions, files changed, tests/results, commit SHAs, and resumable state.

### 6.9 Project-state memory

Writes human-readable state such as `ROADMAP.md`, `ALINACODER.md`, or `docs/decisions/` when useful. Raw model transcripts are not committed.

### 6.10 Safety policy

Returns `ALLOW`, `DENY`, or `REWRITE_SAFE`. Checks path boundaries, command category, destructive operations, protected paths, elevation attempts, self-modification constraints, change-scope limits, and repeated-action loops. The model cannot override policy.

### 6.11 Network policy

Controls outbound network use. v0.1 permits controlled development access such as GitHub, approved package registries, and approved documentation sources. Unknown destinations are not automatically trusted.

### 6.12 Recovery manager

Canonical flow:

`failure → diagnose → hypothesis → minimal fix → retest → progress check`

If attempts repeat without measurable progress, recovery can change strategy, replan, restore a healthy checkpoint, mark the task `BLOCKED`, or continue elsewhere only when safe and logically valid.

## 7. Memory and resume

Three conceptual layers:

1. Session state: current goal/step/action/results/errors/retry budget/touched files/checkpoint.
2. Persistent project state: roadmap, task state, stable commits, decisions, expected tests, project config.
3. Condensed model memory: compact technical summaries to reduce rereads and prompt growth.

Startup always performs:

`load SQLite → inspect Git/filesystem → compare → reconcile → resume/recover/rollback`

Stale memory must never overwrite newer repository state blindly.

## 8. Checkpoints, rollback, interruption

Before significant modification, record at least Git HEAD, working-tree status, active task/plan step, and relevant test baseline where available.

Ctrl+C requests a graceful stop:

`stop requested → finish current atomic action → persist state → checkpoint → exit`

`alinacoder resume` reconstructs work from persisted state plus actual Git state.

After abnormal failure, startup detects partial actions and chooses resume, recover, or rollback from evidence.

## 9. Safety model

### 9.1 Workspace boundary

Writes are restricted to configured workspaces. Reads outside them remain conservative and cannot be used as a hidden path to execute or write elsewhere.

### 9.2 Shell restrictions

Policy blocks categories including disk formatting, destructive deletion outside active scope, arbitrary registry/security modification, Windows account management, disabling security controls, forced changes to critical services, and implicit privilege escalation. This is category-based policy, not a brittle blacklist.

### 9.3 Network restrictions

GitHub, approved registries, and approved documentation sources are valid destination classes. Unknown endpoints are denied or require explicit configuration.

### 9.4 Dependency installation

AlinaCoder may add a necessary project dependency only when justified, recorded, reflected in the project’s official dependency declaration where applicable, non-global by default, and followed by relevant verification.

### 9.5 Loop and scope protection

Track repeated attempts/failures, lack of test progress, and unexpectedly large diffs. Stop, replan, or recover instead of allowing uncontrolled mutation.

## 10. Self-modification policy

AlinaCoder may modify its own repository only under stricter gates:

1. mandatory pre-change Git checkpoint;
2. complete applicable test suite before push;
3. relevant post-change doctor/health checks;
4. available rollback path;
5. elevated scrutiny for `safety`, `git`, `recovery`, and validation code;
6. no silent weakening of mandatory protections.

A self-change that cannot demonstrate an equal-or-stronger validated safety posture is not eligible for autonomous push.

## 11. Done Contracts and verification

A task is never `DONE` merely because the model says so.

Default pipeline:

`change → format/lint → targeted tests → broader tests/build → diff review → Git checks → verdict`

A task Done Contract can require expected files, targeted tests, lint/type/build checks, broader regressions, no unrelated file changes, goal-aligned diff, no protected-path violation, and no unresolved known failure.

### 11.1 LLM review

Before commit, the selected Ollama model receives objective, plan, diff, executed tests, and results. It searches for omissions, dead code, out-of-scope changes, weak error handling, and inconsistencies. This is advisory; deterministic checks have higher authority.

### 11.2 Publication rule

Commit/push on `main` is allowed only when mandatory Done Contracts are green. Persist traceability:

`task → files → tests → commit SHA`

## 12. Project understanding and context

Maintain a refreshed project map containing directory structure, languages, manifests, README/instructions, roadmap files, tests/commands, Git state, and important files/symbols discovered during work.

Use progressive disclosure:

`goal → key docs/config → relevant files → direct dependencies → wider context only when necessary`

Start with lightweight search/indexing. Vector DB/heavy RAG is out of scope unless evidence later proves it necessary.

## 13. Structured LLM actions

Action-producing outputs use a typed, versioned schema rather than free-form executable text. Representative shape:

```json
{
  "reasoning_summary": "The failing test shows the API now expects a Path.",
  "action": "edit_file",
  "target": "src/alinacoder/workspace/manager.py",
  "verification": ["python -m pytest tests/workspace"]
}
```

Malformed or ambiguous outputs are rejected and regenerated, never executed speculatively. AlinaCoder needs concise reasoning summaries/evidence/action justifications, not hidden chain-of-thought storage.

## 14. CLI

Running `alinacoder` opens conversational interactive mode.

Required structured commands:

- `alinacoder run` — start autonomous mission
- `alinacoder resume` — resume interrupted run
- `alinacoder status` — show goal/task/Git/tests/checkpoint/blockers
- `alinacoder doctor` — diagnose environment and agent health
- `alinacoder chat` — explicit conversational mode
- `alinacoder stop` — request clean stop after current atomic action
- `alinacoder config` — inspect/modify config
- `alinacoder memory` — inspect retained state/decisions
- `alinacoder roadmap` — show inferred next work

Non-interactive commands return meaningful process exit codes.

## 15. Configuration

### 15.1 Global

Default: `%USERPROFILE%\.alinacoder\config.toml`

May include Ollama endpoint/model override, allowed workspaces, Git behavior compatible with v0.1, approved network destinations/classes, runtime limits, and log verbosity.

### 15.2 Per-project

Optional `ALINACODER.toml` may define tests/build commands, protected paths, roadmap files, and extra Done Contract requirements.

Representative configuration:

```toml
[project]
name = "alinacoder"
default_branch = "main"

[tests]
commands = ["python -m pytest"]

[safety]
protected_paths = [".git"]

[network]
mode = "controlled"
allowed_classes = ["github", "package_registry", "documentation"]

[autonomy]
continuous = true
push_after_success = true
```

A repo without project config must still work via discovery plus conservative defaults.

## 16. Observability

Every run gets an ID and structured events such as `run.started`, `goal.selected`, `plan.created`, `action.requested`, `action.allowed`, `action.denied`, `command.executed`, `test.finished`, `checkpoint.created`, `rollback.performed`, `commit.created`, `push.completed`, `task.done`, and `task.blocked`.

Detailed logs stay under `%USERPROFILE%\.alinacoder\logs\`. Git receives durable project information, not raw LLM transcripts.

CLI verbosity: `--quiet`, `--normal`, `--verbose`, `--debug`.

Normal output emphasizes goal, plan, action, result, verification, commit, and next task.

## 17. `alinacoder doctor`

Doctor validates at least Python 3.12+, Git/repo access, PowerShell, Ollama, usable model selection, SQLite state directory/database, workspace permissions, configured network capability where testable, test command discovery/configuration, and critical config validity. It distinguishes fatal blockers from warnings.

## 18. Installation and distribution

v0.1 is a standard Python package installable with:

```powershell
pip install -e .
```

and exposes an `alinacoder` console command via `pyproject.toml`.

Initial setup creates/validates `%USERPROFILE%\.alinacoder\`, initializes SQLite, detects Ollama models, and configures allowed workspaces.

A standalone `.exe`/Windows installer is intentionally deferred until the autonomous core is stable; the architecture must remain compatible with later packaging.

## 19. Error handling

Classify at least: transient provider/tool failure, deterministic test/build failure, malformed model output, policy denial, external dependency unavailable, repo conflict/inconsistent state, non-progressing recovery loop, and human decision required.

Each class maps explicitly to bounded retry, replan, recover, rollback, block, or clean stop. No exception path may silently mark a task complete.

## 20. v0.1 non-goals

- GUI/desktop app
- macOS/Linux support
- cloud LLM providers
- multiple simultaneous LLM agents/models
- unrestricted browsing
- arbitrary machine-wide administration
- vector DB/heavy RAG
- distributed workers/event bus
- branch/PR workflow
- standalone Windows installer
- weakening guardrails for convenience

## 21. Security and reliability invariants

1. LLM output alone never proves completion.
2. No shell command executes before structured validation and safety checks.
3. No write escapes an allowed workspace.
4. No autonomous push occurs with a red mandatory Done Contract.
5. Persisted memory never overrides contradictory Git/filesystem state.
6. Recovery loops are bounded and progress-aware.
7. Self-modification cannot silently weaken mandatory protections.
8. Direct-to-`main` autonomy remains checkpointed and recoverable.
9. Malformed actions are regenerated, not guessed.
10. Every successful autonomous commit is traceable to task and verification evidence.

## 22. v0.1 success criteria

A clean Windows environment with Python 3.12+, Git, PowerShell, and Ollama can:

1. install AlinaCoder as a CLI;
2. run `alinacoder doctor` with a meaningful verdict;
3. configure at least one allowed Git workspace;
4. detect/select a suitable Ollama model;
5. inspect a repo and infer project structure;
6. accept an explicit development goal;
7. derive an actionable roadmap task when no explicit goal exists;
8. plan and perform a safe code edit;
9. execute targeted deterministic tests;
10. detect a failing change and attempt bounded auto-recovery;
11. rollback to a known good checkpoint when recovery fails;
12. create/push directly to `main` only after mandatory checks pass;
13. persist run/task/test/commit state in SQLite;
14. resume after graceful interruption;
15. reconcile correctly after abnormal interruption;
16. expose useful `status`, `memory`, and `roadmap` output;
17. modify its own repo under the stricter self-modification gate without bypassing invariants.

## 23. Implementation sequencing guidance

The later implementation plan should favor a vertical slice before broad feature depth, approximately:

1. package/CLI skeleton and typed domain models;
2. configuration and workspace boundary;
3. SQLite state and run lifecycle;
4. Ollama provider and structured responses;
5. shell plus safety policy;
6. Git checkpoint/diff/rollback;
7. test discovery/execution and Done Contracts;
8. orchestrator/planner vertical loop;
9. recovery and resume;
10. roadmap-derived goal selection;
11. controlled network policy;
12. self-modification hardening;
13. doctor/observability polish;
14. end-to-end autonomous acceptance tests.

This is sequencing guidance, not the implementation plan. The implementation plan must break work into test-driven reviewable steps with explicit verification commands.

## 24. Final design contract

AlinaCoder v0.1 is a Windows-first, Python 3.12+, Ollama-only autonomous coding CLI. It operates continuously across allowed repositories, works directly on `main`, uses deterministic safety and verification around one local model, persists state in SQLite plus human-readable project documents, recovers through checkpointed Git operations, and may improve itself only under stricter validation.

The product should feel autonomous without being opaque: every important action has a reason, policy decision, execution result, verification result, and recoverable state transition.
