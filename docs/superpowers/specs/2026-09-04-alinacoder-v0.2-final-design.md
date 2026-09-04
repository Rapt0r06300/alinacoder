# AlinaCoder v0.2 — Final Frozen Design Specification

Date: 2026-09-04  
Status: **FROZEN FOR IMPLEMENTATION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical development branch: `main` only  

## 1. Normative authority

This document is the **primary normative specification for AlinaCoder v0.2 implementation**.

It consolidates and supersedes the need to interpret the following documents independently during implementation, while preserving their compatible requirements:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.1-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-conversation-and-external-self-improvement-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-research-voice-context-specialists-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-resource-awareness-model-calibration-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-resource-anti-oscillation-checkpoints-amendment.md`

Historical specs remain useful provenance. If an implementation ambiguity exists, this frozen document wins unless an explicitly approved later spec reopens v0.2.

No new v0.2 feature should be introduced silently after this freeze. New capabilities belong to v0.3 unless the user explicitly reopens v0.2.

---

## 2. Product definition

AlinaCoder v0.2 is a fully autonomous, local, Windows-first coding agent powered by Ollama.

It must be capable of:

- understanding natural user intent in French;
- understanding highly noisy conversational/vocal French;
- reconstructing the correct project, goal, task or problem from context;
- understanding large code repositories structurally rather than as flat text;
- planning work hierarchically and revising plans when evidence changes;
- exploring multiple hypotheses and implementation alternatives;
- choosing simple, robust, testable solutions;
- editing code safely;
- running commands, tests, builds and verification;
- detecting its own mistakes and regressions;
- learning from project history and validated experience;
- researching current external information when needed;
- using conditional specialized reasoning when measured to help;
- adapting to actual machine resources;
- selecting local models using real repeated mini-tests on the target machine;
- recognizing when the local model or evidence is insufficient;
- decomposing tasks into simpler, more verifiable work;
- recovering from failure and returning to the best known valid state;
- improving its own implementation only under protected before/after evaluation;
- committing and pushing autonomously directly to `main` only when deterministic gates pass.

---

## 3. Non-negotiable invariants

1. **Full autonomy remains enabled.**
2. **Canonical Git development is direct to `main`.**
3. **No autonomous feature-branch/PR workflow in v0.2.**
4. **Python 3.12+** is the implementation language.
5. **Windows-first** is the supported operating-system target.
6. **Ollama is the local model provider.**
7. The model never directly bypasses deterministic shell/filesystem/Git/network policy.
8. Execution evidence outranks model claims.
9. Safety and verification floors cannot be traded for speed or apparent intelligence.
10. No push occurs with a red mandatory Done Contract.
11. Checkpoint, rollback, resume and BestKnownState are mandatory.
12. Memory is evidence, not authority; live repository state wins.
13. Self-improvement cannot weaken its evaluator or safety floor.
14. Resource pressure may change strategy, not correctness requirements.
15. Reliability and verifiability take precedence over maximal task breadth.
16. AlinaCoder may say that it does not know or cannot prove a task reliably enough.

---

## 4. Governing engineering priority

The v0.2 decision priority is:

```text
Safety
→ Correctness
→ Verifiability
→ Regression resistance
→ Architectural fit
→ Machine/model compatibility
→ Simplicity
→ Reversibility
→ Efficiency
→ Breadth / ambition
```

When two solutions are comparable, AlinaCoder chooses the smaller, easier-to-verify, easier-to-reverse solution.

---

## 5. Canonical cognitive loop

The full v0.2 loop is:

```text
Reconcile
→ Understand Intent
→ Recover Project Context
→ Localize
→ Gather Evidence / Research if needed
→ Hypothesize
→ Plan
→ Compare Alternatives
→ Critique / Seek Counter-Evidence
→ Check Capability + Resource Fit
→ Act
→ Reproduce / Verify
→ Impact / Regression Analysis
→ Critic Review
→ Reliability Assessment
→ Commit / Push
→ Learn
→ Next
```

Low-risk mechanical work may use a compressed path, but mandatory safety and verification gates remain.

---

## 6. High-level source architecture

Conceptual responsibilities:

```text
src/alinacoder/
├─ cli/
├─ core/
│  ├─ orchestrator.py
│  ├─ state_machine.py
│  └─ risk.py
├─ conversation/
│  ├─ session.py
│  ├─ natural_language.py
│  ├─ context_fusion.py
│  ├─ reference_resolution.py
│  └─ response_policy.py
├─ intelligence/
│  ├─ intent.py
│  ├─ intent_confidence.py
│  ├─ mission_compiler.py
│  ├─ planner.py
│  ├─ decision_engine.py
│  ├─ hypotheses.py
│  ├─ critic.py
│  ├─ reliability.py
│  ├─ task_decomposer.py
│  ├─ capability_policy.py
│  ├─ agent_value.py
│  └─ specialist_router.py
├─ providers/
│  ├─ ollama.py
│  ├─ model_probe.py
│  └─ model_selector.py
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
├─ research/
│  ├─ planner.py
│  ├─ source_broker.py
│  ├─ source_ranker.py
│  ├─ claim_grouper.py
│  ├─ contradiction.py
│  └─ evidence_bundle.py
├─ speech/
│  ├─ stream_state.py
│  ├─ disfluency.py
│  └─ repair.py
├─ resources/
│  ├─ discovery.py
│  ├─ controller.py
│  ├─ budgets.py
│  ├─ pressure.py
│  ├─ scheduler.py
│  └─ telemetry.py
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
├─ self_improvement/
│  ├─ supervisor.py
│  ├─ benchmark.py
│  ├─ experiment.py
│  ├─ evaluator.py
│  ├─ promotion.py
│  ├─ rollback.py
│  └─ version_history.py
├─ safety/
│  └─ policy.py
└─ network/
   └─ policy.py
