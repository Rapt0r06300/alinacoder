# AlinaCoder v0.2 — Frontier Oracle, OOD Safety & Certified Continuity Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose

This amendment strengthens the existing Self-Optimizing Frontier Hunter so that AlinaCoder can autonomously seek the strongest legitimate zero-additional-cost intelligence available **without trusting unsupported router confidence, stale benchmark reputation, unsafe free tiers, or another model's failed trajectory**.

The core objective is:

> **If the router does not know, it must know that it does not know. New models should join without retraining the whole router; router gains must be certified; handoffs must preserve verified task state rather than inherit another model's mistakes; and “free” must be a hard-stop entitlement, never a hope.**

This amendment is additive and normative together with the existing v0.2 baseline and later approved amendments, especially:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-routing-seamless-handoff-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-adaptive-frontier-fabric-routing-stability-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-autopilot-control-plane-hardening-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-self-optimizing-frontier-hunter-seamless-failover-amendment.md`

This amendment has precedence for:

- out-of-distribution routing safety;
- open-set onboarding of previously unseen models;
- routing evidence precision;
- statistical certification of router gain;
- compositional cognitive-operation routing;
- progressive local-model escalation;
- direction-aware trajectory handoff;
- task-relative sufficient state;
- staged continuity restoration;
- per-session compare-and-swap sequencing;
- experimental cross-model context mobility;
- resource-shadow-price routing over free quotas;
- pessimistic routing under uncertainty;
- hard-stop free-entitlement classification;
- per-feature billing proof;
- Alibaba Cloud Model Studio Singapore Free Quota Only integration candidate;
- Scaleway and SiliconFlow eligibility classification;
- release-radar onboarding of newly published frontier models;
- optional Supabase durable evidence scheduling/replay refinements.

All prior IntentContract, safety, privacy, local-first, zero-paid-spend, verification, rollback, resource, continuity and Git `main`-only invariants remain binding.

The monetary policy remains absolute:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
ALLOW_PAID_FALLBACK = false
ALLOW_AUTO_RELOAD = false
ALLOW_PURCHASED_CREDIT_CONSUMPTION = false
```

---

# Part I — Router epistemics: know when the router does not know

## 2. Routing uncertainty is a first-class state

A routing policy must not always output a confident winner.

It must estimate whether the current task lies inside the region where its historical routing evidence is relevant.

Introduce:

```text
TaskDistributionSupportScore
```

This score estimates how well the current task is supported by previously verified routing experience.

## 3. Support dimensions

Support should consider at least:

```text
task family
repository language
framework/toolchain
bug/failure class
required tools
required modality
reasoning depth
expected horizon
context length
mutation risk
verification shape
project sensitivity
conversation/noise pattern
current stage
```

## 4. OODRouterGuard

Introduce:

```text
OODRouterGuard
```

States:

```text
IN_DISTRIBUTION
WEAKLY_SUPPORTED
OUT_OF_DISTRIBUTION
UNKNOWN_SUPPORT
```

## 5. OOD behavior

When support is weak or unknown, AlinaCoder must not blindly trust a learned route ranking.

Preferred escalation:

```text
retrieve nearest verified tasks
→ widen uncertainty
→ use conservative capability gates
→ favor strongest proven eligible route
→ add independent verifier when consequence is high
→ run bounded challenger probes when quota permits
```

## 6. No forced winner

The router may return:

```text
NO_CERTIFIED_ROUTE_PREFERENCE
```

This is a valid result.

## 7. ConservativeFallbackSelector

When the learned policy is unsupported:

```text
ConservativeFallbackSelector
```

chooses from routes that satisfy:

```text
hard eligibility
minimum verified capability
strong semantic health
continuity compatibility
sufficient quota reserve
```

and prioritizes the most robust proven route rather than the highest uncertain predicted score.

## 8. OOD is not task failure

OOD detection means the **router** lacks evidence.

The underlying task can still be solved by a strong model.

## 9. OOD feedback

Completed OOD tasks become especially valuable evidence.

They should update:

```text
routing memory
behavior profiles
support geometry
challenge calibration set
```

only after objective verification.

---

# Part II — ExecutionGroundedRoutingMemory

## 10. Information deficit is a routing bottleneck

The routing system should explicitly remember **which exact routes succeeded on which verified task characteristics**.

Introduce:

```text
ExecutionGroundedRoutingMemory
```

## 11. Routing memory item

A routing memory record may contain:

```text
routing_memory_id
task_descriptor
repo_stack_descriptor
route_cell_id
computation_regime
terminal outcome
Done Contract result
verification evidence
latency profile
quota consumption
continuity result
recovery loops
failure signature
observation precision
created_at
freshness state
```

No secret-bearing raw prompt is required.

## 12. Retrieval modes

Routing memory retrieval should combine:

```text
exact symbolic match
semantic similarity
task ontology similarity
failure-signature similarity
temporal recency
route fingerprint compatibility
```

## 13. Memory cannot override current route identity

If the RouteCell fingerprint changed, old memory becomes a prior only.

## 14. Nearest verified examples

Before an uncertain routing choice, the router may retrieve the nearest small set of verified historical tasks.

This is preferable to extrapolating from a global average.

## 15. Evidence not rhetoric

A prior task record is useful only if its outcome was actually verified.

Model self-report is not a routing memory success label.

---

# Part III — TaskDescriptorPredictor separated from policy

## 16. Prediction and policy must be separate

A model that predicts task characteristics must not decide billing, privacy or mutation authority.

Introduce:

```text
TaskDescriptorPredictor
```

## 17. Predicted fields

The predictor can estimate:

```text
task family
difficulty
reasoning mode
expected output size
expected number of tool rounds
likely modalities
likely context growth
likely verification type
likely stage transitions
```

## 18. Hard policy remains deterministic

These predictions feed routing but cannot bypass:

```text
BillingSurfaceGuard
privacy gate
license/use-scope gate
capability minimums
state lease
mutation policy
Done Contract
```

## 19. Tiny local routing model

AlinaCoder may use a small local router model or classifier for this prediction layer.

Requirements:

```text
fast
low memory
locally runnable
replaceable
benchmarkable
not authoritative
```

## 20. Session-incremental routing cache

The lightweight task descriptor layer may cache stable session features so each routing decision does not recompute the entire conversation.

This cache is derived state, never canonical user intent.

---

# Part IV — Open-set model onboarding

## 21. New models must not require full router retraining

The model ecosystem changes too quickly for a fixed-class router.

Introduce:

```text
ModelBehaviorProfile
OpenSetRouteEmbedder
```

## 22. ModelBehaviorProfile

A behavior profile describes what a new RouteCell actually does on a compact, discriminative calibration suite.

Fields can include:

```text
route_cell_id
fingerprint
coding_behavior_vector
debugging_behavior_vector
reasoning_behavior_vector
tool_behavior_vector
structured_output_vector
French_instruction_vector
long_context_vector
vision_vector
latency_vector
continuity_vector
abstention_calibration
sample_count
uncertainty
```

## 23. Profile, not class label

The router should compare:

```text
task representation
↔ route behavior profile
```

instead of treating every concrete model ID as a permanently trained class.

## 24. OpenSetRouteEmbedder

`OpenSetRouteEmbedder` maps previously unseen RouteCells into the routing space from their measured profile.

This allows immediate participation as a challenger without retraining the full router.

## 25. CalibrationBudgetAllocator

Calibration quota is scarce.

Allocate probes among:

```text
coverage probes
diagnostic/disagreement probes
semantic diversity probes
```

## 26. Coverage probes

Coverage probes sample common task families so the profile is not built only on pathological cases.

## 27. Diagnostic probes

