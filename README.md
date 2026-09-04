# AlinaCoder

AlinaCoder is a Windows-first, Python 3.12+ autonomous coding agent designed to understand large repositories, plan work, edit code, run tests, detect regressions, recover from failures, learn from project history, adapt to the local machine, and work directly on `main` under deterministic safety and verification gates.

## Canonical user experience

The target product is a single conversational Windows application:

```text
User
  ↓ ordinary French / optional voice
AlinaCoder.exe
  ↓
Frontier Autopilot over Adaptive Zero-Cost Frontier Fabric
  ↓
Strongest proven zero-cost brain/regime that fits this task and next critical stage
  ↓
Task Affinity + Continuity Spine + Standby Capsule + governed local tools
  ↓
Repository / tests / Git / memory
```

The user should normally only need to open `AlinaCoder.exe`, talk to it, and optionally click **Tout arrêter** when finished.

AlinaCoder remains **local-first with Ollama**, but may automatically use external intelligence only when it can prove immediately before the call that the selected route is free under the current account/model/feature/quota state **and that the billing surface cannot silently turn the request into paid usage**.

The canonical monetary policy is:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
ALLOW_PAID_FALLBACK = false
ALLOW_AUTO_RELOAD = false
```

No paid API, credit purchase, wallet reload, billing upgrade or surprise pay-as-you-go fallback may be triggered automatically.

## Current v0.2 normative specification

The consolidated implementation baseline remains:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`

v0.2 was explicitly reopened and extended by approved normative amendments. The current implementation contract is the baseline **plus all later normative v0.2 amendments**, with the newest relevant amendment winning where it explicitly strengthens or supersedes an affected subsystem.

The current zero-cost/frontier norms are:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-routing-seamless-handoff-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-adaptive-frontier-fabric-routing-stability-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-autopilot-control-plane-hardening-amendment.md`

The desktop corrective amendment supersedes the earlier assumption that a personal ChatGPT Plus subscription could be treated as an automatic read/write MCP or programmatic model endpoint for AlinaCoder.

The intelligence-mesh amendment establishes a self-updating, zero-cost multi-provider architecture.

The autonomous frontier-routing amendment establishes continuous model discovery, champion/challenger learning, provider failover and a model-independent Continuity Spine.

The adaptive frontier-fabric amendment adds catalog-independent capability routing, task affinity, anti-thrashing switch logic, terminal outcome learning, per-call cost attestations, provider-capability handshakes and stale-response rejection.

The frontier-autopilot/control-plane amendment adds official-first source retraction, billing-surface hard stops, regime-level routing, capability-versus-knowledge freshness, future-stage lookahead, router prompt-injection resistance, model-identity attestation, continuity SLOs, standby capsules, protected free-quota reserves and chaos-tested failover.

## Frontier Autopilot

AlinaCoder must not rely on one permanent cloud provider, one gateway, one model family, one static benchmark, one static provider list or one global ranking.

It maintains a live evidence graph of currently verified-free local and remote routes, measures what each model is actually good at, separately tracks whether its knowledge is fresh for the current domain, predicts the capabilities required by the current task and likely next critical stage, tracks quotas/health/data policies/billing surfaces, and selects the strongest eligible **model plus computation regime** using conservative execution-grounded evidence.

The core selection idea is now:

```text
Task + IntentContract
  ↓
CurrentStage + FutureStageForecast
  ↓
CapabilityRequirementVector + KnowledgeFreshnessRequirement
  ↓
Live evidence-verified model/provider catalog
  ↓
BillingSurfaceGuard + privacy/license/terms gates
  ↓
ModelCapabilityVector + KnowledgeDomainProfile
  ↓
ComputationRegimeRouter
  ↓
TaskAffinityLease / SwitchUtility
  ↓
