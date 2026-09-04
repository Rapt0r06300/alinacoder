# AlinaCoder v0.2 — Zero-Cost Intelligence Mesh Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment extends the zero-cost desktop architecture with a heterogeneous, self-measuring **Zero-Cost Intelligence Mesh**.

It is normative together with:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`

This amendment has higher precedence for:

- discovery of free inference providers and models;
- provider/model eligibility;
- free-quota accounting;
- heterogeneous model routing;
- multi-model collaboration;
- model-lineage diversity;
- zero-cost provider onboarding;
- route learning and route certification.

All earlier safety, verification, resource, intent, memory and Git invariants remain in force.

The monetary invariant remains absolute:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAID_FALLBACK = false
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
```

The objective is not to call as many models as possible. The objective is:

> **Extract the greatest verified coding intelligence available at zero additional monetary cost, while preserving privacy, quotas, machine resources, reliability and deterministic evidence.**

---

# Part I — Product Model

## 2. One application, many brains

The canonical daily experience remains:

```text
User
  ↓ ordinary French / optional voice
AlinaCoder.exe
  ↓
ZeroCostIntelligenceMesh
  ├─ local open-weight models
  ├─ renewable free API tiers
  ├─ free model gateways
  ├─ free development/evaluation tiers
  └─ opportunistic zero-price models
       ↓
Orchestrator + Verifier + Memory + deterministic tools
       ↓
Repository / tests / Git / project state
```

The user must not have to manually decide which model or provider should answer each subtask.

AlinaCoder must choose automatically from measured evidence.

## 3. Intelligence modes

The desktop UI exposes three understandable modes:

```text
AUTO_ZERO_COST
MAX_INTELLIGENCE_ZERO_COST
LOCAL_PRIVATE
```

### AUTO_ZERO_COST

Default mode. Optimize verified quality while conserving scarce free quotas and local resources.

### MAX_INTELLIGENCE_ZERO_COST

Use more free test-time compute, more candidate diversity and more verification for difficult work, while still enforcing `MAX_PAID_SPEND_EUR = 0.00`.

### LOCAL_PRIVATE

No repository content, prompt, metadata or derived task context leaves the machine. Only approved local engines may run.

No mode may silently weaken the zero-cost gate.

---

# Part II — Provider Discovery and Eligibility

## 4. FreeProviderRegistry

Provider support must be data-driven rather than hard-coded around a permanent static list.

```text
ProviderDescriptor
- provider_id
- display_name
- adapter_type
- base_url
- auth_requirement
- free_class
- usage_scope
- model_catalog_endpoint
- pricing_or_free_status_source
- quota_probe
- billing_probe
- privacy_class
- terms_source
- account_state
- live_status
- last_verified_at
```

Possible `free_class` values:

```text
LOCAL_UNLIMITED
RENEWABLE_FREE_TIER
FREE_GATEWAY
DEV_ONLY_FREE
FREE_EVALUATION
MICRO_FREE_CREDIT
MODEL_SPECIFIC_ZERO_PRICE
GRANT_BASED
TRIAL_ONLY
PAID
RETIRED
UNPROVEN
```

## 5. Provider lifecycle

Every provider/model route has a lifecycle:

```text
DISCOVERED
→ FREE_STATUS_CHECK
→ VERIFIED_FREE
→ QUARANTINED
→ BENCHMARKING
→ ELIGIBLE
```

Operational states include:

```text
RATE_LIMITED
QUOTA_LOW
QUOTA_EXHAUSTED
DEGRADED
TERMS_CHANGED
PRICE_CHANGED
MODEL_RETIRED
PROVIDER_RETIRED
AUTH_EXPIRED
REVOKED
UNPROVEN
```

A newly discovered model is never promoted directly into critical coding work merely because its catalog says `free`.

## 6. Continuous catalog refresh

Refresh provider/model state:

- at application startup;
- once per day while active;
- after `402`, `403`, `404`, `429` or model-not-found responses;
- when a provider reports a model retirement;
- before using a route whose free proof is stale;
- after authentication/account changes.

Prefer, in order:

1. authenticated provider account/quota endpoints;
2. provider model/pricing APIs;
3. official provider documentation;
4. trusted fallback metadata only for discovery, never for final zero-cost admission.