Diagnostic probes target boundaries where current champion routes disagree.

These maximize information about whether the new model fills a real gap.

## 28. Diversity probes

Diversity probes intentionally span different semantic/task regions.

## 29. Stop early when dominated

If a new route is clearly dominated across relevant capabilities and has no specialist niche, stop consuming quota on calibration.

## 30. Accelerate promising routes

If early evidence shows material capability gain on high-value task families, allocate more calibration budget subject to reserves.

## 31. Open-set uncertainty

A newly profiled route always starts with elevated uncertainty.

A profile enables routing participation; it does not grant champion status.

---

# Part V — EvidencePrecision

## 32. Not all feedback is equally trustworthy

Introduce:

```text
EvidencePrecision
RewardObservationQuality
```

## 33. Precision hierarchy

Highest precision examples:

```text
deterministic tests
compiler/build result
machine-checked task outcome
reproducible runtime assertion
schema validation
```

Medium precision examples:

```text
independent verifier with evidence
repeatable property checks
user-confirmed correction/outcome
```

Lower precision examples:

```text
LLM judge
heuristic score
proxy reward
self-reported confidence
```

## 34. Weighted posterior update

Route learning updates should be weighted by observation precision.

A low-confidence judge result must not move the route posterior as much as a deterministic successful build/test.

## 35. Selective logging bias

Evidence precision should also account for whether outcomes are missing non-randomly.

Example:

```text
only easy tasks receive deterministic tests
```

must not create an illusion that a route is universally reliable.

## 36. Drift reduces precision

Older evidence under a changed workload or serving environment receives lower effective precision.

## 37. Precision is learned/calibrated

Where useful, AlinaCoder can measure how well each proxy predicted later deterministic outcomes and recalibrate it.

---

# Part VI — RouterGainCertificate

## 38. A complicated router must prove that routing helps

Introduce:

```text
RouterGainCertificate
```

The router itself is treated as a candidate subsystem that must demonstrate value.

## 39. BaselinePrimaryPolicy

Always retain at least one simple baseline:

```text
BaselinePrimaryPolicy
```

Examples:

```text
strongest proven eligible route for task family
static champion + deterministic failover
```

## 40. Certification question

Before broad promotion, answer:

> Does the candidate routing policy produce a reliably positive terminal gain over the baseline under the deployment distribution?

## 41. Lower bound, not average optimism

Promotion should use a conservative confidence lower bound on measured gain.

If the lower bound does not exceed the minimum promotion threshold:

```text
WITHHOLD_ROUTER_PROMOTION
```

## 42. Correct sampling unit

Do not treat thousands of similar prompts from the same workload as thousands of independent deployment conditions.

Certification should resample/group by meaningful units such as:

```text
repository
task family
bug class
project
workflow type
```

## 43. Cluster-aware robustness

A routing gain concentrated in only a tiny number of workload clusters is fragile.

The certificate must report this concentration.

## 44. Distribution-shift allowance

Where feasible, the certificate should include a robustness margin for plausible deployment shift.

## 45. Certification states

```text
CERTIFIED_POSITIVE_GAIN
INSUFFICIENT_EVIDENCE
NO_MEASURABLE_GAIN
NEGATIVE_GAIN
DISTRIBUTION_FRAGILE
```

## 46. No vanity promotion

A router may have excellent route-classification accuracy while still failing to improve terminal task success.

Only terminal outcome gain matters.

## 47. Router rollback

The last certified router policy is retained as:

```text
BestKnownRouterState
```

A newly active router that regresses automatically rolls back.

---

# Part VII — Pessimistic routing under uncertainty

## 48. PessimisticOptimisticRouter

Introduce a conservative control mode:

```text
PessimisticOptimisticRouter
```

## 49. Principle

When evidence is uncertain:

```text
quality/success
→ use conservative lower estimate

resource/quota consumption
→ use conservative upper estimate
```

## 50. Why

A speculative route should not be selected merely because its mean estimate is high if:

```text
few observations
quota consumption uncertain
failure probability uncertain
```

## 51. Risk classes

For high-consequence tasks, uncertainty penalties increase.

For low-risk read-only exploration, uncertainty can instead justify a challenger probe.

## 52. Safety is not averaged

Hard safety/price/privacy gates remain lexicographic and are never converted into expected-value penalties.

---

# Part VIII — ResourceShadowPriceController

## 53. Zero-money routing still has scarce resources

Even when every eligible route costs exactly €0 autonomously, free capacity is finite.

Treat resources such as:

```text
requests/day
requests/minute
tokens/day
tokens/minute
monthly included tokens
model-specific trial tokens
recovery reserve
latency budget
local GPU time
context budget
```

as constrained resources.

## 54. ResourceShadowPriceController

Introduce:

```text
ResourceShadowPriceController
```

This controller assigns an internal scarcity value to each resource without converting monetary spend into an allowed objective.

## 55. Future-value conservation

Do not spend the last high-quality free quota on low-value work if a likely critical stage is imminent.

## 56. Multiple resource constraints

A route can be attractive in one resource and expensive in another.

Example:

```text
fast RPM
but tiny daily token allowance
```

## 57. Hard meter before commitment

Immediately before each remote call:

```text
exact route
exact feature set
estimated worst-case resource use
reserve floor
```

must pass a hard resource meter.

## 58. Shadow price adapts

As quota reset approaches or alternate capacity improves, the scarcity value may change.

## 59. Money never becomes a shadow-price escape hatch

There is no internal price at which a paid route becomes acceptable.

Paid routes remain hard-ineligible.

---

# Part IX — FreeAccessClass v2

## 60. Extend free-access classification

Canonical classes become:

```text
LOCAL_NO_API_BILLING
ZERO_PRICE_MODEL
HARD_STOP_FREE_QUOTA
SOFT_FREE_QUOTA_PAID_OVERFLOW
RECURRING_FREE_CREDIT_HARD_STOP
RECURRING_FREE_CREDIT_SOFT_OVERFLOW
TRIAL_CREDIT_HARD_STOP
TRIAL_CREDIT_SOFT_OVERFLOW
PROMOTIONAL_CREDIT_HARD_STOP
PROMOTIONAL_CREDIT_SOFT_OVERFLOW
EVALUATION_ONLY
UNKNOWN_BILLING_BEHAVIOR
```

## 61. Safe-by-default classes

Potentially eligible after all other gates:

```text
LOCAL_NO_API_BILLING
ZERO_PRICE_MODEL
HARD_STOP_FREE_QUOTA
RECURRING_FREE_CREDIT_HARD_STOP
TRIAL_CREDIT_HARD_STOP
PROMOTIONAL_CREDIT_HARD_STOP
```

## 62. Blocked-by-default classes

```text
SOFT_FREE_QUOTA_PAID_OVERFLOW
RECURRING_FREE_CREDIT_SOFT_OVERFLOW
TRIAL_CREDIT_SOFT_OVERFLOW
PROMOTIONAL_CREDIT_SOFT_OVERFLOW
UNKNOWN_BILLING_BEHAVIOR
```

## 63. Evaluation-only routes

An evaluation-only route may be used only when the current project/use actually fits that scope.

It cannot silently become normal production capacity.

---

# Part X — FeatureBillingVector

## 64. Model price is not enough

A nominally free inference route can become paid when optional features are enabled.

Introduce:

```text
FeatureBillingVector
```

## 65. Feature fields

At minimum:

```text
text_inference
reasoning_tokens
cached_input
web_search
grounding
maps/search connector
file storage
OCR
image input
image generation
audio
embeddings
reranking
tool execution
provider-hosted code execution
```

## 66. Exact request proof