Best proven route + prepared standby
```

The router predicts required capabilities rather than hard-coding concrete model IDs, so newly discovered models can enter the pool without retraining the whole router.

## Current zero-cost research candidates

Every item below remains subject to **live official/account re-verification** immediately before autonomous use:

- local Ollama/open-weight models;
- Google Gemini Free Tier — selected model variants only;
- Groq Free Plan — current eligible GPT-OSS/Qwen/open-model capacity under live limits;
- SambaNova Cloud Free Tier — current free-entitlement models under strict quotas;
- Mistral Free mode — evaluation/prototyping usage under account-specific limits;
- OpenRouter `:free` variants and `openrouter/free`;
- Kilo Gateway `kilo-auto/free` and explicit `:free` routes;
- Z.AI zero-price Flash routes such as currently documented GLM-4.7-Flash / GLM-4.5-Flash;
- Cloudflare Workers AI Free daily allocation — only models actually eligible under the Free plan;
- Ollama Cloud Free starter allowance — only current starter models/allowance with paid overflow structurally blocked;
- NVIDIA NIM trial/development endpoints, currently exposing frontier-scale open models such as Kimi K3, DeepSeek V4 Pro and Nemotron 3 Ultra, subject to exact model/license/use-scope proof;
- OpenCode Zen explicit free promotional routes such as current Nemotron free variants, only when account auto-reload/paid billing paths are structurally blocked;
- Weights & Biases Serverless Inference free credits, only while remaining free credit is above the protected reserve and PayGo is disabled;
- Vercel AI Gateway Free-tier subset, only when exact free credits/model state and zero-overage behavior are proven;
- OVHcloud AI Endpoints as a privacy-interesting discovery candidate pending exact route-level zero-cost proof;
- Cohere free evaluation capacity;
- ModelScope API-Inference after official account/quota/use-scope proof;
- Hugging Face monthly free inference credits;
- other newly discovered gateways/providers only after official zero-cost proof and account-level capability probes.

The list is deliberately dynamic. A provider/model that stops being free is quarantined before another inference request and replaced automatically by another eligible route.

GitHub Models is not an active provider: current official GitHub documentation confirms it was fully retired on July 30, 2026. Cerebras is not standing zero-cost capacity under its currently verified official policy: current official documentation describes a payment-method-gated $5 trial expiring after 30 days and explicitly states there is no permanently free tier.

## “Free” is proved at both route and billing surface

A Free plan label or `$0` model row is not enough.

Before every remote inference route, AlinaCoder creates a `CostProofReceipt` and a `BillingSurfaceState` covering the exact account, model variant, endpoint, service tier, feature set, current quota/credit balance, overage behavior, PAYG state and auto-reload state.

The route must prove:

```text
prompt price = 0
completion price = 0
request price = 0
requested optional features = 0
remaining allowance sufficient + reserve margin
no automatic paid overage
no automatic wallet reload
no charged gateway fallback
privacy/use-scope/license compatible
```

Unknown means **do not call**.

This prevents mistakes such as using a paid-only frontier model simply because the provider itself also offers a Free plan, or using a `$0` promotional model through an account whose wallet can automatically reload.

## Intelligence routing principles

AlinaCoder optimizes for **verified terminal task success at exactly zero autonomous monetary cost**, not raw parameter count, marketing rank or the number of models consulted.

Important rules include:

- official/account state outranks third-party directories for price, entitlement, availability and terms;
- stale provider claims are actively retracted through `SourceFreshnessTrustGraph` / `EvidenceRetractionEngine`;
- external leaderboards/catalog rankings are priors only;
- real repeated mini-tests and project outcomes decide routing;
- routing is multidimensional across reasoning, coding, debugging, architecture, tools, context, structured output, vision and conversational fidelity;
- capability and knowledge freshness are tracked separately;
- the router is catalog-independent and does not permanently map prompt classes to hard-coded model IDs;
- new models enter through cost/billing proof → identity/capability handshake → canary → challenger → probation → champion/specialist evaluation;
- the control plane distinguishes the user/policy channel from untrusted repo/web/log/model text;
- model aliases are fingerprinted so a silently changed checkpoint does not inherit old champion evidence;
- scarce free quotas are split into protected production/recovery reserves and bounded exploration/research buckets;
- multiple providers serving the same checkpoint provide hosting redundancy but not independent cognitive diversity;
- hard tasks may use several genuinely different model families only when measured complementarity justifies it;
- `ComputationRegimeRouter` may choose one champion, specialist, planner/executor, research+coder, independent verifier or multi-agent topology based on measured gain;
- dense “ask every model” swarms are forbidden by default;
- model consensus never outranks repository truth or deterministic verification;
- no hosted gateway may become the only failover path.

## Stable routing instead of model thrashing

AlinaCoder distinguishes three routing levels:

```text
Task level
= preferred cognitive lineage / TaskAffinityLease

