# AlinaCoder v0.2 — Zero-Cost Desktop Intelligence Corrective Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 CORRECTIVE EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment corrects the previously approved frontier/ChatGPT integration design after verifying the current product limitations of a personal ChatGPT Plus account and after the user made **zero additional monetary cost** a hard requirement.

It is normative together with:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-frontier-chatgpt-mcp-amendment.md`

This corrective amendment has higher precedence for:

- the primary user interface;
- ChatGPT Plus integration;
- frontier-provider selection;
- cloud authentication;
- cost policy;
- automatic provider routing;
- idle resource behavior;
- full application shutdown.

The earlier frontier amendment remains valuable provenance and its provider-neutral ideas remain normative where they do not conflict with this correction. In particular, its candidate-first patching, stale-SHA protection, adversarial verification, test-time compute, model routing, context intelligence, memory, trajectory learning, specialist reasoning and meta-harness concepts remain in force.

The following earlier assumptions are explicitly superseded:

1. ChatGPT must not be the required primary conversation surface.
2. A personal ChatGPT Plus subscription must not be assumed to provide full read/write MCP access.
3. A personal ChatGPT Plus subscription must not be assumed to provide a programmatic model endpoint for `AlinaCoder.exe`.
4. AlinaCoder must not depend on browser scraping, DOM automation, session-cookie extraction, private web endpoints or automatic extraction of ChatGPT output.
5. OpenAI API usage must not be required, because it is billed separately from ChatGPT Plus.
6. The normal user must not need Business, Enterprise, Edu, Pro, Copilot, an additional paid subscription, or paid API credits to use AlinaCoder.

---

# Part I — Non-Negotiable Zero-Cost Contract

## 2. Hard monetary invariant

The default and canonical user policy is:

```text
MAX_PAID_SPEND_EUR = 0.00
ALLOW_PAY_AS_YOU_GO = false
ALLOW_AUTOMATIC_PLAN_UPGRADE = false
ALLOW_AUTOMATIC_CREDIT_PURCHASE = false
ALLOW_PAID_FALLBACK = false
```

This is a hard execution gate, not a preference.

Before any remote inference request, AlinaCoder must establish that the selected route is eligible for zero-cost use under the currently detected provider/account/model state.

If zero cost cannot be established with sufficient confidence:

```text
COST_STATUS = UNPROVEN
→ REFUSE_REMOTE_CALL
→ try another verified-free route
→ otherwise fall back to local Ollama
```

No provider outage, rate limit, weak local model, difficult task, user impatience or frontier score may bypass this rule.

## 3. No surprise billing

AlinaCoder must never:

- add a payment method;
- upgrade a provider account;
- buy credits;
- enable pay-as-you-go;
- select a paid model because a free model is unavailable;
- silently fall through from a free model identifier to a billable model;
- use an OpenAI API key whose billing state would permit paid inference under the zero-cost policy;
- ask the user to pay in order to complete normal operation.

A provider that requires paid usage may remain implemented as a future adapter, but it must stay disabled while `MAX_PAID_SPEND_EUR == 0.00`.

## 4. Free does not mean trusted

A zero-price external provider is still external.

For every free cloud provider AlinaCoder must record:

```text
ProviderCapability
- provider_id
- account_tier
- model_id
- cost_status: VERIFIED_FREE | UNPROVEN | PAID | UNAVAILABLE
- rate_limit_state
- privacy_policy_class
- training_on_submitted_content_if_known
- context_limit
- tool_support
- structured_output_support
- reliability_score
- last_probe_at
- evidence_source
```

If a free tier may use submitted content to improve the provider's products, the setup wizard must say so plainly. Secret scanning and redaction remain mandatory before external transmission.

---

# Part II — AlinaCoder.exe Is the Product

## 5. Primary interaction model

The canonical daily experience becomes:

```text
User
  ↓ ordinary French / text / optional voice
AlinaCoder.exe
  ↓ intent + context + provider router
Best verified zero-cost intelligence available
  ↓ structured proposal
AlinaCoder deterministic execution + verification
  ↓
