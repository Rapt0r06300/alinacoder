# AlinaCoder v0.2 — Reliable Research, Noisy French Voice, Deep Context and Conditional Specialists Amendment

Date: 2026-09-04  
Status: Approved normative amendment to AlinaCoder v0.2  
Repository: `Rapt0r06300/alinacoder`  
Canonical development branch: `main` only  
Extends:
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-conversation-and-external-self-improvement-amendment.md`

## 1. Normative status

This document is an official extension of the AlinaCoder v0.2 specification. It strengthens three areas without weakening any prior invariant:

1. reliable internet research with grouped evidence and anti-overfitting evaluation;
2. robust understanding of highly noisy conversational French and hesitant voice input;
3. deeper contextual reasoning, self-critique, alternative-solution exploration, regression detection and optional specialist-agent orchestration when it measurably improves results.

All prior v0.2 requirements remain mandatory unless this amendment explicitly imposes a stronger rule.

The following invariants are unchanged:

- full autonomy is retained;
- direct commit/push to `main` is retained;
- Windows-first and Python 3.12+ are retained;
- local Ollama remains the model provider;
- deterministic execution evidence outranks model claims;
- safety, regression and evaluator-integrity floors are non-negotiable;
- checkpoints, rollback, resume and BestKnownState remain mandatory;
- specialist-agent use is conditional, evidence-driven and never an excuse to weaken verification.

---

## 2. Product objective

AlinaCoder should understand what the user means even when the request is incomplete, short, colloquial, spoken, hesitant, corrected mid-sentence or only understandable from project context.

It should independently determine when local repository evidence is sufficient and when trustworthy external research is required. When researching, it must seek multiple high-quality sources, group them around claims, preserve provenance, detect disagreement and prefer primary/official evidence when appropriate.

For nontrivial engineering decisions, AlinaCoder must not lock onto the first plausible answer. It should compare alternatives, search for disconfirming evidence, detect its own mistakes and regressions, and invoke temporary specialist reasoning only where evaluation shows that specialization is likely to improve the result.

The central rule becomes:

> Understand the real intent first; recover the right project context; gather the strongest available evidence; compare viable solutions; challenge the preferred solution; execute the smallest robust change; verify against visible and hidden regressions; then learn from measured outcomes.

---

# Part I — Reliable Internet Research

## 3. Research is evidence acquisition, not browsing for reassurance

Internet research is used only when it can materially improve correctness, freshness or decision quality.

Typical triggers include:

- current documentation, APIs or package behavior may have changed;
- a library/tool error cannot be explained reliably from local evidence;
- architecture choices depend on external standards or current best practice;
- the repository depends on an unfamiliar third-party component;
- multiple plausible solutions require external comparison;
- local evidence is contradictory or insufficient;
- a security, compatibility or versioning question requires current authoritative guidance.

Research must not be invoked merely to confirm an already-selected answer.

## 4. Research architecture

Add conceptual components such as:

```text
src/alinacoder/research/
├─ planner.py
├─ source_broker.py
├─ search_router.py
├─ source_ranker.py
├─ claim_grouper.py
├─ contradiction.py
├─ evidence_bundle.py
├─ freshness.py
└─ cache.py
```

Implementation may merge small modules while preserving responsibilities.

## 5. Research Planning

A research request is decomposed into explicit questions rather than one broad query.

Representative structure:

```text
ResearchPlan
- decision_to_support
- questions
- required_freshness
- preferred_source_classes
- disallowed/low-trust source classes
- contradiction_checks
- stopping_criteria
- evidence_budget
```

The research planner must distinguish:

- factual lookup;
- API/documentation verification;
- comparative engineering research;
- security/reliability verification;
- community-practice discovery;
- benchmark/research-literature review.

## 6. Source quality hierarchy

Source quality is contextual, but default precedence should usually favor:

1. official documentation/specification/source repository;
2. primary research paper or benchmark artifact;
3. authoritative maintainer release notes/issues/discussions;
4. trusted technical organizations or established engineering publications;
5. independent practitioner evidence when official material is incomplete;
6. community discussion for experience/sentiment, clearly labeled as such.

No single ranking replaces domain judgment.

## 7. Claim-centric evidence grouping

Research output is organized by claim, not by webpage.

Representative structure:

```text
ResearchClaim
- statement
- status: SUPPORTED / CONTESTED / WEAK / UNKNOWN
- supporting_sources[]
- contradicting_sources[]
- source_independence
- freshness
- confidence_class
- applicability_to_project
```

A final `ResearchEvidenceBundle` contains the minimum set of sources needed to justify a decision.

## 8. Source independence and duplication

Multiple pages repeating the same upstream announcement do not count as independent confirmation.

The system should identify likely common origin and avoid inflating confidence from copied/syndicated content.

## 9. Contradiction search

Before a high-impact external claim becomes part of a design or fix, AlinaCoder should actively search for evidence that would make the claim false, stale or inapplicable.

Examples:

- deprecated API despite current-looking tutorial;
- benchmark result dependent on a narrow setup;
- package behavior changed across versions;
- official documentation and field reports disagreeing;
- performance claim hiding regression/safety costs.

Contradictions remain visible in the evidence bundle.

## 10. Freshness and project applicability

Every external claim used for current engineering should store:

- retrieved date;
- publication/release date when available;
- package/tool/version applicability;
- project version match/mismatch;
- source provenance.

A correct statement for another version is not automatically valid for the current project.

## 11. Research stopping criteria

Research stops when additional sources are unlikely to change the decision materially.

Signals include:

- primary source found and independently corroborated where useful;
- key contradictions resolved or explicitly retained;
- source quality threshold reached;
- enough evidence exists to discriminate candidate solutions;
- remaining uncertainty is known and bounded.

Endless browsing is an anti-pattern.

## 12. Research provenance in decisions

For complex decisions, retain a compact chain:

```text
Intent
→ Research question
→ Claims
→ Sources
→ Contradictions
→ Decision impact
→ Selected/rejected solution
```

Raw webpages are not stored as permanent truth; durable lessons store distilled claims plus provenance and freshness anchors.

---

# Part II — Hidden Benchmarks and Anti-Overfitting Evaluation

## 13. Why hidden evaluation is mandatory

Self-improvement cannot be judged only on benchmarks the improving agent can inspect. Doing so creates direct incentives for overfitting, benchmark gaming and narrow optimization.

The evaluation system therefore separates visible development feedback from hidden promotion evidence.

## 14. Evaluation tiers

At minimum:

```text
DEVELOPMENT_SET
VALIDATION_HOLDOUT
HIDDEN_HOLDOUT
CANARY_SET
```

### DEVELOPMENT_SET

- cases may be visible to the improvement loop;
- detailed failures can be used for debugging;
- used to iterate rapidly.

### VALIDATION_HOLDOUT

- cases are not directly optimized during routine candidate edits;
- aggregated or bounded feedback may be exposed after evaluation;
- used to detect ordinary overfitting.

### HIDDEN_HOLDOUT

- cases, expected answers and detailed scoring logic are not exposed to the candidate-generating context;
- executed by an external evaluator process;
- only promotion-safe aggregate verdicts are returned.

### CANARY_SET

- refreshed or newly generated tasks intended to expose brittle memorization, evaluator gaming and distribution shift.

## 15. Hidden benchmark isolation

The candidate agent must not have filesystem, prompt, memory or tool access to hidden test definitions or expected outputs.

Where feasible:

- hidden evaluation lives outside the editable candidate workspace;
- evaluator files are integrity-checked;
- candidate process receives only task inputs it is allowed to see;
- hidden outputs are withheld;
- results return only safe aggregate metrics or categorical reasons.

## 16. Benchmark rotation

The supervisor should periodically rotate:

- natural-language paraphrases;
- French noise/disfluency patterns;
- repo layouts;
- error traces;
- dependency graphs;
- seeds;
- hidden regression scenarios;
- context-disambiguation cases;
- multi-agent trigger cases.

This makes memorizing fixtures less useful than acquiring the underlying capability.

## 17. Hidden evaluation dimensions

Hidden benchmarks should cover more than raw coding success.

Required dimensions include:

- task correctness;
- pass-to-pass regression rate;
- repository localization;
- transitive dependency understanding;
- intent inference from short requests;
- noisy French understanding;
- mid-utterance correction handling;
- project-context disambiguation;
- research source quality;
- contradiction detection;
- solution simplicity/robustness;
- self-error detection;
- correct choice to use or not use specialists;
- recovery/rollback;
- safety invariants;
- context efficiency.

## 18. Promotion vector

No single scalar score is sufficient.

Use an ordered or constrained vector such as:

```text
Safety
→ Correctness
→ Regression
→ Reliability
→ Context/Intent Accuracy
→ Research Quality
→ Reasoning/Decision Quality
→ Recovery
→ Efficiency
→ Complexity
```

A candidate cannot compensate for a safety regression by scoring higher on reasoning or speed.

## 19. Anti-gaming safeguards

Reject candidate changes that:

- weaken evaluator assertions;
- detect benchmark file names/case IDs to special-case behavior;
- bypass or mock required execution;
- remove hard test cases;
- alter scoring thresholds without separately validated evaluator evolution;
- use hidden-set leakage;
- improve only known benchmarks while hidden/canary performance deteriorates.

## 20. External self-improvement integration

The existing external self-improvement supervisor is strengthened to:

```text
Stable Version
→ Development baseline
→ Hidden/holdout baseline
→ Improvement hypothesis
→ Isolated candidate
→ Development evaluation
→ Validation holdout
→ Hidden holdout
→ Canary evaluation
→ Promotion vector comparison
→ PROMOTE / REJECT / WATCH
→ Post-promotion monitoring
→ automatic ROLLBACK if degraded
```

---

# Part III — Highly Noisy Conversational French and Voice Repair

## 21. Voice input is an incremental stream

Spoken French must not be treated as a finished clean sentence arriving all at once.

The conversation layer should support incremental utterance state.

Conceptual components:

```text
src/alinacoder/speech/
├─ stream_state.py
├─ segmenter.py
├─ disfluency.py
├─ repair.py
├─ intent_revision.py
└─ stabilization.py
```

## 22. Noise classes to support

The system must tolerate and reason through:

- `euh`, `ben`, fillers and hesitation;
- repetitions;
- partial words;
- false starts;
- reformulations;
- interruptions;
- corrections mid-sentence;
- self-contradiction followed by a final choice;
- missing words;
- ASR punctuation errors;
- homophone or near-homophone mistakes;
- mixed French/English technical terminology;
- colloquial contractions;
- abrupt change of topic;
- change of mind before action.

## 23. Do not normalize too early

Raw spoken evidence and normalized intent must remain distinct.

Representative structure:

```text
UtteranceState
- raw_segments[]
- normalized_segments[]
- active_repair_spans[]
- cancelled_spans[]
- tentative_intents[]
- confirmed_intent
- confidence
- last_stable_boundary
```

A cleanup pass must not silently erase a correction signal.

## 24. Intent revision states

Intent fragments may be:

- `TENTATIVE`;
- `CONFIRMED`;
- `REVISED`;
- `CANCELLED`.

Example:

```text
"améliore euh... non attends... pas la mémoire... enfin si mais surtout le contexte"
```

must not be reduced to the first stable noun. The system should preserve the revision chain and infer that context is primary while memory remains relevant but secondary.

## 25. Interruption semantics

When the user interrupts while AlinaCoder is still interpreting a live utterance:

- unfinished intent remains tentative;
- new speech may revise the pending intent;
- already-started irreversible actions must not be triggered from unstable intent fragments;
- reversible evidence gathering may continue only if it remains valid under plausible interpretations.

## 26. Stable-boundary execution

For conversational voice mode, execution should begin when either:

- an intent reaches a stable semantic boundary with sufficient confidence; or
- delaying further would provide no meaningful safety/accuracy benefit.

This must not make voice interaction sluggish. Low-risk reversible inspection can begin earlier than code mutation.

## 27. Change-of-mind handling

If the user changes their mind before publication:

- active mission is revised;
- obsolete steps are cancelled;
- already-created candidate changes are re-evaluated against the new intent;
- unrelated safe progress may be retained only if still useful;
- commit/push occurs only against the latest stable intent.

## 28. Noisy French acceptance scenarios

Hidden and visible fixtures must include examples such as:

- filler-heavy speech;
- repeated words;
- correction after negation;
- two consecutive changes of mind;
- interrupted technical nouns;
- wrong project name corrected later;
- ASR substitution requiring project context;
- colloquial Nice/French phrasing where technically relevant vocabulary is absent;
- French sentence containing English library/API names;
- short utterance such as `non l'autre` that requires live conversational context.

