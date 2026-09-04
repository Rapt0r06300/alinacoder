# AlinaCoder v0.2 — Adaptive Frontier Fabric & Routing Stability Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment strengthens the autonomous frontier fabric with a second-generation routing policy designed for a rapidly changing free-model ecosystem.

The objective is not merely to have many providers. The objective is to make `AlinaCoder.exe` continuously discover the strongest legitimately zero-cost intelligence available, understand what each engine is actually good at, connect to eligible routes automatically after supported enrollment, remain stable on a good model while work is coherent, switch only when switching is expected to improve the final verified task outcome, and recover on another provider or model without losing the user's intent or verified project state.

It is normative together with:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-routing-seamless-handoff-amendment.md`

This amendment has higher precedence for:

- model-catalog-independent routing;
- multidimensional capability matching;
- routing granularity and task affinity;
- switching utility, hysteresis, dwell and anti-thrashing;
- delayed/terminal credit assignment;
- active challenger exploration;
- free-route cost attestation;
- contradiction handling between pricing/catalog sources;
- protocol/capability handshakes;
- adaptive handoff encoding;
- stale in-flight response rejection;
- route selection invariance across French/noisy French paraphrases;
- optional local-model self-strengthening from verifier-backed replay;
- current 2026-09-04 provider classification refinements.

All earlier safety, zero-cost, privacy, intent, memory, verification, resource and Git invariants remain binding.

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
ALLOW_PAID_FALLBACK = false
```

Central principle:

> **Discover broadly, prove narrowly, route by capability, stay stable while stability is valuable, and switch only from a verified checkpoint when the expected terminal benefit is decisively positive.**

---

# Part I — Stop predicting model names; predict required capability

## 2. Catalog-independent routing

A router that directly learns:

```text
prompt → model_id
```

is structurally brittle.

Free-model catalogs change too quickly. A model can appear, disappear, be repriced, be renamed, move to another host or change checkpoint behind an alias without any change to the user's task.

The canonical routing architecture therefore becomes:

```text
Task / stage
  ↓
CapabilityRequirementVector
  ↓
eligible live model catalog
  ↓
ModelCapabilityVector per route
  ↓
shortfall matching + verified outcome evidence
  ↓
route family / provider selection
```

The learned router predicts **requirements**, not fixed model identities.

Adding or removing a model must normally require only updating its evidence-backed capability profile, not retraining the routing policy.

## 3. CapabilityRequirementVector

Every meaningful task or stage receives a normalized requirement vector.

Minimum dimensions:

```text
reasoning_depth
code_generation
code_editing
bug_localization
debugging
architecture
repo_navigation
tool_use
function_calling
structured_output
long_context
context_precision
vision
multimodal
web_research
math
security_reasoning
regression_reasoning
instruction_fidelity
negation_fidelity
french_understanding
noisy_french_understanding
conversation_repair
handoff_rehydration
latency_sensitivity
```

Additional task-specific dimensions may be registered without changing the stable router contract.

Each dimension records:

```text
required_level
importance
minimum_acceptable_level
confidence
source_of_requirement
```

## 4. ModelCapabilityVector

Every model lineage maintains a measured capability vector using the same dimension ontology.

Each dimension records:

```text
posterior_mean
lower_confidence_bound
sample_count
last_measured_at
benchmark_family
project_specific_evidence
known_failure_modes
```

Provider-specific differences such as tool-schema correctness, output truncation or context handling are layered on top of the cognitive lineage profile as `RouteCapabilityOverrides`.

## 5. ShortfallMatcher

A candidate has capability shortfall when:

```text
model_lcb[dimension] < task.minimum_required[dimension]
```

Hard shortfalls make the route ineligible.

Soft shortfalls remain visible as routing risk.

The router should prefer the eligible route with the strongest conservative task-success evidence, not the model with the biggest nominal parameter count.

## 6. Language-invariant requirement prediction

Equivalent tasks expressed as:

```text
clean French
noisy French
ASR-like French
French with English technical vocabulary
abbreviations
minor spelling mistakes
clean English
```

should produce materially equivalent `CapabilityRequirementVector`s unless meaning changed.

Routing quality must not drop merely because the user speaks ordinary French.

---

# Part II — Hierarchical routing granularity

## 7. Routing has three different layers

AlinaCoder must not use one switching policy for every call.

Canonical hierarchy:

```text
TASK LEVEL
  cognitive affinity lease

STAGE LEVEL
  deliberate cognitive re-routing at safe checkpoints

CALL / HOSTING LEVEL
  transparent same-lineage provider failover
```

## 8. TaskAffinityLease

At task admission, AlinaCoder assigns a preferred cognitive lineage for the first coherent portion of work.

A `TaskAffinityLease` contains:

```text
task_id
preferred_lineage
started_at
minimum_dwell
current_stage
state_version
lease_reason
quality_prior
handoff_cost_estimate
cache_locality_estimate
```

The lease is not an absolute lock. It is a bias toward continuity.

## 9. Same-lineage host failover is cheap

If the current provider fails but another eligible provider hosts the same lineage, AlinaCoder may perform hosting failover without treating it as a major cognitive change.

Examples:

```text
GPT-OSS lineage: provider A → provider B
Nemotron Ultra lineage: gateway A → direct NVIDIA route
Poolside Laguna lineage: gateway A → gateway B
```

