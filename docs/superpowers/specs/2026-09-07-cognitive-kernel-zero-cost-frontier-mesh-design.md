# AlinaCoder Cognitive Kernel + Zero-Cost Frontier Mesh — Design Specification

Date: 2026-09-07
Status: DESIGN — awaiting user review before implementation
Repository: `Rapt0r06300/alinacoder`
Baseline before design: `991bb4884296436046319e3aa7e5317ccb49674e`
Branch policy: `main` only

## 1. Mission

AlinaCoder must become a coherent long-horizon coding agent rather than a set of capable but loosely coupled subsystems. Conversation, goals, memory, planning, execution state, verification, model routing, quota control, learning and desktop observability must share explicit state and reinforce each other.

Success means measurable gains in correctness, robustness, recovery, long-session coherence and efficiency. It does not mean claiming that the agent can never fail or that a local/free model is equivalent to a frontier paid model.

Hard requirements:

1. preserve corrections, references, constraints, preferences and evolving intent across long conversations;
2. maintain an explicit machine-checkable execution state;
3. couple planning and episodic memory bidirectionally;
4. select the strongest eligible model for the exact task from measured evidence;
5. exploit legitimate free inference while never evading provider quotas or enabling paid spillover;
6. retain local Ollama as the foundational no-API-billing fallback;
7. reserve scarce frontier quota for high-value reasoning rather than routine inspection;
8. use uncertainty to control inspect / experiment / verify / escalate / ask decisions;
9. ground completion in fresh execution evidence, never model self-report alone;
10. expose a concise Codex-like operational trace without exposing hidden chain-of-thought.

## 2. Hard prohibitions

AlinaCoder MUST NOT:

- rotate IPs, proxies, accounts, identities, organizations, fingerprints or API keys to bypass rate limits or free quotas;
- impersonate new users/devices to obtain more free allocation;
- silently enable billing, auto-reload, credit purchase or pay-as-you-go;
- use unknown or stale pricing as proof of zero cost;
- treat a model/provider name as sufficient proof of quality or free status;
- persist or display hidden chain-of-thought;
- authorize destructive actions from model confidence alone;
- promote unverified generated advice into durable project memory;
- erase unrelated verified work when the user corrects one requirement.

## 3. Existing foundations that must survive

This is an incremental migration, not a rewrite.

Preserve and extend:

- `conversation/engine.py`, `advanced.py`, `models.py`, `voice.py`: RAW+MEANING, perspectives, anchors, targeted repairs, user-origin preferences, clarification cost, stable micro-turn mutation gate, context branches, failure replay;
- `goal/engine.py`, `goal/models.py`: explicit objective/criteria, stale/verified evidence, pause/resume/cancel, replanning, proof-before-impossibility;
- `memory/store.py`, `context.py`, `retrieval.py`, `planner.py`, `graph.py`, `skillbook.py`: project scoping, freshness, repository index, graph retrieval, bounded context, verified skill promotion, SQLite durability;
- `intelligence_mesh/*`: zero-cost proof, fail-closed pricing, provider/model failover, hybrid local fallback, retired-provider tombstones;
- `orchestration/core.py`: leases/fencing, semantic conflict detection, lineage-aware voting, value-gated council and multi-agent topology;
- `desktop/*`: canonical simple chat/workbench and live activity surface;
- installer/release self-healing and exact-artifact release gates.

## 4. Canonical architecture

```text
User / Voice / Desktop
        |
        v
Intent Compiler v2
        |
        v
+====================================================+
| COGNITIVE KERNEL                                   |
| Goal <-> Plan <-> Episodic Memory                  |
|   \       |       /                                |
|       Execution Ledger                             |
|              |                                     |
|      Uncertainty Controller                        |
+====================================================+
        |                         |
        v                         v
Tool/Repo Runtime          Zero-Cost Frontier Mesh
        |                  profiles / quota / health
        +-------------+-----------+
                      v
              Verification Kernel
                      |
                      v
           Evidence + Skill Learning
                      |
                      v
             Desktop Activity Trace
```