---

# Part IV — Deep Contextual Intelligence

## 29. Context resolution precedes planning

Before planning a short or ambiguous request, AlinaCoder should identify which project, goal, task or problem is most likely being referenced.

Canonical flow:

```text
User utterance
→ candidate projects
→ candidate goals/missions
→ candidate active problems
→ evidence ranking
→ context selection
→ intent compilation
→ planning
```

## 30. Context candidate model

Representative structure:

```text
ContextCandidate
- project_id
- mission_id
- task_id
- problem_id
- supporting_evidence[]
- contradictory_evidence[]
- recency
- conversational_link
- repository_link
- confidence
- risk_if_wrong
```

## 31. Deep context evidence

Context resolution may use:

- current conversation;
- most recent user objective;
- active/incomplete missions;
- roadmap next steps;
- current Git repo and HEAD;
- dirty working tree;
- recent commits;
- recently touched files/symbols;
- recent test failures;
- active hypotheses;
- unresolved blockers;
- project decisions;
- memory/lessons;
- repository architecture;
- history of similar wording;
- explicit project names when present.

## 32. Short-request behavior

Requests such as:

```text
continue
corrige ça
reprends
fini le truc
ça plante encore
mets ça propre
fais comme avant
non l'autre
```

must trigger context recovery before clarification.

