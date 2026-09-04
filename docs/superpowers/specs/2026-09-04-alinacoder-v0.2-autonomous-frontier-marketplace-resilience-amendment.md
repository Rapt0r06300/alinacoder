# AlinaCoder v0.2 — Autonomous Frontier Marketplace & Resilient Zero-Cost Routing Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose

This amendment extends the existing Frontier Oracle into a **live autonomous frontier marketplace control plane**.

AlinaCoder must not merely know a static list of strong models. It must continuously discover, qualify, rank, monitor, retire, and replace provider/model routes while preserving the user's task state and the absolute zero-autonomous-spend invariant.

The target is:

> **Always seek the strongest currently eligible intelligence, but treat model quality, price, account state, provider identity, quota, terms, latency, and continuity as live facts that can change at any moment. Every remote route must prove itself immediately before use, every hidden fallback must remain inside the zero-cost safety closure, and every switch must preserve verified canonical state rather than provider-specific conversation state.**

This amendment is additive and normative together with the existing v0.2 baseline and approved amendments, including especially:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-routing-seamless-handoff-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-adaptive-frontier-fabric-routing-stability-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-autopilot-control-plane-hardening-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-self-optimizing-frontier-hunter-seamless-failover-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-oracle-ood-certified-continuity-amendment.md`

This amendment has precedence for:

- provider lifecycle and retirement;
- live pricing epochs;
- account billing-mode proof;
- auto-reload/post-pay hazard detection;
- nested/aggregator routing transparency;
- provider-side fallback closure;
- current zero-cost provider atlas policy;
- quota-header normalization and exhaustion forecasting;
- semantic health and silent-200 failure detection;
- provider circuit breakers and half-open recovery;
- route binding granularity;
- eligible Pareto frontier selection;
- router-policy portfolios;
- joint runtime-state promotion;
- provider/model catalog drift handling;
- provider authentication/onboarding boundary;
- credential-handle storage requirements;
- long-task end-of-availability forecasting;
- model-name semantic prohibition;
- current provider tombstones and supersession rules.

All previous IntentContract, OOD, continuity, safety, privacy, resource, verification, rollback, Git `main`-only and local-first rules remain binding.

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

A provider may be powerful, popular, or nominally “free” and still be **ineligible** if this invariant cannot be structurally proven.

---

# Part I — The live marketplace is canonical, not a static provider list

## 2. FrontierMarketplaceController

Introduce:

```text
FrontierMarketplaceController
```

It owns the live catalog of all candidate intelligence routes.

## 3. Route identity

A route is not merely a model name.

Canonical identity is at least:

```text
provider
aggregator_or_direct
account/workspace
region
plan
endpoint/protocol
model_id
model_revision_or_snapshot
backend_provider_when_known
serving_configuration_fingerprint
billing_mode
feature_set
privacy_scope
use_scope
```

This complete identity is a `RouteCell`.

## 4. Market facts are time-bounded

Every externally sourced fact has:

```text
observed_at
source
source_authority
freshness_ttl
effective_from
known_expiry
confidence
```

## 5. No permanent free flag

There is no durable boolean:

```text
model.is_free = true forever
```

Free eligibility is a time-bounded proof.

## 6. Current-at-dispatch principle

A route may pass discovery hours earlier and still fail dispatch admission if price, quota, plan, backend, terms, or model identity changed.

---

# Part II — ProviderLifecycleState

## 7. Provider lifecycle is first-class

Introduce:

```text
ProviderLifecycleState
```

States:

```text
DISCOVERED
PROBATION
ACTIVE
DEGRADED
PRICE_CHANGED
TERMS_CHANGED
PROTOCOL_CHANGED
AUTH_CHANGED
DEPRECATED
RETIRED
QUARANTINED
TOMBSTONED
```

## 8. ProviderLifecycleEvent

Every material change creates an immutable event containing:

```text
provider_id
old_state
new_state
reason
source
source_timestamp
observed_at
affected_route_cells
required_action
```

## 9. Retirement is immediate

Official retirement of a provider/service causes:

```text
RETIRED
→ remove from eligible graph
→ cancel future probes
→ preserve historical evidence
→ activate replacement search
```

## 10. Tombstones preserve knowledge

Introduce:

```text
ProviderTombstoneRegistry
```

A retired or structurally unsafe provider is not rediscovered every scan as if new.

## 11. Tombstone content

```text
provider
reason
superseding evidence
last valid state
retired_at
source
recheck_after
```

## 12. Tombstones are reversible only by new authoritative evidence

Community listings cannot resurrect an officially retired provider.

## 13. GitHub Models canonical tombstone

As of 2026-07-30, GitHub officially states that GitHub Models is fully retired and that its playground, catalog, inference API and BYOK are unavailable.

Therefore:

```text
GitHub Models
→ RETIRED
→ TOMBSTONED
```

until GitHub itself publishes a new supported service.

---

# Part III — ProviderPolicyChangeDiff

## 14. Provider policy drift is normal

Introduce:

```text
ProviderPolicyChangeDiff
```

## 15. Diff targets

Monitor changes in:

```text
pricing
free-tier definition
credit behavior
payment-method requirement
post-pay behavior
auto-reload behavior
rate limits
model catalog
context limits
tool billing
privacy/data-use terms
commercial/evaluation scope
API protocol
authentication
region support
deprecations
retirement notices
```

## 16. Material policy diff fails closed

A material change causes affected routes to become:

```text
REQUALIFICATION_REQUIRED
```

before the next call.

## 17. Free → paid transition

If an exact route changes from zero price to non-zero price:

```text
immediate quarantine
```

No grace period.

## 18. Trial change

If an ongoing free tier becomes trial-credit-only or payment-method-gated, prior free evidence is superseded.

## 19. Silent provider mutation

If provider documentation did not change but behavior/canaries indicate a material serving change, the route can still be downgraded or quarantined.

---

# Part IV — PriceEpochLease

## 20. Pricing evidence gets a lease

Introduce:

```text
PriceEpochLease
```

## 21. Lease identity

```text
route_cell_id
exact_model_id
exact_feature_set
price_vector
billing_mode
source_hash
issued_at
expires_at
```

## 22. Dispatch requires a valid lease

Immediately before a remote call:

```text
PriceEpochLease.valid == true
```

must hold.

## 23. Short TTL for volatile catalogs

Live promotional gateways with rapidly changing free catalogs use especially short leases.

## 24. Catalog frequency can guide TTL

Example: Kilo's first-party free-model catalog reports live zero-price data and updates every 60 seconds.

For a Kilo free route, pricing proof should therefore be treated as highly dynamic.

## 25. No stale completion after expiry

If a long-running stage crosses a known promotion/entitlement expiry boundary, the controller prepares a safe standby before the boundary.

---

# Part V — ModelNameSemanticsForbidden

## 26. Names are not billing evidence

The following are prohibited inference shortcuts:

```text
"flash" means free
"free" suffix means safe
"mini" means cheap enough
"preview" means free
"open" means free hosted inference
```

## 27. Exact example

Current Z.AI pricing demonstrates why:

```text
GLM-4.7-Flash → currently Free
GLM-4.5-Flash → currently Free
GLM-5.3-Flash → currently paid
```

Therefore suffix semantics are never authoritative.

## 28. Exact live row wins

Eligibility must use the exact current price/plan/account evidence for the exact model ID.

---

# Part VI — BillingModeProof

## 29. Account state is part of the route

Introduce:

```text
BillingModeProof
```

## 30. Required fields

```text
provider
account/workspace
plan
payment_method_linked
pay_as_you_go_enabled
postpay_enabled
auto_reload_enabled
purchased_credit_available
included_credit_remaining
hard_stop_enabled
hard_stop_scope
feature_overage_behavior
proof_source
verified_at
expires_at
```

## 31. Same provider can be safe or unsafe

Example classes:

```text
Cloudflare Workers Free plan
!=
Cloudflare Workers Paid plan
```

and:

```text
SambaNova account without payment method
!=
SambaNova Developer account with payment method
```

## 32. Account proof outranks provider reputation

A provider with a safe free plan can still be ineligible on an account configured for paid overflow.

---

# Part VII — AccountAutomationHazardScanner

## 33. Automatic billing features are hazards

Introduce:

```text
AccountAutomationHazardScanner
```

## 34. Hazards

Detect where available:

```text
auto-reload
auto-top-up
automatic credit purchase
PAYG enabled
post-pay enabled
fallback to paid balance
minimum-balance refill
automatic plan upgrade
provider-managed paid fallback
```

## 35. Hazard rule

If a paid automation path exists and cannot be structurally disabled/proven inactive:

```text
BLOCK_REMOTE_ROUTE
```

## 36. OpenCode Zen special handling

Current OpenCode Zen documentation lists several zero-price models but also documents a broader credit/billing system and auto-reload behavior.

Therefore Zen free models are **not automatically admitted merely because their token row says Free**.

Admission requires proof that:

```text
auto-reload is disabled
paid fallback is impossible for the exact request
exact model row is Free
no paid feature is activated
```

## 37. Positive hard-stop examples

Provider-native protections such as:

```text
Alibaba Free Quota Only
Tencent post-payment disabled
SambaNova Free Tier with no payment method
```

can produce stronger `BillingModeProof` when current account state confirms them.

---

# Part VIII — SpendInvariantProof

## 38. Global proof at startup

Introduce:

```text
SpendInvariantProof
```

At startup and periodically, verify that every enabled remote RouteCell belongs to one of the allowed structural classes.

## 39. Allowed structural classes

Examples:

```text
ZERO_PRICE_MODEL
HARD_STOP_FREE_QUOTA
NO_PAYMENT_METHOD_FREE_TIER
FREE_MODE_PAYG_DISABLED
LOCAL_NO_API_BILLING
```

## 40. Proof failure

If global proof fails:

```text
remote route disabled
→ local route remains available
→ provider requalification scheduled
```

## 41. No monetary tolerance

The acceptable paid amount is not “very small”.

It is:

```text
0.00 EUR autonomous
```

---

# Part IX — ProviderAuthOnboardingBoundary

## 42. Autonomous connection begins after legitimate authorization

AlinaCoder may automatically use a provider once valid credentials/account authorization have been legitimately supplied and stored.

## 43. It must not autonomously create identities

It must never automatically:

```text
create new provider accounts
solve CAPTCHAs
bypass phone verification
fabricate KYC
link a payment method
create extra identities for quotas
circumvent geographic restrictions
```

## 44. Missing credential behavior

When a highly valuable route lacks authorization:

```text
mark AUTH_REQUIRED
preserve candidate score
continue with best available eligible route
surface compact one-time setup action to user when useful
```

## 45. No blocking of current task when alternatives exist

Missing one provider credential does not stop the task if another eligible route exists.

---

# Part X — CredentialHandle architecture

## 46. Credentials never enter task memory

Canonical state stores only:

```text
CredentialHandle
```

not raw keys.

## 47. Windows-first secret storage

Preferred local credential storage uses an OS-backed secure mechanism such as:

```text
Windows Credential Manager / DPAPI-backed storage
```

or another equivalent audited secret store.

## 48. Secret redaction

Provider keys must never appear in:

```text
prompts
Git commits
logs
routing memory
benchmarks
Supabase public tables
crash reports
```

## 49. Optional Supabase Vault

If optional cloud synchronization is explicitly enabled, Supabase Vault may store encrypted secret material for cloud workers.

It is not required for local operation.

## 50. Local-first remains canonical

Cloud secret storage never becomes a dependency for starting `alinacoder.exe` locally.

---

# Part XI — QuotaHeaderNormalizer

## 51. Runtime quota telemetry must be normalized

Introduce:

```text
QuotaHeaderNormalizer
```

## 52. Normalized fields

```text
remaining_requests_minute
remaining_requests_day
remaining_tokens_minute
remaining_tokens_day
remaining_audio_or_other_units
reset_requests_at
reset_tokens_at
retry_after
observed_at
source_route
```

## 53. Provider adapters

Native headers from providers such as Groq and SambaNova are translated into this common structure.

## 54. Headers outrank stale local counters

Provider-supplied remaining quota is authoritative for the provider's own live bucket when trustworthy.

## 55. Local counters still matter

Track local usage to detect:

```text
header inconsistencies
shared-account usage by another client
unexpected quota loss
provider accounting drift
```

---

# Part XII — ExhaustionForecast

## 56. Remaining quota is not enough

Introduce:

```text
ExhaustionForecast
```

## 57. Forecast inputs

```text
current remaining quota
observed task token velocity
expected stage horizon
expected context growth
retry probability
handoff cost
verification reserve
reset time
expiry time
```

## 58. Preemptive safe switch

If current route is likely to exhaust mid-stage:

```text
switch at next safe checkpoint before exhaustion
```

rather than waiting for a hard 429/403.

## 59. Preserve recovery reserve

Never consume the last viable remote capacity without a recovery plan when a long mutation stage is in progress.

---

# Part XIII — EndOfAvailabilityForecast

## 60. Availability has future boundaries

Introduce:

```text
EndOfAvailabilityForecast
```

Track:

```text
promotion end
trial expiry
quota expiry
announced EOL
deprecation date
provider retirement date
model snapshot replacement
```

## 61. Long-task rule

A route predicted to expire before the current long-running stage completes may still be used only if:

```text
standby exists
continuity package is ready
safe handoff boundary exists
```

## 62. Explicit campaign dates

Provider campaigns with published end dates are never modeled as permanent free capacity.

---

# Part XIV — ProviderCapabilityFeed

## 63. Dynamic provider adapters

The live marketplace should support direct adapters for current high-value zero-cost candidates and discovery sources.

## 64. Direct-provider priority

Prefer direct first-party provider APIs when they offer equivalent zero-cost access and better identity/billing transparency.

## 65. Aggregators remain valuable

Aggregators can add:

```text
broader model discovery
simpler protocol
failover
benchmarking
```

but they add another hidden-routing and billing layer that must be governed.

---

# Part XV — Current zero-cost provider atlas policy

## 66. Research-time snapshot is not runtime truth

The provider examples below reflect official documentation checked on 2026-09-04.

Every runtime use must still pass live requalification.

## 67. Kilo Gateway — high-priority live free catalog

Current first-party Kilo documentation reports a live free-model catalog derived from hosted pricing, with zero input and output pricing and no credit card required for free hosted models.

Current examples include:

```text
MiniMax M3 (free)
Ling-3.0-flash (free)
Laguna S 2.1 (free)
Hy3 (free)
Nex-N2-Pro (free)
Nemotron 3 Ultra (free)
Ring-2.6-1T (free)
Ling-2.6-1T (free)
Hy3 preview (free)
Ling-2.6-flash (free)
Gemma 4 26B A4B (free)
Nemotron 3 Super (free)
```

Current catalog count and members are explicitly dynamic.

## 68. Kilo capability advantage

Current Kilo Gateway documentation exposes:

```text
OpenAI-compatible chat API
/models
/providers
pricing metadata
context metadata
tool calling
structured output
```

and `/models` and `/providers` can be queried without authentication.

## 69. CredentiallessRegistryProbe

Introduce:

```text
CredentiallessRegistryProbe
```

When a provider exposes unauthenticated catalog metadata, use it for low-cost discovery before credentialed inference.

## 70. Kilo admission rule

A Kilo route requires:

```text
current exact model price == 0 input && 0 output
valid Kilo account/key for inference
no paid fallback
no unsafe extra feature
fresh PriceEpochLease
```

## 71. Kilo promotions are ephemeral

Kilo explicitly notes that free hosted promotions can end.

Therefore Kilo routes use aggressive freshness checks.

## 72. Z.AI — exact zero-price direct models

Current first-party Z.AI pricing lists:

```text
GLM-4.7-Flash → Free
GLM-4.5-Flash → Free
GLM-4.6V-Flash → Free
```

## 73. Z.AI feature billing

Current Z.AI built-in Web Search is separately priced.

Therefore:

```text
free inference + provider web search
!= free request
```

Paid built-in tools must be disabled unless replaced by another eligible zero-cost mechanism.

## 74. SambaNova Cloud — structural free plan

Current first-party SambaNova documentation states:

```text
Free Tier applies when no payment method is linked
```

with current free-tier model-specific rate limits and response quota headers.

## 75. SambaNova current examples

Current production/preview free-tier examples include:

```text
DeepSeek-V3.1
gpt-oss-120b
Meta-Llama-3.3-70B-Instruct
DeepSeek-V3.2 preview
gemma-4-31B-it preview
```

with current documented free limits around:

```text
20 RPM
20 RPD
200,000 TPD
```

for listed routes.

Live account limits remain authoritative.

## 76. SambaNova safe class

If and only if:

```text
plan == Free Tier
payment_method_linked == false
```

classify as:

```text
NO_PAYMENT_METHOD_FREE_TIER
```

## 77. Groq — recurring free quota candidate

Current Groq first-party rate-limit documentation exposes Free Plan quotas per model and live remaining/reset headers.

Current examples include:

```text
gpt-oss-120b
qwen3.6-27b
qwen3.8-27b
groq/compound
groq/compound-mini
```

## 78. Groq pool semantics

Groq limits are organization-level.

Multiple API keys in the same organization are not independent free pools.

## 79. Cloudflare Workers AI — plan-dependent safety

Current Cloudflare documentation states:

```text
Workers Free → 10,000 Neurons/day, no paid overage on Free plan
Workers Paid → 10,000 free Neurons/day then paid usage
```

## 80. Cloudflare route class

```text
Workers Free plan
→ potentially HARD_SAFE_FREE_PLAN

