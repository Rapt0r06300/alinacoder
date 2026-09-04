# AlinaCoder v0.2 — Autonomous Frontier Routing & Seamless Handoff Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment strengthens the existing Zero-Cost Intelligence Mesh into an autonomous, continuously self-measuring routing fabric capable of discovering, enrolling, ranking, switching and recovering across heterogeneous LLM engines without losing the user's intent, repository state or verified progress.

It is normative together with:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`

This amendment has higher precedence for:

- autonomous discovery of free LLM routes;
- provider enrollment and credential health;
- model/provider ranking and promotion;
- champion/challenger routing;
- provider and model failover;
- context mobility and model handoff;
- mid-stream recovery;
- continuity verification;
- quota portfolio management;
- provider circuit breaking and health routing;
- routing-learning state;
- automatic adoption of newly available stronger free models.

All earlier safety, intent, memory, verification, resource, Git and zero-cost invariants remain in force.

The monetary invariant is absolute:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAID_FALLBACK = false
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
```

The central rule is:

> **Portable state, replaceable models, verified progress. Use the strongest proven zero-cost intelligence available for the current task, but never allow a model, provider, gateway or conversation transcript to become the source of truth.**

---

# Part I — Definition of “strongest”

## 2. “Most powerful” is task-specific

AlinaCoder must never equate “most powerful” with:

- largest parameter count;
- newest release;
- provider marketing;
- public leaderboard rank alone;
- one global Elo score;
- one benchmark;
- one gateway's preferred model;
- one model's self-reported confidence.

For AlinaCoder, the strongest route is the eligible route with the highest evidence-backed probability of successfully completing the **current stage of the current task** while preserving all invariants.

Selection is lexicographic rather than a single opaque weighted score:

```text
1. policy / safety / permission eligibility
2. proven zero monetary cost for this exact call
3. privacy and use-scope eligibility
4. context / modality / tool-schema capability fit
5. predicted verified task-success lower confidence bound
6. handoff and structured-output reliability
7. provider health and quota health
8. latency / resource efficiency among near-equal candidates
```

A route that fails an earlier layer is not rescued by being strong on a later layer.

## 3. External rankings are priors, never verdicts

Provider catalogs, Artificial Analysis-style indices, OpenRouter coding/agentic/intelligence sorting, published SWE-Bench results, model cards and community benchmarks may seed a prior.

They may not directly promote a model to `CHAMPION`.

AlinaCoder's final routing belief must be execution-grounded using repeated mini-tasks, real project outcomes, deterministic tests and regression evidence on the user's actual machine and workflows.

---

# Part II — Autonomous Zero-Cost Frontier Discovery

## 4. FreeRouteDiscoveryEngine

A `FreeRouteDiscoveryEngine` continuously maintains the candidate universe.

It discovers routes from:

1. official provider model/pricing/quota APIs;
2. official provider model catalogs;
3. official release notes, RSS or changelogs;
4. official model metadata endpoints;
5. known gateway `/models` endpoints;
6. curated third-party directories only as **leads** requiring official re-verification;
7. local Ollama/llama.cpp/LM Studio inventories;
8. new compatible OpenAI-style endpoints explicitly configured by the user.

Third-party lists can create `DISCOVERED` candidates only. They cannot prove price, privacy, entitlement or production eligibility.

### 4.1 Discovery cadence

Refresh occurs:

- on AlinaCoder startup when provider evidence is stale;
- at least daily while active;
- after a provider 404/model-not-found;
- after a pricing or quota mismatch;
- after authentication changes;
- after repeated provider degradation;
- when a provider's model catalog hash changes;
- when release feeds announce new models;
- before reusing a route whose cost proof has expired.

Refresh work is lightweight and resource-budgeted. It must not keep a large local model resident.

## 5. FrontierDriftDetector

`FrontierDriftDetector` compares the latest provider/model universe with the previous signed snapshot.

It emits typed changes:

```text
MODEL_ADDED
MODEL_REMOVED
MODEL_RENAMED
PRICE_CHANGED
FREE_STATUS_CHANGED
RATE_LIMIT_CHANGED
CONTEXT_CHANGED
CAPABILITY_CHANGED
TERMS_SCOPE_CHANGED
PRIVACY_CHANGED
PROVIDER_DEGRADED
PROVIDER_RECOVERED
```

A stronger-looking new model is not immediately trusted. It enters the canary pipeline.

A model whose price/free status becomes ambiguous is quarantined **before another inference call**.

## 6. Provider-route lifecycle

The route lifecycle becomes:

```text
DISCOVERED
  ↓
OFFICIAL_COST_PROOF
  ↓
ENROLLMENT_READY
  ↓
AUTH_PROBE
  ↓
CAPABILITY_PROBE
  ↓
CANARY
  ↓
PROBATION
  ↓
ELIGIBLE
  ↓
CHAMPION or SPECIALIST
```

Negative/temporary states:

```text
UNENROLLED
UNPROVEN_FREE
RATE_LIMITED
QUOTA_EXHAUSTED
DEGRADED
QUARANTINED
TERMS_CHANGED
PRIVACY_INELIGIBLE
PAID_OR_UNPROVEN
RETIRED
```

No route may skip `OFFICIAL_COST_PROOF` for remote inference.

---

# Part III — Provider enrollment without brittle browser hacks

