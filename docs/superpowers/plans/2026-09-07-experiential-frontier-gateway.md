# Experiential Frontier Gateway Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Experiential Labs as a safe optional aggregator in AlinaCoder's Intelligence Mesh while preserving strict zero-cost semantics and adding a separate hard-stop sponsored-credit admission path.

**Architecture:** Keep AlinaCoder as the outer router and verification authority. Add a new provider safety class and sponsored-credit qualification proof, register Experiential as an OpenAI-compatible aggregator, and teach `InferenceFabric` to admit non-zero list-price routes only when a fresh sponsored-credit proof establishes platform-funded capacity with no paid/BYOK spillover. All existing exact-zero-price and Ollama behavior remains unchanged.

**Tech Stack:** Python 3.12/3.13, `unittest`/pytest-compatible tests, existing `urllib` transport, Windows DPAPI credential vault, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-07-experiential-frontier-gateway-amendment.md`

## Global Constraints

- Branch policy: `main` only.
- Never weaken `PROVEN_ZERO_COST` semantics.
- Promotional credits are not zero list price.
- No paid spillover, auto-recharge, autonomous top-up, or BYOK fallback in zero-cost execution.
- Existing local Ollama fallback must remain intact.
- Experiential is optional and subordinate to AlinaCoder routing/policy.
- Credentials remain in the existing secret boundary and are never emitted into prompts/logs/Activity.
- Remote content telemetry remains disabled by default.

---

### Task 1: Red tests for sponsored-credit admission

**Files:**
- Create: `tests/test_experiential_frontier_gateway.py`

**Interfaces:**
- Consumes: `ProviderSafetyClass`, `CostProofReceipt`, `QualificationRegistry`, `SponsoredCreditQualification`, `InferenceFabric`, `ProviderDefinition`, `OpenAICompatibleProvider`.
- Produces: executable contract for all later tasks.

- [ ] **Step 1: Add failing tests**

Tests must assert:

```python
ProviderSafetyClass.SPONSORED_CREDIT_HARD_STOP.value == "SPONSORED_CREDIT_HARD_STOP"
```

and construct a `SponsoredCreditQualification` with fields:

```python
provider_id: str
model_id: str
verified_at: datetime
expires_at: datetime
list_prompt_price: float
list_completion_price: float
list_request_price: float
credit_remaining_usd: float
platform_funded_lane: bool
auto_recharge_disabled: bool
hard_quota_stop: bool
byok_fallback_disabled: bool
paid_fallback_disabled: bool
account_safe: bool
source: str
zdr_satisfied: bool = True
no_training_satisfied: bool = True
```

`admissible(now)` must be true only when proof is fresh, credit is positive, the platform-funded lane is active, auto-recharge is disabled, quota exhaustion hard-stops, BYOK/paid fallback is disabled, account is safe, and policy posture is satisfied.

Also assert a positive-price `CostProofReceipt` with verdict `SPONSORED_CREDIT_HARD_STOP` is admissible only when `sponsored_credit_remaining_usd > 0`, `auto_recharge_disabled`, `byok_fallback_disabled`, and `paid_fallback_disabled` are all true.

- [ ] **Step 2: Commit the RED tests**

Commit message: `test: define Experiential sponsored-credit safety contract`

- [ ] **Step 3: Verify RED in GitHub Actions**

Expected: CI fails because the new enum/class/receipt fields do not exist yet.

---

### Task 2: Add sponsored-credit proof primitives

**Files:**
- Modify: `src/alinacoder/intelligence_mesh/provider_atlas.py`
- Modify: `src/alinacoder/intelligence_mesh/models.py`
- Modify: `src/alinacoder/intelligence_mesh/qualification.py`
- Modify: `src/alinacoder/intelligence_mesh/__init__.py`

**Interfaces:**
- Produces `ProviderSafetyClass.SPONSORED_CREDIT_HARD_STOP`.
- Produces `SponsoredCreditQualification.admissible(now: datetime) -> bool`.
- Extends `CostProofReceipt` with sponsored-credit metadata while preserving all existing constructor calls through defaults.
- `QualificationRegistry` stores and reads both exact-zero and sponsored-credit proofs independently.

- [ ] **Step 1: Implement the enum and proof class**

`SponsoredCreditQualification.admissible()` must fail closed on stale proofs, zero/negative credits, any enabled/unknown recharge/fallback path, unsafe account state, or failed ZDR/no-training flags.

- [ ] **Step 2: Extend `CostProofReceipt` compatibly**

Append defaulted fields:

```python
billing_class: str = "ZERO_PRICE_MODEL"
sponsored_credit_remaining_usd: float = 0.0
auto_recharge_disabled: bool = False
byok_fallback_disabled: bool = False
paid_fallback_disabled: bool = False
```

`is_admissible()` keeps the old exact-zero path unchanged and adds a separate sponsored path for verdict `SPONSORED_CREDIT_HARD_STOP`.

- [ ] **Step 3: Extend the registry and exports**

Add `upsert_sponsored()` / `get_sponsored()` methods without changing existing zero-cost methods.

- [ ] **Step 4: Commit**

Commit message: `feat: add hard-stop sponsored-credit proof model`

---

### Task 3: Register Experiential and enforce outer-router safety

**Files:**
- Modify: `src/alinacoder/intelligence_mesh/provider_atlas.py`
- Modify: `src/alinacoder/intelligence_mesh/fabric.py`
- Modify: `src/alinacoder/intelligence_mesh/runtime.py`
- Extend: `tests/test_experiential_frontier_gateway.py`

**Interfaces:**
- Provider id: `experiential_gateway`.
- Base URL: `https://api.experientiallabs.ai/v1`.
- Discovery URL: `https://api.experientiallabs.ai/v1/models`.
- Vault key: `experiential_gateway`.