Workers Paid plan
→ SOFT_FREE_QUOTA_PAID_OVERFLOW unless stronger hard cap proven
```

## 81. Cloudflare quota unit

The `ResourceShadowPriceController` must understand Neurons as a provider-specific capacity unit rather than pretending everything is tokens.

## 82. OpenRouter — strict `:free` handling

Current OpenRouter documentation exposes explicit free-model routing and free-model rate limits.

## 83. OpenRouter paid boundary

Only exact zero-price/free route IDs may be used.

Positive account credits or prior credit purchase must never make paid routes eligible.

## 84. OpenRouter fallback closure

Provider-side fallback must be constrained so that no fallback can move the request onto a paid route.

If that cannot be proven:

```text
disable provider-side fallback
→ let AlinaCoder fail over itself
```

## 85. Google Gemini API Free Tier

Current Google documentation states new accounts begin on the Gemini API Free Tier, with access to certain models under free-tier limits, and billing linkage/prepay is required to move into paid usage.

## 86. Gemini account-class rule

A genuinely unlinked Free Tier project can be considered a candidate zero-cost route after privacy/use-scope checks.

If billing is linked, account-level spend-cap delay must not be relied on as the only zero-spend guard.

## 87. Gemini privacy projection

Data-use rules differ by tier/region.

ProviderSafeContextProjection must apply the current account/region terms before transmitting code or user context.

## 88. Mistral Free mode

Current Mistral documentation states Free mode is enabled by default with usage/rate limits.

It also documents:

```text
pay-as-you-go off → usage can stop when included usage is exhausted
pay-as-you-go on → additional usage may be billed
```

## 89. Mistral safe class

Mistral may enter:

```text
FREE_MODE_PAYG_DISABLED
```

only after current account state proves PAYG is off.

## 90. Hugging Face Inference Providers

Current Hugging Face documentation provides small monthly free credits to free users and supports many inference providers behind one API.

It is primarily:

```text
TRIAL_OR_INCLUDED_CREDIT_ROUTER
```

not automatically an unrestricted zero-price provider.

## 91. Hugging Face extra usage

Because extra inference may require purchased credits/pay-as-you-go depending on account state, exact account billing behavior must be proven before use.

## 92. Tencent TokenHub / Hunyuan

Current official Tencent materials describe free experience quotas for models and state that when post-payment is not enabled, service stops when the free quota is exhausted.

## 93. Tencent hard-stop class

If current account state proves:

```text
postpayment_enabled == false
free_entitlement_remaining > reserve
```

then a route can enter:

```text
HARD_STOP_FREE_QUOTA
```

## 94. Tencent model campaigns are time-bounded

Current promotions and eligible model lists must be tracked with explicit expiry/campaign metadata.

## 95. Alibaba Model Studio

The prior amendment remains authoritative for Alibaba Singapore `Free Quota Only` handling.

This amendment unifies Alibaba under `BillingModeProof`, `PriceEpochLease`, `ExhaustionForecast` and `AccountAutomationHazardScanner`.

## 96. SiliconFlow

The prior amendment remains authoritative: only exact live zero-price routes may be admitted.

## 97. Scaleway

The prior amendment remains authoritative: a free allowance that automatically rolls into paid billing is blocked unless an independent hard zero-spend control is proven.

## 98. Ollama local

Local Ollama remains a foundational zero-API-billing fallback.

Local electricity/hardware cost is a machine resource concern, not remote metered API spend.

## 99. Ollama Cloud

Current Ollama Cloud Free plan includes starter usage but may coexist with extra purchased credits.

It is eligible only if exact account behavior proves included free usage cannot silently consume purchased/paid capacity.

## 100. NVIDIA NIM

Hosted NVIDIA trial/evaluation routes must honor current use-scope terms.

Evaluation-only access cannot be treated as unrestricted production capacity.

## 101. Cerebras

Previously free Cerebras assumptions must be continuously rechecked.

If current access requires a payment method and temporary trial credit, classify as trial/payment-gated rather than standing free capacity.

## 102. OpenCode Zen

Current zero-priced models are useful discovery candidates, particularly free Nemotron/Ling/MiMo-style routes.

But billing/autoreload hazards make account-state proof mandatory before autonomous use.

## 103. No provider ranking from this list alone

The atlas says who may deserve a live probe.

It does not declare one permanent champion.

---

# Part XVI — ZeroCostFallbackClosure

## 104. Hidden fallback can violate zero-spend

Introduce:

```text
ZeroCostFallbackClosure
```

## 105. Closure definition

For any provider-side router/aggregator fallback set `F`:

```text
forall route in F:
  price == 0
  && billing_mode is safe
  && privacy/use-scope allowed
  && capability >= minimum