No component may turn assistant prose into proof of success.

## 5. Cognitive state and Intent Compiler v2

Add a persisted, event-reconstructible `CognitiveState` containing operational facts only:

- session/state version;
- active goal;
- intent and plan revisions;
- phase/subtask;
- active requirements, constraints and prohibitions;
- open questions and structured uncertainty;
- selected artifacts;
- verified/stale facts;
- recent failures;
- execution-ledger and memory snapshot versions;
- current model route;
- last verified repository state.

Each committed user turn produces a versioned `IntentEnvelope` with:

- raw input and normalized meaning;
- primary intent and plausible alternatives;
- references/entities;
- requirements added/changed/cancelled;
- constraints and prohibitions;
- desired result;
- continuation/priority signals;
- confidence class/provenance;
- uncertainty causes;
- source turn IDs.

LLM parsing proposes an envelope; deterministic conversation/context rules remain authoritative.

### Causal correction

Add a dependency graph from intent assumptions to plan nodes, memory hits, observations, tool results and verification evidence. A correction stales dependent descendants only. Independent verified evidence remains valid.

Example: changing “installer” to “model bridge” invalidates installer-specific hypotheses and plan nodes, but a still-current provider-atlas read can remain valid.

## 6. Clarification and uncertainty control

Replace fixed-threshold questioning with expected-information-gain control.

Decision order:

1. resolve ambiguity by cheap safe inspection when possible;
2. use a reversible sandbox probe if it resolves uncertainty safely;
3. for low-cost reversible ambiguity, act on the best-supported interpretation while exposing the assumption;
4. for high-cost ambiguity, ask the single question expected to reduce the most decision uncertainty;
5. block when required evidence cannot be obtained safely.

Track uncertainty dimensions separately: intent, repository state, factual, route/model, verification, tool effect and environment.

Controller outputs: `ACT`, `INSPECT`, `SANDBOX_PROBE`, `VERIFY`, `ESCALATE_MODEL`, `CALL_COUNCIL`, `ASK_USER`, `BLOCK`.

Numeric confidence may be used only when calibrated from observed outcomes. Otherwise use LOW/MEDIUM/HIGH plus provenance.

## 7. Hierarchical planning + bidirectional memory

Represent active work as a versioned plan graph, not only strings. Node fields include phase, subtask, dependencies, required evidence, completion predicate, affected files/symbols, expected tools, status, attempts, failure reasons and memory-query intent.

Default software-repair phases: understand, reproduce/baseline, localize, hypothesize, implement, verify, adversarial review, release/commit. Trivial tasks may collapse phases.

Memory retrieval is conditioned on goal, phase, subtask, blast radius, relevant prior failures, user constraints and current repository state. Fixed source constants must not be the sole ranking method.

Ranking combines lexical relevance, graph relationship, phase relevance, freshness, source authority, evidence validity, diversity/MMR, known-failure relevance and context cost.

Memory/failure evidence triggers targeted replanning when the agent repeats failed strategies, re-runs unchanged actions without new information, keeps failing reproduction, discovers invalidating constraints, contradicts its hypothesis or materially changes blast radius.

Completed independent plan nodes survive targeted replan.

## 8. Deterministic Execution Ledger

Canonical path: `src/alinacoder/runtime/ledger.py`.

The ledger contains no LLM-generated reasoning and requires zero additional model calls.

### Observations

Store observation ID, repository state/version, path/query/range/symbol, content/result digest, order, validity and invalidation cause.

### Modifications

Store mutated paths, before/after digests, originating tool/agent, state version and affected symbols when known. Relevant reads become stale after mutation unless exact validity can be proven.

### Commands/tool calls

Store normalized invocation, arguments, repository state, effect class, result/exit digest, duration, reuse eligibility and failure class.

