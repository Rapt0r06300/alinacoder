# AlinaCoder v0.2 — Cognitive Intelligence & Natural Interaction Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Normative status

This amendment explicitly **reopens and extends AlinaCoder v0.2** after the previous freeze, following direct user approval.

It is normative for implementation together with:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`

Where this amendment adds stricter or more capable behavior, this amendment wins for the affected subsystem.

All prior non-negotiable invariants remain unchanged unless explicitly strengthened here:

- full autonomy remains enabled;
- Windows-first remains the supported OS target;
- Python 3.12+ remains the implementation language;
- Ollama remains the local model provider;
- deterministic safety/verification continues to outrank model claims;
- canonical Git development remains direct to `main`;
- no autonomous feature-branch/PR workflow is introduced;
- local-first remains the default architecture;
- no mandatory Supabase dependency is introduced;
- reliability, testability and reversibility outrank ambition.

The purpose of this amendment is to make AlinaCoder substantially better at:

- understanding ordinary human French without requiring technical phrasing;
- preserving user intent through ambiguity, disfluency and correction;
- maintaining deep project context over long sessions;
- remembering not just facts, but why decisions were made and which attempts failed;
- reasoning under uncertainty;
- choosing when to ask, infer, research, deliberate, debate or abstain;
- learning from mismatches between prediction and reality;
- avoiding repeated mistakes and cognitive drift;
- measuring understanding itself through hidden metamorphic tests.

---

# Part I — Natural Intent Understanding

## 2. Intent Beam

AlinaCoder must not collapse ambiguous language into a single interpretation too early.

For underspecified requests, maintain a bounded set of ranked candidate intents:

```text
IntentCandidate
- candidate_id
- interpreted_goal
- project_candidate
- object/referent candidate
- constraints
- supporting evidence
- contradicting evidence
- confidence
- risk_if_wrong
- status
```

Typical status values:

```text
ACTIVE
WEAKENED
REJECTED
SELECTED
```

Examples:

```text
"continue"
→ candidate A: resume current active mission
→ candidate B: resume most recent interrupted roadmap task
→ candidate C: resume recently blocked bug investigation
```

Candidate intents must be updated as new evidence arrives from:

- recent conversation;
- active mission;
- project memory;
- Git state;
- roadmap;
- current files;
- test failures;
- latest user corrections.

Selection rule:

```text
choose one interpretation only when evidence separation is sufficient
OR when one candidate has clearly lower risk than alternatives
```

If ambiguity remains material and high-impact, use the Ask-or-Infer Controller defined later.

### Acceptance scenarios

- `continue` resumes the correct unfinished task among multiple recent projects.
- a vague pronoun such as `ça` resolves to the correct object when project evidence is sufficient.
- a wrong early hypothesis is discarded after a later user correction.

---

## 3. Persistent Intent Contract

Once the intent is sufficiently resolved, AlinaCoder must compile a persistent `IntentContract`.

Required fields:

```text
IntentContract
- literal_request
- inferred_goal
- active_project
- constraints
- forbidden_actions
- preservation_requirements
- success_definition
- non_goals
- assumptions
- unresolved_questions
- evidence_sources
- confidence
- last_revalidated_at
```

The contract is not static. It can be revised when the user changes their mind or stronger evidence appears.

Mandatory revalidation points:

- before finalizing a plan;
- before a high-impact edit;
- before broad scope expansion;
- before commit;
- before push;
- after a material user correction;
- after a recovery/resume event.

AlinaCoder must detect `IntentDrift` when work remains technically coherent but no longer matches the active contract.

### Normative rule

A technically correct patch that violates the user's active intent is not `DONE`.

---

## 4. Conversation Repair Graph

Noisy spoken or typed French must preserve repair structure instead of being flattened into one rewritten sentence.

Represent corrections explicitly:

```text
REPLACE
CANCEL
NARROW
EXTEND
REORDER
NEGATE
CONFIRM
```

Example:

```text
"améliore la mémoire... euh non attends, surtout le contexte, mais garde la mémoire"
```

must become approximately:

```text
initial_goal: improve memory
repair: NARROW priority toward context
preserve: memory improvement remains allowed
final_priority: context > memory
```

The repair graph must track which earlier fragments were superseded rather than merely deleting them.

This prevents stale intent from surviving after phrases such as:

- `non attends`;
- `plutôt`;
- `je me suis mal expliqué`;
- `en fait`;
- `oublie ça`;
- `garde ça mais...`;
- `pas comme ça`;
- `je change d'avis`.

