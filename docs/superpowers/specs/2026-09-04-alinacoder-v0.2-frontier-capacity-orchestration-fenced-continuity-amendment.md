# AlinaCoder v0.2 — Frontier Capacity, Orchestration & Fenced Continuity Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose

This amendment extends the Autonomous Frontier Marketplace with a stronger objective:

> **AlinaCoder must autonomously maximize effective intelligence, not merely select the largest advertised model. It must discover the strongest legitimate zero-autonomous-spend capacity, understand where that capacity really comes from, reserve scarce free intelligence for the work where it has the highest marginal value, choose the best reasoning/orchestration regime, and transfer authority between models without losing state or allowing stale workers to commit.**

This amendment is additive and normative together with the existing v0.2 baseline and approved amendments, especially:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-oracle-ood-certified-continuity-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-marketplace-resilience-amendment.md`

This amendment has precedence for:

- entitlement/funding-source proof;
- free-credit bucket isolation;
- recurring allowance classification;
- provider dependency and shared-failure-domain modeling;
- source reliability and stale-claim handling;
- logical-model versus concrete-endpoint routing;
- task requirement vectors and model capability vectors;
- cognitive-regime selection;
- orchestration-topology selection;
- shared free-capacity optimization;
- quota reservations and stage admission;
- routing credit assignment;
- transient-error recovery versus switching;
- adaptive cross-model handoff encoding;
- pairwise handoff compatibility;
- continuity certification metrics;
- fenced route ownership and stale-response rejection;
- semantic dependency validation at commit time;
- current provider corrections/additions including Vercel AI Gateway, LLM7, Pollinations, Cohere, Cerebras, Ollama Cloud and NVIDIA NIM;
- optional Supabase queue topology for provider discovery and evidence refresh.

All previous IntentContract, local-first, zero-paid-spend, privacy, OOD, verification, rollback, resource, provider lifecycle, semantic health, continuity and Git `main`-only invariants remain binding.

The monetary policy remains absolute:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
ALLOW_PAID_FALLBACK = false
ALLOW_AUTO_RELOAD = false
ALLOW_PURCHASED_CREDIT_CONSUMPTION = false
ALLOW_AUTOMATIC_PAYMENT_METHOD_LINKING = false
ALLOW_AUTOMATIC_POSTPAY_ENABLE = false
```

---

# Part I — Entitlement is more precise than “free”

## 2. Free is not one state

A provider may expose zero-cost access through very different mechanisms:

```text
ZERO_PRICE_RECURRING
RECURRING_INCLUDED_CREDIT
RECURRING_RATE_QUOTA
ONE_TIME_TRIAL_CREDIT
PAYMENT_METHOD_GATED_TRIAL
EVALUATION_ONLY
PROTOTYPING_ONLY
USER_FUNDED_WALLET
PROMOTIONAL_ZERO_PRICE
LOCAL_COMPUTE
PAID_WITH_FREE_ALLOWANCE
UNKNOWN
```

These classes are not interchangeable.

## 3. EntitlementClass

Introduce:

```text
EntitlementClass
```

Fields:

```text
entitlement_class
provider
account/workspace
model_scope
feature_scope
starts_at
resets_at
expires_at
renewal_rule
requires_payment_method
requires_subscription
can_overflow_to_paid
can_consume_purchased_balance
hard_stop_behavior
use_scope
source
verified_at
```

## 4. Strongest structurally safe classes

Highest-confidence autonomous zero-spend classes include:

```text
LOCAL_COMPUTE
ZERO_PRICE_RECURRING
RECURRING_RATE_QUOTA with no paid overflow
RECURRING_INCLUDED_CREDIT with hard bucket stop
PROMOTIONAL_ZERO_PRICE with exact live price lease
```

## 5. Weak classes

Classes such as:

```text
PAYMENT_METHOD_GATED_TRIAL
PAID_WITH_FREE_ALLOWANCE
USER_FUNDED_WALLET
UNKNOWN
```

are blocked by default unless an independent hard zero-spend mechanism proves the exact request cannot touch paid funds.

---

# Part II — FundingSourceProof

## 6. Billing mode is not enough

Knowing that an account is “Free” does not prove which balance the next request will consume.

Introduce:

```text
FundingSourceProof
CreditBucketSourceAttestation
```

## 7. Funding source fields

```text
provider
account_id_hash
route_cell_id
included_free_bucket_remaining
recurring_free_bucket_remaining
trial_bucket_remaining
promotional_bucket_remaining
purchased_bucket_remaining
subscription_bucket_remaining
external_user_wallet_remaining
bucket_priority_order
request_can_cross_bucket_boundary
hard_free_bucket_only_mode
paid_bucket_reachable
proof_source
verified_at
expires_at
```

## 8. Paid balance contamination rule

If a Free account can silently consume purchased credits after the included allowance is exhausted:

```text
paid_bucket_reachable == true
&& hard_free_bucket_only_mode != true
→ BLOCK_REMOTE_ROUTE
```

## 9. Existing money is still money

The fact that credits were purchased previously does not make their consumption free.

```text
ALLOW_PURCHASED_CREDIT_CONSUMPTION = false
```

remains absolute.

## 10. User-funded wallets

A gateway where another user wallet pays is not “zero spend” in the semantic sense unless the user explicitly authorizes that funding model.

For AlinaCoder's default autonomous mode:

```text
USER_FUNDED_WALLET
→ not eligible as free autonomous capacity
```

unless an exact zero-priced route exists independently of the wallet.

---

# Part III — FreeCapacityLedger

## 11. Free capacity is a resource inventory

Introduce:

```text
FreeCapacityLedger
```

Each capacity bucket is tracked independently.

## 12. Capacity bucket

```text
bucket_id
provider/account
entitlement_class
unit_type
remaining
reset_at
expires_at
hard_stop
route_cells_supported
shared_scope
confidence
last_refresh
```

Possible `unit_type` values:

```text
TOKENS
REQUESTS
NEURONS
CREDITS
GPU_TIME
CONCURRENCY_SLOTS
WALLET_UNITS
UNKNOWN_PROVIDER_UNIT
```

## 13. Shared buckets

A quota shared across models or keys must appear once in the ledger, not once per route.

## 14. Organization-scoped buckets

Provider limits shared across an organization are modeled as one shared resource.

Creating additional API keys must never be treated as creating extra capacity.

---

# Part IV — SharedQuotaKnapsackController

## 15. Independent greedy routing wastes premium free capacity

A powerful model with scarce free quota should not answer trivial tasks if a cheaper abundant route can achieve the same verified result.

Introduce:

```text
SharedQuotaKnapsackController
```

## 16. Objective

Within the hard €0 policy, maximize expected terminal task value over the whole workload rather than one request at a time.

## 17. Resource vector

For each candidate action estimate consumption of:

```text
free requests
free tokens
provider-specific capacity units
latency budget
local CPU
local GPU/VRAM
RAM
context-transmission tokens
verification reserve
recovery reserve
```

## 18. MarginalIntelligenceGainPerScarceUnit

Introduce:

```text
MarginalIntelligenceGainPerScarceUnit
```

Conceptually:

```text
expected terminal success uplift over next-best eligible route
-------------------------------------------------------------
scarce free capacity consumed
```

This is not a literal universal scalar; it is a routing signal bounded by quality/safety gates.

## 19. Preserve premium quota

If two routes both exceed the quality floor and the stronger route offers negligible expected uplift:

```text
prefer abundant route
reserve frontier route
```

## 20. Spend frontier intelligence where it changes outcomes

High-value uses include:

```text
architecture ambiguity
hard debugging
security-sensitive reasoning
complex repo-wide refactor
failed local attempts
OOD task
verifier disagreement
critical recovery
```