Clarification is allowed only when the best candidates remain materially ambiguous and choosing incorrectly could cause meaningful unwanted change.

## 33. Context contradiction detection

If conversation memory says one task is active but Git/repository state proves another task was completed or superseded, live repository evidence wins and memory is marked stale.

## 34. Project/Goal/Problem Identity Graph

Extend the Project Mental Model with explicit identity links:

```text
Project
→ Goals
→ Missions
→ Tasks
→ Problems
→ Artifacts
→ Tests
→ Commits
→ Decisions
→ Conversations
→ Lessons
```

Cross-links include:

- `IMPLEMENTS`;
- `BLOCKS`;
- `SUPERSEDES`;
- `FIXES`;
- `REGRESSES`;
- `VALIDATES`;
- `REFERENCED_BY`;
- `RELATED_TO`;
- `EVOLVED_FROM`.

This graph supports reference resolution across long-lived projects.

---

# Part V — Deep Reasoning, Self-Critique and Multiple Solutions

## 35. Deep reasoning is risk-adaptive

AlinaCoder should reason more deeply when:

- impact is broad;
- architecture/public API may change;
- evidence is contradictory;
- prior attempts failed;
- regression surface is large;
- current confidence is limited;
- external research materially affects the choice;
- several viable implementation paths exist.

