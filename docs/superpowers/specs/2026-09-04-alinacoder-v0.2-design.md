# AlinaCoder v0.2 — Intelligence, Reliability and Repository-Scale Design Specification

Date: 2026-09-04  
Status: Audit-derived design specification  
Repository: `Rapt0r06300/alinacoder`  
Default and only development branch: `main`  
Supersedes: `2026-09-04-alinacoder-v0.1-design.md` where explicitly overridden; all compatible v0.1 decisions remain in force.

## 1. Purpose

AlinaCoder v0.2 is a fully autonomous, local, Windows-first coding agent powered only by Ollama. It must be able to understand large software repositories, reason about architecture and dependencies, choose robust solutions, diagnose failures causally, detect regressions before publishing, learn from validated project history and its own attempts, recover from mistakes, and continuously execute useful development work directly on `main`.

v0.2 strengthens intelligence without turning AlinaCoder into a complex multi-agent framework. The core remains a single deterministic orchestrator around one selected Ollama model. Intelligence comes from better evidence, better repository representations, better decision protocols, and stronger execution-grounded verification.

## 2. Non-negotiable invariants carried from v0.1

1. **Full autonomy remains enabled.** AlinaCoder may analyze, plan, edit, test, correct, commit and push without approval when gates pass.
2. **All GitHub development is direct to `main`.** No autonomous feature branches or PR workflow.
3. **Python 3.12+** remains the implementation language.
4. **Windows-only for v0.2.**
5. **Ollama-only.** No cloud LLM provider.
6. **One selected Ollama model.** Logical roles are context/prompt modes, not separate concurrent model agents.
7. **CLI-first.**
8. **Extended workspace allowlist.**
9. **Controlled network access.**
10. **Deny-by-default safety policy.**
11. **Continuous autonomous loop.**
12. **SQLite plus human-readable project state.**
13. **Execution evidence outranks model claims.**
14. **Checkpoint, rollback and resume remain mandatory capabilities.**
15. **Self-modification is allowed only under stricter validation.**

## 3. Design philosophy

### 3.1 Simple control loop, rich evidence

AlinaCoder should not become more capable by accumulating dozens of LLM roles or hundreds of tools. The runtime should remain understandable enough that a developer can trace every state transition.

Complexity belongs primarily in deterministic repository analysis, evidence management and verification—not in opaque orchestration.

### 3.2 Evidence before edits

For nontrivial work, the default next action is evidence collection until AlinaCoder can explain:

- required behavior;
- observed current behavior;
- relevant code locations;
- direct and transitive dependencies;
- assumptions and uncertainties;
- regression surface;
- verification strategy.

### 3.3 Simplicity prior

When several solutions are valid, choose the smallest robust change that:

1. satisfies the behavior;
2. preserves stable interfaces where possible;
3. minimizes changed files and dependency surface;
4. is easy to verify;
5. is easy to reverse;
6. does not introduce unnecessary abstractions or dependencies.

### 3.4 Reality and freshness

Repository state, test execution and artifact content are authoritative. Stored memories and earlier conclusions may become stale and must be invalidated automatically.

## 4. Canonical v0.2 cognitive loop

`Reconcile → Understand → Localize → Hypothesize → Plan → Compare → Act → Reproduce/Verify → Impact/Regression → Critique → Commit/Push → Learn → Next`

The loop is risk-adaptive.

Low-risk mechanical work may use a compressed path:

`Reconcile → Plan → Act → Verify → Commit → Learn`

Medium/high-risk work must use deeper localization, hypothesis, comparison and regression phases.

## 5. Proposed source architecture

```text
src/alinacoder/
├─ cli/
├─ core/
│  ├─ orchestrator.py
│  ├─ state_machine.py
│  └─ risk.py
├─ intelligence/
│  ├─ planner.py
│  ├─ decision_engine.py
│  ├─ hypotheses.py
│  ├─ critic.py
│  └─ confidence.py
├─ providers/
│  └─ ollama.py
├─ context/
│  ├─ manager.py
│  └─ evidence_packet.py
├─ repository/
│  ├─ workspace.py
│  ├─ indexer.py
│  ├─ graph.py
│  ├─ retrieval.py
│  ├─ history.py
│  └─ impact.py
├─ tools/
│  ├─ shell.py
│  ├─ patch.py
│  ├─ git.py
│  └─ tests.py
├─ verification/
│  ├─ baseline.py
│  ├─ contracts.py
│  ├─ regression.py
│  ├─ interfaces.py
│  └─ adequacy.py
├─ memory/
│  ├─ store.py
│  ├─ episodic.py
│  ├─ lessons.py
│  ├─ evidence.py
│  └─ project_state.py
├─ recovery/
│  ├─ manager.py
│  └─ best_state.py
├─ safety/
│  └─ policy.py
└─ network/
   └─ policy.py
```