### Inform boundary

Before the model acts, inject a compact view of valid observations, changes, failing tests, last verification point, repeated failures and open unknowns.

### Govern boundary

- exact repeated read-only work under unchanged relevant state may reuse the cached result;
- repeated tests under unchanged code produce a nudge, not a hard prohibition;
- a known-failed mutation strategy without new evidence triggers replanning;
- destructive effects remain subject to existing security/approval gates.

## 9. Adaptive context management

Use three tiers:

1. stable anchors: goal, active user constraints, prohibitions and definitions;
2. working memory: current phase/subtask, fresh key observations, diff/test state;
3. lossless history: complete event/tool/interaction log outside prompt context.

At phase boundaries, proactive folding may replace verbose trajectory material in working context with an actionable summary containing decision, evidence, files/symbols, rejected hypotheses, unresolved questions, verification state and source event IDs. The underlying lossless log is never deleted.

Expose programmatic history search by text, event type, file/path, failure, model/provider and step/time range, plus structured export usable by Python tooling.

Mandatory constraints and verification evidence may never be silently truncated. If they do not fit, route to an eligible larger-context model or fail explicitly.

## 10. Zero-Cost Frontier Mesh

Routing pipeline:

`Discover -> prove zero cost -> health -> capability profile -> quota -> context fit -> conservative quality -> latency/quota value -> route -> observe outcome -> update profile`.

Support authenticated free providers, documented anonymous free providers, aggregator free routers, exact free model routes and local no-API-billing routes.

### Kilo anonymous bridge

Current Kilo documentation states that free `:free` models may be used anonymously and that free traffic is limited by IP. Implement a zero-configuration anonymous Kilo route only while current provider evidence still proves this behavior.

Rules:

- no fake authentication;
- no IP/quota evasion;
- obey 429 and reset/cooldown;
- anonymous and authenticated Kilo routes are distinct;
- pricing/discovery is requalified before dispatch;
- exhaustion immediately routes elsewhere;
- explicit profiled free models outrank `kilo-auto/free` when AlinaCoder has stronger task-fit evidence; `kilo-auto/free` remains a useful fallback.

### OpenRouter

Discover exact free models and profile them independently. Use provider generic free routing as fallback only when zero cost is proven and paid fallback is impossible.

### Groq and other hard-stop free tiers

Use only after the account/plan proves no paid spillover. Consume reset/remaining headers into the quota ledger when available.

### DeepSeek

The official DeepSeek API is treated as paid unless current authoritative evidence explicitly proves otherwise. DeepSeek-family routes are allowed only through a currently proven zero-price third-party route or local execution. The name “DeepSeek” never implies “free.”

### Local model ladder

Benchmark machine resources and maintain, when hardware allows:

- strongest stable local coding model;
- fast local utility model;
- CPU-safe fallback.

Measure memory fit/headroom, context capacity, prompt/generation throughput, simple code repair, tool following and repeated-inference stability. No model name is permanently hardcoded as “best.”

## 11. Measured model capability profiles

Add `ModelCapabilityProfile` dimensions for code generation, debugging, repository reasoning, architecture, tool-use reliability, instruction following, long-context stability, conversational repair, summarization, speed, failure rate, context window, freshness and sample count.

Evidence order:

1. current AlinaCoder outcome observations;
2. AlinaCoder microbenchmarks;
3. provider metadata;
4. versioned seed priors.

Fresh measured evidence dominates stale priors.

### Conservative quality score — fixed design

For each task capability, benchmark outcomes are stored as success/failure trials. The route’s primary `quality_lcb` is the **95% Wilson score lower bound** for that capability.

- before 5 measured trials, use a versioned seed prior but apply a cold-start penalty so an unmeasured model cannot outrank a strongly proven model solely from a name/prior;
- at 5+ trials, Wilson LCB is the primary observed success score;
- graded secondary signals may break ties but cannot override failure of a mandatory capability requirement;
- profiles expire/revalidate when model ID/version, provider behavior or benchmark version changes.