The Continuity Spine remains authoritative.

## 10. Cognitive switches are expensive decisions

Switching to another model family can:

- lose provider-native prompt/KV caches;
- incur handoff tax;
- change tool behavior;
- change reasoning style;
- amplify inherited mistakes;
- require re-tokenizing context;
- spend scarce free quota;
- increase latency;
- destabilize a trajectory that might have recovered naturally.

Therefore a single transient error is not sufficient evidence for a cognitive switch.

---

# Part III — SwitchUtilityCalculator

## 11. Switch only when expected terminal value is positive

Before a cognitive model change, compute a `SwitchUtilityEstimate`.

Conceptual terms:

```text
expected_terminal_success_gain
+ capability_shortfall_reduction
+ provider_reliability_gain
+ context_fit_gain
+ tool_compatibility_gain
+ quota_survival_gain
- handoff_tax
- cache_loss_cost
- rehydration_risk
- latency_penalty
- scarce_quota_cost
- trajectory_disruption_risk
- switch_uncertainty
```

The exact scoring method may evolve, but all major terms must remain observable.

## 12. Terminal outcome dominates local elegance

A model response that looks good locally but causes final task failure must not be rewarded as a successful routing decision.

Routing learns from:

```text
terminal Done Contract
stage verification
local parser/schema validity
regression tests
user correction signal
rollback/failure outcomes
```

with terminal success receiving the highest authority.

## 13. SwitchHysteresis

A cognitive switch occurs only when one of the following holds:

```text
A. current route is hard-ineligible
B. current route is unavailable and no same-lineage host is eligible
C. decisive capability shortfall is observed
D. repeated evidence shows current route is unlikely to recover
E. another route's conservative terminal-success estimate exceeds current by the switch margin
F. context/tool/privacy requirements changed so the current route no longer fits
```

`SwitchHysteresis` includes:

```text
minimum_gain_margin
minimum_dwell
consecutive_evidence_required
post_switch_cooldown
max_cognitive_switches_per_stage
max_cognitive_switches_per_task
```

Limits are adaptive, not arbitrary fixed constants, but they must prevent thrashing.

## 14. Error tolerance

The router classifies errors into:

```text
TRANSIENT_RECOVERABLE
HOSTING_FAILURE
MODEL_CAPABILITY_FAILURE
SCHEMA_COMPATIBILITY_FAILURE
CONTEXT_FAILURE
POLICY_FAILURE
TERMINAL_QUALITY_FAILURE
```

`TRANSIENT_RECOVERABLE` normally triggers retry/backoff or same-lineage hosting failover, not an immediate family switch.

## 15. RemainingWorkEstimator

Switch utility depends on how much work is left.

Estimate:

```text
remaining_stages
remaining_tool_calls
remaining_expected_tokens
remaining_code_surface
remaining_test_surface
remaining_reasoning_complexity
```

A late switch for one trivial formatting step is often lower value than an early switch before architectural reasoning.

---

# Part IV — Delayed credit assignment

## 16. RoutingDecisionLedger

Every selection records:

```text
decision_id
task_id
stage_id
state_version
selected_lineage
selected_route
alternatives
requirement_vector
capability_evidence
switch_utility
reason_for_selection
```

## 17. DelayedCreditAssigner

When the task reaches a terminal or major-stage outcome, credit is propagated back to prior routing decisions.

Signals include:

```text
DONE
PARTIAL
FAILED
ROLLED_BACK
USER_CORRECTED_INTENT
REGRESSION_FOUND
WRONG_PROJECT
WRONG_FILE
MALFORMED_TOOL_CALL
RECOVERED_AFTER_TRANSIENT_ERROR
SUCCESS_AFTER_SWITCH
FAILURE_AFTER_SWITCH
```

This avoids training the router to prefer a model merely because one intermediate output looked plausible.

## 18. Routing regret

Track at least:

```text
oracle_gap_when_known
cumulative_routing_regret
switch_regret
avoidable_switch_count
missed_switch_count
late_switch_count
premature_switch_count
```

The system should improve its ability to know both **which model** and **when not to switch**.

---

# Part V — High-information challenger learning

## 19. Do not explore randomly

Uniform random challenger traffic wastes scarce free quota and produces weak evidence.

Prefer exploration where the decision boundary is uncertain.

## 20. RoutingBoundaryMiner

Mine high-information cases such as:

```text
champion barely passed
champion failed but verifier localized the reason
router had low confidence
models disagreed on a testable hypothesis
new model has sparse evidence in an important task family
current capability vectors overlap strongly
switch utility was near threshold
previous route choice was later reversed
```

## 21. ChallengerValueOfInformation

Before spending a scarce free call on a challenger, estimate:

```text
probability_evidence_changes_future_routing
× future_task_frequency
× consequence_of_wrong_routing
× uncertainty_reduction
÷ quota_cost
```

Low-value canaries are skipped.

## 22. ShadowChallenger

Where useful, a challenger may run against:

- synthetic tasks;
- hidden evaluation tasks;
- recorded/replay task slices;
- read-only repository snapshots;
- already-completed real tasks.

Shadow challengers receive no authority to mutate the user's live worktree.

## 23. Paired promotion evidence