## 7. ProviderEnrollmentBroker

`ProviderEnrollmentBroker` automates every supported step while respecting provider authentication and terms.

Enrollment states:

```text
NO_AUTH_REQUIRED
OFFICIAL_API_KEY_REQUIRED
OFFICIAL_OAUTH_AVAILABLE
OFFICIAL_DEVICE_FLOW_AVAILABLE
USER_ENROLLMENT_REQUIRED
CONNECTED
EXPIRED
REVOKED
```

### 7.1 What “automatic connection” means

After a supported one-time enrollment, AlinaCoder should reconnect, probe, rotate among eligible models and fail over without requiring the user to choose a model manually.

AlinaCoder may automatically use no-auth routes immediately when their terms permit it.

Where an account, API key, CAPTCHA, MFA, identity verification or acceptance of terms is required, AlinaCoder must not pretend it can legally or reliably create/authorize the account itself. It may open the official enrollment flow and ask for the minimum one-time user action.

### 7.2 Credential rules

Secrets must:

- be stored in Windows Credential Manager or an equivalent OS-protected key store;
- never be committed to Git;
- never be copied into ordinary logs;
- never be put into shared model context;
- be referenced by opaque credential IDs;
- be health-checked without exposing values;
- be deleted on explicit disconnect.

Forbidden enrollment methods include:

- scraping browser cookies;
- extracting hidden session tokens;
- reverse engineering private endpoints;
- bypassing CAPTCHA/MFA;
- automatically accepting changed legal terms;
- creating multiple accounts to evade quotas;
- key farming or IP/account rotation to bypass fair-use limits.

---

# Part IV — Live zero-cost proof

## 8. ZeroCostAdmissionGate v2

Every remote inference request, including fallbacks, challengers, verifier calls, background tasks and hidden canaries, passes `ZeroCostAdmissionGate` immediately before transmission.

The gate verifies:

```text
provider connected or legitimately no-auth
AND model currently exists
AND exact route price == 0 for the current entitlement
AND current free quota > predicted request requirement
AND no paid overage can activate
AND no paid balance will be consumed
AND use-scope permits the task
AND privacy class permits the payload
AND route is not quarantined
```

If any element is unknown:

```text
DO_NOT_CALL
```

Unknown is not free.

### 8.1 Payment-method isolation

When practical, AlinaCoder should prefer provider accounts/tiers with no payment method attached because they make accidental overage structurally impossible.

If a provider free tier exists inside an account that can also bill, the route remains ineligible unless the provider exposes a machine-verifiable hard spending cap or an equivalent mechanism proving the call cannot incur a charge.

Promotional credits that can silently roll into billable usage are not treated as free autonomous capacity.

---

# Part V — 2026-09-04 provider baseline

## 9. Provider classes are a dated bootstrap, not permanent truth

The following is a research bootstrap as of 2026-09-04. Runtime evidence has precedence.

### 9.1 Renewable / standing zero-cost candidates

Subject to live entitlement and quota verification:

- **Local Ollama/open-weight inference** — unlimited monetary cost of inference on owned hardware; machine resource limits still apply.
- **Google Gemini Free Tier** — currently exposes multiple zero-price free-tier models; exact model IDs and limits must be queried live.
- **Groq Free Plan** — official free limits currently include `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.6-27b` and `qwen/qwen3.8-27b`, subject to account-specific current limits.
- **SambaNova Cloud Free Tier** — official no-payment-method free tier currently exposes large models including GPT-OSS, DeepSeek and Gemma with strict daily limits.
- **Mistral Studio Free mode** — free API mode with current usage/rate limits; catalog must be probed live.
- **OpenRouter `:free` routes** — rotating zero-price model variants and `openrouter/free`; model availability and free-request limits change frequently.
- **Kilo Gateway free routes** — `kilo-auto/free` and explicit `:free` models; gateway currently supports no-auth free inference with rate limiting and server-side rotating model mappings.
- **Z.AI zero-price Flash routes** — only models whose official current pricing is exactly zero.
- **Cloudflare Workers AI Free allocation** — free Workers accounts receive a daily Neuron allowance and cannot overrun into Workers AI charges without upgrading; current catalog includes GPT-OSS and Qwen families.
- **Ollama Cloud Free starter usage** — only models and monthly starter allowance proved free for the current account.

### 9.2 Development / evaluation-only zero-cost routes

These can be excellent specialist brains but their license/use scope must be honored:

- **NVIDIA NIM Developer Program hosted endpoints** — NVIDIA documents free hosted NIM API access for prototyping, research, development and testing during Developer Program membership; not a production entitlement.
- **Cohere evaluation keys** — free but usage-limited and intended for evaluation/development.
- **ModelScope API-Inference** — candidate free shared inference with account/identity prerequisites; runtime enrollment and official quota proof are required before eligibility.

### 9.3 Micro-credit / tiny free allowance

- **Hugging Face Inference Providers** free-account monthly credit.
- any provider whose free entitlement is a small hard-capped, non-billable allowance.

These routes should normally be saved for canaries or specialist tasks where their measured marginal value is high.

### 9.4 Discovery-only / unproven

OpenCode Zen, Together zero-price promotions, Requesty, Venice, SiliconFlow, Chutes, OVH endpoints and other newly discovered gateways/providers may be investigated automatically, but they stay `UNPROVEN_FREE` until official current evidence and account-level probes pass.