Routine deterministic edits do not require maximal deliberation.

## 36. Multiple-solution exploration

For medium/high-risk work where genuine alternatives exist, generate multiple candidate solution designs in isolated reasoning passes.

Each candidate should include:

- hypothesis;
- files/interfaces likely affected;
- dependency impact;
- expected benefits;
- likely failure modes;
- testability;
- complexity;
- reversibility;
- project-convention fit;
- external evidence where relevant.

## 37. Counter-evidence pass

After a preferred solution emerges, perform a dedicated adversarial pass asking:

- what assumption could be wrong?
- which dependency may have been missed?
- what previously passing behavior could break?
- is there a simpler solution?
- does external evidence contradict this approach?
- is the selected fix treating a symptom rather than root cause?
- is the test envelope too narrow?

A solution cannot be promoted while an unresolved critical counter-evidence finding remains.

## 38. ReasoningMismatch

Compare predicted outcomes to observed outcomes after meaningful actions.

Representative record:

```text
ReasoningMismatch
- prediction
- observation
- mismatch_type
- affected_hypothesis
- severity
- evidence
- required_response
```

Examples:

- expected targeted test to pass but it fails differently;
- expected dependency closure to be local but many downstream consumers change;
- expected API compatibility but import/build checks break;
- expected external behavior based on docs but actual installed version differs.