This removes the current “all discovered models default to 0.5” weakness from production routing.

## 12. Task-aware routing and quota ledger

Classify inference calls into capability classes such as conversation, intent resolution, planning, repository search, architecture, code generation, debugging, review, verification analysis, summarization and research synthesis. Use deterministic classification first and model escalation only when necessary.

Persist a `QuotaLedger` containing known RPM/RPD/TPM/TPD, remaining requests/tokens, reset timestamps, 429/402/403/5xx history, cooldown, latency, success/failure counts, discovery time and cost-proof expiry.

States: AVAILABLE, DEPLETED_UNTIL_RESET, TEMP_UNHEALTHY, AUTH_BLOCKED, BILLING_BLOCKED, RETIRED, UNKNOWN.

Error policy:

- 429 -> record reset/cooldown and route elsewhere;
- 402 -> hard block;
- 401/403 -> disable until credentials/account state changes;
- 5xx/network -> bounded retry + circuit breaker;
- malformed response -> health penalty/failover;
- semantic failure -> do not blindly retry identical strategy/prompt/model lineage.

Scarce high-quality free calls may be reserved for architecture, hard debugging, adversarial review and release-critical decisions while local/cheaper routes perform routine indexing and summarization.

## 13. Multi-model cognition

For difficult/high-criticality work use primary + independent critic:

1. primary proposes plan/hypothesis/patch;
2. critic from an independent lineage receives task contract, evidence and proposed result — never private hidden reasoning;
3. critic returns defects, missing tests, contradictions or PASS/INCONCLUSIVE;
4. deterministic verification remains final authority.

Existing lineage-aware aggregation stays mandatory. Same underlying model served by multiple providers counts as one cognitive lineage.

Council is value-gated using criticality, uncertainty, disagreement, repeated failures, blast radius, latency and quota cost. Simple work stays single-model/local.

## 14. Verification Kernel

A plan node or goal criterion completes only from fresh evidence bound to the relevant repository state.

Evidence includes test invocation/result, fail-before/pass-after reproduction, compilation/static analysis, independent verifier output, artifact hashes/provenance and packaged smoke tests.

When a bug is reproducible, reproduction becomes a first-class gate. A patch cannot be “fixed” while the latest valid reproduction still fails.

Any edit affecting a proven surface stales dependent evidence until rerun. Stale green tests cannot certify later state.

High-criticality release/installer/security work should combine independent review with deterministic proof.

## 15. Verified learning and negative memory

Extend `SkillBook` experience cards with problem signature, scope, strategy, preconditions, failed alternatives, evidence IDs, state/commit binding, revalidation policy and outcome statistics.

Promotion requires verified outcome, evidence, project scoping and no conflict with protected governance. Human acceptance is a strong signal but executable proof remains required when available.

Store failed strategies with the conditions under which they failed. They prevent loops but are not permanent prohibitions; changed state/new evidence can reopen them.

Track learned-skill outcomes. Poor skills are quarantined, never silently deleted.

## 16. Conversation robustness campaign

Build a deterministic/model-assisted replay corpus covering corrections, pronouns/artifact anchors, multiple-selection ambiguity, continue-after-restart, “do the same,” negation, scope/priority changes, voice interruption, partial ASR, noisy French, mixed French/English technical language, stale references, old commit vs current state, messages arriving during long work, subtask stop vs full stop, undo, 100+ turn constraint retention, false-memory rejection and causal invalidation.

Milestones:

- first implementation stage: hundreds of generated variations;
- release target: at least 1,000 retained replay cases;
- every discovered real failure becomes a regression fixture when safely reproducible.

## 17. Desktop — simple chat, rich operational trace

Chat remains primary. Add compact operational surfaces for:

- active goal;
- current phase;
- next action;
- blocker;
- verification state;
- selected provider/model.