This layout describes responsibility boundaries. Implementation may merge very small modules if tests and interfaces remain clear.

## 6. Repository Intelligence Graph (RIG)

### 6.1 Goal

AlinaCoder must reason about repositories as structured systems rather than flat collections of text files.

The Repository Intelligence Graph is a deterministic, incrementally maintained representation of code and project structure.

### 6.2 Core node types

At minimum:

- repository;
- package/module;
- file;
- class;
- function/method;
- public symbol/interface;
- test file;
- test case;
- build/config artifact;
- dependency/package declaration.

Optional language-specific nodes may include variables/statements when deeper analysis is needed.

### 6.3 Core edge types

At minimum:

- `CONTAINS`;
- `IMPORTS`;
- `CALLS` / `INVOKES` where statically resolvable;
- `INHERITS`;
- `EXPORTS`;
- `DEPENDS_ON`;
- `BUILDS_WITH`;
- `TESTS`;
- `COVERS` when coverage evidence exists;
- `CONFIGURES`;
- `CO_CHANGES_WITH` from Git history;
- `AFFECTS` for derived impact relations.

### 6.4 Evidence-backed edges

Every graph edge stores its origin where practical: AST parser, import declaration, test naming/linker, coverage result, build metadata, Git history, or inferred relation.

Inferred edges must carry lower confidence than deterministic edges.

### 6.5 Incremental maintenance

The graph must not be rebuilt from scratch after every edit. Changed files invalidate only affected nodes/edges and relevant derived closures.

### 6.6 Large repository strategy

v0.2 uses a **lightweight global graph + partial on-demand expansion**.

Global indexing gives orientation. Expensive traversals/data-flow analysis are built only around active task entry points.

No mandatory Neo4j/vector database is introduced in v0.2.

## 7. Repository retrieval

### 7.1 Hybrid evidence routes

Context retrieval combines several routes rather than trusting a single similarity system:

1. lexical search (`rg`, names, error signatures);
2. symbol/index lookup;
3. graph traversal;
4. dependency/test-impact traversal;
5. Git/history search;
6. runtime traces/logs;
7. optional similarity ranking if a lightweight local mechanism is later justified.

### 7.2 Intent-aware retrieval

Retrieval strategy depends on task type.

Examples:

- bug: reproduce → traceback/error anchors → callers/dependencies → tests → history;
- feature: requirement anchors → public interfaces → architecture neighbors → dependents → tests;
- regression: changed artifacts → reverse dependency closure → pass-to-pass tests → recent history;
- architecture question: component/build/dependency graph → transitive closure;
- API migration: changed signatures → consumers → history → integration tests.

### 7.3 Evidence packets

The model receives compact `EvidencePacket` objects rather than unrestricted raw output.

Each packet contains:

- source kind;
- path/symbol/line span;
- content excerpt or structured relation;
- provenance;
- freshness/version;
- relevance rationale;
- confidence class;
- recoverable pointer to full source.

### 7.4 Context budget

The context manager applies explicit per-route and global budgets, deduplicates overlapping evidence and preserves exact paths/error messages needed for tool use.

## 8. Hierarchical adaptive planning

### 8.1 Plan levels

Planning is represented as:

`Mission → Milestone → Task → Step`

A short bug fix may contain one milestone/task. A roadmap run may contain many.

### 8.2 Task state

Each task stores:

- objective;
- acceptance criteria;
- assumptions;
- dependencies/prerequisites;
- affected architecture scope;
- risk level;
- current evidence;
- verification envelope;
- status;
- blockers;
- parent/child relationships.

### 8.3 Plans are hypotheses, not truth