Prefer paired comparison on equivalent task slices over independent benchmark averages.

A challenger may become champion only after:

```text
sufficient sample size
+ statistically/conservatively better verified outcome
+ no safety/privacy regression
+ stable structured/tool behavior
+ acceptable handoff behavior
```

---

# Part VI — Zero-cost proof becomes a first-class attestation

## 24. CostProofReceipt

Every remote inference attempt must have a machine-readable `CostProofReceipt` produced immediately before the call.

Minimum fields:

```text
receipt_id
provider
route
model_id
model_version_or_alias
account_tier
entitlement_type
prompt_price
completion_price
request_price
other_metered_price
included_allowance_remaining
hard_overage_block
payment_method_risk
proof_sources
source_hashes
verified_at
expires_at
verdict
```

`verdict` is one of:

```text
PROVEN_ZERO_COST
UNPROVEN
PAID
TRIAL_BILLING_RISK
ENTITLEMENT_EXHAUSTED
```

Only `PROVEN_ZERO_COST` can enter autonomous inference.

## 25. Structural zero-cost classes

Classify routes by how strongly zero cost is enforced:

```text
HARD_FREE_NON_BILLABLE
FREE_WITH_HARD_CAP
EVAL_ONLY_FREE
PROMOTIONAL_NON_BILLABLE_HARD_CAP
BILLING_CAPABLE_BUT_HARD_ZERO_LIMIT
BILLING_CAPABLE_UNPROVEN
PAID
```

Preferred order is structural, not marketing-based.

`BILLING_CAPABLE_UNPROVEN` is ineligible by default.

## 26. Free provider != free model

A provider-level Free plan is not sufficient.

Proof must cover the exact:

```text
account
model variant
endpoint
service tier
feature flags
region if relevant
request type
```

Example: a provider may have a daily free allocation while selected frontier models require a paid plan. Such models remain ineligible even though the account itself is “Free.”

## 27. No hidden paid features inside a free call

Before inference, separately check whether requested features can trigger billing:

```text
web grounding
search tools
image generation
long-term cache storage
batch processing
premium service tier
paid tool execution
provider-side agents
```

If a feature is not proven free, disable it or select another route.

---

# Part VII — Evidence contradiction resolver

## 28. Source hierarchy

For price, entitlement and terms:

```text
1. current account-specific provider API/dashboard metadata when machine-readable
2. official provider pricing/quota documentation
3. official provider model catalog
4. official provider changelog
5. trusted gateway metadata for that gateway route
6. independent/current directories as discovery leads only
```

## 29. ProviderEvidenceResolver

If sources disagree:

```text
official says paid + community says free
→ PAID_OR_UNPROVEN

gateway says $0 + direct provider says paid
→ gateway route may still be free, but proof applies only to that gateway route

catalog says model exists + pricing says unavailable on Free
→ INELIGIBLE_ON_FREE

cached proof says zero + fresh source changed
→ QUARANTINE_AND_REFRESH
```

Uncertainty is resolved conservatively.

## 30. NegativeEvidenceCache

Store recent disqualifications so AlinaCoder does not repeatedly rediscover and retry an unsafe route.

Examples:

```text
requires payment method
trial expired
paid model on otherwise free provider
free only for non-commercial evaluation
quota exhausted until reset
privacy incompatible
endpoint retired
```

Negative evidence has a TTL and must be re-checkable because providers change.

---

# Part VIII — ProviderCapabilityHandshake

## 31. Never trust model metadata without probing behavior

After cost proof and enrollment, a new route performs a non-mutating capability handshake.

Discover or probe:

```text
models endpoint
context window
max output
text input
image input
audio input
vision
system messages
tool/function calls
parallel tool calls
JSON mode
strict structured output
reasoning controls
streaming
stream error semantics
usage metadata
rate-limit headers
retry-after behavior
provider-native continuation
cache behavior
```

## 32. ProtocolAdapter

AlinaCoder supports provider-native protocols behind one typed internal contract.

Potential adapters include:

```text
OpenAI-compatible Chat Completions
OpenAI-compatible Responses-style APIs
Gemini native API
Anthropic Messages-style APIs
Ollama native API
provider-specific extensions
```

Do not flatten away useful provider-specific capabilities merely to force every model into a lowest-common-denominator API.

## 33. ToolSchemaTranscompiler

A canonical internal tool schema is compiled into the exact format required by the selected provider.

Before tool use is admitted, test:

```text
schema acceptance
required fields
enum fidelity
nested object fidelity
nullability
parallel tool-call semantics
argument JSON validity
unknown-field behavior
```

## 34. StructuredOutputReliabilityProfile

For each route, measure:

```text
valid_json_rate
schema_exact_rate
repair_needed_rate
truncation_rate
tool_argument_validity
stream_completion_integrity
```

This evidence can outweigh headline model intelligence on tool-heavy tasks.

---

# Part IX — Adaptive handoff codec

## 35. One handoff representation is not universally optimal

The previous `HandoffFormatRouter` is strengthened into an `AdaptiveHandoffCodec`.

Available codecs:

```text
TYPED_STATE_ONLY
DEPENDENCY_GRAPH
VERIFIED_GISTS
CONCISE_NARRATIVE
GRAPH_PLUS_NARRATIVE
STATE_PLUS_EVIDENCE_UNFOLD
```