Live activity shows structured events: interpretation/assumption update, plan/replan, repository search/read, test, patch, verify, route selection, quota failover, critic/council, recovery, evidence pass/fail, commit/release.

For each inference call expose provider, model, task class, zero-cost proof state and concise route reason such as “best verified debugging LCB among available zero-cost routes.” Never expose credentials, auth headers or hidden chain-of-thought.

## 18. Performance strategy

Deterministic fast paths handle exact state lookup, known paths, ledger reuse, hashes, quota checks and basic routing without model calls.

Preferred expensive-call flow:

1. deterministic/local inspection;
2. local/cheap context preparation;
3. frontier reasoning/code/review only when valuable;
4. deterministic execution;
5. deterministic verification;
6. frontier revisit only if evidence fails or uncertainty remains.

All caches are state-bound and invalidated by relevant repository changes.

## 19. Reliability and recovery

Use per-route circuit breakers with CLOSED / OPEN / HALF_OPEN states.

Cognitive state, quota ledger, execution ledger, plan, memory and goal state survive restart without treating interrupted work as complete. Critical writes use existing atomic/event-sourced persistence patterns.

Every retry is bounded or waiting for a documented state/reset change. Repeating the same failed action with unchanged evidence is a defect and triggers replan.

## 20. Evaluation and A/B gates

Track:

- task and first-pass success;
- verified completion;
- repeated action rate;
- stale evidence use rate;
- clarification turns;
- correction-recovery success;
- tokens/frontier calls/local calls/tool calls per task;
- latency;
- failover success;
- zero-cost violations (must be 0);
- conversation replay pass rate.

Build versioned microbenchmarks for code repair, localization, tests, architecture, instruction following, tool calls, conversational repair and long-context retrieval.

A/B test plan-memory coupling, ledger, adaptive folding, Wilson-LCB routing and council activation against current baselines. A complex mechanism that cannot prove net terminal value remains disabled by default.

## 21. TDD and release gates

Implementation is test-first.

Unit suites cover intent envelopes, causal invalidation, uncertainty control, clarification, plan graph, plan-memory coupling, ledger, folding/history search, profiles/Wilson LCB, anonymous provider policy, quota ledger, circuit breakers, task routing, DeepSeek paid/free distinction, council/critic independence and skill quarantine.

Integration scenarios include:

- Kilo anonymous free -> quota exhaustion -> another legitimate free route -> local fallback;
- higher-quality paid model never selected in zero-cost mode;
- stale price proof blocks dispatch;
- user correction invalidates only dependent plan/evidence;
- repeated read reused only under unchanged state;
- edit invalidates relevant reads/tests;
- failing reproduction blocks completion;
- critic defect blocks promotion until resolved;
- restart mid-task avoids duplicate mutation;
- 100-turn constraints remain active.

Adversarial tests inject misleading model metadata, missing prices, wrong returned model, stale quota data, repeated 429, 401/403, 5xx, hallucinated success, stale reads, conflicting agents, corrupted persisted state and semantic retry loops.

Release cannot be READY unless the full Python suite, canonical spec, zero-cost policy, conversation replay, provider fabric, local Ollama/release smoke where applicable, installer self-healing, packaged desktop self-test and independent final artifact-bound audit are green.

External free-provider live checks are diagnostic unless deterministic CI entitlement is available; mocked contract tests remain release authority for provider behavior.

## 22. Migration order

### Stage A — deterministic truth and routing

Execution ledger, quota ledger, measured profiles, Kilo anonymous policy/adapter, task-aware routing, circuit breakers.

### Stage B — cognitive state

IntentEnvelope v2, CognitiveState, causal invalidation, uncertainty controller, clarification policy.

### Stage C — long-horizon intelligence

Plan graph, plan-guided retrieval, memory-driven replan, proactive folding, programmatic history access.

### Stage D — deliberation and learning

Independent critic, council integration, richer verified experience, negative memory, reliability/quarantine.

