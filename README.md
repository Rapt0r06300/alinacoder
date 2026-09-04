# AlinaCoder

AlinaCoder is a Windows-first, Python 3.12+ autonomous coding agent designed to understand large repositories, plan work, edit code, run tests, detect regressions, recover from failures, learn from project history, adapt to the local machine, and work directly on `main` under deterministic safety and verification gates.

## Canonical user experience

The target product is a single conversational Windows application:

```text
User
  ↓ ordinary French / optional voice
AlinaCoder.exe
  ↓
Autonomous Zero-Cost Intelligence Fabric
  ↓
Strongest proven free brain(s) for this exact stage
  ↓
Continuity Spine + governed local tools
  ↓
Repository / tests / Git / memory
```

The user should normally only need to open `AlinaCoder.exe`, talk to it, and optionally click **Tout arrêter** when finished.

AlinaCoder remains **local-first with Ollama**, but may automatically use external intelligence only when it can prove immediately before the call that the selected route is free under the current account/model/quota state.

The canonical monetary policy is:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
ALLOW_PAID_FALLBACK = false
```

No paid API, credit purchase, billing upgrade or surprise pay-as-you-go fallback may be triggered automatically.

## Current v0.2 normative specification

The consolidated implementation baseline remains:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`

v0.2 was explicitly reopened and extended by approved normative amendments. The current implementation contract is the baseline **plus all later normative v0.2 amendments**, with the newest relevant amendment winning where it explicitly strengthens or supersedes an affected subsystem.

The current zero-cost/frontier norms are:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-intelligence-mesh-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-autonomous-frontier-routing-seamless-handoff-amendment.md`

The desktop corrective amendment supersedes the earlier assumption that a personal ChatGPT Plus subscription could be treated as an automatic read/write MCP or programmatic model endpoint for AlinaCoder.

The intelligence-mesh amendment establishes a self-updating, zero-cost multi-provider architecture.

The autonomous frontier-routing amendment strengthens that mesh with continuous model discovery, champion/challenger learning, provider failover and a model-independent Continuity Spine so AlinaCoder can switch engines without losing verified project state or user intent.

## Autonomous Zero-Cost Intelligence Fabric

AlinaCoder must not rely on one permanent cloud provider, one gateway, one model family or one global ranking.

It maintains a live registry of currently verified-free local and remote routes, benchmarks them on real AlinaCoder workloads, tracks quota/provider changes, learns champions **per task stage**, and prepares safe fallbacks before critical work.

Current research candidates include, subject to live re-verification:

- local Ollama/open-weight models;
- Google Gemini Free Tier;
- Groq Free Plan, currently including GPT-OSS and Qwen families under free limits;
- SambaNova Cloud Free Tier, currently exposing large-model free access without a linked payment method under strict quotas;
- Mistral Studio Free mode;
- OpenRouter `:free` variants and `openrouter/free`;
- Kilo Gateway `kilo-auto/free` and explicit `:free` routes;
- Z.AI zero-price Flash models;
- Cloudflare Workers AI free daily allocation;
- Ollama Cloud Free starter usage;
- NVIDIA NIM Developer Program endpoints for prototyping/development/testing;
- Cohere free evaluation keys;
- ModelScope API-Inference after official account/quota proof;
- Hugging Face monthly free inference credits;
- other newly discovered gateways/providers only after official zero-cost proof and account-level capability probes.

The list is deliberately dynamic. A provider/model that stops being free is quarantined before another inference request and replaced automatically by another eligible route.

GitHub Models is not an active provider: it was retired on July 30, 2026. Cerebras is not standing zero-cost capacity under its current official policy because its free access is a 30-day credit trial requiring a verified payment method and the documentation explicitly says there is no permanent free tier.

## Intelligence routing principles

AlinaCoder optimizes for **verified task success at exactly zero monetary cost**, not for raw parameter count or marketing rank.

Important rules include:

- external leaderboards/catalog rankings are priors only;
- real repeated mini-tests and project outcomes decide routing;
- the best route is learned separately for intent understanding, repository localization, architecture, patching, debugging, testing, review, research, vision and long-context work;
- new models enter through cost proof → capability probe → canary → probation → champion/challenger evaluation;
- scarce free quotas are reserved for tasks where they add the most measured value;
- multiple providers serving the same checkpoint provide hosting redundancy but not independent cognitive diversity;
- hard tasks may use several genuinely different model families only when their complementarity has been measured;
- dense “ask every model” swarms are forbidden by default;
- multi-model routes must earn a `RouteGainCertificate` before recurring promotion;
- model consensus never outranks repository truth or deterministic verification;
- no hosted gateway may become the only failover path.

## Seamless model switching

“No loss of thread” is implemented by preserving verified state, not by dumping the entire raw conversation into every new model.

A local `ContinuitySpine` stores a versioned `CanonicalSessionState` containing the active `IntentContract`, project/repository identity, HEAD/worktree hashes, accepted decisions, constraints, plan/task DAG, verified evidence, failed hypotheses, current artifacts, pending actions and rollback checkpoint.

Before a model can take over, AlinaCoder performs an atomic handoff:

```text
freeze mutations
→ flush verified state
→ snapshot HEAD/worktree/artifacts
→ select best eligible zero-cost target
→ build direction-aware HandoffEnvelope
→ target ContinuityProof
→ dry next-action verification
→ resume
```

The handoff is direction-aware: escalation from a weak model strips most speculative weak-model trajectory while preserving facts and repository state; downshift from a strong model preserves more accepted high-quality planning guidance. Partial or malformed streamed output is never admitted as canonical state or applied as a patch.

Provider-native session IDs, prompt caches or KV caches may accelerate continuation, but AlinaCoder must always be able to resume on a completely different provider from its portable canonical state.

## Reliability and failover

AlinaCoder distinguishes:

```text
Hosting failover
= same model lineage, different eligible provider

