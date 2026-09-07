# AlinaCoder Cognitive Kernel + Zero-Cost Frontier Mesh — Design Specification

Date: 2026-09-07
Status: DESIGN — awaiting user review before implementation
Repository: `Rapt0r06300/alinacoder`
Baseline: `991bb4884296436046319e3aa7e5317ccb49674e`
Branch policy: `main` only

## 1. Purpose

This design upgrades AlinaCoder from a collection of capable subsystems into a coherent long-horizon coding agent whose conversational understanding, planning, memory, execution state, verification, model routing, quota management, and desktop observability reinforce one another.

The target is not to claim that AlinaCoder will always be correct or equivalent to a frontier commercial coding agent. The target is a system that is measurably more capable, robust, efficient, self-correcting, transparent, and resilient than the current implementation, while preserving strict zero-cost routing rules for remote inference when zero-cost mode is selected.

The system MUST:

1. understand corrections, references, constraints, preferences, and evolving intent across long conversations;
2. keep an explicit, current, machine-checkable execution state instead of inferring state only from chat history;
3. couple planning and memory bidirectionally;
4. select the strongest eligible model for the exact task, based on evidence rather than static names;
5. use free remote capacity without violating provider terms, bypassing quotas, rotating identities, or deliberately evading rate limits;
6. preserve local Ollama as the foundational no-API-billing fallback;
7. spend scarce remote quota only where expected quality gain justifies it;
8. detect uncertainty and use it as a control signal for inspect / experiment / verify / ask / escalate decisions;
9. verify work from execution evidence, not model self-report;
10. expose a concise operational trace in the desktop UI similar to modern coding agents without exposing hidden chain-of-thought.

## 2. Non-goals and hard prohibitions

The following are explicitly out of scope:

- rotating IP addresses, proxies, accounts, identities, API keys, or organizations to bypass provider quotas or rate limits;
- impersonating a new user/device to obtain additional free allocations;
- automatic paid fallback when the user selected zero-cost mode;
- silently enabling billing, auto-reload, credit purchase, or pay-as-you-go;
- treating a model as free because of stale documentation or a past promotion;
- treating provider/model names as a sufficient quality benchmark;
- storing or displaying hidden model chain-of-thought;
- allowing model confidence alone to authorize destructive or irreversible actions;
- promoting unverified model-generated advice into durable project memory;
- silently deleting previously learned user constraints or verified work when the conversation changes direction.

## 3. Existing foundations to preserve

The implementation MUST extend rather than rebuild these current systems:

### Conversation

Current files:

- `src/alinacoder/conversation/engine.py`
- `src/alinacoder/conversation/advanced.py`
- `src/alinacoder/conversation/models.py`
- `src/alinacoder/conversation/voice.py`

Existing valuable invariants to preserve:

- RAW + MEANING turn preservation;
- user/assistant perspective separation;
- artifact anchors;
- targeted correction without deleting unrelated verified work;
- user-origin requirement for durable preferences;
- clarification cost concept;
- micro-turn stability and committed-user-turn mutation gate;
- branchable conversational context;
- failure replay.

### Goals

Current files:

- `src/alinacoder/goal/engine.py`
- `src/alinacoder/goal/models.py`

Existing valuable invariants to preserve:

- explicit objective and criteria;
- verified/stale criterion state;
- evidence-gated completion;
- pause/resume/cancel;
- strategy failure recording;
- replanning after repeated failures;
- proof required before declaring impossibility.

### Memory

Current files:

- `src/alinacoder/memory/store.py`
- `src/alinacoder/memory/context.py`
- `src/alinacoder/memory/retrieval.py`
- `src/alinacoder/memory/planner.py`
- `src/alinacoder/memory/graph.py`
- `src/alinacoder/memory/skillbook.py`

Existing valuable invariants to preserve:

- project-scoped memory;
- source freshness;
- repository index integration;
- graph retrieval;
- bounded context compilation;
- verified-evidence requirement before experience becomes a skill;
- SQLite WAL/FULL durability for SkillBook.

### Intelligence mesh

Current files:

- `src/alinacoder/intelligence_mesh/provider_atlas.py`
- `src/alinacoder/intelligence_mesh/providers.py`
- `src/alinacoder/intelligence_mesh/fabric.py`
- `src/alinacoder/intelligence_mesh/routing.py`
- `src/alinacoder/intelligence_mesh/runtime.py`
- `src/alinacoder/intelligence_mesh/qualification.py`

Existing valuable invariants to preserve:

- exact zero-cost proof;
- no paid spillover;
- fail-closed pricing;
- route depletion after quota exhaustion;
- provider/model failover;
- hybrid remote-to-local fallback;
- local-only and free-cloud isolation;
- retired provider tombstones.

### Orchestration

Current file:

- `src/alinacoder/orchestration/core.py`

Existing valuable invariants to preserve:

- lease/fencing semantics;
- semantic conflict detection;
- lineage-aware independent voting;
- topology selection based on coupling;
- council value gate;
- diverse specialist selection;
- disable multi-agent topology when it cannot prove terminal value.

### Desktop and live activity

Current files:

- `src/alinacoder/desktop/app.py`
- `src/alinacoder/desktop/workbench.py`
- `src/alinacoder/desktop/activity.py`
- `src/alinacoder/desktop/experience.py`

These remain the canonical user surface.

## 4. Target architecture

The target architecture is a layered system:

```text
User / Voice / Desktop
        |
        v
+-----------------------------+
| Intent Compiler             |
| - raw + meaning             |
| - alternatives              |
| - constraints               |
| - references                |
| - uncertainty               |
+-----------------------------+
        |
        v
+=====================================================+
| COGNITIVE KERNEL                                    |
|                                                     |
| Goal State <----> Plan State <----> Episodic Memory |
|     |                |                 |             |
|     +--------> Execution Ledger <------+             |
|                      |                              |
|                 Uncertainty                         |
|                      |                              |
|               Cognitive Controller                  |
+=====================================================+
        |
        +------------------+
        |                  |
        v                  v
 Tool/Repo Runtime     Frontier Mesh
        |              - capability profiler
        |              - quota ledger
        |              - dynamic router
        |              - provider health
        |              - council/escalation
        |              - local fallback
        |                  |
        +--------+---------+
                 v
         Verification Kernel
                 |
                 v
       Evidence / Skill Learning
                 |
                 v
         Desktop Activity Trace
```

No layer may infer success solely from assistant text.

## 5. Cognitive Kernel

### 5.1 Canonical cognitive state

Add a canonical `CognitiveState` persisted through the existing state store. It MUST be reconstructible from events and MUST include identifiers/versioning rather than opaque serialized model thoughts.

Proposed fields:

- `session_id`
- `state_version`
- `active_goal_id`
- `intent_revision`
- `plan_revision`
- `current_phase`
- `current_subtask_id`
- `active_requirements`
- `active_constraints`
- `prohibitions`
- `open_questions`
- `uncertainties`
- `selected_artifacts`
- `verified_facts`
- `stale_facts`
- `recent_failures`
- `execution_ledger_version`
- `memory_snapshot_version`
- `current_model_route`
- `last_verified_repo_state`

The state MUST contain operational facts and contracts only. It MUST NOT persist private hidden chain-of-thought.

### 5.2 Intent Compiler v2

The current conversation engine stores a single normalized meaning. Extend it so each committed user turn can produce a versioned `IntentEnvelope`:

- raw input;
- normalized meaning;
- primary intent;
- plausible alternatives;
- referenced artifacts/entities;
- requirements added;
- requirements changed;
- requirements cancelled;
- constraints;
- prohibitions;
- desired output/result;
- urgency / explicit continuation intent;
- confidence per interpretation;
- uncertainty causes;
- source turn IDs.

The deterministic engine remains authoritative over stored state. LLM interpretation is only a proposal until validated against context and repair rules.

### 5.3 Causal correction propagation

Current targeted correction preserves unrelated work. Extend this with a dependency graph:

- intent assumptions;
- plan steps;
- retrieved memories;
- observations;
- tool results;
- verification evidence.

When the user corrects one assumption, all descendants depending on that assumption become stale. Independent verified evidence remains valid.

Example:

- User: “repair the installer”
- Agent inspects Windows installer.
- User: “no, I mean the model bridge.”
- Installer-specific hypotheses and plan nodes become stale.
- Unrelated repository index and provider-atlas reads remain usable if their source state is unchanged.

This MUST be deterministic and testable.

### 5.4 Clarification by expected information gain

Replace the scalar-only clarification rule with a policy that considers:

- probability of ambiguity;
- cost of wrong action;
- reversibility;
- information expected from one clarifying question;
- ability to resolve ambiguity through safe read-only inspection;
- question cost / interruption cost.

Decision order:

1. if safe inspection can resolve ambiguity cheaply, inspect;
2. if a reversible sandbox experiment can resolve it safely, experiment;
3. if uncertainty remains and wrong-action cost is low, choose the best-supported interpretation and expose the assumption;
4. if uncertainty remains and wrong-action cost is high, ask one highest-information-gain question.

AlinaCoder MUST avoid asking questions merely because confidence is below a fixed threshold.

### 5.5 Uncertainty as a control signal

Add structured uncertainty dimensions:

- intent uncertainty;
- repository-state uncertainty;
- factual uncertainty;
- model-route uncertainty;
- verification uncertainty;
- tool-effect uncertainty;
- environment uncertainty.

Map uncertainty + action criticality into policies:

- `ACT`
- `INSPECT`
- `SANDBOX_PROBE`
- `VERIFY`
- `ESCALATE_MODEL`
- `CALL_COUNCIL`
- `ASK_USER`
- `BLOCK`

Confidence MUST NOT be displayed as fake precision. Internally it may be numeric if calibrated from observed outcomes; otherwise use bounded classes such as LOW/MEDIUM/HIGH with provenance.

## 6. Plan–Memory coupling

### 6.1 Hierarchical planning

Replace flat plan strings as the only active representation with a versioned plan graph:

- phase;
- subtask;
- dependencies;
- required evidence;
- completion predicate;
- affected files/symbols;
- expected tools;
- status;
- attempts;
- failure reasons;
- memory query intent.

Recommended phases for software repair:

1. understand;
2. reproduce / establish baseline;
3. localize;
4. hypothesize;
5. implement;
6. verify;
7. adversarial review;
8. release/commit.

Phases are guidance, not rigid mandatory steps. Trivial tasks may collapse phases.

### 6.2 Plan-guided memory retrieval

Memory retrieval MUST be conditioned on:

- active goal;
- current phase;
- current subtask;
- files/symbols in the blast radius;
- prior failures relevant to this subtask;
- explicit user constraints;
- current repository state version.

Static source weights such as fixed `0.55` / `0.65` MUST not be the sole ranking mechanism.

Use a budgeted ranking combining:

- lexical relevance;
- graph relationship;
- phase relevance;
- recency/freshness;
- source authority;
- evidence validity;
- diversity / maximal marginal relevance;
- known failure relevance;
- cost to include.

### 6.3 Memory-driven replanning

Memory statistics MUST inform plan control. Replan when evidence shows:

- repeated failed strategy;
- same command/edit pattern repeating without new information;
- issue reproduction still failing after changes;
- key observation becoming stale;
- newly discovered constraint invalidating a planned step;
- verification contradicting the active hypothesis;
- expected blast radius materially changing.

The planner MUST be able to preserve completed independent nodes while replacing only affected descendants.

## 7. Execution Ledger

Add `src/alinacoder/runtime/ledger.py` (final exact path may be adjusted during implementation plan, but the responsibility boundary is mandatory).

The ledger is deterministic and contains mechanically derived execution facts.

### 7.1 Observation records

For every file/search/read observation record:

- observation ID;
- repository state/version;
- path;
- range/symbol/query;
- content digest or result digest;
- timestamp/order;
- validity status;
- invalidation cause.

### 7.2 Modification state

Record:

- mutated paths;
- before/after digests;
- originating tool/agent;
- commit/worktree/state version;
- semantic affected symbols if known.

A previous read of an affected file becomes stale after mutation unless the exact observed span is proven unchanged.

### 7.3 Command records

Record:

- normalized command/tool call;
- arguments;
- repo state version;
- effect class;
- exit/result digest;
- duration;
- whether still reusable;
- failure classification.

### 7.4 Inform path

Before each model decision, provide a compact ledger summary:

- what has been inspected and remains valid;
- what changed;
- current failing tests;
- last verification point;
- repeated failures to avoid;
- pending unknowns.

### 7.5 Govern path

Before execution:

- exact repeat of a read-only command under unchanged relevant state may reuse prior result;
- repeated test under unchanged state should be nudged, not blindly blocked;
- repeated known-failed mutation strategy without new evidence should trigger replanning;
- destructive actions remain governed by existing approval/security policies.

This layer MUST require zero additional LLM calls.

## 8. Adaptive context management

### 8.1 Three-tier context workspace

Use:

1. **stable anchors** — goal, user constraints, prohibitions, current definitions;
2. **working memory** — current phase, active subtask, key fresh observations, current diff/test state;
3. **lossless history store** — complete event/tool/interaction log outside prompt context.

### 8.2 Proactive context folding

At meaningful phase boundaries, completed trajectories may be folded into an actionable summary containing:

- decision made;
- evidence supporting it;
- files/symbols involved;
- rejected hypotheses;
- unresolved questions;
- verification state;
- source/event IDs for reconstruction.

Folding MUST NOT delete the lossless underlying log.

### 8.3 Programmatic history access

Expose search/filter tools over the lossless trajectory/ledger so the agent can recover detail without restoring the entire chat into the prompt.

At minimum:

- text search;
- event type filter;
- file/path filter;
- failure filter;
- model/provider filter;
- time/step range;
- Python-accessible structured export when available.

### 8.4 Context budget controller

The controller chooses what to include based on:

- task complexity;
- model context window;
- phase;
- mandatory anchors;
- information value;
- expected token cost.

Mandatory constraints and verified evidence MUST never be silently dropped. If they exceed budget, route to a larger-context eligible model or explicitly fail closed rather than truncating critical constraints.

## 9. Zero-Cost Frontier Mesh

## 9.1 Routing principle

AlinaCoder MUST select the strongest eligible route for the current capability requirement, not the most famous model and not the provider that appears first.

Selection pipeline:

```text
Discover -> Prove zero cost -> Health check -> Capability profile
-> Quota check -> Context-fit check -> Quality LCB -> Latency/quota value
-> Route -> Observe outcome -> Update profile
```

### 9.2 Provider classes

Maintain current provider-atlas safety classes. Add explicit runtime capability for:

- authenticated zero-cost provider;
- anonymous zero-cost provider when provider documentation permits it;
- aggregator free router;
- exact free model route;
- local no-API-billing route.

### 9.3 Kilo anonymous bridge

Kilo currently documents anonymous access to free models with a rate limit per IP. AlinaCoder MAY use this as a zero-configuration source only when current provider evidence confirms anonymous free access.

Required behavior:

- no fake authentication;
- no IP rotation or quota evasion;
- obey 429 and Retry-After/reset signals;
- anonymous route kept separate from authenticated Kilo route;
- exact current pricing/discovery checked before dispatch;
- when the allowance is exhausted, route elsewhere rather than retry-spam.

`kilo-auto/free` MAY be an eligible fallback router, but explicit individually profiled free models SHOULD outrank it when AlinaCoder has stronger evidence about task fit.

### 9.4 OpenRouter free routes

Discover exact free models and profile them independently. Use provider-side generic free router only when:

- exact free routes are unavailable or inferior;
- the router itself is currently free;
- provider-side paid fallback is impossible;
- returned model identity can be recorded where available.

### 9.5 Groq and other hard-stop free quotas

Use only after account/plan qualification proves no paid spillover. Read remaining quota/reset headers where available and update the quota ledger.

### 9.6 DeepSeek

Official DeepSeek API pricing MUST be treated as paid unless live authoritative evidence says otherwise.

AlinaCoder MAY use DeepSeek model families when:

- a third-party provider exposes an exact zero-price route that passes current qualification; or
- the model is running locally under the local no-API-billing policy.

The name `DeepSeek` MUST never imply free status.

### 9.7 Local model ladder

Installer/runtime should benchmark available machine resources and maintain at least:

- a **strong local coding model** selected for the machine;
- a **fast local utility model** for cheap classification/summarization/simple tasks, if resources allow;
- a safe CPU-capable fallback when GPU models cannot fit.

Candidate families are discovered dynamically and versioned; no model name is permanently hardcoded as “best.”

Local qualification should measure:

- memory fit/headroom;
- context capacity;
- prompt throughput;
- generation throughput;
- simple code-repair score;
- tool-following score;
- stability under repeated inference.

### 9.8 Capability profiler

Add a `ModelCapabilityProfile` with dimensions such as:

- code generation;
- debugging;
- repository reasoning;
- architecture/design;
- tool-use reliability;
- instruction following;
- long-context stability;
- conversational repair;
- summarization;
- speed;
- measured failure rate;
- context window;
- freshness timestamp;
- sample count;
- confidence/lower bound.

Profiles may combine:

1. provider metadata;
2. known static seed priors;
3. AlinaCoder microbenchmarks;
4. task outcome observations.

Observed evidence MUST dominate stale priors over time.

### 9.9 Quality lower confidence bound

Routing should use a conservative score rather than raw average.

Example conceptual form:

`quality_lcb = mean_quality - uncertainty_penalty`

The exact estimator will be fixed in the implementation plan and tests. A model with one lucky success MUST not immediately outrank a repeatedly proven model.