```

must hold.

## 106. Unknown fallback set is unsafe

If the gateway cannot reveal or constrain its fallback set:

```text
provider-managed failover disabled
```

## 107. AlinaCoder-owned failover preferred

When closure cannot be proven, AlinaCoder performs its own explicit next-route selection.

---

# Part XVII — NestedRouterTransparency

## 108. Aggregator route identity can be nested

Introduce:

```text
NestedRouterTransparency
```

## 109. Nested identity

Where observable:

```text
aggregator
requested_model
actual_backend_provider
actual_model_revision
serving_tier
```

## 110. Backend change affects evidence

If the aggregator silently switches backend provider or serving configuration, old performance evidence receives reduced confidence.

## 111. Hidden identity penalty

A route with opaque backend identity receives a `TransparencyRisk` penalty and may be unsuitable for critical tasks.

## 112. No false independence

Two aggregator routes that ultimately use the same backend/model are not independent failure domains.

---

# Part XVIII — SemanticHealthCell

## 113. HTTP health is insufficient

A route can return HTTP 200 while silently corrupting the task.

Introduce:

```text
SemanticHealthCell
```

## 114. Health dimensions

```text
transport
streaming protocol
schema/tool-call integrity
conversation-state integrity
instruction retention
model identity
output completeness
quality canary
```

## 115. States

```text
HEALTHY
SUSPECT
DEGRADED
EJECTED
HALF_OPEN
```

## 116. Silent-200 incidents

Examples include:

```text
missing conversation turn
truncated tool arguments
stream index collision
wrong model variant
format drift
garbage/refusal under 200 OK
```

## 117. Semantic canaries

Background canaries can test a small fixed suite for:

```text
JSON/schema adherence
simple deterministic reasoning
constraint retention
tool-call shape
conversation continuity
```

## 118. Canary cost gate

Canaries consume only legitimate zero-cost capacity and obey resource reserves.

## 119. Half-open recovery

An ejected provider is not restored on one successful ping.

Recovery requires bounded semantic canaries and real health evidence.

---

# Part XIX — ProviderCircuitBreaker

## 120. Circuit-breaker state

Introduce:

```text
ProviderCircuitBreaker
```

with:

```text
CLOSED
OPEN
HALF_OPEN
```

## 121. Inputs

```text
5xx
429
timeouts
stream stalls
semantic canary failure
schema corruption
continuity failure
billing-safety failure
```

## 122. Hysteresis

Use consecutive evidence, dwell time and cooldown to prevent flapping.

## 123. Jittered retry

Retries use exponential backoff plus jitter.

Fixed synchronized retry intervals are prohibited.

## 124. Global retry budget

Retries across providers are bounded per task/stage to avoid retry storms and quota destruction.

---

# Part XX — HedgedInferencePolicy

## 125. Hedging is exceptional

Hedged requests may reduce tail latency but duplicate quota consumption.

## 126. Eligibility

Hedging is allowed only when:

```text
both routes are zero-cost eligible
quota reserve is sufficient
request is side-effect-free
no duplicate external tool mutation occurs
expected latency benefit justifies duplicate quota
```

## 127. First-valid-semantic-response wins

The winner is not merely first bytes.

It must pass minimal response/protocol integrity checks.

## 128. Loser cancellation

Cancel loser promptly where provider semantics support safe cancellation.

---

# Part XXI — ProviderAvailabilitySLOMemory

## 129. Availability evidence is route-specific

Track:

```text
p50 latency
p95 latency
p99 latency
TTFT
stream stall rate
429 rate
5xx rate
timeout rate
schema failure rate
semantic canary pass rate
continuity pass rate
recovery time
```

## 130. Quality cannot be traded away for speed

A very fast weak route cannot outrank a much more capable route solely because of latency.

## 131. Quality floor first

Candidate selection first enforces a task-relative capability/quality floor.

Only then may latency/service capacity differentiate eligible peers.

---

# Part XXII — EligibleParetoFrontier

## 132. “Most powerful” is task-relative

The largest parameter count or highest public benchmark is not always the most effective route for the current coding operation.

Introduce:

```text
EligibleParetoFrontier
```

## 133. Hard gates happen before Pareto selection

First require:

```text
zero-spend proof
privacy/use scope
protocol compatibility
semantic health
minimum capability
context capacity
continuity compatibility
quota reserve
```

## 134. Pareto axes

Among eligible routes compare:

```text
verified terminal success lower bound
coding/debugging specialization
latency/service capacity
quota consumption
handoff risk
context fit
privacy/data-use quality
provider reliability
```

## 135. Dominated routes are removed

A route strictly worse on all relevant axes need not consume production traffic.

## 136. Public benchmark is a prior

Public benchmarks seed expectations but cannot dominate verified AlinaCoder task evidence.

---

# Part XXIII — QualityFloorController

## 137. Explicit capability floor

Introduce:

```text
QualityFloorController
```

## 138. Task-relative floor

Examples:

```text
simple extraction → modest floor
routine patch → coding/tool floor
architecture → high reasoning floor
security-sensitive change → high reasoning + verifier floor
```

## 139. No weak free route merely to conserve quota

If a weaker free route falls below task floor, it is not eligible even if abundant.

## 140. Local fallback can decompose

When no single free model meets the floor, AlinaCoder may decompose, add verification, or use specialist collaboration rather than silently lowering the correctness requirement.

---

# Part XXIV — BindingGranularityPolicy

## 141. Avoid both churn and over-pinning

Introduce:

```text
BindingGranularityPolicy
```

## 142. Binding levels

```text
TASK
STAGE
OPERATION
REQUEST
```

## 143. TASK binding

Prefer when:

```text
handoff tax high
route clearly dominant
long coherent reasoning trajectory
quota sufficient
```

## 144. STAGE binding

Prefer when different models dominate architecture, implementation and verification.

## 145. OPERATION binding

Prefer for highly compositional workflows with cheap canonical-state handoff.

## 146. REQUEST binding

Use mainly for stateless/low-context utility work.

## 147. Binding decision variables

```text
handoff cost
model complementarity
stage heterogeneity
context size
quota forecast
continuity confidence
route stability
```

## 148. Route churn metric

Track:

```text
unnecessary_switch_rate
```

and reject policies that increase churn without terminal benefit.

---

# Part XXV — RouterPolicyPortfolio

## 149. No router family dominates all conditions

Introduce a small certified portfolio:

```text
STATIC_CHAMPION
PROFILE_MATCHER
EXECUTION_MEMORY_BANDIT
OOD_CONSERVATIVE
PARETO_SELECTOR
```

## 150. RouterPolicyPortfolio

```text
RouterPolicyPortfolio
```

selects a routing policy for the current support/drift regime.

## 151. Avoid recursive meta-routing explosion

The policy portfolio is small, deterministic to inspect, and bounded.

## 152. Baseline always remains

`STATIC_CHAMPION` or equivalent simple baseline must remain available.

## 153. Policy promotion still requires RouterGainCertificate

No meta-policy bypasses the existing router certification requirement.

---

# Part XXVI — Drift/change-point control

## 154. Model quality can regress silently

Introduce:

```text
RouteDriftDetector
```

## 155. Drift signals

```text
recent vs historical verified success
canary score
schema adherence
latency distribution
provider identity changes
context/tool behavior changes
```

## 156. Per-route adaptive memory horizon

Fast-drifting routes should discount old evidence faster than stable local routes.

## 157. Abrupt-change trigger

A statistically/materially abrupt drop can immediately shrink the evidence window and move route to `SUSPECT`.

## 158. Shadow-audit stream

A small bounded fraction of eligible zero-cost quota may audit alternate routes to detect frontier changes without routing every task to every model.

---

# Part XXVII — SafeExplorationEnvelope

## 159. New routes explore safely

Introduce:

```text
SafeExplorationEnvelope
```

## 160. Initial exploration order

```text
synthetic fixtures
read-only repo analysis
noncanonical shadow tasks
isolated candidate patches
verified low-risk tasks
then broader eligibility
```

## 161. No immediate canonical mutation

An unseen provider/model does not receive direct high-impact mutation authority merely because public benchmarks are excellent.

## 162. ChallengerCanaryBudget

Each new route receives a bounded free-quota exploration budget.

## 163. Stop conditions

Stop exploration on:

```text
billing uncertainty
privacy conflict
semantic corruption
repeated schema failure
clear capability domination
provider instability
```

---

# Part XXVIII — JointRuntimeStatePromotion

## 164. Self-improvements interact

Router, skill memory, verifier thresholds, context policy and optional local adapter form one runtime system.

Introduce:

```text
JointRuntimeState
```

## 165. Bundle identity

```text
router_policy_fingerprint
skillbook_fingerprint
local_adapter_fingerprint
verifier_policy_fingerprint
context_policy_fingerprint
provider_atlas_version
```

## 166. Promotion is joint

A candidate improvement must be replayed/evaluated as the **whole bundle actually deployed**.

## 167. Component-local wins are insufficient

Example:

```text
new router + old verifier = better
```

but:

```text
new router + new verifier = regression
```

means the combined runtime cannot be promoted.

## 168. BestKnownJointRuntimeState

Retain:

```text
BestKnownJointRuntimeState
```

for atomic rollback.

## 169. Experience-to-skill adaptation

Execution-verified lessons from failed routes may become reusable skills only after replay and anti-overfitting checks.

---

# Part XXIX — ContextTransmissionBudget

## 170. Handoff itself consumes free quota

Introduce:

```text
ContextTransmissionBudget
```

## 171. Measure portable context footprint

Before switching remote models estimate:

```text
canonical exact state tokens
compressed evidence tokens
raw observations required
repo excerpts required
verification context
```

## 172. Handoff-aware route choice

A route with 5k tokens left cannot safely take over a stage needing 20k tokens of required context even if its nominal model quality is higher.

## 173. Compression cannot violate TaskRelativeSufficientState

Quota pressure never permits dropping MUST_EXACT state.

---

# Part XXX — ProtocolAdapterCapabilityMatrix

## 174. Protocol differences must be explicit

Introduce:

```text
ProtocolAdapterCapabilityMatrix
```

## 175. Protocols

Examples:

```text
OpenAI Chat Completions
OpenAI Responses
Anthropic Messages
Gemini native
provider-native proprietary
local Ollama
```

## 176. Capability fields

```text
streaming
tool calls
parallel tool calls
structured output
reasoning controls
vision/files
usage reporting
finish reasons
cancellation
idempotency
```

## 177. Compatibility is empirical

“OpenAI-compatible” is not enough.

Run protocol canaries for exact behavior.

## 178. Tool-call normalization

Provider-specific tool IDs, orphan messages and finish reasons must be normalized without losing semantics.

---

# Part XXXI — ModelIdentityAttestation

## 179. Requested model may differ from served reality

Introduce:

```text
ModelIdentityAttestation
```

## 180. Evidence sources

```text
response model field
provider metadata
version headers
catalog fingerprint
behavioral canary fingerprint
```

## 181. Identity confidence

States:

```text
ATTESTED
LIKELY
OPAQUE
MISMATCH
```

## 182. Mismatch action

`MISMATCH` invalidates inherited route evidence and can quarantine the route.

---

# Part XXXII — Canonical failover transaction v4

## 183. Failover is a transaction

A provider/model switch must follow:

```text
DETECT
→ FREEZE OUTPUT/MUTATION BOUNDARY
→ SNAPSHOT CANONICAL STATE
→ SANITIZE TRAJECTORY
→ SELECT ELIGIBLE PARETO CANDIDATES
→ PROVE BILLING MODE + PRICE EPOCH
→ PROVE QUOTA/END-OF-AVAILABILITY
→ PREFLIGHT PROTOCOL + SEMANTIC HEALTH
→ BUILD HANDOFF PACKAGE
→ RESTORE BARRIER
→ CONTINUITY PROBE
→ SESSION CAS
→ COMMIT ROUTE LEASE
→ RESUME
```

## 184. Failed takeover

If continuity proof fails:

```text
new route not committed
→ previous valid route remains canonical if still healthy
→ otherwise try next eligible standby
```

## 185. No mixed-model partial response

A user-visible semantic response must not splice arbitrary partial text from two models unless a deterministic composition mechanism explicitly owns the merge.

## 186. Tool call boundary

Never switch inside an uncommitted tool mutation transaction.

---

# Part XXXIII — WarmStandbyPool

## 187. Standby improves seamless failover

Introduce:

```text
WarmStandbyPool
```

## 188. Standby qualification

For important long-running work maintain at least one alternate route with:

```text
valid auth
fresh billing proof
fresh price lease
sufficient quota
protocol canary pass
continuity codec compatibility
```

## 189. Standby does not consume inference unnecessarily

Warm means metadata/auth/protocol readiness, not constant token-consuming generation.

## 190. Failure-domain diversity

Prefer standby from a different provider/failure domain when quality is adequate.

---

# Part XXXIV — Provider route health under 429 and quota reset

## 191. Quota exhaustion is not provider failure

A 429 caused by expected free quota depletion should not lower model semantic quality score.

## 192. Rate-state classification

```text
TEMPORARY_RATE_LIMIT
DAILY_QUOTA_EXHAUSTED
TOKEN_QUOTA_EXHAUSTED
ACCOUNT_LIMIT
PROVIDER_OVERLOAD
UNKNOWN_429
```

## 193. Reset-aware scheduling

If reset occurs soon and task permits, route may be parked until reset.

Otherwise use standby.

## 194. Never upgrade automatically

An upgrade suggestion from provider response/UI is not an allowed recovery action.

---

# Part XXXV — Privacy and contributor-free models

## 195. Free may be paid with data

Some providers offer zero monetary price in exchange for broader training/data-use permissions.

Introduce:

```text
DataUseCostClass
```

## 196. Data-use classes

```text
NO_TRAINING_BY_DEFAULT
OPT_OUT_AVAILABLE_AND_VERIFIED
TRAINING_PERMITTED
CONTRIBUTOR_FREE_TRAINING_EXCHANGE
UNKNOWN
```

## 197. Sensitive project restriction

Routes whose terms allow training on prompts/outputs may be blocked for sensitive/private code even when monetary price is zero.

## 198. Data use is not silently accepted

A zero-price route cannot bypass privacy simply because it is powerful.

---

# Part XXXVI — Current provider-specific operational rules

## 199. Kilo

Priority:

```text
HIGH discovery value
HIGH free-catalog value
SHORT pricing TTL
```

Use exact live zero-price route IDs.

## 200. Z.AI

Priority:

```text
HIGH for exact zero-price GLM Flash routes
```

Disable separately paid tools unless a free replacement is selected.

## 201. SambaNova

Priority:

```text
HIGH as structurally safe no-payment-method free tier
```

but low RPD means preserve quota for high-value calls.

## 202. Groq

Priority:

```text
HIGH for fast free inference and live quota headers
```

but free availability is model/account-limit dependent.

## 203. Cloudflare Workers AI

Priority:

```text
MEDIUM/HIGH on Workers Free
```

shared Neuron budget requires careful allocation.

## 204. OpenRouter

Priority:

```text
HIGH discovery/coverage
MEDIUM direct execution risk due nested routing
```

Use strict free-only closure.

## 205. Gemini Free Tier

Priority:

```text
HIGH when current free-tier models provide strong capability
```

subject to account billing and data-use proof.

## 206. Mistral Free mode

Priority:

```text
HIGH for coding-oriented Mistral/Codestral capability when Free mode + PAYG disabled is live
```

## 207. Tencent TokenHub/Hunyuan

Priority:

```text
HIGH for time-limited hard-stop free entitlement when post-pay disabled
```

Campaign expiry must be tracked.

## 208. Hugging Face Inference Providers

Priority:

```text
HIGH discovery breadth
LOWER autonomous execution priority unless credit-overflow safety is proven
```

## 209. NVIDIA NIM

Priority:

```text
EVALUATION_ONLY unless current terms allow target use
```

## 210. OpenCode Zen

Priority:

```text
GOOD free-model discovery
EXECUTION BLOCKED until autoreload/paid-path proof is safe
```

## 211. GitHub Models

```text
TOMBSTONED RETIRED
```

## 212. Future providers

A provider not named here may still be admitted by the generic qualification protocol.

The architecture must never require a code release just to recognize a new OpenAI-compatible zero-price endpoint.

---

# Part XXXVII — Discovery-source hierarchy

## 213. Evidence authority levels

```text
L0 account live state / provider API response
L1 official provider pricing/docs/changelog
L2 official provider model catalog
L3 reputable research / benchmark
L4 maintained community directory
L5 unverified community claim
```

## 214. Billing decisions require L0/L1

L3-L5 can discover candidates but cannot alone authorize spending/billing safety.

## 215. Contradiction resolution

Higher authority and fresher exact-scope evidence wins.

## 216. Community directories remain useful

Daily free-model indexes increase recall and can trigger official-source verification jobs.

---

# Part XXXVIII — Provider discovery worker

## 217. Autonomous recurring discovery

`FrontierReleaseRadar` is extended with a periodic:

```text
ProviderDiscoveryWorker
```

## 218. Inputs

```text
official /models
official pricing endpoints/pages
official changelogs
official deprecation notices
provider account quota endpoints
trusted community lead feeds
research leaderboards as capability priors
```

## 219. Diff-first scanning

Prefer content/hash diffs over reprocessing entire documentation each cycle.

## 220. New lead pipeline

```text
LEAD
→ OFFICIAL_VERIFY
→ BILLING_VERIFY
→ AUTH/ACCOUNT_VERIFY
→ PROTOCOL_CANARY
→ BEHAVIOR_PROFILE
→ SAFE_EXPLORATION
→ ROUTE_ELIGIBLE
```

## 221. Removal pipeline

```text
PRICE/TERMS/EOL CHANGE
→ FREEZE
→ REQUALIFY
→ RESTORE or TOMBSTONE
```

---

# Part XXXIX — Optional Supabase orchestration refinements

## 222. Supabase remains optional

Local SQLite/event log remains sufficient and canonical for a single local machine.

## 223. Durable provider-recheck queue

When Supabase sync is enabled, `pgmq` may hold jobs such as:

```text
provider_recheck
catalog_diff
semantic_canary
quota_refresh
model_profile_probe
```

## 224. Visibility timeout

A worker crash leaves the job retriable after visibility timeout rather than losing it.

## 225. Idempotency

Every job includes:

```text
job_id
provider_id
route_cell_id
expected_source_hash
expected_policy_epoch
```

so retry cannot apply stale evidence twice.

## 226. Queue archival

Completed/failed probes may be archived for audit and replay analysis.

## 227. pg_cron

Optional scheduled provider discovery may use `pg_cron` + `pg_net`/Edge Functions.

## 228. Vault

Supabase documentation recommends Vault for secret material used by scheduled functions.

Only optional cloud-worker credentials may use this path.

## 229. Realtime is notification, not truth

Realtime Broadcast/Replay can notify clients that a provider changed or a route was quarantined.

Durable state remains in local state/database/queue.

## 230. Managed realtime schema restriction

Do not create/alter/drop arbitrary objects in Supabase's managed `realtime` schema.

## 231. Changelog migration awareness

Supabase breaking changes, including Management API logging endpoint changes, must be treated through the same policy-diff mechanism when optional integrations depend on them.

---

# Part XL — Router robustness under paraphrase

## 232. Equivalent user intent should not randomly flip providers

Routing metamorphic tests extend to provider selection.

## 233. RoutePickStability

Measure whether semantically equivalent French/noisy paraphrases produce unjustified route changes.

## 234. Margin tie-break

When top candidate estimates are statistically indistinguishable, prefer:

```text
current healthy route
or historically more robust route
```

rather than switching for a tiny score difference.

## 235. Stability is subordinate to real capability gain

Do not remain pinned to a weaker route when evidence of a meaningful stronger route is clear.

---

# Part XLI — Terminal-outcome learning with delayed feedback

## 236. Route reward can arrive later

Coding success may not be known until tests/build/review complete.

## 237. DelayedRewardLedger

Introduce:

```text
DelayedRewardLedger
```

linking:

```text
routing_decision_id
→ later Done Contract evidence
```

## 238. No premature positive reward

A fluent patch proposal is not a success until relevant verification completes.

## 239. Failed handoff attribution

Separate whether failure came from:

```text
model reasoning
provider transport
handoff loss
stale context
quota interruption
verifier bug
```

before updating model quality posterior.

---

# Part XLII — Quality-adaptive canary scheduling

## 240. Stable routes need fewer probes

Canary frequency can decay for routes with long stable history.

## 241. Drift triggers denser probes

Increase probe cadence after:

```text
model revision
provider migration
pricing change
latency shift
unexpected task failure
terms change
```

## 242. Probe budget never starves user work

Canary traffic has lower priority than active task recovery reserve.

---

# Part XLIII — Provider configuration fingerprint

## 243. Model name alone is insufficient

Introduce:

```text
ServingConfigurationFingerprint
```

## 244. Fingerprint fields where observable

```text
model revision
quantization
reasoning mode
context policy
tool mode
provider/backend
region
serving tier
```

## 245. Configuration change causes evidence decay

Old success data becomes a prior, not direct current truth.

---

# Part XLIV — Capability-specific champions

## 246. Maintain multiple champion tables

Examples:

```text
architecture_champion
debugging_champion
patch_generation_champion
test_generation_champion
code_review_champion
noisy_french_champion
long_context_champion
vision_champion
fast_utility_champion
```

## 247. Global champion is optional

There need not be one universal best model.

## 248. Stage router uses champion table as prior

Then live task evidence/Pareto filtering selects the route.

---

# Part XLV — Frontier route benchmarking policy

## 249. Benchmarks are repeated

For stochastic models, repeat compact benchmark items when quota permits.

## 250. Measure dispersion

Store:

```text
median
worst case
dispersion
schema failure
latency
quota cost
```

## 251. Include real interaction forms

Benchmark prompts include:

```text
clean English
ordinary French
noisy French
ASR-like corrections
short casual coding asks
long repo context
mid-task handoff
```

## 252. Provider configuration is benchmarked with model

Benchmark result belongs to the exact RouteCell, not abstract model brand.

---

# Part XLVI — New failure taxonomy

## 253. Add failure reasons

```text
PROVIDER_RETIRED
PROVIDER_PRICE_CHANGED
PROVIDER_TERMS_CHANGED
PROVIDER_AUTH_CHANGED
PRICE_EPOCH_EXPIRED
BILLING_MODE_UNPROVEN
AUTO_RELOAD_HAZARD
POSTPAY_HAZARD
PAYG_HAZARD
PAID_FALLBACK_NOT_CLOSED
NESTED_BACKEND_OPAQUE
NESTED_BACKEND_CHANGED
MODEL_IDENTITY_MISMATCH
SEMANTIC_200_FAILURE
STREAM_CORRUPTION
TOOL_CALL_CORRUPTION
CONVERSATION_STATE_CORRUPTION
PROVIDER_CIRCUIT_OPEN
ROUTE_QUOTA_FORECAST_EXHAUSTION
PROMOTION_EXPIRY_RISK
END_OF_AVAILABILITY_RISK
DATA_USE_SCOPE_UNSAFE
PROVIDER_CAMPAIGN_EXPIRED
ROUTER_PICK_INSTABILITY
```

## 254. Billing failures are terminal for that route attempt

Do not retry a billing-unsafe route hoping it becomes free.

## 255. Semantic corruption invalidates response

A semantically corrupted HTTP-200 response cannot update canonical state.

---

# Part XLVII — Acceptance scenarios: provider lifecycle

## 256. Retired provider

1. Community directory still lists GitHub Models.
2. Official GitHub evidence says retired.
3. Tombstone wins.
4. No inference attempt occurs.

## 257. Free-to-paid change

1. Route was free yesterday.
2. Live catalog now reports paid output tokens.
3. PriceEpochLease invalidates.
4. Route quarantines before dispatch.
5. Standby takes over.

## 258. Name trap

1. New model ID ends in `-Flash`.
2. Pricing row is non-zero.
3. Route remains paid/ineligible.

## 259. Promotion expiry

1. Kilo route is currently zero price.
2. Exact free promotion disappears.
3. Catalog diff triggers requalification.
4. No stale “free” cache remains active.

---

# Part XLVIII — Acceptance scenarios: account billing safety

## 260. SambaNova

1. No payment method linked.
2. Account is Free Tier.
3. Exact model has Free Tier quota.
4. Route may be eligible.

## 261. SambaNova upgrade hazard

1. Payment method later linked.
2. BillingModeProof changes.
3. Route immediately requalifies before further autonomous use.

## 262. Cloudflare Free

1. Workers Free plan.
2. Under 10,000 Neurons/day.
3. No paid overage path.
4. Candidate eligible.

## 263. Cloudflare Paid

1. Workers Paid plan.
2. Same first 10k free allowance.
3. Overage can bill.
4. Route blocked absent stronger hard cap.

## 264. Mistral

1. Free mode active.
2. PAYG disabled.
3. Included usage ends.
4. Service stops rather than charging.
5. Failover occurs.

## 265. Tencent

1. Free quota remaining.
2. Post-payment disabled.
3. Quota exhausts.
4. Provider stops service.
5. AlinaCoder switches without charge.

## 266. OpenCode Zen

1. Nemotron free row exists.
2. Auto-reload is enabled or cannot be verified off.
3. Route is blocked despite zero token price.

---

# Part XLIX — Acceptance scenarios: nested routing

## 267. Aggregator fallback

1. Requested free model is unavailable.
2. Aggregator wants to fall back.
3. Fallback set includes a paid route.
4. ZeroCostFallbackClosure fails.
5. Provider-side fallback disabled/rejected.

## 268. Backend identity changed

1. Same aggregator/model ID.
2. Response metadata indicates new backend provider.
3. Old route evidence decays.
4. Semantic canary runs.
5. New backend gets its own RouteCell evidence.

## 269. Opaque backend

1. Aggregator cannot reveal actual backend.
2. Route remains usable only for risk classes compatible with opacity.
3. Critical work prefers attested direct route when available.

---

# Part L — Acceptance scenarios: continuity and health

## 270. Silent HTTP 200

1. Provider returns 200.
2. Tool-call arguments are malformed/truncated.
3. SemanticHealthCell detects protocol corruption.
4. Response is not committed.
5. Provider circuit degrades/ejects.
6. Standby rehydrates canonical state.

## 271. Conversation loss

1. Provider drops an earlier constraint.
2. Continuity canary fails.
3. Route cannot commit mutation.
4. New route receives MUST_EXACT canonical state.

## 272. Rate exhaustion

1. Groq headers show daily free quota nearing reserve floor.
2. ExhaustionForecast predicts mid-stage failure.
3. Switch occurs at next safe checkpoint.
4. No work is lost.

## 273. Temporary outage

1. Primary returns 5xx.
2. Circuit breaker opens after configured evidence.
3. Retry uses jitter.
4. Standby resumes.
5. Primary only re-enters after half-open canaries pass.

---

# Part LI — Acceptance scenarios: routing intelligence

## 274. Pareto domination

1. Model A has same/lower verified success and worse latency/quota/continuity than B.
2. A is removed from the active Pareto frontier.

## 275. Strong slow model

1. Route A is substantially more capable but slower.
2. Task is architecture-critical.
3. Quality floor/terminal success dominate latency.
4. A may still win.

## 276. Tiny score difference

1. Two routes differ by statistically meaningless score margin.
2. Current route is healthy.
3. BindingGranularityPolicy avoids switch.

## 277. Stage specialization

1. Architecture stage favors Model A.
2. Implementation favors Model B.
3. Verification favors Model C.
4. Stage binding performs controlled handoffs rather than per-request churn.

---

# Part LII — Metrics

## 278. Marketplace metrics

```text
provider_discovery_latency
provider_policy_diff_latency
free_to_paid_detection_latency
retirement_detection_latency
catalog_staleness_rate
price_epoch_expiry_rate
```

## 279. Billing metrics

```text
billing_mode_proof_coverage
auto_reload_hazards_blocked
postpay_hazards_blocked
paid_fallback_closure_failures
false_free_admission_rate
paid_autonomous_calls
```

Hard targets:

```text
false_free_admission_rate = 0
paid_autonomous_calls = 0
```

## 280. Provider health metrics

```text
semantic_200_failure_rate
protocol_corruption_rate
conversation_integrity_failure_rate
circuit_open_rate
half_open_recovery_success
mean_recovery_time
```

## 281. Quota metrics

```text
quota_forecast_error
unexpected_exhaustion_rate
recovery_reserve_violation_rate
quota_wasted_on_dominated_routes
```

Hard target:

```text
recovery_reserve_violation_rate = 0
```

## 282. Nested routing metrics

```text
backend_identity_observability
backend_change_rate
zero_cost_fallback_closure_rate
hidden_backend_incident_rate
```

## 283. Binding metrics

```text
switches_per_task
unnecessary_switch_rate
handoff_tax_per_switch
stage_binding_success
operation_binding_success
```

## 284. Pareto metrics

```text
eligible_frontier_size
dominated_route_elimination_rate
quality_floor_violation_rate
verified_success_lower_bound_of_selected_route
```

Hard target:

```text
quality_floor_violation_rate = 0
```

## 285. Joint runtime metrics

```text
joint_runtime_promotion_gain
interaction_regression_rate
joint_runtime_rollback_rate
```

---

# Part LIII — Conceptual modules

## 286. Suggested additions

```text
src/alinacoder/intelligence_mesh/
  frontier_marketplace.py
  provider_lifecycle.py
  provider_policy_diff.py
  provider_tombstones.py
  price_epoch.py
  billing_mode_proof.py
  account_hazard_scanner.py
  spend_invariant.py
  quota_headers.py
  exhaustion_forecast.py
  availability_forecast.py
  zero_cost_fallback_closure.py
  nested_router.py
  semantic_health.py
  provider_circuit_breaker.py
  hedged_inference.py
  availability_slo.py
  eligible_pareto.py
  quality_floor.py
  binding_granularity.py
  router_policy_portfolio.py
  route_drift.py
  safe_exploration.py
  joint_runtime_state.py
  context_transmission_budget.py
  protocol_matrix.py
  model_identity_attestation.py
  warm_standby.py
  data_use_cost.py

