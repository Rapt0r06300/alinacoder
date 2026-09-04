# AlinaCoder v0.2 — Self-Optimizing Frontier Hunter & Seamless Failover Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment extends the existing Frontier Autopilot into a continuously learning **Self-Optimizing Frontier Hunter**.

The objective is not to accumulate a static list of “free LLMs”. The objective is for `AlinaCoder.exe` to autonomously find, prove, benchmark, rank and exploit the strongest legitimate zero-additional-cost intelligence currently usable for the exact task, while preserving the user's verified context across provider/model changes and never silently crossing into paid usage.

This amendment is normative together with the existing v0.2 baseline and later approved amendments, especially:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-routing-seamless-handoff-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-adaptive-frontier-fabric-routing-stability-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-autopilot-control-plane-hardening-amendment.md`

This amendment has higher precedence for the following subsystems:

- route identity as model × provider × serving configuration × entitlement;
- continuous frontier discovery and provider-atlas maintenance;
- shadow-first online routing policy learning;
- non-stationary contextual-bandit adaptation;
- task-level delayed terminal credit assignment;
- route-specific semantic health and quality canaries;
- congestion-aware admission control and correlated failure domains;
- adaptive delayed hedged inference;
- emission/failover commit barriers;
- quota-failure-domain accounting;
- safe route exploration and promotion;
- provider/model serving-fidelity fingerprints;
- pre-failure route forecasting and standby preparation;
- reproducible routing-decision journals and off-policy replay;
- current official zero-cost provider facts explicitly added by this amendment.

All previous safety, IntentContract, Done Contract, privacy, zero-cost, local-first, verification, rollback, resource and `main`-only Git invariants remain binding.

The absolute money policy remains:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
ALLOW_PAID_FALLBACK = false
ALLOW_AUTO_RELOAD = false
ALLOW_PURCHASED_CREDIT_CONSUMPTION = false
```

Central principle:

> **The strongest model is not a name. It is the best currently proven route cell for the current task, under current entitlement, serving configuration, continuity state, privacy policy, quota pressure and measured terminal outcomes.**

---

# Part I — The real routing unit: RouteCell

## 2. Model names are insufficient

The same checkpoint can behave materially differently depending on where and how it is served.

Differences can include:

```text
quantization / numerical precision
served context length
maximum output length
reasoning-mode support
tool/function calling behavior
JSON/schema reliability
streaming protocol
cache behavior
provider system transformations
endpoint region
latency / congestion
rate-limit pool
provider retention/training policy
fallback behavior
```

Therefore AlinaCoder must not treat `model_id` as the atomic routing identity.

## 3. RouteCell

The canonical atomic unit is:

```text
RouteCell =
  model lineage
  × provider/gateway
  × resolved endpoint
  × serving configuration
  × account entitlement
  × privacy/use-scope state
```

Minimum identity fields:

```text
route_cell_id
model_lineage_id
resolved_model_id
provider_id
gateway_id_if_any
endpoint_id
endpoint_region
serving_variant_id
quantization_or_precision_if_known
served_context_limit
served_output_limit
reasoning_modes
tool_protocol
structured_output_mode
stream_protocol
cache_semantics
account_entitlement_hash
privacy_policy_hash
license_scope_hash
billing_surface_hash
quota_failure_domain_id
infrastructure_failure_domain_id
observed_at
```

## 4. No blind score inheritance

A high score on:

```text
Model X @ Provider A
```

must not automatically promote:

```text
Model X @ Provider B
```

The second route may inherit only a conservative lineage prior.

It must earn route-specific evidence for:

```text
quality
tools
context
continuity
latency
semantic health
billing safety
privacy
```

## 5. ServingVariantFingerprint

Each route receives a `ServingVariantFingerprint` derived from:

```text
official route metadata
resolved model identifiers
provider headers where available
supported parameters
context/output limits
pricing fingerprint
protocol behavior
non-sensitive deterministic canaries
```

A material fingerprint change triggers:

```text
ROUTE_CELL_DRIFT
→ invalidate route-specific posterior
→ revoke champion status
→ re-run admission canaries
→ probation
```

## 6. RouteCell versus ModelLineage

`ModelLineage` answers:

> Which underlying cognitive family/checkpoint is this?

`RouteCell` answers:

> What exact usable service am I about to call now?

Both are required.

---

# Part II — FrontierProviderAtlas

## 7. Atlas goal

`FrontierProviderAtlas` is a live, evidence-backed inventory of all candidate zero-cost intelligence routes AlinaCoder is legitimately able to use.

It is not a hard-coded registry.

## 8. Discovery adapters

The atlas should support independent discovery adapters for:

```text
provider /models APIs
provider model-detail APIs
provider pricing APIs/pages
provider quota/usage endpoints
provider account-plan endpoints
provider changelogs
provider status pages
provider RSS/model-release feeds
gateway model catalogs
open-weight model registries
trusted benchmark feeds
community directories as lead generators only
```

## 9. Discovery source classes

```text
ACCOUNT_MACHINE_STATE
OFFICIAL_MACHINE_READABLE
OFFICIAL_DOCUMENTATION
OFFICIAL_CHANGELOG
OFFICIAL_STATUS
GATEWAY_METADATA
BENCHMARK_PRIOR
COMMUNITY_DISCOVERY_LEAD
```

Only the first six may contribute directly to runtime eligibility.

Benchmarks influence capability priors only.

Community sources can create leads only.

## 10. Atlas delta processing

Every refresh computes:

```text
new routes
retired routes
renamed routes
price changes
quota changes
privacy changes
license changes
context changes
feature changes
provider fallback changes
model identity changes
```

Each delta is typed and can invalidate only affected evidence.

## 11. FrontierChronicle

Maintain append-only history of:

```text
route appeared
route disappeared
became free
stopped being free
model remapped
provider changed limits
provider changed data policy
route quality regression detected
route restored
```

This prevents repeated rediscovery loops and supports temporal reasoning.

## 12. NegativeEvidenceCache

Known-invalid routes are remembered with expiry/recheck policy.

Examples:

```text
RETIRED
PAID
TRIAL_EXPIRED
PRIVACY_INCOMPATIBLE
LICENSE_INCOMPATIBLE
UNSUPPORTED_PROTOCOL
SEMANTICALLY_BROKEN
QUOTA_UNAVAILABLE
```

Negative evidence is refreshable, not eternal.

## 13. Catalog-independent frontier hunt

The router must be able to discover a newly released model it has never seen before.

Required process:

```text
lead discovered
→ official identity proof
→ zero-cost/billing proof
→ privacy/license proof
→ serving fingerprint
→ capability handshake
→ semantic canary
→ continuity canary
→ shadow benchmark
→ challenger probation
→ route posterior
→ champion/specialist consideration
```

No client release should be required merely to add a new OpenAI-compatible route when the existing generic adapter can support it safely.

---

# Part III — Official current free-capacity facts added on 2026-09-04

## 14. These are bootstrap facts, never permanent constants

