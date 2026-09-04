# AlinaCoder

AlinaCoder is a Windows-first, Python 3.12+ autonomous coding agent designed to understand large repositories, plan work, edit code, run tests, detect regressions, recover from failures, learn from project history, adapt to the local machine, and work directly on `main` under deterministic safety and verification gates.

## Canonical user experience

The target product is now a single conversational Windows application:

```text
User
  ↓ ordinary French / optional voice
AlinaCoder.exe
  ↓ zero-cost intelligence router
Best verified-free model available
  ↓ governed local tools
Repository / tests / Git / memory
```

The user should normally only need to open `AlinaCoder.exe`, talk to it, and optionally click **Tout arrêter** when finished.

AlinaCoder remains **local-first with Ollama**, but may automatically use external intelligence only when it can prove that the selected route is free under the current account/model state. The canonical monetary policy is:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAID_FALLBACK = false
```

No paid API, credit purchase, billing upgrade or surprise pay-as-you-go fallback may be triggered automatically.

## Current v0.2 normative specification

The consolidated implementation baseline remains:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`

v0.2 was explicitly reopened and extended by approved normative amendments. The current implementation contract is the baseline **plus all later normative v0.2 amendments**, with the newest corrective amendment winning where it explicitly supersedes an earlier assumption.

The latest corrective norm is:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`

It supersedes the earlier assumption that a personal ChatGPT Plus subscription could be treated as an automatic read/write MCP or programmatic model endpoint for AlinaCoder.

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
- provider-neutral zero-cost routing across Ollama and verified-free external tiers when available;
- planned adapters for currently free tiers such as Gemini, Groq, OpenRouter and limited Hugging Face free credits, always capability-probed at runtime rather than assumed forever;
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
- a visible **Tout arrêter** control that stops workers, provider streams, indexers, models, AlinaCoder-managed helpers and Ollama according to the configured all-Ollama shutdown policy;
- shutdown verification before displaying `Tout est arrêté`;
- trajectory learning, procedural skill evolution and guarded meta-harness evolution;
- optional hybrid memory synchronization backends such as Supabase without making cloud storage mandatory;
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

A new message wakes what is needed automatically.

`Tout arrêter` means full runtime shutdown, not merely hiding the window.

## Latest normative amendments

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-chatgpt-mcp-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-zero-cost-desktop-intelligence-corrective-amendment.md`

The zero-cost desktop corrective amendment has precedence for primary UX, ChatGPT Plus integration, cost policy, provider routing, idle resources and full shutdown.

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

New capabilities may continue to extend v0.2 only when explicitly approved as normative amendments; otherwise they should target the next version.