A blog, leaderboard or third-party catalog is insufficient proof that a request is free.

---

# Part III — Zero-Cost Admission Gate

## 7. ZeroCostAdmissionGate

Every remote inference call must pass this gate immediately before network dispatch.

Required evidence:

```text
provider eligible
AND model eligible
AND account route is non-billable
AND current model price == 0 OR request is covered by proven included free quota
AND paid fallback disabled
AND automatic top-up disabled or impossible
AND remaining free quota is sufficient or safely bounded
AND usage scope permits the intended development task
```

If any condition is unknown:

```text
COST_STATUS = UNPROVEN
→ DO_NOT_SEND
→ choose another verified-free route
→ otherwise use local inference
```

## 8. Billing tripwires

The provider adapter must treat these as hard faults:

```text
HTTP 402
unexpected non-zero model price
auto-upgrade prompt
payment-method-required state
paid-only model substitution
credit purchase requirement
free-tier removal
provider-side silent model alias to paid route
```

On detection:

```text
FREE_STATUS_CHANGED
→ cancel retry chain
→ quarantine affected route
→ refresh provider metadata
→ fall back to another zero-cost route
```

Never retry by selecting a paid sibling model.

## 9. Free usage is also a scarce resource

Money remains fixed at zero, but the scheduler tracks other costs:

```text
quota burn
latency
remote token allowance
provider daily/monthly limits
local GPU/RAM/CPU load
privacy exposure
failure probability
context capacity
```

The strongest scarce free model should not answer trivial deterministic work if a cheaper-in-quota route can solve and verify it reliably.

---

# Part IV — Current Provider Mesh Snapshot

## 10. Verified provider classes as of 2026-09-04

This table is a **research snapshot, not a permanent allowlist**. Runtime admission still requires live verification.

| Provider | Current zero-cost opportunity | Normative classification | Notes |
|---|---|---|---|
| Local Ollama | local inference, no token billing | `LOCAL_UNLIMITED` | canonical offline fallback |
| Google Gemini Developer API | models with official Free Tier | `RENEWABLE_FREE_TIER` | current official pricing explicitly lists free input/output for eligible Flash models; free-tier privacy terms must be respected |
| Groq | Free Plan with model-specific RPM/RPD/TPM/TPD quotas | `RENEWABLE_FREE_TIER` | current Free Plan includes GPT-OSS and Qwen families among others |
| Mistral Studio | Free mode, API enabled by default, no card required | `RENEWABLE_FREE_TIER` | rate/usage limits apply; never enable paid extension |
| OpenRouter | `:free` variants and `openrouter/free` | `FREE_GATEWAY` | live free catalog changes; query key/free-tier state and model metadata |
| Kilo Gateway | free model variants and `kilo-auto/free` | `FREE_GATEWAY` | useful low-friction resilience route; live capability/terms check required |
| Z.AI | explicitly zero-price Flash models | `RENEWABLE_FREE_TIER` / `MODEL_SPECIFIC_ZERO_PRICE` | current official pricing lists GLM-4.7-Flash and GLM-4.5-Flash as free |
| Cloudflare Workers AI | Free plan daily neuron allowance | `RENEWABLE_FREE_TIER` | quota-aware use; larger models consume allowance faster |
| Ollama Cloud | Free plan starter monthly usage for selected starter models | `MICRO_FREE_CREDIT` / `RENEWABLE_FREE_TIER` | only selected starter models; never consume purchased extra credits |
| NVIDIA NIM hosted endpoints | free developer-program prototyping/development access | `DEV_ONLY_FREE` | enforce development/testing scope; production terms differ |
| Cohere | free evaluation/trial keys with monthly request limits | `FREE_EVALUATION` | useful specialist/critic route within evaluation terms |
| Hugging Face Inference Providers | small monthly free credit for free users | `MICRO_FREE_CREDIT` | exhaust free credit then stop; no purchase |
| OpenCode Zen | changing set of free models | `MODEL_SPECIFIC_ZERO_PRICE` | opportunistic; many free offers are temporary |
| Together AI | occasional zero-price individual models | `MODEL_SPECIFIC_ZERO_PRICE` | never assume provider-wide free tier |
| Pollinations | grants/Quest Pollen and possibly zero-price routes | `GRANT_BASED` | disabled unless live account/model state proves no paid balance can be consumed |