All facts in this part must be reverified by `SourceFreshnessTrustGraph` and account-specific probes before autonomous use.

## 15. Groq Free Plan

Current official Groq documentation exposes a Free Plan with model-specific limits.

Current examples observed in official docs include:

```text
openai/gpt-oss-120b
openai/gpt-oss-20b
qwen/qwen3.6-27b
qwen/qwen3.8-27b
```

with published baseline Free Plan limits at the time of this amendment of approximately:

```text
30 RPM
1,000 RPD
8K TPM
200K TPD
```

for those listed models.

`groq/compound` and `groq/compound-mini` have different limits.

Groq explicitly states rate limits apply at the **organization level**, not per user/key.

Therefore:

```text
multiple Groq keys in same organization
!= additional independent quota
```

Account `Limits` state always outranks static docs.

## 16. Google Gemini Free Tier

Current official Gemini pricing provides selected Free Tier models with free input and output tokens.

Current official pricing examples include:

```text
gemini-3.6-flash
gemini-3.5-flash
```

with Free Tier input/output listed as free of charge.

Important caveats:

```text
only selected models/features are free
free-tier content may be used to improve Google products
search/maps grounding is not generally a free-tier capability in the same way
account/tier state must be checked
```

Free provider != all Gemini models/features free.

## 17. Cloudflare Workers AI

Current official Cloudflare documentation states:

```text
Workers Free allocation = 10,000 Neurons per day
reset = 00:00 UTC
Free plan above allocation = operations fail / upgrade required
Paid plan above allocation = billed
```

This is **allowance-based zero marginal cost**, not a claim that model token prices are intrinsically zero.

Therefore the safe route state differs by account:

```text
Workers Free + remaining neurons
→ FREE_HARD_STOP eligible

Workers Paid + remaining free allocation
→ potentially BILLING_SURFACE_UNSAFE unless a true hard zero-spend cap is independently proven
```

The exact requested model's projected neuron consumption must fit inside the remaining free reserve.

## 18. OpenRouter

Current official OpenRouter documentation provides:

```text
:free variants
openrouter/free
/api/v1/models
/api/v1/key
provider fallback for same model
model fallback support
```

Current official pricing states the Free plan includes 25+ free models and 50 requests/day under the base free account state.

Important control-plane facts:

```text
additional accounts/API keys do not legitimately multiply global rate limits
free model availability changes
provider-side 429s may cause automatic same-model provider fallback
/api/v1/key exposes account/key usage and limits
/models exposes canonical slug, context, pricing, supported params and expiry metadata
```

AlinaCoder must capture the resolved provider/model when the gateway exposes it.

`openrouter/free` is useful for discovery/fallback but is too opaque to become the authoritative quality router.

## 19. Kilo Auto Free

Current official Kilo documentation provides:

```text
kilo-auto/free
explicit :free routes
live models metadata
server-side changing model mapping
```

Current published free-model rate limit:

```text
200 requests/hour/IP
```

Current official model examples include routes such as:

```text
stepfun/step-3.7-flash:free
poolside/laguna-s-2.1:free
poolside/laguna-xs-2.1:free
nvidia/nemotron-3-ultra-550b-a55b:free
tencent/hy3:free
openrouter/free
```

The set is volatile.

Kilo explicitly warns Auto Free can route to providers that log prompts/outputs and may use them to improve services.

Therefore Auto Free is forbidden for sensitive contexts unless the exact resolved route and its data policy satisfy `ProjectSensitivityClass`.

## 20. OpenCode Zen

Current official Zen documentation exposes time-limited free routes including examples such as:

```text
mimo-v2.5-free
ling-3.0-flash-fin-free
nemotron-3-ultra-free
nemotron-3.5-lightning-free
Big Pickle
Muse Spark contributor free variants
```

The current model catalog is available through:

```text
https://opencode.ai/zen/v1/models
```

Zen explicitly documents an account auto-reload feature where a low balance may trigger a credit purchase unless auto-reload is disabled.

Therefore a `$0` Zen route remains blocked until:

```text
auto_reload_enabled = false
paid_overage_path = impossible
exact model price = 0
exact route data policy = compatible
```

## 21. Mistral Free

Current official Mistral pricing states the Free plan currently includes:

```text
$10/month in API credits
```

Official billing documentation also states monthly included usage is shared and that access beyond it depends on PayGo configuration.

Therefore Mistral Free is classified as:

```text
RECURRING_FREE_CREDIT
```

not `PERPETUAL_ZERO_PRICE_MODEL`.

Eligibility requires:

```text
remaining included credit > reserve
PayGo disabled
paid continuation impossible
project use compatible with free/evaluation terms
```

## 22. Z.AI

Current official Z.AI pricing lists:

```text
GLM-4.7-Flash = Free input / Free cached input / Free output
GLM-4.5-Flash = Free input / Free cached input / Free output
```

Current official pricing also shows:

```text
GLM-5.3-Flash != free
```

It is a paid route even though the `Flash` name may suggest otherwise.

This is a mandatory anti-assumption test:

```text
name suffix != billing proof
```

The free GLM-4.x routes can enter the atlas after account/quota/privacy/tool capability proof.

## 23. NVIDIA NIM

Current official NVIDIA NIM documentation states all model endpoints offer a free trial tier with no credit card required.

This remains:

```text
EVALUATION_TRIAL / DEVELOPMENT_TRIAL
```

not standing perpetual free capacity.

Frontier-scale model availability makes NIM a high-value opportunistic source, but expiration/use-scope/privacy restrictions remain hard gates.

## 24. Ollama Cloud

Current official Ollama pricing states:

```text
Free account includes starter usage credits
starter usage resets monthly from signup date
Free concurrency = 1
extra credits may be added
included credits are consumed before extra balance
```

Therefore `Free account` does not prove every cloud call is free.

If purchased/extra credits are present and cannot be excluded from consumption after free allowance is exhausted, the cloud route becomes ineligible under AlinaCoder's zero-autonomous-spend policy.

Local Ollama remains structurally zero monetary inference cost, subject only to local machine resources/electricity already outside API billing.

## 25. ModelScope

ModelScope API-Inference remains a useful discovery candidate for Qwen/DeepSeek/open-weight models.

Because first-party English-accessible documentation for exact free quotas/use scope is less robustly machine-verifiable than the providers above, runtime state remains:

```text
DISCOVERED_REQUIRES_OFFICIAL_ACCOUNT_PROOF
```

Third-party reports of 2,000 calls/day or specific free models cannot independently promote the route.

If authenticated official ModelScope account/catalog endpoints prove zero-cost entitlement and use scope, the route can proceed normally through the admission pipeline.

## 26. Existing providers remain eligible candidates

Existing v0.2 provider candidates remain in scope, including where live proof succeeds:

```text
SambaNova
Cloudflare
Hugging Face Inference Providers
Weights & Biases Serverless Inference
Vercel AI Gateway
OVHcloud AI Endpoints
Cohere evaluation
other legitimate newly discovered providers
```

No route is entitled to permanent trust.

---