### 9.10 Task-aware capability requirements

Classify each inference call, e.g.:

- `conversation`
- `intent_resolution`
- `planning`
- `repository_search`
- `architecture`
- `code_generation`
- `debugging`
- `review`
- `verification_analysis`
- `summarization`
- `research_synthesis`

The classifier itself should preferably be deterministic/cheap first, with LLM escalation only when needed.

### 9.11 Quota Ledger

Persist provider/model quota state:

- last known RPM/RPD/TPM/TPD limits if provided;
- remaining requests/tokens;
- reset timestamps;
- recent 429/402/403/5xx events;
- cooldown deadline;
- average latency;
- successful calls;
- failed calls;
- last discovery timestamp;
- cost proof expiry.

The ledger MUST distinguish:

- depleted until reset;
- temporarily unhealthy;
- authentication failure;
- billing blocked;
- retired;
- unknown.

### 9.12 Quota-aware reservation

Scarce high-quality free capacity MAY be reserved for higher-value phases.

Examples:

- local model performs repository indexing;
- cheap remote model summarizes logs;
- strongest free frontier model reviews the architecture or resolves a hard debugger fork;
- independent second lineage reviews a high-criticality patch.

Reservation is advisory and evidence-based; it MUST NOT block progress when a strong route is genuinely necessary.

### 9.13 Retry and failover

Do not repeatedly hit a route known to be exhausted.

Error policy:

- 429 -> record reset/cooldown; route elsewhere;
- 402 -> hard block route;
- 401/403 -> disable until credentials/account state changes;
- 5xx/network -> bounded retry/circuit breaker;
- malformed response -> penalize health and try another route;
- semantic failure -> do not blindly retry same prompt/model; change strategy or model lineage.

## 10. Multi-model cognition

### 10.1 Primary + critic pattern

For hard/critical work:

1. primary model proposes hypothesis/patch/plan;
2. independent critic receives task contract + evidence + proposed result, not the primary hidden reasoning;
3. critic returns defects, missing tests, contradictions, or PASS/INCONCLUSIVE;
4. verification kernel remains final authority.

### 10.2 Lineage diversity

Existing lineage-aware vote aggregation remains mandatory. Multiple routes serving the same underlying model family do not count as independent cognitive votes.

### 10.3 Council activation

Council runs only if expected terminal value exceeds latency/quota/resource cost. Signals include:

- high criticality;
- high uncertainty;
- disagreement between evidence and current hypothesis;
- repeated failures;
- large blast radius;
- release-gate work;
- security-sensitive changes.

Trivial interactions remain single-model/local.

## 11. Verification Kernel

### 11.1 Execution-grounded completion

A plan node or goal criterion can be complete only from fresh evidence bound to the relevant repository state.

Evidence examples:

- test invocation + exit status + state digest;
- issue reproduction fail-before/pass-after;
- compilation result;
- static check result;
- independent verifier result;
- file/hash/provenance receipt;
- release artifact smoke test.

### 11.2 Reproduction gates

When a bug is reproducible, its reproduction MUST be a first-class completion gate. A code change cannot be called fixed while the latest valid reproduction result still fails.

### 11.3 Evidence invalidation

Any edit affecting the proven surface invalidates dependent evidence until rerun. No stale green test may certify a later state.

### 11.4 Independent final audit

High-criticality release/installer/security changes should require a separate verifier context or lineage where practical, plus deterministic execution proof.

## 12. Learning and self-improvement

### 12.1 Experience cards

Extend existing `SkillBook` experience model. A candidate experience should include:

- problem signature;
- repository/project scope;
- strategy;
- preconditions;
- failed alternatives if useful;
- verification evidence IDs;
- commit/state binding;
- expiry/revalidation policy;
- confidence/sample count.

### 12.2 Promotion gate

Durable experience is promoted only when:

- outcome is verified;
- evidence is available;
- it does not conflict with protected governance rules;
- it is project-scoped unless explicitly generalizable;
- repeated failures are not mislearned as success.

Human acceptance/commit is a strong signal but does not replace executable verification when executable proof is available.

### 12.3 Negative memory

Record known failed strategies, including conditions under which they failed, to prevent loops.

A failed strategy is not a permanent prohibition. New evidence or changed state can reopen it.

### 12.4 Skill quality tracking

Skill usage outcomes should update reliability statistics. Low-performing learned skills become quarantined rather than silently deleted.

## 13. Conversation robustness campaign

Create a large deterministic conversation replay suite covering at least these families:

1. correction after several turns;
2. reference pronouns to selected files/diffs/tests;
3. multiple selected artifacts ambiguity;
4. “continue” after restart;
5. “do the same for X”;
6. negation (“not X, Y”);
7. constraint tightening mid-task;
8. constraint removal;
9. scope expansion;
10. scope narrowing;
11. priority reorder;
12. interruption while assistant is speaking;
13. partial ASR not authorizing mutation;
14. noisy French technical vocabulary;
15. English/French mixed technical input;
16. typo correction;
17. user contradicts assistant assumption;
18. assistant uncertainty without user contradiction;
19. stale artifact reference after file deletion/rename;
20. user references old commit vs current worktree;
21. new message arrives during long run;
22. “stop only this subtask” vs stop whole run;
23. “undo that last change”;
24. user changes desired output format without changing goal;
25. long 100+ turn conversation retaining active constraints;
26. false memory candidate rejected;
27. unrelated verified work preserved after correction;
28. correction invalidates dependent plan only;
29. ambiguous destructive request asks/blocks;
30. safe read-only ambiguity resolves by inspection.

The first milestone should include hundreds of generated variations. The release gate target is a stable corpus of at least 1,000 replay cases across deterministic and model-assisted interpretation scenarios, with failures retained as regression fixtures.

## 14. Desktop UX — Codex-like operational trace

The desktop stays simple: chat is primary.

### 14.1 Main surface

- conversation stream;
- input/voice controls;
- active project/repository;
- compact current status.

### 14.2 Live activity surface

Show structured operational events, not hidden chain-of-thought:

- understanding / assumption changed;
- plan created/revised;
- searching repository;
- reading file;
- running test;
- applying patch;
- verifying;
- model route selected;
- provider changed due to quota/health;
- critic invoked;
- retry/recovery;
- evidence passed/failed;
- commit/release event.

### 14.3 Model route explanation

For each inference call expose concise facts:

- provider;
- model;
- task class;
- zero-cost proof state;
- why selected, e.g. “best verified debugging score among available free routes”;
- fallback reason when route changes.

Do not expose secret keys, billing identifiers, raw authorization headers, private hidden reasoning, or unnecessarily verbose provider internals.

### 14.4 Cognitive status card

Optional compact card:

- Goal
- Current phase
- Next action
- Open blocker
- Verification state
- Model

The user must be able to understand what AlinaCoder is doing without reading logs.

## 15. Performance and efficiency

### 15.1 Fast-path policy

Simple deterministic tasks MUST avoid expensive inference.

Examples:

- exact state lookup;
- known file path resolution;
- repeated read reuse;
- hash checks;
- quota/reset checks;
- basic routing classification;
- formatting known structured state.

### 15.2 Remote frontier call minimization

A strong remote call should receive precompiled high-value context rather than raw repository/history dumps.

Preferred pattern:

1. deterministic/local inspect;
2. local/cheap summarize if needed;
3. frontier reason/code/review;
4. deterministic execute;
5. deterministic verify;
6. frontier revisit only if evidence fails or uncertainty remains.

### 15.3 Cache correctness

Caching is allowed only with explicit state binding and invalidation. No cache hit may survive a relevant repository state change without proof that the cached observation remains valid.

## 16. Reliability and failure containment

### 16.1 Circuit breakers

Per provider/model/tool:

- closed -> normal;
- open -> unavailable until deadline/change;
- half-open -> limited probe.

### 16.2 State recovery

Cognitive state, quota ledger, execution ledger, plan and goal state MUST survive application restart without treating incomplete work as complete.

### 16.3 Crash safety

Use existing atomic/event-sourced persistence patterns. Critical state updates must be atomic or reconstructible.

### 16.4 No infinite loops

Every retry family MUST be bounded or governed by new evidence/reset time. Repeating the same failed action without changed state/evidence is a defect.

## 17. Security and provider compliance

### 17.1 Credential isolation

Keep provider credentials in the existing protected vault. Activity logs expose only provider IDs and non-secret route metadata.

### 17.2 Zero-cost invariant

In zero-cost modes:

- unknown price = blocked;
- non-zero price = blocked;
- expired proof = blocked/requalified;
- possible paid spillover without hard stop = blocked;
- provider-side paid fallback = blocked;
- automatic credit purchase = prohibited.

### 17.3 Quota compliance

Quota exhaustion is a routing event, not an invitation to evade limits.

AlinaCoder MUST NOT automatically rotate IPs, accounts, identities, API keys, organizations, fingerprints, or proxies to regain free quota.

