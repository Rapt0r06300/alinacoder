# AlinaCoder v0.2 — Autonomous Provider Fabric, Live Free-Model Oracle & Seamless Protocol Continuity Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose

This amendment extends the existing Frontier Intelligence, Autonomous Frontier Marketplace and Frontier Capacity/Continuity architecture with a new provider-fabric layer.

The target is no longer merely:

> choose a good free model and fail over when it stops working.

The target is:

> **AlinaCoder must continuously discover the strongest legitimate intelligence currently reachable at zero autonomous monetary spend, prove the exact entitlement and authentication channel for every candidate, connect through officially supported mechanisms, benchmark new brains against verified coding outcomes, choose the strongest useful model or orchestration regime for each stage, and transfer execution authority between heterogeneous providers without losing the user's intent, repository state, evidence, tool state, safety constraints or commit authority.**

This amendment is additive and jointly normative with the previously approved v0.2 specifications, especially:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-oracle-ood-certified-continuity-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-marketplace-resilience-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-capacity-orchestration-fenced-continuity-amendment.md`

The stricter rule wins where provisions overlap.

This amendment has precedence for:

- provider authentication and reconnect flows;
- auth-channel-specific entitlements;
- live free-model discovery;
- conditional/time-window pricing;
- model-level free eligibility;
- provider catalog authority ranking;
- terms/use-scope snapshots;
- strongest-useful-model semantics;
- zero-cost route union construction;
- protocol normalization across OpenAI/Anthropic/Gemini-compatible APIs;
- context-fit planning;
- tool/schema compatibility preflight;
- model champion/challenger promotion;
- active routing exploration;
- retrieval usefulness gating;
- consensus blind-spot protection;
- causal/counterfactual routing attribution;
- failover-storm suppression;
- live provider atlas corrections/additions documented on 2026-09-04.

All existing IntentContract, local-first, deterministic verification, zero-paid-spend, privacy, OOD, rollback, resource, provider lifecycle, semantic-health, quota, fencing, continuity and Git `main`-only invariants remain binding.

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
ALLOW_ACCOUNT_FARMING = false
ALLOW_QUOTA_EVASION = false
```

---

# Part I — The provider is not the routing atom

## 2. RouteCell v3

The real routing atom is the exact combination:

```text
provider
account/workspace
region
auth channel
endpoint
protocol
logical model
model revision
service tier
pricing branch
entitlement bucket
feature bundle
privacy/use scope
backend identity
```

A provider name alone proves almost nothing.

## 3. Example

`Cloudflare Workers AI` can simultaneously have:

- a free daily Neuron allowance;
- ordinary models usable within that allowance;
- frontier model IDs that require a paid billing method or prepaid credits.

Therefore:

```text
provider_is_free == true
```

is prohibited as an admission rule.

## 4. RouteCell key

Canonical identity:

```text
RouteCellKey = hash(
  provider,
  account,
  region,
  auth_channel,
  endpoint,
  protocol,
  model_revision,
  service_tier,
  pricing_branch,
  feature_bundle
)
```

Evidence and health are stored against this identity.

---

# Part II — ProviderAuthBroker

## 5. Official connection broker

Introduce:

```text
ProviderAuthBroker
```

Its job is to connect AlinaCoder to providers through their officially supported client mechanisms.

## 6. Supported auth modes

```text
ANONYMOUS
API_KEY
BEARER_TOKEN
DEVICE_OAUTH_RFC8628
AUTHORIZATION_CODE_PKCE
ADC
SERVICE_ACCOUNT
SCOPED_PROVIDER_TOKEN
USER_MEDIATED_ONE_TIME_CODE
UNSUPPORTED
```

## 7. Browser rule

A browser may be opened only for an official authorization/consent flow such as OAuth PKCE/device authorization.

AlinaCoder must never:

```text
scrape a consumer chat UI
read browser cookies
copy localStorage/sessionStorage credentials
extract private browser tokens
simulate a human chat session to evade API rules
reuse hidden consumer endpoints without official authorization
```

## 8. One-time consent semantics

Autonomous connection means:

```text
user authorizes a provider once when required
→ AlinaCoder stores the resulting provider-authorized credential securely
→ refreshes/reconnects automatically when the protocol permits
→ no repeated user interaction during ordinary operation
```

It does not mean bypassing authorization.

## 9. ProviderConnectionLadder

For a provider/model candidate, attempt in this order:

```text
1. supported anonymous access
2. already-valid scoped credential
3. refresh existing credential
4. officially supported device OAuth / PKCE
5. existing user-supplied API key
6. explicit one-time manual credential import
7. mark unavailable
```

Never downgrade from an official safe flow to a browser-scraping workaround.

## 10. Auth capability record

```text
ProviderAuthCapability
provider
auth_mode
supports_localhost_callback
supports_headless_code
supports_refresh
supports_revoke
scope_model
credential_lifetime
credential_rotation
account_binding
org_binding
provider_documentation
verified_at
```

---

# Part III — Credential custody

## 11. Windows-first credential storage

For `alinacoder.exe`, local credentials must default to an OS-protected secret store appropriate to Windows, for example a DPAPI/Credential-Manager-backed abstraction.

## 12. CredentialHandle only

All runtime objects carry:

```text
CredentialHandle
```

not raw tokens.

## 13. Never persist secrets in

```text
Git repository
Markdown specs
SQLite plaintext fields
logs
telemetry
model prompts
experience cards
Supabase public tables
crash dumps where avoidable
```

## 14. Token refresh single-flight

Concurrent tasks must not all refresh the same credential.

Introduce:

```text
CredentialRefreshSingleFlight
```

Only one refresh runs per credential generation; waiting tasks consume the new result.

## 15. Rotation

If refresh returns a new refresh token:

```text
write new credential atomically
→ verify decrypt/read
→ revoke/retire old generation where supported
```

## 16. Revocation

Provider logout/revocation invalidates all RouteCells dependent on the credential before the credential is removed locally.

---

# Part IV — AuthChannelEntitlement

## 17. Authentication method can change quota

Introduce:

```text
AuthChannelEntitlement
```

The entitlement is indexed by:

```text
provider + account + auth_channel + model + feature
```

not merely provider/account/model.

## 18. Why this matters

Current provider programs can expose independent quota systems for:

- ordinary API keys;
- OAuth-authenticated integrations;
- coding-plan-specific endpoints;
- anonymous access;
- trial credentials;
- provider-specific app keys.

These channels must never be mixed silently.

## 19. No quota multiplication abuse

The existence of multiple legitimate channels does **not** authorize:

```text
creating duplicate identities
creating extra accounts
rotating API keys to evade organization quotas
using VPN/proxy/IP rotation to evade limits
misrepresenting application type
```

## 20. Shared quota detection

Two channels that map to one upstream entitlement bucket are represented by one shared `FreeCapacityLedger` resource.

---

# Part V — ProviderAuthStateMachine

## 21. States

```text
UNKNOWN
DISCOVERED
AUTH_NOT_REQUIRED
NEEDS_USER_CONSENT
AUTHORIZING
AUTHORIZED
REFRESHING
DEGRADED
REVOKED
EXPIRED
BLOCKED_BY_POLICY
UNSUPPORTED
```

## 22. Mutation authority

An auth transition can alter route availability but can never directly grant mutation authority to a model.

Model authority still requires the existing IntelligenceLease, continuity and CommitEpoch gates.

## 23. Auth failure

On authentication failure:

```text
classify failure
→ refresh if officially supported
→ one bounded retry
→ mark route unavailable/degraded
→ route elsewhere
```

No unauthorized workaround.

---

# Part VI — LiveFreeModelOracle

## 24. Replace static free-model lists

Introduce:

```text
LiveFreeModelOracle
```

The repository may contain bootstrap provider adapters, but free model membership must be determined from live authoritative evidence.

## 25. Adapter contract

Every provider adapter should expose as many of these as the provider supports:

```text
list_models()
get_model_metadata()
get_pricing()
get_pricing_overrides()
get_entitlement()
get_quota_state()
get_rate_limit_state()
get_auth_state()
get_terms_scope()
get_data_policy()
get_backend_identity()
probe_protocol()
probe_semantics()
```

## 26. Free oracle result

```text
FreeRouteObservation
route_cell_id
logical_model_identity
zero_spend_proof
pricing_proof
funding_proof
quota_state
capabilities
context_window
protocol_features
terms_scope
privacy_class
health
freshness
source_chain
```

## 27. TTL is volatility-based

Catalog/pricing claims receive shorter TTLs when a provider changes them frequently.

Static legal/use-scope claims and volatile model pricing have different TTLs.

---

# Part VII — CatalogSourceAuthority

## 28. Evidence ranking

Introduce:

```text
CatalogSourceAuthority
```

Default authority order:

```text
FIRST_PARTY_LIVE_ACCOUNT_API
FIRST_PARTY_LIVE_PUBLIC_API
FIRST_PARTY_CONSOLE_STATE
FIRST_PARTY_DOCUMENTATION
FIRST_PARTY_CHANGELOG/ANNOUNCEMENT
SIGNED_OR_CANONICAL_PROVIDER_REPOSITORY
TRUSTED_LIVE_PROBE_DIRECTORY
COMMUNITY_TRACKER
BLOG/AGGREGATOR
UNVERIFIED
```