## 11. Explicitly excluded or downgraded discoveries

### GitHub Models

GitHub Models was retired on **2026-07-30**. It is:

```text
PROVIDER_RETIRED
```

It must not appear as an active provider merely because older tutorials mention it.

### Cerebras

Current official Cerebras documentation describes a free trial using temporary credits and a verified payment method, not a permanent free tier.

Under the canonical zero-spend/no-surprise-billing product rule it is:

```text
TRIAL_ONLY
→ NOT_CANONICAL
```

### Paid APIs

OpenAI API, Anthropic API and every other non-zero-price route remain unavailable to the canonical mesh unless a future model-specific route is independently and live-proven to be zero-cost.

ChatGPT Plus remains a user-mediated optional consultation surface under the previous corrective amendment; it is not treated as a hidden API entitlement.

## 12. Source-of-truth snapshot

The September 2026 research used current official material including:

- Google Gemini pricing: `https://ai.google.dev/gemini-api/docs/pricing`
- Groq rate limits: `https://console.groq.com/docs/rate-limits`
- Mistral free API mode: `https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key`
- OpenRouter free variants: `https://openrouter.ai/docs/guides/routing/model-variants/free`
- OpenRouter limits: `https://openrouter.ai/docs/api_reference/limits`
- OpenRouter free catalog: `https://openrouter.ai/collections/free-models`
- Z.AI pricing: `https://docs.z.ai/guides/overview/pricing`
- Cloudflare Workers AI pricing: `https://developers.cloudflare.com/workers-ai/platform/pricing/`
- Ollama pricing: `https://ollama.com/pricing`
- Ollama cloud documentation: `https://docs.ollama.com/cloud`
- NVIDIA NIM documentation: `https://docs.api.nvidia.com/nim/docs/run-anywhere`
- Cohere free evaluation-key limits: `https://docs.cohere.com/docs/rate-limits`
- Hugging Face Inference Providers pricing: `https://huggingface.co/docs/inference-providers/pricing`
- Supabase billing/free-plan limits: `https://supabase.com/docs/guides/platform/billing-on-supabase`

These URLs are evidence for the design snapshot only. Runtime behavior must never assume they remain unchanged.

---

# Part V — Local Intelligence Pool

## 13. Local models are first-class brains

Local inference provides:

- unlimited monetary usage;
- privacy;
- deterministic availability;
- low coordination overhead;
- free background routing, summarization and verification capacity.

AlinaCoder should evaluate installed/open candidates rather than pin a single permanent model.

Current useful model families for real-machine benchmarking include, where hardware permits:

```text
gpt-oss-20b
Qwen3-Coder / Qwen3-Coder-Next family
Qwen 3.x reasoning families
GLM lightweight/open families
Nemotron efficient local families
Gemma families
Mistral/Devstral families
other newly discovered open-weight coding/reasoning models
```

The list is illustrative. A model is not selected because its release notes claim superiority.

## 14. Hardware-fit before prestige

A huge model that thrashes system RAM or destroys responsiveness can be worse than a smaller model with clean GPU residency and sufficient context.

Every local candidate must be profiled on the actual machine for:

```text
load success
VRAM peak
RAM peak
CPU load
tokens/sec
time-to-first-token
context-size stability
structured-output reliability
tool-call reliability
crash/OOM rate
quality on mini-benchmarks
```

Existing anti-oscillation and checkpoint-only model-switching rules remain mandatory.

## 15. Multiple local serving adapters

Ollama remains the canonical Windows-first provider, but the architecture may support alternative local serving adapters where measured beneficial:

```text
Ollama
llama.cpp compatible server
LM Studio compatible local server
future proven Windows-compatible local engine
```

Only one engine is needed for a model if another engine provides no measurable gain.

Alternative engines must not create duplicate resident model copies that waste RAM/VRAM.

---

# Part VI — Capability Profiling and FreeBrainBench

## 16. ModelCapabilityProfile

Every eligible model receives a machine/task-specific profile:

```text
ModelCapabilityProfile
- provider_id
- model_id
- model_lineage_fingerprint
- free_proof_timestamp
- context_window
- modalities
- reasoning_modes
- tool_support
- structured_output_support
- French_intent_score
- repo_localization_score
- architecture_score
- code_generation_score
- debugging_score
- test_generation_score
- regression_review_score
- research_synthesis_score
- long_context_score
- instruction_following_score
- abstention_score
- latency_distribution
- failure_rate
- quota_efficiency
- privacy_class
- benchmark_sample_count
- benchmark_dispersion
- last_benchmarked_at
```

## 17. FreeBrainBench

Create a repeatable benchmark suite measuring the work AlinaCoder actually performs.

Task families include:

```text
ordinary/noisy French intent
corrections and negation
repository search and symbol localization
architecture comprehension
small patch generation
multi-file patch planning
root-cause debugging
test generation
discriminating experiment design
regression review
structured JSON/tool output
long-context repository synthesis
research synthesis
honest abstention
failure recovery
```

Use 3–5 repeated trials where quota/resources permit and store:

```text
median
worst case
dispersion
success rate
verification score
latency
quota consumed
resource footprint
```

Hidden holdouts remain outside candidate-visible/public benchmark context.

## 18. Calibration beats marketing

Provider benchmark claims, public leaderboards and model size are priors only.

Canonical model preference comes from:

```text
real AlinaCoder task performance
+ actual machine behavior for local models
+ verified project outcomes
+ hidden/canary evaluation
```

---

# Part VII — Lineage and Real Diversity

## 19. ModelLineageFingerprint

The same underlying model exposed by several gateways must not count as several independent brains.

Track, when known:

```text
base_family
checkpoint_or_version
instruction/reasoning variant
quantization
serving_provider
context adaptation
known derivative lineage
```

For example, GPT-OSS-120B through Groq and GPT-OSS-120B through another gateway are principally the same reasoning lineage even if latency differs.

## 20. Diversity score

When parallel reasoning is useful, optimize for complementary failure modes rather than provider count.

A diversity score may use:

```text
model-family distance
historical disagreement
error correlation
task-specialization difference
training/checkpoint lineage
reasoning topology
provider independence
```

Do not spend three scarce free calls to obtain nearly identical answers from the same checkpoint on three hosts.

---

# Part VIII — Adaptive Routing

## 21. Context → Action → Feedback loop

The router follows an execution-grounded loop:

```text
Context
→ classify subtask and uncertainty
→ shortlist eligible zero-cost models
→ select route
→ execute
→ deterministic verify
→ record Feedback
→ update routing Memory
→ next decision
```

This follows the key lesson from current agent-routing research: routing quality improves when the router sees verified historical outcomes rather than static global rankings.

## 22. Route by stage, not merely by mission

A single task may use different brains for different stages:

```text
intent resolution
repo localization
planning
implementation candidate
debugging
test generation
adversarial review
final synthesis
```

The best generator is not automatically the best debugger or verifier.

## 23. Quota-aware objective

The route objective is:

```text
maximize expected verified quality
subject to:
  monetary_cost == 0
  privacy admissible
  free quota available
  machine resource budget satisfied
  reliability gate satisfied
```

Tie-break using:

```text
lower quota scarcity
lower latency
lower local resource cost
higher reversibility
higher historical reliability
```

## 24. QuotaLedger

Maintain live per-provider/model quota information:

```text
QuotaLedgerEntry
- provider
- model
- requests_remaining_if_known
- tokens_remaining_if_known
- neurons_or_credits_remaining_if_known
- RPM/TPM/RPD/TPD limits
- reset_at
- recent_429_rate
- reserved_hard_task_budget
- scarcity_score
- last_probe_at
```

Reserve scarce high-capability free quotas for tasks where their measured value is highest.

---

# Part IX — Sparse Multi-Brain Collaboration

## 25. Do not call every brain on every task

Dense model swarms waste quota and context.

Use a sparse escalation ladder:

```text
L0 deterministic/local direct path
L1 one measured best model + deterministic verification
L2 specialist + independent verifier
L3 2–4 diverse candidate models
L4 tournament/refinement + discriminating tests
L5 heterogeneous specialist council for genuinely hard/stalled tasks
```