Cost proof is computed for the exact feature set requested.

## 67. Automatic feature downgrading

If the base model call is free but an optional provider feature is paid:

```text
disable paid feature
→ provide equivalent local/free tool if safe
→ otherwise reject route
```

## 68. Built-in web search is not assumed free

The router must treat provider-built search/grounding as a separate billable feature unless officially proven otherwise for the exact account/tier.

---

# Part XI — Alibaba Cloud Model Studio Singapore

## 69. High-priority zero-cost frontier candidate

Current official Alibaba Cloud Model Studio documentation describes model-specific new-user free quotas in the Singapore region for eligible International-scope models.

The exact account/model console state is authoritative.

## 70. Critical capability: Free Quota Only

Current official documentation exposes a per-model:

```text
Free Quota Only
```

control.

When enabled and the model's free quota is exhausted, the service stops instead of continuing into normal paid usage.

The documented failure is:

```text
403 AllocationQuota.FreeTierOnly
```

## 71. Classification

A model with:

```text
remaining official free quota > reserve
AND Free Quota Only = enabled
AND exact region/scope eligible
```

can be classified:

```text
HARD_STOP_FREE_QUOTA
```

subject to privacy/license/terms/capability gates.

## 72. High-value current model families to monitor

Current official Model Studio documentation exposes strong families including examples such as:

```text
qwen3.8-max
qwen3.8-max-0902
qwen3.8-flash
qwen3.7-max
qwen3.7-plus
qwen3.6-flash
deepseek-v4-pro
deepseek-v4-pro-0813
deepseek-v4-flash
kimi-k3
glm-5.2
```

Whether each exact model currently receives free quota must be proven from current official/account state.

## 73. Independent per-model quotas

Official documentation states eligible free quotas are model-specific rather than one globally shared token pool.

This creates legitimate independent entitlement cells.

## 74. SnapshotEntitlementCell

Introduce:

```text
SnapshotEntitlementCell
```

Identity includes:

```text
provider
region
model snapshot
account/workspace
free-quota entitlement
expiry
hard-stop state
```

## 75. Snapshot quota does not imply quality inheritance

A dated snapshot with separate free quota is still a distinct RouteCell.

It must not inherit live-quality evidence blindly from an alias or sibling snapshot.

## 76. FreeQuotaPortfolioPlanner

Introduce:

```text
FreeQuotaPortfolioPlanner
```

It may intelligently distribute work across **provider-sanctioned independent free quotas**.

## 77. No quota evasion

This mechanism never:

```text
creates extra accounts
rotates identities
rotates IPs
manufactures keys
```

to bypass provider limits.

## 78. Expiry-aware planning

Free quota expiry is a resource deadline.

The planner may prefer expiring legitimate free quota before long-lived quota when task quality is comparable, while preserving recovery capacity.

## 79. Free quota activation-date uncertainty

Provider program rules can change over time.

The client must inspect actual account entitlement rather than assuming a static activation-era rule.

---

# Part XII — Scaleway Generative APIs

## 80. Current official free tier

Current official Scaleway documentation describes a Serverless free tier of:

```text
1,000,000 tokens
+ 60 minutes audio transcription
```

## 81. Current strong candidate models

Official model documentation currently exposes examples such as:

```text
glm-5.2
deepseek-v4-flash-0731
qwen3.5-397b-a17b
qwen3.6-35b-a3b
mistral-medium-3.5-128b
qwen3-235b-a22b-instruct-2507
qwen3-coder-30b-a3b-instruct
gpt-oss-120b
devstral-2-123b-instruct-2512
```

## 82. Critical billing behavior

Current official FAQ states that after the free tier is exhausted, additional usage is billed.

Therefore the default class is:

```text
SOFT_FREE_QUOTA_PAID_OVERFLOW
```

## 83. Default runtime state

Under AlinaCoder's €0 autonomous-spend policy:

```text
BLOCKED
```

unless an independent official/account-level hard zero-spend cap can be proven before use.

## 84. Discovery value remains

Scaleway remains valuable in the atlas because:

```text
model catalog is strong
European hosting may matter for privacy
future hard-stop controls may appear
```

but “1M free tokens” alone is insufficient.

---

# Part XIII — SiliconFlow

## 85. Dynamic provider candidate

Current official SiliconFlow documentation exposes a machine-readable `/models` endpoint and a mixture of paid and explicitly free model routes.

## 86. Current official free examples

Official docs currently list explicit free routes such as examples from smaller Qwen/GLM/ChatGLM families.

The live model/pricing page remains authoritative.

## 87. Frontier catalog is not automatically free

SiliconFlow also serves powerful current models such as DeepSeek V4, Qwen3/3.x, Kimi and GPT-OSS variants.

Their presence on the platform does not imply zero price.

## 88. Classification

Exact zero-priced routes:

```text
ZERO_PRICE_MODEL
```

subject to account and overage proof.

Promotional signup credit for paid models:

```text
PROMOTIONAL_CREDIT_*
```

with `HARD_STOP` or `SOFT_OVERFLOW` determined from actual account billing controls.

## 89. No free-credit optimism

If promotional credits can silently roll into paid balance/charges, paid-model use remains blocked.

---

# Part XIV — FrontierReleaseRadar

## 90. Discover strong new models before static code catches up

Introduce:

```text
FrontierReleaseRadar
```

## 91. Inputs

The radar monitors, where permitted:

```text
provider /models diffs
official pricing diffs
official changelogs
model release pages
official RSS feeds
trusted model metadata APIs
open-weight registries
benchmark feeds as priors only
```

## 92. Release event

A new route creates:

```text
FrontierReleaseEvent
```

with:

```text
model identity
provider identity
release time
claimed capabilities
context
license
pricing/free evidence
available protocols
source freshness
```

## 93. FrontierCandidatePriorityScore

This score helps decide which newly discovered candidates deserve scarce calibration quota.

Inputs may include:

```text
coding benchmark prior
agentic benchmark prior
context capability
open-weight reputation
new capability coverage
provider quality
potential zero-cost entitlement
```

## 94. Priority score never bypasses gates

A spectacular external benchmark cannot bypass billing/privacy/license proof.

## 95. New release fast lane

A highly promising, officially free/hard-stop route can enter an accelerated **shadow** calibration lane.

It still cannot skip semantic/protocol/continuity canaries.

---

# Part XV — OperationGraphRouter

## 96. The best brain is not always the best workflow

The router must choose not only a model but the sequence of cognitive/execution operations.

Introduce:

```text
OperationGraphRouter
CognitiveProgramPolicy
```

## 97. Candidate operations

```text
DIRECT_REASON
DECOMPOSE
RETRIEVE_LOCAL
SEARCH_WEB
INSPECT_REPO
RUN_PROBE
GENERATE_TEST
DEBUG_CAUSALLY
DELEGATE_SPECIALIST
VERIFY
ADVERSARIAL_REVIEW
REFINE
```

## 98. Composition matters

A task may require:

```text
DECOMPOSE
→ INSPECT_REPO
→ RUN_PROBE
→ DEBUG_CAUSALLY
→ GENERATE_TEST
→ PATCH
→ VERIFY
```

rather than one model call.

## 99. Model selection can vary by operation

Each operation receives its own capability requirement while respecting task affinity and handoff cost.

## 100. Static proven workflow fallback

When operation-selection confidence is diffuse/OOD:

```text
fallback to proven static workflow
```

rather than composing an incomplete cognitive program.

## 101. Operation reward

Do not reward operation selection from whether an operation was invoked.

Reward comes from terminal task success and useful intermediate evidence.

---

# Part XVI — ProgressiveEscalationProbe

## 102. Early weakness detection for local/open models