## 29. Conflict rule

A newer low-authority claim does not automatically defeat a slightly older first-party source.

Use:

```text
authority × freshness × claim_specificity
```

## 30. Official current evidence wins

If a community directory says a service is retired/free while current first-party documentation exposes the opposite state, the official source wins and the contradiction is recorded.

## 31. Discovery versus admission

Low-authority sources are valuable to find candidates.

They cannot authorize a RouteCell.

---

# Part VIII — ConditionalPriceFunction

## 32. Price is a function

Introduce:

```text
ConditionalPriceFunction
PriceFunctionProof
```

A model can be:

- zero-price only during a promotion;
- zero-price only with a suffix such as `:free`;
- zero-price only below a quota;
- zero-price on one provider but not another;
- zero-price for text but not web/search/tool features;
- subject to time-window pricing overrides.

## 33. Price variables

```text
provider
model/revision
time
region
auth channel
service tier
feature
input modality
output modality
context size
cache status
account class
quota state
```

## 34. Admission proof

Before remote inference:

```text
PriceFunctionProof(exact_request) == ZERO
or
HardFreeBucketStopProof(exact_request) == TRUE
```

must hold.

## 35. Unknown pricing branch

```text
UNKNOWN → BLOCK
```

for autonomous remote execution.

---

# Part IX — ModelEligibilityMatrix

## 36. Exact model-level free eligibility

Introduce:

```text
ModelEligibilityMatrix
```

Columns include:

```text
RouteCell
zero monetary spend
free bucket reachable
paid bucket reachable
payment method required
model allowed on free plan
feature allowed on free plan
use scope
privacy scope
context capability
tool support
structured output
vision/files
production/evaluation/trial class
```

## 37. Provider-level marketing labels prohibited

A provider's “Free plan” cannot automatically mark every hosted model eligible.

---

# Part X — FreePoolUnionRouter

## 38. Union of all legitimate zero-cost intelligence

Introduce:

```text
FreePoolUnionRouter
```

It builds a live union of eligible RouteCells across all providers and local engines.

## 39. Union stages

```text
collect
→ normalize
→ deduplicate logical model identity
→ resolve backend dependencies
→ remove unsafe use scopes
→ remove paid-risk cells
→ apply health/capability gates
→ rank by task requirements
```

## 40. Do not count mirrors twice

A logical model exposed through five gateways remains one logical intelligence candidate with five endpoint realizations.

## 41. Availability diversity

Independent hosting can still increase availability even when cognitive diversity is zero.

---

# Part XI — StrongestUsefulModelPolicy

## 42. “Strongest” is task-conditional

The user objective “always find the most powerful LLM” becomes:

```text
STRONGEST_USEFUL_MODEL
```

not “largest parameter count” or “highest global benchmark”.

## 43. Strongest-useful definition

A candidate is stronger for the current stage when it has higher expected verified terminal contribution under:

```text
required skills
context fit
tool compatibility
continuity compatibility
health
privacy/use scope
free capacity
latency constraints
verification evidence
```

## 44. Context can dominate nominal intelligence

If Model A is nominally stronger but cannot safely fit required repository/evidence context while Model B can, Model B may be operationally stronger for the stage.

## 45. Tool compatibility can dominate

A model that cannot reliably execute required structured tool calls is excluded from a tool-intensive stage even if it has higher chat benchmarks.

---

# Part XII — ContextFitPlanner

## 46. Introduce

```text
ContextFitPlanner
```

## 47. Estimate required context

```text
MUST_EXACT bytes/tokens
relevant code
active evidence
IntentContract
WorkGraph
current errors
recent turns
optional supporting memory
```

## 48. Candidate fit outcomes

```text
FULL_FIT
FIT_WITH_SAFE_COMPACTION
FIT_WITH_RETRIEVAL_ON_DEMAND
UNSAFE_TRUNCATION_REQUIRED
NO_FIT
```

## 49. Never silently truncate MUST_EXACT state

If context fit would discard a user constraint, hash, exact error, test result, commit epoch or active safety blocker:

```text
candidate not eligible
```

## 50. Context-normalized quality

Benchmarks should compare models with the context representation they will actually receive in AlinaCoder, not idealized full context they cannot fit in production.

---

# Part XIII — CanonicalInferenceEnvelope

## 51. Provider-neutral state

Introduce:

```text
CanonicalInferenceEnvelope
```

AlinaCoder must not make provider-specific transcript syntax the canonical conversation state.

## 52. Envelope fields

```text
IntentContract
system policy digest
user turn
semantic repair state
selected evidence objects
tool declarations
tool results
repo snapshot identifiers
WorkGraph node
expected response schema
context budget
continuity metadata
CommitEpoch
```

## 53. Provider adapters are projections

The envelope is projected into:

```text
OpenAI Chat Completions
OpenAI Responses
Anthropic Messages
Gemini/Google GenAI
provider-specific OpenAI-compatible dialect
local Ollama dialect
```

## 54. Response normalization

Provider responses are normalized back into a canonical result object before orchestration consumes them.

---

# Part XIV — ProviderProtocolNormalizer

## 55. Introduce

```text
ProviderProtocolNormalizer
```

## 56. Normalize differences in

```text
system/developer role semantics
tool declaration schema
tool-call IDs
tool-result encoding
structured-output declaration
reasoning/thinking switches
max-token parameters
streaming events
finish reasons
usage accounting
cached-token fields
error shapes
```

## 57. Provider quirk registry

Maintain:

```text
ProviderProtocolQuirkRegistry
```

with evidence/freshness per endpoint.

## 58. No blind “OpenAI-compatible” assumption

“OpenAI-compatible” means compatible enough for a class of calls, not bit-for-bit semantics.

Every RouteCell must prove the exact features AlinaCoder intends to use.

---

# Part XV — CompatibilityPreflight

## 59. Before a model receives a stage

Run:

```text
CompatibilityPreflight
```

## 60. Preflight checks

```text
context fits
tool calling supported
required number of tools supported
structured output supported
required modalities supported
system instruction semantics acceptable
streaming compatible
max output sufficient
reasoning parameter compatible
file/image payload limits sufficient
provider use scope permits task
privacy class permits payload
```

## 61. Failed preflight

Select the next RouteCell before sending privileged context.

---

# Part XVI — StatefulContinuationBundle v2

## 62. Cross-provider handoff packet

Extend existing handoff architecture with:

```text
StatefulContinuationBundleV2
```

## 63. Bundle contains

```text
CanonicalInferenceEnvelope digest
IntentContract version
ExecutionEvidenceGraph slice
WorkGraph state
repo HEAD and touched hashes
MUST_EXACT constraints
failed hypotheses
last discriminating observations
current tests/verification state
provider-independent tool state
pending effects
quota reservations
CommitEpoch
source route
handoff schema version
```

## 64. It does not contain

```text
private chain-of-thought
raw access tokens
browser session material
provider hidden reasoning fields
unnecessary full transcript
```

## 65. Rebuild, do not replay blindly

On handoff, destination context is reconstructed from canonical operational state rather than dumping source-provider raw messages.

---

# Part XVII — WarmStandbySnapshot

## 66. Faster safe failover

Introduce:

```text
WarmStandbySnapshot
```

## 67. Warm means prepared state, not paid inference

A standby can be “warm” by maintaining locally prepared:

```text
continuation bundle
context token estimate
protocol projection
compatibility result
quota reservation
health lease
```

without consuming a model request.

## 68. Refresh at checkpoints

Regenerate standby packet after significant verified checkpoints, not every token.

## 69. Benefits

Reduces:

```text
failover latency
context reconstruction errors
quota waste
handoff size surprises
```

---

# Part XVIII — ProviderHealthVector v2

## 70. Health is multi-dimensional

Introduce:

```text
ProviderHealthVector
```

## 71. Signals

```text
TCP/TLS availability
HTTP protocol health
auth health
catalog presence
exact model presence
pricing consistency
quota remaining
latency p50/p95
stream integrity
tool-call validity
structured-output validity
semantic canary
context-length canary
model-identity attestation
error-rate trend
provider status evidence
```

## 72. Partial degradation

A provider can remain eligible for plain text while being temporarily ineligible for tool-calling tasks.

## 73. Semantic degradation outranks HTTP 200

A route returning malformed or semantically corrupted responses is unhealthy even when availability is 100%.

---

# Part XIX — Live refresh triggers

## 74. FrontierRefreshTrigger

Refresh the oracle when:

```text
application startup
high-value task start
provider evidence TTL expires
model-not-found
pricing mismatch
quota threshold crossed
429/403/401 behavior changes
provider catalog changes
new model announcement discovered
known quota reset passes
before long stage reservation
OOD detected
champion confidence decays
standby becomes unavailable
```

## 75. Avoid blind constant polling

Discovery is event/TTL/need-driven.

## 76. Refresh priority

Safety/pricing/auth refresh outranks exploratory new-model discovery.

---

# Part XX — NewModelCandidatePipeline

## 77. New unknown model

Introduce:

```text
UnknownModelCandidate
ChampionChallengerController
```

## 78. Pipeline