## 36. Codec selection

Codec selection depends on:

```text
source model capability
target model capability
switch direction
task type
reasoning adaptivity
constraint density
dependency structure
context budget
prior pairwise handoff success
```

Graph-only handoffs must not be assumed universally better.

## 37. HandoffCodecProfile

Maintain pairwise measurements:

```text
source_lineage
target_lineage
task_family
codec
continuity_success
constraint_retention
rehydration_tokens
rehydration_latency
receiver_error_rate
```

## 38. Incoming-model reconstruction

The target should independently reconstruct a short next-step plan from canonical evidence.

It is not asked to continue an outgoing model's private reasoning trace.

---

# Part X — State leases and stale-response rejection

## 39. StateVersionLease

Every provider request is issued against:

```text
session_id
canonical_state_version
state_checksum
repo_head_sha
working_tree_fingerprint
intent_contract_version
```

## 40. ResponseAdmissionGate

A response may arrive after:

- the user corrected the request;
- another model already changed the plan;
- a test changed the evidence;
- repository HEAD moved;
- a rollback occurred;
- a failover completed.

Before admitting any response:

```text
response.state_version == current admissible version
AND expected hashes still match
AND response route is still eligible
```

Otherwise:

```text
STALE_IN_FLIGHT_RESPONSE
```

and the response cannot mutate current state.

## 41. Optimistic concurrency for LLM work

Treat model calls like optimistic transactions:

```text
read state version
compute candidate
compare current version
commit only if preconditions still hold
```

This is mandatory for parallel agents and shadow challengers.

---

# Part XI — Provider/load-aware scheduling

## 42. ProviderLoadSnapshot

Routing considers current operational state:

```text
recent_ttft
recent_tokens_per_second
recent_p95_latency
inflight_calls
known_queue_depth_if_available
recent_429_rate
recent_5xx_rate
circuit_state
quota_remaining
quota_reset_time
```

## 43. LocalInferenceLoadSnapshot

For local models:

```text
VRAM_free
RAM_free
GPU_utilization
CPU_utilization
model_resident
model_load_time
estimated_tokens_per_second
thermal/resource pressure
```

## 44. Performance slack

If two routes have near-equal conservative quality and one is severely congested, selection may prefer the faster healthy route.

But latency must never cause a hard capability shortfall to be ignored.

## 45. Cache locality

Cache locality is a legitimate routing input.

If continuing on the current strong route has a large reusable prefix/cache advantage, a marginally higher-scoring alternate model should not trigger a switch unless expected terminal gain clears the switch margin.

---

# Part XII — The strongest model pool remains maximally broad

## 46. Provider universe architecture

The `FreeRouteDiscoveryEngine` should maintain three discovery rings.

### Ring A — direct first-party providers

Examples, always live-verified:

```text
Google Gemini API
Groq
SambaNova Cloud
Mistral AI Studio/API
Z.AI
Cloudflare Workers AI
Ollama Cloud
NVIDIA NIM
Hugging Face Inference Providers
Cohere
ModelScope
future legitimate first-party free endpoints
```

### Ring B — gateways / aggregators

Examples:

```text
OpenRouter
Kilo Gateway
other legitimate OpenAI-compatible gateways discovered later
```

### Ring C — discovery leads

Community-maintained free-LLM directories, provider comparisons and GitHub lists may reveal candidates, but can never alone prove zero cost or acceptable terms.

## 47. AutoDiscoveryManifest

Provider discovery definitions should be data-driven rather than hardcoded throughout the codebase.

Conceptual manifest:

```text
provider_id
discovery_url
models_url
pricing_url
quota_probe
account_probe
api_style
auth_method
terms_url
privacy_url
known_free_class
proof_ttl
```

New providers can be added as adapters/manifests without modifying router algorithms.

---

# Part XIII — Current provider evidence snapshot, 2026-09-04

## 48. This snapshot is bootstrap evidence only

All facts below decay. Runtime verification has precedence.

## 49. Google Gemini

Current official Gemini Developer API documentation exposes a Free usage tier and currently marks selected model variants as free of charge for input/output.

Current examples in official pricing include Free Tier entries for models such as:

```text
Gemini 3.6 Flash variants
Gemini 3.5 Flash variants
other selected Flash/Flash-Lite models
```

Important constraints:

- exact variant matters;
- not every Gemini model/variant is free;
- Free Tier content may be used to improve Google products;
- billing must be separately linked to move to paid tiers;
- current rate limits are account/model dependent and should be read live;
- a 1M-context model existing in the catalog does not prove free entitlement for that route.

Gemini is therefore a high-value candidate family, not a blanket “all Gemini free” rule.

## 50. Groq Free Plan

Current official Free Plan evidence includes strong open models such as:

```text
openai/gpt-oss-120b
openai/gpt-oss-20b
qwen/qwen3.6-27b
qwen/qwen3.8-27b
groq/compound
groq/compound-mini
```

Exact limits are account/model dependent and may change.

Groq should be capability-probed for reasoning effort, tools, prompt caching and structured output per current model.

## 51. SambaNova Cloud Free Tier

Current official documentation states:

```text
Free Tier = no payment method linked
Developer Tier = payment method linked
```