For routes where token-level/logit signals are legitimately available, introduce:

```text
ProgressiveEscalationProbe
```

## 103. Candidate signals

```text
entropy
margin between likely tokens
repetition instability
schema drift
invalid tool-call probability
abnormal stop behavior
```

## 104. Signal is not correctness

Token confidence cannot prove answer correctness.

It is only an escalation feature.

## 105. Pre-emission escalation

If the local route shows strong early instability before semantic output is committed:

```text
stop candidate generation
→ escalate at PRE_EMISSION boundary
→ rehydrate stronger eligible route from canonical state
```

## 106. Cloud limitation

If a hosted provider does not expose trustworthy token probabilities, AlinaCoder must not invent them.

## 107. Calibration requirement

Progressive escalation thresholds must be calibrated against later verified outcomes on the actual model/quantization.

---

# Part XVII — HandoffFormatRouter

## 108. One handoff format is not optimal for every task

Introduce:

```text
HandoffFormatRouter
```

## 109. Handoff formats

```text
TYPED_GRAPH
NATURAL_LANGUAGE_DIGEST
HYBRID_GRAPH_PLUS_DIGEST
EXACT_CANONICAL_RECORDS
```

## 110. Typed graph best use

Prefer structured graph for:

```text
constraints
dependencies
accepted decisions
proof relationships
task DAG
failed hypotheses
files/symbols
rollback points
```

## 111. Natural-language digest best use

Prefer compact NL for:

```text
subtle motivation
trade-offs
ambiguous user phrasing
context needed for flexible continuation
```

## 112. Hybrid default

For difficult coding handoff, the preferred format is often:

```text
exact typed core
+
small narrative rationale
```

## 113. Receiving-model compatibility

The codec must consider whether the target model reliably understands the selected graph schema.

## 114. Format canary

A model that fails to reconstruct key constraints from graph handoff cannot receive graph-only takeover authority.

---

# Part XVIII — DirectionAwareTrajectorySanitizer

## 115. Full trajectory transfer can harm escalation

A weak model's failed reasoning can anchor a stronger model to the same mistaken approach.

Introduce:

```text
DirectionAwareTrajectorySanitizer
```

## 116. Weak → strong escalation

Default policy:

```text
DO NOT forward the weak model's full narrative trajectory
```

Instead transfer primarily:

```text
user intent
constraints
verified repo state
accepted decisions
objective observations
error signatures
disproven hypotheses
failed experiments + results
current artifacts
next safe objective
```

## 117. Preserve failed evidence, not failed persuasion

The stronger model should know:

```text
“attempt X produced error Y”
```

but need not inherit pages of weak-model reasoning that motivated X.

## 118. Strong → weak downshift

A weaker target may benefit from more distilled rationale produced by the stronger model.

Transfer may include:

```text
accepted architecture rationale
validated decomposition
known dangerous alternatives
precise next steps
```

## 119. Same-strength lateral failover

Use normal canonical state + minimal route-specific continuity data.

## 120. Direction-specific benchmark

Measure:

```text
weak_to_strong_full_trajectory
weak_to_strong_sanitized
strong_to_weak_full_digest
strong_to_weak_minimal
```

on controlled tasks.

## 121. No hidden chain-of-thought portability

Sanitization deals only with observable/admissible trajectory information.

Canonical continuity never requires private hidden chain-of-thought.

---

# Part XIX — TaskRelativeSufficientState

## 122. Handoff is a pre-query coding problem

The handoff must remain useful even before the exact next tool result or downstream query is known.

Introduce:

```text
TaskRelativeSufficientState
```

## 123. Retention classes

Every handoff item is classified as:

```text
MUST_EXACT
COMPRESSIBLE_WITH_LOSS_BOUND
RAW_OBSERVATION_REQUIRED
RECOMPUTABLE
DISCARDABLE
```

## 124. MUST_EXACT examples

```text
current IntentContract
explicit user negations/corrections
security/safety constraints
repo identity
HEAD/worktree state
accepted architectural decisions
Done Contract
rollback boundary
```

## 125. COMPRESSIBLE_WITH_LOSS_BOUND examples

Repeated evidence can be summarized only if the replacement's impact on later decisions is understood/tested.

## 126. RAW_OBSERVATION_REQUIRED examples

Keep raw observation when:

```text
summary may erase decisive detail
failure signature is fragile
exact compiler/runtime output matters
user wording carries unresolved referential meaning
```

## 127. RECOMPUTABLE examples

Derived indexes or cheap summaries can be regenerated from canonical source.

## 128. HandoffRetentionRisk

Each proposed compaction carries:

```text
HandoffRetentionRisk
```

## 129. Context budget is not sufficient justification

Do not drop high-risk exact state merely because newer conversational turns are more recent.

---

# Part XX — ContinuityRestoreBarrier

## 130. Restoration is staged

Introduce:

```text
ContinuityRestoreBarrier
```

## 131. Restore phases

```text
DISCOVER_AVAILABLE_STATE
→ STAGE_REQUIRED_COMPONENTS
→ VALIDATE_COMPONENTS
→ VERIFY_STATE_VERSION
→ DRY_CONTINUATION_CHECK
→ COMMIT_RESTORED_STATE
```

## 132. Partial restore never becomes canonical

If any required component is invalid/missing:

```text
RESTORE_ABORTED
```

and AlinaCoder falls back to a lower valid restoration tier or deterministic reconstruction.

## 133. Bounded restore working set

Large reusable context/cache artifacts may be restored in bounded chunks so restoration does not require all external state to live in memory simultaneously.

## 134. All-or-nothing semantic validity

Chunked transport does not imply chunked semantic commitment.

The request becomes restored only when all required semantic components validate.

---

# Part XXI — Per-session sequencing and compare-and-swap

## 135. Concurrent turns are a correctness risk

Two workers must never both believe they own the same canonical session version.

## 136. SessionVersionCAS

Every canonical state mutation uses:

```text
expected_state_version
→ compare-and-swap
```

## 137. Per-session sequencer

Introduce a lightweight:

```text
SessionSequencer
```

for ordering commits within one conversation/task.

## 138. Model calls can be concurrent, canonical commits cannot race

Parallel challengers may reason simultaneously.

Only a response holding the valid lease/version can commit state.

## 139. No shared mutable history arrays

Each async model attempt receives an immutable snapshot/projection of the canonical session state.

## 140. Context bleed is catastrophic

Cross-session contamination triggers:

```text
SEVERE_CONTINUITY_INCIDENT
```

and invalidates the affected outcome evidence.

---

# Part XXII — Context mobility and KV reuse research lane

## 141. KV cache is computation state, not task truth

No KV cache may replace the canonical task record.

## 142. CrossModelKVReuseCandidate

Introduce an experimental local optimization:

```text
CrossModelKVReuseCandidate
```

## 143. Initial scope

Initial eligible scope should be conservative:

```text
local/self-hosted
same model family
known compatible architecture
pair-specific calibration
```

## 144. Pair-specific proof

A KV mapper is enabled only after demonstrating acceptable retention on:

```text
long-context tests
multi-turn tests
coding tasks
constraint-retention probes
```

## 145. Accuracy floor

If mapped-cache performance falls below the configured target-route floor:

```text
full target prefill
```

wins.

## 146. Drift measurement

Track quality drift over repeated handoffs/turns.

## 147. ContextMobilityLab

Future research lane:

```text
ContextMobilityLab
```

may evaluate cross-family cache/context transformations.

## 148. Cross-family use is not production-default

It remains experimental until hidden evaluation proves reliability and rollback is trivial.

## 149. Semantic state remains portable even if cache is not