```text
catalog discovery
→ source authority
→ pricing/funding proof
→ terms/privacy proof
→ identity attestation
→ protocol canary
→ feature probes
→ low-risk hidden benchmark slice
→ coding benchmark slice
→ continuity probes
→ posterior update
→ challenger/champion decision
```

## 79. Names do not prove quality

A model called “Ultra”, “Pro”, “Frontier”, “Opus”, “Max” or “Coder” receives no automatic quality bonus beyond metadata used as a weak prior.

## 80. Stealth/unknown model

Unknown identity models may be benchmarked in read-only/sandboxed contexts but cannot receive privileged mutation authority until identity/use-scope/continuity gates are sufficient.

---

# Part XXI — ChampionChallengerPosterior

## 81. Online evidence

Maintain task/skill-conditioned posterior evidence for current champion and challengers.

## 82. Lower-confidence decision

Promote challenger only when evidence indicates meaningful expected improvement and sufficient confidence, subject to safety and continuity.

## 83. Avoid one lucky run

Single-sample benchmark wins cannot promote a model globally.

## 84. Decay

Older performance evidence decays faster after provider/model revision changes.

---

# Part XXII — RoutingBoundaryCaseMiner

## 85. Exploration should target uncertainty

Introduce:

```text
RoutingBoundaryCaseMiner
```

## 86. High-value samples

Prioritize shadow comparisons where:

```text
champion and challenger estimates overlap
router recently misrouted
new task family appears
current winner changed revision
handoff pair evidence is weak
provider semantic drift suspected
```

## 87. Avoid random quota burn

Do not spend frontier free quota repeatedly proving obvious winners or losers.

## 88. Boundary learning

Routing data should disproportionately teach **where model choice changes outcomes**.

---

# Part XXIII — WorkflowEscalationGate

## 89. Heavy orchestration is conditional

Introduce:

```text
WorkflowEscalationGate
```

Possible actions:

```text
EARLY_EXIT
LOCAL_ONLY
SINGLE_STRONG
VERIFY
REPAIR_SAME_ROUTE
ESCALATE_STRONGER
PARALLEL_COMPARE
SPECIALIST_COUNCIL
ADVERSARIAL_REVIEW
```

## 90. Strongest useful model remains default for meaningful reasoning

The gate does not weaken the user's objective.

It prevents wasting scarce frontier calls on deterministic bookkeeping that cannot benefit from them.

## 91. Deterministic early exit

Examples:

```text
formatting only
known deterministic parser operation
hash comparison
successful exact test result interpretation
simple file existence check
```

may avoid a remote frontier call.

## 92. Non-trivial reasoning

Architecture, uncertain debugging, cross-file design and safety-critical reasoning should normally receive the strongest eligible intelligence or a stronger orchestration regime.

---

# Part XXIV — ConsensusBlindSpotGuard

## 93. Agreement can still be wrong

Introduce:

```text
ConsensusBlindSpotGuard
```

## 94. Consensus is weak evidence when

```text
models share same weights/upstream
same prompt induces same systematic error
OOD is high
no deterministic oracle exists
security consequences are high
all candidates rely on same false premise
```

## 95. High-risk consensus rule

High-impact action cannot waive independent verification solely because several LLMs agree.

## 96. Same model through different providers

Counts as availability diversity, not independent cognitive consensus.

---

# Part XXV — RetrievalUtilityGate

## 97. Memory retrieval can hurt

Introduce:

```text
RetrievalUtilityGate
```

## 98. Retrieved experience admission

Before injecting an ExperienceCard or previous route trace, estimate:

```text
semantic match
same project applicability
same environment/dependency versions
same failure signature
same user-intent constraints
freshness
historical utility
contradiction risk
```

## 99. High hit rate is not success

A retrieval subsystem is evaluated on downstream verified task improvement, not retrieval frequency.

## 100. No-match is valid

If no experience is sufficiently aligned:

```text
inject nothing
```

rather than noise.

---

# Part XXVI — CounterfactualRoutingAudit

## 101. Proxy attribution can mislead

Introduce:

```text
CounterfactualRoutingAudit
```

## 102. Bounded leave-one-out comparisons

On carefully selected hidden/canary tasks, occasionally compare:

```text
champion only
challenger only
champion + verifier
specialist topology
```

## 103. Goal

Estimate actual causal routing value rather than using response similarity/agreement as contribution.

## 104. Bounded quota

Counterfactual audits consume only allocated exploration reserve and cannot starve active user tasks.

---

# Part XXVII — ProviderFreeSafetyRank

## 105. Quality is ranked after eligibility

Introduce ordering:

```text
1. zero-spend certainty
2. authorization legitimacy
3. use-scope/privacy eligibility
4. semantic/protocol health
5. mandatory capability fit
6. context fit
7. expected verified task quality
8. continuity/recovery quality
9. latency/quota efficiency
```

## 106. “Powerful but unsafe” is not powerful for AlinaCoder

A route that risks payment, leaks confidential code into a training-allowed trial endpoint, or violates use scope is ineligible regardless of benchmark quality.

---

# Part XXVIII — AnonymousRoutePolicy

## 107. Anonymous free routes

Some gateways currently expose free inference without authentication.

Introduce:

```text
AnonymousRoutePolicy
```

## 108. Allowed payload classes

Anonymous routes default to:

```text
PUBLIC_OR_NON_SENSITIVE_ONLY
```

unless current data terms prove stronger confidentiality.

## 109. No IP evasion

Rate-limit exhaustion produces normal backoff/failover.

Never rotate IPs/proxies/VPN endpoints to obtain extra free capacity.

## 110. Identity uncertainty

Anonymous virtual routers that may change the underlying model require stronger response metadata/semantic attestation before continuation-sensitive use.

---

# Part XXIX — RetryBudgetController

## 111. A provider outage can create a quota cascade

Introduce:

```text
RetryBudgetController
FailoverStormGuard
```

## 112. Global retry budgets

Retries are controlled per:

```text
provider
route cell
task
failure signature
time window
```

## 113. Backoff

Use provider retry hints when present, otherwise bounded exponential backoff with jitter.

## 114. Circuit states

```text
CLOSED
DEGRADED
OPEN
HALF_OPEN
```

## 115. Half-open probe

Only a small number of canary requests probe recovery before full route admission resumes.

---

# Part XXX — FailoverStormGuard

## 116. Shared standby protection

If many tasks lose the same primary provider simultaneously, they cannot all stampede into a scarce free standby.

## 117. Admission queue

Use:

```text
priority
reserved quota
user-facing blocking state
stage criticality
continuity compatibility
```

## 118. Recovery reserve is protected

Shadow benchmarking stops automatically during provider-wide failover pressure.

---

# Part XXXI — Exact capability canaries

## 119. Feature canary suite

A route may be separately certified for:

```text
plain chat
long context
structured JSON
tool calling
multiple tool calls
streaming
vision
file payload
reasoning control
code generation
French/noisy French
```

## 120. Capability certification key

```text
RouteCell × feature × protocol × model revision
```

## 121. Canary expiration

Feature certificates expire when model revision, endpoint protocol or provider routing behavior materially changes.

---

# Part XXXII — Live provider atlas: recurring/standing candidates

## 122. Snapshot caveat

This section records the 2026-09-04 research snapshot only.

Runtime must requalify every candidate from current first-party/live evidence.

## 123. Kilo AI Gateway — major standing candidate

Current first-party Kilo documentation exposes an unauthenticated model catalog containing pricing, context and features.

Current documented free model examples include:

```text
stepfun/step-3.7-flash:free
poolside/laguna-s-2.1:free
poolside/laguna-xs-2.1:free
nvidia/nemotron-3-ultra-550b-a55b:free
tencent/hy3:free
openrouter/free
```

Current docs also show other `:free` IDs can exist dynamically.

## 124. Kilo anonymous capacity

Current first-party docs state free models can be called anonymously, with an IP-based limit currently documented as:

```text
200 requests/hour/IP
```

This is useful standing free capacity.

## 125. Kilo privacy caveat

Auto Free/free NVIDIA routes can have trial/data-use conditions.

Confidential repository content must not be sent unless exact upstream data policy permits it.

## 126. Kilo auto-free role

`kilo-auto/free` can be used as:

```text
dynamic discovery source
low-risk fallback
public/non-sensitive emergency capacity
```

but privileged work should prefer an exact known free model RouteCell when possible so AlinaCoder retains model identity/control.

## 127. Kilo provider dependency

Kilo may route some free traffic through OpenRouter or other providers.

Dependency graph evidence is required before treating Kilo and OpenRouter as independent standby domains.

---

# Part XXXIII — Groq Free

## 128. Strong recurring candidate

Current first-party Groq rate-limit documentation describes a Free Plan with model-specific recurring request/token limits.

Current examples include:

```text
openai/gpt-oss-120b
openai/gpt-oss-20b
qwen/qwen3.6-27b
qwen/qwen3.8-27b
groq/compound
groq/compound-mini
```

## 129. Current free-plan examples

At research time, first-party documentation lists for `gpt-oss-120b`, `gpt-oss-20b`, Qwen 3.6/3.8 27B approximately:

```text
30 RPM
1,000 RPD
8K TPM
200K TPD
```

and `groq/compound`/`compound-mini` with their own current limits.

These figures are snapshots and must be refreshed from account headers/settings.