# Part IV — OnlineRouteLearner

## 27. Why the router must learn

A hard-coded ranking becomes wrong because:

```text
new models appear
providers change serving quality
latency changes
quotas change
models silently regress
project/task mix changes
prompt scaffolds benefit models differently
tool calling differs by host
```

Routing is therefore a non-stationary online decision problem.

## 28. Contextual routing state

A routing observation may include:

```text
task family
current stage
IntentContract features
repository language/framework
required tools
required modalities
context length bucket
risk/consequence class
project sensitivity
current model affinity
remaining work estimate
current route health
quota reserve
latency state
continuity state
known knowledge freshness
```

No raw secret-bearing prompt text is required for the learning state.

## 29. Arms

The candidate action is not simply a model.

Conceptually:

```text
arm = RouteCell × ComputationRegime
```

The implementation may factor this hierarchically for sample efficiency.

## 30. Reward

The strongest learning signal is delayed terminal outcome.

Example reward components:

```text
Done Contract passed
correct tests passed
regressions absent
user correction rate
number of recovery loops
verification confidence
intent fidelity
terminal latency
continuity failures
quota consumed
```

No provider marketing score or LLM self-confidence can dominate terminal evidence.

## 31. Terminal reward before turn-level vanity

For agentic coding tasks:

```text
“produced plausible text quickly”
```

is not success.

Credit assignment must emphasize:

```text
verified task completion
```

rather than individual response attractiveness.

## 32. Delayed/out-of-order feedback

Tasks can finish out of order.

Each decision records:

```text
routing_decision_id
task_id
canonical_state_version
chosen arm
policy version
eligible arm set
selection probability if stochastic
```

When terminal feedback arrives later, it updates only the correct decision lineage.

## 33. Non-stationarity

The learner must not assume old outcomes remain equally relevant forever.

Use one or more conservative mechanisms:

```text
recency weighting
geometric forgetting
sliding windows
change-point reset
identity-fingerprint reset
```

Abrupt verified model/price/serving changes should trigger explicit reset rather than relying only on slow decay.

## 34. Cold-start prior

New routes start with:

```text
external capability priors
lineage priors
provider reliability priors
strict uncertainty
```

but not champion status.

A model that looks spectacular on a public leaderboard must still earn AlinaCoder-specific evidence.

---

# Part V — Shadow-first router evolution

## 35. RouterDeploymentMode

Every materially new routing policy progresses through:

```text
OFFLINE_REPLAY
SHADOW_LEARN
LIMITED_ACTION
ACTIVE
QUARANTINED
ROLLED_BACK
```

## 36. OFFLINE_REPLAY

Replay historical task decisions using recorded route metadata and outcomes.

Measure:

```text
counterfactual disagreement
estimated utility
estimated quota use
predicted switch count
predicted continuity risk
```

Counterfactual estimates are screens, not proof.

## 37. SHADOW_LEARN

The candidate policy sees live routing contexts and records:

```text
would_have_selected
why
confidence
eligible_set
```

but cannot influence user traffic.

This detects obvious policy pathologies at zero mutation risk.

## 38. LIMITED_ACTION

A candidate policy may serve a tightly bounded eligible slice only after:

```text
minimum shadow sample
no policy violations
route eligibility stable
rollback available
```

High-consequence tasks can remain excluded until further evidence.

## 39. ACTIVE

Promotion requires measured on-policy terminal outcomes.

A shadow direct-method estimate alone can never establish final superiority.

## 40. One-flag rollback

The router architecture must retain a deterministic safe fallback policy that can be restored atomically.

A router learning bug must never strand AlinaCoder.

---

# Part VI — Safe exploration

## 41. Exploration is necessary but bounded

Without exploration, a new stronger free model may never receive traffic.

Uncontrolled exploration can damage task quality or exhaust free quota.

Therefore exploration is treated as a governed resource.

## 42. Exploration classes

```text
OFFLINE_REPLAY_EXPLORATION
SHADOW_EXPLORATION
CANARY_EXPLORATION
DISPOSABLE_READ_ONLY_EXPLORATION
VERIFIED_PARALLEL_CHALLENGER
LIVE_ACTION_EXPLORATION
```

## 43. Default exploration order

Prefer:

```text
offline
→ shadow
→ synthetic/hidden canary
→ read-only real tasks
→ verified parallel challenger
→ limited action
```

before exposing high-risk mutation work.

## 44. Mutation-risk rule

A novel route may propose code on a candidate workspace, but its proposal cannot mutate the canonical worktree until deterministic verification and existing mutation gates pass.

Thus even exploratory cognition remains separated from canonical action.

## 45. Protected quota

Exploration cannot consume:

```text
PRODUCTION_RESERVE
RECOVERY_RESERVE
```

unless the current user task itself is the reason for that call.

## 46. Exploration stopping

Stop exploring an arm when evidence shows:

```text
material capability deficit
semantic health deficit
privacy incompatibility
continuity incompatibility
quota inefficiency
repeated tool/schema failure
```

Do not waste requests merely to finish a benchmark quota.

---

# Part VII — Semantic health, not HTTP health

## 47. 200 OK is not healthy

Providers/models can return:

```text
empty output
garbage output
wrong language
broken JSON
invalid tool schema
truncated reasoning
unexpected refusal
wrong model
severe quality regression
```

while the HTTP endpoint remains technically up.

## 48. QualityHealthCell

Track route health dimensions separately:

```text
transport_health
latency_health
protocol_health
schema_health
tool_health
semantic_health
continuity_health
billing_health
identity_health
```

## 49. Quality canaries

Use a tiny deterministic, non-sensitive canary suite appropriate to the route's intended role.

Examples:

```text
strict JSON echo contract
tool-call schema microtask
small code transformation
French instruction fidelity
context-retention probe
negative-instruction test
```

Canaries must be low-cost and quota-aware.

## 50. Canary frequency

Canary cadence is adaptive:

```text
stable high-traffic route
→ infer health mostly from real traffic

new/volatile route
→ more explicit canaries

scarce quota
→ fewer proactive canaries

recent incident
→ targeted recovery canaries
```

## 51. Real traffic is evidence

Successful verified real tasks can satisfy health observations and reduce synthetic canary needs.

## 52. Failure is signal

Do not silently discard:

```text
timeouts
schema failures
tool errors
continuity failures
semantic garbage
```

These become bounded negative observations in route reliability learning.

---

# Part VIII — ProviderCongestionController

## 53. Failover can create a thundering herd

If Provider A degrades and all requests instantly jump to B, Provider B can be overloaded, causing oscillation B→C→A.

Per-route circuit breakers alone are insufficient.

## 54. Congestion tokens

Maintain dynamic admission capacity per real provider/quota/failure domain.

A practical control law may use AIMD-style behavior:

```text
successful stable traffic
→ additive capacity increase

429 / overload / tail-latency breach
→ multiplicative decrease
```

Exact parameters must be tuned from replay/chaos tests.

## 55. Failure-domain admission

Capacity is attached to actual shared resources, not just API keys.