Repeated mismatches force hypothesis/planning reconsideration rather than patching blindly.

## 39. Regression of reasoning quality

Self-improvement evaluation must detect not just code regressions but cognitive regressions such as:

- asking unnecessary clarifying questions;
- choosing wrong project context;
- trusting weak sources over primary evidence;
- failing to search for contradictions;
- overusing specialists;
- underusing specialists where they reliably help;
- selecting more complex solutions without benefit;
- repeating previously failed reasoning patterns.

---

# Part VI — Conditional Specialist Agents

## 40. Default remains a strong generalist

The default execution architecture remains one primary Ollama-driven AlinaCoder reasoning loop.

Permanent multi-agent decomposition is not introduced.

Specialists are temporary reasoning/exploration processes, activated only when expected value is positive.

## 41. Specialist roles

Potential temporary specialists include:

- `Researcher` — external-source acquisition and contradiction search;
- `RepositoryArchitect` — architecture/dependency impact analysis;
- `Debugger` — competing causal hypotheses and reproduction strategy;
- `RegressionReviewer` — pass-to-pass and hidden impact analysis;
- `SecurityCritic` — high-risk safety/security scrutiny;
- `AlternativeDesigner` — independent solution generation;
- `TestStrategist` — adequacy, regression and property/mutation strategy.

Roles are logical capabilities and may reuse the same installed Ollama model with isolated contexts.

## 42. AgentValueEstimator

Before spawning specialists, estimate whether they are likely to improve the outcome.

Representative factors:

- task risk;
- uncertainty;
- number of plausible hypotheses;
- architecture breadth;
- prior specialist benefit on similar tasks;
- remaining context budget;
- time/resource budget;
- hidden benchmark evidence;
- cost of a wrong decision.

Representative result:

```text
SpecialistDecision
- proposed_roles[]
- expected_quality_gain
- expected_cost
- confidence
- trigger_evidence
- decision: USE / SKIP
```

## 43. Context isolation

Specialists receive bounded, role-relevant evidence rather than the full primary reasoning trace.

This reduces correlated anchoring and context pollution.

## 44. Specialists cannot directly mutate canonical state

By default, specialist outputs are advisory evidence/designs.

The primary orchestrator remains responsible for:

- policy checks;
- final design selection;
- code mutation;
- verification;
- commit/push.

A future implementation may allow tightly scoped specialist mutation only if separately validated; it is not required by this amendment.

## 45. Specialist disagreement

Disagreement is retained explicitly.

The primary decision engine resolves it using:

- deterministic evidence;
- reproduction/tests;
- source quality;
- project invariants;
- regression impact;
- simplicity and reversibility.

Voting alone is not considered proof.

## 46. Measuring specialist value

Track by task category:

- success delta with/without specialists;
- regression delta;
- hidden benchmark delta;
- time/tool/token overhead;
- disagreement frequency;
- cases where specialists prevented a wrong solution;
- cases where specialists added noise.

If a specialist pattern does not improve measured outcomes, it should be disabled for similar tasks.

## 47. Specialist anti-patterns

Avoid:

- spawning specialists for every task;
- using more agents as a substitute for better evidence;
- majority vote without execution grounding;
- copying all context into every role;
- letting specialist suggestions bypass safety/verification;
- treating specialist self-confidence as proof;
- keeping a complex specialist architecture that fails hidden benchmarks.

---

# Part VII — Integrated Runtime Flow

## 48. Canonical strengthened flow

For a nontrivial conversational task:

```text
Voice/Text Input
→ Incremental normalization/repair
→ Context candidate recovery
→ Intent stabilization
→ Mission compilation
→ Local evidence collection
→ Decide whether web research is needed
→ Group claims/sources/contradictions
→ Risk/uncertainty classification
→ Decide whether specialists add value
→ Generate competing hypotheses/designs
→ Counter-evidence search
→ Select simplest robust evidence-backed plan
→ Execute in bounded steps
→ Compare predictions vs observations
→ Detect ReasoningMismatch
→ Replan if needed
→ Run targeted + impacted + hidden-safe verification
→ Critic/regression review
→ Commit/push to `main`
→ Persist evidence, lessons and context
→ Continue autonomously
```

## 49. Low-risk compressed path

Low-risk tasks may use:

```text
Understand Context
→ Plan
→ Act
→ Verify
→ Commit
```

No unnecessary research or specialist ceremony.

## 50. High-risk expanded path

High-risk tasks require stronger use of:

- context identity checks;
- competing hypotheses;
- research contradiction checks when external facts matter;
- multiple solutions;
- specialist evaluation when beneficial;
- stronger regression envelope;
- counter-evidence;
- rollback readiness.

Risk changes depth, not autonomy.

---

# Part VIII — Acceptance and Hidden Evaluation Scenarios

## 51. Research acceptance scenarios

At minimum:

1. current official docs contradict an old blog post; official current evidence wins;
2. three articles repeat one upstream source; independence score does not falsely become three confirmations;
3. sources disagree across library versions; installed/project version is used to choose applicability;
4. research stops after decision-quality evidence is sufficient;
5. external claim is stored with provenance/freshness and later invalidated after version change;
6. high-impact claim triggers deliberate contradiction search.

## 52. Hidden benchmark acceptance scenarios

At minimum:

1. candidate improves visible development tests but degrades hidden context understanding → reject;
2. candidate special-cases known fixture names → hidden/canary exposes failure;
3. candidate weakens evaluator assertion → integrity gate rejects;
4. candidate improves speed but worsens regression rate → reject;
5. candidate improves one metric while safety floor regresses → reject;
6. rotated French paraphrases remain correctly understood.

## 53. Noisy voice acceptance scenarios

At minimum:

1. `euh continue enfin non attends reprend le bug d'avant` resolves final corrected intent;
2. repeated fragments do not duplicate tasks;
3. `pas la mémoire... enfin si mais surtout le contexte` produces primary/secondary priority correctly;
4. live interruption cancels tentative plan before mutation;
5. `non l'autre projet` switches project context from conversation evidence;
6. ASR misrecognition is corrected from repository/project context;
7. change of mind before push revalidates candidate work against latest intent.

## 54. Deep context acceptance scenarios

At minimum:

1. `continue` chooses the right unfinished mission across multiple known projects;
2. `ça plante encore` connects to the most recent unresolved reproduction;
3. stale memory conflicts with Git reality and is invalidated;
4. short reference selects project/goal/problem using evidence ranking;
5. high-impact ambiguity unresolved by context produces one concise clarification instead of guessing.

## 55. Reasoning and specialists acceptance scenarios

At minimum:

1. first plausible root cause is falsified and agent switches hypothesis;
2. a complex alternative is rejected in favor of a smaller equally correct patch;
3. predicted local impact proves broad; `ReasoningMismatch` triggers replan;
4. specialist architect prevents a transitive dependency regression on a high-risk task;
5. same task class shows no benefit from specialists and future routing skips them;
6. specialist disagreement is resolved by tests/evidence, not voting;
7. primary agent performs better alone on simple task and specialist router correctly stays off.

---

# Part IX — Metrics

## 56. New metrics

Add at least:

### Research