Stage level
= deliberate model-family or computation-regime change at a safe checkpoint

Call/hosting level
= transparent same-lineage provider failover
```

A cognitive switch is not triggered by every timeout, malformed response or temporary error.

`SwitchUtility` compares the expected terminal gain against:

- handoff tax;
- lost prompt/KV cache locality;
- rehydration risk;
- latency;
- remaining work;
- likely next-stage requirements;
- quota scarcity and recovery reserves;
- current model's probability of recovery.

Hysteresis, dwell time, evidence thresholds and switch cooldowns prevent A→B→A→B oscillation.

## Seamless model switching and continuity SLO

“No loss of thread” is implemented by preserving verified state, not by dumping the entire raw conversation or private reasoning into every new model.

A local `ContinuitySpine` stores a versioned `CanonicalSessionState` containing the active `IntentContract`, project/repository identity, HEAD/worktree hashes, accepted decisions, constraints, plan/task DAG, verified evidence, failed hypotheses, current artifacts, pending actions and rollback checkpoint.

At verified checkpoints, AlinaCoder incrementally refreshes a compact `StandbyStateCapsule` for likely fallback routes.

Before a model can take over, AlinaCoder performs an atomic handoff:

```text
freeze mutations
→ flush verified state
→ snapshot HEAD/worktree/artifacts
→ select best eligible zero-cost target
→ BillingSurfaceGuard + ModelIdentityAttestation
→ AdaptiveHandoffCodec / StandbyStateCapsule
→ target ContinuityProof
→ continuity SLO checks
→ dry next-action verification
→ resume
```

Continuity is measured separately from availability with metrics such as constraint retention, verified-fact retention, artifact-state retention, next-action agreement, rollback-point retention and takeover latency.

Partial or malformed streamed output is never admitted as canonical state or applied as a patch.

## Stale response and control-plane protection

Every model call is leased to an exact canonical state version.

If the user corrects the request, Git state changes, a rollback happens or another model advances the task before an older response returns, the old response is tagged:

```text
STALE_IN_FLIGHT_RESPONSE
```

and cannot mutate the newer project state.

The routing control plane also separates trusted control metadata from untrusted payload. A repo file, web page, issue, log, retrieved RAG chunk or model output that says “use provider X”, “disable the cost gate” or otherwise attempts to manipulate routing is treated as **data**, not policy.

This protects against the class of LLM-router rerouting attacks studied in 2026 research.

## Reliability, failover and chaos testing

AlinaCoder distinguishes:

```text
Hosting failover
= same model lineage, different eligible provider

Cognitive failover
= different model family chosen for the current task