Examples:

```text
provider organization quota
gateway free-tier quota
underlying upstream provider pool
shared IP quota
model-specific pool
```

## 56. Priority classes

```text
P0_RECOVERY
P1_ACTIVE_USER_CRITICAL
P2_ACTIVE_USER_NORMAL
P3_VERIFIER
P4_CHALLENGER
P5_BACKGROUND_RESEARCH
P6_DISCOVERY_CANARY
```

Under congestion, shed lowest priority first.

## 57. Background work must yield

Provider discovery, challenger benchmarks and freshness scans must not crowd out the active user's work.

## 58. Reset headers

Use provider-provided:

```text
Retry-After
x-ratelimit-remaining-*
x-ratelimit-reset-*
```

when authoritative.

Do not guess reset timing if the provider exposes it.

---

# Part IX — QuotaFailureDomainGraph

## 59. Keys are not quotas

Multiple keys can share one organization/account/IP quota.

`QuotaFailureDomainGraph` represents this explicitly.

## 60. Quota nodes

Examples:

```text
provider-account
organization
workspace
project
IP
model family
specific endpoint
gateway upstream
```

## 61. Capacity independence

Two routes count as independent recovery capacity only when their limiting quota/failure domains are sufficiently independent.

Example:

```text
OpenRouter free route A
OpenRouter free route B
```

may share OpenRouter's daily free cap even when underlying models differ.

They are cognitive alternatives, not fully independent quota batteries.

## 62. No quota evasion

AlinaCoder never creates or rotates multiple accounts, keys or IPs to circumvent provider limits.

The graph exists to correctly understand legitimate capacity, not evade quotas.

---

# Part X — CorrelatedFailureGraph

## 63. Provider diversity can be fake

Different gateways can route to the same underlying provider or same infrastructure.

Same model on several gateways may fail together.

## 64. Failure correlation

Record observed correlations in:

```text
CorrelatedFailureGraph
```

Edges can represent:

```text
same upstream
same gateway
same cloud region
same auth domain
same quota domain
same model deployment
observed simultaneous failures
```

## 65. Standby selection

When possible, the first standby should reduce both:

```text
cognitive shortfall
AND
failure correlation
```

not merely select the next-highest score.

---

# Part XI — Predictive standby and route forecasting

## 66. Do not wait for failure

`RouteRiskForecast` estimates near-term risk using signals such as:

```text
remaining requests/tokens
reset time
recent 429 frequency
TTFT p50/p95 trend
timeout trend
semantic canary trend
error burstiness
provider status changes
catalog deprecation date
credit expiry
```

## 67. Forecast states

```text
STABLE
PRESSURE_RISING
QUOTA_AT_RISK
LATENCY_DEGRADING
QUALITY_DEGRADING
RETIREMENT_IMMINENT
FAILURE_LIKELY
```

## 68. Prewarm behavior

When risk rises:

```text
refresh standby proof
refresh StandbyStateCapsule
verify alternate route health
reserve recovery quota
```

without switching immediately.

This reduces recovery latency while preserving task affinity.

## 69. Forecast does not overrule evidence

Prediction alone cannot trigger unnecessary cognitive switching when current route remains healthy and continuity value is high.

It prepares options; `SwitchUtility` still decides.

---

# Part XII — AdaptiveHedgeController

## 70. Hedging purpose

For some pure/read-only inference calls, tail latency can be reduced by issuing a delayed duplicate to an independent route and accepting the first valid response.

This is optional and tightly constrained.

## 71. Never hedge blindly

Hedging is forbidden when:

```text
request can cause side effects
a tool may mutate external state
both calls cannot be proven zero-cost
quota reserve is scarce
privacy policy differs incompatibly
a duplicate could create contradictory user-visible actions
```

## 72. Delayed hedge

Do not launch two requests immediately by default.

Use a dynamic delay such as a measured route-specific TTFT percentile:

```text
primary starts
→ if no first valid token before adaptive hedge threshold
→ launch verified standby
→ first valid response wins
→ cancel loser
```

## 73. Hosting hedge preferred

First preference:

```text
same cognitive lineage
+ independent hosting/failure domain
```

because this preserves semantic continuity while reducing hosting tail risk.

## 74. Cross-model hedge

Different-model hedging requires a deterministic or independent response selector and enough quota.

It is reserved for cases where terminal gain justifies the duplication.

## 75. Hedge accounting

Both calls count against:

```text
quota treasury
provider congestion
route posterior
```

Cancelled calls are not assumed free in quota terms.

---

# Part XIII — EmissionCommitBarrier

## 76. Streaming changes failover semantics

Before user-visible/canonical emission, a route can fail transparently and be replaced.

After accepted output has begun, silently swapping to a cognitively different model can create contradictions.

## 77. Emission states

```text
PRE_EMISSION
EMITTING_UNCOMMITTED
EMITTED_TO_USER
CANONICAL_ACTION_COMMITTED
```

## 78. PRE_EMISSION failover

Safe transparent retry/failover may occur if:

```text
no canonical mutation
no user-visible semantic commitment
state lease still valid
```

## 79. Post-emission cognitive failover

If the current model fails after meaningful output has been exposed:

```text
freeze canonical action
mark generation interrupted
rehydrate target from canonical state + accepted emitted facts only
resume/restart with explicit continuity repair
```

Do not concatenate arbitrary partial generations from different models.

## 80. Tool-call barrier

A tool call becomes actionable only after:

```text
complete payload
schema validation
state-version validation
policy validation
```

Partial streamed tool arguments are never executed.

---

# Part XIV — Task-level affinity plus evidence-based stage switching

## 81. Task consistency remains valuable

Recent agentic routing research shows task-level delayed outcomes often provide a better signal than per-call routing.

Therefore `TaskAffinityLease` remains default.

## 82. But permanent task pinning is not absolute

Some long tasks have genuinely different stages.

A switch can occur only at safe checkpoints when evidence shows:

```text
stage capability mismatch
repeated verified failure
modality change
context ceiling risk
route health degradation
quota exhaustion risk
material expected terminal gain
```

## 83. Error tolerance

A single transient formatting/tool error should not automatically cause cognitive failover.

Prefer:

```text
repair prompt
protocol adapter recovery
same-route retry if safe
same-lineage hosting failover
```

before cognitive lineage change when evidence suggests recoverability.

## 84. Switch tax is explicit

Include:

```text
rehydration cost
cache loss
continuity risk
new-model warmup risk
additional quota
remaining task horizon
```

in `SwitchUtility`.

---

# Part XV — Correlation-aware learning

## 85. Route outcomes are correlated

Closely related models/routes can provide partial information about one another.

Example:

```text
same model lineage on two hosts
related model family
same provider serving configs
```

## 86. Surrogate evidence is never true reward

A correlation model may predict likely performance of uncalled routes.

Keep:

```text
true_observed_reward
```

separate from:

```text
surrogate_predicted_reward
```

## 87. Prediction mixing

Use surrogate signals to improve sample efficiency only if calibrated.