## 130. Organization quota

Groq says limits apply at organization level.

Multiple keys must not be modeled as independent capacity.

## 131. Groq catalog

Use the live active-model endpoint rather than hardcoded IDs.

## 132. Free/paid separation

Current billing documentation describes explicit upgrade from Free to Developer requiring a payment method.

A Free-tier attestation can therefore be a strong funding-safety signal when current account state confirms it.

---

# Part XXXIV — GitHub Models free usage

## 133. Public-preview free candidate

Current first-party GitHub Models documentation describes rate-limited free API usage for experimentation/prototyping.

## 134. Paid usage separation

Paid usage requires explicit billing/payment enablement.

When paid usage is disabled/unavailable, free quota exhaustion should block rather than silently charge.

## 135. Eligibility

GitHub Models may be admitted only when:

```text
current free-use scope permits task
paid usage disabled or unreachable
exact model currently available
current per-model quota known
```

## 136. Preview caveat

Public-preview behavior and limits can change.

Use shorter evidence TTL than mature providers.

---

# Part XXXV — SambaNova Free

## 137. Structural free distinction

Current first-party SambaNova documentation states:

```text
Free Tier = no payment method linked
Developer Tier = payment method linked
```

This makes account-state classification particularly useful.

## 138. Current documented free examples

Examples at research time include:

```text
DeepSeek-V3.1
gpt-oss-120b
Meta-Llama-3.3-70B-Instruct
```

with current free limits around:

```text
20 RPM
20 RPD
200,000 TPD
```

for those listed routes.

Preview models may differ.

## 139. Role

Low RPD makes SambaNova especially useful as:

```text
high-value specialist
standby
shadow challenger
```

rather than a high-volume background worker.

---

# Part XXXVI — Gemini Free Tier

## 140. Standing account candidate

Google Gemini API currently exposes model-specific Free Tier quotas for eligible projects/accounts.

## 141. Account/project scope

Rate limits are project-scoped and current limits must be queried from the official account tooling/documentation.

## 142. Paid transition

Paid access requires billing setup.

AlinaCoder must prove project billing state and exact free route before use.

## 143. Privacy/use-scope

Free-tier data-use terms must be checked before confidential repository content is sent.

---

# Part XXXVII — OpenRouter free pool

## 144. Dynamic free suffixes

Use current OpenRouter model metadata and exact pricing to discover `:free` routes.

## 145. Free router

`openrouter/free` dynamically selects among current free models and filters on required capabilities.

## 146. Strong use cases

```text
discovery
emergency free capacity
candidate generation
non-sensitive tasks
```

## 147. Identity-sensitive work

If the exact underlying model matters for continuity or benchmark attribution, select an explicit free model instead of the virtual router when possible.

## 148. OAuth PKCE

Current first-party OpenRouter documentation supports PKCE login, including localhost callbacks for local apps and a headless code flow.

After authorization, the code is exchanged for a user-controlled API key.

This is a preferred supported onboarding mechanism over manual key copy when suitable.

## 149. Credit contamination

OpenRouter accounts with purchased credits require the existing FundingSourceProof/zero-spend closure before any route is eligible.

---

# Part XXXVIII — Cloudflare Workers AI

## 150. Daily free compute

Current first-party docs state Workers Free includes:

```text
10,000 Neurons/day
reset 00:00 UTC
operations fail after limit
```

## 151. Critical frontier exclusion

Current first-party docs explicitly state several current frontier models require a paid billing method or prepaid AI Gateway credits, including at research time:

```text
Kimi K2.6
Kimi K2.7 Code
GLM-5.2
GLM-5.3
GLM-5.3 Flash
DeepSeek V4 Flash
DeepSeek V4 Pro
```

Therefore these RouteCells are **not** admitted as free merely because the account has the Workers Free daily allocation.

## 152. Cloudflare value

The free allocation remains useful for eligible models and helper workloads, while the strongest paid-gated models remain excluded under €0 policy.

---

# Part XXXIX — Hugging Face Inference Providers

## 153. Tiny recurring credit

Current Hugging Face documentation provides small monthly free credits for free users.

## 154. Strategic role

Use for:

```text
small canaries
rare specialist tasks
model discovery
```

not as a guaranteed high-volume frontier backbone.

## 155. Paid overflow

If purchased credits/PAYG can be consumed after included credits, block unless hard free-bucket isolation exists.

---

# Part XL — Requesty

## 156. Provisional standing candidate

Current first-party Requesty material advertises a free tier restricted to free models with:

```text
200 requests/day
no credit card
no trial timer
OpenAI-compatible endpoint
```

## 157. Admission status

Classify:

```text
PROVISIONAL_RECURRING_FREE
```

until current terms, account state and live model metadata confirm the exact intended use.

## 158. Same-key upgrade risk

Because the same account/key can later access paid catalog after upgrade, account tier and allowed-model set must be part of FundingSourceProof.

---

# Part XLI — Mistral

## 159. Free-access candidate with use-scope proof

Current Mistral material exposes free/limited developer experiences and current models, but the exact API free-entitlement rules can vary by product/workspace.

## 160. Rule

Never import community claims of a 1B-token monthly API allowance as authoritative without current first-party account evidence.

## 161. Codestral/Mistral value

Keep as a high-priority candidate for live requalification, especially coding-specific models.

---

# Part XLII — Temporary frontier capacity

## 162. Trial capacity is valuable but not standing

Introduce:

```text
TemporaryFrontierBucket
```

## 163. Use

Temporary credits can be intelligently scheduled for:

```text
champion comparison
hard architecture task
rare OOD recovery
benchmark calibration
```

before expiry, but cannot be assumed available later.

---

# Part XLIII — Alibaba Cloud Model Studio / QwenCloud

## 164. New-user free quota

Current first-party Alibaba/Qwen documentation describes model-specific new-user free quotas, generally time-limited around 90 days for eligible routes/regions.

## 165. Free Quota Only

Current docs expose a `Free Quota Only`/worry-free hard-stop mode for eligible models.

## 166. Synchronization delay

Because changing the protection can take time and displayed quota can lag:

```text
console switch requested
→ wait for attestation window
→ probe zero-cost behavior
→ only then enable route
```

## 167. Auth-channel distinction

Current Alibaba documentation states OAuth authentication can have an independent free model-inference quota distinct from general API-key quota.

This must be represented by `AuthChannelEntitlement`, not merged blindly.

## 168. Coding Plan restriction

Current Coding Plan documentation restricts plan-specific keys to supported interactive coding tools/use cases and warns against automated scripts/application backends.

Therefore:

```text
AlinaCoder autonomous backend use
→ BLOCK unless current official scope explicitly permits it
```

regardless of whether the user owns such a plan.

---

# Part XLIV — Tencent TokenHub promotional capacity

## 169. Current promotion candidate

Current Tencent Cloud material describes new-account free trial allocations for multiple frontier/open models, including DeepSeek, GLM, Kimi and MiniMax families, with model-specific validity windows.

## 170. Postpaid rule

If postpaid billing is disabled and current provider behavior guarantees exhaustion stops service, trial cells may be eligible.

If postpaid is enabled:

```text
BLOCK unless hard zero-spend mode proven
```

## 171. Promotion expiry

Do not treat 2026 promotional availability as standing architecture.

---

# Part XLV — Z.AI / GLM

## 172. Current flagship discovery

Current first-party Z.AI documentation identifies GLM-5.3 and GLM-5.3-Flash among current flagship options.

## 173. Free status correction

Current new-user coding access described in provider tooling is time-limited trial capacity, not a permanent free backbone.

## 174. General API

General API access and paid Coding Plans are not automatically eligible under the €0 policy.

## 175. Supported account authorization

Where official Z.AI/ZCode account-binding flows are supported for the exact use case, they can be integrated through `ProviderAuthBroker`; entitlement still requires separate proof.

---

# Part XLVI — OpenCode Zen

## 176. Limited-time free model discovery

Current Zen documentation lists multiple models with zero token price at research time, including Nemotron/MiMo/Ling/Muse/stealth free entries.

## 177. Billing hazard

Zen also documents credit balance and auto-reload behavior.

Therefore no Zen account is autonomous-zero-spend eligible until:

```text
auto reload disabled
paid model allowlist blocked
exact model price == zero
funding source cannot touch balance
```

## 178. Training/data caveats

Some free Zen routes explicitly permit data use or use NVIDIA trial endpoints.

Use-scope/privacy gate applies before repository context is sent.

---

# Part XLVII — Pollinations

## 179. Live catalog value

Pollinations exposes public model listing endpoints and a broad OpenAI-compatible generation surface.

## 180. Supported app auth

Current first-party docs describe App Keys usable as OAuth clients, including authorization/device flows that can mint scoped user credentials.

## 181. Funding remains separate

OAuth convenience does not make a model free.

Exact price/funding proof remains mandatory.

## 182. Zero-price public model

A public Pollinations model may be admitted only while the current exact price is zero and any downstream/tool generation costs also satisfy zero-spend closure.

---

# Part XLVIII — ModelScope

## 183. High-potential discovery candidate

Current ecosystem evidence indicates ModelScope API-Inference exposes a very large zero-priced open-model catalog, potentially including strong Qwen/DeepSeek/GLM/MiniMax routes.