### 9.5 Trial-only / excluded from autonomous standing capacity

- **Cerebras Inference** — current official documentation describes a $5, 30-day Free Trial requiring a verified payment method and explicitly states there is no permanent free tier. It therefore remains outside the standing zero-cost pool.
- time-limited Alibaba Model Studio promotional quotas and similar trial credits are not permanent capacity.
- any route that can continue as pay-as-you-go after the free credit expires is excluded unless hard-blocked before billing.

### 9.6 Retired

- **GitHub Models** — retired 2026-07-30; never probe as an active provider unless GitHub later announces a distinct supported successor.

---

# Part VI — Model identity, mirrors and failure domains

## 10. ModelLineageGraph

A model is not identified only by provider/model string.

`ModelLineageGraph` stores:

```text
model_family
model_version
base_lineage
provider
provider_route
checkpoint_or_digest_if_known
quantization
reasoning_mode
context_mode
tool_schema_profile
vision_profile
license_scope
privacy_profile
```

The same GPT-OSS checkpoint on Groq, Cloudflare, SambaNova, OpenRouter and Kilo is one cognitive lineage with multiple hosting routes.

### 10.1 Why mirrors still matter

Mirrors are valuable for **availability** even when they do not add cognitive diversity.

AlinaCoder distinguishes:

```text
COGNITIVE_DIVERSITY
HOSTING_REDUNDANCY
```

For a provider outage, same-model/different-provider failover is preferred because behavior and handoff burden are lower.

For a reasoning failure, a different model family is preferred because it may provide complementary errors and strategies.

## 11. FailureDomainGraph

Routes also carry failure-domain relationships:

- same gateway;
- same upstream provider;
- same model family;
- same geographic region if known;
- same authentication account;
- same quota pool.

Fallback chains should maximize independence where it matters. Two “different” endpoints behind one gateway are not considered independent against gateway failure.

---

# Part VII — Execution-grounded routing intelligence

## 12. TaskFingerprint

Every meaningful model call receives a structured `TaskFingerprint` containing at least:

```text
intent_class
task_stage
repo_languages
frameworks
change_risk
required_tools
required_modalities
context_size
expected_output_schema
failure_signature
complexity
uncertainty
privacy_class
resource_state
similar_experience_ids
```

Routing happens at stage granularity rather than once for an entire user request.

## 13. RoutePosterior

For every useful tuple:

```text
(TaskFingerprint cluster, model lineage, provider route, reasoning mode, scaffold topology)
```

AlinaCoder maintains execution-grounded statistics:

- verified success posterior;
- lower confidence bound;
- sample count;
- recency;
- regression rate;
- structured-output validity;
- tool-call validity;
- context-retention score;
- handoff success by direction/source;
- first-token and completion latency;
- rate-limit frequency;
- provider failure frequency;
- quota consumption;
- verifier catch rate;
- failure signatures.

## 14. ChampionChallengerRegistry

There is no permanent global best model.

There are champions by task cluster and stage:

```text
intent_champion
repo_localization_champion
architecture_champion
patch_champion
debug_champion
test_generation_champion
regression_review_champion
research_champion
long_context_champion
vision_champion
```

New candidates enter as challengers.

Promotion requires sufficient execution evidence. A challenger should beat the current champion's conservative success estimate or deliver comparable verified quality with materially better quota availability/latency/resource behavior.

Demotion can happen automatically after:

- repeated verified failures;
- new regressions;
- increased malformed output;
- stale capability profile;
- provider degradation;
- free-tier reduction;
- model replacement under an unchanged alias.

## 15. Safe online learning

Routing may use contextual-bandit-inspired exploration such as Thompson sampling or confidence-bound methods, but exploration is risk-bounded.

Rules:

- critical/high-impact work defaults to certified champions;
- challengers first receive synthetic canaries, hidden evals or low-risk subtasks;
- exploration never bypasses the Done Contract;
- a small exploration budget prevents the router from becoming stale;
- no single success is sufficient for promotion;
- routing memory uses real verified outcomes, not model self-ratings.

---

# Part VIII — Quota as a portfolio

## 16. QuotaPortfolioManager

Free quotas are scarce renewable resources and must be managed as a portfolio.

Track separately per route:

```text
RPM
RPD
TPM
TPD
monthly_tokens
credits
neurons
concurrency
reset_time
remaining_estimate
confidence_in_estimate
```

The manager reserves scarce high-value capacity for difficult bottleneck reasoning.

Examples:

- local model for deterministic extraction or simple formatting;
- fast Groq route for short reasoning when measured strong enough;
- rare 1M-context free route for repository-scale synthesis;
- independent high-end route for adversarial verification;
- tiny Hugging Face credit only when it adds unique value.

Quota exhaustion produces `QUOTA_EXHAUSTED` and a known reset time, not repeated failing calls.

## 17. Quota anti-abuse rule

AlinaCoder must never increase capacity by evading provider rules through:

- multiple throwaway accounts;
- rotating IPs to bypass per-IP limits;
- generating duplicate keys solely to bypass shared quotas;
- misrepresenting request origin;
- using credentials belonging to other users without explicit authorization.

---

# Part IX — Adaptive orchestration, not just model routing

