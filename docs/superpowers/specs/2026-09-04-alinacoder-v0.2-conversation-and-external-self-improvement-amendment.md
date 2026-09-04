# AlinaCoder v0.2 — Conversational Intelligence and External Self-Improvement Amendment

Date: 2026-09-04  
Status: Approved normative amendment to AlinaCoder v0.2  
Repository: `Rapt0r06300/alinacoder`  
Canonical development branch: `main` only  
Extends: `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`

## 1. Normative status

This document is an **official extension of the AlinaCoder v0.2 design specification**. It does not replace or weaken the existing v0.2 architecture. All compatible v0.2 decisions remain mandatory.

Where this amendment adds stronger requirements for conversational intelligence, intent understanding, autonomous planning, project-context fusion, or self-improvement, the stronger requirement defined here is normative.

The following invariants remain unchanged:

1. AlinaCoder retains **full autonomy**.
2. AlinaCoder may understand, plan, edit, test, diagnose, recover, commit and push autonomously when deterministic gates pass.
3. Canonical development and publication happen **directly on `main`**.
4. No GitHub feature branch or PR workflow is introduced by this amendment.
5. AlinaCoder remains **Ollama-only** and uses one selected local model.
6. The system remains Windows-first and Python 3.12+.
7. Execution evidence outranks model claims.
8. Safety, regression and evaluator-integrity floors cannot be traded away for apparent intelligence gains.

This amendment adds two major capabilities:

- an **External Self-Improvement Supervisor** that evaluates candidate improvements independently with before/after measurements and automatic rollback;
- a **Natural Conversational Intelligence Layer** that lets the user speak naturally in French, including short, imperfect, ambiguous or non-technical requests, while AlinaCoder reconstructs intent and autonomously determines the technical work.

---

## 2. Product objective

AlinaCoder should feel natural to use in the same broad sense as a strong conversational coding assistant: the user expresses what they want in ordinary language, and AlinaCoder determines how to achieve it from the actual repository state.

The user must not need to know:

- which file should be edited;
- which symbol is responsible;
- which command should be executed;
- which test should be run;
- which dependency is involved;
- which architectural layer owns the behavior;
- how to formulate an implementation plan;
- how to reproduce a bug technically;
- how to choose between alternative designs.

The central interaction rule is:

> **The user expresses intent. AlinaCoder reconstructs context, determines the engineering objective, plans the implementation, verifies the result and continues autonomously.**

This principle must hold even when the user's request is short, informal, non-technical, partially incorrect or linguistically imperfect.

---

## 3. Updated source architecture

The v0.2 source architecture is extended with the following responsibility boundaries:

```text
src/alinacoder/
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
│  └─ confidence.py
├─ self_improvement/
│  ├─ supervisor.py
│  ├─ benchmark.py
│  ├─ experiment.py
│  ├─ evaluator.py
│  ├─ promotion.py
│  ├─ rollback.py
│  └─ version_history.py
└─ ... existing v0.2 modules ...
```

Implementation may merge very small modules when doing so improves clarity. The conceptual boundaries remain mandatory even if fewer physical files are used.

---

# Part I — Natural Conversational Intelligence

## 4. Conversation is the primary interface

Running:

```powershell
alinacoder
```

opens a natural conversational session.

Structured commands such as `alinacoder status`, `doctor`, `resume`, `memory` and `roadmap` remain available for scripting, diagnostics and explicit control, but they must not be required for normal use.

The user should be able to write ordinary messages such as:

```text
continue
```

```text
fini ce qu'on faisait
```

```text
ça marche toujours pas
```

```text
améliore jarvis sans tout refaire
```

```text
regarde pourquoi ça plante quand je relance le truc
```

```text
fais le plus simple mais robuste
```

```text
reprends là où tu t'es arrêté hier
```

```text
termine la roadmap
```

```text
je veux que ça comprenne mieux les gros projets
```

AlinaCoder must first attempt to resolve these requests from project state and memory rather than immediately asking the user for technical clarification.

---

## 5. French is a first-class interaction language