Failover correctness must work with zero cache portability.

---

# Part XXIII — Provider-specific hard-stop capability

## 150. FreeQuotaOnlyCapability

Normalize provider-native hard-stop mechanisms into:

```text
FreeQuotaOnlyCapability
```

## 151. Manifest fields

```text
supported
scope
model_specific
account_specific
can_be_enabled_programmatically
proof_source
enabled_state
exhaustion_error
last_verified_at
```

## 152. Hard-stop proof outranks balance prediction

A provider-native free-only mode is stronger than merely estimating that current balance is probably enough.

## 153. Soft-overflow provider cannot be made safe by optimism

If paid overflow can happen and AlinaCoder cannot structurally prevent it:

```text
BLOCK_REMOTE_ROUTE
```

---

# Part XXIV — FreeQuotaPortfolioPlanner

## 154. Goal

Maximize verified task success using the strongest legitimate free capacity while preserving recovery reserves.

## 155. Portfolio unit

Capacity is tracked by:

```text
entitlement cell
quota failure domain
route cell
reset/expiry clock
```

## 156. Independence proof

Two quotas are considered independent only when provider/account semantics prove it.

## 157. Legitimate per-model quotas

Provider-documented independent per-model quotas may be used independently.

This is not quota evasion.

## 158. Reset-aware scheduling

For similar-quality routes:

```text
expiring legitimate quota
```

may be preferred before long-lived quota, but never at the expense of required reliability.

## 159. Recovery reserve remains protected

Each failure domain retains minimum reserve based on available alternatives and current task horizon.

---

# Part XXV — New-model behavioral probe design

## 160. Probe suite must be discriminative

Do not spend quota running thousands of redundant generic benchmarks.

## 161. Probe categories

```text
repo navigation
exact patch generation
bug localization
causal debugging
test generation
tool schema adherence
structured JSON
long-context retrieval
cross-file dependency reasoning
ordinary/noisy French
negation/correction handling
abstention under missing evidence
security constraint retention
```

## 162. Difficulty ladder

Each category includes a small ladder from trivial to difficult.

## 163. Adaptive stopping

If a route fails low-rung essentials repeatedly, skip expensive high-rung probes for that category.

## 164. Boundary probes

The highest-value probes are often those where current top routes differ.

`RoutingBoundaryMiner` supplies such cases.

## 165. Real project probes

Where safe, anonymized/fixture versions of real project failure patterns should supplement synthetic tests.

---

# Part XXVI — Router self-improvement loop

## 166. Router changes are self-improvements

A modification to routing logic follows the same disciplined loop as any other self-improvement:

```text
baseline
→ hypothesis
→ candidate policy
→ offline replay
→ hidden evaluation
→ shadow
→ limited action
→ RouterGainCertificate
→ promote or reject
```

## 167. No self-edit direct promotion

A router must never rewrite its own policy and immediately trust it on canonical traffic.

## 168. RouterPolicyFingerprint

Every deployed router policy receives:

```text
RouterPolicyFingerprint
```

covering:

```text
code/version
features
weights
thresholds
active model pool assumptions
```

## 169. Changed features invalidate certification

A materially changed policy cannot claim the previous certificate.

## 170. Auto-rollback triggers

Examples:

```text
terminal success regression
false-free admission
OOD overconfidence increase
switch-rate explosion
continuity regression
quota-reserve violation
```

---

# Part XXVII — Multi-model verification quorum

## 171. Quorum is conditional, not default

For high-risk tasks with weak deterministic verification, AlinaCoder may seek independent cognitive verification.

## 172. IndependentVerifierSet

Choose verifiers to maximize:

```text
cognitive diversity
failure-domain diversity
relevant capability
zero-cost eligibility
```

## 173. Same checkpoint mirrors are not cognitive quorum

Two providers serving the same model can add hosting reliability, not independent reasoning diversity.

## 174. Evidence quorum, not vote quorum

Prefer:

```text
independent evidence
counterexample
reproduction
```

over simple answer voting.

## 175. Consensus cannot override tests

Three agreeing models remain wrong if deterministic verification fails.

---

# Part XXVIII — OOD-aware computation regime

## 176. Computation regime changes under OOD

For well-supported tasks:

```text
single proven champion
```

may be enough.

For high-impact OOD tasks:

```text
strong champion
+ execution-grounded retrieval
+ independent verifier
```

may be preferable.

## 177. Do not swarm every OOD task

OOD increases uncertainty; it does not automatically justify a dense multi-agent swarm.

Use Value of Information.

## 178. Local verification remains central

When external model evidence is weak, execute discriminating repository/test probes instead of buying confidence through more model opinions.

---

# Part XXIX — Routing regret decomposition

## 179. Routing regret should be diagnosed

Total regret can be decomposed into:

```text
eligibility regret
capability-estimation regret
OOD-support regret
switch regret
handoff regret
quota-allocation regret
congestion regret
computation-regime regret
verification regret
```

## 180. Why decomposition matters

If failures come from handoff loss, training a better prompt classifier will not solve them.

## 181. Regret-driven improvement

Self-improvement should prioritize the largest measured regret source.

---

# Part XXX — Canonical task ontology

## 182. Task ontology is expandable

Maintain an extensible ontology rather than one flat prompt category.

## 183. Axes

Possible independent axes:

```text
operation family
domain
risk
language
repository stack
horizon
modalities
verification type
interaction pattern
```

## 184. Ontology does not constrain open-set routing

Unknown task types can be represented semantically without requiring a predefined class.

## 185. Ontology revisions preserve provenance

New aliases/supersessions are versioned so old routing evidence remains interpretable.

---

# Part XXXI — Provider research lead ingestion

## 186. Community directories improve recall only

Daily-updated free-LLM directories are useful for finding candidates quickly.

They are not billing authority.

## 187. Lead states

```text
COMMUNITY_LEAD
OFFICIAL_SOURCE_FOUND
ACCOUNT_PROOF_FOUND
ELIGIBLE
REJECTED
```

## 188. Lead freshness

A community lead expires quickly if official confirmation cannot be found.

## 189. Contradiction rule

If directory and official documentation disagree:

```text
official/account evidence wins
```

---

# Part XXXII — Supabase optional evidence orchestration v2

## 190. Supabase remains optional

Local SQLite/event log remains canonical for single-machine operation.

## 191. Current changelog constraints

Current Supabase changelog states the `realtime` schema is locked against arbitrary schema modifications.

AlinaCoder must not attempt to create/alter objects inside that managed schema.

## 192. PGMQ visibility leases

Optional cloud evidence jobs use PGMQ with task-appropriate visibility timeout.

## 193. Poison-job quarantine

Use:

```text
read_ct
oldest_msg_age
failure signature
```

to quarantine repeatedly failing discovery/canary jobs.

## 194. Durable queue before ephemeral notification

The durable job/evidence state is stored before sending Realtime notification.

## 195. Realtime Broadcast Replay

Current Supabase documentation supports replay of earlier database-published Broadcast messages on private channels.

This can help UI/worker clients recover recent route-quarantine or evidence-ready notifications after reconnect.

## 196. Replay is not canonical durability

Finite Broadcast retention means canonical provider evidence remains in durable state/local database/queues.

## 197. pg_cron optional scheduler

When Supabase sync is enabled, `pg_cron` may schedule bounded evidence refresh work.

It must not become required for local operation.

## 198. Queue exactly-once scope

PGMQ's delivery guarantees operate within visibility semantics; consumer-side effects still require idempotency keys.

## 199. Provider probes are idempotent

Every cloud discovery/canary job uses:

```text
probe_id
route_cell_id
expected fingerprint
```

so retry cannot double-apply state.

---