Cognitive failover
= different model family chosen for the current task
```

Each route has typed health, quota and failure state. Circuit breakers, exponential backoff with jitter, provider reset headers, context-window prechecks and hot-standby fallback plans prevent a `429`, timeout, model retirement or gateway outage from becoming project-state corruption.

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
- automatic detection of newly free/newly stronger models without automatic trust;
- runtime discovery of free model catalogs rather than permanent hard-coded provider assumptions;
- `ModelLineageGraph` and `FailureDomainGraph` so mirrors, cognitive diversity and shared failure domains are not confused;
- task-specific `RoutePosterior` and `ChampionChallengerRegistry` updated from execution-grounded outcomes;
- `ScaffoldGainProfile` so manager/worker, debate or parallel-agent modes are used only on models/tasks where they actually help;
- local `ContinuitySpine`, event-sourced session state, verified shared gists and hierarchical evidence unfolding;
- direction-aware `HandoffEnvelope`, `ContinuityProof` and transactional model switching;
- mid-stream failure isolation and incomplete-generation rejection;
- two-layer same-lineage and cross-lineage failover;
- per-route circuit breakers, quota reset awareness and prepared standby chains;
- strict cost gate: if zero cost cannot be proven, the remote call is refused before inference;
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
- trajectory learning, procedural skill evolution and guarded meta-harness evolution;
- optional Supabase Free synchronization of non-secret routing/benchmark metadata using hybrid lexical/vector retrieval without making cloud storage mandatory;
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

The zero-cost desktop corrective amendment has precedence for primary UX, ChatGPT Plus integration, cost policy, idle resources and full shutdown.

The zero-cost intelligence-mesh amendment has precedence for the base free-provider registry, model eligibility and multi-model collaboration.

The autonomous frontier-routing amendment has precedence for continuous discovery, route promotion/demotion, credential health, quota portfolio management, provider failover, context mobility, model handoff, continuity proofs and mid-stream recovery.

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

New capabilities may continue to extend v0.2 only when explicitly approved as normative amendments; otherwise they should target the next version.