French must be a native interaction target for v0.2.

The natural-language layer must tolerate:

- spelling mistakes;
- missing accents;
- imperfect grammar;
- incomplete sentences;
- shorthand;
- informal vocabulary;
- non-technical vocabulary;
- mixed French and English engineering terms;
- references such as `ça`, `le truc`, `comme avant`, `continue`, `l'autre fichier`, `ce qu'on faisait`;
- terminology that differs from the actual code symbol names;
- user misconceptions about implementation details.

The system must normalize meaning without requiring the user to rewrite the message into formal technical language.

Example:

```text
fait que ça bug plus quand je relance
```

may compile internally into a goal similar to:

```text
Eliminate the observed restart-time failure while preserving existing intended behavior and preventing regressions.
```

The user-facing interaction remains in the user's language unless the user requests otherwise.

---

## 6. Natural Language Intent Engine

Every conversational request passes through a dedicated intent-understanding layer before becoming implementation work.

Canonical flow:

```text
User Message
→ Normalize Language
→ Recover Active Context
→ Resolve References
→ Infer Intent
→ Identify Constraints
→ Estimate Confidence/Risk
→ Compile Mission
→ Autonomous Planning
→ Execute
```

The LLM must not receive the raw message as if it were a complete engineering specification and immediately start editing.

The intent layer constructs a structured representation.

Representative contract:

```text
UserIntent
- literal_request
- normalized_request
- inferred_goal
- target_project
- target_scope
- contextual_references
- explicit_constraints
- implied_constraints
- user_preferences_relevant_to_task
- acceptance_intent
- ambiguity_candidates
- assumptions
- confidence
- risk_if_misinterpreted
- evidence_sources
```

The original user message is always retained as provenance.

---

## 7. Context Fusion Engine

Intent cannot be inferred from the latest message alone.

The context fusion layer dynamically combines relevant evidence from:

1. current conversation;
2. active mission;
3. active milestone/task/step;
4. repository state;
5. Git HEAD and working tree;
6. current diff;
7. roadmap;
8. project documentation;
9. `ALINACODER.md` and project instructions;
10. Repository Intelligence Graph;
11. project architecture/contracts;
12. tests and most recent test results;
13. recent runtime errors;
14. current hypotheses and blockers;
15. episodic memory;
16. validated lessons;
17. project-history patterns;
18. relevant prior commits and decisions;
19. verification claims and their freshness;
20. last known unfinished work.

The fusion is selective and budgeted. It must not dump every memory or repository file into the model.

The goal is to provide the smallest evidence set sufficient to disambiguate the user's intent.

---

## 8. Reference Resolution

AlinaCoder must resolve conversational references against live project state.

Examples:

```text
continue
```

should first search for:

- an interrupted active mission;
- last non-DONE task;
- last explicit user objective;
- roadmap next action;
- last known blocker;
- pending verification/recovery work.

```text
ça marche toujours pas
```

should inspect:

- the immediately preceding attempted fix;
- last changed files;
- last reproduction command;
- recent failing output;
- active hypothesis;
- last commit or uncommitted candidate state.

```text
fais comme on avait décidé
```

should retrieve the relevant project decision and verify that it is still fresh before using it.

References are resolved with evidence pointers, not by guessing blindly.

---

## 9. Project Mental Model

The Repository Intelligence Graph describes structural relationships. The conversational layer additionally needs a **Project Mental Model** representing project intent and evolution.

The Project Mental Model links:

```text
requirements
↔ user objectives
↔ roadmap
↔ architecture
↔ components
↔ code
↔ tests
↔ decisions
↔ history
↔ failures
↔ lessons
↔ active work
```

It should answer questions such as:

- What is this project trying to become?
- Which architectural choices are deliberate?
- Which features are finished?
- What is currently incomplete?
- Which parts are fragile?
- What did the user previously reject?
- Which constraints must not regress?
- Which work is logically next?
- Which modules correspond to the user's non-technical terms?

The Project Mental Model is evidence-backed and incrementally updated. It is not a free-form personality profile.

---