repository / tests / Git / memory
```

The user should not need to open ChatGPT, a terminal, Ollama, a tunnel, a browser developer page or an MCP configuration file for ordinary work.

The intended daily routine is:

```text
1. Open AlinaCoder.exe.
2. Say or type what you want in normal French.
3. AlinaCoder chooses the best available free reasoning route.
4. AlinaCoder reads the project and performs the work through its governed tools.
5. It verifies before committing to main.
6. Close/stop everything with one visible control when desired.
```

## 6. Desktop window requirements

`AlinaCoder.exe` must provide a clean, nontechnical Windows desktop window containing at minimum:

```text
Conversation
Current project
Current mission / state
Intelligence route in use
Ollama status
External-free-provider status
CPU usage
RAM usage
GPU / VRAM usage
Current activity
Pause
Tout arrêter
```

Advanced technical diagnostics exist behind an expandable panel and must not dominate the default UI.

The conversation window remains usable while heavy inference is asleep.

## 7. Simple status language

Prefer human-readable states such as:

```text
Prêt
Je réfléchis
Je vérifie le projet
Je teste
J'ai besoin d'un autre cerveau gratuit
Quota gratuit épuisé — je passe en local
Mode local
En pause
Tout est arrêté
```

Do not expose raw provider/API jargon unless the user opens diagnostics.

---

# Part III — Zero-Cost Intelligence Router

## 8. Provider-neutral architecture

All reasoning providers implement a common interface:

```text
IntelligenceProvider
- probe()
- list_capabilities()
- estimate_cost_status(request)
- prepare_context(request)
- infer(request)
- stream(request)
- health()
- quota_state()
- cancel()
```

The orchestrator depends on `IntelligenceProvider`, never directly on a provider SDK.

Providers may appear/disappear without changing the rest of AlinaCoder.

## 9. Canonical zero-cost routing order

The router does not blindly use a fixed brand ranking. It chooses from the currently available `VERIFIED_FREE` providers based on measured task performance, remaining free quota, latency, privacy class and reliability.

Initial supported provider classes should include:

```text
OLLAMA_LOCAL
GEMINI_FREE_TIER
GROQ_FREE_TIER
OPENROUTER_FREE
HUGGINGFACE_INCLUDED_FREE_CREDIT
CHATGPT_PLUS_MANUAL_BRIDGE
CHATGPT_ACCOUNT_PROVIDER_FUTURE
```

The list is extensible.

A provider is never considered usable merely because its name appears in the list. Runtime capability and zero-cost eligibility must pass first.

## 10. Ollama local baseline

Ollama is the always-available zero-marginal-cost baseline when installed and compatible with the machine.

AlinaCoder continues to:

- discover hardware automatically;
- benchmark local candidate models on the actual machine;
- select by real task performance, not VRAM alone;
- respect CPU/GPU/RAM/context/time budgets;
- use checkpoint-only model switching;
- decompose tasks when the local model is weak;
- abstain when confidence is insufficient;
- verify claims deterministically.

Local operation must remain functional if every remote provider disappears.

## 11. Gemini Free Tier adapter

As of the design date, official Gemini Developer API documentation exposes a Free Tier for selected models with zero-priced input/output subject to rate limits, including current Flash-family models.

The implementation must not assume today's exact model names forever.

Required behavior:

```text
probe current available models
→ identify models explicitly eligible for free-tier inference
→ run AlinaCoder mini-benchmarks
→ register only verified-free candidates
```

If the free quota is exhausted or the request becomes billable:

```text
DO NOT UPGRADE
DO NOT PAY
→ next provider
```

## 12. Groq Free Plan adapter

As of the design date, Groq documents a Free Plan with explicit request/token rate limits and models including OpenAI GPT-OSS 120B.

AlinaCoder may use it automatically only while the account/model/request path is verified as Free Plan eligible.

HTTP `429` or exhausted free quota means route elsewhere, not upgrade.

## 13. OpenRouter Free adapter

AlinaCoder may support only routes that are explicitly zero-priced, for example provider/model identifiers exposed as free or the documented free-model router when available.

Hard rule:

```text
free route unavailable
≠ paid fallback
```

Any automatic model fallback must preserve `cost_status == VERIFIED_FREE`.

## 14. Hugging Face free-credit adapter

Hugging Face may be used only within currently included no-cost credits and only if AlinaCoder can prevent paid overage.

Because free credits may be small and provider availability changes, this is a tertiary opportunistic route, not a foundational dependency.

## 15. Free-provider tournament

For difficult tasks, if free quota permits, AlinaCoder may ask two or more independent free providers/local models for candidate solutions and use the existing tournament/refinement/verifier architecture.

The routing objective is:

```text
maximize verified task success
subject to:
  monetary_cost == 0
  safety gates pass
  resource budgets pass
  privacy policy permits requested context