src/alinacoder/providers/
  kilo.py
  zai.py
  sambanova.py
  groq.py
  cloudflare_workers_ai.py
  openrouter.py
  gemini_free.py
  mistral_free.py
  huggingface_inference.py
  tencent_tokenhub.py
  opencode_zen.py
  ollama_cloud.py
  nvidia_nim.py
  github_models_tombstone.py

src/alinacoder/credentials/
  credential_handle.py
  windows_secret_store.py

src/alinacoder/evaluation/
  provider_lifecycle_bench.py
  price_epoch_bench.py
  billing_hazard_bench.py
  nested_fallback_bench.py
  semantic_200_bench.py
  provider_drift_bench.py
  route_pick_stability_bench.py
  binding_granularity_bench.py
  joint_runtime_bench.py
```

Names remain conceptual and may be reorganized during implementation without weakening contracts.

---

# Part LIV — Recommended implementation order

## 287. Phase K1 — hard billing/account safety first

Implement:

```text
BillingModeProof
AccountAutomationHazardScanner
SpendInvariantProof
PriceEpochLease
```

before adding more gateways.

## 288. Phase K2 — provider lifecycle

Implement:

```text
ProviderLifecycleState
ProviderPolicyChangeDiff
ProviderTombstoneRegistry
EndOfAvailabilityForecast
```

## 289. Phase K3 — live quota control

Implement:

```text
QuotaHeaderNormalizer
ExhaustionForecast
ContextTransmissionBudget
```

## 290. Phase K4 — semantic resiliency

Implement:

```text
SemanticHealthCell
ProviderCircuitBreaker
ModelIdentityAttestation
WarmStandbyPool
```

## 291. Phase K5 — high-value provider adapters

First candidates by current structural usefulness:

```text
Kilo Gateway
Z.AI
SambaNova
Groq
Cloudflare Workers AI
Tencent TokenHub/Hunyuan
Gemini Free Tier
Mistral Free mode
OpenRouter free-only
```

subject to live verification at implementation time.

## 292. Phase K6 — nested router safety

Implement:

```text
ZeroCostFallbackClosure
NestedRouterTransparency
```

before trusting aggregator-managed fallback.

## 293. Phase K7 — smarter selection

Implement:

```text
EligibleParetoFrontier
QualityFloorController
BindingGranularityPolicy
RouterPolicyPortfolio
```

## 294. Phase K8 — joint self-improvement

Implement:

```text
JointRuntimeState
BestKnownJointRuntimeState
```

and replay the complete runtime bundle.

## 295. Phase K9 — optional cloud orchestration

Only then add optional Supabase queues/Vault/cron notifications where useful.

---

# Part LV — Research basis added by this pass

## 296. Research date

Primary research was performed on 2026-09-04 with emphasis on first-party provider documentation and 2026 routing literature.

## 297. Kilo

First-party pages reviewed include:

```text
https://kilo.ai/landing/free-models
https://kilo.ai/docs/gateway/api-reference
```

Key architectural lessons:

```text
live zero-price catalog
frequent catalog refresh
credentialless model/provider discovery
OpenAI-compatible gateway
free promotions can end
```

## 298. OpenCode Zen

First-party page reviewed:

```text
https://opencode.ai/docs/zen/
```

Key lessons:

```text
zero-priced models can coexist with paid catalog
auto-reload/payment configuration is an independent hazard
provider/model combinations are curated for agentic coding
```

## 299. Z.AI

First-party pricing reviewed:

```text
https://docs.z.ai/guides/overview/pricing
```

Key lessons:

```text
exact models can be zero-priced
model suffix does not determine price
provider tools can be paid even when inference is free
```

## 300. SambaNova

First-party rate-limit documentation reviewed:

```text
https://docs.sambanova.ai/docs/en/models/rate-limits
```

Key lessons:

```text
no-payment-method state defines Free Tier
per-model free quotas
live quota response headers
```

## 301. Groq

First-party documentation reviewed:

```text
https://console.groq.com/docs/rate-limits
https://console.groq.com/docs/models
```

Key lessons:

```text
organization-level free quotas
per-model limits
remaining/reset headers
fast serving is useful but quality remains task-relative
```

## 302. Cloudflare Workers AI

First-party pricing reviewed:

```text
https://developers.cloudflare.com/workers-ai/platform/pricing
```

Key lesson:

```text
same provider has materially different zero-spend behavior on Free vs Paid plan
```

## 303. OpenRouter

First-party limits reviewed:

```text
https://openrouter.ai/docs/api_reference/limits
```

Key lessons:

```text
free model limits are explicit
aggregator routing requires free-only closure
account credit state must not expand paid eligibility
```

## 304. Google Gemini

First-party billing/pricing documentation reviewed:

```text
https://ai.google.dev/gemini-api/docs/billing
https://ai.google.dev/gemini-api/docs/pricing
```

Key lesson:

```text
Free Tier is an account/project state distinct from paid/prepaid usage
```

## 305. Mistral

First-party documentation reviewed on Free mode, account limits and PAYG behavior.

Key lesson:

```text
Free mode + PAYG disabled can structurally stop after included usage
```

subject to live account verification.

## 306. Hugging Face Inference Providers

First-party pricing/docs reviewed:

```text
https://huggingface.co/docs/inference-providers/pricing
https://huggingface.co/docs/inference-providers/index
```

Key lesson:

```text
small included credits and nested provider routing require account/fallback proof
```

## 307. Tencent

Official Tencent Cloud/TokenHub/Hunyuan documentation reviewed.

Key lesson:

```text
post-payment disabled can provide a real hard-stop after free entitlement
```

while campaigns/eligible models remain time-sensitive.

## 308. GitHub Models

Official GitHub retirement notice reviewed:

```text
https://github.blog/changelog/2026-07-30-github-models-is-now-retired/
```

Key lesson:

```text
provider retirement must automatically tombstone stale routes
```

## 309. FailureAtlas — 2026

Recent research on multi-provider LLM gateways highlights silent failures that return HTTP 200 while corrupting session/tool payload state.

Applied through:

```text
SemanticHealthCell
ModelIdentityAttestation
semantic canaries
conversation/tool integrity checks
```

## 310. ParetoBandit — 2026

Recent routing work studies runtime addition/removal of models and adaptation to silent quality/price drift.

Applied through:

```text
ProviderPolicyChangeDiff
RouteDriftDetector
SafeExplorationEnvelope
EligibleParetoFrontier
```

without importing paid-budget optimization into the zero-spend policy.

## 311. LQM-ContextRoute — 2026

Research on functionally equivalent providers shows that latency should not simply compensate for lower answer quality.

Applied through:

```text
QualityFloorController
ProviderAvailabilitySLOMemory
Pareto selection
```

## 312. OrcaRouter / router portfolio findings — 2026

Recent production routing results reinforce evolving model pools, offline warmup plus online evidence, and instability under paraphrases.

Applied through:

```text
RouterPolicyPortfolio
RoutePickStability
margin tie-breaking
```

## 313. MERA-style joint adaptation — 2026

Recent model-evolution/routing research motivates execution-verified skill adaptation and evaluating interacting runtime components together.

Applied through:

```text
JointRuntimeStatePromotion
BestKnownJointRuntimeState
```

## 314. Supabase docs/changelog

Current Supabase docs/changelog were reviewed for:

```text
PGMQ queues
visibility timeouts
queue archival
pg_cron
pg_net
Vault
Realtime Broadcast Replay
managed realtime schema restrictions
```

Supabase remains optional and cannot weaken local-first operation.

---

# Part LVI — Canonical Autonomous Frontier Marketplace loop

## 315. Marketplace loop v4

```text
Receive task
→ repair-aware IntentContract
→ TaskDescriptor + OOD support
→ current Stage / BindingGranularityPolicy
→ refresh ProviderLifecycle diffs due now
→ FrontierReleaseRadar / ProviderDiscoveryWorker
→ tombstone filter
→ construct exact RouteCells
→ ModelNameSemanticsForbidden
→ BillingModeProof
→ AccountAutomationHazardScanner
→ SpendInvariantProof
→ current PriceEpochLease
→ FeatureBillingVector
→ ZeroCostFallbackClosure
→ privacy/DataUseCostClass/use-scope
→ credential availability
→ QuotaHeaderNormalizer
→ ExhaustionForecast
→ EndOfAvailabilityForecast
→ protocol/capability matrix
→ ModelIdentityAttestation
→ SemanticHealthCell
→ TaskDistributionSupport / ExecutionGroundedRoutingMemory
→ EvidencePrecision-aware capability posterior
→ QualityFloorController
→ EligibleParetoFrontier
→ ResourceShadowPriceController
→ RouterPolicyPortfolio
→ choose exact primary RouteCell
→ qualify WarmStandbyPool
→ TaskAffinity/Binding lease
→ execute OperationGraph
→ observe live quota/latency/semantic health
→ on degradation, freeze at safe boundary
→ canonical failover transaction
→ DirectionAwareTrajectorySanitizer
→ TaskRelativeSufficientState
→ ContinuityRestoreBarrier
→ ContinuityProof
→ SessionVersionCAS
→ resume
→ deterministic verification / Done Contract
→ delayed terminal reward
→ update route/provider evidence
→ drift detector
→ RouterGainCertificate / JointRuntimeState promotion or rollback
```

---

# Part LVII — Non-negotiable invariants

## 316. AlinaCoder must never

- treat a provider/model list embedded in code as permanent market truth;
- treat “free”, “flash”, “preview”, “open”, or similar model-name text as billing evidence;
- use stale zero-price evidence after its lease expires;
- continue using a route after an official retirement or material billing-policy change without requalification;
- resurrect a tombstoned provider from a lower-authority community directory;
- automatically add a payment method;
- automatically enable post-pay or PAYG;
- automatically enable auto-reload or credit top-up;
- consume purchased credits merely because they already exist;
- allow provider-side fallback to a paid route;
- assume an aggregator backend is stable when it is opaque;
- treat two mirrors of the same underlying model/backend as independent cognitive diversity;
- accept HTTP 200 as proof of semantic correctness;
- commit malformed/truncated tool calls into canonical state;
- commit a response after detected conversation-state loss;
- perform fixed synchronized retry storms;
- hedge requests when duplicate quota or side effects violate safety;
- let low latency compensate for failure to meet the task quality floor;
- switch models for statistically meaningless score differences;
- over-pin a weak route through an entire task when stage-specific evidence shows a materially stronger route;
- over-switch on every request when handoff tax dominates benefit;
- give an unseen route immediate high-impact mutation authority;
- promote router/skill/verifier changes only in isolation when they interact at runtime;
- expose raw provider credentials to models, logs, Git, memory, or public state;
- require Supabase for local execution;
- treat Realtime notifications as durable canonical truth;
- use browser scraping/session-token extraction to access consumer AI products when no officially supported automation path exists;
- weaken IntentContract, Done Contract, deterministic verification, rollback, resource gates or canonical state continuity in pursuit of a stronger model.

## 317. Final target behavior

The desired user experience is:

```text
Open alinacoder.exe
→ speak/write naturally
→ task state becomes canonical and model-independent
→ AlinaCoder continuously knows which providers still exist
→ it discovers newly released models automatically
→ it knows which exact route is really free right now
→ it knows whether the current account can ever charge
→ it knows remaining quota and likely exhaustion time
→ it rejects hidden paid fallback and billing automation
→ it verifies the real backend and semantic health
→ it ranks only hard-eligible routes
→ it chooses the strongest verified route for the current stage
→ it stays on that route while staying useful
→ before exhaustion/degradation it prepares a standby
→ it switches at a safe boundary
→ the replacement receives exact verified task state
→ failed-model confusion is sanitized
→ continuity is proven before mutation resumes
→ the completed work is verified locally
→ routing/model/provider evidence is updated
→ new champions can replace old ones automatically
→ retired/paid/degraded routes disappear automatically
→ autonomous paid API spend remains exactly €0
```

The architectural destination is:

> **A continuously self-updating, zero-cost Frontier Marketplace inside AlinaCoder: a system that treats LLM intelligence as a volatile market of verifiable RouteCells, discovers and profiles new brains automatically, proves exact account-level non-billability, monitors real quota and semantic health, selects from a task-relative Pareto frontier, preserves model-independent canonical context, and performs transactional failover so the strongest currently legitimate model can take over without losing the user's thread.**