## 10. Intent confidence and ambiguity policy

Ambiguity must not automatically produce a question.

Intent confidence is classified at least as:

- `HIGH` — context strongly identifies one intended objective;
- `MEDIUM` — one interpretation is materially more likely than alternatives;
- `LOW` — insufficient evidence, but autonomous evidence collection can reduce uncertainty;
- `AMBIGUOUS_HIGH_IMPACT` — multiple materially different interpretations remain and choosing incorrectly could cause significant unwanted change.

Required behavior:

### HIGH

Execute autonomously.

### MEDIUM

Proceed with the best-supported interpretation. Record assumptions and prefer reversible/minimal changes.

### LOW

Gather more project evidence autonomously before asking the user.

### AMBIGUOUS_HIGH_IMPACT

Ask one concise clarification only after repository/context investigation cannot resolve the ambiguity safely.

This policy preserves full autonomy while avoiding reckless interpretation.

---

## 11. Intent-to-Mission Compiler

A user intent is compiled into executable engineering state rather than passed downstream as raw prose.

Representative mission structure:

```text
Mission
- objective
- rationale
- acceptance intent
- constraints
- non-goals
- inferred scope
- confidence
- assumptions
- evidence anchors
- milestones
- tasks
- dependencies
- risk classification
- verification envelope
- Done Contracts
```

The mission compiler maps non-technical intent to technical work by inspecting the codebase rather than expecting the user to provide implementation instructions.

Example:

```text
User: améliore la mémoire, elle oublie trop de trucs
```

may become:

```text
Mission:
Improve durable project-memory recall and freshness without increasing stale-memory decisions.

Investigate:
- current memory schema
- retrieval ranking
- context condensation
- stale-record invalidation
- lesson reuse

Verification:
- memory recall fixture
- stale-memory fixture
- long-session resume fixture
- token/context budget
```

The exact technical mission is derived from the actual repository, not from this example.

---

## 12. Autoplanning from natural language

The user is not expected to provide a technical plan.

AlinaCoder autonomously decides:

- what to inspect;
- whether to reproduce first;
- which symbols are relevant;
- which dependencies matter;
- which architecture path is appropriate;
- which alternative designs should be compared;
- which code should change;
- which tests should be written or executed;
- which historical context is useful;
- when a plan must be revised;
- when the task is complete;
- when to commit and push to `main`.

Natural conversation is therefore an intent surface, not a reduction in engineering rigor.

---

## 13. Conversational continuity

Conversation state must survive long runs and restarts through structured state, not by storing unlimited raw dialogue.

Durable conversational context includes:

- active user objective;
- relevant user constraints;
- accepted/rejected decisions;
- unresolved references;
- active task;
- last meaningful result;
- last blocker;
- expected next action;
- links to project evidence.

Old conversational text may be condensed, but its decision-critical semantics must remain recoverable.

When the user returns after interruption and says:

```text
reprends
```

AlinaCoder should reconcile persisted conversational state with current Git/repository reality before resuming.

---

## 14. Natural response policy

AlinaCoder's conversational responses should be concise, natural and task-oriented.

The user should not be forced to read internal implementation ceremonies after every message.

Normal behavior:

1. briefly state what AlinaCoder understood when useful;
2. act autonomously;
3. surface meaningful progress or decisions;
4. report verification and actual result;
5. mention blockers only when they materially require attention.

The internal structured intent, hypothesis ledger, graph traversal and verification details remain available through verbose/debug modes and logs.

The system should not pretend to be certain when evidence is weak, but it should prefer investigation over unnecessary questioning.

---

## 15. Conversational acceptance scenarios

The v0.2 implementation must include automated fixtures demonstrating at least:

1. `continue` resumes the correct unfinished task from project state.
2. `fini ce qu'on faisait` selects the active incomplete mission rather than inventing a new task.
3. a misspelled French request maps to the correct technical objective.
4. a non-technical description of a bug localizes the correct subsystem through repository evidence.
5. `ça marche toujours pas` reconnects to the latest failed attempted fix and reproduction evidence.
6. `fais le plus simple` causes candidate designs to prefer the smallest robust equivalent solution.
7. `sans tout refaire` becomes a scope/minimal-change constraint.
8. `comme on avait décidé` retrieves a fresh prior project decision and rejects it if it has become stale/superseded.
9. a short ambiguous low-risk request proceeds with explicit internal assumptions without interrupting the user.
10. a genuinely high-impact unresolved ambiguity triggers one concise clarification instead of an unsafe guess.
11. mixed French/English technical vocabulary resolves correctly.
12. conversational state remains coherent after crash/resume.
13. the agent answers `où t'en es ?` using real run/task/Git/test state.
14. the user can complete a realistic feature/bug workflow without ever naming a source file or test command.

---

# Part II — External Self-Improvement Supervisor

## 16. Purpose

The existing v0.2 self-improvement design is extended with a separate **External Self-Improvement Supervisor**.

Its job is not to reduce autonomy. Its job is to make autonomous self-improvement measurable, reversible and resistant to self-deception.

The supervisor treats the currently promoted AlinaCoder version as a stable candidate baseline and evaluates proposed improvements from outside the normal task loop.

Canonical flow:

```text
Stable Version
→ Baseline Benchmark
→ Improvement Hypothesis
→ Isolated Candidate Copy
→ Candidate Modification
→ Candidate Tests
→ After Benchmark
→ Comparative Evaluation
→ PROMOTE or REJECT
→ Post-Promotion Watch
→ automatic ROLLBACK if later evidence proves regression
```

---

## 17. Separation of candidate and evaluator

A candidate self-improvement must not be allowed to redefine the success criteria that promote itself.

The external supervisor owns or integrity-checks:

- benchmark definitions;
- mandatory safety fixtures;
- regression fixtures;
- scoring rules;
- baseline results;
- evaluator configuration;
- promotion thresholds;
- benchmark artifact hashes.

Candidate code is evaluated against these external criteria.

If evaluator code itself is intentionally changed, that change is treated as a separate high-risk evaluator-upgrade mission and must pass a higher-order validation procedure.

---

## 18. Isolated candidate experimentation while keeping `main` only

The GitHub policy remains unchanged: no feature branches or PRs.

Self-improvement experiments run in a disposable local copy/scratch workspace.

The candidate may freely modify that isolated copy under the normal safety policy.

The canonical repository remains unchanged until promotion.

Only an accepted candidate is transferred into the canonical working tree, reverified, committed and pushed directly to `main`.

A rejected candidate leaves no GitHub development branch and no canonical code mutation.

---

## 19. Baseline-before-change requirement

Before an external self-improvement experiment, the supervisor records a fresh baseline under the same applicable environment/configuration.

Baseline evidence includes as relevant:

- mandatory unit tests;
- integration tests;
- safety fixtures;
- workspace-boundary fixtures;
- structured action adherence;
- repository localization accuracy;
- dependency/impact correctness;
- regression detection;
- planning fixtures;
- conversational intent fixtures;
- French-language understanding fixtures;
- memory recall/freshness fixtures;
- recovery/resume fixtures;
- deadlock recovery;
- autonomous task completion;
- latency;
- peak memory where practical;
- token/context consumption where measurable;
- tool-call count;
- unnecessary diff/dependency behavior;
- benchmark run stability.

Baseline artifacts and evaluator hashes are stored with the experiment.

---

## 20. Focused improvement hypothesis

Each self-improvement experiment begins with an explicit hypothesis.

Example structure:

```text
ImprovementHypothesis
- target capability
- observed weakness
- proposed mechanism
- metrics expected to improve
- metrics that must not regress
- affected modules
- expected risk
- rollback anchor
```

The system should prefer one focused improvement per experiment rather than uncontrolled simultaneous rewrites.

This makes causality and lessons easier to establish.

---

## 21. Before/after evaluation

The candidate is evaluated with the same benchmark protocol used for the baseline whenever possible.

The supervisor compares the candidate against the baseline using a priority-ordered score vector rather than one easily gamed scalar.