## 18. Evaluation framework

### 18.1 Model routing benchmark

Build a repeatable microbenchmark suite with classes:

- code repair;
- bug localization;
- test generation;
- architecture reasoning;
- instruction adherence;
- tool-call formatting;
- conversation correction;
- long-context retrieval.

Profiles are tied to:

- model ID;
- provider;
- adapter version;
- benchmark version;
- timestamp;
- sample count.

### 18.2 Agent-level metrics

Track at least:

- task success rate;
- first-pass success;
- verified completion rate;
- repeated action rate;
- stale evidence use rate;
- clarification turns per task;
- wrong-assumption correction recovery rate;
- tokens / task;
- frontier remote calls / task;
- local calls / task;
- tool calls / task;
- latency;
- provider failover success;
- zero-cost violation count (must remain 0);
- conversation replay pass rate.

### 18.3 A/B gates

New cognitive mechanisms MUST demonstrate value against the current baseline on fixed fixtures before becoming default.

Examples:

- plan-memory coupling vs isolated retrieval;
- execution ledger on/off;
- adaptive context folding on/off;
- quality-LCB router vs static hint router;
- council on/off for high-complexity fixtures.

If a complex mechanism provides no net terminal gain, keep it disabled by default.

## 19. Test strategy

All implementation follows TDD.

### 19.1 Unit tests

New suites should cover:

- intent envelope;
- causal invalidation;
- uncertainty controller;
- information-gain clarification;
- plan graph;
- plan-guided memory retrieval;
- memory-driven replanning;
- execution ledger inform/govern;
- context folding;
- history search;
- model profile updater;
- quality LCB;
- anonymous-provider policy;
- quota ledger;
- circuit breaker;
- task-aware routing;
- DeepSeek paid/free distinction;
- council gating;
- critic independence;
- skill promotion/quarantine.

### 19.2 Integration tests

Scenarios:

- Kilo anonymous free route -> quota exhausted -> another free route -> local fallback;
- paid model with higher nominal quality never selected in zero-cost mode;
- stale pricing proof blocks dispatch;
- user correction invalidates dependent plan/memory evidence;
- repeated repository read reused only under unchanged state;
- edit invalidates relevant read and test evidence;
- bug reproduction remains failing -> goal cannot complete;
- independent critic finds defect -> final verifier blocks promotion;
- restart mid-task -> exact state recovered without duplicate mutation;
- 100-turn conversation -> active constraints preserved.

### 19.3 Adversarial tests

Inject:

- misleading model metadata;
- missing pricing fields;
- provider returning a different model than requested;
- stale quota headers;
- repeated 429;
- 401/403;
- provider response claiming free while discovery says paid;
- hallucinated success text while tests fail;
- stale file reads;
- conflicting simultaneous agents;
- corrupted ledger/state record;
- semantic retry loops;
- user correction during an active run.

### 19.4 Release gates

A release cannot be READY unless:

- entire Python suite passes on supported versions;
- canonical spec validation passes;
- zero-cost policy tests pass;
- conversation replay gate passes;
- provider-fabric integration gate passes with mocked deterministic providers;
- local Ollama smoke evidence passes on release VM where applicable;
- installer self-healing gate remains green;
- desktop packaged self-test passes;
- independent final audit evidence is bound to exact commit/artifact.

Network-dependent free-provider smoke tests should be diagnostic/non-deterministic unless a stable CI credential/allowance exists; deterministic mocked contract tests remain the release authority for provider behavior.

## 20. Source/research anchors

The implementation should preserve references to authoritative/current sources in provider policy files where applicable. Research informing this design includes:

- Kilo Gateway authentication/free-model documentation: `https://kilo.ai/docs/gateway/authentication`
- Kilo model/provider routing: `https://kilo.ai/docs/gateway/models-and-providers`
- OpenRouter free router: `https://openrouter.ai/openrouter/free`
- Groq rate limits: `https://console.groq.com/docs/rate-limits`
- DeepSeek API pricing: `https://api-docs.deepseek.com/quick_start/pricing/`
- PMCoder plan-memory coupling: `https://arxiv.org/abs/2608.06811`
- Ledger execution-state layer: `https://arxiv.org/abs/2608.00808`
- SWE-MeM proactive memory: `https://arxiv.org/abs/2606.28434`
- CAT context-as-tool: ACL Findings 2026, “Context as a Tool: Context Management for Long-Horizon SWE-Agents”
- PARC self-reflective independent assessment: `https://arxiv.org/abs/2512.03549`
- MemCoder repository-history learning: `https://arxiv.org/pdf/2603.13258`