---

## 5. Dual speech representation: RAW + MEANING

For speech/transcription input, maintain two distinct representations.

### RAW

Immutable or append-only representation containing:

- original ASR text;
- timing where available;
- pauses;
- repeated fragments;
- fillers;
- false starts;
- revisions;
- speaker turns;
- confidence metadata when available.

### MEANING

Structured semantic interpretation containing:

- current intent;
- active entities;
- corrected values;
- constraints;
- negations;
- unresolved ambiguities;
- conversational repair links.

The system must never destroy RAW evidence merely because a normalized interpretation exists.

If MEANING later appears inconsistent, AlinaCoder may re-interpret RAW.

### Safety invariant

Normalization must not silently delete nouns, constraints, negations or changed values merely to produce smoother language.

---

## 6. Semantic Turn Manager

Voice interaction must distinguish acoustic silence from semantic completion.

Required turn states:

```text
LISTENING
SEMANTICALLY_INCOMPLETE
PAUSED
BACKCHANNEL
COMPLETE
REVISING
INTERRUPTED
```

Rules:

- silence alone is not sufficient to declare `COMPLETE`;
- a phrase like `je voudrais que tu...` followed by a pause should normally remain incomplete;
- backchannels such as `oui`, `hm`, `vas-y` must not always become new missions;
- phrases such as `attends`, `non`, `en fait` can reopen a nearly completed turn;
- important irreversible actions require a stable semantic turn boundary.

AlinaCoder may perform safe background context preparation while the user is speaking, but must not finalize high-impact actions from unstable partial intent.

---

## 7. Ask-or-Infer Controller using Value of Information

AlinaCoder must not use a simplistic fixed confidence threshold to decide whether to ask the user.

For each ambiguity, estimate:

```text
expected_decision_change
× consequence_if_wrong
× probability_user_has_unique_missing_info
```

Then choose among:

```text
INFER_AND_CONTINUE
SEARCH_LOCAL_CONTEXT
SEARCH_PROJECT_HISTORY
SEARCH_EXTERNAL_EVIDENCE
DECOMPOSE
ASK_USER
```

Default priority:

```text
resolve autonomously first
→ ask only if missing information is both inaccessible and decision-relevant
```

Examples:

- missing symbol name: inspect repository first;
- unclear `continue`: inspect mission/history first;
- unclear architectural preference with two equally risky incompatible choices: ask if no prior decision exists;
- noncritical naming ambiguity: infer conservatively and continue.

This controller preserves full autonomy by minimizing unnecessary clarification while avoiding dangerous guessing.

---

# Part II — Context and Memory Intelligence

## 8. Context Operating System

Context management becomes a first-class tool surface.

Required operations:

```text
PIN
UNPIN
RECALL
FOLD
SUMMARIZE
DROP
REFRESH
REHYDRATE
```

Context classes:

```text
IMMUTABLE_ANCHOR
ACTIVE_WORKING_SET
RECENT_HIGH_FIDELITY
CONDENSED_HISTORY
ON_DEMAND_MEMORY
EXTERNAL_EVIDENCE
```

Typical immutable anchors include:

- active IntentContract;
- non-negotiable project invariants;
- task Done Contract;
- reproduced bug signature;
- selected baseline/checkpoint.

The agent must proactively manage context at milestones instead of waiting for token exhaustion.

Context pressure must trigger selective condensation, not blind truncation.

---

## 9. Reasoning Digests + Recent Cognitive Window

AlinaCoder must preserve high-fidelity recent reasoning while compacting older state into structured digests.

A `ReasoningDigest` contains:

```text
- established facts
- disproven hypotheses
- unresolved hypotheses
- decisions and rationale
- latest verification evidence
- regression status
- next discriminating experiment
- open risks
```

The recent cognitive window retains detailed short-horizon continuity.