# Part XXXIII — Context projection under OOD

## 200. OOD may increase context needs

A novel task can require more context to reason correctly.

Privacy redaction must not silently make the task unsolvable.

## 201. ProjectionAdequacyScore

Introduce:

```text
ProjectionAdequacyScore
```

## 202. Remote eligibility after projection

A route is remote-eligible only if:

```text
privacy safe
AND projected context still sufficient
```

## 203. If not sufficient

Choose:

```text
local model
private provider
or decomposition that keeps sensitive evidence local
```

rather than transmitting forbidden context.

---

# Part XXXIV — Failure taxonomy extension

## 204. New failure reasons

```text
ROUTER_OOD
ROUTER_GAIN_UNCERTIFIED
ROUTER_POLICY_REGRESSION
ROUTING_MEMORY_LOW_SUPPORT
REWARD_SIGNAL_LOW_PRECISION
OPEN_SET_PROFILE_INCOMPLETE
HANDOFF_TRAJECTORY_CONTAMINATION
HANDOFF_FORMAT_MISMATCH
SUFFICIENT_STATE_LOSS
RESTORE_PARTIAL_INVALID
SESSION_CAS_CONFLICT
CONTEXT_BLEED_DETECTED
FREE_QUOTA_HARD_STOP
FREE_QUOTA_SOFT_OVERFLOW_RISK
FEATURE_BILLING_UNSAFE
SNAPSHOT_ENTITLEMENT_EXPIRED
```

## 205. Failure-specific response

Examples:

```text
ROUTER_OOD
→ conservative fallback + optional verifier

ROUTER_GAIN_UNCERTIFIED
→ baseline policy

SESSION_CAS_CONFLICT
→ reject stale commit and rebase attempt on new canonical state

FREE_QUOTA_HARD_STOP
→ normal eligible failover

FREE_QUOTA_SOFT_OVERFLOW_RISK
→ quarantine route before inference
```

---

# Part XXXV — Acceptance scenarios

## 206. OOD routing

1. A Python web bug resembles many verified tasks → `IN_DISTRIBUTION`, learned route may be used.
2. A novel Rust embedded build failure has no similar history → `OUT_OF_DISTRIBUTION`, router widens uncertainty.
3. OOD task still has one clearly capability-dominant free route → conservative selector can choose it.
4. OOD high-risk mutation lacks deterministic verification → add independent verifier if zero-cost capacity permits.
5. Learned router gives 0.98 confidence on unsupported task → OOD guard can still override it.

## 207. Open-set onboarding

6. New model appears in official `/models` → release event created automatically.
7. Model is paid → tracked but never calibrated with autonomous paid calls.
8. Model is hard-stop free → small calibration begins in shadow/challenger lane.
9. New model dominates early tool/schema probes but fails coding tasks → specialist profile only.
10. New model is clearly dominated after minimal probes → calibration stops early.
11. New model fills a known debugging weakness → additional diagnostic probes allocated.
12. Router need not be retrained merely to represent this new model.

## 208. Evidence precision

13. LLM judge says patch is correct but tests fail → failure receives high-precision negative reward.
14. Deterministic build passes repeatedly → strong positive evidence.
15. Old proxy scores stop predicting real outcomes → proxy precision decays.
16. Few low-precision observations cannot dethrone champion.

## 209. Router certification

17. Candidate router wins average prompt score but gain exists in only one repo family → cluster-aware certificate may withhold promotion.
18. Candidate improves terminal outcomes across diverse repos with positive lower bound → promotion allowed.
19. Shadow estimate predicts gain but no on-policy evidence exists → not fully certified.
20. Active router later regresses → BestKnownRouterState restored.

## 210. Alibaba Free Quota Only

21. Exact eligible model has 1M remaining free tokens and Free Quota Only enabled → can be admitted.
22. Quota is nearly exhausted below reserve → route may be withheld for critical recovery.
23. Provider returns `AllocationQuota.FreeTierOnly` → no error panic; fail over to next eligible zero-cost route.
24. Another eligible model has its own independent provider-sanctioned free quota → planner may use it.
25. Same account lacks Free Quota Only on a model and paid continuation is possible → route blocked.
26. Dated snapshot has independent quota → separate entitlement cell, separate route evidence.
27. Alias moves to new snapshot → previous quality posterior not blindly inherited.

## 211. Scaleway

28. Account has 800k free tokens but paid overflow remains enabled with no hard cap → blocked before call.
29. Future account control proves hard zero-spend cap → classification may change after live proof.

## 212. SiliconFlow

30. Exact live model row says input/output free → candidate can enter admission.
31. Strong DeepSeek/Kimi route is present but priced >0 → excluded despite provider having other free models.
32. Promotional credits exist but paid overflow cannot be disabled → powerful paid route remains excluded.

## 213. Feature billing

33. LLM inference free but provider web search charged → web search disabled.
34. Free route requires paid OCR for supplied file → route ineligible unless local/free OCR replacement exists.
35. Cached input is free but output paid → not a free route.

## 214. Handoff tax

36. Weak model repeatedly fails and stronger route is selected → sanitizer removes weak narrative while retaining failed experiment facts.
37. Strong architect hands task to weaker executor → distilled validated plan/rationale retained.
38. Full weak trajectory benchmark performs worse than sanitized takeover → sanitizer policy promoted for that direction.

## 215. Handoff format

39. Receiving model reliably parses typed dependency graph → graph core used.
40. Model loses subtle user intent from graph-only handoff → hybrid graph + narrative required.
41. Handoff codec cannot represent required attachment → takeover blocked.

## 216. Sufficient state

42. Compaction wants to drop old explicit user prohibition → MUST_EXACT prevents deletion.
43. Repeated benchmark logs can be summarized with proven retention → compressible.
44. Exact compiler error contains decisive detail → raw observation retained.

## 217. Restoration

45. First three of four restore chunks load, fourth fails → entire restored semantic state remains uncommitted.
46. Lower local tier is valid → fall back to it.
47. No cache reusable → deterministic text/structured canonical-state reconstruction.

## 218. Concurrency

48. Two model attempts both started from state v41 → only first valid CAS commit creates v42.
49. Second response arrives later → stale lease rejected, cannot overwrite v42.
50. Session snapshot is immutable per attempt → no cross-task mutable-array bleed.

## 219. Progressive escalation

51. Local model shows calibrated early schema instability before emission → escalate cleanly.
52. Local model emits confident tokens but deterministic result later fails → confidence feature is recalibrated downward.
53. Cloud route has no logits → no fake uncertainty estimator.

## 220. Context mobility

54. Local Qwen-family KV mapper passes pair-specific hidden tests → optional prefill optimization enabled.
55. Mapper quality drifts below floor → disable and full-prefill target.
56. Cross-family cache experiment looks promising → remains lab-only until hidden evaluation and rollback gates pass.
57. Cache transfer unavailable → semantic continuity still works.

## 221. Supabase optional bus

58. Canary worker crashes before delete/archive → PGMQ visibility expires and job retries.
59. `read_ct` grows beyond poison threshold → job quarantined.
60. Realtime client disconnects → Broadcast Replay may recover recent notification.
61. Replay misses older event → durable queue/table/local evidence still has truth.
62. Supabase unavailable → local routing continues.

---

# Part XXXVI — New metrics

## 222. OOD metrics

```text
ood_detection_recall
ood_false_positive_rate
unsupported_route_overconfidence_rate
nearest_verified_task_coverage
```

## 223. Open-set metrics

```text
new_route_time_to_profile
new_route_probe_count_to_decision
open_set_profile_quality
new_route_time_to_first_verified_use
new_route_false_champion_rate
calibration_value_per_request
```

