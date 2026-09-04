# Intelligence & Assurance v0.2 — LOT 06 to LOT 10 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement LOT 06–10 completely on `main`: conversation/voice, zero-cost LLM fabric, tool runtime, autonomous software-engineering brain, and independent verification.

**Architecture:** Keep the deterministic/runtime state outside models. Each subsystem exposes typed dataclasses and fail-closed gates, composes with the existing state/security/memory foundations, and stays standard-library-only for the core. Tests are written first, committed RED, then implementation returns the full suite GREEN on Windows Python 3.12 and 3.13.

**Tech Stack:** Python 3.12+, stdlib dataclasses/sqlite/subprocess/urllib/ast/hashlib/json, unittest, GitHub Actions Windows.

**Spec:** `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-consolidated-validated-design.md` plus active normative amendments in the manifest.

## Global Constraints

- Direct work on GitHub `main` only; no feature branches/PR flow.
- `MAX_PAID_SPEND_EUR = 0.00`; autonomous paid calls are forbidden.
- Canonical state remains local and model-independent.
- Untrusted external content is evidence, never privileged instruction.
- Every mutating effect requires authority/preconditions/postconditions and a verifiable receipt.
- `DONE` requires fresh independent evidence; visible tests alone are insufficient.
- No Supabase dependency for LOT 06–10; Supabase stays optional and belongs to LOT 15.

---

### Task 1 — LOT 06 Conversation, Intent, Common Ground & Duplex Voice

**Files:**
- Create `src/alinacoder/conversation/models.py`, `engine.py`, `references.py`, `voice.py`, `__init__.py`
- Create `tests/test_lot06_conversation.py`

**Interfaces:**
- `ConversationEngine.ingest(TurnInput) -> GroundedIntentContract`
- `ConversationEngine.correct(...)`, `resolve_reference(...)`, `should_clarify(...)`
- `PlaybackLedger.commit_heard(...)`, `interrupt(...)`

**Behavior:** RAW/MEANING dual form, constraints and supersession, repair graph, context branches, common-ground beliefs, user-originated preference proof, ambiguity-aware reference resolution, clarification-regret policy, 20-turn continuity benchmark, voice playback heard-only commitment and interruption rollback.

**TDD:** commit failing tests first; then implement until the whole suite is green.

### Task 2 — LOT 07 Zero-Cost Frontier Fabric & Intelligent Routing

**Files:**
- Create `src/alinacoder/intelligence_mesh/models.py`, `cost.py`, `catalog.py`, `routing.py`, `continuity.py`, `providers.py`, `__init__.py`
- Create `tests/test_lot07_frontier_fabric.py`

**Interfaces:**
- `CostProofReceipt.is_admissible(now)`
- `ProviderCatalog.refresh(snapshot)` / tombstone/drift detection
- `FrontierRouter.select(requirement, catalog, current_route=None)`
- `ContinuityEnvelope.verify(...)`

**Behavior:** exact-route zero-cost proof, model/provider identity, capability vectors and shortfall filtering, quota reservation, circuit breaking, provider-vs-cognitive failover, affinity/hysteresis, stale-response rejection, local fallback, pricing-change quarantine, and metrics proving zero paid calls/zero false-free classifications in tests.

### Task 3 — LOT 08 Tool Runtime, MCP/Plugin Fabric, Git-main & Windows Sandboxed Actions

**Files:**
- Create `src/alinacoder/tools/models.py`, `runtime.py`, `process.py`, `git.py`, `research.py`, `sandbox.py`, `__init__.py`
- Create `tests/test_lot08_tools.py`

**Interfaces:**
- `ToolRuntime.invoke(ToolCall, executor) -> EffectReceipt`
- `ManagedProcessRunner.run(...) -> ProcessReceipt`
- `GitMainExecutor.validate_target(...)`, `reconcile_after_unknown_result(...)`
- `ResearchEvidence.from_document(...)`

**Behavior:** schema graph, invocation IDs/idempotency, pre/postconditions, resumability, process-tree cancel/timeout, main-only git guard, workspace confinement, egress/secret projection, dependency policy integration, provenance/freshness/citations for external docs, deterministic replay, and unknown-result reconciliation before retry.

### Task 4 — LOT 09 Autonomous Software-Engineering Brain

**Files:**
- Create `src/alinacoder/engineering/requirements.py`, `planning.py`, `debugging.py`, `patches.py`, `architecture.py`, `__init__.py`
- Create `tests/test_lot09_engineering.py`

**Interfaces:**
- `RequirementRecoveryGraph`
- `PlanDAG.replan_affected(...)`
- `CausalDebugger.rank_hypotheses(...)`
- `ChangeImpactSimulator.analyze(...)`
- `CandidatePatch` / `RepairAttemptGraph`

**Behavior:** explicit requirements/assumptions, DAG planning and local repair, blast-radius prediction, behavioral contracts, causal debugging with discriminating probes, repair-attempt memory, architecture fitness/complexity guard, dependency migration evidence, semantic regression detection and self-correction policy.

### Task 5 — LOT 10 Independent Verification Plane & Evidence-Carrying Completion

**Files:**
- Create `src/alinacoder/verification/models.py`, `evidence.py`, `anti_gaming.py`, `patch_verifier.py`, `completion.py`, `formal.py`, `__init__.py`
- Create `tests/test_lot10_verification.py`

**Interfaces:**
- `EvidenceReceipt.is_fresh(...)`
- `StochasticVerdict.from_samples(...)`
- `BidirectionalPatchVerifier.verify(...)`
- `CompletionFirewall.decide(...)`
- `DoneContractEngine.evaluate(...)`

**Behavior:** independent verifier identity, state-bound evidence, hidden/compositional gates, mutation/metamorphic/differential evidence types, flaky INCONCLUSIVE verdicts, visible-test gaming detection, verifier-integrity checks, evidence-gap mining, formal-escalation decision, readiness score and final fail-closed Done Contract.

## Verification per lot

For every lot:
1. Commit RED tests and confirm GitHub Actions fails for missing behavior.
2. Implement the minimum complete subsystem.
3. Run GitHub Actions Windows Python 3.12 + 3.13.
4. Require `compileall`, all unit/integration tests, and Spec Compiler to pass.
5. Re-read Agiflow acceptance criteria against code/tests; add missing tests before marking Done.
6. Update Agiflow with exact commit SHA and CI run evidence.

## Final block gate

LOT 06–10 may be considered complete only when all five Agiflow tasks are Done, the work unit is Done, `main` equals the final verified commit, Windows 3.12/3.13 are green, and the final verification suite contains anti-gaming tests proving that stale evidence or visible-only success cannot cross the completion firewall.