Execution evidence may invalidate a plan. The planner must update or replace steps rather than forcing the original plan to completion.

### 8.4 Plan-memory coupling

Current phase/task controls which episodic and historical memories are retrieved.

Memory-derived signals can force replanning, including:

- same failed command repeated;
- same file edited repeatedly without test improvement;
- new evidence contradicting an assumption;
- dependency closure larger than expected;
- reproduction remains unchanged after attempted fix;
- context exploration saturates without localization progress.

### 8.5 Dependency-aware scheduling

For multi-part work, prerequisites and dependency direction guide order. Prefer implementing/verifying foundations and stable interfaces before dependents.

## 9. Hypothesis-driven debugging

### 9.1 Reproduction first

For bug/failure tasks, AlinaCoder should attempt to identify or create a deterministic reproduction before editing implementation code.

Reproduction classes:

- `STRONG`: deterministic failing test/script reproduces issue;
- `PARTIAL`: deterministic symptom exists but not full issue;
- `WEAK`: only static/log evidence available;
- `NONE`: reproduction impossible with available environment.

The class is part of final confidence and Done Contract evidence.

### 9.2 Hypothesis Ledger

For nontrivial failures, store multiple candidate root causes:

```text
Hypothesis
- statement
- supporting evidence
- contradicting evidence
- confidence
- falsification probe
- expected observation
- status: OPEN / SUPPORTED / REJECTED / CONFIRMED
```

### 9.3 Anti-anchoring behavior

The first plausible diagnosis must not automatically trigger a broad edit. AlinaCoder should prefer low-cost probes that distinguish hypotheses.

### 9.4 Structured failure diagnosis

Failure diagnosis integrates:

- exact error/trace;
- command and environment state;
- changed artifacts;
- graph neighborhood;
- related tests;
- prior attempts;
- relevant Git history;
- runtime instrumentation where justified.

### 9.5 Bounded guidance

A diagnosis becomes an executable repair action only if it defines:

- target;
- operation;
- verification signal;
- boundary/stop condition.

## 10. Multiple-design decision gate

### 10.1 Trigger

Use multiple candidate designs for medium/high-risk changes where more than one architecture or implementation approach is plausible.

Do not invoke it for trivial formatting, obvious one-line fixes or deterministic mechanical changes.

### 10.2 Same model, isolated passes

The one selected Ollama model generates 2–3 candidate designs in separate context passes to reduce anchoring.

### 10.3 Scoring

Candidate designs are compared on:

- behavioral correctness evidence;
- architectural fit;
- direct/transitive dependency impact;
- regression risk;
- changed surface area;
- simplicity;
- testability;
- reversibility;
- public-interface stability;
- new dependency cost;
- expected maintenance burden;
- consistency with project history/conventions.

### 10.4 Simplicity rule

When scores are otherwise comparable, choose the lower-complexity design.

## 11. Critical review and self-questioning

Before commit, a context-isolated critic pass receives:

- original requirement;
- selected design and rejected alternatives;
- assumptions;
- patch/diff;
- changed dependency closure;
- reproduction result;
- impacted regression results;
- static/build/type results;
- unresolved warnings.

The critic must actively search for:

- requirement mismatch;
- accidental scope expansion;
- hidden API break;
- missing dependent updates;
- untested behavior;
- stale assumption;
- edge cases;
- needless complexity;
- duplicate functionality;
- error handling regressions;
- dependency/version mistakes;
- test gaming.

The critic is advisory. Deterministic failing evidence always wins.

## 12. Change impact analysis

### 12.1 Pre-edit impact estimate

Before medium/high-risk edits, compute expected affected nodes using forward/reverse graph traversal.

### 12.2 Post-edit impact

After patching, recompute from actual changed files/symbols.

### 12.3 Transitive closure

Impact analysis must explicitly calculate transitive dependencies to a configured risk-dependent depth or full closure. The model is not trusted to infer that one-hop traversal is sufficient.

### 12.4 Risk classification

Example classes:

- `LOW`: local implementation, no public interface/dependency edge changes;
- `MEDIUM`: multiple symbols/files, internal interfaces or meaningful behavior;
- `HIGH`: public API, persistence/schema, build/config, concurrency, security/safety, dependency upgrade, architecture boundary, or broad reverse-dependency closure.