## 184. Evidence limitation

This research pass did not obtain sufficiently authoritative first-party English-language proof for all quota/use-scope details.

Therefore classification is:

```text
DISCOVERY_CANDIDATE
REQUIRES_FIRST_PARTY_USE_SCOPE_PROOF
```

## 185. No premature eligibility

Community reports of large daily free request allowances are discovery hints only.

AlinaCoder must confirm current official terms/account behavior before execution.

---

# Part XLIX — NVIDIA NIM

## 186. Free development/prototyping

Current NVIDIA material provides free hosted NIM API access for prototyping/development.

## 187. Scope restriction

Classify conservatively as:

```text
PROTOTYPING_ONLY_FREE_CAPACITY
```

unless exact current terms permit the intended task.

## 188. Privacy

Trial endpoints that log data for security/product improvement cannot receive confidential project content unless user/project policy permits it.

---

# Part L — Fireworks and other one-time starter credits

## 189. One-time credit class

Providers that offer only a small signup credit are:

```text
ONE_TIME_TRIAL_CREDIT
```

not recurring free capacity.

## 190. Role

Useful for bounded evaluation only if no payment-risk path exists.

They do not enter the standing free backbone.

---

# Part LI — Discovery federation

## 191. ProviderDiscoveryFederation

Use several discovery channels:

```text
first-party model APIs
first-party pricing APIs/docs
provider changelogs
Kilo/OpenRouter live catalogs
models.dev-style metadata
trusted live free-provider trackers
research/search engines
GitHub ecosystem adapters
```

## 192. Search engines propose, never authorize

Exa/Parallel/web research may discover a provider or changed rule.

Runtime admission still requires source authority + canary + funding/use-scope proof.

## 193. New-provider queue

Discovery produces:

```text
ProviderCandidateEvidence
```

not an automatically trusted adapter.

---

# Part LII — TermsSnapshot

## 194. Terms are runtime dependencies

Introduce:

```text
ProviderTermsSnapshot
```

## 195. Fields

```text
provider
product/tier
automation_allowed
production_allowed
commercial_allowed
training/data-use policy
confidential-data suitability
geographic restrictions
rate-limit/fair-use rules
auth restrictions
source
content hash
verified_at
```

## 196. Terms change

Material terms diff:

```text
route → REVIEW_REQUIRED/BLOCKED
```

until requalification.

## 197. No silent privilege broadening

A provider becoming more permissive does not automatically widen data scope without the project privacy policy also permitting it.

---

# Part LIII — Provider capability adapters are generated, then verified

## 198. AdapterGenerator

For a new OpenAI-compatible provider, AlinaCoder may generate a candidate adapter from documentation/schema.

## 199. Candidate status

Generated adapter starts:

```text
UNTRUSTED_ADAPTER
```

## 200. Required tests

```text
auth negative test
model-list probe
plain chat
streaming
structured response if claimed
tool call if claimed
rate-limit parsing
pricing/quota parsing
error normalization
secret-redaction test
```

## 201. Promotion

Only test-proven adapter becomes runtime-eligible.

---

# Part LIV — ModelIdentityAttestation v2

## 202. Aggregators may reroute silently

Extend identity evidence with:

```text
requested model ID
returned model metadata
provider response headers
stable semantic fingerprint
context-limit behavior
feature behavior
upstream provider metadata when available
```

## 203. Virtual router identity

For `openrouter/free`, `kilo-auto/free` or similar:

```text
virtual_route_id
resolved_model_if_available
resolved_provider_if_available
```

are logged separately.

## 204. Unresolved backend

A virtual route with unknown backend cannot be treated as a continuity-certified exact model.

---

# Part LV — ModelStrengthEvidence

## 205. Strength is execution-grounded

Introduce:

```text
ModelStrengthEvidence
```

Evidence sources ranked:

```text
project-specific deterministic success
hidden coding benchmark
recent verified comparable task
independent external benchmark
provider benchmark claim
model size/name
```

## 206. Project-specific evidence wins

A model that solves the user's real repository tasks more reliably can outrank a model with a higher generic benchmark.

## 207. Temporal split

Evaluation should distinguish:

```text
known historical benchmark tasks
fresh temporal tasks
project-generated hidden tasks
```

so new models are not promoted from contamination-prone public benchmarks alone.

---

# Part LVI — Online routing loop v2

## 208. Context–Action–Feedback

Every meaningful model-selection decision records:

```text
routing context
selected route
alternatives
prediction
verified outcome
failure class
quota/resource use
handoff cost
```

## 209. Regret

Track cumulative regret versus the best route known from later verified evidence where counterfactual evidence exists.

## 210. OOD

New task families increase exploration/verification rather than causing confident extrapolation.

---

# Part LVII — Retrieval and router memory separation

## 211. Routing memory is not prompt memory

Performance history may inform route selection without injecting the old task's content into the execution model.

## 212. Prefer metadata first

Router can use:

```text
skill tags
model success stats
failure signatures
route availability
```

without contaminating the coding prompt with irrelevant previous solutions.

---

# Part LVIII — Adaptive orchestration escalation

## 213. Two-stage scheduler

For complex workflows:

```text
cheap deterministic/lightweight gate
→ strong scheduler only when routing ambiguity remains
```

## 214. Intermediate artifact signals

Gate may consume:

```text
test status
schema validity
spec adherence
error novelty
verifier confidence
model history
regression risk
```

## 215. Early stopping

If deterministic Done Contract is already satisfied, no extra “smart” review call is required merely to consume available quota.

---

# Part LIX — Consensus and diversity allocation

## 216. Diversity dimensions

```text
model family
training lineage
provider/backend
prompt strategy
specialist role
verification method
```

## 217. Diverse council only when useful

Spend additional free calls when disagreement information can materially change the decision.

## 218. Deterministic verifier dominates council

Passing tests are stronger than three models saying code “looks correct”.

---

# Part LX — Free capacity valuation

## 219. Expiry-aware value

Free capacity has:

```text
remaining amount
reset/expiry
future expected task demand
capability scarcity
standby importance
```

## 220. Trial expiry

A powerful 90-day trial bucket can be more aggressively used near expiry if it is not reserved for active recovery and no higher-value task is expected.

## 221. Standing versus promotional

The scheduler explicitly distinguishes:

```text
STANDING_RENEWABLE
RECURRING_CREDIT
RECURRING_RATE_QUOTA
PROMOTIONAL
TRIAL
LOCAL
```

---

# Part LXI — Route availability forecast

## 222. QuotaExhaustionForecast

Predict whether the current route can finish the active stage based on:

```text
recent tokens/call
remaining calls/tokens
stage expected turns
provider resets
retry probability
verification reserve
```

## 223. Preemptive handoff

If forecast predicts exhaustion before the next safe checkpoint:

```text
prepare handoff before hard failure
```

rather than waiting for a 429 mid-stage.

## 224. Do not switch unnecessarily

If reset arrives before quota is expected to block progress, stay with current model.

---

# Part LXII — Handoff equivalence tests

## 225. Destination semantic reconstruction

Before mutation authority transfer, ask destination to emit a structured reconstruction of:

```text
goal
constraints
forbidden actions
repo state
current problem
failed hypotheses
verification status
next proposed action
```

## 226. Compare deterministically where possible

Exact constraints/hashes/test IDs require exact equality.

Semantic fields use bounded equivalence evaluation.

## 227. Mismatch

```text
widen packet
→ retry once/boundedly
→ alternate standby
```

No silent continuation.

---

# Part LXIII — Cross-protocol tool state

## 228. Tool call IDs are transport details

Canonical tool operations use AlinaCoder-generated IDs independent of provider tool-call IDs.

## 229. Provider mapping

Maintain:

```text
canonical_tool_call_id ↔ provider_tool_call_id
```

per attempt.

## 230. Failover after tool execution

Destination receives canonical tool result and receipt, not a fake replay of source-provider tool-call syntax.

## 231. Exactly-once effects

Existing CommitEpoch/idempotency/fencing rules prevent destination from re-executing a completed external effect merely because provider conversation state changed.

---

# Part LXIV — Stream interruption recovery

## 232. Partial generation is not committed state

A truncated model stream is an attempt artifact.

## 233. Safe salvage

Only structured, fully parsed sub-artifacts whose boundaries are provably complete may be salvaged.

## 234. Otherwise

Reconstruct from last committed semantic checkpoint on same or fallback route.

---

# Part LXV — Provider response cache awareness

## 235. Cache affinity

Switching can lose provider prompt-cache advantages.

Track:

```text
cache-capable route
prefix stability
observed cache-hit rate
cache lifetime
switch cache penalty
```

## 236. Routing decision

A marginally stronger standby should not replace a healthy current model if expected gain is lower than context-reprocessing/handoff penalty.

## 237. Safety exception

Billing/privacy/corruption failures override cache affinity immediately.

---

# Part LXVI — Dynamic free-provider scorecard

## 238. Score dimensions

Every currently eligible free RouteCell shows:

```text
verified quality lower bound
skill profile
context fit
free quota remaining
reset/expiry
availability
p95 latency
protocol completeness
privacy/use scope
handoff compatibility
failure-domain diversity
source confidence
```

## 239. No single opaque score

A composite rank may exist, but all gate dimensions remain inspectable.