Current Free Tier examples include:

```text
DeepSeek-V3.1
Meta-Llama-3.3-70B-Instruct
gpt-oss-120b
DeepSeek-V3.2 preview
gemma-4-31B-it preview
```

Current published free examples show strict per-model daily/request/token limits, including 20 RPM / 20 RPD / 200,000 TPD on listed models at time of research.

Preview models may disappear and should receive lower availability confidence.

## 52. Mistral Free mode

Current official Mistral usage documentation states that Free mode can create API keys and use included monthly usage under current limits.

Free mode is aimed at evaluation/prototyping and has lower limits than pay-as-you-go.

Rules:

- account-specific Limits page is authoritative for exact quotas;
- phone/account enrollment may be required;
- privacy/training settings must be checked before sensitive material;
- pay-as-you-go must remain disabled;
- the exact model must still pass CostProofReceipt.

## 53. Z.AI zero-price models

Current official Z.AI pricing explicitly lists:

```text
GLM-4.7-Flash  → Free input / cache / output
GLM-4.5-Flash  → Free input / cache / output
```

Other newer GLM variants have non-zero prices or temporary discounts and must not be confused with the genuinely zero-price Flash routes.

A provider's newest GLM model is not automatically eligible merely because an older Flash route is free.

## 54. OpenRouter

OpenRouter remains useful for breadth and discovery:

- rotating `:free` variants;
- `openrouter/free`;
- public model metadata;
- current pricing fields;
- current coding/agentic/intelligence ranking metadata where exposed;
- same-model provider failover.

Rules:

- exact route price must be zero;
- OpenRouter rankings are priors only;
- free availability can change quickly;
- OpenRouter is never the only failover path;
- the underlying model lineage is preserved in telemetry.

## 55. Kilo Gateway

Current official Kilo Gateway documentation exposes no-credit free routes and a dynamic `kilo-auto/free` tier.

Current examples include:

```text
nvidia/nemotron-3-ultra-550b-a55b:free
poolside/laguna-s-2.1:free
poolside/laguna-xs-2.1:free
stepfun/step-3.7-flash:free
tencent/hy3:free
openrouter/free
```

The mapping changes server-side as free models change.

Important:

- free models can be available anonymously under current rate limits;
- some free upstreams may log prompts/outputs for improvement;
- NVIDIA free endpoints are subject to NVIDIA trial/development terms;
- a marketing/blog statement that a model is “free for a limited time” requires short proof TTL;
- exact `GET /models` metadata should be checked before each proof window.

## 56. NVIDIA NIM

Current NVIDIA developer access is valuable because the catalog includes very large open models such as:

```text
Nemotron 3 Ultra 550B A55B
Nemotron 3 Super 120B A12B
Nemotron Nano/Omni variants
Mistral-Nemotron
```

Nemotron Ultra currently advertises up to 1M context and is designed for agentic reasoning/coding.

However hosted free NIM access is development/prototyping/testing scoped under current terms.

It must therefore be tagged `EVAL_ONLY_FREE` unless current official entitlement proves a broader use scope.

## 57. Cloudflare Workers AI

Current official pricing provides 10,000 Neurons/day on Workers Free.

Crucial refinement:

**some models in the Workers AI catalog currently require a paid billing method or prepaid AI Gateway credits.**

Therefore:

```text
Workers Free account
≠ every Workers AI model is free eligible
```

Current catalog examples like some Kimi, GLM 5.x and DeepSeek V4 routes may require paid billing even though the platform has a Free allocation.

The admission gate must prove the selected model is actually usable inside the Free allocation without upgrade.

## 58. Ollama local and cloud

Local Ollama remains the strongest structural zero-cost fallback:

```text
local inference monetary cost = 0
```

subject to hardware/resources.

Ollama Cloud currently has a Free plan with a small monthly starter allowance for a subset of starter models, but the cloud catalog also has explicit per-token pricing and allows additional paid usage/credits.

Therefore Cloud routes require strict allowance proof and no-overage proof.

Local routes do not require a CostProofReceipt for provider billing, but still require resource/capability admission.

## 59. Hugging Face, Cohere, ModelScope and other micro/evaluation routes

These remain useful as specialist/challenger capacity where current entitlement proves zero cost.

Small credit allowances should be conserved.

ModelScope may require identity/account prerequisites and can have evaluation/non-commercial scope constraints.

## 60. Cerebras

Current official research remains incompatible with standing zero-cost capacity:

- free access is a bounded trial;
- payment verification may be required;
- no renewing permanent free tier is currently documented.

Cerebras remains `TRIAL_ONLY / INELIGIBLE_STANDING_ZERO_COST` unless official policy later changes.

---

# Part XIV — Privacy is an eligibility dimension

## 61. ProviderDataPolicyProfile

Record:

```text
may_train
may_log
retention_period
zero_data_retention_available
account_tier_dependency
region
terms_scope
commercial_scope
personal_confidential_data_allowed
last_verified_at
```

## 62. ProjectSensitivityClass

At minimum:

```text
PUBLIC_REPO
PRIVATE_REPO
PERSONAL_DATA
SECRET_BEARING
ENTERPRISE_CONFIDENTIAL
LOCAL_ONLY_REQUIRED
```

## 63. RemoteEligibilityMatrix