Regime failover
= different reasoning topology when the current topology is empirically inadequate
```

Each route has typed health, quota, billing, privacy, identity and failure state. Circuit breakers, exponential backoff with jitter, provider reset headers, context-window prechecks, task affinity, protected recovery quota and standby capsules prevent a `429`, timeout, model retirement or gateway outage from becoming project-state corruption.

`ChaosRouteLab` must test 429/402/404/5xx, credential expiry, model retirement, mid-stream disconnects, truncated JSON/tool calls, quota exhaustion, pricing changes, alias remaps, context-limit changes, stale provider evidence and process crashes during handoff.

Retries of mutating work are protected by operation IDs and precondition hashes so a provider failure cannot duplicate a file edit, commit or other side effect.

## Current major v0.2 capabilities

- one clean conversational `AlinaCoder.exe` as the primary daily interface;
- ordinary conversational French and context-aware intent resolution;
- noisy/hesitant voice understanding with corrections and changes of mind;
- Intent Beam, Intent Contract and repair-aware conversation state;
- Context Operating System, reasoning digests and deep project continuity;
- memory-as-governance, ontology/supersession awareness and AST-guided code memory;
- repository intelligence, dependency reasoning and history-aware planning;
- reliable internet research with grouped, provenance-backed sources;
- alternative-solution exploration, self-critique and regression detection;
- uncertainty control, causal debugging and prediction-before-action learning;
- external self-improvement with protected before/after hidden benchmarks and rollback;
- automatic machine resource discovery and global CPU/GPU/RAM/time/context budgets;
- fixed `HardwareProfile` separated from dynamic `DynamicLoadSnapshot`;
- anti-oscillation through smoothing, hysteresis, dwell time and cooldown;
- local model selection from repeated real mini-tests on the actual machine;
- model switching only at explicit safe checkpoints;
- weak-model detection, honest uncertainty and verifiability-first task decomposition;
- frontier-style test-time compute, independent candidate rollouts, tournament/refinement and adversarial verification;
- dynamic `FreeProviderRegistry`, `FreeRouteDiscoveryEngine`, `FrontierDriftDetector`, `ZeroCostAdmissionGate` and `QuotaPortfolioManager`;
- `SourceFreshnessTrustGraph` and `EvidenceRetractionEngine` so stale third-party/provider claims lose authority automatically;
- `CostProofReceipt` plus `BillingSurfaceGuard` for exact route/account/feature zero-cost attestation and zero-overage enforcement;
- `FreeAccessClass` distinguishing perpetual free, renewing quota, free credits, promotions, trials and restricted-use routes;
- automatic detection of newly free/newly stronger models without automatic trust;
- runtime discovery of free model catalogs rather than permanent hard-coded provider assumptions;
- catalog-independent `CapabilityRequirementVector`, `ModelCapabilityVector` and `ShortfallMatcher`;
- `CapabilityKnowledgeTwin` separating model capability from factual/domain freshness;
- `FutureStageForecast` and conservative counterfactual route lookahead;
- `ComputationRegimeRouter` selecting the measured best agent topology as well as the best model;
- `ControlPlaneIntegrityGuard` / `RouterPromptInjectionGuard` protecting model-selection policy from untrusted payload;
- `ModelIdentityAttestation` preventing silent alias/checkpoint drift from inheriting stale benchmark evidence;
- `ModelLineageGraph` and `FailureDomainGraph` so mirrors, cognitive diversity and shared failure domains are not confused;
- task-specific `RoutePosterior` and `ChampionChallengerRegistry` updated from execution-grounded outcomes;
- `TaskAffinityLease`, `SwitchUtility`, `SwitchHysteresis` and delayed terminal credit assignment;
- active challenger learning through `RoutingBoundaryMiner` and Value of Information instead of random quota burn;
- `FreeQuotaTreasury` protecting production/recovery reserve from background benchmarks and low-value exploration;
- `ProviderCapabilityHandshake`, `ProtocolAdapter`, `ToolSchemaTranscompiler` and structured-output reliability measurement;
- `ScaffoldGainProfile` so manager/worker, debate or parallel-agent modes are used only on models/tasks where they actually help;
- local `ContinuitySpine`, event-sourced session state, verified shared gists and hierarchical evidence unfolding;
- direction-aware `AdaptiveHandoffCodec`, `StandbyStateCapsule`, `ContinuityProof` and continuity SLOs;
- state-version leases and stale in-flight response rejection;
- mid-stream failure isolation and incomplete-generation rejection;
- two-layer same-lineage and cross-lineage failover plus regime-level recovery;
- per-route circuit breakers, quota reset awareness and prepared standby chains;
- `ChaosRouteLab` for provider/billing/identity/continuity fault injection;
- privacy/data-use and model license/use-scope as hard eligibility dimensions;
- secure provider credentials through OS-backed storage/`CredentialBroker`, never repo/prompts/ordinary telemetry;
- strict cost gate: if zero cost or zero-overage cannot be proven, the remote call is refused before inference;
- no automatic upgrade from a free provider/model to a paid route;
- ChatGPT Plus retained only as an optional **user-mediated consultation bridge** under current personal-account limitations;
- no ChatGPT DOM scraping, cookie reuse, hidden browser automation or private endpoint reverse engineering;
- a dormant future ChatGPT account provider that can activate only if OpenAI later exposes an official, programmatic, subscription-included, zero-extra-cost mechanism;
- exact file/code patch proposals through typed contracts, regardless of reasoning provider;
- stale-patch SHA protection, candidate-first application, local verification and commit to `main` only after the Done Contract passes;
- `IdleResourceManager` to unload heavy models and release GPU/RAM while the lightweight desktop UI remains open;
- `ManagedProcessRegistry` so AlinaCoder can prove which processes it owns;
- a visible **Pause** control;
- a visible **Tout arrêter** control that stops workers, provider streams, background refresh jobs, indexers, models, AlinaCoder-managed helpers and Ollama according to the configured all-Ollama shutdown policy;
- shutdown verification before displaying `Tout est arrêté`;
- trajectory learning, procedural SkillBook evolution and guarded meta-harness evolution;
- optional verifier-backed local-model capability evolution/LoRA experiments behind replay and hidden holdouts;
- optional Supabase Free synchronization of non-secret routing/benchmark metadata using hybrid lexical/vector RRF retrieval without making cloud storage mandatory;
- optional PGMQ-backed durable provider-discovery/canary queues with local SQLite still canonical;
- local-only fallback retained when every external provider is unavailable.

## ChatGPT Plus clarification

A personal ChatGPT Plus subscription is useful to the user but is **not** treated as an API entitlement.

Under the currently verified product/terms state, AlinaCoder may offer:

```text
Demander à mon ChatGPT Plus
```

This prepares the complete consultation packet and opens ChatGPT, but the user performs the send/copy-back step. AlinaCoder then validates the returned advice locally. This remains intentionally user-mediated until OpenAI provides a supported zero-additional-cost programmatic bridge for personal accounts.

## Resource-silent behavior

Keeping the AlinaCoder window open must not keep a large model resident unnecessarily.

After idle periods, AlinaCoder should progressively:

```text
unload model weights
→ release VRAM/RAM
→ stop unnecessary workers/indexers
→ optionally stop the AlinaCoder-owned Ollama daemon
→ leave only the lightweight UI/controller
```

A verified-free cloud route may also allow unnecessary local model weights to be unloaded while a task is running remotely.

A new message wakes only what is needed automatically.

`Tout arrêter` means full runtime shutdown, not merely hiding the window.

## Latest normative amendments

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-chatgpt-mcp-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-routing-seamless-handoff-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-adaptive-frontier-fabric-routing-stability-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-autopilot-control-plane-hardening-amendment.md`