Older raw reasoning is not treated as always-needed prompt context.

The goal is to avoid:

- context explosion;
- repeated re-derivation;
- semantic drift;
- loss of early constraints;
- long-session degradation.

---

## 10. Memory-as-Governance pre-action gate

Memory must actively influence actions before they occur.

Add deterministic or semi-deterministic checks such as:

```text
precheck_file(path)
precheck_strategy(strategy_signature)
precheck_architecture(decision_signature)
precheck_dependency(package)
precheck_migration(target)
```

The gate should surface:

- previously failed attempts on the same area;
- known-fragile files/components;
- superseded architectural choices;
- negative lessons;
- high-churn zones;
- historical regression patterns;
- relevant invariants.

Possible outputs:

```text
CLEAR
WARN
REQUIRE_REEVALUATION
BLOCK_AS_REPEATED_PROVEN_FAILURE
```

A past failure is not an eternal ban: applicability, freshness and changed conditions must be checked.

---

## 11. Ontology-grounded memory with negation and supersession

Extend memory beyond isolated records into typed relationships.

Required relation examples:

```text
SUPERSEDES
CONTRADICTS
REQUIRES
FORBIDS
DEPENDS_ON
APPLIES_TO
INVALIDATED_BY
DERIVED_FROM
RESOLVED_BY
FAILED_BECAUSE
```

Examples:

```text
Decision B SUPERSEDES Decision A
Invariant X FORBIDS Strategy Y
Lesson L APPLIES_TO package/api version range Z
Fact F INVALIDATED_BY commit SHA C
```

Queries must support not only similarity but logical distinctions such as:

- what is the latest valid decision?;
- which previous decisions are superseded?;
- what strategies are explicitly forbidden?;
- what is known not to work under current conditions?;
- which constraints depend on an artifact that changed?

---

## 12. Four-way Hybrid Memory Retrieval

Memory retrieval should combine multiple retrieval modes:

1. exact lexical / identifier matching;
2. symbolic/graph traversal;
3. semantic similarity;
4. temporal/contextual relevance.

Results should be fused using a deterministic rank-fusion method where practical.

No single retrieval method is authoritative.

Examples:

- exact error string should strongly favor lexical match;
- vague phrase such as `le bug de reprise` may need semantic + temporal retrieval;
- architectural decision questions should prefer symbolic supersession edges;
- current task references should weigh recency and mission membership.

### Local-first requirement

The implementation must remain local-first. Supabase is not a mandatory runtime dependency.

A valid local implementation may use:

- SQLite/FTS;
- local metadata indexes;
- AST/symbol indexes;
- local embeddings generated with an approved local model;
- deterministic reciprocal/rank fusion.

External services may be optional integrations only.

---

## 13. Freshness propagation to semantic indexes

Freshness must propagate through all derived memory artifacts.

If a supporting artifact changes, affected derived objects become:

```text
STALE_PENDING_REFRESH
STALE
UNPROVABLE
SUPERSEDED
```

This applies to:

- memory records;
- summaries;
- embeddings;
- repository graph edges;
- verification claims;
- experience cards;
- architectural conclusions.

Examples:

```text
source file SHA changed
→ symbol summary stale
→ embedding stale
→ derived lesson applicability rechecked
```

Stale semantic artifacts must not silently outrank fresh repository evidence.

---

## 14. AST-guided Code Memory + Forgetting Detector

Add a code-centric memory keyed to real structural entities.

Track over time:

- symbol signatures;
- contracts/invariants;
- caller/callee relationships;
- associated tests;
- public API behavior;
- previously corrected defects;
- user-required behavior attached to symbols.

After meaningful edits, compare the candidate state against validated structural memory.

Detect possible forgetting such as:

- reintroducing previously removed logic;
- restoring a deprecated parameter;
- dropping an invariant;
- recreating a previously fixed edge case;
- contradicting a later project decision.

Potential finding classes:

```text
POSSIBLE_FORGETTING
REINTRODUCED_PATTERN
CONTRACT_LOSS
HISTORY_CONFLICT
```

These findings require verification before promotion.

---

## 15. Internal and external Experience Cards

Validated experience should be normalized into reusable cards.

Required schema:

```text
ExperienceCard
- symptom
- context
- environment/version
- root_cause
- failed_approaches
- winning_strategy
- files/symbols
- verification_method
- regression_risks
- applicability
- provenance
- freshness
```

Sources may include:

### Internal

- successful AlinaCoder runs;
- user-validated fixes;
- historical commits;
- prior failed investigations.

### External

- official issue trackers;
- maintainer discussions;
- merged PRs;
- high-quality bug reports;
- primary documentation.

External cards must capture the repair logic rather than blindly copying patches.

Cards from unrelated codebases are advisory only until validated against the current repository.

---

# Part III — Reasoning, Uncertainty and Scientific Debugging

## 16. Uncertainty Control Plane

Uncertainty becomes an actionable control signal, not only a final confidence score.

Required uncertainty reason classes include:

```text
MISSING_CONTEXT
UNCERTAIN_REFERENCE
UNCERTAIN_API
CONFLICTING_EVIDENCE
WEAK_MODEL
UNTESTED_ASSUMPTION
DEPENDENCY_UNKNOWN
REPRODUCTION_MISSING
REGRESSION_RISK
STALE_MEMORY
TOOL_RESULT_UNRELIABLE
MULTI_AGENT_DISAGREEMENT
```

Each reason maps to preferred intervention classes.

Examples:

```text
UNCERTAIN_API → external research / inspect installed version
DEPENDENCY_UNKNOWN → graph expansion / runtime trace
REPRODUCTION_MISSING → construct reproduction before patch
WEAK_MODEL → decompose / strengthen deterministic evidence
STALE_MEMORY → refresh source before use
```

Track uncertainty at:

- intent level;
- planning level;
- hypothesis level;
- tool result level;
- specialist handoff level;
- final verification level.

The objective is to stop uncertainty from silently propagating into irreversible decisions.

---

## 17. Cognitive Mode Router

Reasoning depth must be task-adaptive.

Required modes:

```text
REFLEX
DELIBERATE
DEBUG
RESEARCH
VERIFY
ARCHITECT
RECOVERY
```

Examples:

- deterministic file listing: `REFLEX`;
- public API redesign: `ARCHITECT`;
- unexplained failing test: `DEBUG`;
- dependency version uncertainty: `RESEARCH`;
- pre-push regression sweep: `VERIFY`.

Escalation signals include:

- rising uncertainty;
- critic disagreement;
- broadened dependency impact;
- repeated failure;
- weak model capability;
- high-risk scope.

Deep reasoning is therefore concentrated where it provides decision value rather than applied indiscriminately.

---

## 18. Prediction-before-Action learning

Before important actions, record an explicit prediction.

Example:

```text
Prediction
- expected test delta
- expected files touched
- expected behavior change
- expected error disappearance
- expected unaffected invariants
- confidence
```

After execution, compute `PredictionRealityDelta`.

Mismatch classes may include:

```text
EXPECTED_PASS_BUT_FAILED
UNEXPECTED_FILE_IMPACT
UNEXPECTED_REGRESSION
ERROR_SIGNATURE_CHANGED
NO_EXPECTED_EFFECT
SURPRISE_SIDE_EFFECT
```

Repeated mismatch patterns become calibration signals.

Examples:

- if AlinaCoder repeatedly underestimates a subsystem's impact radius, future tasks in that subsystem automatically expand impact analysis;
- if a model repeatedly predicts false test outcomes for a task class, lower its capability score for that class.

Prediction mismatch is evidence for learning; it is not automatically blame assigned to the model.

---

## 19. Causal debugging through discriminating experiments

When multiple hypotheses remain, choose experiments that best discriminate between them rather than applying multiple speculative fixes.

Each hypothesis should support:

```text
- expected observation if true
- expected observation if false
- cheapest discriminating probe
- risk of probe
- information gain estimate
```

Possible probes:

- targeted temporary assertion;
- focused unit test;
- runtime trace;
- controlled input perturbation;
- feature flag;
- dependency version check;
- Git bisect or historical comparison;
- mock/stub isolation;
- minimal reproduction.

Preferred probe:

```text
maximize expected uncertainty reduction
subject to safety/resource constraints
```