## 18. ScaffoldGainProfile

Research shows that manager-worker or multi-agent scaffolds can strongly help some models and harm others. Therefore AlinaCoder benchmarks orchestration topology per model/task family.

Candidate modes:

```text
DIRECT
PLAN_THEN_ACT
PLANNER_IMPLEMENTER
MANAGER_WORKER
PARALLEL_CANDIDATES
CRITIC_REPAIR
ADVERSARIAL_VERIFY
SELECTIVE_DEBATE
HYBRID_DAG
```

A model may be champion in direct patching but weak as a manager, or vice versa.

## 19. TopologyRouter

The task dependency graph determines whether work should run sequentially, in parallel, hierarchically or hybrid.

Dense “ask every model everything” swarms remain forbidden by default.

For hard tasks, use the smallest diverse set that has demonstrated complementarity.

`RouteGainCertificate` remains mandatory before a recurring ensemble is considered superior to the best relevant single-route baseline.

---

# Part X — Continuity Spine: the source of truth across models

## 20. No-loss-of-thread definition

“No loss of thread” does **not** mean copying the full raw transcript into every new model.

It means preserving all state that can change the correct next action:

- current user intent;
- corrections and superseded instructions;
- project identity;
- repository HEAD and workspace state;
- accepted decisions;
- hard constraints;
- active plan and current stage;
- verified evidence;
- failed/disproven approaches;
- candidate patch state;
- pending actions;
- success criteria;
- rollback point.

## 21. CanonicalSessionState

Model-independent state is persisted in a `ContinuitySpine`.

Conceptual record:

```text
session_id
state_version
intent_contract
conversation_repair_graph
active_project
repo_path
head_sha
working_tree_fingerprint
diff_sha
active_plan_id
task_dag
current_stage
current_subtask
accepted_decisions
hard_constraints
forbidden_actions
success_definition
active_files_and_symbol_hashes
verified_evidence_refs
verified_test_results
disproven_hypotheses
candidate_artifact_refs
pending_actions
rollback_checkpoint
provider_history
model_history
resource_state
freshness_map
created_at
updated_at
state_checksum
```

`state_version` is monotonic.

The checksum covers the canonical serialized state.

## 22. Event-sourced session history

The Continuity Spine should use an append-only local event log plus materialized snapshots.

Events include:

```text
USER_TURN_ACCEPTED
USER_CORRECTION_APPLIED
INTENT_CONTRACT_UPDATED
TOOL_CALL_STARTED
TOOL_CALL_FINISHED
PATCH_CANDIDATE_CREATED
TEST_RESULT_VERIFIED
HYPOTHESIS_REJECTED
DECISION_ACCEPTED
MODEL_SWITCH_REQUESTED
MODEL_SWITCH_COMMITTED
PROVIDER_FAILURE
ROLLBACK_COMPLETED
```

This allows deterministic reconstruction after crash, restart or model switch.

Raw conversation remains preserved separately for provenance but is not automatically injected into every model.

## 23. VerifiedSharedContext

Shared state visible to future models contains compact **verified gists**, not unrestricted model claims.

Every reusable gist records:

- claim;
- supporting evidence reference;
- verifier result;
- freshness/version;
- originating model/route;
- whether it is a fact, decision, hypothesis, failure or constraint.

Unverified model prose never silently becomes project truth.

The system supports hierarchical unfolding:

```text
compact gist
  ↓ when needed
reference-grounded summary
  ↓ when needed
raw evidence / file / tool output
```

This preserves detail without flooding every context window.

---

# Part XI — Direction-aware seamless handoff

## 24. Handoff is a separate optimization problem

Routing decides **who acts next**.

Handoff decides **what the receiver inherits**.

They are optimized separately.

Recent coding-agent evidence shows a “handoff tax”: a stronger model can be harmed by inheriting a weaker model's full trajectory, while a weaker receiver can benefit from preserving more of a stronger sender's useful plan/context.

Therefore full raw-history transfer is not the default.

## 25. HandoffEnvelope

Every cross-model switch creates a provider-neutral typed envelope containing:

```text
handoff_id
switch_reason
switch_direction
source_model_lineage
target_model_lineage
canonical_state_version
canonical_state_checksum
intent_contract
active_project
repo_head_sha
working_tree_fingerprint
current_stage
current_subtask
accepted_decisions
hard_constraints
success_definition
relevant_verified_gists
relevant_code_evidence
current_candidate_artifacts
verified_test_results
known_failed_approaches
pending_actions
rollback_checkpoint
requested_output_contract
freshness_hashes
```

The envelope is generated locally from canonical state, never by trusting the outgoing model to summarize itself as the sole source.

## 26. DirectionAwareHandoffPolicy

### 26.1 `ESCALATE_WEAK_TO_STRONG`

When switching because the current model appears too weak:

- retain repository/workspace state;
- retain user intent and hard constraints;
- retain verified facts/tests/errors;
- retain complete accepted artifacts;
- retain disproven hypotheses as compact facts;
- strip most speculative weak-model reasoning;
- avoid forwarding long dead-end trajectories;
- let the stronger model independently reconstruct its strategy from evidence.

### 26.2 `DOWNSHIFT_STRONG_TO_FAST`

When a strong model completed hard reasoning and a faster/lighter model will execute routine work:

- retain the strong model's **accepted and verified** plan structure;
- retain architectural rationale that constrains implementation;
- retain important edge cases and invariants;
- compact but do not discard useful high-capability guidance.

### 26.3 `PEER_SWITCH`

For similar-capability but cognitively different families:

- transfer canonical state;
- transfer accepted decisions and evidence;
- transfer only concise rationale required to avoid repeating work;
- avoid speculative chain-of-thought inheritance.

### 26.4 `MIRROR_SWITCH`

For the same model lineage on another provider:

- keep the same canonical envelope;
- provider-native session/cache reuse may be attempted if officially supported;
- correctness never depends on provider-native state.

### 26.5 `RECOVERY_SWITCH`

After malformed output, crash or failed patch:

- start from the last verified checkpoint;
- include exact failure evidence;
- exclude incomplete model output from canonical facts;
- require a new next-action proposal before mutations resume.

## 27. HandoffFormatRouter

Typed state is the default for code/workflow continuity.

A concise natural-language supplement may be added when ambiguity, architecture or creative synthesis benefits from it.

Neither an unstructured transcript-only handoff nor a graph-only handoff is mandated universally.

The format is selected and benchmarked per task/model pair.

---

# Part XII — Atomic model switch protocol

## 28. Safe switch checkpoints

Prior anti-oscillation rules remain binding.

A model switch is forbidden during:

- file write;
- patch application;
- Git commit/ref mutation;
- database/memory transaction;
- non-idempotent tool side effect;
- unresolved partial structured output;
- active recovery rollback;
- unstable speech/intent boundary.

## 29. ModelSwitchTransaction

A switch is a transaction:

```text
1. acquire mutation barrier
2. stop scheduling new mutating tool calls
3. finish or safely cancel in-flight provider call
4. commit all completed deterministic tool results
5. discard incomplete/unparseable generation tails
6. flush ContinuitySpine event log
7. snapshot CanonicalSessionState
8. verify repo HEAD / working-tree / artifact hashes
9. classify handoff direction and reason
10. rank eligible target routes
11. run ZeroCostAdmissionGate for target
12. build HandoffEnvelope
13. establish target provider/model session
14. run ContinuityProof
15. ask target for dry next-action proposal without mutation
16. verify proposal against IntentContract and current repo state
17. commit MODEL_SWITCH_COMMITTED event
18. release mutation barrier
19. resume work
```

If any step fails, the switch does not partially commit.

The system either reuses the previous healthy model at the same checkpoint or tries the next eligible target.

## 30. ContinuityProof

Before an incoming model may mutate anything, it must produce a compact structured acknowledgement of:

```text
canonical_state_version
state_checksum
user_goal
active_project
repo_head_sha
current_stage
current_subtask
hard_constraints
known_failed_approaches
success_definition
proposed_next_action
```

The deterministic controller compares these fields with canonical state.

Mismatch response:

```text
REHYDRATE_MORE_EVIDENCE
  ↓
retry ContinuityProof
  ↓ if still wrong
REJECT_ROUTE_FOR_THIS_HANDOFF
```

A model that cannot correctly rehydrate the task is not allowed to “just continue.”

---

# Part XIII — Mid-stream failures without corruption

## 31. Incomplete model output is not state

If a provider stream dies halfway through JSON, a patch, a plan or code:

- incomplete tail is tagged `INCOMPLETE_GENERATION`;
- it is not admitted into verified shared context;
- it is not applied to files;
- it is not handed to another model as truth;
- the next model resumes from the last semantic/artifact checkpoint.

Complete deterministic tool calls that already succeeded remain recorded.

## 32. Provider output commit boundaries

Internal model work should use commit boundaries such as:

```text
STRUCTURED_OBJECT_PARSED
PATCH_UNIT_PARSED
PLAN_STAGE_ACCEPTED
VERIFIED_GIST_ADMITTED
USER_RESPONSE_SEGMENT_COMMITTED
```

For coding tasks, AlinaCoder should generally show high-level activity rather than streaming raw provider tokens directly into workflow state.

This allows provider replacement without stitching incompatible token streams.

## 33. Idempotency and side-effect ledger

Every mutating tool call receives an `operation_id` and expected precondition hash.

Before retrying after a provider failure, the controller checks whether the operation already completed.

This prevents duplicate:

- file edits;
- commits;
- package installs;
- migrations;
- external writes;
- issue/comment creation.

Retrying inference is safe only if its downstream side effects are also protected.

---

# Part XIV — Provider health and automatic failover

## 34. Typed provider failure taxonomy

Normalize provider errors into:

```text
RATE_LIMIT
DAILY_QUOTA_EXHAUSTED
MONTHLY_QUOTA_EXHAUSTED
AUTH_EXPIRED
AUTH_REVOKED
MODEL_NOT_FOUND
MODEL_RETIRED
CONTEXT_OVERFLOW
CAPABILITY_MISMATCH
PRIVACY_MISMATCH
PRICE_CHANGED
TIMEOUT
NETWORK
PROVIDER_5XX
MALFORMED_STREAM
MALFORMED_OUTPUT
QUALITY_FAILURE
GATEWAY_FAILURE
```

Different errors require different recovery.

## 35. ProviderCircuitBreaker

Each route maintains:

```text
CLOSED → OPEN → HALF_OPEN → CLOSED
```