The zero-cost desktop corrective amendment has precedence for primary UX, ChatGPT Plus integration, cost policy, idle resources and full shutdown.

The zero-cost intelligence-mesh amendment has precedence for the base free-provider registry and multi-model collaboration.

The autonomous frontier-routing amendment has precedence for continuous discovery, credential health, quota portfolio management, provider failover, portable state and base model handoff.

The adaptive frontier-fabric amendment has precedence for catalog-independent capability routing, task affinity, switch utility/hysteresis, terminal credit assignment, route cost attestations, provider-capability handshakes, adaptive handoff encoding and stale-response rejection.

The frontier-autopilot/control-plane amendment has precedence for source-freshness retraction, billing-surface safety, free-access classification, capability-versus-knowledge freshness, computation-regime routing, future-stage lookahead, control-plane integrity, model-identity attestation, continuity SLOs/standby capsules, protected quota reserves and chaos-tested failover.

## Design history

Historical design/audit documents remain available for provenance:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.1-design.md`
- `docs/audits/2026-09-04-v0.1-critical-intelligence-audit.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-conversation-and-external-self-improvement-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-research-voice-context-specialists-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-resource-awareness-model-calibration-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-resource-anti-oscillation-checkpoints-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-chatgpt-mcp-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-routing-seamless-handoff-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-adaptive-frontier-fabric-routing-stability-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-autopilot-control-plane-hardening-amendment.md`

New capabilities may continue to extend v0.2 only when explicitly approved as normative amendments; otherwise they should target the next version.