Normative priority order:

1. **Safety floors**
2. **Functional correctness / acceptance**
3. **Regression behavior**
4. **Reliability / recovery**
5. **Reasoning and localization quality**
6. **Intent/conversation quality**
7. **Efficiency and resource use**
8. **Complexity / maintainability cost**

A gain in a lower-priority dimension cannot compensate for violating a hard higher-priority floor.

Example: faster reasoning never compensates for new workspace escape behavior.

---

## 22. Promotion verdicts

The external supervisor supports at least:

### `PROMOTE`

Candidate demonstrably improves the intended capability or fixes a defined defect, all mandatory floors remain satisfied, no unacceptable regression appears, and evaluator integrity is intact.

### `REJECT`

Candidate is worse, inconclusive, unstable, overly complex relative to benefit, breaks mandatory floors, or fails to establish its claimed improvement.

The isolated candidate is discarded or retained only as non-canonical experiment evidence.

### `PROMOTE_WITH_WATCH`

Candidate passes promotion criteria but affects a broad/high-risk subsystem. It may be promoted with additional post-promotion verification checkpoints.

### `ROLLBACK`

A previously promoted candidate is found through expanded tests, real project use or later evaluation to be inferior to its verified predecessor on a mandatory dimension. The supervisor automatically restores the last `BestKnownVersion`, verifies it and republishes the corrective state to `main` when necessary.

---

## 23. Automatic rollback rule

Rollback must be autonomous.

User approval is not required when the system has deterministic evidence that its last self-improvement broke a mandatory invariant or produced a measured unacceptable regression and a previously verified good version is available.

Rollback sequence:

```text
Regression detected
→ freeze further promotion
→ capture evidence
→ identify last compatible BestKnownVersion
→ restore candidate-independent evaluator
→ restore code
→ run mandatory verification
→ commit corrective rollback on main
→ push main
→ record failed improvement lesson
→ resume from stable version
```

No force push is required. Rollback is performed through a normal corrective commit on `main` unless repository recovery semantics require otherwise.

---

## 24. BestKnownVersion ledger

Self-improvement maintains a durable version ledger.

Each promoted version stores:

```text
VersionRecord
- commit SHA
- parent version
- improvement hypothesis
- changed capabilities
- benchmark-before ID
- benchmark-after ID
- evaluator hashes
- safety result
- correctness result
- regression result
- reasoning result
- conversation result
- efficiency result
- promotion verdict
- post-promotion findings
- rollback relation if any
```

This provides a verifiable evolutionary history instead of vague memories that a previous version was "better".

---

## 25. Learning from self-improvement experiments

Every experiment becomes an episode, but only evidence-grounded conclusions become durable lessons.

Useful lesson shape:

```text
SelfImprovementLesson
- target weakness
- attempted mechanism
- benchmark delta
- unexpected side effects
- causal confidence
- applicability scope
- avoid/reuse guidance
- supporting experiment IDs
```

Rejected experiments are valuable negative evidence.

AlinaCoder should avoid retrying substantially equivalent failed improvement strategies unless:

- project/model/environment conditions changed;
- new evidence invalidates the prior lesson;
- the new design materially differs from the failed approach.

---

## 26. Anti-gaming safeguards

The supervisor must explicitly defend against self-improvement reward gaming.

At minimum:

- evaluator files/config are hashed before candidate evaluation;
- candidate modifications to evaluator-controlled paths cause evaluation invalidation unless explicitly authorized as an evaluator-upgrade experiment;
- tests cannot be deleted/relaxed simply to increase score;
- expected outputs cannot be hardcoded from benchmark cases;
- benchmark fixtures are separated from normal candidate context where practical;
- metric calculation is deterministic where possible;
- unexpected benchmark coverage loss is treated as regression, not improvement;
- candidate complexity is considered when gains are marginal.

A candidate that improves measured scores by weakening evidence is rejected.

---

## 27. External improvement scheduling

External self-improvement may be triggered autonomously when there is evidence of a meaningful weakness, including:

- repeated failure pattern;
- benchmark weakness;
- excessive context/tool cost;
- recurring localization failure;
- repeated user correction of misunderstood intent;
- regression-detection miss;
- memory-staleness failure;
- recovery deadlock;
- newly available compatible Ollama model capability;
- validated project lesson suggesting a better mechanism.

It must not continuously rewrite itself merely because idle time exists.

Self-improvement requires a testable hypothesis and measurable target.

---

## 28. External self-improvement acceptance scenarios

The v0.2 test suite must include at least:

1. candidate improves localization with no regression → promoted.
2. candidate improves target score but weakens safety fixture → rejected.
3. candidate is faster but breaks an impacted regression test → rejected.
4. candidate produces no statistically/operationally meaningful improvement and adds complexity → rejected.
5. candidate changes evaluator file unexpectedly → experiment invalidated.
6. candidate passes short evaluation but fails extended post-promotion gate → automatic corrective rollback.
7. rollback restores last verified behavior and records the failed experiment.
8. rejected self-improvement does not create a GitHub branch.
9. accepted self-improvement is reverified and pushed only to `main`.
10. historical failed improvement is retrieved when an equivalent new strategy is proposed.
11. conversation-quality improvement is benchmarked against French short/imperfect requests.
12. a conversational improvement that increases intent success but causes unsafe high-impact guesses is rejected.

---

# Part III — Integration Rules

## 29. Updated cognitive entry loop

For conversational work, the canonical v0.2 loop becomes:

```text
Listen
→ Resolve Context
→ Infer Intent
→ Compile Mission
→ Reconcile Repository
→ Understand
→ Localize
→ Hypothesize
→ Plan
→ Compare
→ Act
→ Reproduce/Verify
→ Impact/Regression
→ Critique
→ Commit/Push main
→ Learn
→ Continue Conversation
```

The existing risk-adaptive shortened path remains valid for obvious low-risk work.

---

## 30. Full autonomy remains non-negotiable

Neither conversational intelligence nor external self-improvement introduces routine confirmation gates.

AlinaCoder remains responsible for making technical choices autonomously.

The user is not expected to approve:

- ordinary plans;
- file selection;
- test selection;
- implementation detail;
- normal bug-fix hypotheses;
- dependency traversal;
- commits that meet autonomous Done Contracts;
- rollback from a deterministically worse self-improvement to a previously verified stable version.

Human clarification is reserved for genuinely unresolved intent ambiguity with material consequences, policy constraints, unavailable credentials/permissions, or decisions whose answer cannot be inferred safely from project evidence.

---

## 31. Updated Done Contract requirements

In addition to the existing v0.2 Done Contract, conversationally initiated work requires:

1. final implementation must map back to the inferred user intent;
2. material inferred constraints must be preserved;
3. unresolved intent assumptions with high impact must be cleared before publication;
4. verification must prove the implemented behavior, not merely the internally compiled technical task;
5. final response must describe the actual user-level result in natural language.

Self-improvement work additionally requires:

1. fresh benchmark-before evidence;
2. candidate-isolated evaluation;
3. fresh benchmark-after evidence;
4. mandatory-floor comparison;
5. evaluator-integrity verification;
6. explicit promotion verdict;
7. a rollback anchor;
8. version-ledger update;
9. post-promotion watch when required.

---

## 32. Updated observability events

Add at least:

```text
conversation.message.received
intent.inferred
intent.reference_resolved
intent.assumption.recorded
intent.ambiguity_detected
mission.compiled
conversation.context.condensed
project_model.updated
self_improvement.baseline.started
self_improvement.baseline.completed
self_improvement.candidate.created
self_improvement.candidate.evaluated
self_improvement.promoted
self_improvement.rejected
self_improvement.watch.failed
self_improvement.rollback.started
self_improvement.rollback.completed
self_improvement.lesson.promoted
```

Normal conversational output remains concise. These events are primarily for logs, debugging and auditability.

---

## 33. Updated engineering metrics

Add metrics for conversational quality:

- intent resolution accuracy;
- short-request task success;
- French noisy-input success;
- reference-resolution accuracy;
- unnecessary clarification rate;
- incorrect autonomous interpretation rate;
- high-impact ambiguity catch rate;
- user correction frequency;
- mission compilation correctness;
- resumed-context correctness.

Add metrics for self-improvement quality:

- self-improvement acceptance rate;
- post-promotion rollback rate;
- benchmark delta by capability;
- safety-floor rejection count;
- regression-floor rejection count;
- evaluator-integrity violations;
- repeated failed-strategy avoidance;
- complexity delta per accepted improvement;
- retained improvement after extended validation.

Metrics are diagnostic evidence, not standalone optimization targets.

---

## 34. Explicit new anti-patterns

AlinaCoder v0.2 must additionally avoid:

1. treating every short message as under-specified;
2. asking the user which file to edit when repository evidence can answer it;
3. requiring technical terminology from the user;
4. trusting only the most recent chat message while ignoring active project state;
5. interpreting `continue` without reconciling Git/task state;
6. silently inventing a high-impact intent when multiple interpretations remain plausible;
7. storing unlimited raw chat history instead of structured conversational state;
8. converting user wording errors into technical constraints without evidence;
9. overexplaining internal architecture during normal conversation;
10. optimizing conversation naturalness at the expense of engineering verification;
11. letting a self-modifying candidate change its own promotion benchmark unnoticed;
12. accepting a self-improvement because one metric increased while a mandatory floor decreased;
13. keeping a worse promoted version merely because it already reached `main`;
14. using GitHub feature branches for self-improvement experiments;
15. repeatedly self-modifying without a measurable weakness or hypothesis.

---

## 35. Implementation priority update

The v0.2 implementation sequence should be updated so these capabilities are not bolted on at the end.

Recommended integrated sequence:

1. typed domain state + risk model;
2. deterministic patch tool and drift guard;
3. conversation session + structured `UserIntent`;
4. context fusion and reference resolution;
5. `Intent → Mission` compiler;
6. repository symbol/index foundation;
7. typed RIG + query API;
8. test impact / baseline / regression vertical slice;
9. plan-memory coupling;
10. hypothesis ledger + reproduction classes;
11. evidence packets + active context management;
12. natural French/noisy-input fixtures;
13. critic + alternative design gate;
14. history intelligence + Project Mental Model;
15. validated lessons + conversational continuity;
16. best-known-state recovery / deadlock detection;
17. interface/invariant verification;
18. Ollama capability probes;
19. locked external self-improvement benchmark harness;
20. isolated self-improvement supervisor + before/after evaluator;
21. BestKnownVersion promotion/rollback system;
22. repository-scale and conversation-scale E2E acceptance suite.

This remains sequencing guidance. Detailed implementation work should later be decomposed into TDD-sized steps.

---

## 36. Final amended design contract

AlinaCoder v0.2 is a **fully autonomous, single-Ollama-model coding agent whose primary human interface is natural conversation**.

The user should be able to explain a need simply in French without translating it into software-engineering instructions. AlinaCoder reconstructs the intended mission from conversation, repository state, architecture, roadmap, memory, history, tests and prior decisions, then autonomously chooses and verifies the implementation.

Its conversational intelligence is not a chatbot layer placed on top of a rigid CLI. Conversation is an intent interface connected directly to the same evidence-grounded planning, repository reasoning, debugging and verification system that performs the engineering work.

Its self-improvement is equally autonomous but externally disciplined. Candidate changes are tested outside the canonical runtime against an integrity-protected benchmark, compared with a fresh baseline, promoted only when they are genuinely better under mandatory safety/correctness/regression floors, and rolled back automatically if later evidence proves them worse.

The target behavior is therefore:

> **Speak naturally → understand deeply → infer intelligently → plan autonomously → change minimally → verify rigorously → publish directly to `main` → learn from evidence → improve itself only when measurable improvement is real.**

This amendment preserves the original v0.2 principle: maximize useful autonomy per unit of complexity, while making that autonomy substantially more natural to direct and substantially safer to evolve.