This makes debugging closer to evidence-driven experimentation and reduces random patching.

---

# Part IV — Adaptive Multi-Agent Intelligence

## 20. Adaptive Specialist Council

The existing conditional specialist system is strengthened into a temporary `SpecialistCouncil`.

It remains disabled by default unless expected value is positive.

Possible roles:

```text
Researcher
Repository Architect
Debugger
Regression Reviewer
Security Critic
Alternative Designer
Intent Resolver
Test Strategist
```

Council requirements:

1. specialists receive partially separated context when diversity is useful;
2. each specialist returns evidence, uncertainty and assumptions, not merely a conclusion;
3. handoffs are typed and checked;
4. agreement is not treated as proof;
5. suspiciously rapid consensus may trigger a diversity check;
6. deterministic tests and tools remain authoritative.

### Handoff failure taxonomy

At every important specialist handoff, detect:

```text
DATA_GAP
SIGNAL_CORRUPTION
REFERENTIAL_DRIFT
CAPABILITY_GAP
UNSUPPORTED_CONCLUSION
```

A clarifier or additional evidence step should be inserted when a handoff is unreliable.

---

## 21. Selective debate with confidence and diversity

Multi-agent debate must never be triggered automatically for every difficult task.

Debate trigger should consider:

- uncertainty;
- disagreement between independent candidate solutions;
- recoverability of likely error;
- task risk;
- expected information gain;
- compute/resource budget;
- historical value of debate for this task class.

Debate pool creation should favor **diverse independent hypotheses**, not duplicated prompts producing the same anchored answer.

Each contribution must communicate:

```text
claim
evidence
counter-evidence
confidence/uncertainty
assumptions
```

Aggregation must down-weight unsupported confidence.

If debate historically worsens a task class on hidden benchmarks, disable it for that class until new evidence supports reactivation.

---

# Part V — Evaluation of Understanding

## 22. Metamorphic Intelligence Benchmark

Understanding itself becomes a first-class hidden evaluation target.

For each canonical user intent, generate semantically equivalent variants such as:

- clean French;
- spelling mistakes;
- abbreviated French;
- informal French;
- missing punctuation;
- ASR-like substitutions;
- repetitions;
- hesitations;
- false starts;
- self-correction;
- pronouns/references;
- reordered clauses;
- code-switching with English technical terms;
- interrupted continuation;
- project switch and switch-back.

Equivalent variants must preserve the same essential `IntentContract`.

Conversely, minimal but important semantic changes must produce a materially different contract.

Examples:

```text
"ne supprime pas X"
!=
"supprime X"
```

and:

```text
"continue"
```

should resolve differently depending on the controlled project/history fixture.

### Hidden evaluation families

The metamorphic suite must include:

1. intent equivalence;
2. negation sensitivity;
3. correction precedence;
4. project disambiguation;
5. stale-memory rejection;
6. context distractors;
7. ASR/noisy French robustness;
8. cross-session continuity;
9. Ask-or-Infer quality;
10. appropriate abstention;
11. debate trigger quality;
12. intent-drift prevention.

Cases, mutation rules and expected normalized intents remain hidden from self-improving candidates.

---

# Part VI — Integration with Existing v0.2

## 23. Updated cognitive loop

The canonical cognitive loop is strengthened to:

```text
Receive / Stream
→ Maintain RAW input
→ Update Conversation Repair Graph
→ Build Intent Beam
→ Fuse Project Context
→ Estimate Uncertainty
→ Ask / Infer / Retrieve / Research decision
→ Select Intent
→ Compile / Revalidate Intent Contract
→ Select Cognitive Mode
→ Retrieve Governed Memory
→ Localize Repository Context
→ Hypothesize
→ Choose Discriminating Experiments
→ Plan
→ Compare Alternatives
→ Trigger Specialists/Debate only if valuable
→ Predict Expected Effects
→ Safety / Resource / Capability Gate
→ Act
→ Observe Reality
→ Compute Prediction-Reality Delta
→ Verify / Regression Analysis
→ Forgetting Detector
→ Critic Review
→ Reliability Assessment
→ Commit / Push to main
→ Build Experience Card / Lessons
→ Context Fold / Memory Refresh
→ Next
```