---

# Part V — QuotaReservationLedger

## 21. Long tasks need reservations

Introduce:

```text
QuotaReservationLedger
```

## 22. Reservation

```text
reservation_id
task_id
stage_id
bucket_id
reserved_minimum
reserved_recovery
expected_consumption
expires_at
release_condition
```

## 23. Stage admission rule

A long stage may start only if one of these is true:

```text
primary has sufficient reserved capacity
or
primary + certified standby reservations cover completion/recovery
or
stage is safely checkpointable before predicted exhaustion
```

## 24. StageAdmissionController

Introduce:

```text
StageAdmissionController
```

It prevents starting an architecture/refactor/test loop on a premium provider that is forecast to disappear halfway through without a viable continuation route.

## 25. Release unused reservation

Unused capacity returns immediately to the global ledger after the stage terminates or changes shape.

---

# Part VI — ProviderDependencyGraph

## 26. Provider names do not imply independent capacity

Two gateways can depend on the same upstream provider, same model host, or even the same infrastructure.

Introduce:

```text
ProviderDependencyGraph
```

## 27. Graph node classes

```text
AGGREGATOR
DIRECT_PROVIDER
MODEL_HOST
MODEL_FAMILY
REGION
AUTH_SYSTEM
BILLING_SYSTEM
UPSTREAM_API
NETWORK_DOMAIN
```

## 28. Edge classes

```text
ROUTES_TO
HOSTS
MIRRORS
RESELLS
SHARES_QUOTA_WITH
SHARES_AUTH_WITH
SHARES_BILLING_WITH
FALLS_BACK_TO
LIKELY_DEPENDS_ON
UNKNOWN_DEPENDENCY
```

## 29. FailureDomainDiversityScore

Introduce:

```text
FailureDomainDiversityScore
```

A standby is valuable only if it is sufficiently independent from the primary.

## 30. Fake diversity is rejected

Examples:

```text
Gateway A → upstream X/model M
Gateway B → upstream X/model M
```

must not count as two independent frontier brains for availability purposes.

## 31. Cognitive diversity also needs backend diversity

Two endpoints serving the same exact model revision may provide availability diversity but little reasoning diversity.

The system records both:

```text
infrastructure_diversity
cognitive_model_diversity
```

separately.

---

# Part VII — SourceReliabilityLedger

## 32. Discovery sources can go stale

Current ecosystem directories may continue advertising services that official providers have retired or reclassified.

Introduce:

```text
SourceReliabilityLedger
ExternalClaimContradictionScanner
```

## 33. Source record

```text
source_id
authority_level
claims_checked
claims_confirmed
claims_stale
claims_contradicted
last_checked
reliability_score
scope
```

## 34. Repeated stale claims reduce discovery weight

A community source that repeatedly lists retired/free-no-longer-free providers gets lower future priority.

## 35. Official tombstone always wins

No low-authority source can resurrect an officially retired provider.

## 36. ClaimFreshnessDebt

Introduce:

```text
ClaimFreshnessDebt
```

A claim whose verification age exceeds the volatility of its provider/catalog becomes progressively less actionable.

---

# Part VIII — TwoLevelIntelligenceRouting

## 37. Separate intelligence choice from endpoint choice

Introduce:

```text
TwoLevelIntelligenceRouting
```

Two questions are solved independently:

```text
Level A: what logical intelligence/capability is best for this task stage?
Level B: what exact zero-cost healthy RouteCell should realize it right now?
```

## 38. LogicalModelCandidate

A logical candidate abstracts capability from hosting.

```text
logical_model_family
model_revision
capability_profile
behavior_profile
context capability
tool capability
modality
verified task performance
```

## 39. EndpointRealizationCandidate

Concrete execution adds:

```text
provider
region
account
quota bucket
protocol
latency
health
funding proof
privacy/use scope
backend identity confidence
```

## 40. Benefit

Provider outages/pricing changes can move execution between equivalent realizations without forcing the intelligence router to relearn which model capability was preferred.

## 41. Capability substitution

If no endpoint for the desired logical model remains eligible, the logical router may choose the nearest capability-equivalent model, then continuity must be re-certified.

---

# Part IX — RequirementVector × CapabilityVector

## 42. Never learn direct query → fixed model ID as the primary architecture

Model catalogs change too fast.

Introduce:

```text
TaskRequirementVector
RouteCapabilityVector
```

## 43. Requirement dimensions

At minimum:

```text
reasoning_depth
code_generation
code_localization
debugging
tool_use
repository_navigation
architecture
security_reasoning
test_generation
long_context
vision
French_understanding
noisy_French_understanding
structured_output
abstention
continuity
speed_sensitivity
```

## 44. Capability dimensions

Measured using exact RouteCell evidence where possible.

## 45. CapabilityShortfall

For each dimension:

```text
shortfall = required - lower_confidence_capability
```

## 46. Admission

A route with material positive shortfall on a mandatory dimension is excluded even if its global benchmark score is high.

## 47. Language invariance

Equivalent tasks expressed in clean French, noisy French, English, typos or ASR-like speech should produce materially equivalent requirement vectors.

---

# Part X — SkillBundleRouter

## 48. Task labels are too coarse

Introduce:

```text
SkillBundle
SkillBundleRouter
```

## 49. Skill examples

```text
find relevant symbols
understand failing test
infer contract
plan migration
produce minimal patch
write discriminating test
reason about concurrency
review security boundary
interpret build logs
verify package compatibility
```

## 50. Skill-conditioned evidence

A model can be excellent at localization but mediocre at architecture.

Store performance by skill bundle, not only task family.

## 51. Skill handbook

Execution-verified experience can update a reusable local skill handbook independent of the current routing model.

---

# Part XI — CognitiveRegimeRouter

## 52. The strongest system is not always one strongest model

Introduce:

```text
CognitiveRegimeRouter
```

## 53. Regimes

```text
SINGLE_STRONG
SINGLE_STABLE_WITH_VERIFIER
LOCAL_DECOMPOSE_THEN_STRONG
PARALLEL_DIVERSE_ROLLOUTS
SPECIALIST_PIPELINE
ADVERSARIAL_REVIEW
TOURNAMENT_REFINE
CONSENSUS_WITH_EVIDENCE
RECOVERY_PAIR
```

## 54. Regime inputs

```text
task coupling
uncertainty
OOD state
side-effect risk
quota abundance
independent-route availability
expected verifier value
parallelism opportunity
latency tolerance
```

## 55. Regime before model multiplication

Do not invoke multiple models just because multiple models are available.

Multi-model collaboration must have positive expected value after quota, latency, handoff and coordination cost.

## 56. Diversity requirement

Parallel agents intended to provide independent reasoning should preferably use different cognitive model families and/or independent providers.

## 57. Agreement is not proof

Even multiple frontier models agreeing cannot bypass deterministic verification.

---

# Part XII — WorkGraphTopologyRouter

## 58. Orchestration topology is first-class

Introduce:

```text
WorkGraphTopologyRouter
```

## 59. Work graph features

```text
node_count
parallelism_width
critical_path_depth
coupling_density
shared_file_overlap
shared_resource_overlap
side_effect_edges
verification_dependencies
```

## 60. Topologies

```text
SEQUENTIAL
PARALLEL
HIERARCHICAL
HYBRID
```

## 61. Parallel is not automatically smarter

Highly coupled reasoning can degrade under naive parallel decomposition.

## 62. Safe parallel candidates

Examples:

```text
read-only repository localization
independent documentation research
alternative design exploration
independent test generation
adversarial review
```

## 63. Mutation conflicts

Tasks touching overlapping files/resources cannot commit concurrently without the transaction/fencing rules defined later.

## 64. Topology must be benchmarked

