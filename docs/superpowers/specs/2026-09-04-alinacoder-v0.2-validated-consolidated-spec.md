# AlinaCoder v0.2 — Validated Consolidated Specification

Date: 2026-09-04  
Status: **V0.2 DESIGN VALIDATED FOR IMPLEMENTATION — RUNTIME NOT YET IMPLEMENTED**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Role of this document

This document is the canonical human-readable current view of AlinaCoder v0.2.

It does not delete, rewrite or invalidate the approved historical specifications. Instead, it incorporates them through the machine-readable `2026-09-04-alinacoder-v0.2-normative-manifest.json`, applies the precedence and conflict rules established by the Spec Constitution amendment, and gives implementers one coherent system contract.

The historical files remain authoritative provenance. If this consolidated view accidentally omits a stricter active rule from an incorporated amendment, the stricter active rule remains binding until the compiler/conflict process explicitly resolves it. Silent downgrade is forbidden.

After this consolidation, new non-critical feature research should normally target v0.3. A v0.2 amendment after this point is appropriate only for a critical correction, contradiction, security issue or implementation-blocking ambiguity.

## 2. Product definition

AlinaCoder is a Windows-first, Python 3.12+ autonomous software-engineering agent whose primary daily surface is a single conversational desktop application, `AlinaCoder.exe`.

The intended experience is:

```text
User speaks/types naturally in French
→ AlinaCoder resolves current intent, context and visible references
→ strongest currently eligible zero-cost intelligence is selected
→ repository and project state are inspected
→ plan and bounded work are executed
→ tests and independent evidence verify progress
→ safe changes are committed directly to main
→ verified state, memory and lessons are persisted
→ the conversation continues without the user rebuilding context
```

The user should not normally need a separate terminal, Git client, model selector, memory editor or provider dashboard.

## 3. Constitutional invariants

The following rules are non-negotiable across every subsystem.