This extends but does not remove previous v0.2 verification, safety, resource, model calibration, rollback or Git gates.

---

## 24. Proposed source architecture extensions

Conceptual additions:

```text
src/alinacoder/
├─ conversation/
│  ├─ intent_beam.py
│  ├─ repair_graph.py
│  ├─ turn_manager.py
│  ├─ raw_stream.py
│  └─ ask_or_infer.py
├─ context/
│  ├─ context_os.py
│  ├─ reasoning_digest.py
│  └─ anchors.py
├─ memory/
│  ├─ governance.py
│  ├─ ontology.py
│  ├─ hybrid_retrieval.py
│  ├─ freshness.py
│  ├─ code_memory.py
│  └─ experience_cards.py
├─ intelligence/
│  ├─ uncertainty_control.py
│  ├─ cognitive_mode.py
│  ├─ prediction.py
│  ├─ causal_probe.py
│  └─ council.py
└─ evaluation/
   ├─ metamorphic_intent.py
   ├─ noisy_french.py
   ├─ hidden_mutations.py
   └─ intent_drift.py
```

Exact module names may change during implementation, but these responsibilities are normative.

---

## 25. Data-model additions

Important new durable entities include:

```text
IntentCandidate
IntentContract
ConversationRepair
RawUtterance
SemanticTurn
ReasoningDigest
MemoryRelation
CodeMemoryRecord
ExperienceCard
UncertaintySignal
Prediction
PredictionRealityDelta
SpecialistHandoff
MetamorphicEvalResult
```

All durable objects should include provenance and timestamps where meaningful.

Project-scoped objects must include project identity and repository state references.

---

## 26. New reliability rules

The following become mandatory:

1. No high-impact action from an unresolved unstable speech fragment.
2. No single ambiguous interpretation may silently override a plausible lower-risk alternative without evidence.
3. User corrections supersede stale inferred intent.
4. IntentContract must be revalidated before commit/push.
5. Context truncation must not remove immutable anchors.
6. Stale memory/embeddings cannot outrank fresh repository state.
7. Previously failed strategies must trigger governance review before repetition.
8. Uncertainty must have a reason when it affects a major decision.
9. High uncertainty must trigger targeted intervention, not blind reflection loops.
10. Multi-agent consensus is not proof.
11. Multi-agent use must remain conditional and benchmarked.
12. Prediction-reality mismatch must be recorded for significant actions.
13. Metamorphic intent tests are mandatory for conversation-quality self-improvement.
14. No local-first requirement is weakened by optional retrieval integrations.
15. No new mechanism may bypass existing Done Contracts, rollback or resource control.

---

# Part VII — New Acceptance Scenarios

## 27. Mandatory conversation intelligence scenarios

Implementation must prove at least:

1. `continue` resolves the correct active task from three plausible recent projects.
2. `corrige ça` resolves the intended failing component from current error + conversation.
3. a later `non attends` revision supersedes the earlier spoken goal.
4. a pause does not finalize an obviously incomplete sentence.
5. an ASR-like typo in a project/symbol name is resolved from repository context.
6. a negative constraint such as `ne touche pas à X` survives normalization and planning.
7. `comme on avait décidé` retrieves the latest non-superseded project decision.
8. ambiguity is resolved locally without asking when Git/roadmap evidence is sufficient.
9. a question is asked when two high-impact interpretations remain equally supported and unavailable evidence cannot resolve them.

---

## 28. Mandatory memory/context scenarios

10. a known failed strategy produces a governance warning before re-execution.
11. a superseded decision is not retrieved as the current architectural choice.
12. a stale embedding/summary is invalidated after source SHA changes.
13. AST-guided memory detects reintroduction of a previously removed defect pattern.
14. long sessions preserve IntentContract and open hypotheses after context folding.
15. exact symbol retrieval and semantic retrieval produce a fused result without similarity-only dependence.
16. an experience card improves localization while its patch is not blindly copied.

---

## 29. Mandatory reasoning scenarios