A topology change is a system change and requires terminal-outcome evidence, not aesthetic preference.

---

# Part XIII — RoutingCreditAssignmentScope

## 65. Learning scope must match execution scope

Introduce:

```text
RoutingCreditAssignmentScope
```

Possible scopes:

```text
TASK
STAGE
OPERATION
REQUEST
```

## 66. Task-pinned route

If one model is pinned for an entire task, terminal reward can be attributed primarily to that task-level route decision.

## 67. Multi-stage route

If architecture, implementation and verification use different models, a single terminal reward cannot be naively copied to every model.

## 68. TerminalRewardAttributionGraph

Introduce:

```text
TerminalRewardAttributionGraph
```

It links terminal success/failure to:

```text
stage outputs
causal dependencies
handoffs
verifier findings
tests
regressions
provider faults
```

## 69. CounterfactualAttributionGuard

Do not blame a downstream model for an invalid assumption inherited from upstream if the downstream stage could not reasonably detect it.

## 70. Handoff failures are separate

A model's quality posterior must not be reduced for a failure caused by corrupted/missing handoff state.

---

# Part XIV — SameRouteRecoveryProbe

## 71. One error does not prove the model is bad

Multi-turn routing research shows that aggressive switch-on-error can create unnecessary churn.

Introduce:

```text
SameRouteRecoveryProbe
SwitchBenefitThreshold
```

## 72. Safe same-route recovery

After a non-provider, non-billing, non-corruption error, first estimate whether the current model can recover using new execution evidence.

Examples:

```text
test failure reveals discriminating information
compiler error pinpoints API mismatch
command output invalidates one hypothesis
```

## 73. Immediate switch conditions remain

Do not stay on route after:

```text
billing safety loss
semantic corruption
model identity mismatch
critical protocol failure
provider circuit open
continuity contract violation
repeated same failure without information gain
```

## 74. Learned switch threshold

Switch only when expected benefit exceeds:

```text
handoff tax + context retransmission + quota cost + continuity risk
```

subject to hard safety gates.

---

# Part XV — AdaptiveHandoffEncodingRouter

## 75. Natural-language handoff is expensive and lossy

Introduce:

```text
AdaptiveHandoffEncodingRouter
```

## 76. Handoff encodings

```text
RAW_EXACT
TYPED_GRAPH
STRUCTURED_SUMMARY
NATURAL_LANGUAGE_AUGMENTED
HYBRID_EXACT_GRAPH_NL
```

## 77. MUST_EXACT data

The following cannot be paraphrased away:

```text
user constraints
forbidden actions
current HEAD/hash
file/symbol identifiers
test names/results
error signatures
external effect receipts
commit epoch
unresolved safety blockers
current transaction state
```

## 78. Typed graph content

A compact graph may encode:

```text
IntentContract
WorkGraph
files/symbols
hypotheses
observations
decisions
disproved paths
tests
provider state
quota reservations
pending effects
dependencies
```

## 79. NL is retained where semantics are hard to discretize

Ambiguous user nuance, design rationale and open-ended reasoning context may require natural-language augmentation.

## 80. Encoding choice is task-specific

Graph-only is prohibited as a universal handoff format.

## 81. Handoff interpretation guide

Every typed handoff schema includes a short deterministic interpretation contract for the destination model.

---

# Part XVI — HandoffRoundTripProbe

## 82. Compression must prove semantic retention

Introduce:

```text
HandoffRoundTripProbe
```

## 83. Probe questions

Before mutation authority transfers, verify that destination can recover at least:

```text
user goal
forbidden actions
current stage
known facts
failed hypotheses
next intended operation
critical file/symbol targets
current verification status
```

## 84. Round-trip failure

If destination reconstructs a materially different IntentContract or WorkGraph:

```text
handoff rejected
→ widen handoff encoding
→ retry boundedly
→ choose another route if needed
```

---

# Part XVII — HandoffCompatibilityMatrix

## 85. Continuity is pair-specific

Introduce:

```text
HandoffCompatibilityMatrix
```

Indexed by:

```text
(source RouteCell family, destination RouteCell family, handoff encoding, task class)
```

## 86. Pair evidence

Store:

```text
continuity success
constraint recall
state reconstruction
latency overhead
handoff token overhead
tool-state preservation
mutation safety
sample count
confidence
```

## 87. Direction matters

A → B can be reliable while B → A is weaker.

Do not assume symmetry.

## 88. Standby ranking includes handoff compatibility

A slightly weaker model with excellent destination continuity may be a better emergency standby than a stronger model with poor handoff fidelity.

---

# Part XVIII — ContinuityCertificationSuite

## 89. Formal continuity metrics

Introduce:

```text
ContinuityCertificationSuite
```

## 90. Core metrics

```text
CPR  = Continuity Preservation Rate
CLO  = Continuity Latency Overhead
CRF  = Context Reconstruction Fidelity
CRR  = Constraint Recall Rate
TSPR = Tool-State Preservation Rate
MSPR = Mutation-Safety Preservation Rate
HCO  = Handoff Context Overhead
```

## 91. Certification is per pair

A failover route receives `CERTIFIED_SEAMLESS` only for pairings with enough evidence.

## 92. Emergency unproven fallback

If all certified pairs are unavailable, an unproven fallback may perform read-only recovery/reconstruction, but cannot immediately receive high-impact mutation authority.

## 93. Continuity benchmark corpus

Use metamorphic tasks with:

```text
long conversations
corrections/negations
repo changes
mid-debug failover
mid-plan failover
quota exhaustion
provider outage
stream truncation
concurrent late responses
```

Hidden cases remain outside the public repo.

---

# Part XIX — RouteOwnershipFence

## 94. Failover creates a split-brain risk

A timed-out old provider can return after the new provider has already taken over.

Introduce:

```text
RouteOwnershipFence
CommitEpoch
```

## 95. Monotonic epoch

Every task mutation authority carries a monotonically increasing epoch.

```text
epoch 41 → primary A
timeout/failover
epoch 42 → primary B
```

## 96. Late response rejection

Any result from epoch 41 attempting to commit after epoch 42 exists is rejected regardless of apparent quality.

## 97. Provider response never writes directly

Provider/model outputs are proposals only.

They append an attempt result containing:

```text
task_id
epoch
route_cell_id
request_digest
response_digest
semantic_validation
```

Only the local commit authority can mutate canonical state.

## 98. Fencing is durable

Epoch state must live in the durable canonical store, not only process memory.

## 99. Timeout is not proof of death

Failover can promote a new route after timeout, but old route authority is revoked through fencing, not by assuming the old request disappeared.

---

# Part XX — ResourceFrontierCommitGate

## 100. Parallel workers require resource-scoped commit ordering

Introduce:

```text
ResourceFrontierCommitGate
```

## 101. Resource scopes

Examples:

```text
repo
file
symbol
package manifest
migration
external account/resource
```

## 102. Buffer local mutations

Where technically feasible, speculative file mutations stay in shadow state until verification and commit authorization.

## 103. Resource epoch

A mutation can commit only if its observed base version/hash and fencing epoch remain current.

## 104. OCC for long inference

For read-heavy planning:

```text
read base hashes
→ reason without holding global lock
→ at commit validate dependency hashes
→ rebase/replan if stale
```

## 105. Side effects

External irreversible effects must remain behind existing approval/safety gates and use idempotency/receipt tracking where available.

---

# Part XXI — PlanDependencyFence

## 106. Fresh facts can coexist with stale plans

Introduce:

```text
PlanDependencyFence
```

## 107. Plan provenance

Every executable plan records exact dependencies:

```text
IntentContract version
repo HEAD
relevant file hashes
provider-policy epoch
tool capability versions
critical retrieved facts
```

## 108. Pre-action validation