Open triggers may include:

- repeated 429 beyond known quota/backoff behavior;
- repeated 5xx;
- timeouts;
- malformed streams;
- model-not-found;
- invalid structured responses well above baseline.

Rules:

- exponential backoff with jitter for transient errors;
- respect `Retry-After` and reset headers;
- do not retry permanent 4xx configuration errors blindly;
- known quota exhaustion sleeps until reset rather than hammering;
- price/terms changes quarantine immediately rather than retrying;
- half-open uses low-impact probes before normal traffic resumes.

## 36. Two-layer failover

Failover is explicitly layered:

### Layer A — hosting failover

Same model lineage, different eligible provider/gateway where possible.

Purpose: preserve behavior while escaping a provider outage or quota issue.

### Layer B — cognitive failover

Different model lineage selected from the current task-specific ranking.

Purpose: recover when the model itself lacks capability, context, modality or output reliability.

## 37. Gateway independence

OpenRouter and Kilo are valuable upstreams, but neither may become a mandatory single point of failure.

Where practical AlinaCoder maintains both:

- direct provider adapters;
- gateway adapters.

If one gateway fails, direct providers and another gateway remain eligible.

---

# Part XV — Prepared fallback without quota waste

## 38. HotStandbyPlan

For a long/high-risk task, AlinaCoder prepares a local ranked fallback plan **before** starting the critical stage.

The standby plan contains:

- primary route;
- same-lineage mirror routes;
- independent-family fallback routes;
- minimum required context window;
- required tool/modality capabilities;
- current quota headroom;
- prebuilt HandoffEnvelope template.

Preparing a standby plan does not imply calling all standby models.

Canary pings are used only when their value exceeds quota/privacy cost.

## 39. No default hedged duplicate inference

Hedged requests can reduce latency tails but duplicate quota consumption and may duplicate tool-side effects.

Because AlinaCoder operates under scarce free quotas, hedging is disabled by default.

It may only be enabled for pure, idempotent inference when experiments prove a material benefit and both calls remain provably free.

---

# Part XVI — Context mobility optimizations

## 40. Provider-native context is an optimization, not truth

AlinaCoder may exploit official provider-native continuation mechanisms, but portable state always remains sufficient to resume elsewhere.

Examples:

- Gemini Interactions `previous_interaction_id` where storage/privacy settings permit it;
- local same-model KV/prefix cache reuse;
- Groq/OpenRouter/provider prompt caching where officially supported;
- gateway task IDs/prefix caching when documented.

If native state disappears, the task must still resume from the Continuity Spine.

## 41. ContextCompiler

Every target model gets context compiled for **its** window and capabilities.

`ContextCompiler` prioritizes:

```text
IMMUTABLE user/project invariants
current IntentContract
current task/subtask
repository truth and relevant code
verified recent evidence
accepted decisions
known failures
only then optional older context
```

It removes:

- superseded instructions;
- irrelevant project history;
- repeated raw logs already represented by verified gists;
- speculative reasoning not needed by the receiver.

Even a 1M-token model should not receive context pollution merely because it can fit it.

## 42. MinimumWorkingSet

Every stage defines a minimum semantically complete context set.

A target whose effective context window cannot fit the minimum set after tokenization and tool-schema overhead is ineligible for that stage.

## 43. Experimental cross-model KV transfer

Research on cross-model context/KV reuse is promising but immature.

Any cross-family KV/state translation is classified:

```text
EXPERIMENTAL_NON_NORMATIVE_OPTIMIZATION
```

It may be benchmarked in isolated tests, but correctness and continuity must never depend on it until independently validated and promoted by the normal self-improvement gates.

---

# Part XVII — Privacy-aware strength

## 44. PrivacyClass

A powerful free model is ineligible if its data policy is unacceptable for the current payload.

Routes record at least:

```text
LOCAL_ONLY
REMOTE_NO_TRAINING_ASSERTED
REMOTE_RETENTION_LIMITED
REMOTE_MAY_TRAIN
REMOTE_UNKNOWN
DEV_EVAL_ONLY
```

Sensitive/local-private tasks stay on eligible local routes unless the user explicitly permits an appropriate remote class.

Examples of why this matters:

- some free Gemini tiers currently state submitted content may be used to improve products;
- Kilo documents that Auto Free may route to providers that log prompts/outputs for improvement;
- NVIDIA free hosted NIM access is development/prototyping scoped.

Model strength never overrides privacy policy.

## 45. Context minimization

Remote packets contain only the code/evidence needed for the subtask.

Secrets, credentials, unrelated personal files and irrelevant repository content are excluded by default.

---

# Part XVIII — Routing memory and optional Supabase

## 46. Local-first routing memory

The source of truth for routing learning remains local and must function offline.

Recommended local components:

- SQLite WAL for durable events/state;
- FTS for lexical retrieval;
- local embeddings for semantic retrieval;
- structured metadata filters;
- deterministic rank fusion.

## 47. Hybrid retrieval for model experience

Router memory retrieval combines:

1. exact lexical similarity;
2. symbolic/task metadata similarity;
3. semantic vector similarity;
4. recency/freshness;
5. repository/project match;
6. failure-signature match.

A single embedding nearest-neighbor query is insufficient.

## 48. Optional Supabase Free mirror

Supabase remains optional and non-blocking.