---

# Part LXVII — Autonomous connection UX

## 240. First run

`alinacoder.exe` should be capable of:

```text
detect local Ollama
probe anonymous free gateways
show zero-input routes already usable
identify providers where one-time account authorization would unlock valuable free capacity
```

## 241. Consent prompt quality

When user consent is genuinely required, explain:

```text
provider
what access is requested
whether free quota is recurring/trial
whether provider may use data
whether a payment method exists/is required
what AlinaCoder will store
how to revoke
```

## 242. Minimal interruptions

Do not ask the user to authenticate low-value providers if current free capacity is already sufficient.

## 243. Value-of-auth

Introduce:

```text
ProviderAuthorizationVOI
```

Request user authorization only if expected capability/availability gain justifies interruption.

---

# Part LXVIII — Auto-connect without overpermission

## 244. Scope minimization

Request only scopes needed for inference/catalog/quota state.

## 245. Billing/admin scope

Do not request billing modification, purchase, subscription-upgrade or payment-method scopes merely to run inference.

## 246. Organization access

If provider returns multiple organizations/workspaces, default selection requires:

```text
explicit saved user choice
or
only one viable zero-spend workspace
```

Never choose a paid organization because it has higher limits.

---

# Part LXIX — Zero-spend canary

## 247. Before first real task on a newly authorized provider

Run a minimal safe canary and verify:

```text
request succeeds
expected model responds
quota/usage state moves as predicted
no monetary balance decreases
no paid tier transition occurs
```

where provider telemetry permits.

## 248. Inability to observe spend

If a route can reach paid funds and AlinaCoder cannot observe/enforce which bucket will be charged:

```text
BLOCK
```

---

# Part LXX — Current free model discovery priority

## 249. Standing high-value discovery order

At startup/requalification, prioritize current live evidence from:

```text
local Ollama
Kilo free catalog
OpenRouter free catalog
Groq Free
Gemini Free
GitHub Models free usage
SambaNova Free
Requesty free catalog if qualified
Cloudflare Workers Free eligible models
Vercel AI Gateway free models
LLM7 free tier if still qualified
other current provider-specific recurring free tiers
```

Then evaluate temporary/promotional buckets.

## 250. This is an order of discovery, not a fixed model ranking

The actual winner is learned from live task-conditioned evidence.

---

# Part LXXI — Provider churn

## 251. Free-model churn is expected

Zero-price models may appear/disappear with hours/days of notice.

## 252. No manual code release required

If a provider uses a compatible schema and already has a validated adapter, catalog changes should be ingestible without rebuilding `alinacoder.exe`.

## 253. Policy schema

Use data-driven model metadata and policy configuration rather than one `if model == ...` branch per model.

---

# Part LXXII — Unknown endpoint quarantine

## 254. New endpoint from search result

Status:

```text
QUARANTINED_DISCOVERY
```

## 255. Must prove

```text
first-party ownership or legitimate service
HTTPS/TLS validity
auth mechanism
terms/use scope
pricing/funding
model identity
protocol behavior
```

before any real project data is sent.

---

# Part LXXIII — Secret-aware payload classification

## 256. Before remote inference

Run existing/new secret scanning over selected payload.

## 257. Redaction classes

```text
CAN_REDACT
MUST_NOT_SEND
SAFE_PUBLIC
USER_APPROVED_SENSITIVE
```

## 258. Model quality never overrides secret policy

If strongest free model has weak privacy terms, choose another route or local model.

---

# Part LXXIV — Provider-specific data-policy routing

## 259. Data policy becomes a route constraint

Example categories:

```text
NO_TRAINING_ZERO_RETENTION
NO_TRAINING_LIMITED_RETENTION
TRAINING_OPT_OUT
TRAINING_ALLOWED_FREE_TIER
TRIAL_DATA_COLLECTION
UNKNOWN
```

## 260. Confidential project defaults

Prefer strongest eligible route in the safest data class that satisfies required capability.

---

# Part LXXV — Multi-provider model deduplication

## 261. LogicalModelFingerprint

Include where known:

```text
canonical family
revision/date
quantization/serving variant
context config
tool template
provider modifications
```

## 262. Same weights, different serving behavior

Keep endpoint-specific quality evidence separate even if logical weights are same.

---

# Part LXXVI — Model release detector

## 263. FrontierReleaseDetector

Monitor authoritative catalog diffs rather than social hype alone.

## 264. Trigger

A new high-capability model automatically enters challenger pipeline if a legitimate zero-spend RouteCell exists.

## 265. No blind promotion

“Newer” does not equal “better”.

---

# Part LXXVII — Benchmark integrity

## 266. Hidden cases

Public repository contains benchmark framework and categories, not secret hidden cases.

## 267. Temporal freshness

Continuously add fresh locally generated or real-task-derived evaluation cases to reduce benchmark gaming.

## 268. Real task signal

Actual repository Done Contracts remain the highest-value evidence.

---

# Part LXXVIII — Exploration budget policy

## 269. Budget classes

```text
USER_TASK
RECOVERY_RESERVE
VERIFICATION_RESERVE
ROUTING_EXPLORATION
PROVIDER_CANARY
```

## 270. Priority

```text
USER_TASK > RECOVERY > VERIFICATION > safety canary > exploration
```

unless an urgent safety requalification blocks all work.

---

# Part LXXIX — Provider quota reset scheduler

## 271. Reset-aware probes

After a known daily reset, refresh only providers likely to become useful.

## 272. Reset jitter

Do not stampede provider endpoints exactly at reset time; add bounded jitter to non-urgent housekeeping.

---

# Part LXXX — Supabase optional control/evidence plane v3

## 273. Local remains canonical

Single-machine AlinaCoder must work fully without Supabase.

## 274. Optional queues

Current Supabase PGMQ documentation supports durable queue messages with visibility timeouts, retries and archival.

If cloud evidence workers are enabled, use distinct queues such as:

```text
provider_auth_recheck
provider_catalog_refresh
provider_terms_diff
free_quota_refresh
pricing_recheck
semantic_canary
protocol_canary
champion_challenger_eval
handoff_pair_eval
```

## 275. FIFO truth

PGMQ is FIFO without native priority levels.

Priority remains in AlinaCoder's scheduler via separate queues/admission order.

## 276. Visibility timeout

A crashed worker's job becomes visible for retry after visibility timeout.

## 277. Archive

Archive completed discovery/probe jobs for audit/replay.

## 278. Supabase Vault

Current Supabase docs support encrypted-at-rest Vault secrets.

If optional cloud workers are explicitly enabled, Vault can hold worker-required secrets under least privilege.

Local desktop credentials must not be uploaded merely because Supabase is available.

## 279. Cron

`pg_cron` + `pg_net` may schedule non-urgent provider evidence refreshes when optional cloud mode is configured.

---

# Part LXXXI — Acceptance: provider auto-connection

## 280. Anonymous Kilo route

1. Kilo live catalog exposes an exact `:free` model.
2. Task payload is non-sensitive under current data policy.
3. No auth required.
4. Preflight and canary pass.
5. Route can become eligible without user setup.

## 281. OpenRouter PKCE

1. Valuable free routes exist but user has no credential.
2. Authorization VOI is high.
3. AlinaCoder opens official OpenRouter PKCE URL.
4. User approves once.
5. Authorization code exchanged through official endpoint.
6. User-controlled key stored in OS-protected secret store.
7. Funding/free-route gates remain separate.

## 282. Auth refresh

1. Provider access token expires.
2. Refresh protocol is officially supported.
3. Single-flight refresh succeeds.
4. Tasks resume without user intervention.
5. No context state is lost.

## 283. Auth cannot refresh

1. Credential expires and no supported refresh exists.
2. Route becomes unavailable.
3. Standby receives canonical continuation packet.
4. AlinaCoder continues elsewhere.
5. No browser token scraping occurs.

---

# Part LXXXII — Acceptance: strongest free model

## 284. New powerful free model appears

1. Live catalog diff detects model.
2. Pricing/funding/use-scope proof passes.
3. Challenger canaries pass.
4. Hidden coding eval outperforms current champion with enough confidence.
5. Context/tool compatibility passes.
6. Handoff compatibility tested.
7. Model promoted for matching skills.

## 285. New model has impressive name only

1. Model called “Ultra”.
2. No reliable performance evidence.
3. It stays challenger.
4. No global promotion.

## 286. Nominally strongest cannot fit context

1. Model A has best generic benchmark.
2. Required repo context exceeds safe capacity.
3. Model B safely fits context and meets capability floor.
4. B is selected.

---

# Part LXXXIII — Acceptance: provider-level free trap

## 287. Cloudflare frontier model

1. Account has 10k free Neurons/day.
2. Requested GLM/Kimi/DeepSeek frontier ID requires paid method/current paid credits.
3. ModelEligibilityMatrix marks route ineligible.
4. Free provider allowance does not override model-level rule.

## 288. Free model on same provider

1. Another exact Cloudflare model is allowed under Workers Free allocation.
2. Capacity remains.
3. No paid overflow possible on Workers Free.
4. Route may be eligible.

---

# Part LXXXIV — Acceptance: temporary quota

## 289. Alibaba trial