Risk level controls reasoning depth and verification strength, not autonomy.

## 13. Regression prevention and test impact

### 13.1 Verification envelope

Every task has an explicit verification envelope built from:

1. acceptance/fail-to-pass checks;
2. previously-passing impacted tests;
3. static/lint/type checks;
4. build/import checks;
5. public-interface/invariant checks;
6. optional high-assurance adequacy checks.

### 13.2 Baseline

Where execution cost permits, record a pre-change baseline for impacted checks.

Test states distinguish:

- already failing before patch;
- fail-to-pass target;
- previously passing / now passing;
- previously passing / now failing regression;
- not runnable/unavailable.

### 13.3 Test-impact map

RIG-derived source/test edges plus conventions, imports and optional coverage produce an impacted-test set.

A concise mapping artifact may be cached for efficient retrieval.

### 13.4 Broader verification

After targeted success, broaden based on impact/risk rather than blindly running everything first.

### 13.5 Test adequacy escalation

For high-risk changes with weak tests, AlinaCoder may autonomously add or run:

- regression tests;
- property-based tests;
- differential tests;
- selective mutation testing;
- contract/invariant checks.

These tools are escalations, not mandatory ceremony.

## 14. Public interfaces and architecture invariants

AlinaCoder tracks important project contracts including:

- exported/public symbols;
- typed signatures where available;
- CLI/API contracts;
- file/config schema expectations;
- dependency declarations/lockfiles;
- key architecture constraints documented in `ALINACODER.md`, project config or decisions.

A detected interface change automatically expands impact analysis to downstream consumers.

## 15. Deterministic edit tool

### 15.1 Why

Shell access remains powerful, but file mutation needs stronger integrity than arbitrary PowerShell text manipulation.

### 15.2 Patch contract

`tools/patch.py` supports atomic edits with:

- normalized allowed path;
- expected pre-image hash;
- exact/unique replacement or unified patch;
- stale-file rejection;
- atomic temporary-file write + replace;
- encoding/newline preservation where practical;
- post-write parse/syntax check when available;
- diff summary returned to orchestrator.

### 15.3 Drift handling

If a file changed since the model saw it, the edit is rejected and context is refreshed/replanned rather than applying a stale patch.

## 16. Context management

### 16.1 Context tiers

Maintain:

1. **Stable anchors** — mission, requirements, non-negotiable constraints;
2. **Plan state** — current milestone/task/assumptions;
3. **Recent working memory** — high-fidelity latest actions/observations;
4. **Reasoning digests** — concise prior-phase summaries;
5. **Retrieved evidence packets**;
6. **Durable memory references**.

### 16.2 Active condensation

Condense proactively at phase/milestone boundaries or context pressure.

A digest must preserve:

- unresolved hypotheses;
- decisions and rationale;
- changed files/symbols;
- exact failing checks;
- important tool results;
- current Git state;
- next intended action;
- evidence pointers.

### 16.3 No raw hidden reasoning archive

Store concise reasoning summaries, hypotheses, evidence and decisions—not private chain-of-thought transcripts.

## 17. Memory architecture

### 17.1 Memory classes

Durable memory is explicitly typed:

- `FACT`;
- `DECISION`;
- `EPISODE`;
- `LESSON`;
- `INVARIANT`;
- `HISTORY_PATTERN`;
- `VERIFICATION_CLAIM`.

### 17.2 Provenance

Each durable record stores where practical:

- source/run/task;
- Git commit/version;
- artifact/path/symbol anchors;
- evidence type;
- confidence class;
- creation time;
- freshness state;
- superseded-by relation;
- applicability scope.

### 17.3 Freshness

Artifact-backed records can be:

- `FRESH`;
- `STALE`;
- `UNPROVABLE`;
- `SUPERSEDED`.

A content hash or semantic anchor change invalidates dependent claims until reverified.

### 17.4 Memory is not automatically trusted

Retrieved memory is evidence input. It may be contradicted by live state.

## 18. Learning from errors

### 18.1 Episode capture

Every meaningful attempt records:

- problem state;
- chosen hypothesis/design;
- actions;
- outcome;
- verification delta;
- regression delta;
- reason for rollback/block/success.

### 18.2 Candidate lesson

After success or an informative failure, AlinaCoder may distill a reusable candidate lesson.