If surrogate reliability falls:

```text
reduce its weight
or ignore it
```

True terminal outcomes remain authoritative.

## 88. RouteLineageTransferPrior

A new host of a known model can receive a cautious prior based on lineage, but host-specific serving evidence must dominate after observations accumulate.

---

# Part XVI — RoutingDecisionJournal

## 89. Every important routing choice must be reproducible

Persist a structured routing decision containing:

```text
decision_id
timestamp
policy_version
canonical_state_version
IntentContract hash
current stage
future-stage forecast hash
capability requirement vector
knowledge freshness requirement
eligible routes
rejected routes + reasons
billing proof hashes
privacy/license proof hashes
quota snapshot
health snapshot
route fingerprints
posterior/score per candidate
switch utility
chosen route
standby chain
computation regime
exploration flag
selection probability if stochastic
```

## 90. No secret prompt storage required

The journal can store derived, redacted routing features and hashes rather than sensitive prompt bodies.

## 91. Replay

The journal supports:

```text
router regression tests
off-policy screening
incident reconstruction
route regret analysis
policy version comparison
```

## 92. CounterfactualOffPolicyEvaluator

Estimate what alternative policies might have done using:

```text
logged outcomes
shadow decisions
challenger results
calibrated surrogate reward
```

Counterfactual estimates are explicitly labeled estimates.

Promotion still requires real measured evidence where risk warrants it.

---

# Part XVII — Anti-reward-hacking

## 93. The router can optimize the wrong target

A learner could select models that:

```text
produce pretty answers
pass weak judges
avoid hard tasks
use fewer tools
terminate early
```

while failing the user's actual goal.

## 94. Reward hierarchy

Prefer evidence in this order:

```text
1. deterministic Done Contract
2. tests / build / runtime verification
3. user-corrected terminal outcome
4. independent verifier evidence
5. task-specific objective metrics
6. calibrated judge/proxy scores
7. model self-report
```

## 95. Abstention is not failure when correct

A route that honestly detects insufficient evidence may outperform a hallucinating route.

Calibrated abstention can receive positive reliability credit when it prevents unsafe incorrect mutation.

## 96. Completion gaming detector

Watch for patterns such as:

```text
premature “done”
skipping verification
reducing test scope
changing acceptance criteria
ignoring user constraints
```

Such outcomes receive severe negative reward even if text appears confident.

---

# Part XVIII — ProviderSafeContextProjection

## 97. Best free route may have weaker data policy

Some current free/trial routes explicitly permit logging or model improvement use.

Therefore route quality is conditional on what context can legally/safely be sent.

## 98. Context projection

`ProviderSafeContextProjection` derives a minimum sufficient packet based on:

```text
ProjectSensitivityClass
provider data policy
route role
required symbols/files
authorized externalization scope
```

## 99. Projection rules

Potentially remove/redact:

```text
secrets
credentials
personal data
unneeded proprietary files
private comments/history
unrelated logs
```

before remote inference.

## 100. Projection adequacy

If redaction removes information essential to correct reasoning:

```text
route becomes capability-ineligible for that task
```

rather than sending prohibited context anyway.

## 101. Local fallback

Sensitive projects can remain local-only even when a stronger cloud model exists.

Privacy is a hard eligibility dimension, not a quality penalty.

---

# Part XIX — ProviderCapabilityManifest

## 102. Generic adapters need machine-readable capability

For each provider/route, normalize:

```text
chat/completions support
responses support
messages support
streaming
tool calling
parallel tools
strict JSON/schema
vision/audio/pdf
reasoning controls
seed/determinism controls
context length
output length
usage accounting
rate-limit headers
resolved-provider metadata
cancellation
idempotency semantics
```

## 103. Protocol normalization

`ProtocolAdapter` translates from AlinaCoder's canonical request into provider-native format.

Provider-native quirks must not leak into canonical reasoning state.

## 104. Manifest drift

If `/models` or capability metadata changes:

```text
manifest hash changes
→ affected capability proof stale
→ canary required
```

## 105. Capability false positives

A provider advertising tools is not sufficient.

Actual tool reliability must be measured.

---

# Part XX — Model/route promotion proof

## 106. Promotion pipeline

```text
DISCOVERED
→ OFFICIALLY_VERIFIED
→ COST_SAFE
→ PRIVACY_LICENSE_SAFE
→ FINGERPRINTED
→ PROTOCOL_CANARY_PASS
→ SEMANTIC_CANARY_PASS
→ CONTINUITY_CANARY_PASS
→ SHADOW_EVALUATED
→ CHALLENGER
→ PROBATION
→ SPECIALIST_OR_CHAMPION
```

## 107. Promotion is task-family specific

A route may be:

```text
champion for debugging
weak for tool use
specialist for research
ineligible for sensitive code
```

No universal badge is required.

## 108. Demotion

Immediate demotion triggers include:

```text
billing uncertainty
identity drift
privacy/terms change
severe semantic regression
repeated protocol failures
continuity failure
```

Gradual performance decline can be handled through posterior decay and challenger comparison.

---

# Part XXI — FreeRoute strength ranking

## 109. Strongest-free ranking is multi-objective

A conservative utility can depend on:

```text
P(verified terminal success)
continuity probability
semantic health
latency distribution
remaining quota
privacy/license eligibility
stage fit
future-stage fit
switch tax
failure correlation
```

Monetary cost is not a soft dimension because eligible routes must already equal zero autonomous spend.

## 110. Lexicographic hard gates

Before quality scoring:

```text
billing safe?
privacy safe?
license/use scope safe?
protocol minimally compatible?
state lease valid?
quota reserve sufficient?
```

If any hard gate fails, the route is removed rather than merely penalized.

## 111. Confidence-adjusted quality

Prefer a slightly lower mean with strong evidence over an untested spectacular mean when task risk is high.

For low-risk exploration, uncertainty can justify challenger trials.

---

# Part XXII — Continuity strengthening

## 112. Canonical state remains model-independent

Never transfer raw hidden chain-of-thought as the canonical continuity mechanism.

Transfer:

```text
verified facts
accepted decisions
IntentContract
constraints
plan graph
current repo state
observed errors
disproven hypotheses
artifacts
next safe action
```

## 113. ContinuityDeltaJournal

Between full checkpoints, append verified deltas:

```text
STATE_FACT_ADDED
DECISION_ACCEPTED
HYPOTHESIS_REJECTED
FILE_CHANGED
TEST_RESULT
INTENT_CORRECTION
ROLLBACK_POINT
```

## 114. Incremental capsule update

`StandbyStateCapsule` is refreshed using deltas, avoiding expensive full-history summarization on every turn.

## 115. Semantic checksums

Important continuity objects receive hashes/versions:

```text
intent hash
constraint hash
repo state hash
plan hash
verified evidence hash
```

Incoming models must acknowledge expected versions.

## 116. ContinuityProof enhancement

A takeover should answer structured questions such as:

```text
What exactly is the user's goal now?
What was explicitly cancelled or superseded?
What must never happen?
What repo/HEAD is current?
What facts are proven?
What hypotheses already failed?
What is the next safe action?
What would require rollback?
```

Failure blocks mutation.

## 117. State compatibility adapter

If a provider/model has special conversation-state semantics, translate from canonical state.

Never make canonical state depend on one provider's opaque session.

---

# Part XXIII — Supabase optional FrontierEvidenceBus

## 118. Local state remains canonical

No Supabase dependency is required for AlinaCoder to run.

Local SQLite/event log remains authoritative.

## 119. PGMQ role

Current Supabase Queues documentation supports durable Postgres-native queues with visibility windows, guaranteed delivery and archival.

Optional queues:

```text
frontier_discovery_jobs
provider_fact_refresh_jobs
route_canary_jobs
route_identity_probe_jobs
shadow_evaluation_jobs
policy_replay_jobs
```

## 120. Visibility leases

Slow provider probes use a visibility timeout appropriate to expected duration.

If worker dies:

```text
message becomes visible again
→ safe retry
```

## 121. Queue retry telemetry

Use fields/metrics such as:

```text
read_ct
queue_length
oldest_msg_age
```

to detect poison/stuck discovery jobs.

## 122. Archive

Successful/failed non-secret probe metadata can be archived for audit and learning.

## 123. Supabase Realtime role

Realtime Broadcast can be used only for ephemeral notifications such as:

```text
“new provider fact available”
“canary completed”
“route quarantined”
```

It must not become canonical persistence.

Current Supabase docs note database broadcast messages have finite retention; durable truth belongs in normal tables/queues/local state.

## 124. Cloud outage behavior

Supabase outage:

```text
→ background distributed evidence sync pauses
→ local router keeps operating from verified local evidence/TTL policy
```

---

# Part XXIV — Local/open-weight frontier hunt

## 125. Free hosted is not the only frontier

Open-weight models may improve enough that a locally runnable model becomes the strongest eligible route for some tasks.

## 126. Hardware-fit gate

Before downloading/loading a model, estimate:

```text
VRAM
RAM
disk
download size
quantization
context memory
expected tokens/sec
other running workloads
```

## 127. Giant model restraint

A model being open-weight does not mean it is practical on the user's machine.

Do not automatically download hundreds of gigabytes merely because a benchmark is attractive.

## 128. Quantization is a new RouteCell

Different local quantizations receive distinct fingerprints and capability evidence.

A Q4 route must not inherit full-precision capability scores blindly.

## 129. Local champion advantage

Local routes can receive substantial practical value from:

```text
privacy
unlimited API requests
offline resilience
predictable availability
zero external quota
```

but quality remains measured rather than assumed.

---

# Part XXV — Adaptive context length and long-task survival

## 130. Served context, not advertised context

Use the context length actually supported by the exact RouteCell.

## 131. Preflight context budget

Before routing:

```text
canonical context tokens
expected tool-output growth
expected response tokens
safety margin
```

must fit.

## 132. Long-task route risk

A route that fits the current turn but will likely overflow before the next critical stage can be inferior to a slightly slower larger-context route.

`FutureStageForecast` includes context survival.

## 133. Context compaction neutrality

Compaction is performed from canonical verified state, not from whichever model happens to be active.

---

# Part XXVI — Router policy architecture

## 134. Recommended layered selector

Canonical conceptual stack:

```text
HardPolicyGate
→ AtlasRetriever
→ RouteEligibilityFilter
→ Capability/Knowledge Matcher
→ SemanticHealthFilter
→ Failure/Quota Forecast
→ RoutePosterior
→ OnlineRouteLearner
→ TaskAffinity/SwitchUtility
→ ComputationRegimeRouter
→ CongestionAdmission
→ Standby Planner
→ final route
```

## 135. Graceful degradation

If advanced learning state is unavailable:

```text
bandit policy unavailable
→ posterior/rule scorer

posterior unavailable
→ capability matcher

external atlas unavailable
→ last verified local registry

all external routes unavailable
→ local eligible route
```

The system must become simpler, not unsafe.

## 136. Router latency budget

Routing itself should remain tiny relative to model inference.

Expensive deep search is used only when expected terminal value justifies it.

---

# Part XXVII — Failure taxonomy extension

## 137. Route failures

Add typed failures:

```text
TRANSPORT_FAILURE
AUTH_FAILURE
PAYMENT_REQUIRED
RATE_LIMIT
PROVIDER_OVERLOAD
MODEL_RETIRED
MODEL_IDENTITY_DRIFT
SERVING_VARIANT_DRIFT
CONTEXT_LIMIT_CHANGED
PROTOCOL_REGRESSION
TOOL_REGRESSION
SEMANTIC_REGRESSION
PRIVACY_POLICY_DRIFT
LICENSE_DRIFT
QUOTA_DOMAIN_EXHAUSTED
CORRELATED_FAILURE_EVENT
CONTINUITY_FAILURE
EMISSION_INTERRUPTED
```

## 138. Failure-specific response

Do not treat all failures as “switch model”.

Examples:

```text
429
→ congestion/quota handling

schema malformed once
→ protocol repair/retry

same model provider outage
→ hosting failover

repeated semantic regression
→ cognitive route demotion

billing uncertainty
→ hard quarantine
```

---

# Part XXVIII — Current frontier candidates versus current free routes

## 139. Distinguish frontier intelligence from free availability

Current frontier/open model families worth continuously tracking include examples such as:

```text
Kimi K3
DeepSeek V4 Pro / Flash
GLM-5.3 / GLM-5.3-Flash
Qwen3.8 family
Nemotron 3 Ultra / Super / Lightning
Poolside Laguna coding models
GPT-OSS-120B
new releases discovered later
```

But **tracking a frontier model does not make it eligible**.

## 140. Four separate questions

For every frontier model:

```text
1. Is it strong?
2. Is there a legitimate route currently accessible?
3. Is that exact route zero autonomous monetary cost right now?
4. Is the route privacy/license/quota/continuity compatible with this task?
```

Only “yes” to all required questions makes it actionable.

## 141. Example: GLM-5.3-Flash

Current Z.AI official pricing:

```text
strong current-generation candidate
but paid API route
```

Therefore it remains tracked in `FrontierChronicle` but is excluded from autonomous remote use under zero-spend policy unless another independent provider legitimately exposes that exact model at verified zero cost and compatible terms.

## 142. Example: Nemotron 3 Ultra

May appear through multiple current free/trial gateways.

Each host is separately evaluated.

One route can be eligible while another is blocked for billing/privacy/trial scope.

---

# Part XXIX — Acceptance scenarios

## 143. Route identity

1. Same model served by two providers with different context limits → two RouteCells.
2. Provider B quantizes model more aggressively and coding quality drops → only B is demoted.
3. `latest` alias changes checkpoint → fingerprint reset prevents inherited champion status.
4. Gateway switches hidden upstream → identity confidence drops until resolved/canary passes.

## 144. Frontier discovery