If enabled within its verified Free limits, it may mirror non-secret:

- route performance records;
- provider/model catalog snapshots;
- benchmark summaries;
- failure signatures;
- champion/challenger history;
- Experience Cards.

Use official Postgres full-text search + pgvector hybrid retrieval with rank fusion where valuable.

Do not make alpha Vector Buckets or any cloud-only feature a runtime requirement.

Loss/pause/unavailability of Supabase must not break routing or continuity.

---

# Part XIX — Autonomous frontier self-improvement

## 49. New-model canary ladder

When `FrontierDriftDetector` sees a promising new free model:

```text
DISCOVERED
→ official zero-cost proof
→ schema/tool/capability probe
→ tiny deterministic canaries
→ hidden task-family evaluation
→ low-risk real task challenger
→ probation
→ champion comparison
→ promote / retain specialist / reject
```

Promotion is reversible.

## 50. Model aliases are not trusted identities

If a provider silently changes the checkpoint behind a stable alias, capability history becomes stale.

The system detects identity drift using available version/digest metadata plus behavioral canaries.

A changed alias is treated as a new challenger until revalidated.

## 51. Search for stronger engines automatically

AlinaCoder should periodically search official provider catalogs and release channels for better zero-cost candidates rather than waiting for the user to name them.

The discovery loop asks:

```text
Is there a newly available free model?
Is there a newly free mirror of a known strong model?
Did a formerly paid model gain a true zero-price tier?
Did a provider add longer context/tool use/vision?
Did a free tier become paid or trial-only?
Did a champion degrade or get retired?
```

The system records evidence and does not spam the user with routine discoveries.

---

# Part XX — Verification and benchmarks

## 52. SeamlessHandoffBench

Hidden/adversarial evaluation must include at least:

1. long refactor switches Gemini → Groq;
2. same-model Groq → Cloudflare mirror switch;
3. OpenRouter gateway outage → direct provider;
4. Kilo rate limit → another free gateway;
5. weak → strong escalation with trajectory stripping;
6. strong → fast downshift preserving accepted plan;
7. peer-family switch after disagreement;
8. provider 429 during planning;
9. provider stream dies halfway through JSON;
10. provider stream dies halfway through a patch;
11. model retired between two stages;
12. cost metadata changes from zero to non-zero;
13. free quota exhausts mid-task;
14. target has a smaller context window;
15. target lacks a required tool capability;
16. user correction occurs immediately before switch;
17. user changes project immediately before switch;
18. attempted switch while a file mutation is active;
19. stale HEAD in a handoff packet;
20. uncommitted multi-file candidate patch;
21. target forgets a negation/forbidden action;
22. target identifies the wrong active project;
23. AlinaCoder process crashes and restarts during a provider outage;
24. native provider session state is lost;
25. new higher-ranked free model appears mid-session but switch must wait for a safe checkpoint.

## 53. Continuity metrics

Measure:

```text
goal_preservation_rate
constraint_preservation_rate
project_identity_accuracy
state_checksum_match_rate
handoff_success_rate
resumed_task_success
lost_fact_rate
stale_state_rate
regression_rate
rollback_rate
mean_time_to_resume
handoff_context_tokens
provider_failure_recovery_rate
midstream_corruption_rate
```

A seamless-switch feature is not considered done because the UI stayed open. It must preserve correctness.

## 54. Routing metrics

Measure:

- champion solve rate;
- oracle gap across the free model pool;
- cumulative routing regret;
- challenger promotion precision;
- false promotion rate;
- route availability;
- quota efficiency;
- success per scarce free request;
- family diversity contribution;
- mirror failover success;
- verifier catch rate;
- provider health prediction precision;
- value-add of ensembles over champion-only;
- scaffold gain per model/task class.

---

# Part XXI — Acceptance scenarios

## 55. Mandatory acceptance behavior

### Scenario A — strongest current route disappears

A champion returns model-not-found. AlinaCoder quarantines it, freezes mutation, persists canonical state, selects the next best eligible route, proves continuity, resumes and does not ask the user to reconstruct the task.

### Scenario B — rate limit on a mirrored model

Groq rate-limits GPT-OSS. If an eligible same-lineage mirror exists, AlinaCoder prefers that hosting failover. If not, it performs a direction-aware cognitive handoff to the best different-family candidate.

### Scenario C — new strong free model appears

The model is discovered automatically but only runs canaries/challenger work. It becomes champion only after evidence.

### Scenario D — provider becomes paid

The next cost proof fails. The route is quarantined before another inference call. No paid fallback occurs.

### Scenario E — free-tier account has billing capability

If the system cannot prove hard zero-cost behavior for the exact call, it refuses the route even if marketing labels the plan “free.”

### Scenario F — partial patch stream

The stream dies. No partial patch is applied. Completed deterministic state remains. A new model resumes from the last verified artifact boundary.

### Scenario G — user corrects himself

The correction updates the IntentContract and repair graph before the switch. The new model receives the corrected canonical intent, not the obsolete earlier wording.

### Scenario H — context does not fit target

The ContextCompiler attempts verified compaction/unfolding. If the MinimumWorkingSet still cannot fit, the model is ineligible and another route is selected.

### Scenario I — all remote routes unavailable

AlinaCoder falls back to the best eligible local model, decomposes work if needed, remains honest about uncertainty, and continues without violating safety gates.