- primary-source usage rate;
- claim/source independence ratio;
- contradiction discovery rate;
- stale-source rejection rate;
- decision-changing research rate;
- unnecessary research rate.

### Hidden evaluation

- development-to-hidden generalization gap;
- canary degradation rate;
- benchmark-gaming detections;
- hidden regression count;
- evaluator-integrity violations.

### French/voice

- noisy-intent accuracy;
- repair/correction accuracy;
- wrong-action-from-tentative-intent count;
- unnecessary clarification rate;
- project-switch interpretation accuracy.

### Context

- project selection accuracy;
- goal/task/problem resolution accuracy;
- stale-context catches;
- short-request resolution accuracy.

### Reasoning

- hypothesis falsification success;
- first-hypothesis anchoring rate;
- ReasoningMismatch detection rate;
- mismatch-to-replan success;
- complexity avoided while preserving correctness.

### Specialists

- specialist-trigger precision;
- specialist-trigger recall on beneficial cases;
- quality delta;
- regression delta;
- hidden benchmark delta;
- overhead per useful specialist invocation.

---

# Part X — Implementation Priority Guidance

## 57. Sequencing guidance

After prior v0.2 foundations, preferred implementation order for this amendment is:

1. context candidate/identity graph extension;
2. incremental noisy-French utterance state and intent revision;
3. research plan/source/claim/evidence bundle pipeline;
4. contradiction/freshness/source-independence logic;
5. hidden evaluation isolation and holdout interfaces;
6. ReasoningMismatch records and replanning integration;
7. multi-solution/counter-evidence pass hardening;
8. AgentValueEstimator and specialist router;
9. specialist measurement feedback loop;
10. rotated hidden/canary acceptance suite;
11. full E2E conversational + research + specialist scenarios.

This is sequencing guidance, not the detailed implementation plan.

---

## 58. Explicit anti-patterns

AlinaCoder v0.2 must avoid:

1. browsing until it finds a source agreeing with its first answer;
2. counting duplicated/syndicated sources as independent evidence;
3. storing current web claims forever without freshness/version anchors;
4. exposing hidden benchmark fixtures to the candidate improvement loop;
5. optimizing only public/visible benchmarks;
6. stripping speech disfluencies before understanding corrections;
7. acting on tentative voice intent as if final;
8. asking for clarification before trying project-context resolution;
9. choosing context from memory when Git/repository evidence contradicts it;
10. committing to the first plausible solution on high-risk work;
11. self-reflecting repeatedly without new evidence;
12. using multi-agent decomposition by default;
13. trusting specialist consensus without deterministic validation;
14. keeping specialists whose measured hidden benefit is non-positive;
15. trading safety/regression floors for benchmark gains;
16. weakening tests/evaluators to make self-improvement look better;
17. adding architecture complexity without measurable outcome improvement.

---

## 59. Final strengthened v0.2 contract

AlinaCoder v0.2 is a fully autonomous coding system that should:

- understand natural and highly noisy French, including voice hesitation, corrections, repetition, interruption and change of mind;
- automatically recover which project, goal, task or problem the user means from deep live context;
- seek reliable internet evidence only when it materially improves the decision;
- group sources around claims, distinguish independent evidence, detect contradictions and track freshness;
- protect self-improvement with development, holdout, hidden and canary evaluations that resist overfitting;
- explore multiple plausible solutions for meaningful work;
- actively search for evidence that its preferred answer is wrong;
- detect mismatches between predicted and observed outcomes and replan;
- detect both code regressions and reasoning/context regressions;
- remain a strong single-agent generalist by default;
- invoke temporary specialists only where measured evidence suggests they improve results;
- resolve specialist disagreement through execution evidence and project invariants rather than voting;
- autonomously edit, test, recover, commit and push directly to `main` once all deterministic gates pass;
- learn only from evidence-backed outcomes and invalidate stale lessons when the project changes.

The target is not the largest agent architecture. The target is the highest reliable engineering quality and autonomy that can be demonstrated on both known and hidden evidence.