```

Physical files may be merged when that improves clarity. Responsibility boundaries remain mandatory.

---

# Part I — Conversation and Intent

## 7. Conversation is the primary user interface

Running `alinacoder` opens a natural conversational session.

Structured commands such as `status`, `doctor`, `resume`, `memory`, `roadmap` and `config` remain available but are not required for normal use.

The user may speak naturally and non-technically.

Examples:

```text
continue
fini ce qu'on faisait
ça marche toujours pas
améliore jarvis sans tout refaire
regarde pourquoi ça plante quand je relance le truc
fais le plus simple mais robuste
reprends là où tu t'es arrêté
```

AlinaCoder must attempt contextual resolution before asking for clarification.

---

## 8. French as first-class language

The system must tolerate:

- spelling mistakes;
- missing accents;
- informal language;
- mixed French/English technical vocabulary;
- incomplete syntax;
- short commands;
- vague references such as `ça`, `le truc`, `comme avant`;
- user misconceptions about technical implementation.

The user does not need to translate intent into engineering instructions.

---

## 9. Noisy voice understanding

For streaming/transcribed speech, the system must preserve meaning-bearing disfluencies rather than cleaning them prematurely.

It must handle:

- hesitation;
- filler words;
- repetition;
- false starts;
- interrupted words;
- self-correction;
- correction mid-sentence;
- explicit reversal such as `non attends`;
- change of mind;
- partial interruption.

Intent fragments may be:

```text
TENTATIVE
CONFIRMED
REVISED
CANCELLED
```

Actions with material side effects must not start from a still-unstable spoken fragment.

---

## 10. Context fusion

Intent reconstruction may use:

- current conversation;
- active mission/task;
- repository and Git state;
- current diff;
- roadmap;
- project docs;
- tests/results;
- recent runtime failures;
- Repository Intelligence Graph;
- project decisions;
- episodic memory;
- validated lessons;
- history patterns;
- verification claims;
- unfinished work.

The smallest sufficient evidence set is preferred over dumping all context.

---

## 11. Intent confidence policy

Required classes:

```text
HIGH
MEDIUM
LOW
AMBIGUOUS_HIGH_IMPACT
```

Behavior:

- `HIGH`: proceed autonomously;
- `MEDIUM`: proceed with best-supported reversible interpretation;
- `LOW`: gather more evidence autonomously first;
- `AMBIGUOUS_HIGH_IMPACT`: ask one concise clarification only after context investigation fails to resolve safely.

Ambiguity alone is not a reason to stop autonomy.

---

# Part II — Repository Intelligence and Planning

## 12. Repository Intelligence Graph

AlinaCoder maintains an incremental graph of repository structure.

Core nodes include:

- repository;
- package/module;
- file;
- class;
- function/method;
- public symbol/interface;
- test file/test case;
- build/config artifact;
- dependency declaration.

Core edges include:

```text
CONTAINS
IMPORTS
CALLS
INHERITS
EXPORTS
DEPENDS_ON
BUILDS_WITH
TESTS
COVERS
CONFIGURES
CO_CHANGES_WITH
AFFECTS
```

Edges carry provenance/confidence where practical.

Large repositories use lightweight global indexing plus on-demand local expansion.

---

## 13. Hybrid retrieval

Retrieval combines:

1. lexical search;
2. symbol lookup;
3. graph traversal;
4. dependency/test-impact traversal;
5. Git/history search;
6. runtime evidence;
7. optional local similarity ranking only when justified.

Similarity-only repository understanding is forbidden.

---

## 14. Hierarchical adaptive planning

Planning hierarchy:

```text
Mission → Milestone → Task → Step
```

Plans are hypotheses, not truth.

They must be revised when:

- evidence contradicts an assumption;
- dependencies are broader than expected;
- reproduction remains unchanged;
- repeated edits do not improve verification;
- resource/capability constraints materially change feasibility.

---

## 15. Hypothesis-driven debugging

Nontrivial debugging stores multiple candidate root causes with:

- statement;
- supporting evidence;
- contradicting evidence;
- confidence;
- falsification probe;
- expected observation;
- status.

Reproduction is preferred before mutation where possible.

The first plausible explanation must not automatically trigger a broad patch.

---

## 16. Alternative solutions and self-critique

Medium/high-risk changes should compare 2–3 plausible approaches when meaningful.

Comparison dimensions include:

- behavioral correctness;
- architecture fit;
- transitive impact;
- regression risk;
- changed surface;
- simplicity;
- testability;
- reversibility;
- interface stability;
- dependency cost;
- project-history consistency.

A context-isolated critic must actively search for reasons the preferred design could be wrong.

---

# Part III — Research

## 17. Reliable internet research

External research is used when current external evidence materially affects correctness or freshness.

Typical triggers:

- current API/docs behavior;
- dependency/version issues;
- external standards;
- unfamiliar third-party systems;
- contradictory local evidence;
- comparison of viable engineering approaches.

Research must not be used merely to confirm an already-selected answer.

---

## 18. Source grouping and provenance

Research output is grouped by claim.

Each claim records:

- supporting sources;
- source type;
- freshness;
- authority;
- independence;
- contradictions;
- confidence;
- source pointers.

Default source preference usually favors:

1. official docs/spec/source;
2. primary research/benchmark artifacts;
3. maintainer release notes/issues;
4. established technical sources;
5. practitioner/community evidence when needed.

Search stops when further evidence has low decision value.

---

# Part IV — Verification and Regression Control

## 19. Test impact analysis

Before and after meaningful changes, AlinaCoder derives impacted tests from repository structure, dependencies, conventions and optional coverage.

Verification distinguishes:

- already failing before change;
- fail-to-pass target;
- previously passing and still passing;
- previously passing and now failing regression;
- unavailable/unrunnable.

A targeted fix cannot be promoted while relevant pass-to-pass regressions remain.

---

## 20. Done Contract

A task may be `DONE` only when:

1. acceptance criteria map to explicit evidence;
2. required reproduction/behavior is satisfied or evidence limitation is explicitly classified;
3. no relevant new regression remains;
4. required static/build/type checks pass;
5. public interfaces/invariants are validated for impacted scope;
6. critic has no unresolved critical finding;
7. diff remains in intended scope or expansion is justified;
8. Git/workspace state is reconciled;
9. verification claims are fresh;
10. task/memory state is persisted;
11. reliability meets the task floor.

Only then may commit/push occur.

---

## 21. Verification confidence

Required classes:

```text
PROVEN
STRONG
ADEQUATE
MARGINAL
UNRELIABLE
UNPROVABLE
```

Confidence is derived from evidence, not the model's confidence language.

---

# Part V — Memory and Learning

## 22. Typed durable memory

Memory classes include:

```text
FACT
DECISION
EPISODE
LESSON
INVARIANT
HISTORY_PATTERN
VERIFICATION_CLAIM
```

Each record should carry provenance, applicability scope and freshness.

Freshness states:

```text
FRESH
STALE
UNPROVABLE
SUPERSEDED
```

Live repository state can invalidate memory automatically.

---

## 23. Learning from errors

Attempts record:

- problem state;
- chosen hypothesis/design;
- actions;
- outcome;
- verification delta;
- regression delta;
- rollback/block/success cause.

A reusable lesson is promoted only when grounded, scoped and not contradicted by current state.

Negative lessons may capture when not to repeat a failed strategy.

---

## 24. Project history intelligence

Git history may provide:

- prior fixes;
- file/function evolution;
- co-change patterns;
- interface migration conventions;
- likely root-cause history;
- project-specific architectural practice.

History-derived claims retain commit provenance and may become stale.

---

# Part VI — Resource Awareness and Model Calibration

## 25. HardwareProfile versus DynamicLoadSnapshot

The runtime must keep fixed capability and temporary load separate.

### HardwareProfile

Relatively stable:

- CPU identity/core capacity;
- total RAM;
- GPU identity and total VRAM;
- machine architecture;
- storage characteristics;
- OS;
- Ollama version;
- installed model digests.

### DynamicLoadSnapshot

Transient:

- CPU utilization;
- available/committed RAM;
- paging pressure;
- GPU utilization;
- free/used VRAM;
- thermal signal where reliable;
- active workload pressure;
- measured latency;
- free disk.

Temporary load must not rewrite intrinsic hardware capability.

---

## 26. Global ResourceController

Resource budgets cover independently:

- CPU;
- GPU/VRAM;
- RAM;
- wall-clock time;
- context size;
- subprocess/test/index concurrency.

Default runtime profile is `AUTO`.

Other profiles may include:

```text
CONSERVATIVE
BALANCED
PERFORMANCE
```

Profiles control resource ceilings, never correctness floors.

---

## 27. Anti-oscillation

Dynamic pressure states:

```text
NORMAL
ELEVATED
HIGH
CRITICAL
```

Transitions use:

```text
repeated samples
→ smoothing
→ consecutive evidence
→ hysteresis
→ minimum dwell time
→ cooldown
```

A single noisy sample cannot trigger a model switch except for emergency protection.

When pressure disappears before a safe checkpoint, a pending switch may be cancelled.

---

## 28. Real repeated model mini-tests

Model selection is based on measured behavior on the actual machine, not parameter count or VRAM alone.

Mandatory probe families include:

- structured output compliance;
- instruction adherence;
- code localization;
- causal code reasoning;
- patch quality;
- regression awareness;
- French understanding;
- noisy/ambiguous intent handling;
- context use;
- latency/resource fit.

Important probes use repeated trials/variants, typically 3–5 where cost permits.

Reports include central result, variance, worst-tail behavior, schema failures, regression misses, p50/p95 latency where meaningful, OOM/crashes and load conditions.

Repeated reliability is preferred over one exceptional run.

---

## 29. Stable model capability identity

Durable `ModelCapabilityProfile` identity is based on:

```text
model_digest
HardwareProfile fingerprint
Ollama version
probe-suite version
```

Dynamic load is benchmark metadata, not capability identity.

A contaminated benchmark trial may be repeated instead of permanently penalizing capability.

---

## 30. Model switching only at checkpoints

A model must not change during an atomic reasoning/execution phase.

Required `ModelSwitchCheckpoint` classes:

```text
TASK_START
TASK_END
PLAN_REVISED
RECOVERY_COMPLETED
CONTEXT_CONDENSED
EXPLICIT_SAFE_CHECKPOINT
```

Forbidden switch windows include:

- active patch generation/write;
- hypothesis + immediate falsification probe;
- active command/test;
- Git commit;
- memory transaction;
- rollback/recovery mutation.

Switch protocol:

```text
persist state
→ capture Git/workspace
→ close reasoning phase
→ select candidate
→ switch
→ smoke probe
→ accept or restore previous model
→ resume
```

---

## 31. Weak-model detection

Weakness is task-relative.

Signals include:

- probe score below task requirement;
- repeated schema errors;
- localization failures;
- constraint violations;
- critic repeatedly finding basic mistakes;
- high independent-pass disagreement;
- context saturation;
- regression misses;
- tool misuse;
- poor calibration.

---

## 32. Reliability-first fallback

If model/task fit is insufficient:

```text
collect deterministic evidence
→ shrink context
→ reduce scope
→ decompose task
→ improve reproduction/tests
→ choose smaller reversible patch
→ reassess
```

If reliability remains insufficient, AlinaCoder may explicitly conclude:

```text
Je ne sais pas avec assez de fiabilité.
```

or classify the task `UNRELIABLE` / `UNPROVABLE`.

This is correct behavior, not an autonomy failure.

---

# Part VII — Conditional Specialists

## 33. Specialist reasoning is conditional

The default remains one active general model path.

Temporary specialist roles may be used when the `AgentValueEstimator` predicts measurable benefit, for example:

- Researcher;
- Repository Architect;
- Debugger;
- Regression Reviewer;
- Security Critic;
- Alternative Designer.

Specialist output is advisory evidence. It cannot bypass deterministic verification.

---

## 34. Resource-aware specialist routing

A specialist is used only if:

```text
expected quality gain
> resource cost + latency cost + coordination risk
```

Under pressure, prefer sequential specialists, fewer specialists or deterministic tools instead of fan-out.

Multi-agent use must be benchmarked; if it does not improve hidden outcomes for a task class, it should not be activated for that class.

---

# Part VIII — External Self-Improvement

## 35. Independent supervisor

Self-improvement uses an external supervisor around the stable runtime.

Canonical flow:

```text
Stable Version
→ benchmark BEFORE
→ improvement hypothesis
→ isolated candidate copy
→ modification
→ tests
→ benchmark AFTER
→ compare
→ PROMOTE / REJECT / WATCH
→ rollback if later evidence is worse
```

Canonical Git history remains on `main`; experiments may use disposable local copies but no GitHub feature branches.

---

## 36. Evaluation hierarchy

Self-improvement comparison priority:

```text
Safety
→ Correctness
→ Regression
→ Reliability
→ Reasoning quality
→ Conversation quality
→ Resource stability
→ Efficiency
→ Complexity
```

No gain on a lower dimension compensates for violating a mandatory higher-level floor.

---

## 37. Hidden benchmarks

Evaluation is separated into:

```text
DEVELOPMENT
VALIDATION_HOLDOUT
HIDDEN_HOLDOUT
CANARY
```

The candidate may receive detailed development feedback.

Hidden cases, expected outputs and adversarial details remain outside the candidate context.

The hidden suite must cover:

- regression detection;
- intent resolution;
- noisy French;
- research-source quality;
- contradiction handling;
- model selection;
- resource oscillation;
- checkpointed switching;
- weak-model abstention/decomposition;
- multi-agent value decisions;
- evaluator-gaming attempts.

Self-improvement benchmarks use repeated robust trials where stochastic behavior matters.

---

## 38. Anti-gaming

Evaluation scripts/configuration used for promotion must be protected through checksums/read-only or equivalent integrity mechanisms where practical.

A candidate that weakens evaluation rather than improving behavior is rejected.

---

# Part IX — Recovery and Git

## 39. BestKnownState

Recovery does not blindly return to the latest state.

States are compared using ordered evidence including:

1. safety violations;
2. acceptance/reproduction status;
3. newly introduced regressions;
4. required static/build/type status;
5. targeted tests;
6. diff/risk size;
7. unresolved critical hypotheses.

A state with a regression cannot outrank a clean state merely because it passes more unrelated tests.

---

## 40. Deadlock detection

Detect:

- repeated normalized actions;
- repeated same error;
- edit/revert loops;
- no verification-vector improvement;
- diff growth without localization improvement;
- repeated model switching without progress;
- repeated plan revision without new evidence.

Deadlock triggers strategy change, evidence gathering, task decomposition, model pinning, best-state restoration or block.

---

## 41. Direct-to-main Git contract

Before commit:

- branch is `main`;
- working tree is reconciled;
- tracked run owns its changes;
- no stale external modifications collide;
- Done Contract is green.

Commit scope should be small and coherent.

Push directly to `main` after verification.

No autonomous force-push.

If upstream moved, reconcile safely and rerun affected verification before pushing.

---

# Part X — Observability and CLI

## 42. CLI commands

Required commands include:

```text
alinacoder
alinacoder run
alinacoder resume
alinacoder status
alinacoder doctor
alinacoder chat
alinacoder stop
alinacoder config
alinacoder memory
alinacoder roadmap
```

Normal conversational output remains concise. Detailed evidence is available via verbose/debug/logs.

---

## 43. Structured events

Important event families include:

- run/task lifecycle;
- intent/context resolution;
- evidence/research;
- hypotheses/planning;
- impact/regression;
- critic/reliability;
- memory/lesson freshness;
- recovery/best-state;
- hardware/load/resource pressure;
- model probing/selection/switching;
- self-improvement/benchmarking.

Logs must preserve evidence needed for reproducibility without storing hidden private reasoning transcripts.

---

# Part XI — v0.2 Implementation Acceptance

## 44. Mandatory acceptance scenarios

Implementation is not complete until automated fixtures/E2E tests prove at least:

### Core autonomy
1. explicit user goal is executed autonomously end-to-end;
2. next roadmap task can be inferred without an explicit goal;
3. successful work commits/pushes directly to `main` only after verification.

### Conversation/context
4. `continue` resumes the correct unfinished task;
5. short imperfect French maps to the correct objective;
6. noisy spoken self-correction updates intent instead of executing stale intent;
7. ambiguous project reference is resolved from project state when evidence is sufficient.

### Repository intelligence
8. relevant symbols are found without reading the whole repo;
9. transitive dependency impact beyond one hop is found;
10. project history informs a fix without blindly copying stale code.

### Reasoning/debugging
11. initially plausible false hypothesis is rejected by evidence;
12. smaller robust design is chosen over unnecessary complexity;
13. critic catches at least one intentionally seeded regression/omission fixture.

### Verification
14. fail-to-pass target is fixed;
15. pass-to-pass regression blocks promotion;
16. stale verification claim is invalidated after supporting artifact changes.

### Recovery
17. interrupted task resumes coherently;
18. deadlock is detected and strategy changes;
19. BestKnownState restores a cleaner earlier state when later state regresses.

### Research
20. official/primary evidence outranks weak conflicting sources when appropriate;
21. sources are grouped by claim and contradictions surfaced;
22. research stops when marginal evidence no longer affects the decision.

### Resource/model
23. HardwareProfile and DynamicLoadSnapshot remain distinct;
24. one noisy load sample does not trigger a resource transition;
25. hysteresis/dwell/cooldown prevent oscillation;
26. model switch is impossible outside a safe checkpoint;
27. pending transient switch can be cancelled before checkpoint;
28. repeated mini-tests penalize unstable model performance;
29. biggest model can lose to a smaller model on measured reliability;
30. weak model causes task decomposition instead of reckless broad edit;
31. insufficient evidence yields `UNRELIABLE`/`UNPROVABLE` rather than invented certainty.

### Specialists
32. specialist fan-out is rejected when measured gain does not justify resource/coordination cost;
33. specialist use is enabled when hidden evaluation proves benefit for that task class.

### Self-improvement
34. candidate improvement is measured before/after in isolation;
35. hidden holdout cannot be read by candidate;
36. candidate that improves visible metric but breaks a safety/regression floor is rejected;
37. previously promoted version can be rolled back when later robust evidence is worse;
38. evaluator gaming is detected/rejected.

---

## 45. Implementation sequence

The implementation plan should build vertical slices in this order unless later evidence justifies a small reordering:

1. Python package/CLI skeleton and typed domain models;
2. HardwareProfile + DynamicLoadSnapshot;
3. ResourceController state machine with anti-oscillation;
4. repeated model-probe framework;
5. checkpointed model selection/switching;
6. SQLite run/task/checkpoint state;
7. workspace boundaries + deterministic patch tool;
8. shell/Git/test tools and Done Contracts;
9. orchestrator vertical loop;
10. repository index/RIG and test impact;
11. hypothesis/reproduction/critic/reliability;
12. context fusion + natural French intent;
13. noisy voice incremental intent state;
14. history/lessons/freshness;
15. reliable internet research;
16. conditional specialist routing;
17. BestKnownState/deadlock/recovery;
18. external self-improvement supervisor + hidden evaluation;
19. repository-scale E2E acceptance suite;
20. observability/doctor/packaging polish.

This is sequencing guidance; the detailed TDD implementation plan is a separate artifact produced after this spec is reviewed.

---

## 46. Frozen-scope rule

This document freezes v0.2 for implementation.

After this commit:

- implementation should target this contract;
- bug fixes, clarifications and test-derived corrections are allowed if they do not silently add product scope;
- new major capabilities should be proposed as v0.3;
- reopening v0.2 scope requires explicit user approval and a new normative amendment.

---

## 47. Final design contract

AlinaCoder v0.2 is a **fully autonomous, evidence-driven, machine-aware coding agent** that behaves naturally in French while remaining deterministic where execution and verification matter.

It must understand the user's real intent, recover the correct project context, understand repository architecture and history, gather trustworthy evidence, compare alternatives, challenge its own conclusions, choose the smallest robust solution, adapt to the actual machine without oscillating, select local models through repeated real tests, change models only at recoverable checkpoints, detect when it is not reliable enough, decompose work when necessary, verify regressions rigorously, recover to the best known valid state, and publish only verified work directly to `main`.

The final governing principle is:

> **Understand deeply, measure reality, prefer simple verifiable work, adapt without oscillation, never invent confidence, and only publish what the evidence supports.**