- [ ] **Step 1: Add/extend RED tests**

Assert the atlas entry is an aggregator, requires account proof, is not structurally auto-admissible, and carries `SPONSORED_CREDIT_HARD_STOP`.

Assert `InferenceFabric` rejects a positive-list-price Experiential model without sponsored proof and admits it with fresh sponsored proof.

Assert 429/`QUOTA_EXHAUSTED` and 402/`BILLING_BLOCKED` deplete the route and fail over rather than reusing it.

- [ ] **Step 2: Register Experiential**

Add the `ProviderDefinition` to `normative_provider_atlas()`.

- [ ] **Step 3: Implement sponsored admission in the fabric**

For a positive-list-price remote model:

```python
proof = registry.get_sponsored(provider_id, model_id)
if proof and proof.admissible(now):
    admit as SPONSORED_CREDIT_HARD_STOP
else:
    reject
```

Never synthesize `PROVEN_ZERO_COST` for a sponsored route. Preserve actual list prices in the receipt.

- [ ] **Step 4: Preserve runtime compatibility**

The existing generic OpenAI-compatible runtime builder should instantiate Experiential when its DPAPI vault entry exists, with no provider-specific secret-handling path.

- [ ] **Step 5: Commit**

Commit message: `feat: integrate Experiential as guarded frontier aggregator`

---

### Task 4: Security/provenance regression coverage

**Files:**
- Extend: `tests/test_experiential_frontier_gateway.py`
- Modify only if needed: `src/alinacoder/intelligence_mesh/providers.py`

**Interfaces:**
- Provider/model lineage remains the model lineage, not the gateway identity.
- Error handling remains fail-closed.

- [ ] **Step 1: Add tests**

Cover stale proof, empty credit, auto-recharge enabled, BYOK fallback enabled, paid fallback enabled, policy flags false, and exact-zero regression behavior.

Cover that OpenAI-compatible HTTP auth uses a Bearer key without surfacing the secret in `ProviderResponse.metadata` or exceptions.

- [ ] **Step 2: Make only the minimum production changes required**

Do not add remote content telemetry or management-API writes.

- [ ] **Step 3: Commit**

Commit message: `test: harden Experiential cost and secret boundaries`

---

### Task 5: Canonical verification

**Files:**
- No production file unless verification exposes a defect.

- [ ] **Step 1: Run the full GitHub Actions CI on the final `main` SHA**

Expected: Python 3.12 and 3.13 core jobs, packaging/release gates, and all existing v0.2 acceptance gates remain green.

- [ ] **Step 2: Inspect failing job logs if necessary**

Only fix failures causally introduced by this integration; do not weaken existing release gates.

- [ ] **Step 3: Verify final commit history and exact `main` HEAD**

Report final SHA and CI conclusion.