### 18.3 Lesson promotion gate

A lesson becomes durable only if:

- grounded in concrete evidence;
- not contradicted by current repo state;
- scoped to explicit applicability conditions;
- not merely “this prompt worked”;
- likely reusable;
- free of secrets/raw sensitive data.

### 18.4 Negative lessons

Record failed approaches when useful:

`symptom/context → attempted strategy → observed failure → why it failed → when not to repeat`

### 18.5 Lesson invalidation

Lessons tied to changed APIs/architecture become stale through artifact anchors.

## 19. Learning from project history

### 19.1 History Intelligence

Use Git history as repository-specific experience:

- `git log`;
- commit messages;
- `git show` diffs;
- `git blame` where relevant;
- function/file evolution;
- co-change frequency;
- prior fixes near current symbols;
- dependency/API migration patterns.

### 19.2 Task-directed history retrieval

Do not load broad history by default. Retrieve it when current evidence suggests value: recurring bug, migrated API, confusing convention, blameable regression, or architecture evolution.

### 19.3 History-derived patterns

Promotable patterns include:

- files that commonly change together;
- conventional locations for functionality;
- recurring compatibility rules;
- prior root causes/fix strategies;
- evolution of interfaces.

History-derived claims retain commit provenance.

## 20. Runtime diagnostics and instrumentation

For difficult failures, AlinaCoder may add temporary diagnostic probes or invoke available tracing/profiling tools to collect evidence such as:

- traceback/call path;
- selected variable values;
- assertion deltas;
- timing/ordering evidence;
- resource/state transitions.

Instrumentation changes are tracked separately and removed before final commit unless intentionally part of the solution.

Raw logs are filtered into concise evidence while preserving pointers to full local logs.

## 21. Confidence and uncertainty

### 21.1 Confidence is evidence-derived

Confidence labels are based on evidence strength, not model self-confidence alone.

Suggested classes:

- `PROVEN`: deterministic acceptance + relevant regressions + required static/build checks;
- `STRONG`: strong behavior and impact evidence with minor unverifiable surface;
- `LIMITED`: partial reproduction/coverage;
- `WEAK`: mostly static/inferential evidence;
- `UNPROVABLE`: required evidence unavailable.

### 21.2 Uncertainty register

Plans may contain explicit unresolved uncertainties. The agent should autonomously reduce high-impact uncertainties before committing when possible.

## 22. Best-known-state recovery

### 22.1 Beyond last checkpoint

Recovery tracks multiple candidate states and identifies a `BestKnownState`.

### 22.2 Score vector

Do not collapse correctness to one scalar test count. Compare states using an ordered vector including:

1. safety/invariant violations;
2. issue reproduction/acceptance state;
3. newly introduced regressions;
4. required build/type/static status;
5. targeted test pass vector;
6. diff/risk size;
7. unresolved critical hypotheses.

A state with a safety or regression violation cannot outrank a clean state merely because it passes more unrelated tests.

### 22.3 Cognitive deadlock detection

Signals include:

- repeated normalized action;
- repeated same error;
- repeated edit/revert to same file;
- no verification-vector improvement;
- growing diff without localization confidence improvement;
- repeated plan revision without new evidence.

Deadlock triggers strategy diversification, evidence gathering, best-state restoration or task block—not endless edits.

## 23. Controlled local experimentation while staying on `main`

The Git policy remains `main` only.

AlinaCoder may use temporary scratch directories or disposable local execution copies for risky experiments, benchmarks or reproduction work, but it must not create GitHub development branches. Canonical commits and pushes are always made to `main` after validation.

Temporary experimental artifacts are not treated as project history unless promoted intentionally.

## 24. Ollama model selection v0.2

### 24.1 Discovery

Detect installed models and hardware constraints.

### 24.2 Capability probes

When selection is not forced, `doctor`/selector may run bounded local probes measuring:

- structured JSON/schema compliance;
- instruction/tool adherence;
- small code reasoning/edit task;
- context retrieval/use;
- latency and memory fit.

### 24.3 Selection

Use actual probe results plus model metadata/hardware fit. Cache results per model digest/version and invalidate when the model changes.

## 25. Self-improvement

### 25.1 Full autonomy retained