Immediately before a high-impact action, validate only dependencies capable of invalidating that action.

## 109. Replan once, then block safely

When a material dependency changed:

```text
invalidate affected plan node
→ refresh context
→ replan boundedly
→ execute only new valid plan
```

## 110. Fresh memory is not enough

Simply injecting the latest fact does not authorize execution of a plan derived from older facts.

---

# Part XXII — SemanticEnvironmentManifest

## 111. Durable workflows bind more than model state

Introduce:

```text
SemanticEnvironmentManifest
```

## 112. Manifest contents

```text
route/model fingerprint
prompt/schema version
tool contracts
retrieval/index versions
skillbook version
verifier policy
provider policy epoch
continuity schema version
```

## 113. Resume validation

A resumed task validates compatibility of changed semantic dependencies before executing the saved plan.

## 114. Allowed upgrade

A newer provider/model/tool may be adopted only if compatibility is proven or the affected plan/context is deliberately regenerated.

---

# Part XXIII — Provider corrections and additions, research snapshot 2026-09-04

## 115. Snapshot rule

Everything in this section is discovery-time evidence only.

Runtime use still requires current first-party/account-level proof.

## 116. Vercel AI Gateway — new candidate

Current Vercel documentation describes a recurring free tier for AI Gateway with a subset of free-tier models and lower rate limits.

The free tier is described as monthly included credit rather than a one-time trial.

## 117. Vercel paid transition

Current documentation states purchasing AI Gateway Credits transitions the team to the paid tier and removes the monthly free-credit behavior.

Therefore classify:

```text
Vercel free team with no purchased credits
→ RECURRING_INCLUDED_CREDIT_GATEWAY candidate

Vercel paid team / purchased AI Gateway credits
→ blocked by default for autonomous zero-spend routing
```

## 118. Vercel free catalog

Do not hardcode model names.

The discovery worker queries the current free-tier-filtered model catalog and creates RouteCells only for presently covered models.

## 119. Vercel fallback

Any gateway-managed provider fallback must pass `ZeroCostFallbackClosure` and dependency transparency.

## 120. LLM7 — new recurring daily capacity candidate

Current first-party LLM7 documentation states text-generation limits including:

```text
Anonymous: 500,000 input+output tokens per 24h
Free token: 1,000,000 input+output tokens per 24h
```

with current request-rate limits documented separately.

## 121. LLM7 live catalog

Current docs expose:

```text
GET https://api.llm7.io/v1/models
```

with live model IDs, tiers, pricing, context windows and capability flags.

## 122. LLM7 admission

Treat as:

```text
RECURRING_DAILY_FREE_CAPACITY_CANDIDATE
```

only when:

```text
exact route tier is free/anonymous
no topped-up paid balance can be consumed
current terms/use scope permit task
backend opacity is acceptable
current semantic canaries pass
```

## 123. LLM7 dependency caution

Historical ecosystem evidence indicates potential overlap with Pollinations/upstream routing.

The `ProviderDependencyGraph` must measure actual current dependency/failure-domain independence before LLM7 is counted as a distinct standby.

## 124. Pollinations — discovery-rich but funding-sensitive

Current Pollinations generation API is OpenAI-compatible, exposes a large live model catalog and public model metadata, and uses Pollen/account funding for model calls.

## 125. Pollinations exact-zero-price rule

A named frontier model in Pollinations is **not** presumed free.

Only:

```text
exact public model current price == zero
```

or another hard-zero funding proof can make the RouteCell eligible.

## 126. Pollinations wallet rule

User-wallet/BYOP behavior is not part of default zero-spend autonomy.

## 127. Pollinations value

Its broad live catalog remains highly valuable for:

```text
new-model discovery
capability metadata
future zero-price route detection
```

## 128. Cohere — evaluation capacity, not generic production free tier

Current Cohere documentation distinguishes free evaluation keys from paid production keys.

Current trial/evaluation limits include roughly:

```text
1,000 API calls/month
```

for relevant trial access.

## 129. Cohere classification

```text
EVALUATION_ONLY_FREE_KEY
```

unless exact current terms explicitly permit the intended use.

Evaluation access can benchmark candidates but must not silently become production/autonomous capacity outside permitted scope.

## 130. Cerebras correction

Current Cerebras documentation no longer supports treating its hosted API as a permanent free tier.

Current new-account flow is described as:

```text
$5 trial credits
30-day expiry
verified payment method required
```

## 131. Cerebras classification

```text
PAYMENT_METHOD_GATED_ONE_TIME_TRIAL
```

Under AlinaCoder's default policy:

```text
ALLOW_AUTOMATIC_PAYMENT_METHOD_LINKING = false
→ Cerebras hosted trial BLOCKED as autonomous free capacity
```

Public model catalog metadata can still be used for discovery.

## 132. Ollama Cloud correction/refinement

Current Ollama pricing describes Free accounts as receiving starter usage for starter models, resetting monthly, while every plan can also add extra usage credits.

## 133. Ollama Cloud bucket safety

If extra purchased credits exist and the service automatically consumes them after included Free capacity:

```text
BLOCK
```

unless `CreditBucketSourceAttestation` proves a free-bucket-only hard stop.

## 134. Ollama Cloud account probe

Community trackers may identify models observed working on Free accounts, but only current account/runtime probes can authorize execution.

## 135. NVIDIA NIM refinement

Current NVIDIA first-party material advertises free NIM API access for prototyping/development.

Classify hosted free NIM access conservatively as:

```text
PROTOTYPING_ONLY_FREE_CAPACITY
```

until exact current use-scope evidence authorizes the intended workload.

## 136. Existing provider atlas remains active

All prior valid candidates remain under live requalification, including:

```text
Kilo Gateway
Z.AI
SambaNova
Groq
Cloudflare Workers AI
OpenRouter free-only
Gemini Free Tier
Mistral Free mode
Tencent TokenHub/Hunyuan
Alibaba safe free-quota mode
SiliconFlow exact-zero routes
Scaleway where hard-zero safety is proven
Hugging Face included credits where paid overflow is impossible
OpenCode Zen where autoreload/paid path is proven safe
local Ollama
```

No item in this list is permanently eligible merely because it appears here.

---

# Part XXIV — FrontierPoolBuilder v2

## 137. Candidate collection

Build the candidate pool from:

```text
direct provider live catalogs
aggregator live catalogs
current account entitlements
local Ollama model inventory
official new-model announcements
trusted research/benchmark leads
community leads only as discovery hints
```

## 138. Normalize into three graphs

```text
CapabilityGraph
EndpointGraph
DependencyGraph
```

## 139. CapabilityGraph

Answers:

> What forms of intelligence are available?

## 140. EndpointGraph

Answers:

> Where can each capability be executed under current health/quota/billing constraints?

## 141. DependencyGraph

Answers:

> Which candidates share upstream failure domains, funding buckets or hidden backends?

## 142. Result

The router does not see a flat list of model strings.

It sees a structured, continuously changing intelligence market.

---

# Part XXV — IntelligenceLease

## 143. Route selection creates an explicit lease

Introduce:

```text
IntelligenceLease
```

## 144. Lease fields

```text
task/stage
logical intelligence candidate
primary RouteCell
standby RouteCells
CommitEpoch
quota reservations
PriceEpochLease
BillingModeProof
FundingSourceProof
semantic health epoch
handoff encoding
continuity certification
expires_at
```

## 145. Lease invalidation

Invalidate immediately on:

```text
price change
funding-source change
quota reserve breach
backend identity mismatch
semantic-health degradation
plan dependency invalidation
provider retirement
terms/use-scope change
```

## 146. Renewal at safe checkpoint

Long stages renew the lease only at safe boundaries unless a hard safety event forces immediate revocation.