### Stage E — desktop and release hardening

Cognitive status UI, route explanations, activity events, 1,000+ conversation replays, A/B gates and release evidence.

Order is intentional: sophisticated cognition must depend on deterministic current state before more LLM calls are added.

## 23. Compatibility invariants

During migration:

- preserve existing public behavior or provide tested adapters;
- keep existing conversation/goal/state records readable;
- migrate memory/SkillBook forward without destructive reset;
- preserve provider credentials and fail-closed safety;
- preserve desktop state/session compatibility where format migrations are needed;
- preserve installer self-healing and current release gates.

## 24. Done contracts

### Cognitive Kernel DONE

- corrections causally invalidate only dependent state;
- long conversations preserve active constraints and unrelated verified work;
- uncertainty changes behavior in tests;
- stale evidence cannot complete goals.

### Frontier Mesh DONE

- real discovered models receive differentiated measured profiles;
- task-specific strongest eligible zero-cost route wins by conservative evidence;
- unknown/paid routes never leak into zero-cost mode;
- Kilo anonymous route functions only when current policy allows it and obeys limits;
- exhausted routes fail over without quota evasion;
- hybrid mode automatically reaches local fallback.

### Long-horizon DONE

- plan controls retrieval;
- memory/failure evidence can trigger targeted replan;
- ledger prevents/reduces redundant work under unchanged state;
- stale observations/evidence never survive relevant mutation;
- folding remains losslessly recoverable.

### Learning DONE

- verified success promotes;
- unverified memory is rejected;
- negative memory prevents loops without creating permanent false bans;
- poor learned skills can be quarantined.

### Desktop DONE

- goal, phase, next action, model route, tool activity and verification state are understandable live;
- UI stays primarily a simple chat/workbench;
- no secret or hidden chain-of-thought is exposed.

### Release DONE

- deterministic suites and Windows packaging/release gates are green;
- exact evidence is bound to the final commit/artifacts;
- no known critical defect remains open in these subsystems.

## 25. Research/source anchors

Provider facts are revalidated during implementation because catalogs, pricing and limits change.

- Kilo anonymous/free authentication: `https://kilo.ai/docs/gateway/authentication`
- Kilo usage/billing and free rate limits: `https://kilo.ai/docs/gateway/usage-and-billing`
- Kilo models/auto free: `https://kilo.ai/docs/gateway/models-and-providers`
- OpenRouter free router: `https://openrouter.ai/openrouter/free`
- Groq rate limits: `https://console.groq.com/docs/rate-limits`
- DeepSeek API pricing: `https://api-docs.deepseek.com/quick_start/pricing`
- PMCoder plan-memory coupling: `https://arxiv.org/abs/2608.06811`
- Execution Ledger: `https://arxiv.org/abs/2608.00808`
- SWE-MeM proactive memory: `https://arxiv.org/abs/2606.28434`
- Context as a Tool: `https://arxiv.org/abs/2512.22087`
- PARC independent self-assessment: `https://arxiv.org/abs/2512.03549`
- MemCoder repository-history learning: `https://arxiv.org/abs/2603.13258`

## 26. Rejected alternatives

- **Only add providers:** more capacity, not enough intelligence.
- **Always use a large swarm:** wastes quota and adds coordination failure; councils remain value-gated.
- **Always trust provider auto-routing:** useful fallback, not a substitute for AlinaCoder’s measured task-specific profiles.
- **Show full internal reasoning:** rejected; expose structured operational trace/evidence instead.
- **Quota evasion by IP/account rotation:** rejected for reliability/compliance.
- **Rewrite around a new framework:** rejected; current deterministic foundations are valuable.

## 27. Final invariant

> AlinaCoder must always know the difference between what the user asked, what the agent currently believes, what the repository actually proves, what remains uncertain, what action is planned next, and which model/tool is the best admissible way to obtain the missing evidence.

Every implementation decision must preserve that separation.