AlinaCoder may autonomously improve its own code.

### 25.2 Locked evaluation harness

Self-improvement requires a local benchmark/acceptance suite whose integrity is protected from the candidate change where feasible.

The evaluation includes:

- core unit/integration tests;
- safety policy fixtures;
- workspace escape tests;
- resume/recovery fixtures;
- repository localization fixtures;
- dependency/impact fixtures;
- regression-detection fixtures;
- memory freshness/invalidation fixtures;
- autonomous task fixtures;
- performance/resource ceilings where useful.

### 25.3 Promotion rule

A candidate self-change is promoted only if:

- mandatory tests pass;
- no safety floor regresses;
- no regression metric exceeds configured floor;
- target quality metric improves or fixes a defined defect;
- evaluator integrity is unchanged unless the evaluator change itself passes a higher-order review gate.

### 25.4 No reward gaming

Benchmark scripts/config used to decide promotion are checksummed or otherwise integrity-checked. Changes that weaken the evaluator are rejected unless explicitly part of a separately validated evaluator upgrade.

## 26. Verification claims ledger

Every important completion statement can be represented as a verification claim, for example:

- “CLI command `status` returns exit 0”;
- “public signature X is unchanged”;
- “tests A/B/C pass”;
- “module Y no longer reproduces issue Z”.

Each claim stores supporting artifacts/tests and freshness anchors.

If supporting content changes, the claim becomes stale automatically and cannot silently remain part of a future Done Contract.

## 27. Done Contract v0.2

A task may be marked `DONE` only when:

1. requirement/acceptance criteria are mapped to explicit evidence;
2. required reproduction/behavior check is satisfied or evidence limitation is explicitly classified;
3. impacted pass-to-pass checks are not newly broken;
4. required build/type/static checks pass;
5. public interface/invariants are validated for the impacted closure;
6. critic has no unresolved critical finding;
7. diff is within intended scope or scope expansion is justified;
8. repository/Git state is reconciled;
9. verification claims are fresh;
10. memory/task state is persisted;
11. only then may commit/push occur.

## 28. Direct-to-main Git policy

### 28.1 Before commit

- `main` must be current/reconciled;
- working tree must match tracked run state;
- no stale external changes;
- Done Contract green;
- commit scope coherent.

### 28.2 Commit

Prefer small task-coherent commits with descriptive messages.

### 28.3 Push

Push directly to `main` after validation.

If upstream `main` moved, pull/reconcile safely, rerun affected verification and only then push.

No force push is permitted autonomously by default.

## 29. Observability v0.2

In addition to v0.1 events, emit structured events for:

- `repository.index.updated`;
- `evidence.retrieved`;
- `hypothesis.created`;
- `hypothesis.rejected`;
- `hypothesis.confirmed`;
- `assumption.invalidated`;
- `plan.revised`;
- `design.compared`;
- `impact.computed`;
- `baseline.recorded`;
- `regression.detected`;
- `critic.finding`;
- `memory.stale`;
- `lesson.promoted`;
- `lesson.rejected`;
- `best_state.updated`;
- `deadlock.detected`.

Normal CLI remains concise; deep evidence is available under verbose/debug or run logs.

## 30. Metrics

AlinaCoder should measure its own engineering performance rather than relying only on “task completed”.

Core metrics include:

- task acceptance success;
- fail-to-pass rate;
- pass-to-pass regression rate/count;
- impacted-test recall on fixtures;
- localization accuracy on fixtures;
- dependency/impact correctness;
- repeated failed-action rate;
- recovery success;
- deadlock frequency;
- plan revisions and causes;
- stale-memory catches;
- lesson reuse success;
- rejected invalid lessons;
- average files/lines changed per task relative to expected scope;
- context/tool-call budget;
- unnecessary dependency additions;
- public interface regressions;
- self-improvement benchmark delta.

## 31. Risk-adaptive reasoning depth

AlinaCoder must not apply maximum ceremony to every change.

### LOW

- concise evidence;
- single design path acceptable;
- targeted checks + appropriate broader gate.

### MEDIUM

- impact analysis;
- assumptions;
- at least one explicit alternative where meaningful;
- targeted + impacted regression checks;
- critic pass.

### HIGH