Escalate on evidence such as:

- repeated verification failure;
- material uncertainty;
- conflicting candidate patches;
- architecture-level changes;
- weak-model indicators;
- failure to reproduce;
- regression risk;
- router low confidence.

## 26. Heterogeneous reasoning roles

Available roles include:

```text
Direct Solver
Repository Locator
Architecture Planner
Causal Debugger
Test Designer
Adversarial Reviewer
Alternative Designer
Long-Context Analyst
Researcher
French Intent Resolver
Synthesis Judge
```

Roles are not permanently bound to brands. The router assigns the currently best verified model for that role.

## 27. Explore independently, converge before commit

For hard work:

```text
independent candidates
→ compact evidence-backed digests
→ disagreement analysis
→ discriminating experiment/test
→ candidate ranking/refinement
→ deterministic verification
→ one promoted patch
```

Model consensus is evidence of agreement, not evidence of correctness.

## 28. No blind majority vote

Prefer:

```text
verified tests
reproduction evidence
static analysis
repository invariants
counterexamples
regression probes
```

over vote count.

A minority candidate that passes the decisive experiment must beat a majority candidate that fails it.

---

# Part X — Route Gain Certification

## 29. Ensembles must earn their complexity

Multi-model routing can fail when supposedly different advisors share the same blind spots.

Create:

```text
RouteGainCertificate
- route_or_ensemble_id
- baseline_single_model
- task_family
- evaluation_sample_count
- verified_success_baseline
- verified_success_route
- latency_delta
- quota_delta
- error_correlation
- confidence_interval_or_stability_metric
- status
```

Statuses:

```text
UNCERTIFIED
WATCH
CERTIFIED
REVOKED
```

Only promote recurring multi-brain routes when they demonstrate robust gain over the strongest relevant single-model baseline.

A route is revoked if newer evidence shows redundancy, regression or free-quota inefficiency.

---

# Part XI — Privacy and Remote Data Governance

## 30. DataSensitivityClassifier

Before a remote prompt is constructed, classify relevant content:

```text
PUBLIC
NORMAL_PROJECT
PRIVATE_PROJECT
SECRET
CREDENTIAL
PERSONAL_SENSITIVE
```

`SECRET` and `CREDENTIAL` never leave the machine.

Sensitive values are redacted before any external model call.

## 31. Provider privacy profile

A provider's free tier may have different data-use rules from its paid tier.

Record:

```text
training_use_possible
retention_policy_known
region_known
user_opt_out_available
acceptable_for_private_code
last_terms_reviewed
```

If the active privacy policy forbids sending a class of project content, use local-only inference for that content.

Free inference is not worth leaking secrets.

---

# Part XII — Zero-Friction Onboarding

## 32. "Ajouter les cerveaux gratuits"

`AlinaCoder.exe` must provide a guided screen:

```text
Ajouter les cerveaux gratuits
```

Each provider displays human-readable state:

```text
Disponible sans compte
Compte gratuit requis
Clé gratuite requise
Connecté — quota disponible
Quota faible
Quota épuisé — revient à <date/time>
Usage développement seulement
Offre devenue payante — désactivée
Retiré
```

The normal user must not edit JSON, environment files or terminal commands.

Where a provider requires a free account/key, the wizard may open the official registration/key page and then securely store the credential through Windows facilities.

## 33. Credential safety

Credentials must never be committed.

Prefer Windows Credential Manager / DPAPI-backed storage or an equivalent OS-protected secret mechanism.

Never log full API keys.

Never use a credential to modify billing, purchase credits or upgrade an account.

---

# Part XIII — Supabase Optional Learning Sync

## 34. Local state remains authoritative

SQLite/local files remain the source of truth required for operation.

Supabase may be used only as an optional free synchronization layer for non-secret intelligence metadata such as:

```text
provider capability profiles
benchmark summaries
route outcomes
RouteGainCertificates
non-sensitive experience-card metadata
non-sensitive task embeddings
catalog snapshots
```

## 35. Supabase Free safeguards

The current Supabase Free Plan includes two free projects and a 500 MB database-size limit per project; free projects may pause after low activity.

Therefore:

- a paused/unavailable Supabase project must never block AlinaCoder;
- no automatic Supabase upgrade is permitted;
- sync storage must be bounded/pruned;
- large raw trajectories stay local;
- embeddings should preferably use a local free embedding model;
- the app must tolerate delayed rehydration after a free project pause.

---

# Part XIV — Resource Management

## 36. Cloud intelligence should release local compute

When a suitable verified-free remote model handles reasoning, AlinaCoder should not keep an unnecessary heavy Ollama model resident merely "just in case".

The existing `IdleResourceManager` must coordinate with the router:

```text
remote route active
→ unload unused local heavy model when safe
→ preserve lightweight controller/UI
→ wake local model only when needed
```

## 37. Tout arrêter remains absolute

The existing `Tout arrêter` contract remains unchanged and includes:

```text
cancel provider streams
stop workers
stop background provider refresh jobs
stop indexers
unload local model weights
stop AlinaCoder-owned model daemons according to policy
release GPU/RAM/CPU resources
verify child-process termination
then display "Tout est arrêté"
```

---

# Part XV — Failure and Recovery

## 38. Provider failures are normal operating events

Expected conditions:

```text
429 rate limit
quota exhausted
provider outage
model removed
free tier changed
auth expired
context limit changed
tool support changed
privacy terms changed
```

These are routing events, not reasons to corrupt or abandon a mission.

Recovery:

```text
persist mission state
→ mark route unavailable
→ choose next certified zero-cost route
→ refresh exact context needed
→ continue from safe checkpoint
```

## 39. No retry storms

Use provider-specific cooldowns and exponential backoff.

Do not burn every free provider simultaneously on a transient network error.

---

# Part XVI — Self-Improving Mesh

## 40. Route memory

For every verified attempt record compact metadata:

```text
task fingerprint
stage
provider/model
lineage
prompt/context strategy
result
verification outcome
failure signature
latency
quota consumed
resource use
surprise/prediction delta
```

Future routing retrieves analogous prior attempts.

## 41. Exploration without recklessness

The router should occasionally benchmark promising new free models on safe mini-tests, but production work should favor proven routes.

Use an exploration policy bounded by:

```text
zero monetary cost
quota budget
resource budget
non-secret benchmark inputs
safe checkpoints
```

## 42. Provider retirement resilience

The architecture must assume providers and free models will disappear.

A retired provider should require:

```text
registry update
→ capability-profile invalidation
→ reroute
```

not application redesign.

GitHub Models' July 2026 retirement is a concrete example of why this rule is mandatory.

---

# Part XVII — Acceptance Scenarios

## 43. Mandatory acceptance cases

The implementation is not complete until automated tests cover at least these scenarios:

1. Gemini free route is available and benchmarked; AlinaCoder selects it for a task where it currently leads.
2. Groq quota is exhausted; the task reroutes without any paid fallback.
3. OpenRouter returns a free model whose price later becomes non-zero; the route is quarantined before another billable request.
4. Two providers expose the same GPT-OSS checkpoint; lineage logic does not count them as two independent reasoning families.
5. A diverse three-model ensemble disagrees; a discriminating local test selects the correct minority candidate.
6. A multi-model route consumes far more quota without measurable quality gain; `RouteGainCertificate` refuses certification.
7. Mistral account is in Free mode; AlinaCoder can use it while paid extension remains disabled.
8. Z.AI zero-price Flash model is discoverable; a non-zero-price flagship is rejected.
9. Cloudflare free daily allocation is low; router reserves it for a task where it has measured value.
10. Ollama Cloud starter usage is available; AlinaCoder uses only proven included free allowance and never extra purchased balance.
11. NVIDIA NIM route is marked development-only and is not treated as unrestricted production capacity.
12. Cohere evaluation quota reaches its limit; it is disabled until reset rather than upgraded.
13. Hugging Face monthly free credit is exhausted; no purchased inference follows.
14. GitHub Models appears in stale local metadata; runtime retirement refresh disables it.
15. Cerebras appears in a third-party "free API" list; official billing probe classifies it as trial-only and canonical routing refuses it.
16. Provider metadata cannot prove zero price; request is blocked before network inference.
17. A secret is present in a relevant file; remote prompt redaction/local-only routing prevents exposure.
18. Supabase is paused; local router learning and mission execution continue unaffected.
19. All cloud providers are unavailable; Ollama/local route continues.
20. `Tout arrêter` cancels active remote streams, local inference and owned background workers and verifies resource release.