### ALINA.COST.ZERO.001 — zero autonomous monetary spend

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
ALLOW_PAID_FALLBACK = false
ALLOW_AUTO_RELOAD = false
```

Unknown cost or overage behavior means the remote route is ineligible.

### ALINA.GIT.MAIN_ONLY.001 — main only

Canonical work, commits and pushes occur on `main`. The runtime must not invent a feature-branch/PR workflow for ordinary execution.

### ALINA.INTENT.USER_AUTHORITY.001 — user intent outranks model inference

The current grounded user intent, approved project constitution and verified environment state govern action. A model proposal cannot silently redefine the task.

### ALINA.STATE.CANONICAL.001 — one canonical versioned state

Conversation, plans, UI, tools, memory and model handoffs consume the same versioned canonical state. Stale in-flight output cannot mutate newer state.

### ALINA.EFFECT.MEDIATION.001 — proposals do not directly cause durable effects

Durable writes/effects pass typed authority, freshness, state and verification gates outside ordinary free-form model reasoning.

### ALINA.VERIFY.EVIDENCE.001 — completion requires evidence

“Done” is an evidence-carrying state, not a model utterance. Relevant tests, artifact checks and Done Contracts must pass.

### ALINA.MEMORY.PROVENANCE.001 — evidence before belief

Derived memories remain linked to their source evidence, temporal validity and authority. Contradictions and supersession are explicit.

### ALINA.PROVIDER.LIVE_PROOF.001 — static model/provider facts never authorize a call

Pricing, quota, entitlement, availability and model identity are volatile runtime facts and require current official/account proof.

### ALINA.RECOVERY.DURABLE.001 — recover from verified checkpoints

Crash, timeout, provider failure or model switch may not destroy verified progress or duplicate side effects.

### ALINA.SPEC.NO_SILENT_DOWNGRADE.001 — cumulative spec integrity

No implementation may weaken an approved invariant because a newer summary forgot to repeat it.

## 4. Canonical architecture

AlinaCoder is organized as cooperating planes rather than one unconstrained model loop.

### 4.1 Interaction Plane

Responsibilities:

- ordinary French text and optional voice;
- evolving-intent tracking;
- repair/correction handling;
- reference resolution;
- common-ground maintenance;
- context branching and context surgery;
- clarification policy;
- visible artifact anchoring;
- user steering, pause, takeover and resume;
- unified desktop workbench.

### 4.2 Cognitive Plane

Responsibilities:

- Intent Beam and Grounded Intent Contract;
- uncertainty and ask/infer/retrieve decisions;
- repository/project understanding;
- hypothesis generation and discriminating probes;
- planning and alternative evaluation;
- specialist councils only when measured useful;
- prediction-before-action;
- causal debugging;
- bounded reasoning modes.

### 4.3 Control Plane

Responsibilities:

- policy and authority ceilings;
- semantic action schemas;
- taint/provenance controls;
- cost and privacy eligibility;
- state leases and fencing;
- resource budgets;
- external effect admission;
- cancellation/revocation;
- specification snapshot binding.

### 4.4 Execution Plane

Responsibilities:

- repository reads/writes;
- commands and tests;
- package/build tooling;
- Git operations;
- research/tool calls;
- local and remote model invocation;
- artifact production.

Execution does not self-certify success.

### 4.5 Evidence and Record Plane

Responsibilities:

- immutable/raw evidence;
- event-sourced canonical state;
- test evidence;
- review evidence;
- provenance;
- transaction journals;
- failure history;
- rollback checkpoints;
- audit reports.

### 4.6 Memory Plane

Responsibilities:

- working context;
- episodic/project memory;
- semantic and ontology memory;
- AST/code memory;
- causal state anchors;
- user-confirmed preferences;
- Experience Cards and SkillBook;
- freshness, contradiction and forgetting detection;
- hybrid lexical/semantic/graph retrieval.

### 4.7 Frontier Intelligence Plane

Responsibilities:

- discover candidate local and remote models/providers;
- prove exact zero-cost entitlement and billing safety;
- attest model identity and protocol capabilities;
- maintain capability/knowledge posteriors;
- route by task/stage capability requirements;
- preserve task affinity;
- perform same-lineage hosting failover cheaply;
- perform cross-lineage cognitive switches only when expected terminal benefit exceeds handoff tax;
- maintain standby continuity capsules and quota reserves;
- quarantine stale, paid, privacy-ineligible or degraded routes.

### 4.8 Self-Improvement Plane

Responsibilities:

- benchmark current behavior before modification;
- mine verified failures and user corrections;
- propose skills, procedures, router changes or bounded harness changes;
- validate on protected holdouts/canaries;
- promote only with evidence;
- preserve rollback and negative knowledge;
- never use self-confidence as promotion evidence.

## 5. Canonical mission lifecycle

```text
Receive user turn / voice / UI action
→ capture raw evidence
→ repair graph + evolving-intent update
→ resolve visible/contextual references
→ compile active conversation/project context
→ clarification value decision
→ GroundedIntentContract
→ retrieve governed memory and repository state
→ capability requirements + route eligibility
→ choose strongest proven zero-cost regime
→ build bounded mission / plan node
→ predict expected state transition
→ execute under semantic transaction + authority leases
→ observe real environment
→ independent verification / tests
→ update verified canonical state
→ repair or continue
→ enforce final Done Contract
→ commit/push main when allowed and verified
→ persist evidence-linked memory/lessons
→ refresh continuity/standby state
→ continue conversation
```

## 6. Conversation and human-machine understanding contract

The user-facing conversation is not a flat transcript. The raw chronological transcript is preserved as evidence, while active reasoning uses a structured `ConversationContextGraph`.

The graph supports typed relationships such as:

```text
REFERS_TO
CORRECTS
REPLACES
CANCELS
NARROWS
EXTENDS
DEPENDS_ON
CONFLICTS_WITH
SUPPORTS
SUPERSEDES
BRANCHES_FROM
MERGES_INTO
GROUNDS
```

### 6.1 Mainline and branches

Side questions, alternatives, temporary research and abandoned ideas may form branches. Inactive branches do not pollute the active task merely because they are older chat history.

The user can explicitly branch, return, include, exclude, pin or promote context. AI may suggest structural changes but may not silently change a consequential mainline interpretation.

### 6.2 Local corrections

Corrections mutate the narrowest justified semantic scope. A correction to one function, plan node or test must not reset unrelated constraints or completed verified work.

### 6.3 Perspective ledger

AlinaCoder distinguishes:

```text
USER_STATED
USER_CONFIRMED
USER_RETRACTED
ASSISTANT_INFERRED
ASSISTANT_PROPOSED
TOOL_OBSERVED
REPOSITORY_OBSERVED
EXTERNAL_SOURCE_CLAIM
MUTUALLY_GROUNDED
UNKNOWN
DISPUTED
```

An assistant inference does not become a user belief through repetition.

### 6.4 Clarification regret

Clarification is a sequential control decision. The assistant considers information gain, probability the answer changes the next action, consequence of a wrong assumption, user interruption cost, delay and redundancy.

It should first use safe retrieval, repository inspection or read-only probes when these can resolve ambiguity better. It stops asking once residual ambiguity cannot materially change the next safe action or terminal result.

### 6.5 Visible-object references

Every meaningful visible object in the workbench can receive a stable anchor: plan node, file, symbol, diff hunk, test, error, decision, memory item, commit or research evidence.

Expressions such as “ça”, “celui-là”, “cette étape” or “le deuxième” are resolved using explicit language, explicit selection, current focus, task structure and recency. An anchor never silently retargets after its underlying artifact changes.

### 6.6 User steering

A user intervention is scoped by mode, scope and abstraction level. Targeted correction should lead to targeted replanning, with unaffected plan boundaries frozen where possible.

Plan nodes may be owned by `ALINA`, `USER`, `SHARED`, `PAUSED`, `REVIEW_REQUIRED` or `BLOCKED`. Human edits are reconciled into canonical state rather than treated as drift to be overwritten.

### 6.7 Correction-derived runtime rules

Repeated, verified user corrections may become scoped enforcement rules only when they have user-originating evidence, bounded scope, counterexamples, deterministic semantics, tests and a revocation path.

This forbidden loop is constitutional:

```text
assistant proposes a preference
→ assistant repeats it
→ memory labels it as user preference
→ runtime enforces it
```

Only user-originating evidence or explicit user confirmation can cross the user-authority boundary.

## 7. Unified AlinaCoder.exe workbench

The primary surface is a clean conversation-first Windows application with progressive disclosure.

Default surfaces:

- conversation and composer;
- concise current task/status;
- collapsible plan;
- collapsible context map;
- workspace/file inspection;
- verification/tests;
- Git state;
- run inspector;
- memory and provider diagnostics in advanced views.

The plan must remain persistent and directly selectable. Context and plan edits update canonical backend state rather than an isolated UI copy.

The user must be able to:

- interrupt a response;
- redirect work mid-run;
- pause and resume;
- select an artifact and refer to it naturally;
- edit a plan or artifact locally;
- inspect why a warning exists;
- request a targeted verification;
- take over a step and return it to Alina;
- stop all AlinaCoder-managed work through a visible control.

The UI shows concise reasons, evidence, state transitions and verification. Private chain-of-thought is not a product surface.

## 8. Voice contract

Voice and text feed the same intent/state system.

Voice must support semantic turn states, interruption, pauses, backchannels, speaker-directedness and playback-grounded context. Silence alone is not sufficient endpoint evidence.

Generated speech not actually played to the user cannot become normal shared context. After interruption, unheard output is revoked from the conversational basis before new user input is processed.

Voice quality is evaluated end-to-end on grounded tasks under accents, noise, hesitation, technical identifiers and mixed French/English developer vocabulary, not only on clean ASR accuracy.

## 9. Software-engineering intelligence contract

Repository work is evidence-grounded and long-horizon aware.

Required behaviors include:

- repository topology and dependency understanding;
- history and blame-aware reasoning where useful;
- implicit requirement recovery;
- explicit assumptions and unknowns;
- bounded plans with dependency-aware nodes;
- tests before/after changes where appropriate;
- candidate-first patch application;
- stale-patch and stale-state protection;
- targeted repair rather than blind repeated edits;
- architectural immunity and regression surfaces;
- dual executable contracts for desired behavior and verification;
- verifier co-evolution without circular self-certification;
- long-horizon progress accounting and calibrated stopping;
- exact evidence for completion.

Current external research further confirms that long-horizon repository construction and terminal work remain difficult even for frontier agents. Therefore v0.2 must treat long-horizon verification, progress state and stopping discipline as core architecture rather than optional polish.

## 10. Semantic transactions, authority and recovery

Every material mutation is a semantic transaction bound to exact canonical state, authority, policy epoch and artifact preconditions.

Concurrent or delayed workers cannot commit stale work. Cancellation and timeout revoke outstanding mutation authority.

Recovery is journaled and idempotent. Restart must reconcile whether an effect occurred rather than blindly repeat it.

High-impact durable state such as memory promotion, provider enrollment, skill promotion, policy updates or Git commits passes pre-persistence governance.

## 11. Verification and formal assurance

No single verifier is a universal proxy for user intent. Verification is layered:

```text
task-native tests
+ static/deterministic checks
+ artifact/state inspection
+ contract checks
+ independent agent review when useful
+ user verification for irreducibly subjective intent
```

Generator and verifier do not gain authority merely by agreeing.

Verification evidence is bound to exact candidate artifacts and becomes stale when relevant inputs change.

## 12. Memory integrity

Memory is infrastructure, not prompt decoration.

Rules include:

- raw source evidence preserved before derived memory;
- derived facts carry provenance and temporal validity;
- contradictory/superseded memories remain traceable;
- retrieval is multi-route rather than embedding-only;
- code memory includes AST/symbol/dependency structure;
- causal and decision-critical anchors are preserved for long-horizon tasks;
- stale or low-trust memory cannot silently authorize effects;
- user preferences require actual user evidence;
- memory compaction cannot erase critical constraints without detection;
- forgetting detection compares expected anchors with compiled context.

Optional Supabase may mirror non-secret metadata and support lexical/vector hybrid retrieval with RLS, but local storage remains canonical and offline-capable.

## 13. Resource and model calibration

`HardwareProfile` describes relatively stable machine capacity. `DynamicLoadSnapshot` describes current pressure.

Resource control uses budgets for CPU, GPU, VRAM, RAM, context, time, concurrency and background work.

Model/resource switching uses smoothing, hysteresis, dwell time and cooldown. Heavy local models unload when idle. The UI remains lightweight.

## 14. Zero-cost frontier fabric

The provider/model registry is dynamic.

Concrete provider names and model prices in historical specs are research snapshots, not authorization. Live runtime proof decides eligibility.

The fabric maintains:

- official/account evidence and freshness;
- exact route-level `CostProofReceipt`;
- billing-surface proof and zero-overage guarantee;
- provider/model identity attestation;
- capability and knowledge-freshness profiles;
- privacy, data-use and license eligibility;
- quotas and protected recovery reserves;
- health/circuit breakers;
- model lineage and failure-domain graphs;
- provider protocol/tool/schema reliability;
- champion/challenger evidence;
- task affinity and switch hysteresis;
- standby continuity state;
- chaos tests for route failure.

Same model through two providers is hosting redundancy, not cognitive diversity.

## 15. Continuity across models and crashes

The `ContinuitySpine` stores versioned verified state: current intent, constraints, repository identity, Git state, plan, evidence, artifacts, failures, pending work and rollback checkpoints.

Model handoff transfers this canonical state rather than an unbounded reasoning trace.

Before takeover, the target route must prove understanding of the relevant state and next action. Partial streamed output cannot become canonical state.

## 16. Research and self-improvement

Research is provenance-backed and freshness-aware. External claims remain evidence, not authority.

Self-improvement follows:

```text
measure baseline
→ state hypothesis
→ make isolated candidate change
→ run deterministic tests + protected evaluation
→ compare
→ promote/reject/watch
→ retain rollback and negative lesson
```

User corrections can improve pragmatic understanding and scoped runtime checks, but cannot cause unreviewed global personality/policy mutation.

## 17. Specification governance

The active v0.2 contract is determined by the normative manifest plus the precedence/conflict rules from the Spec Constitution amendment.

Rule categories include:

```text
DURABLE_NORMATIVE_RULE
VOLATILE_RUNTIME_FACT
HISTORICAL_SNAPSHOT
RESEARCH_PRIOR
EXAMPLE_ONLY
```

Volatile facts cannot authorize current behavior.

The future implementation must generate a deterministic compiled policy bundle and `SpecificationSnapshotID`. Missions bind to a snapshot; safety/intent-relevant spec changes require safe revalidation.

## 18. Evaluation matrix

A v0.2 runtime is not accepted until it demonstrates all of the following families.

### 18.1 Conversation

- evolving intent;
- correction/negation;
- branch isolation;
- deictic visible-object references;
- clarification stopping;
- user preference revision;
- repeated correction without repeated violation;
- French noisy/hesitant input.

### 18.2 Repository engineering

- multi-file bug repair;
- feature addition;
- dependency-sensitive refactor;
- implicit requirement recovery;
- test generation/use;
- regression detection;
- partial failure and recovery;
- long-horizon task completion without premature stopping.

### 18.3 Control and safety

- stale response rejection;
- cancellation fencing;
- stale patch rejection;
- effect idempotency;
- untrusted repository instructions treated as data;
- memory promotion governance;
- exact `main` enforcement.

### 18.4 Provider fabric

- free route disappears;
- quota exhausted;
- model alias changes;
- provider timeout;
- same-lineage failover;
- cognitive failover;
- no eligible cloud route;
- local-only fallback;
- zero paid calls under every test.

### 18.5 Continuity

- process crash;
- restart during mission;
- model switch;
- user correction while a model call is in flight;
- partial stream failure;
- recovery without duplicate side effect.

### 18.6 Desktop UX

- clean first-run startup;
- ordinary chat use without advanced panels;
- pause/resume;
- all-stop behavior;
- plan/artifact selection;
- targeted edit and continuation;
- verification visibility;
- low idle resource use.

## 19. Release gates

### SPEC_READY

This specification is `SPEC_READY` when:

- all approved v0.2 documents are enumerated in the manifest;
- precedence is explicit;
- no known unresolved contradiction is silently ignored;
- all major subsystems have implementation and acceptance contracts;
- volatile provider facts are separated from durable rules.

### IMPLEMENTATION_READY

The repository is `IMPLEMENTATION_READY` when an implementation plan maps every active rule/domain to code, tests and evidence.

### RUNTIME_ALPHA_READY

Requires an installable executable, working core loop, local model path, basic conversation, repository operations, tests, main-only Git, crash recovery and zero-cost enforcement.

### RUNTIME_V0_2_READY

Requires the full acceptance matrix, reproducible clean-Windows installation, packaged `AlinaCoder.exe`, end-to-end hidden evaluations, security/control tests, provider-failover tests, conversation/voice tests, durable recovery and release artifacts.

No documentation status may substitute for these runtime gates.

## 20. Implementation order

Recommended dependency order:

1. project skeleton, packaging, deterministic configuration and local state;
2. compiled spec/rule registry and constitutional gates;
3. canonical session state + event journal + recovery;
4. repository reader/indexer and bounded semantic actions;
5. local model adapter and capability interface;
6. intent/repair/context conversation core;
7. planner/executor/verifier loop and Done Contracts;
8. Git main-only transaction path;
9. memory/governance and retrieval;
10. zero-cost provider discovery/routing/continuity;
11. unified desktop workbench and artifact anchoring;
12. voice streaming/duplex behavior;
13. self-improvement and benchmark labs;
14. clean-Windows packaging, installer and release validation.

Each phase is TDD/evidence-driven and may not claim completion from code existence alone.

## 21. Current validation verdict

At the design level, v0.2 is now sufficiently specified to stop accumulating broad new architecture and begin implementation planning.

The architecture covers the major dimensions repeatedly surfaced in current research:

- human intent and evolving conversation;
- long-horizon state and memory;
- repository reasoning;
- planning and execution;
- independent verification;
- effect authority;
- crash recovery;
- human steering;
- desktop/voice interaction;
- model/provider routing;
- cost/privacy/resource governance;
- self-improvement;
- spec traceability.

This does **not** mean the software is ready to use.

At the time of this design freeze, the repository root contains documentation rather than an implemented runtime. Therefore the correct state is:

```text
SPEC_READY = YES
IMPLEMENTATION_READY = NOT YET PROVEN
RUNTIME_ALPHA_READY = NO
RUNTIME_V0_2_READY = NO
```

## 22. Final v0.2 target

```text
Open AlinaCoder.exe
→ speak or type naturally
→ optionally select visible objects instead of restating context
→ Alina preserves the exact active task and constraints
→ it asks only high-value clarification
→ it chooses the strongest proven zero-cost intelligence for the stage
→ it edits and tests the repository under deterministic authority gates
→ the user may interrupt, correct, pause, take over or resume at any time
→ verified progress survives model switches and crashes
→ no paid route activates automatically
→ no stale response or stale memory can override current intent
→ completion is proven by evidence
→ verified work is committed directly to main
→ the next conversation continues from the same grounded state
```

That is the validated v0.2 design contract.