- reproduction/baseline where possible;
- dependency/architecture closure;
- multiple designs;
- hypothesis/uncertainty register;
- stronger test adequacy;
- interface/invariant verification;
- isolated critic;
- robust rollback/best-state checkpoint.

Risk controls verification depth, not whether AlinaCoder is autonomous.

## 32. Explicit anti-patterns

v0.2 must avoid:

1. reading the entire repository into every prompt;
2. similarity-only code retrieval;
3. one-hop-only impact reasoning when transitive impact matters;
4. blindly trusting raw memory;
5. treating model review as independent proof;
6. endless self-reflection without new evidence;
7. broad refactors during narrow bug fixes;
8. adding dependencies for convenience when standard library/project tools suffice;
9. storing full private reasoning transcripts as memory;
10. accepting a patch because target tests pass while pass-to-pass regressions fail;
11. repeatedly editing the same locus without measurable progress;
12. changing tests solely to make broken behavior appear correct;
13. weakening the self-evaluation harness to promote a self-change;
14. introducing multi-agent complexity without measured benefit;
15. creating GitHub branches despite the `main`-only project policy.

## 33. v0.2 acceptance scenarios

Implementation is not considered complete until fixtures/E2E tests demonstrate at least:

1. **Large-repo localization fixture:** find relevant symbols using lexical + structural evidence without reading the whole repo.
2. **Transitive dependency fixture:** identify downstream consumers beyond one hop.
3. **Regression fixture:** detect a previously passing impacted test broken by a candidate patch and refuse promotion.
4. **Bug reproduction fixture:** produce/identify fail-to-pass behavior before fixing and confirm it afterward.
5. **Competing hypothesis fixture:** reject an initially plausible but falsified cause and choose the evidence-supported cause.
6. **Alternative design fixture:** choose a smaller robust patch over a more complex equivalent design.
7. **History fixture:** retrieve a relevant prior commit/fix and use it without blindly copying stale code.
8. **Memory freshness fixture:** invalidate a verification claim after its supporting artifact changes.
9. **Negative lesson fixture:** avoid repeating a previously failed strategy when applicability conditions match.
10. **Deadlock fixture:** detect repeated no-progress edits and restore/branch strategy internally without endless looping.
11. **Best-state fixture:** prefer a cleaner earlier state over a later state that passes more tests but introduces a regression.
12. **External drift fixture:** reject stale patch after file changes outside the current action.
13. **Resume fixture:** crash and resume with plan/hypothesis/evidence state coherent with Git reality.
14. **Self-improvement fixture:** candidate improvement that raises one metric but breaks a safety floor is rejected.
15. **Direct-main fixture:** successful task commits and pushes only to `main` with no branch creation.

## 34. Implementation priority guidance

The later implementation plan should build v0.2 in vertical slices rather than implementing every analysis feature at once.

Recommended sequence:

1. typed domain state + risk model;
2. deterministic patch tool and drift guard;
3. repository symbol/index foundation;
4. typed RIG edges + query API;
5. test-impact/baseline/regression vertical slice;
6. plan-memory coupling;
7. hypothesis ledger + reproduction classes;
8. evidence packets + active context manager;
9. critic + alternative design gate;
10. history intelligence + validated lessons;
11. best-known-state recovery/deadlock detection;
12. interface/invariant verification;
13. model capability probes;
14. locked self-improvement evaluation harness;
15. repository-scale E2E acceptance suite.

This section is sequencing guidance, not the detailed implementation plan.

## 35. Final design contract

AlinaCoder v0.2 remains a **fully autonomous single-model coding agent**, not a committee of agents.

Its intelligence is grounded in five externalized cognitive capabilities:

1. **Repository understanding:** structured architecture/dependency/test/history evidence;
2. **Adaptive reasoning:** hierarchical plans, assumptions, falsifiable hypotheses and alternative designs;
3. **Critical verification:** impact-aware regression detection, behavior reproduction, interface/invariant checks and fresh verification claims;
4. **Learning:** validated episodic lessons and project-history patterns with provenance/freshness;
5. **Recovery:** progress-aware deadlock detection and return to the best known verified state.

The engineering target is not maximal complexity. It is **maximal useful autonomy per unit of complexity**, with every important decision tied to inspectable evidence and every published change proven as far as the local environment reasonably allows.