## 224. Router certification metrics

```text
router_gain_mean
router_gain_lower_bound
router_gain_cluster_concentration
router_certification_sample_size
router_certificate_failure_rate
router_policy_rollback_rate
```

## 225. Evidence metrics

```text
reward_observation_precision
proxy_to_terminal_calibration_error
judge_false_positive_rate
judge_false_negative_rate
```

## 226. Handoff metrics

```text
weak_to_strong_sanitized_gain
weak_to_strong_full_trajectory_gain
strong_to_weak_rationale_gain
handoff_format_success_rate
task_relative_state_retention
must_exact_loss_rate
raw_observation_loss_rate
```

Hard target:

```text
must_exact_loss_rate = 0
```

## 227. Restore metrics

```text
restore_full_commit_rate
partial_restore_exposure_rate
restore_fallback_success_rate
session_cas_conflict_rate
cross_session_bleed_rate
```

Hard targets:

```text
partial_restore_exposure_rate = 0
cross_session_bleed_rate = 0
```

## 228. Free entitlement metrics

```text
hard_stop_free_quota_routes
soft_overflow_routes_blocked
free_quota_utilization_efficiency
recovery_reserve_violations
feature_billing_false_free_admissions
snapshot_entitlement_expiry_detection_latency
```

Hard targets:

```text
paid_autonomous_calls = 0
feature_billing_false_free_admissions = 0
recovery_reserve_violations = 0
```

## 229. Progressive routing metrics

```text
pre_emission_escalation_precision
pre_emission_escalation_recall
wasted_local_generation_tokens
false_escalation_rate
```

## 230. Context mobility metrics

```text
kv_transfer_accuracy_retention
kv_transfer_prefill_speedup
kv_handoff_drift_per_turn
kv_mapper_fallback_rate
```

These metrics never replace semantic continuity metrics.

---

# Part XXXVII — Conceptual modules

## 231. Suggested additions

```text
src/alinacoder/intelligence_mesh/
  task_distribution_support.py
  ood_router_guard.py
  conservative_fallback.py
  execution_routing_memory.py
  task_descriptor_predictor.py
  model_behavior_profile.py
  open_set_route_embedder.py
  calibration_budget.py
  evidence_precision.py
  router_gain_certificate.py
  pessimistic_router.py
  resource_shadow_prices.py
  free_access_class_v2.py
  feature_billing_vector.py
  free_quota_only.py
  free_quota_portfolio.py
  snapshot_entitlement.py
  frontier_release_radar.py
  operation_graph_router.py
  progressive_escalation.py
  handoff_format_router.py
  trajectory_sanitizer.py

src/alinacoder/continuity/
  task_relative_sufficient_state.py
  continuity_restore_barrier.py
  session_sequencer.py
  session_cas.py
  context_mobility_lab.py
  cross_model_kv_candidate.py

src/alinacoder/evaluation/
  ood_router_bench.py
  open_set_onboarding_bench.py
  router_gain_certification_bench.py
  evidence_precision_bench.py
  trajectory_handoff_bench.py
  handoff_format_bench.py
  sufficient_state_bench.py
  restore_atomicity_bench.py
  concurrency_continuity_bench.py
  feature_billing_bench.py
  quota_hard_stop_bench.py
  context_mobility_bench.py
```

Names remain conceptual; implementation may reorganize them without weakening contracts.

---

# Part XXXVIII — Recommended implementation order

## 232. Phase J1 — Evidence and OOD foundations

Implement:

```text
TaskDistributionSupportScore
OODRouterGuard
ExecutionGroundedRoutingMemory
EvidencePrecision
```

before giving more authority to online routing.

## 233. Phase J2 — Open-set route profiles

Implement:

```text
ModelBehaviorProfile
CalibrationBudgetAllocator
OpenSetRouteEmbedder
FrontierReleaseRadar
```

## 234. Phase J3 — Free-entitlement hardening

Implement:

```text
FreeAccessClass v2
FeatureBillingVector
FreeQuotaOnlyCapability
SnapshotEntitlementCell
FreeQuotaPortfolioPlanner
```

and add provider adapters only after these abstractions exist.

## 235. Phase J4 — Alibaba adapter first among new candidates

Prioritize Model Studio Singapore because a provider-native free-quota hard stop is directly aligned with the zero-spend invariant.

## 236. Phase J5 — Soft-overflow provider classification

Add Scaleway discovery adapter as blocked-by-default until hard-stop proof exists.

Add SiliconFlow dynamic free-model discovery with exact pricing evidence.

## 237. Phase J6 — Router certification

Implement offline cluster-aware evaluation and `RouterGainCertificate` before expanding live online-policy authority.

## 238. Phase J7 — Compositional operation routing

Add `OperationGraphRouter` with a safe static workflow fallback.

## 239. Phase J8 — Direction-aware handoff

Implement:

```text
HandoffFormatRouter
DirectionAwareTrajectorySanitizer
TaskRelativeSufficientState
```

before optimizing raw cache mobility.

## 240. Phase J9 — Restore atomicity and session CAS

Implement:

```text
ContinuityRestoreBarrier
SessionSequencer
SessionVersionCAS
```

## 241. Phase J10 — Progressive local escalation

Only after pre-emission semantics and calibration tests are mature.

## 242. Phase J11 — Context mobility lab

KV reuse remains an optimization lane after semantic continuity is proven.

---

# Part XXXIX — Research basis added in this pass

## 243. Research window

This amendment prioritized developments from:

```text
2026-08-05 through 2026-09-04
```

plus directly relevant earlier 2026 work when necessary.

## 244. Drift-Aware Sparse Routing — September 2026

Recent work formulates routing under nonstationary sparse contexts and multiple resource constraints, with rolling audits, conservative reward/resource estimates and a hard resource meter.

Applied here through:

```text
PessimisticOptimisticRouter
ResourceShadowPriceController
hard pre-call resource meter
```

## 245. Agent-as-a-Router / ACRouter — 2026

Research reports that execution-grounded accumulated information can matter more to routing than a static router's raw reasoning ability, especially under OOD tasks.

Applied through:

```text
ExecutionGroundedRoutingMemory
OODRouterGuard
verified feedback loop
```

## 246. SCOPE-Router — August 2026

Open-set routing research demonstrates that unseen models can be represented through compact behavioral profiles and added without retraining the entire router.

Applied through:

```text
ModelBehaviorProfile
OpenSetRouteEmbedder
CalibrationBudgetAllocator
```

## 247. SCX Router — September 2026

Recent zero-shot routing work separates task prediction from policy attributes and uses a lightweight model to predict task type, difficulty, reasoning mode and output length.

Applied through:

```text
TaskDescriptorPredictor
local lightweight router option
strict separation from hard policy gates
```

## 248. LENS — UAI 2026

LENS models varying precision in interaction-derived routing signals under selective logging and drift.

Applied through:

```text
EvidencePrecision
RewardObservationQuality
precision-weighted posterior updates
```

## 249. RouteGuard — August 2026

RouteGuard argues that apparent advisor complementarity or gate AUC does not establish deployable routing gain and proposes finite-sample certification/withholding.

Applied through:

```text
RouterGainCertificate
cluster-aware sampling
promotion withholding
```

## 250. Compositional Meta-Routing — August 2026

Executable routing research shows value in selecting/composing cognitive operations rather than choosing a single operation/model one-shot.

Applied through:

```text
OperationGraphRouter
CognitiveProgramPolicy
OOD fallback to proven static workflow
```

## 251. Pro-Router — August 2026

Progressive routing research uses prompt-level preselection plus token-time uncertainty for escalation.