---

# Part XXVI — FrontierCapacityScheduler

## 147. Scheduler role

Introduce:

```text
FrontierCapacityScheduler
```

It coordinates multiple active tasks/stages competing for scarce free frontier capacity.

## 148. Priority signals

```text
user-visible blocking
risk/criticality
expected frontier uplift
recovery urgency
quota expiry
reset proximity
availability volatility
```

## 149. No starvation

A long low-priority background calibration stream cannot consume all frontier quota while an active user task is blocked.

## 150. Expiring quota

If a free bucket will reset/expire soon and has no higher-value expected use, it may be spent on bounded calibration rather than wasted.

---

# Part XXVII — ShadowAuditAllocator v2

## 151. Shadow audits are strategic exploration

Use a small bounded quota slice to compare current champion against challengers on representative tasks.

## 152. Information gain objective

Prefer audits likely to change routing decisions:

```text
new model
suspected drift
uncertain capability boundary
high disagreement
stale champion evidence
new task family
```

## 153. Do not audit dominated regions

Repeatedly benchmarking a clearly inferior route wastes free capacity.

## 154. Pairwise continuity audit

Some audit budget measures handoff compatibility, not task-solving quality.

---

# Part XXVIII — Frontier value-of-information

## 155. Model probing has opportunity cost

Introduce:

```text
FrontierProbeVOI
```

## 156. Probe if

```text
probability probe changes future route decisions
× expected downstream value
>
quota + latency + opportunity cost
```

## 157. Probe abstention

If evidence already strongly establishes dominance and provider state is stable, skip redundant benchmark calls.

---

# Part XXIX — IndependentVerifierAllocation

## 158. Verification is another intelligence allocation problem

A strong primary may still benefit from a cheaper diverse verifier.

## 159. Verifier route requirements

Prefer:

```text
independent cognitive family
independent provider/failure domain
high skill on review/test reasoning
low enough quota cost
```

## 160. Same-model verifier discount

Self-review by the same exact model/backend receives lower independence weight.

## 161. Deterministic checks remain strongest

Compiler/tests/static analysis outrank LLM reviewer consensus.

---

# Part XXX — RecoveryPair

## 162. A standby is a pair contract

Introduce:

```text
RecoveryPair
```

between primary and standby.

## 163. RecoveryPair fields

```text
primary
standby
failure_domain_diversity
handoff_encoding
continuity_certificate
required quota reserve
capability gap
known incompatibilities
recovery latency
```

## 164. Prefer pair quality over isolated standby rank

The best standalone second model is not necessarily the best recovery destination.

---

# Part XXXI — ProgressiveTakeover

## 165. Takeover authority is staged

Introduce:

```text
ProgressiveTakeover
```

Stages:

```text
READ_ONLY_REHYDRATE
STATE_RECONSTRUCT
PROPOSE_NEXT_ACTION
VERIFY_CONTINUITY
LIMITED_MUTATION
FULL_STAGE_AUTHORITY
```

## 166. Emergency routes start conservatively

An uncertified route cannot jump directly to full mutation authority merely because the primary is unavailable.

## 167. Certified pair can accelerate

A pair with strong continuity certification may move faster through takeover stages.

---

# Part XXXII — EpistemicDelta handoff

## 168. Replicate operational meaning, not private chain-of-thought

Introduce:

```text
EpistemicDelta
```

## 169. Delta content

```text
verified facts
active constraints
decisions
causal evidence references
invalidated beliefs
unresolved hypotheses
next permitted actions
```

## 170. No hidden reasoning requirement

The system never depends on retaining or transferring private chain-of-thought.

Only user-visible/operationally necessary state is persisted.

## 171. Semantic rollback

If a premise is proven wrong, invalidate dependent derived state and regenerate only affected planning/context rather than wiping unrelated valid knowledge.

---

# Part XXXIII — ExecutionEvidenceGraph

## 172. Canonical evidence is graph-structured

Introduce:

```text
ExecutionEvidenceGraph
```

Nodes:

```text
user requirement
repo fact
external source fact
test result
command result
model proposal
plan node
mutation
verification
commit
```

Edges:

```text
DERIVED_FROM
DEPENDS_ON
VALIDATES
INVALIDATES
SUPERSEDES
AUTHORIZED_BY
MUTATES
OBSERVES
```

## 173. Failover uses evidence graph

The destination gets relevant evidence and dependency structure instead of an undifferentiated transcript dump.

## 174. Stale-plan detection uses graph

If a source node changes, affected downstream plan nodes become stale.

---

# Part XXXIV — Provider feature-cost isolation

## 175. A free model call can contain paid subfeatures

Existing `FeatureBillingVector` is extended into:

```text
FeatureFundingIsolation
```

## 176. Features checked independently

```text
web search
file storage
vision
reasoning tier
tool execution
embedding
reranking
cache storage
agent hosting
```

## 177. Mixed request blocked

A request is zero-cost only if **every activated metered feature** is zero-cost or hard-stopped under the funding proof.

---

# Part XXXV — Authentication capability without credential proliferation

## 178. One provider, many routes, one secret handle

Credentials are referenced by `CredentialHandle`; child RouteCells inherit authorization without copying secret material.

## 179. Scope minimization

Prefer provider credentials restricted to:

```text
inference only
specific project/account
no billing/admin permissions
```

where provider supports it.

## 180. Read-only discovery without credential

Use unauthenticated model/catalog endpoints whenever available before touching credentials.

---

# Part XXXVI — Free-tier reset optimization

## 181. Reset clocks matter

Track:

```text
minute
hour
day
month
signup-anniversary
campaign expiry
```

## 182. Reset-aware allocation

A scarce daily quota close to reset can be used more aggressively if enough recovery reserve remains and no higher-value task is queued.

## 183. Never create artificial accounts

Quota optimization must never include account farming, multiple identities, ToS bypass or geographic evasion.

---

# Part XXXVII — Local frontier coexistence

## 184. Local models remain part of the same capability market

Ollama local routes have:

```text
remote monetary cost = 0
network dependency = none
privacy advantage = high
capacity constrained by local hardware
```

## 185. Local-first does not mean local-always

When a remote zero-cost frontier route is safely available and materially improves expected task success, it may be selected.

## 186. Local roles

Even when remote model is primary, local models can perform:

```text
routing classification
context compression
repo indexing
simple extraction
syntax checking assistance
cheap challenger screening
```

without consuming remote quota.

---

# Part XXXVIII — Router collapse protection

## 187. Strongest-model collapse can be irrational

If the router sends everything to one frontier model, it may waste scarce capacity and lose specialization benefits.

Introduce:

```text
RouteCollapseDetector
```

## 188. Collapse metrics

```text
route concentration
skill-conditioned regret
quota concentration
missed specialist uplift
standby diversity erosion
```

## 189. No forced diversity

Diversity itself is not a goal.

If one route objectively dominates for a workload and capacity is abundant, concentration is acceptable.

---

# Part XXXIX — Routing regret decomposition

## 190. Regret has causes

Introduce:

```text
RoutingRegretDecomposition
```

Categories:

```text
CAPABILITY_MISROUTE
ENDPOINT_MISROUTE
QUOTA_MISALLOCATION
HANDOFF_FAILURE
PROVIDER_DRIFT
STALE_EVIDENCE
TOPOLOGY_MISMATCH
VERIFIER_MISALLOCATION
FUNDING_BLOCK_FALSE_POSITIVE
```

## 191. Improve the right subsystem

A task failure caused by endpoint outage should not trigger retraining of the capability predictor.

---

# Part XL — Autonomous provider onboarding v3

## 192. New provider pipeline