1. Eligible model has 90-day free quota.
2. Free Quota Only is enabled and verified active.
3. Route is marked TEMPORARY.
4. Scheduler may use it while valid.
5. After expiry it disappears automatically.

## 290. Tencent postpaid disabled

1. Promotional tokens remain.
2. Postpaid disabled.
3. Exhaustion is documented to stop service.
4. Route can be eligible until expiry/exhaustion.

## 291. Postpaid enabled

1. Same trial account enables postpaid.
2. Funding proof invalidates.
3. Autonomous route is blocked before next request.

---

# Part LXXXV — Acceptance: seamless protocol switch

## 292. OpenAI-compatible → Anthropic-compatible

1. Source model fails.
2. Destination uses different provider protocol.
3. CanonicalInferenceEnvelope remains unchanged.
4. ProtocolNormalizer rebuilds request.
5. Tool IDs are remapped.
6. HandoffRoundTrip passes.
7. CommitEpoch advances.
8. Destination continues from same operational meaning.

## 293. Destination lacks tool support

1. Strong free model exists.
2. Active stage needs function calls.
3. CompatibilityPreflight fails tool gate.
4. Model is skipped for this stage.

---

# Part LXXXVI — Acceptance: failover storm

## 294. Provider-wide outage

1. Ten tasks lose same provider.
2. Standby free quota is scarce.
3. FailoverStormGuard prevents simultaneous stampede.
4. User-blocking/high-risk tasks get reserved capacity.
5. Shadow audits stop.
6. Circuit breaker probes provider recovery separately.

---

# Part LXXXVII — Acceptance: consensus blind spot

## 295. Three models agree

1. Three candidates emit same patch.
2. They share same underlying model family or unsupported assumption.
3. Consensus does not authorize commit.
4. Deterministic tests fail.
5. Patch rejected.

## 296. High-risk no deterministic oracle

1. Models agree.
2. Security implication high.
3. Independent diverse reviewer/evidence is required before action.

---

# Part LXXXVIII — Acceptance: retrieval utility

## 297. Similar-looking old bug

1. Memory retrieval finds old ExperienceCard.
2. Dependency versions differ materially.
3. RetrievalUtilityGate rejects injection.
4. Router may still use its metadata as a weak routing prior.

## 298. Exact recurring signature

1. Same error signature/environment recurs.
2. Previous resolution verified and fresh.
3. Experience is injected.
4. Downstream outcome measured.

---

# Part LXXXIX — Metrics

## 299. Discovery metrics

```text
live_free_route_count
unique_logical_free_models
independent_free_failure_domains
new_candidate_detection_latency
stale_catalog_rate
source_conflict_rate
```

## 300. Auth metrics

```text
auto_reconnect_success_rate
user_consent_frequency
refresh_failure_rate
auth_scope_excess_rate
credential_leak_count
```

Hard target:

```text
credential_leak_count = 0
```

## 301. Price/funding metrics

```text
paid_route_admission_count
unexpected_paid_spend
conditional_price_misclassification
free_bucket_overrun
```

Hard targets:

```text
unexpected_paid_spend = €0.00
paid_route_admission_count = 0
```

## 302. Quality metrics

```text
champion_replacement_precision
challenger_false_promotion_rate
skill_conditioned_terminal_success
routing_regret
OOD_success
```

## 303. Continuity metrics

Existing CPR/CLO/CRF/CRR/TSPR/MSPR/HCO remain, plus:

```text
protocol_switch_success_rate
context_fit_failure_rate
tool_state_replay_error_rate
warm_standby_recovery_latency
```

## 304. Operational metrics

```text
provider_failover_storm_events
retry_amplification_factor
circuit_breaker_false_open_rate
quota_exhaustion_forecast_error
```

---

# Part XC — Conceptual modules

## 305. Provider fabric

```text
src/alinacoder/provider_fabric/
  auth_broker.py
  auth_state.py
  credential_store.py
  auth_channel_entitlement.py
  connection_ladder.py
  live_free_oracle.py
  source_authority.py
  price_function.py
  model_eligibility.py
  free_pool_union.py
  terms_snapshot.py
  catalog_refresh.py
  model_identity.py
  provider_health.py
  retry_budget.py
  failover_storm_guard.py
```

## 306. Protocol layer

```text
src/alinacoder/protocol/
  canonical_envelope.py
  normalizer.py
  quirks.py
  compatibility_preflight.py
  context_fit.py
  tool_state.py
  continuation_bundle.py
  warm_standby.py
```

## 307. Routing intelligence

```text
src/alinacoder/routing/
  strongest_useful.py
  champion_challenger.py
  boundary_case_miner.py
  escalation_gate.py
  consensus_blindspot.py
  retrieval_utility.py
  counterfactual_audit.py
  release_detector.py
```

## 308. Provider adapters

```text
src/alinacoder/providers/
  kilo.py
  openrouter.py
  groq.py
  github_models.py
  gemini.py
  sambanova.py
  cloudflare_workers_ai.py
  requesty.py
  mistral.py
  alibaba_modelstudio.py
  qwencloud.py
  tencent_tokenhub.py
  zai.py
  opencode_zen.py
  pollinations.py
  modelscope.py
  nvidia_nim.py
```

These names are conceptual and may change during implementation without weakening the normative behavior.

---

# Part XCI — Recommended implementation sequence

## 309. Phase P1 — canonical protocol substrate

Before multiplying providers, implement:

```text
CanonicalInferenceEnvelope
ProviderProtocolNormalizer
ProviderProtocolQuirkRegistry
CompatibilityPreflight
ContextFitPlanner
```

## 310. Phase P2 — credential/auth substrate

Implement:

```text
CredentialHandle
Windows protected credential store
ProviderAuthBroker
ProviderConnectionLadder
CredentialRefreshSingleFlight
AuthChannelEntitlement
```

## 311. Phase P3 — live free oracle

Implement:

```text
CatalogSourceAuthority
LiveFreeModelOracle
ConditionalPriceFunction
ModelEligibilityMatrix
TermsSnapshot
```

## 312. Phase P4 — safe first provider breadth

Prioritize mature/valuable adapters with current live evidence:

```text
Kilo
OpenRouter
Groq
Gemini
GitHub Models
SambaNova
Cloudflare Workers AI
Vercel AI Gateway
LLM7
```

## 313. Phase P5 — routing intelligence

Implement:

```text
FreePoolUnionRouter
StrongestUsefulModelPolicy
ChampionChallengerController
RoutingBoundaryCaseMiner
WorkflowEscalationGate
```

## 314. Phase P6 — seamless switching

Implement:

```text
StatefulContinuationBundleV2
WarmStandbySnapshot
cross-protocol tool-state mapping
handoff equivalence tests
stream interruption recovery
```

while retaining CommitEpoch/RouteOwnershipFence from prior amendments.

## 315. Phase P7 — temporary/promotional providers

Add only after standing backbone is safe:

```text
Alibaba/QwenCloud
Tencent TokenHub
Z.AI trial
OpenCode Zen guarded free routes
Pollinations exact-zero routes
Hugging Face credit
```

## 316. Phase P8 — provisional discovery providers

ModelScope and other discovered providers remain quarantined until first-party use-scope evidence is sufficient.

## 317. Phase P9 — optional Supabase plane

Add queues/Vault/cloud refresh only after local behavior is complete.

---

# Part XCII — Research basis added by this pass

## 318. Research date

Research performed 2026-09-04 using Exa, Parallel Search, Supabase documentation and current first-party/provider documentation where available.

## 319. OpenRouter OAuth PKCE

Reviewed:

```text
https://openrouter.ai/docs/guides/overview/auth/oauth
```

Applied lessons:

```text
PKCE S256
localhost callback support
headless authorization-code mode
user-controlled key issuance
official browser authorization instead of browser scraping
```

## 320. OpenRouter free routing/catalog

Reviewed current OpenRouter free-router/models/rate-limit documentation.

Applied lessons:

```text
dynamic free model pool
feature filtering
pricing metadata
conditional/override-aware zero-price proof
virtual route identity handling
```

## 321. Kilo Gateway

Reviewed:

```text
https://kilo.ai/docs/gateway/models-and-providers
https://kilo.ai/docs/gateway/authentication
https://kilo.ai/docs/getting-started/using-kilo-for-free
```

Applied lessons:

```text
unauthenticated live catalog
anonymous free inference
current 200 req/hour/IP free limit
dynamic Auto Free mapping
provider/model data-policy distinctions
BYOK no-fallback semantics
```

## 322. Groq

Reviewed:

```text
https://console.groq.com/docs/rate-limits
https://console.groq.com/docs/models
https://console.groq.com/docs/billing-faqs
https://console.groq.com/docs/prompt-caching
```

Applied lessons:

```text
organization-scoped quotas
current recurring Free Plan model set
live model API
rate-limit headers
free/developer account distinction
cache-affinity routing signal
```

## 323. Cloudflare Workers AI

Reviewed:

```text
https://developers.cloudflare.com/workers-ai/platform/pricing/
```

Applied lessons:

```text
10k Neurons/day Workers Free allowance
hard failure above Workers Free allowance
model-level paid-method requirements
provider-level free != model-level free
```

## 324. GitHub Models

Reviewed current first-party GitHub Models prototyping/billing/rate-limit documentation.