Provider facts must be revalidated during implementation because free tiers, model catalogs, limits and pricing can change.

## 21. Migration design

This is an incremental migration, not a rewrite.

### Stage A — Explicit execution and route truth

- execution ledger;
- quota ledger;
- dynamic provider/model profiles;
- Kilo anonymous free adapter/policy;
- task-aware routing;
- circuit breakers.

### Stage B — Cognitive state

- IntentEnvelope v2;
- CognitiveState;
- causal dependency/invalidation graph;
- uncertainty controller;
- improved clarification.

### Stage C — Long-horizon intelligence

- hierarchical plan graph;
- plan-guided retrieval;
- memory-driven replanning;
- proactive context folding;
- programmatic history access.

### Stage D — Deliberation and learning

- independent critic;
- council gating integration;
- richer verified experience cards;
- negative memory;
- skill reliability/quarantine.

### Stage E — Desktop and release hardening

- cognitive status UI;
- model-route explanations;
- operational trace events;
- conversation replay campaign;
- A/B benchmark gates;
- release evidence updates.

Stages are ordered to make later cognition depend on deterministic state rather than adding more LLM calls first.

## 22. Compatibility and migration invariants

During migration:

- existing public classes remain compatible unless a tested adapter is supplied;
- existing conversation tests remain green;
- existing goal/event persistence remains readable;
- existing memory DBs are migrated forward without destructive reset;
- existing SkillBook entries remain readable;
- existing provider credentials remain usable;
- existing provider atlas safety rules remain fail-closed;
- existing desktop sessions/state survive upgrade where format migration is required;
- existing installer auto-repair behavior may not regress.

## 23. Done contracts

The project phase is not complete merely because classes exist.

### Cognitive Kernel DONE

- user corrections causally invalidate only dependent state;
- long conversations preserve active constraints and verified independent work;
- uncertainty changes control behavior in tested scenarios;
- goals cannot complete on stale evidence.

### Frontier Mesh DONE

- real discovered models receive differentiated capability profiles;
- strongest eligible zero-cost route is chosen for task class;
- unknown/paid routes never leak into zero-cost mode;
- anonymous Kilo free route works when currently permitted and obeys rate limits;
- quota exhaustion produces bounded failover, never quota evasion;
- local model fallback is automatic in hybrid mode.

### Long-horizon DONE

- plan state controls retrieval;
- memory/failure state can trigger targeted replan;
- execution ledger prevents/reduces redundant actions under unchanged state;
- stale observations/evidence are not reused after relevant mutations;
- context folding preserves lossless recoverability.

### Learning DONE

- verified successful experience can be promoted;
- unverified experience is rejected;
- known bad strategies are remembered without permanent false prohibition;
- learned skills can be quarantined by poor outcomes.

### Desktop DONE

- user can see goal, phase, next action, model route, tool activity and verification state;
- no secret or hidden chain-of-thought is exposed;
- UI remains primarily a simple chat/workbench.

### Release DONE

- full deterministic tests green;
- Windows packaging/release gates green;
- exact artifact evidence bound to final commit;
- no known critical defect left open in these subsystems.

## 24. Rejected alternatives

### A. “Just add more providers”

Rejected as insufficient. It increases capacity but does not improve understanding, memory, planning or verification.

### B. “Always use a large multi-agent swarm”

Rejected as default. It wastes free quotas, increases latency and creates coordination errors. Multi-agent work remains value-gated.

### C. “Always use provider auto-router”

Rejected as primary routing policy. Provider routers are useful fallback surfaces but cannot replace AlinaCoder’s own task-aware measured quality profiles and zero-cost proofs.

### D. “Store the full chain-of-thought so the UI looks like Codex”

Rejected. The UI will expose structured operational activity, evidence, assumptions and decisions instead.

### E. “Rotate IP/accounts to evade quotas”

Rejected. This undermines reliability/compliance and is not part of AlinaCoder.

### F. “Rewrite everything around a new agent framework”

Rejected. The repository already contains useful deterministic safety, memory, goal, orchestration, installer and desktop foundations.

## 25. Final architectural invariant

The fundamental invariant is:

> AlinaCoder must always know the difference between what the user asked, what the agent currently believes, what the repository actually proves, what remains uncertain, what action is planned next, and which model/tool is the best admissible way to obtain the missing evidence.

All subsequent implementation decisions must preserve that separation.