---

# Part XVIII — Implementation Boundaries

## 44. Suggested modules

Conceptual structure:

```text
src/alinacoder/intelligence_mesh/
  registry.py
  provider_descriptor.py
  free_admission.py
  lifecycle.py
  quota_ledger.py
  capability_profile.py
  lineage.py
  router.py
  route_memory.py
  route_gain.py
  ensemble.py
  privacy.py
  onboarding.py
  refresh.py

src/alinacoder/providers/
  ollama_local.py
  ollama_cloud.py
  gemini_free.py
  groq_free.py
  mistral_free.py
  openrouter_free.py
  kilo_free.py
  zai_free.py
  cloudflare_free.py
  nvidia_nim_dev.py
  cohere_eval.py
  huggingface_free.py
  optional_dynamic.py
```

Provider-specific classes are adapters, not decision-makers. Routing policy belongs to the intelligence mesh.

## 45. Provider plugin contract

A provider adapter should expose a common contract such as:

```text
discover_models()
probe_account()
prove_zero_cost(model)
probe_quota(model)
probe_capabilities(model)
invoke(request)
cancel(request_id)
health()
```

It must never expose a method whose purpose is to buy credits or upgrade billing.

---

# Part XIX — Research Principles Incorporated

## 46. Current research lessons made normative

The architecture incorporates these findings from contemporary agent-routing/orchestration research:

- **Agent-as-a-Router / ACRouter:** verified execution feedback and routing memory matter more than a static model ranking; use Context → Action → Feedback → Context.
- **EvoRoute:** route at subtask granularity and learn from analogous historical executions.
- **RouteMoA:** pre-screen a large model pool and invoke only a sparse high-potential subset.
- **Disagree to Explore, Agree to Commit:** encourage diversity during exploration, but converge deliberately before patch promotion.
- **PerfOrch:** model strengths differ by stage and category; per-stage routing can outperform one fixed model.
- **PoTRE:** reasoning-topology diversity can matter more than homogeneous repeated samples.
- **Zero-Shot Self-Orchestration with Ledger Control:** manager/worker scaffolds help some models and hurt others; benchmark orchestration per model/task rather than assuming it always helps.
- **RouteGuard:** complementary-looking models do not automatically create reliable routing gain; certify gains with held-out evidence.

The permanent AlinaCoder principle is:

> **Use many possible brains, few necessary calls, real diversity, live zero-cost proof, execution-grounded routing and deterministic verification.**

---

# Part XX — Final Invariants

## 47. Non-negotiable rules

1. `AlinaCoder.exe` remains the primary user interface.
2. Zero additional monetary spend is enforced before every remote call.
3. No paid fallback exists in the canonical route graph.
4. Free-provider status is live-probed and expires; it is never assumed forever.
5. Provider count is not intelligence diversity; underlying model lineage matters.
6. The best model is selected per task stage from measured evidence.
7. Scarce free quotas are reserved intelligently rather than burned uniformly.
8. Dense all-model swarms are forbidden by default.
9. Multi-model routes require evidence that they beat the relevant single-model baseline.
10. Consensus never replaces tests, repository truth or deterministic verification.
11. Secrets and credentials stay local.
12. Provider billing settings are never changed automatically.
13. Optional Supabase sync cannot become a runtime dependency or a paid requirement.
14. Local Ollama remains a guaranteed zero-money fallback.
15. Provider/model retirement must degrade gracefully.
16. Existing resource anti-oscillation, intent, context, memory, Done Contract and `main`-only Git rules remain mandatory.
17. `Tout arrêter` must still release AlinaCoder-owned compute resources completely.
18. No provider marketing claim can outrank real mini-tests and verified project outcomes.

The target outcome is not a static collection of free APIs. It is a **self-updating, evidence-driven intelligence marketplace inside AlinaCoder** that continuously finds the strongest legally and technically available zero-cost reasoning route, proves that it remains free, learns where each brain is actually useful, and uses multiple brains only when their diversity measurably improves the final verified code.