Applied conservatively to local/self-hosted routes through:

```text
ProgressiveEscalationProbe
```

Token confidence remains only a signal, never correctness evidence.

## 252. Routed Graph Handoff — August 2026

Research shows structured graph handoffs can compress delegation but graph-only transfer can regress on tasks needing adaptive reasoning.

Applied through:

```text
HandoffFormatRouter
HYBRID_GRAPH_PLUS_DIGEST
```

## 253. The Handoff Tax — August 2026

Recent coding-agent experiments report that handing a stronger model the full weak-model trajectory can substantially limit escalation gains, while downshift behavior differs.

Applied through:

```text
DirectionAwareTrajectorySanitizer
```

## 254. Handover of In-Context Learning State Across Session Boundaries — August 2026

Recent theory treats session handoff as task-relative state coding and distinguishes exact decisions/constraints from compressible evidence and irreducible observations.

Applied through:

```text
TaskRelativeSufficientState
retention classes
HandoffRetentionRisk
```

## 255. Cross-model KV transfer and universal context reuse — August 2026

Recent systems work suggests cross-model KV reuse can reduce prefill for some calibrated pairs, including emerging cross-family experiments, but retention varies materially.

Applied only as an experimental optimization lane:

```text
CrossModelKVReuseCandidate
ContextMobilityLab
```

## 256. Bounded-State Restoration — August 2026

Recent restoration work separates total reusable state from bounded live staging and exposes reuse only after request-level validity succeeds.

Applied through:

```text
ContinuityRestoreBarrier
bounded staging
fail-closed semantic commit
```

## 257. ContinuityBench — 2026

Existing failover research reinforces that availability and continuity are separate properties and that per-session concurrency isolation plus jittered retry are mandatory.

Applied through:

```text
SessionSequencer
SessionVersionCAS
immutable attempt snapshots
```

---

# Part XL — Official provider evidence added in this pass

## 258. Alibaba Cloud Model Studio

Current official documentation checked in this research pass includes:

```text
new-user free quota management
model pricing/free quota tables
free quota usage statistics
Free Quota Only control
recommended/current model catalog
newly released models
DeepSeek API documentation
Kimi API documentation
```

The important normative fact is not a permanent token number.

It is that the provider exposes account/model-specific free entitlement **plus a provider-native free-only hard stop** that can prevent paid continuation when correctly enabled.

## 259. Scaleway

Current official documentation checked includes:

```text
Generative APIs pricing
Generative APIs FAQ
supported model catalog
```

The free allowance currently rolls into paid billing after exhaustion, so it remains blocked absent a hard-stop proof.

## 260. SiliconFlow

Current official documentation checked includes:

```text
billing rules
free-model examples
rate-limit rules
/models API
chat-completions model catalog
```

Only exact live zero-priced routes may receive `ZERO_PRICE_MODEL` status.

## 261. Community indexes

Current daily-updated community indexes were used to widen provider discovery recall.

They remain lead generators only.

---

# Part XLI — Canonical routing loop v3

## 262. Frontier Oracle loop

```text
Receive user input
→ repair-aware IntentContract
→ ProjectSensitivityClass
→ CurrentStage / FutureStageForecast
→ TaskDescriptorPredictor
→ TaskDistributionSupportScore
→ OODRouterGuard
→ ExecutionGroundedRoutingMemory retrieval
→ FrontierReleaseRadar / ProviderAtlas freshness check
→ exact RouteCell + SnapshotEntitlementCells
→ SourceFreshnessTrustGraph
→ BillingSurfaceGuard
→ FreeAccessClass v2
→ FreeQuotaOnlyCapability
→ FeatureBillingVector
→ privacy/license/use-scope gate
→ ProviderSafeContextProjection + ProjectionAdequacyScore
→ ModelBehaviorProfile / capability match
→ semantic/protocol/continuity health
→ EvidencePrecision-aware RoutePosterior
→ PessimisticOptimisticRouter
→ ResourceShadowPriceController
→ FreeQuotaPortfolioPlanner
→ TaskAffinityLease / SwitchUtility
→ OperationGraphRouter / ComputationRegimeRouter
→ congestion admission
→ select primary + independent standby
→ optional ProgressiveEscalationProbe
→ inference under EmissionCommitBarrier
→ if switch needed: DirectionAwareTrajectorySanitizer
→ HandoffFormatRouter
→ TaskRelativeSufficientState
→ ContinuityRestoreBarrier
→ ContinuityProof
→ canonical SessionVersionCAS
→ deterministic tools/tests
→ Done Contract
→ terminal reward + EvidencePrecision
→ RoutingDecisionJournal
→ ExecutionGroundedRoutingMemory update
→ RouterGainCertificate evidence update
→ champion/router-policy promotion or rollback decision
```

---

# Part XLII — Non-negotiable invariants

## 263. The Frontier Oracle must never

- pretend every task is in-distribution;
- force a learned routing winner when support is insufficient;
- treat router confidence as deployment evidence;
- retrain the entire router merely because a new model appears;
- give a new model champion status from public benchmarks alone;
- treat low-precision proxy reward as deterministic truth;
- promote a routing policy whose measured gain is not sufficiently supported;
- treat correlated prompts from one workload as independent proof of general routing gain;
- remove the simple certified fallback router;
- optimize paid spend as a soft resource;
- use a free allowance that can silently roll into paid billing unless a hard zero-spend mechanism is proven;
- infer that an optional provider feature is free because base inference is free;
- automatically enable paid web search, grounding or storage on a free model route;
- treat provider-sanctioned independent model quotas as one pool when official account evidence proves independence;
- create multiple accounts/keys/IP identities to manufacture free capacity;
- infer that a powerful provider catalog means its frontier routes are free;
- trust a model snapshot's old quality evidence after an identity change without requalification;
- dump an entire weak-model failed narrative into a stronger model by default;
- erase objective failed-experiment evidence during trajectory sanitization;
- treat one handoff format as universally optimal;
- compact away explicit user prohibitions or accepted constraints;
- expose a partially restored continuity state;
- let two asynchronous attempts commit the same canonical state version;
- share mutable session history across independent tasks;
- treat KV cache as canonical task state;
- enable cross-model KV reuse without pair-specific evidence and deterministic fallback;
- use token-confidence signals as proof of correctness;
- allow Supabase or any cloud state service to become required for local operation;
- use Realtime Broadcast as the sole durable source of route truth;
- allow online router learning to bypass deterministic safety, billing, privacy, verification or Git gates.

## 264. User-visible target behavior

The target experience remains simple:

```text
Open AlinaCoder.exe
→ speak/write normally
→ AlinaCoder understands the real task
→ it knows whether its routing knowledge actually applies
→ it discovers newly released strong models automatically
→ it profiles unseen models without rebuilding the whole router
→ it proves exact zero-cost hard-stop entitlement before remote use
→ it intelligently spends legitimate free quotas without evasion
→ it prefers the strongest verified route for this exact task/stage
→ it preserves reserve capacity for later critical work
→ it detects silent quality/routing drift
→ it switches when measured gain justifies the handoff tax
→ a stronger takeover receives clean verified state, not inherited weak-model confusion
→ the new route proves continuity before mutation
→ the router itself must prove it improves outcomes
→ local deterministic verification remains final authority
→ no paid call occurs autonomously
```

The desired system is not merely a multi-provider LLM proxy.

It is:

> **A self-calibrating Frontier Oracle that continuously discovers and profiles newly available intelligence, knows when its own routing evidence is weak, statistically proves that routing helps, conserves legitimate zero-cost resources, performs direction-aware state handoff without inheriting model mistakes, and preserves a model-independent verified project state across every provider/model transition.**