```text
DISCOVER
→ SOURCE_AUTHORITY_CHECK
→ DEPENDENCY_GRAPH_PROBE
→ AUTH_BOUNDARY_CHECK
→ ENTITLEMENT_CLASSIFY
→ FUNDING_SOURCE_PROVE
→ LIVE_CATALOG_PARSE
→ PROTOCOL_CANARY
→ SEMANTIC_CANARY
→ MODEL_IDENTITY_ATTEST
→ CAPABILITY_PROFILE
→ HANDOFF_COMPATIBILITY_PROBE
→ SAFE_EXPLORATION
→ ELIGIBLE
```

## 193. New model within known provider

Faster path:

```text
catalog diff
→ exact price/funding proof
→ model identity
→ capability profile
→ bounded exploration
```

## 194. New endpoint mirror

Require dependency graph + identity proof before treating it as new independent capacity.

---

# Part XLI — Provider de-onboarding v3

## 195. Removal triggers

```text
retirement
price > 0
free bucket contamination
payment requirement
terms incompatibility
semantic degradation
model mismatch
persistent protocol corruption
unacceptable opacity
```

## 196. Drain before remove

If route is still serving a task and removal is non-emergency:

```text
stop new admissions
prepare standby
checkpoint
handoff
revoke lease
remove route
```

## 197. Emergency removal

Billing/privacy/corruption hazards revoke authority immediately and fence late output.

---

# Part XLII — Optional Supabase evidence plane v2

## 198. Supabase remains optional

Local SQLite/event logs remain canonical for single-machine operation.

## 199. PGMQ is FIFO, not priority-native

Do not model one queue as if it supports native priority scheduling.

If optional Supabase orchestration is enabled, use separate durable queues such as:

```text
provider_safety_recheck
provider_policy_diff
quota_refresh
frontier_discovery
semantic_canary
shadow_benchmark
handoff_benchmark
```

and let AlinaCoder's scheduler choose which queue to drain.

## 200. Visibility timeout

Workers use PGMQ visibility timeout so crashed discovery/benchmark jobs become available for retry.

## 201. Idempotency

Each queued job carries:

```text
job_id
provider/route
source_hash
policy_epoch
expected_commit_epoch
```

## 202. Archive evidence

Archive completed probe records for audit/replay rather than deleting all history.

## 203. Stale embedding rule

When a model/provider profile changes materially:

```text
invalidate/clear old derived embedding
→ regenerate asynchronously
```

A stale route embedding cannot remain queryable as current truth.

## 204. Supabase Vault

If cloud workers are explicitly enabled, secret material may use Supabase Vault according to existing security rules.

## 205. Realtime

Realtime may notify UI/other clients about provider state changes but does not become the authoritative ledger.

---

# Part XLIII — Acceptance scenarios: funding and quotas

## 206. Ollama Free with purchased extra credits

1. Account is Free.
2. Included starter usage remains.
3. Purchased extra credits also exist.
4. Provider would consume extra credits after included bucket.
5. No free-bucket-only mode exists.
6. Route is blocked for autonomous use.

## 207. Vercel recurring free tier

1. Team has never purchased AI Gateway credits.
2. Current free-tier model catalog includes candidate.
3. Free allowance remains.
4. Exact fallback closure is zero-cost.
5. Route may be eligible.

## 208. Vercel paid transition

1. User later purchases gateway credits.
2. Entitlement class changes.
3. Funding proof invalidates.
4. Autonomous zero-spend use stops before next request.

## 209. LLM7 daily reset

1. Free token route has daily capacity remaining.
2. Exact live model tier is Free.
3. No paid bucket is reachable.
4. Route can be scheduled.
5. Reset time is tracked.

## 210. Cerebras stale community claim

1. Community directory says Cerebras is permanently free.
2. Current first-party docs say payment-method-gated trial.
3. Official source wins.
4. SourceReliabilityLedger records contradiction.
5. Cerebras is blocked as standing autonomous free capacity.

---

# Part XLIV — Acceptance scenarios: dependency diversity

## 211. Two gateways, same upstream

1. A and B advertise different domains.
2. Dependency probes show both resolve to same upstream model/provider.
3. Infrastructure diversity score falls.
4. They are not paired as sole primary+standby for critical availability.

## 212. Same model, different independent hosts

1. Model revision identical.
2. Providers are independent.
3. Availability diversity is high.
4. Cognitive diversity remains low.
5. System may use them for failover but not treat agreement as independent reasoning consensus.

---

# Part XLV — Acceptance scenarios: routing scope

## 213. Easy task with scarce frontier quota

1. Small free model exceeds quality floor.
2. Frontier model offers tiny predicted uplift.
3. Frontier bucket is scarce.
4. SharedQuotaKnapsackController selects smaller route.
5. Frontier quota is preserved.

## 214. Architecture-critical task

1. Local/small models fail requirement-vector shortfall.
2. Frontier route materially improves expected success.
3. Premium free quota remains.
4. Frontier route selected.

## 215. Specialist topology

1. Repo-wide bug has independent localization, test-design and security-review subproblems.
2. WorkGraph shows high parallelism and low mutation overlap.
3. TopologyRouter chooses parallel read-only specialists.
4. Synthesis/implementation remains fenced and serialized.

---

# Part XLVI — Acceptance scenarios: switching

## 216. Transient test failure

1. Current model proposes patch.
2. Test fails with new discriminating evidence.
3. Provider remains healthy and billing-safe.
4. SameRouteRecoveryProbe estimates high recovery value.
5. Current model gets bounded repair attempt instead of immediate churn.

## 217. Repeated non-informative failure

1. Same signature repeats.
2. No new evidence appears.
3. SwitchBenefitThreshold is exceeded.
4. Handoff begins at safe checkpoint.

## 218. Billing hazard

1. Current route loses funding proof.
2. No same-route retry allowed.
3. Lease revoked immediately.
4. Commit epoch advances.
5. Standby takeover begins.

---

# Part XLVII — Acceptance scenarios: handoff

## 219. Graph-friendly handoff

1. Task state is strongly structured.
2. Typed graph contains all MUST_EXACT fields.
3. Round-trip probe succeeds.
4. Handoff proceeds with lower context overhead.

## 220. Ambiguous design handoff

1. User nuance is hard to encode structurally.
2. Graph-only handoff loses intent detail.
3. Router selects HYBRID_EXACT_GRAPH_NL.
4. Destination recovers IntentContract correctly.

## 221. Pair incompatibility

1. Route A→B has poor constraint recall in prior probes.
2. A→C has strong continuity certification.
3. C is slightly weaker standalone than B.
4. C becomes preferred emergency standby.

---

# Part XLVIII — Acceptance scenarios: fencing

## 222. Late primary response

1. Primary A runs at epoch 17.
2. A times out.
3. Controller advances to epoch 18 and assigns B.
4. B returns, passes verification and commits.
5. A later returns a plausible answer.
6. A's epoch 17 commit is rejected deterministically.

## 223. Two parallel writers

1. Agents read same file hash H0.
2. Agent 1 commits H1.
3. Agent 2 proposes patch based on H0.
4. OCC validation fails.
5. Agent 2 rebases/replans on H1.
6. No last-writer-wins corruption occurs.

## 224. Stale plan after user correction

1. Plan depends on IntentContract v12.
2. User corrects requirement → v13.
3. Model receives v13 facts but old plan node still references v12.
4. PlanDependencyFence blocks action.
5. Affected node replans.

---

# Part XLIX — New metrics

## 225. Funding safety metrics

```text
funding_source_proof_coverage
credit_bucket_boundary_cross_attempts
purchased_credit_consumption
free_bucket_false_positive_rate
```

Hard targets:

```text
purchased_credit_consumption = 0
free_bucket_false_positive_rate = 0
```

## 226. Global quota metrics