A route is excluded before ranking if project sensitivity exceeds provider policy.

The user should not need to manually remember which free tier trains on prompts.

AlinaCoder enforces this automatically from current policy evidence.

---

# Part XV — Router-of-routers architecture

## 64. Deterministic gate first

Many routing decisions do not require an LLM.

First apply deterministic filters:

```text
zero-cost proof
privacy/use-scope
context fit
required modalities
required tool support
circuit health
quota sufficiency
resource fit
```

## 65. Lightweight requirement predictor second

Use a local lightweight predictor/encoder where its benchmarked accuracy is sufficient to estimate the `CapabilityRequirementVector`.

This keeps routing fast and avoids consuming a strong free LLM merely to decide which LLM to call.

## 66. Frontier scheduler only for ambiguous routing

If deterministic and lightweight signals leave substantial ambiguity, a strong eligible model may act as a scheduler over a compact structured route state.

It can choose only among pre-approved actions such as:

```text
KEEP_CURRENT
HOST_FAILOVER
COGNITIVE_SWITCH
DECOMPOSE
RUN_CHALLENGER
ASK_FOR_MORE_EVIDENCE
```

Its decision is advisory and schema-validated.

---

# Part XVI — Self-strengthening local intelligence

## 67. Routing around weakness is not the final ceiling

Verifier-backed failures can eventually improve local cheap models instead of forever escalating around them.

A future/optional `LocalCapabilityEvolutionLoop` may use:

```text
failed local invocation
→ stronger eligible teacher demonstration
→ deterministic/verifier validation
→ Experience Card / SkillBook extraction
→ replay
→ optional LoRA/adaptor candidate
→ holdout evaluation
→ promotion or rejection
```

## 68. SkillBook first

Before expensive model fine-tuning, prefer reusable procedural skills that can improve multiple local models.

Skill entries must include:

```text
trigger signature
procedure
applicability
known counterexamples
source evidence
verification
version
```

## 69. Adapter training is optional and isolated

Any future LoRA/adaptor training must:

- fit hardware budgets;
- use only authorized data;
- never include secrets unintentionally;
- train outside the live canonical worktree;
- pass replay + validation + hidden holdout;
- be reversible;
- never become a requirement for basic AlinaCoder operation.

## 70. Joint admission

Router, SkillBook and optional adapter changes are evaluated end-to-end.

A locally improved model is useful only if the complete routed system preserves or improves verified outcomes.

---

# Part XVII — Supabase optional routing memory refinement

## 71. Local source of truth remains mandatory

Routing memory must work with no Supabase connection.

Recommended local canonical store:

```text
SQLite WAL
+ lexical FTS
+ structured metadata
+ local embeddings
+ deterministic rank fusion
```

## 72. Optional Supabase mirror

When enabled and within verified Free limits, Supabase may mirror non-secret routing evidence.

Good candidates:

```text
model capability observations
provider catalog snapshots
cost proof metadata without secrets
route outcomes
failure signatures
challenger results
handoff codec results
Experience Cards
```

## 73. Hybrid retrieval

Current Supabase documentation supports hybrid search using:

```text
Postgres tsvector / GIN keyword search
+ pgvector semantic search
+ Reciprocal Rank Fusion
```

This is the preferred cloud-mirror retrieval pattern because exact provider/model/error terms and semantic task similarity are both important.

## 74. Freshness filtering before semantic similarity

Search must filter stale/inapplicable evidence by:

```text
provider
model version
project/repo
route generation
freshness
terms version
pricing proof generation
```

before allowing semantically similar old evidence to influence a current routing decision.

## 75. Alpha features are optional

Supabase Vector Buckets or other alpha features must not become required for AlinaCoder's canonical routing memory.

---

# Part XVIII — Local open-model frontier discovery

## 76. LocalModelDiscovery

Enumerate legitimate local engines such as:

```text
Ollama
llama.cpp-compatible servers
LM Studio local server
vLLM where supported
other explicitly installed local inference servers
```

## 77. HardwareFitProfile

For every local model candidate measure or estimate:

```text
model_size
quantization
VRAM_required
RAM_required
load_time
context_memory_growth
tokens_per_second
GPU_offload_ratio
CPU_pressure
stability
```

## 78. LocalCapabilityProbe

A smaller local model that is excellent on a specific task can be a specialist champion even if remote larger models score higher globally.

No local model is promoted only because it is “free forever.” Quality remains evidence-driven.

---

# Part XIX — Acceptance tests added by this amendment

## 79. Catalog portability tests

1. Add a new model profile without retraining router; it becomes routable after probes.
2. Remove the current champion; router selects a valid replacement without code changes.
3. Reprice a model from zero to non-zero; route is quarantined before the next call.
4. Reuse same model on a different provider; hosting redundancy recognized without fake cognitive diversity.
5. Provider alias changes checkpoint; old capability evidence becomes stale.

## 80. Stability tests

6. One transient timeout does not cause cognitive thrash.
7. One recoverable schema error triggers repair/retry before family switch when appropriate.
8. Strong current model remains pinned when alternate gain is below switch margin.
9. Repeated verified capability failure clears hysteresis and triggers a safe switch.
10. Cache-locality advantage prevents a low-value late-stage switch.
11. Max switch budget prevents A→B→A→B oscillation.