Applied lessons:

```text
rate-limited free public-preview usage
explicit paid-use enablement
free-exhaustion hard-stop opportunity
per-model/tier limits
```

## 325. SambaNova

Reviewed:

```text
https://docs.sambanova.ai/docs/en/models/rate-limits
```

Applied lessons:

```text
Free Tier when no payment method linked
model-specific free limits
response rate-limit headers
```

## 326. Alibaba Cloud Model Studio / QwenCloud

Reviewed:

```text
https://www.alibabacloud.com/help/en/model-studio/new-free-quota
https://docs.qwencloud.com/resources/free-quota
```

Applied lessons:

```text
model-specific temporary free quotas
Free Quota Only hard-stop
quota-display/switch synchronization risk
auth-channel-specific free quota
postpaid contamination risk
```

## 327. Tencent TokenHub

Reviewed current Tencent Cloud promotional model-gallery documentation.

Applied lessons:

```text
time-limited model-specific free packages
frontier/open-model trial diversity
postpaid disabled → stop
postpaid enabled → charge
```

## 328. Z.AI / ZCode

Reviewed current Z.AI/ZCode documentation.

Applied lessons:

```text
current GLM flagship discovery
short-lived free trial vs standing entitlement
supported account binding distinct from free entitlement
coding-plan use-scope restrictions
```

## 329. OpenCode Zen

Reviewed:

```text
https://opencode.ai/docs/zen/
```

Applied lessons:

```text
limited-time exact-zero model IDs
auto-reload/payment risk
provider-specific data-use exceptions
exact-model allowlisting
```

## 330. Pollinations

Reviewed:

```text
https://gen.pollinations.ai/docs
```

Applied lessons:

```text
public live model catalogs
OpenAI-compatible API
App Key OAuth/device-flow authorization
scoped user credential issuance
auth convenience != zero price
```

## 331. Supabase

Reviewed current docs for:

```text
PGMQ
Queues
visibility timeout/retry
archival
Vault
pg_cron + pg_net scheduling
```

Applied only as optional control/evidence plane; local execution remains independent.

## 332. Agent-as-a-Router / ACRouter

Source:

```text
https://arxiv.org/html/2606.22902v2
```

Applied principle:

```text
Context → Action → execution-grounded Feedback → updated Context
```

with online routing regret and OOD evidence.

## 333. MTRouter

Source:

```text
https://aclanthology.org/2026.acl-long.2045.pdf
```

Applied principles:

```text
multi-turn history-model utility
selective rather than reactive switching
transient-error recovery
cache/switch overhead
emergent specialization
```

## 334. Drift-Aware Sparse Routing

Source:

```text
https://arxiv.org/abs/2609.00662
```

Applied principles:

```text
rolling evidence windows
shared resource budgets
shadow audits
hard meters
nonstationary routing
```

## 335. LLM-as-Scheduler

Source:

```text
https://aclanthology.org/2026.acl-long.581.pdf
```

Applied principle:

```text
cheap gate + strong scheduler + early exit/test/refine/reroute
```

leading to `WorkflowEscalationGate`.

## 336. ACAR

Source reviewed:

```text
arXiv:2602.21231
```

Important negative results adopted:

```text
agreement can be confidently wrong
naive retrieval can reduce accuracy
proxy attribution can be weak
```

leading to:

```text
ConsensusBlindSpotGuard
RetrievalUtilityGate
CounterfactualRoutingAudit
```

## 337. CASTER

Source reviewed:

```text
arXiv:2601.19793
```

Applied principle:

```text
learn from high-value routing boundary cases and failures rather than indiscriminate random exploration
```

leading to `RoutingBoundaryCaseMiner`.

## 338. Routed Graph Handoff / AdaptOrch / Semantic Router

Prior research remains normative for adaptive handoff encoding, topology routing and provider-neutral capability routing; this amendment operationalizes those ideas through the canonical protocol/provider fabric.

---

# Part XCIII — Canonical autonomous provider loop v6

## 339. Loop

```text
Receive user task
→ repair/revalidate IntentContract
→ classify data sensitivity
→ update ExecutionEvidenceGraph
→ infer TaskRequirementVector + SkillBundle
→ construct WorkGraph
→ WorkflowEscalationGate
→ if meaningful reasoning required: refresh LiveFreeModelOracle as needed
→ discover standing + temporary free candidates
→ CatalogSourceAuthority resolves evidence
→ ProviderTermsSnapshot gate
→ ProviderAuthBroker determines legal connection channel
→ AuthChannelEntitlement
→ ConditionalPriceFunction / FundingSourceProof
→ ModelEligibilityMatrix
→ ProviderHealthVector
→ deduplicate via LogicalModelFingerprint + ProviderDependencyGraph
→ build FreePoolUnion
→ ContextFitPlanner
→ CompatibilityPreflight
→ ChampionChallenger evidence / StrongestUsefulModelPolicy
→ SharedQuotaKnapsack + reservations
→ choose primary + RecoveryPair
→ prepare WarmStandbySnapshot
→ create IntelligenceLease + CommitEpoch
→ build CanonicalInferenceEnvelope
→ ProviderProtocolNormalizer projects request
→ execute
→ normalize response
→ deterministic evidence/tools/tests
→ on transient error: SameRouteRecoveryProbe
→ on provider/auth/quota hazard: revoke route authority and advance CommitEpoch
→ reconstruct StatefulContinuationBundleV2
→ destination CompatibilityPreflight + HandoffRoundTrip
→ ProgressiveTakeover
→ continue with canonical tool/evidence state
→ ResourceFrontier/PlanDependencyFence before mutation
→ deterministic Done Contract
→ record terminal routing outcome
→ RoutingBoundaryCaseMiner / Counterfactual audit if valuable
→ update champion/skill/continuity/health evidence
→ refresh warm standby at checkpoint
→ release quota reservation
```

---

# Part XCIV — Non-negotiable invariants

## 340. AlinaCoder must never

- equate a provider Free plan with all models being free;
- equate OAuth/account login with free entitlement;
- equate API compatibility with semantic/protocol equivalence;
- scrape browser cookies, tokens, consumer chat pages or hidden sessions to automate LLM access;
- bypass a provider's officially supported authentication path;
- create accounts, keys, identities, IPs or network routes to evade quotas;
- select a model because of its marketing name or parameter count alone;
- trust a third-party free-provider directory as execution authorization;
- use a route with an unknown conditional pricing branch;
- use a paid-gated frontier model merely because its provider has a free allowance for other models;
- consume user credits, wallet balances, subscriptions or postpaid funds under the autonomous €0 policy;
- automatically enable payment, postpaid, subscriptions, credit purchase or auto-reload;
- upload local credentials to optional cloud storage without an explicit architectural need and approved configuration;
- send confidential code to anonymous/trial/training-allowed routes when privacy policy does not permit it;
- dump raw provider transcripts as the source of truth for cross-model continuation;
- replay a completed tool side effect during failover;
- let an old provider's late response commit after CommitEpoch advances;
- switch models on every recoverable transient error;
- stay on an unhealthy route merely to preserve prompt-cache affinity;
- promote a new model after a single lucky benchmark;
- let unanimous LLM agreement replace deterministic tests;
- inject retrieved memories merely because they are semantically similar;
- spend exploration quota while user/recovery capacity is starved;
- assume a promotional/free-trial route will remain available in future sessions;
- weaken any prior safety, IntentContract, Done Contract, rollback, verification or zero-spend invariant.

## 341. Final target behavior

```text
Launch alinacoder.exe
→ local models discovered automatically
→ anonymous legitimate free gateways discovered automatically
→ current free model catalogs queried live
→ powerful new free models detected without an AlinaCoder release
→ provider/account/auth-channel entitlements resolved exactly
→ zero-spend and data-use policy proven before context leaves the machine
→ one-time official OAuth/device authorization requested only when it adds real value
→ credentials stored securely and refreshed automatically
→ all currently legitimate zero-cost models merged into one deduplicated intelligence pool
→ strongest useful model selected for the exact coding stage
→ new brains automatically challenged against the current champion
→ scarce free frontier quotas reserved intelligently
→ compatible independent standby prepared without wasting inference
→ provider-specific protocol differences normalized behind one canonical state
→ model works against current IntentContract/repo/evidence
→ tests and tools create execution-grounded feedback
→ temporary error repaired on same model when useful
→ quota/provider/auth/model failure triggers fenced takeover
→ destination reconstructs exact operational state and proves it understands it
→ tool/effect state is preserved without duplicate actions
→ previous route loses commit authority permanently for that epoch
→ task continues as if the intelligence engine changed underneath one coherent AlinaCoder
→ verified outcome updates routing knowledge
→ degraded/paid/unsafe routes automatically disappear
→ better newly free routes can automatically become champion
→ autonomous paid inference spend remains exactly €0
```

The architectural destination is:

> **AlinaCoder is not coupled to Ollama, one API, one gateway, one model family or one vendor. It operates a live, authenticated, zero-spend provider fabric whose canonical state belongs to AlinaCoder itself. Models are replaceable reasoning engines. The system continuously discovers, proves, benchmarks, connects, routes, verifies and safely transfers authority among the strongest currently legitimate engines while preserving one uninterrupted project reality.**