```text
frontier_quota_utilization
premium_quota_wasted_on_low_uplift
reservation_accuracy
stage_midstream_exhaustion_rate
marginal_gain_per_scarce_unit
```

Hard target:

```text
stage_midstream_exhaustion_without_certified_standby = 0
```

## 227. Dependency metrics

```text
unknown_upstream_fraction
false_independence_rate
standby_failure_domain_diversity
cognitive_diversity_score
```

## 228. Routing intelligence metrics

```text
requirement_shortfall_violation
skill_conditioned_regret
route_collapse_rate
routing_regret_by_cause
terminal_success_uplift_vs_static_champion
```

## 229. Handoff metrics

```text
CPR
CLO
CRF
CRR
TSPR
MSPR
HCO
handoff_round_trip_failure_rate
pairwise_continuity_confidence
```

## 230. Fencing metrics

```text
stale_epoch_commit_attempts
stale_epoch_commits_accepted
split_brain_prevented
OCC_rebases
plan_dependency_invalidations
```

Hard targets:

```text
stale_epoch_commits_accepted = 0
```

---

# Part L — Suggested conceptual modules

## 231. New modules

```text
src/alinacoder/intelligence_mesh/
  entitlement.py
  funding_source.py
  free_capacity_ledger.py
  shared_quota_knapsack.py
  quota_reservations.py
  provider_dependency_graph.py
  source_reliability.py
  logical_model_router.py
  endpoint_realization_router.py
  requirement_vector.py
  capability_vector.py
  skill_bundle_router.py
  cognitive_regime_router.py
  topology_router.py
  credit_assignment.py
  same_route_recovery.py
  adaptive_handoff_encoding.py
  handoff_compatibility.py
  continuity_certification.py
  recovery_pair.py
  progressive_takeover.py
  epistemic_delta.py
  intelligence_lease.py
  frontier_capacity_scheduler.py
  shadow_audit_allocator.py
  frontier_probe_voi.py

src/alinacoder/state/
  route_ownership_fence.py
  resource_frontier.py
  plan_dependency_fence.py
  semantic_environment_manifest.py
  execution_evidence_graph.py

src/alinacoder/providers/
  vercel_ai_gateway.py
  llm7.py
  pollinations.py
  cohere_eval.py
  cerebras_trial_guard.py

src/alinacoder/evaluation/
  continuity_pair_bench.py
  funding_bucket_bench.py
  shared_quota_bench.py
  topology_bench.py
  handoff_encoding_bench.py
  fencing_bench.py
  stale_plan_bench.py
  dependency_diversity_bench.py
```

Names are conceptual and may be reorganized during implementation without weakening contracts.

---

# Part LI — Recommended implementation order

## 232. Phase F1 — funding-source correctness

Implement before adding more provider volume:

```text
EntitlementClass
FundingSourceProof
CreditBucketSourceAttestation
FreeCapacityLedger
```

## 233. Phase F2 — dependency truth

Implement:

```text
ProviderDependencyGraph
FailureDomainDiversityScore
SourceReliabilityLedger
```

## 234. Phase F3 — two-level routing

Implement:

```text
TaskRequirementVector
RouteCapabilityVector
LogicalModelRouter
EndpointRealizationRouter
```

## 235. Phase F4 — free-capacity scheduler

Implement:

```text
SharedQuotaKnapsackController
QuotaReservationLedger
StageAdmissionController
FrontierCapacityScheduler
```

## 236. Phase F5 — fenced continuity

Implement:

```text
RouteOwnershipFence
CommitEpoch
ResourceFrontierCommitGate
PlanDependencyFence
```

before allowing aggressive autonomous failover or parallel mutation.

## 237. Phase F6 — handoff intelligence

Implement:

```text
AdaptiveHandoffEncodingRouter
HandoffRoundTripProbe
HandoffCompatibilityMatrix
ContinuityCertificationSuite
RecoveryPair
ProgressiveTakeover
```

## 238. Phase F7 — orchestration intelligence

Implement:

```text
SkillBundleRouter
CognitiveRegimeRouter
WorkGraphTopologyRouter
SameRouteRecoveryProbe
```

## 239. Phase F8 — provider additions/corrections

Add adapters in evidence-driven order:

```text
Vercel AI Gateway
LLM7
Pollinations exact-zero discovery/execution
Cohere evaluation-only adapter
Cerebras trial guard/tombstone-class correction
Ollama Cloud funding-bucket attestation
NVIDIA NIM use-scope refinement
```

## 240. Phase F9 — optional Supabase evidence plane

Only after local primitives are complete, optionally add separated durable PGMQ queues, cron jobs and cloud evidence sync.

---

# Part LII — Research basis added by this pass

## 241. Research date

Research performed 2026-09-04 using current first-party provider documentation plus 2026 routing/failover literature.

## 242. TRACE-Router

Source:

```text
https://arxiv.org/html/2607.22465
```

Applied lesson:

```text
routing/learning scope should align with long-horizon task outcome
```

leading to `RoutingCreditAssignmentScope` and terminal attribution.

## 243. Agent-as-a-Router / ACRouter

Source:

```text
https://arxiv.org/html/2606.22902v2
```

Applied lesson:

```text
execution-grounded verifier feedback + memory closes routing information deficit
```

and reinforces nearest verified analog evidence.

## 244. vLLM Semantic Router

Source:

```text
https://arxiv.org/html/2603.04444
```

Applied lessons:

```text
composable routing signals
stateful multi-turn routing
provider abstraction
separation of semantic model choice from endpoint realization
```

## 245. MTRouter

Source:

```text
https://aclanthology.org/2026.acl-long.2045.pdf
```

Applied lesson:

```text
successful multi-turn routing is selective switching, not maximum switching
```

leading to `SameRouteRecoveryProbe` and `SwitchBenefitThreshold`.

## 246. Drift-Aware Sparse Routing

Source:

```text
https://arxiv.org/abs/2609.00662
```

Applied lessons:

```text
rolling audit windows
shared multi-resource budgets
pessimistic reward / resource uncertainty
hard meters before commitment
```

adapted here to free-capacity resource allocation rather than paid spend.

## 247. Routed Graph Handoff

Source:

```text
https://arxiv.org/abs/2608.25277
```

Applied lesson:

```text
handoff encoding should itself be routed between structured graph and natural language
```

rather than hardcoding one format.

## 248. HyDRA

Source:

```text
https://arxiv.org/html/2605.17106
```

Applied lessons:

```text
multi-dimensional capability requirements
catalog-decoupled routing
language-invariant routing
```

leading to `TaskRequirementVector × RouteCapabilityVector`.

## 249. SkillOrchestra

Source:

```text
https://arxiv.org/pdf/2602.19672
```

Applied lesson:

```text
explicit skills provide transferable orchestration knowledge and reduce routing collapse
```

## 250. BiCSRouter

Source:

```text
https://aclanthology.org/2026.findings-acl.947.pdf
```

Applied lesson:

```text
route between computational regimes, not only model IDs
```

## 251. Adaptive orchestration topology research

Source reviewed:

```text
https://arxiv.org/pdf/2602.16873
```

Applied lesson:

```text
task dependency structure can determine whether sequential, parallel, hierarchical or hybrid orchestration is preferable
```

without accepting benchmark claims as universal truth.

## 252. ContinuityBench

Source:

```text
https://arxiv.org/abs/2607.15899
```

Applied lessons:

```text
availability != conversational continuity
Continuity Preservation Rate
Continuity Latency Overhead
history-forwarding/state reconstruction
jittered retry under failover
```

leading to pairwise continuity certification.

## 253. Atomix

Source:

```text
https://arxiv.org/pdf/2602.14849
```

Applied lessons:

```text
epoch-tagged agent effects
progress-aware commit
resource frontiers
buffered reversible effects
```

leading to fenced commit/resource frontier concepts.

## 254. PlanFence / stale-plan research

Source:

```text
https://arxiv.org/abs/2609.03340
```

Applied lesson:

```text
fresh memory does not prove an old plan remains valid
```

leading to `PlanDependencyFence`.

## 255. Semantic-isolation research

Source reviewed:

```text
https://arxiv.org/html/2608.05412v1
```

Applied lesson:

```text
checkpointed workflows should bind semantic resource versions and validate compatibility across resume/fork/late discovery
```

leading to `SemanticEnvironmentManifest`.

## 256. Provider documentation — Vercel

Reviewed:

```text
https://vercel.com/docs/ai-gateway/pricing
https://vercel.com/docs/ai-gateway/faq
https://vercel.com/ai-gateway/models
```

## 257. Provider documentation — LLM7

Reviewed:

```text
https://docs.llm7.io/limits
https://docs.llm7.io/guides/models-api
```

## 258. Provider documentation — NVIDIA NIM

Reviewed:

```text
https://developer.nvidia.com/nim
```

## 259. Provider documentation — Cohere

Reviewed:

```text
https://docs.cohere.com/docs/rate-limits
```

## 260. Provider documentation — Ollama

Reviewed:

```text
https://ollama.com/pricing
```

## 261. Provider documentation — Pollinations

Reviewed:

```text
https://gen.pollinations.ai/docs
https://github.com/pollinations/pollinations/blob/HEAD/APIDOCS.md
```

## 262. Cerebras correction

Current first-party inference documentation was reviewed for current trial/payment requirements and replaces stale community assumptions of a permanent free tier.

## 263. Supabase

Current Supabase documentation reviewed for:

```text
PGMQ durable queues
visibility timeouts
archival
pg_cron
pg_net
Vault
Realtime observability
```

Important correction:

```text
PGMQ basic queue behavior is FIFO and not native-priority scheduling
```

so optional provider work uses separate queues plus an AlinaCoder scheduler.

---

# Part LIII — Canonical Frontier Intelligence loop v5

## 264. Loop

```text
Receive user task
→ repair-aware IntentContract
→ build/refresh ExecutionEvidenceGraph
→ infer TaskRequirementVector + SkillBundle
→ classify OOD/support
→ derive WorkGraph
→ CognitiveRegimeRouter
→ WorkGraphTopologyRouter
→ refresh due provider/catalog/policy evidence
→ SourceReliabilityLedger filters stale discovery claims
→ construct ProviderDependencyGraph
→ classify EntitlementClass per account/route
→ BillingModeProof
→ FundingSourceProof + CreditBucketSourceAttestation
→ SpendInvariantProof
→ refresh FreeCapacityLedger
→ SharedQuotaKnapsackController
→ QuotaReservationLedger / StageAdmissionController
→ LogicalModelRouter chooses target intelligence capability
→ EndpointRealizationRouter resolves exact eligible RouteCell
→ validate PriceEpoch + privacy/use scope + feature funding
→ validate ModelIdentity + Protocol + SemanticHealth
→ choose RecoveryPair / reserve standby
→ obtain IntelligenceLease + CommitEpoch
→ choose BindingGranularityPolicy
→ execute stage/operation
→ preserve evidence graph + semantic environment manifest
→ on recoverable error run SameRouteRecoveryProbe
→ on beneficial/required switch freeze safe boundary
→ revoke old mutation authority by advancing CommitEpoch
→ choose AdaptiveHandoffEncoding
→ HandoffRoundTripProbe
→ destination ProgressiveTakeover
→ ContinuityCertification gate
→ resume only under current RouteOwnershipFence
→ ResourceFrontier/OCC validates mutations
→ PlanDependencyFence validates action dependencies
→ deterministic verification / Done Contract
→ terminal reward + RoutingCreditAssignment
→ update capability/skill/continuity/dependency evidence
→ drift detection / shadow audits / RouterGainCertificate
→ release unused quota reservations
→ persist BestKnownJointRuntimeState
```

---

# Part LIV — Non-negotiable invariants

## 265. AlinaCoder must never

- flatten every zero-cost mechanism into a single `free=true` flag;
- assume an account's marketing plan determines the exact funding bucket of a request;
- consume purchased credits after a free allowance ends;
- treat user-funded wallet usage as free autonomous capacity by default;
- count two dependent gateways as independent availability or reasoning diversity;
- trust a stale community free-provider claim over newer first-party evidence;
- couple the primary learned router directly to permanent model IDs when capability-decoupled routing can be used;
- route below mandatory capability shortfall thresholds to save quota;
- spend scarce frontier quota on trivial work with negligible expected uplift while higher-value work is pending;
- start a long stage without enough primary/standby quota or a safe checkpoint plan;
- reward every model in a multi-stage task equally from one terminal outcome;
- blame a downstream route for a corrupted handoff without attribution evidence;
- switch models on every transient reasoning/test error;
- use graph-only handoff when nuance cannot be represented safely;
- paraphrase away MUST_EXACT user constraints, hashes, tests or commit epochs;
- assume handoff quality is symmetric between two model families;
- call a failover “seamless” without continuity evidence;
- allow an old timed-out provider response to commit after a newer route epoch exists;
- let provider responses directly mutate canonical state;
- hold stale plans merely because fresh facts were injected into memory;
- resume a checkpoint under incompatible semantic resource versions without validation/replanning;
- parallelize overlapping mutations without resource-version/fencing protection;
- treat HTTP/provider availability as equivalent to semantic continuity;
- allow optional Supabase services to become mandatory for local execution;
- claim Vercel, LLM7, Pollinations, Cohere, Cerebras, Ollama Cloud, NVIDIA NIM or any other provider is permanently free based on this document;
- bypass provider terms, quotas, account verification, payment controls, safety policies or geographic restrictions;
- weaken deterministic verification, rollback, IntentContract, Done Contract or zero-spend rules in pursuit of a stronger model.

## 266. Final target behavior

```text
Open alinacoder.exe
→ speak naturally in French or English
→ AlinaCoder externalizes exact task state
→ discovers all current legitimate intelligence sources
→ learns which sources are truly independent
→ classifies exactly how each free entitlement is funded
→ rejects any route that can reach paid funds
→ tracks all free capacity in one global ledger
→ reserves scarce frontier quota for hard/high-value work
→ infers the skills and capability dimensions the current stage needs
→ chooses the best cognitive regime and collaboration topology
→ selects the strongest logical intelligence meeting those needs
→ resolves it to the safest zero-cost healthy endpoint
→ reserves an independent compatible recovery route
→ gives the primary a fenced commit epoch
→ works while continuously measuring evidence, quota and health
→ recovers on useful transient evidence without pointless model churn
→ when switching is necessary, encodes the handoff intelligently
→ verifies the new model actually reconstructed the task
→ advances the commit epoch so the old model can never write again
→ progressively grants the new model authority
→ validates plan dependencies and resource versions before mutation
→ verifies the final work deterministically
→ attributes success/failure to the correct routing decisions
→ improves capability, quota, handoff and provider models from real outcomes
→ automatically promotes better new brains and retires degraded/paid/unsafe ones
→ autonomous paid inference spend remains exactly €0
```

The architectural destination is:

> **An autonomous frontier-intelligence exchange: AlinaCoder reasons over capabilities, skills, orchestration regimes, concrete endpoints, funding buckets, shared quotas, upstream dependencies and pairwise continuity as one controlled system. It acquires the strongest currently legitimate intelligence, spends scarce free capacity where it changes outcomes most, and performs fenced, semantically verified takeovers so changing LLMs never means surrendering the user's intent, verified state or commit authority.**