## 81. Delayed outcome tests

12. Locally plausible step followed by terminal regression updates route credit negatively.
13. Early weak output recovered by same model does not falsely teach “switch on first error.”
14. A switch that rescues the task receives positive switch evidence.
15. A switch that introduces regressions records negative pairwise handoff evidence.

## 82. Cost proof tests

16. Provider Free plan + paid-only model → model rejected.
17. Zero-price model + paid grounding feature → grounding disabled or route rejected.
18. Promotional credit with automatic paid overflow → rejected.
19. Hard-capped free quota exhausted → route sleeps until reset.
20. Community source says free but official pricing says paid → reject.
21. Gateway route says zero while first-party direct route is paid → gateway may remain eligible independently after proof.

## 83. Capability tests

22. Model claims tools but fails canonical nested schema probe → tool-heavy route demoted.
23. Context window smaller than MinimumWorkingSet → ineligible.
24. Vision required but route is text-only → ineligible.
25. Structured JSON reliability degrades after provider change → route demoted automatically.

## 84. Continuity/staleness tests

26. User correction increments state while old model call is in flight; old response rejected as stale.
27. Git HEAD changes while challenger is running; stale patch cannot apply.
28. Same-lineage host failover resumes from identical canonical state.
29. Cross-lineage switch must pass ContinuityProof before mutation.
30. Crash/restart rebuilds exact current state from event log/snapshot.

## 85. Language invariance tests

31. Equivalent clean French and English task produce compatible capability requirement vectors.
32. Typos/noisy French do not down-route a difficult task merely because surface form is simple.
33. Negation change produces an intentionally different IntentContract while routing complexity remains coherent.
34. ASR false start repaired before routing does not contaminate active requirement vector.

## 86. Challenger tests

35. New model is not promoted after one success.
36. BoundaryMiner prioritizes uncertain/high-value tasks over random easy tasks.
37. Shadow challenger cannot mutate live worktree.
38. Scarce quota challenger is skipped when Value of Information is too low.

---

# Part XX — New observability

## 87. RouterDecisionTrace

Every important routing/switch decision should be explainable after the fact without exposing private chain-of-thought.

Record:

```text
selected route
eligible alternatives
hard exclusions
capability shortfalls
confidence bounds
switch utility summary
quota state
health state
cost proof receipt id
state version
final outcome when known
```

## 88. User-facing simplicity

The ordinary UI should not flood the user with this machinery.

Default status can remain concise:

```text
Moteur: Nemotron 3 Ultra — gratuit vérifié
Secours prêt: GPT-OSS 120B / Gemini Flash
État: stable
```

Detailed router traces belong in diagnostics.

## 89. Mandatory metrics

Track at minimum:

```text
verified_solve_rate
terminal_done_rate
route_regret
switch_regret
cognitive_switches_per_task
hosting_failovers_per_task
avoidable_switch_rate
missed_switch_rate
handoff_success_rate
continuity_proof_pass_rate
stale_response_reject_rate
false_free_classification_rate
cost_proof_failure_rate
capability_shortfall_failure_rate
structured_output_validity
provider_health_precision
quota_efficiency
free_request_value_add
cache_reuse_rate
french_route_invariance
challenger_promotion_precision
```

Target:

```text
false_free_classification_rate = 0
paid_autonomous_calls = 0
```

---

# Part XXI — Conceptual implementation additions

## 90. New modules

```text
src/alinacoder/intelligence_mesh/
  capability_ontology.py
  requirement_vector.py
  capability_vector.py
  shortfall_matcher.py
  task_affinity.py
  switch_utility.py
  switch_hysteresis.py
  delayed_credit.py
  boundary_miner.py
  value_of_information.py
  cost_receipt.py
  evidence_resolver.py
  negative_evidence.py
  capability_handshake.py
  protocol_adapter.py
  tool_schema_transcompiler.py
  structured_output_profile.py
  remaining_work.py
  provider_load.py
  local_discovery.py

src/alinacoder/continuity/
  adaptive_handoff_codec.py
  state_lease.py
  response_admission.py

src/alinacoder/evaluation/
  catalog_portability_bench.py
  route_stability_bench.py
  delayed_credit_bench.py
  cost_attestation_bench.py
  french_route_invariance_bench.py
  handoff_codec_bench.py

src/alinacoder/self_improvement/
  routing_boundary_replay.py
  skillbook.py
  local_capability_evolution.py
```

Names are conceptual; implementation may refine package boundaries without weakening the contracts.

---

# Part XXII — Research basis

## 91. New evidence incorporated

### HyDRA — Hybrid Dynamic Routing Architecture (2026)

Key lesson:

- predict multiple capability requirements rather than a single difficulty scalar;
- decouple router outputs from concrete model IDs;
- new/removed/repriced models should be catalog changes rather than router retraining events;
- language-invariant routing matters in real multilingual products.

Applied here through `CapabilityRequirementVector`, `ModelCapabilityVector` and `ShortfallMatcher`.

### MTRouter — Cost-Aware Multi-Turn LLM Routing (ACL 2026)

Key lesson:

- terminal outcome matters;
- good routing does not mean frequent switching;
- transient errors do not always justify a switch;
- model stability preserves useful trajectory/cache locality.

