# AlinaCoder Experiential Frontier Gateway — Design Amendment

Date: 2026-09-07
Status: APPROVED FOR IMPLEMENTATION
Repository: `Rapt0r06300/alinacoder`
Branch policy: `main` only
Parent design: `docs/superpowers/specs/2026-09-07-cognitive-kernel-zero-cost-frontier-mesh-design.md`

## 1. Decision

Experiential Labs is integrated as an optional aggregator/provider inside AlinaCoder's existing Intelligence Mesh. It is never the authority for model selection, safety, cost policy, verification, or user intent. AlinaCoder remains the final router and verification authority.

The integration is additive. It must not replace direct providers, local Ollama, deterministic verification, or provider/model lineage accounting.

## 2. Why this belongs in the mesh

Experiential exposes OpenAI-compatible Chat Completions and Responses APIs, a model catalog, provider waterfalls, hosted platform credits, BYOK routes, usage metering, spend controls, ZDR/no-training policy controls, and coding-agent compatibility. This makes it useful as a fast path to newly released frontier models without adding a bespoke transport for each model.

Its internal waterfall is treated as an implementation detail that must remain subordinate to AlinaCoder policy. A model served through Experiential retains its underlying model lineage; multiple gateways serving the same model do not count as independent cognitive lineages.

## 3. Billing classes

AlinaCoder must distinguish three states and must never collapse them:

1. `ZERO_PRICE_MODEL`: exact live input/output/request prices are zero.
2. `SPONSORED_CREDIT_HARD_STOP`: the model has non-zero list prices but the current request is covered by platform-funded promotional/welcome credits and paid spillover is proven impossible for the credential/account state.
3. `PAID_OR_UNPROVEN`: anything else; never eligible in `free-cloud` or the remote phase of `hybrid`.

`SPONSORED_CREDIT_HARD_STOP` does not mean the provider's list price is zero. Activity/provenance must report both the list price and the user's current out-of-pocket verdict.

## 4. Sponsored-credit proof contract

A sponsored-credit route is admissible only when all of the following are true at dispatch time:

- exact provider and model are identified;
- proof source is recorded;
- proof is fresh and not expired;
- platform-funded lane is proven for the selected deployment;
- remaining platform credit is strictly positive;
- auto-recharge is proven disabled;
- API-key/customer actions cannot silently purchase/top-up credits;
- a hard spend/budget boundary is present and exhaustion returns a hard quota error rather than continuing onto a billable route;
- BYOK fallback is excluded from the selected waterfall for zero-cost execution;
- any paid/unknown fallback rung is excluded;
- ZDR/no-training/provider allowlist requirements requested by policy are satisfied;
- the request cannot mutate billing controls.

If any required fact is unknown, stale, contradictory, or cannot be verified, the route is rejected fail-closed.

## 5. Experiential provider definition

Add `experiential_gateway` to the normative Provider Atlas:

- protocol: `openai_chat`;
- base URL: `https://api.experientiallabs.ai/v1`;
- discovery URL: `https://api.experientiallabs.ai/v1/models`;
- credential: `EXPERIENTIAL_API_KEY` / DPAPI vault entry under `experiential_gateway`;
- aggregator: true;
- safety class: `SPONSORED_CREDIT_HARD_STOP` plus exact zero-price routes when independently proven;
- account proof required: true;
- structurally auto-admissible: false;
- zero-cost requalification required: true.

The generic OpenAI-compatible adapter may execute the inference lane. Experiential-specific qualification metadata is handled separately and must not be inferred from generic `/v1/models` pricing alone.

## 6. Secrets

The Experiential key is stored through AlinaCoder's existing Windows DPAPI provider vault. It must never be written to Git, prompts, conversation transcripts, Activity details, logs, shell command history, or child-process environments by default.

Provider/BYOK secrets are never copied into AlinaCoder prompts. AlinaCoder does not use the Experiential management API to connect third-party provider keys autonomously.

## 7. Routing and failover

AlinaCoder owns the outer routing decision.

- Experiential is one route candidate among direct providers and Ollama.
- Direct/free routes and Experiential routes are benchmarked using the same capability profile machinery.
- Scarce sponsored frontier capacity is reserved for high-value work: architecture, difficult debugging, adversarial review, verification analysis, and release-critical decisions.
- Routine indexing, deterministic inspection, summarization, and trivial transformations should prefer local or cheaper proven routes.
- 401/403 disables the route pending credential/account change.
- 429 or `insufficient_quota` depletes the route until requalification/reset.
- 402 is a hard billing block.
- 5xx/network errors use bounded retry/circuit breaking then fail over.
- a pricing/lane/waterfall change invalidates prior qualification immediately.

## 8. Data handling

Remote telemetry/traces are disabled by default for AlinaCoder content. Allowed usage metadata is limited to model/provider, token counts, latency, cost attribution, quota state, timestamp, and success/failure classification.

Prompts, responses, source code, file contents, tool arguments, memory, and conversation content must not be uploaded as Experiential telemetry by the AlinaCoder integration.

For sensitive repositories, policy may require ZDR + no-training + approved-provider allowlist before an Experiential route becomes eligible.

## 9. Activity and provenance

For every Experiential inference, the observable activity record must be able to distinguish:

- provider: `experiential_gateway`;
- underlying model slug;
- actual model lineage;
- billing class (`ZERO_PRICE_MODEL` or `SPONSORED_CREDIT_HARD_STOP`);
- list pricing when known;
- out-of-pocket verdict;
- proof freshness/expiry;
- quota/credit state when known;
- concise route reason;
- ZDR/no-training posture when policy requires it.

No secret or hidden chain-of-thought may appear.

## 10. Verification requirements

The implementation is not complete until tests cover at least:

- atlas registration and runtime construction;
- sponsored-credit proof succeeds only under the complete hard-stop contract;
- positive list prices remain rejected without sponsored proof;
- stale/expired sponsored proof is rejected;
- zero/negative credit is rejected;
- auto-recharge enabled/unknown is rejected;
- BYOK/paid fallback allowed is rejected;
- `insufficient_quota`/429 depletes and fails over;
- 402 billing block depletes and fails over without retrying paid execution;
- exact zero-price routes continue to work unchanged;
- local Ollama fallback remains unchanged;
- model lineage is preserved across gateway/provider hosts;
- credentials remain redacted by existing secret boundaries.

GitHub Actions is the canonical verification surface when local repository execution is unavailable.

## 11. Non-goals

This amendment does not:

- make Experiential mandatory;
- grant Experiential authority to choose paid routes;
- enable auto-recharge or purchases;
- upload AlinaCoder traces/content for model training;
- replace direct provider integrations;
- weaken `PROVEN_ZERO_COST` semantics;
- treat promotional credits as zero list price;
- claim GPT-6 Astra, Claude Fable 5.1, or any named model is permanently free or permanently best.