17. uncertainty reason `DEPENDENCY_UNKNOWN` causes dependency analysis instead of arbitrary patching.
18. a task escalates from `REFLEX` to `DELIBERATE` after broader impact is discovered.
19. two competing bug hypotheses are separated by a discriminating experiment before editing.
20. an action's expected test result differs from reality and creates a `PredictionRealityDelta`.
21. repeated underestimation of one subsystem increases future verification scope.
22. a specialist council is not launched when expected gain is lower than resource/coordination cost.
23. a council is launched when independent evidence indicates recoverable disagreement.
24. a specialist handoff with referential drift is intercepted before execution.

---

## 30. Mandatory metamorphic hidden scenarios

25. ten paraphrases of the same French intent yield equivalent normalized contracts.
26. spelling errors and informal syntax do not materially change the intended goal.
27. repetition does not duplicate requested work.
28. false starts followed by corrections preserve only the final active instruction plus explicitly preserved constraints.
29. `ne supprime pas` and `supprime` are never conflated.
30. project-context distractors do not override stronger active-task evidence.
31. a hidden user-intent mutation that materially changes scope produces a changed mission plan.
32. a self-improving candidate that optimizes public conversation fixtures but regresses hidden variants is rejected.

---

# Part VIII — Self-Improvement Extensions

## 31. Cognitive self-improvement scorecard

The external self-improvement supervisor must extend evaluation with:

```text
Intent Resolution Accuracy
Intent Drift Rate
Ask-or-Infer Utility
Negation Preservation
Repair/Correction Accuracy
Project Context Resolution
Long-Horizon Context Retention
Memory Governance Benefit
Stale-Memory Error Rate
Prediction Calibration
Causal Debug Efficiency
Specialist Trigger Precision
Specialist Trigger Recall
Metamorphic Robustness
```

No improvement may be promoted based only on fluent conversational output.

Correctness of inferred intent is more important than natural-sounding wording.

---

## 32. Anti-overfitting extension

The hidden evaluator should mutate:

- wording;
- error patterns;
- project names;
- task ordering;
- speech disfluency placement;
- distractor placement;
- historical memory structure;
- repository shape;
- dependency depth.

The candidate must not receive:

- hidden mutation templates;
- hidden expected IntentContracts;
- hidden project-disambiguation rules;
- hidden benchmark instance identifiers.

Repeated evaluation uses rotating canary tasks to detect specialization to static fixtures.

---

# Part IX — Design Principles

## 33. User-facing interaction principle

The user should be able to speak to AlinaCoder naturally, for example:

```text
"continue"
"ça marche toujours pas"
"fais le plus simple"
"reprends ce qu'on avait fait hier"
"non attends, garde ça mais change l'autre partie"
"je veux que ça arrête de planter quand je relance"
"améliore le projet mais casse rien"
```

The system is responsible for translating ordinary language into technical work.

The user is not required to know:

- file names;
- architecture;
- exact commands;
- test framework;
- dependency graph;
- root cause;
- implementation strategy.

AlinaCoder must infer, investigate, plan and verify those details autonomously.

---

## 34. Simplicity principle

These additions must not become an excuse for uncontrolled architectural complexity.

For each subsystem, prefer:

```text
simple deterministic mechanism
> complex learned controller
```

when measured quality is equivalent.

Examples:

- exact symbol lookup before embedding search;
- deterministic supersession edges before semantic guessing;
- simple rank fusion before complex learned retrieval;
- direct test evidence before multi-agent debate;
- explicit intent correction graph before free-form summarization.

Complexity must earn its place through hidden benchmark improvement.

---

## 35. Final governing principle

The strengthened AlinaCoder v0.2 should behave according to:

```text
Listen faithfully
→ preserve raw evidence
→ understand intent probabilistically
→ resolve context autonomously
→ keep the user's true goal stable
→ manage context proactively
→ remember decisions and failures with provenance
→ expose actionable uncertainty
→ choose the right depth of reasoning
→ test hypotheses with discriminating experiments
→ use specialists only when they add measured value
→ predict before acting
→ compare prediction with reality
→ detect regressions and forgotten constraints
→ learn from verified outcomes
→ remain simple, local-first, testable and reversible
```

The desired outcome is not an agent that merely sounds intelligent.

It is an agent that stays aligned with the user's real intent over long, noisy, technically complex work and can prove when its decisions are reliable.