Applied through `TaskAffinityLease`, `SwitchHysteresis` and delayed terminal credit.

### TRACE-Router (2026)

Key lesson:

- agentic task supervision is often task-level, not per-call;
- persistent backend affinity can outperform independent per-call routing.

Applied through hierarchical routing granularity rather than unrestricted turn-level switching.

### CASTER (2026)

Key lesson:

- learn from current-policy failures and high-value boundary examples;
- random exploration can generate misleading/noisy routing evidence.

Applied through `RoutingBoundaryMiner` and `ChallengerValueOfInformation`.

### Routed Graph Handoff (EMNLP 2026)

Key lesson:

- typed graph handoffs can compress coordination;
- graph-only handoffs can regress adaptive tasks;
- the handoff representation itself should be routed.

Applied through `AdaptiveHandoffCodec`.

### MERA (2026)

Key lesson:

- verifier-backed replay can improve cheaper/local models and reusable skills rather than only routing around weakness;
- router, skills and model adaptation should be admitted jointly.

Applied as optional `LocalCapabilityEvolutionLoop`.

### LLM-as-Scheduler (ACL 2026)

Key lesson:

- cheap deterministic/lightweight gates can handle obvious routing decisions;
- invoke a stronger scheduler only when state is ambiguous.

Applied through the Router-of-Routers architecture.

### Chimera (2026)

Key lesson:

- route quality should account for remaining workflow work and current engine load;
- preserve assignment/locality when gains from switching are marginal.

Applied through `RemainingWorkEstimator`, load snapshots and cache-locality terms.

### ACRouter / Agent-as-a-Router (2026)

Reinforced lesson:

- execution-grounded information and memory are central to adaptive routing;
- cumulative regret is a useful streaming metric.

### Supabase current docs

Current documentation supports hybrid Postgres search using keyword FTS + pgvector semantic retrieval + RRF. This informs the optional non-secret cloud mirror while local memory remains canonical.

---

# Part XXIII — Canonical routing loop after this amendment

## 92. End-to-end selection

```text
User turn / voice
→ Repair Graph
→ IntentContract
→ CanonicalSessionState
→ task/stage fingerprint
→ CapabilityRequirementVector
→ refresh frontier catalog if stale
→ deterministic eligibility filters
    zero cost
    privacy
    terms
    context
    modality
    tools
    quota
    health
→ retrieve route experience
→ compare ModelCapabilityVectors
→ ShortfallMatcher
→ honor current TaskAffinityLease
→ compute SwitchUtility if alternate route considered
→ keep current OR host-failover OR cognitive-switch
→ ContextCompiler
→ inference with StateVersionLease
→ ResponseAdmissionGate
→ deterministic tools / tests / evidence
→ stage verification
→ terminal Done Contract
→ DelayedCreditAssigner
→ update route posterior/capabilities
→ mine high-information challenger cases
→ refresh champion/challenger state
```

## 93. Model failure loop

```text
failure
→ classify failure
→ transient?
     retry/backoff if safe
→ host problem?
     same-lineage eligible mirror
→ capability problem?
     compute cognitive SwitchUtility
→ safe checkpoint
→ snapshot Continuity Spine
→ AdaptiveHandoffCodec
→ CostProofReceipt for target
→ target ContinuityProof
→ resume
```

## 94. Frontier discovery loop

```text
provider catalogs + pricing + changelogs + gateways + discovery leads
→ candidates
→ official/account proof
→ ProviderCapabilityHandshake
→ capability canaries
→ challenger evidence
→ probation
→ specialist/champion if earned
```

---

# Part XXIV — Non-negotiable invariants

## 95. The adaptive frontier fabric must never

- spend money;
- enable paid overage;
- treat a provider Free label as proof that every model is free;
- treat a model catalog entry as proof of entitlement;
- treat a community list as proof of price;
- choose a model only because it is newest/largest;
- couple the core router permanently to model IDs;
- switch families on every transient error;
- destroy useful context/cache locality for a marginal predicted gain;
- let a stale in-flight model response mutate newer canonical state;
- forward secrets to a remote free model;
- ignore provider data-use policy;
- evade rate limits through multiple accounts/IPs/keys;
- scrape consumer browser cookies or private endpoints;
- allow a shadow challenger to mutate the live worktree;
- promote a challenger from self-reported confidence;
- route a hard task down merely because the user's French is informal or noisy;
- make Supabase, OpenRouter, Kilo or any single gateway/provider mandatory;
- count mirrors of one checkpoint as independent cognitive votes;
- bypass IntentContract, Done Contract, verification or rollback gates.

## 96. Final target behavior

For the user, the intended experience remains simple:

```text
Open AlinaCoder.exe
→ speak/write normally
→ AlinaCoder understands the real task
→ silently finds the strongest currently eligible zero-cost intelligence
→ stays on it while continuity is valuable
→ automatically uses another host if the host fails
→ automatically changes model family only when evidence justifies it
→ transfers verified state, not polluted reasoning
→ proves the new model understood the task
→ continues without making the user reconstruct the conversation
→ verifies code/tests locally
→ commits to main only after the Done Contract
```

The goal is not maximum model switching.

The goal is **maximum verified intelligence with minimum cognitive discontinuity at exactly zero autonomous monetary cost**.