```

Consensus is not proof. Every winning candidate still passes local deterministic verification.

---

# Part IV — ChatGPT Plus: Keep It, But Do Not Fake an API

## 16. Verified current limitation

A personal ChatGPT Plus subscription and the OpenAI API are separate products with separate billing.

A personal ChatGPT Plus account must therefore not be treated as an API entitlement.

Current OpenAI consumer terms also prohibit automatic/programmatic extraction of ChatGPT output. Therefore AlinaCoder must not automate the ChatGPT website to harvest responses.

Current personal-account limitations may change. Architecture must be ready for change without depending on it.

## 17. ChatGPT Plus Manual Bridge

ChatGPT Plus remains useful without additional cost through a **user-mediated bridge**.

`AlinaCoder.exe` exposes a button:

```text
Demander à mon ChatGPT Plus
```

When selected, AlinaCoder automatically:

1. builds the smallest high-quality `FrontierConsultationPacket`;
2. removes secrets and irrelevant content;
3. includes the current IntentContract, HEAD SHA, relevant code, failures, tests, decisions and exact question;
4. places the packet in the clipboard and/or creates a temporary share file;
5. opens the normal ChatGPT page in the user's browser;
6. displays one simple instruction: `Envoie ce message à ChatGPT, puis copie sa réponse.`;
7. detects only the user-initiated clipboard copy/paste back into AlinaCoder;
8. parses the returned answer as untrusted advisory evidence;
9. validates any proposed paths, patches and tests locally before use.

AlinaCoder must not read the ChatGPT page or extract its output automatically.

This mode is deliberately semi-automatic because that is the compliant zero-additional-cost boundary today.

## 18. Future official ChatGPT account provider

Keep a dormant adapter:

```text
CHATGPT_ACCOUNT_PROVIDER_FUTURE
```

It may become active only when OpenAI provides an officially supported mechanism that allows a personal account/subscription to supply programmatic reasoning to a local third-party application without separate paid inference.

Activation requires:

```text
official documentation
+ capability probe
+ terms compatibility
+ zero-cost proof
+ integration tests
```

When those conditions become true, AlinaCoder may upgrade from the manual bridge without changing its orchestration architecture.

## 19. Explicitly rejected ChatGPT shortcuts

Do not implement as supported product paths:

- Selenium/Playwright/Chrome automation that sends prompts and scrapes ChatGPT responses;
- DOM observation of ChatGPT answer text;
- accessibility-tree scraping for automatic response extraction;
- browser cookie/session-token reuse;
- private ChatGPT endpoints;
- reverse-engineered web APIs;
- CAPTCHA/rate-limit bypasses;
- a hidden browser used as a fake API.

These paths are brittle and conflict with the zero-cost architecture's requirement to remain supportable and compliant.

---

# Part V — One-Time Setup for Nontechnical Users

## 20. First-run experience

AlinaCoder must work immediately in local mode after installation.

Then it may offer:

```text
Booster gratuitement l'intelligence
```

The wizard explains in ordinary French:

```text
AlinaCoder fonctionne déjà gratuitement sur ton PC.
Tu peux aussi connecter des services qui offrent un quota gratuit.
Aucun paiement ne sera activé par AlinaCoder.
```

Provider setup must be optional.

## 21. Credential setup

For providers requiring a free API token/key, the wizard should reduce setup to the smallest unavoidable user action.

Target experience:

```text
Connecter Gemini gratuit
→ open official provider page
→ user signs in / creates free credential
→ user pastes credential once into AlinaCoder
→ secure local storage
→ free-tier smoke test
→ ready
```

Equivalent flows apply to other free providers.

Credentials must be stored using Windows-protected secret storage such as Windows Credential Manager/DPAPI or an equivalently secure abstraction, never committed to Git or stored in plain text logs.

## 22. No billing setup in the wizard

The wizard must not guide the user through adding a card or enabling billing.

If the provider requires billing for a feature:

```text
Cette option devient payante, je ne l'active pas.
```

Then AlinaCoder offers another free provider or local mode.

---

# Part VI — Resource-Silent Desktop Operation

## 23. Heavy components sleep when unused

Keeping the AlinaCoder window open must not imply keeping a large model resident in VRAM/RAM.

Introduce:

```text
IdleResourceManager
```

It manages:

```text
ACTIVE
COOLING_DOWN
MODEL_UNLOADED
OLLAMA_SLEEPING
UI_ONLY
```

After configurable inactivity:

1. finish or checkpoint any safe atomic work;
2. unload idle local model weights;
3. release VRAM/RAM;
4. stop unnecessary background workers/indexers;
5. optionally stop the AlinaCoder-owned Ollama daemon after a longer idle period;
6. leave only the lightweight UI/controller alive.

A new message wakes required services automatically.

The user should never need to launch Ollama manually.

## 24. Resource ownership

Every process started by AlinaCoder must be registered in a `ManagedProcessRegistry` with:

```text
process_id
role
launch_time
owner=ALINACODER
shutdown_method
grace_period
force_kill_allowed
resource_snapshot
```

This prevents orphan processes and makes full shutdown provable.

Ollama lifecycle policy:

```text
If AlinaCoder launched Ollama:
  AlinaCoder owns and stops it.