### Scenario J — no sufficiently capable free route

AlinaCoder does not silently use paid inference. It decomposes further, uses deterministic tools/local models, or stops at a clearly identified unresolvable capability gap.

---

# Part XXII — Conceptual implementation modules

## 56. Suggested module map

```text
src/alinacoder/intelligence_mesh/
  discovery.py
  frontier_drift.py
  enrollment.py
  cost_proof.py
  provider_registry.py
  lineage_graph.py
  failure_domains.py
  capability_probe.py
  task_fingerprint.py
  route_posterior.py
  champion_challenger.py
  quota_portfolio.py
  topology_router.py
  scaffold_profile.py
  hot_standby.py

src/alinacoder/continuity/
  event_log.py
  canonical_state.py
  verified_context.py
  handoff_envelope.py
  handoff_policy.py
  context_compiler.py
  continuity_proof.py
  switch_transaction.py
  operation_ledger.py
  recovery.py

src/alinacoder/providers/
  base.py
  ollama.py
  gemini.py
  groq.py
  sambanova.py
  mistral.py
  openrouter.py
  kilo.py
  zai.py
  cloudflare.py
  nvidia_nim.py
  cohere.py
  huggingface.py
  modelscope.py

src/alinacoder/reliability/
  error_taxonomy.py
  health.py
  circuit_breaker.py
  backoff.py
  provider_failover.py
  stream_commit.py

src/alinacoder/evaluation/
  free_brain_bench.py
  seamless_handoff_bench.py
  frontier_canary.py
  route_gain.py
```

Adapters remain optional plugins around one stable core contract.

---

# Part XXIII — Non-negotiable prohibitions

## 57. The routing system must never

- spend money;
- enable pay-as-you-go;
- buy credits;
- upgrade a plan;
- use an unproven free route;
- evade quotas or provider terms;
- scrape consumer browser sessions or cookies;
- store API keys in Git or model memory;
- trust public leaderboard rank as sufficient proof;
- trust model consensus above deterministic evidence;
- switch models mid-mutation;
- apply incomplete streamed patches;
- treat a model-generated summary as canonical truth without evidence;
- count provider mirrors as independent cognitive diversity;
- promote a newly released model directly to critical champion work;
- lose user corrections or IntentContract constraints during handoff;
- make a hosted gateway the only recovery path;
- make Supabase or any other cloud state store mandatory;
- claim a seamless handoff without passing continuity benchmarks.

---

# Part XXIV — Research basis recorded for provenance

## 58. Key findings used by this amendment

The architecture is informed by current evidence including:

- **Agent-as-a-Router / ACRouter (arXiv:2606.22902)** — routing improves when it learns from execution-grounded feedback; no model dominates all coding dimensions.
- **EvoRoute (ACL 2026)** — retrieve similar task experience and route at subtask granularity rather than statically assigning one model.
- **RouteMoA / routing-guided ensemble work (ACL 2026)** — screen/rank a large heterogeneous model pool rather than invoking every model.
- **Disagree to Explore, Agree to Commit / Risa (arXiv:2608.22191)** — controlled diversity and evidence-aware convergence can outperform uniform sampling.
- **Zero-Shot Self-Orchestration with Ledger-Based Control (arXiv:2608.26480)** — manager/worker scaffolding gains are real for some models and null/negative for others; benchmark scaffolds per model.
- **The Handoff Tax (arXiv:2608.24358)** — full trajectory transfer can burden a stronger receiver; handoff strategy must depend on switch direction.
- **Decentralized Multi-Agent Systems with Shared Context / DeLM (arXiv:2606.10662)** — compact verified shared state allows agents to reuse progress without passing raw trajectories.
- production gateway reliability patterns from current OpenRouter, LiteLLM and Portkey documentation — typed fallbacks, retries, cooldowns, health routing and explicit treatment of mid-stream failure.
- current provider documentation for Gemini, Groq, SambaNova, Mistral, OpenRouter, Kilo, Z.AI, Cloudflare, NVIDIA NIM, Cerebras and Supabase.

Research results are evidence for design choices, not guarantees. All provider facts decay and therefore must be re-proven at runtime.

---

# Part XXV — Canonical intelligence loop after this amendment

## 59. End-to-end loop

```text
User turn / voice
→ Repair Graph + Intent Beam
→ IntentContract
→ CanonicalSessionState update
→ TaskFingerprint
→ FreeRouteDiscovery refresh if stale
→ Zero-cost / privacy / capability eligibility
→ retrieve similar routing experience
→ select champion or safe challenger
→ choose orchestration topology
→ prepare HotStandbyPlan
→ compile model-specific context from verified state
→ inference
→ deterministic tools / evidence
→ verify result
→ update RoutePosterior + Experience Cards
→ admit only verified gists to shared context
→ if provider/model must switch:
     mutation barrier
     state snapshot
     direction-aware HandoffEnvelope
     target ZeroCostAdmissionGate
     ContinuityProof
     dry next action
     resume
→ Done Contract
→ commit/push `main` only when all gates pass
```

The target behavior is not “one huge free model.”

It is a **self-updating, zero-cost, evidence-driven intelligence fabric** in which models can appear, disappear, improve, degrade or fail without taking the project state, user intent or verified work with them.