5. New free coding model appears in official `/models` → discovery lead enters admission automatically.
6. Community directory finds model first → lead stored, but no inference until official proof.
7. Provider removes free price → route quarantined before next call.
8. Provider restores a free route later → stale negative evidence expires and reevaluation is allowed.

## 145. Billing

9. Cloudflare Workers Free has enough neuron allowance → request can be eligible.
10. Same Cloudflare account is Paid and excess would bill → route blocked unless hard zero-spend cap is proven.
11. Mistral Free has included credit remaining and PayGo disabled → route eligible subject to other gates.
12. Mistral included credit depleted → route stops; no PayGo fallback.
13. Zen free model with auto-reload enabled → blocked.
14. Zen auto-reload disabled and exact free route verified → may proceed.
15. Z.AI GLM-4.7-Flash currently zero-priced → may proceed after account/limits/privacy checks.
16. Z.AI GLM-5.3-Flash name contains Flash but price > 0 → rejected.

## 146. Quota/failure domains

17. Two Groq API keys share same organization → no false double capacity.
18. Two OpenRouter models share same daily free account cap → treasury counts shared cap.
19. Direct provider plus independent gateway route have distinct quota domains → legitimate redundancy may be counted.
20. Background canary traffic approaches reserve floor → canaries suspended.

## 147. Semantic health

21. Endpoint returns HTTP 200 but invalid JSON repeatedly → protocol health opens circuit.
22. Endpoint returns valid JSON but fails deterministic canary → semantic route demoted.
23. Provider latency spikes but quality remains good → congestion controller reduces admissions before cognitive demotion.

## 148. Online learning

24. New policy disagrees with production router in shadow mode → no user impact.
25. Shadow policy looks promising but off-policy estimate uncertain → limited action trial, not immediate promotion.
26. Limited-action terminal outcomes outperform baseline → gradual promotion.
27. New route wins synthetic benchmark but performs poorly on real Done Contracts → real-task posterior demotes it.
28. Model quality drifts slowly under same ID → recency weighting adapts.
29. Model identity jumps → immediate arm reset.

## 149. Task affinity

30. One malformed tool call occurs → repair/retry before model switch.
31. Three verified stage-specific failures occur and alternate route predicts large gain → checkpoint cognitive switch allowed.
32. Next stage needs vision but current model is text-only → planned safe switch.

## 150. Hedging

33. Read-only inference crosses p95 TTFT and independent zero-cost standby exists → delayed hedge allowed.
34. Primary returns first valid response → hedge cancelled.
35. Request may execute Git/tool mutation → hedging forbidden.
36. Hedge would consume recovery reserve → hedge forbidden.

## 151. Streaming continuity

37. Provider fails before first accepted token → transparent failover allowed.
38. Provider fails after user-visible semantic content → explicit continuity repair/restart, no silent concatenation.
39. Tool arguments stream partially → never executed.
40. User corrects intent while hedge response is pending → both stale leases rejected.

## 152. Privacy

41. Auto Free route permits training on prompts and project is sensitive → route ineligible.
42. Safe projection can remove sensitive context while preserving task sufficiency → route may be used with projected packet.
43. Required proprietary code cannot be safely projected → local/private route chosen.

## 153. Supabase

44. PGMQ canary worker crashes → message becomes visible after VT and retries.
45. Poison canary repeatedly fails → read count/age triggers quarantine instead of infinite retry.
46. Realtime notification is missed → durable queue/local state still contains truth.
47. Supabase is offline → active local router continues.

## 154. Correlated outage

48. Two gateways fail because of same upstream → correlation graph learns relation.
49. Next standby prefers a different upstream/failure domain when quality is sufficient.
50. All cloud routes fail → local Ollama path continues under existing local capability rules.

---

# Part XXX — New metrics

## 155. Route quality metrics

```text
route_cell_verified_terminal_done_rate
route_cell_tool_success_rate
route_cell_schema_success_rate
route_cell_semantic_canary_rate
route_cell_continuity_rate
route_cell_ttft_p50
route_cell_ttft_p95
route_cell_tokens_per_second
route_cell_context_survival_rate
```

## 156. Router learning metrics

```text
routing_regret
switch_regret
policy_disagreement_rate
shadow_predicted_gain
limited_action_measured_gain
on_policy_terminal_gain
exploration_value_per_request
new_route_time_to_useful_evidence
new_route_false_promotion_rate
stale_posterior_correction_latency
```

## 157. Reliability metrics

```text
semantic_failure_detection_latency
provider_congestion_recovery_time
correlated_failover_escape_rate
hedge_activation_rate
hedge_win_rate
hedge_wasted_quota
pre_failure_standby_success_rate
emission_interruption_rate
post_emission_continuity_repair_rate
```

## 158. Zero-cost metrics

Hard targets:

```text
paid_autonomous_calls = 0
purchased_credit_autonomous_consumption = 0
auto_reload_triggered_by_alinacoder = 0
false_free_route_admissions = 0
quota_evasion_actions = 0
```

## 159. Privacy metrics

Hard targets:

```text
secret_leak_to_provider = 0
sensitivity_policy_violations = 0
provider_context_overprojection = 0
```

---

# Part XXXI — New conceptual modules

## 160. Suggested additions

```text
src/alinacoder/intelligence_mesh/
  frontier_provider_atlas.py
  route_cell.py
  serving_variant_fingerprint.py
  frontier_chronicle.py
  online_route_learner.py
  router_policy_modes.py
  safe_exploration.py
  semantic_health.py
  provider_congestion.py
  quota_failure_domains.py
  correlated_failure_graph.py
  route_risk_forecast.py
  adaptive_hedging.py
  emission_barrier.py
  routing_decision_journal.py
  off_policy_evaluator.py
  reward_integrity.py
  provider_safe_context.py
  provider_capability_manifest.py
  route_promotion.py

src/alinacoder/continuity/
  continuity_delta_journal.py
  semantic_checksums.py
  takeover_proof.py

src/alinacoder/evaluation/
  shadow_router_replay.py
  route_cell_canary.py
  serving_drift_bench.py
  semantic_health_bench.py
  congestion_chaos_bench.py
  hedge_bench.py
  emission_failover_bench.py
  quota_domain_bench.py
  correlated_outage_bench.py
```

Names are conceptual and may be reorganized without weakening the contracts.

---

# Part XXXII — Recommended implementation sequence

## 161. Phase A — RouteCell foundation

Implement:

```text
RouteCell
ServingVariantFingerprint
ProviderCapabilityManifest
QuotaFailureDomainGraph
```

before advanced learning.

## 162. Phase B — Atlas

Implement official-first live discovery and evidence deltas.

Integrate generic OpenAI-compatible `/models` adapters where safe.

## 163. Phase C — Semantic health

Implement route-specific canaries and semantic health before autonomously expanding provider count.

## 164. Phase D — Decision journal

Persist routing decisions and terminal outcomes before enabling online learning.

Learning without auditable data is forbidden.

## 165. Phase E — Shadow learner

Implement offline replay + `SHADOW_LEARN`.