If an Ollama process already existed before AlinaCoder:
  record EXTERNAL_OR_PREEXISTING.
```

Because the user explicitly wants the ability to free all Ollama resources, setup includes one persistent preference:

```text
TOUT_ARRETER_STOPS_ALL_OLLAMA = true
```

The default for this user's intended product behavior is `true`. The UI may let advanced users change it later.

---

# Part VII — “Tout arrêter” Means Everything

## 25. FullShutdownController

The main window must contain a clearly visible:

```text
Tout arrêter
```

This is not equivalent to closing/minimizing the window.

Required sequence:

```text
FULL_STOP_REQUESTED
→ reject new missions
→ cancel or safely checkpoint current cancellable work
→ persist durable mission/context/memory state
→ stop provider streams and network requests
→ stop tunnels/helpers if any
→ stop watchers/indexers/worker pools
→ unload Ollama models
→ stop Ollama daemon(s) according to configured ownership policy
→ terminate remaining AlinaCoder child processes
→ release locks/temp resources
→ verify process registry
→ verify no managed heavy worker remains
→ close AlinaCoder UI
```

## 26. Shutdown proof

AlinaCoder must not display `Tout est arrêté` merely because shutdown commands were sent.

Verify at least:

```text
managed worker count == 0
managed model sessions == 0
managed tunnel count == 0
managed background indexers == 0
managed provider streams == 0
Ollama state matches configured stop policy
```

If something remains:

```text
Arrêt incomplet : <human-readable component>
→ retry bounded shutdown
→ offer force termination for an owned process
```

## 27. Pause versus Stop

```text
Pause
```

keeps the UI and lightweight state alive but prevents new heavy work and unloads models opportunistically.

```text
Tout arrêter
```

terminates the complete AlinaCoder runtime and Ollama according to policy.

Closing the window through `X` should by default ask once whether the user wants:

```text
Réduire en arrière-plan
or
Tout arrêter
```

The user's choice may be remembered.

---

# Part VIII — Reliability and Coding Behavior

## 28. External intelligence is advisory, never authoritative

Whether a proposal comes from Gemini, Groq, OpenRouter, ChatGPT Plus manually, Ollama or a future provider:

```text
model output != repository truth
```

Mandatory candidate path remains:

```text
intent revalidation
→ evidence retrieval
→ proposal
→ scope validation
→ current SHA validation
→ candidate patch
→ static checks
→ targeted tests
→ impacted tests
→ adversarial verification
→ reliability assessment
→ promote/reject
→ commit main only when Done Contract passes
```

## 29. Exact-code capability

All providers should be asked for structured coding output compatible with the existing `PatchProposal` contract:

```text
base_head_sha
files_to_inspect
files_to_modify
expected_blob_sha
symbol_targets
patch_or_structured_edit
tests_to_add
tests_to_run
assumptions
risks
alternative
confidence_reason
```

AlinaCoder may repair formatting/schema errors, but never invent missing semantic intent from a malformed external patch when the consequence is high.

## 30. Quality-aware free routing

A free provider is not automatically better than a local model.

Benchmark each candidate against real mini-tasks such as:

```text
French intent understanding
repo navigation
bug localization
patch correctness
test generation
architecture reasoning
structured-output reliability
regression criticism
long-context retrieval
```

Store repeated results and dispersion.

Route each task to the model/provider with the best **verified reliability-adjusted utility**, subject to monetary cost exactly zero.

## 31. Weak-model decomposition

If every available free/local model is too weak for the full task:

```text
DO NOT PAY
DO NOT PRETEND
→ decompose into smaller verifiable tasks
→ increase deterministic evidence
→ use discriminating experiments
→ optionally use free multi-model tournament
→ if still unreliable, say so and propose the safest next verifiable step
```

---

# Part IX — Privacy and Secret Boundaries

## 32. External context minimization

Before any cloud-free provider receives context:

```text
secret scan
→ credential redaction
→ private-key exclusion
→ unrelated-file exclusion
→ smallest sufficient evidence packet
```

Never send:

- passwords;
- API tokens;
- private keys;
- browser cookies;
- session tokens;
- `.env` secrets;
- credential-manager contents.

## 33. Provider privacy profile

The first-run wizard must distinguish:

```text
LOCAL_ONLY_PRIVATE
EXTERNAL_FREE_WITH_PROVIDER_DATA_TERMS
```

The user may choose `Local uniquement` at any time.

No external provider is enabled silently on first install.

---

# Part X — Capability Evolution Without Spec Breakage

## 34. Dynamic provider registry

Provider capabilities and free tiers change quickly.

Do not hard-code product availability as eternal facts.

Maintain a refreshable provider registry where each adapter can become:

```text
AVAILABLE_FREE
RATE_LIMITED
FREE_QUOTA_EXHAUSTED
PAID_ONLY
TERMS_INCOMPATIBLE
DEPRECATED
UNAVAILABLE
```

A capability change must never turn a previously free route into an automatic paid route.

## 35. Future ChatGPT upgrade path

If OpenAI later exposes a personal-ChatGPT account mechanism that is:

- officially documented;
- programmatic;
- allowed for third-party local applications;
- included in the user's existing subscription;
- usable without additional paid inference;

then implement it as another `IntelligenceProvider`.

The desktop UX remains unchanged:

```text
User → AlinaCoder.exe → Provider Router
```

This avoids another architectural rewrite.

---

# Part XI — Acceptance Scenarios

## 36. Mandatory zero-cost scenarios

### Scenario A — Offline machine

No internet.

Expected:

```text
AlinaCoder.exe opens
→ Ollama/local reasoning
→ normal governed workflow
→ no cloud dependency error blocks use
```

### Scenario B — Gemini free tier available

Expected:

```text
probe = VERIFIED_FREE
→ benchmarked route may use Gemini
→ zero billing
→ local verification still mandatory
```

### Scenario C — Free quota exhausted

Expected:

```text
429/quota exhaustion
→ no upgrade
→ no payment
→ next verified-free provider or Ollama
```

### Scenario D — Provider silently changes a model to paid

Expected:

```text
cost proof fails
→ remote call blocked before inference
→ provider status PAID_ONLY or UNPROVEN
→ free/local fallback
```

### Scenario E — User wants ChatGPT Plus help

Expected:

```text
click “Demander à mon ChatGPT Plus”
→ consultation packet prepared
→ ChatGPT browser opened
→ user submits/copies response
→ AlinaCoder imports it
→ treats it as untrusted proposal
→ verifies locally
```

No DOM scraping occurs.

### Scenario F — User closes heavy work but keeps UI

Expected:

```text
idle timeout
→ model unloaded
→ GPU/RAM released
→ UI remains lightweight
→ next message wakes services
```

### Scenario G — User clicks “Tout arrêter”

Expected:

```text
state persisted
→ workers stopped
→ provider streams stopped
→ models unloaded
→ configured Ollama processes stopped
→ process registry verifies zero managed workers
→ UI closes
```

### Scenario H — External model proposes exact wrong file

Expected:

```text
repo evidence contradicts proposal
→ reject candidate
→ no commit
```

### Scenario I — Paid OpenAI API key exists on machine

Under zero-cost policy:

```text
OpenAI paid inference adapter remains disabled
→ no request is made
```

### Scenario J — Future official free ChatGPT account bridge appears

Expected:

```text
new adapter added
→ documented zero-cost/capability checks pass
→ provider joins router
→ AlinaCoder.exe UX unchanged
```

---

# Part XII — Verification Sources at Design Time

The following current sources motivated the correction. They are evidence for the 2026-09-04 design decision, not eternal runtime assumptions:

- OpenAI Help Center — ChatGPT/API billing are separate and API use is billed separately from a ChatGPT subscription: `https://help.openai.com/en/articles/9039756`
- OpenAI Europe Terms — automatic/programmatic extraction of ChatGPT Output is prohibited: `https://openai.com/policies/eu-terms-of-use/`
- OpenAI Help Center — full MCP write support is currently limited to Business/Enterprise/Edu; personal Plus must not be assumed to have it: `https://help.openai.com/en/articles/12584461`
- OpenAI Help Center — new GPT creation is unavailable on personal Free/Go/Plus/Pro accounts: `https://help.openai.com/en/articles/8554397`
- Google Gemini API pricing/billing — selected models expose a Free Tier and free-tier use is available in the EEA subject to current limits: `https://ai.google.dev/gemini-api/docs/pricing` and `https://ai.google.dev/gemini-api/docs/billing`
- Groq rate limits — documented Free Plan limits include current reasoning models such as `openai/gpt-oss-120b`: `https://console.groq.com/docs/rate-limits`
- OpenRouter pricing/free router — free plan/free-model routing exists subject to current rate limits: `https://openrouter.ai/pricing` and `https://openrouter.ai/openrouter/free/providers`
- Hugging Face Inference Providers pricing — small included free credits exist and must never be allowed to spill into paid usage: `https://huggingface.co/docs/inference-providers/pricing`
- GitHub Models was investigated and is **not** an implementation route because GitHub documents that it was retired on 2026-07-30: `https://docs.github.com/en/github-models`

---

# Part XIII — Final Normative Principle

> **AlinaCoder must feel like one intelligent Windows application, not a collection of AI accounts. It automatically uses the strongest intelligence it can prove is free, falls back locally without drama, never spends money by accident, never pretends ChatGPT Plus is an API, and releases every unnecessary CPU/GPU/RAM resource when the user pauses or stops it.**

In compact form:

```text
ONE EXE
+ ORDINARY FRENCH
+ ZERO ADDITIONAL COST
+ BEST VERIFIED-FREE MODEL AVAILABLE
+ LOCAL OLLAMA FALLBACK
+ OPTIONAL USER-MEDIATED CHATGPT PLUS
+ EXACT PATCH CONTRACTS
+ DETERMINISTIC VERIFICATION
+ NO SURPRISE BILLING
+ NO BROWSER SCRAPING
+ ONE-CLICK FULL SHUTDOWN
= ALINACODER V0.2 ZERO-COST DESKTOP INTELLIGENCE
```