No policy influence yet.

## 166. Phase F — Limited online adaptation

Enable constrained contextual-bandit/challenger decisions only behind strict gates.

## 167. Phase G — Congestion and predictive standby

Add AIMD-style provider admission, failure-domain awareness and route forecasting.

## 168. Phase H — Adaptive hedging

Only after idempotency/emission barriers are proven.

## 169. Phase I — Advanced correlated learning

Add calibrated surrogate/correlation learning only if measured sample-efficiency gains justify complexity.

---

# Part XXXIII — Research basis added by this amendment

## 170. TRACE-Router (2026)

Recent research on task-consistent adaptive routing reports benefits from:

```text
one task-level backend affinity
terminal delayed reward
context-conditioned online bandits
reduced per-call thrashing
```

Applied here through `TaskAffinityLease`, delayed terminal learning and safe checkpoint stage switches.

## 171. MTRouter (ACL 2026)

MTRouter reports that effective multi-turn routing can make fewer switches, tolerate transient errors and develop model specialization.

Applied here through:

```text
error-tolerant affinity
switch-tax accounting
stage-specialist evidence
```

## 172. OrcaRouter (2026)

Production-oriented contextual-bandit routing with offline warmup and optional online adaptation supports:

```text
changing model pools
partial-feedback learning
UCB/Thompson/exploration comparisons
```

Applied through the shadow-first `OnlineRouteLearner`.

## 173. ParetoBandit (2026)

ParetoBandit explicitly addresses:

```text
non-stationary quality/pricing
runtime model onboarding
geometric forgetting
budget pacing
```

AlinaCoder adapts these ideas to a zero-money setting where the scarce resource is primarily **free quota/recovery capacity**, not allowable dollars.

## 174. WISERouter / SeqRoute (2026)

Workload/session-level budget research shows that greedy per-request consumption can exhaust resources before later critical turns.

Applied here through:

```text
FreeQuotaTreasury
FutureStageForecast
protected recovery reserve
workload/session horizon awareness
```

## 175. Correlation-aware contextual bandits (2026)

Recent research indicates correlated arms and surrogate rewards can improve sample efficiency, but misspecified surrogates can harm routing.

Applied here by separating:

```text
observed terminal reward
from
surrogate route prediction
```

and requiring calibration.

## 176. ContinuityBench (2026)

Current multi-provider failover research separates availability from state continuity.

Applied through:

```text
ContinuitySpine
StandbyStateCapsule
ContinuityDeltaJournal
ContinuityProof
EmissionCommitBarrier
```

## 177. Routing security research (ACL 2026)

Existing v0.2 control-plane safeguards remain mandatory because routing itself is adversarially manipulable.

The new online learner cannot consume untrusted prompt instructions as privileged policy features.

## 178. Production resiliency patterns

Current multi-provider engineering patterns reinforce:

```text
same-model provider failover
circuit breakers
exponential backoff + jitter
adaptive delayed hedging
first-valid-response wins
congestion-aware admission
```

AlinaCoder adds zero-cost, continuity and idempotency constraints around those patterns.

## 179. Official provider sources checked for this amendment

Current first-party documentation reviewed includes:

```text
Groq rate limits
Google Gemini API pricing/rate limits
Cloudflare Workers AI pricing
OpenRouter limits/models/free router
Kilo Auto Free/models/cost safeguards
OpenCode Zen pricing/models/auto-reload/data handling
Mistral pricing/subscriptions/usage limits
Z.AI pricing/model docs
NVIDIA NIM model API docs
Ollama Cloud pricing
Supabase Queues/PGMQ/Realtime documentation
```

Community directories were used only to increase discovery recall and identify candidates requiring official verification.

---

# Part XXXIV — Canonical autonomous loop after this amendment

## 180. Frontier Hunter loop

```text
Receive user intent
→ IntentContract / sensitivity / stage
→ canonical state lease
→ FrontierProviderAtlas refresh if evidence stale
→ SourceFreshnessTrustGraph
→ route-cell construction
→ BillingSurfaceGuard
→ privacy/license/use-scope gate
→ ProviderSafeContextProjection
→ ServingVariantFingerprint
→ ProviderCapabilityManifest
→ semantic/continuity health
→ quota/failure-domain snapshot
→ RouteRiskForecast
→ capability + knowledge match
→ OnlineRouteLearner posterior/policy
→ TaskAffinityLease + SwitchUtility
→ ComputationRegimeRouter
→ ProviderCongestionController admission
→ select primary + standby
→ optional AdaptiveHedgeController
→ inference under EmissionCommitBarrier
→ ResponseAdmissionGate
→ deterministic local tools/tests
→ Done Contract
→ terminal reward
→ RoutingDecisionJournal
→ online route update
→ FrontierChronicle / experience update
→ standby capsule delta refresh
```

---

# Part XXXV — Non-negotiable invariants

## 181. The Self-Optimizing Frontier Hunter must never

- hard-code one permanent “best model”;
- confuse a model name with a route cell;
- inherit host-specific quality blindly across providers;
- treat a community directory as billing authority;
- infer zero price from names such as `free`, `flash`, `auto` or `starter` alone;
- consume a paid model because free credits expired;
- consume purchased credits automatically;
- enable PayGo, auto-reload or a paid plan;
- use extra accounts/keys/IPs to bypass quotas;
- consider multiple keys in one shared quota domain independent capacity;
- benchmark away the protected recovery reserve;
- allow background discovery to starve active work;
- promote a route solely from a leaderboard;
- promote a router solely from shadow/counterfactual estimates;
- learn from model self-confidence as if it were terminal truth;
- reward premature completion or skipped verification;
- treat HTTP 200 as sufficient health;
- execute partial streamed tool calls;
- silently concatenate outputs from different models after an emitted stream failure;
- hedge mutating/non-idempotent operations;
- hedge when either route lacks zero-cost proof;
- transfer hidden chain-of-thought as canonical continuity state;
- send sensitive context to a provider whose policy does not permit it;
- make Supabase/cloud persistence required for local operation;
- let online learning bypass deterministic policy, verification or Git gates.

## 182. Product-level behavior

The user's visible experience should remain:

```text
Open AlinaCoder.exe
→ talk normally
→ AlinaCoder understands the task
→ it continuously knows what zero-cost intelligence is really reachable now
→ it measures the exact served route, not marketing model names
→ it keeps the best route while continuity is valuable
→ it learns from actual finished coding outcomes
→ it detects silent quality/latency/quota degradation
→ it prepares independent standbys before failure
→ it switches/fails over without forgetting verified intent/state
→ it never silently spends money
→ it verifies work locally
→ it commits to main only when the Done Contract is satisfied
```

The desired end-state is not “a router that usually finds a free model”.

It is:

> **A continuously self-correcting intelligence control plane that autonomously hunts the strongest legitimate zero-cost route available at that moment, learns which exact route works best for each stage of real coding work, survives provider/model churn without losing the thread, and remains governed by evidence rather than model confidence or provider marketing.**
