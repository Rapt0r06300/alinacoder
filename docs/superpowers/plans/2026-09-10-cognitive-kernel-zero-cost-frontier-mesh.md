# Cognitive Kernel + Zero-Cost Frontier Mesh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the approved Cognitive Kernel + Zero-Cost Frontier Mesh design on the current AlinaCoder `main` branch with deterministic execution state, plan-memory coupling, task-aware zero-cost routing, persistent quota/health control, robust conversation repair, verified learning, replay gates, and safe Codex-like observability.

**Architecture:** Preserve the existing conversation, goal, memory, intelligence-mesh, orchestration, verification, desktop, installer and release systems. Add narrow, testable components around them and integrate through explicit state contracts rather than rewriting working foundations. Deterministic state/evidence governs actions; LLM output remains advisory until verified.

**Tech Stack:** Python >=3.12 standard library, SQLite WAL/FULL, existing StateStore/MemoryStore/SkillBook/InferenceFabric/Orchestrator/DesktopWorkbench, unittest, GitHub Actions on Windows 3.12/3.13, PyInstaller, Ollama HTTP API.

**Spec:** `docs/superpowers/specs/2026-09-07-cognitive-kernel-zero-cost-frontier-mesh-design.md`

**Current baseline:** `71c51310bf70e025f0f0573fef7808789d16b07d`

## Global Constraints

- Work directly on `main`; the user explicitly authorized it.
- `MAX_PAID_SPEND_EUR = 0.00` for free-cloud/hybrid remote routing.
- Never evade quotas through IP/proxy/account/key rotation.
- Unknown/stale pricing is ineligible.
- Preserve the Experiential sponsored-credit hard-stop extension already present at the baseline.
- Preserve local Ollama as the foundational no-API-billing fallback.
- No hidden chain-of-thought in state, logs, activity, prompts-as-telemetry or UI.
- No completion claim without fresh state-bound execution evidence.
- Preserve installer/release self-healing and exact-artifact provenance gates.
- No new third-party Python dependency unless a later explicit design amendment authorizes it.

---

### Task 1: RED contract suite for the approved architecture

**Files:**
- Create: `tests/test_cognitive_kernel.py`
- Create: `tests/test_frontier_mesh_v2.py`
- Create: `tests/test_execution_ledger.py`
- Create: `tests/test_conversation_replay_v2.py`
- Create: `tests/test_cognitive_release_gate.py`

**Interfaces:**
- Tests define the public contracts consumed by Tasks 2-11.

- [ ] **Step 1: Write failing tests** that import the planned modules/classes and assert behavior for anonymous Kilo, Wilson capability scoring, persistent quota cooldowns, execution-ledger invalidation/reuse, causal invalidation, clarification control, phase-aware retrieval, context folding, critic value-gating, verified skill quarantine, 1,000 replay cases, desktop route trace and release acceptance IDs.
- [ ] **Step 2: Push only the tests.**
- [ ] **Step 3: Verify RED in GitHub Actions** on Python 3.12 and 3.13. Expected failure is missing new modules/classes/acceptance IDs, not syntax or unrelated regressions.
- [ ] **Step 4: Record the RED run id in the final audit.**

### Task 2: Anonymous Kilo free bridge without weakening billing safety

**Files:**
- Modify: `src/alinacoder/intelligence_mesh/runtime.py`
- Modify: `src/alinacoder/intelligence_mesh/provider_atlas.py`
- Modify: `src/alinacoder/intelligence_mesh/providers.py`
- Test: `tests/test_frontier_mesh_v2.py`

**Interfaces:**
- `build_default_inference_fabric(...)` instantiates `kilo_gateway` with an empty credential only when the provider definition explicitly allows anonymous free-model execution.
- `OpenAICompatibleProvider` omits Authorization when key is empty.
- Anonymous Kilo dispatch is limited to exact discovered zero-price routes and explicitly free virtual routes; any non-zero/unknown route remains ineligible.

- [ ] **Step 1: Make the anonymous-Kilo tests GREEN** by adding an explicit provider-definition flag `anonymous_free_allowed: bool = False`, enabling it only for Kilo, and constructing a no-key adapter only for that provider.
- [ ] **Step 2: Preserve `PROVEN_ZERO_COST` checks before dispatch.**
- [ ] **Step 3: Run focused suite and existing provider-fabric regressions.**
- [ ] **Step 4: Commit `feat(mesh): add safe anonymous Kilo free bridge`.**

### Task 3: Measured capability profiles and task-aware model ranking

**Files:**
- Create: `src/alinacoder/intelligence_mesh/profiles.py`
- Create: `src/alinacoder/intelligence_mesh/tasks.py`
- Modify: `src/alinacoder/intelligence_mesh/models.py`
- Modify: `src/alinacoder/intelligence_mesh/fabric.py`
- Modify: `src/alinacoder/intelligence_mesh/__init__.py`
- Test: `tests/test_frontier_mesh_v2.py`

**Interfaces:**
- `wilson_lower_bound(successes: int, trials: int, z: float = 1.959963984540054) -> float`.
- `CapabilityObservation(successes, trials, benchmark_version, observed_at)`.
- `ModelCapabilityProfile(provider_id, model_id, lineage, dimensions, context_tokens, benchmark_version)`.
- `CapabilityProfileStore.record(...)`, `.quality_lcb(...)`, `.capabilities(...)`.
- `TaskClass` enum and `TaskClassifier.classify(messages, requirement) -> TaskClass`.

- [ ] **Step 1: Implement Wilson LCB exactly** using the standard Bernoulli Wilson lower-bound formula; return 0.0 for zero trials.
- [ ] **Step 2: Implement cold-start prior behavior** where fewer than 5 measured trials are penalized below a proven route with the same nominal prior.
- [ ] **Step 3: Implement deterministic task classification** for conversation, intent, planning, repository, architecture, code, debug, review, verification, summarization and research using requirement dimensions and recent user text.
- [ ] **Step 4: Wire discovered routes through profile evidence** so production no longer relies solely on `ProviderModel.quality_hint=0.5`.
- [ ] **Step 5: Keep provider metadata as seed evidence only.**
- [ ] **Step 6: Run focused + existing routing tests; commit `feat(mesh): add measured task-aware capability profiles`.**

### Task 4: Persistent QuotaLedger and provider circuit control

**Files:**
- Create: `src/alinacoder/intelligence_mesh/quota.py`
- Modify: `src/alinacoder/intelligence_mesh/fabric.py`
- Modify: `src/alinacoder/intelligence_mesh/providers.py`
- Modify: `src/alinacoder/intelligence_mesh/__init__.py`
- Test: `tests/test_frontier_mesh_v2.py`

**Interfaces:**
- `QuotaState`: AVAILABLE, DEPLETED_UNTIL_RESET, TEMP_UNHEALTHY, AUTH_BLOCKED, BILLING_BLOCKED, RETIRED, UNKNOWN.
- `QuotaRecord` stores remaining requests/tokens, reset/cooldown timestamps, consecutive failures, EWMA latency, success/failure counts, last error and cost-proof expiry.
- `QuotaLedger(path)` persists SQLite state; `.eligible(...)`, `.observe_response(...)`, `.observe_error(...)`, `.reserve(...)`, `.release(...)`.

- [ ] **Step 1: Implement SQLite WAL/FULL schema and restart persistence.**
- [ ] **Step 2: Parse `Retry-After` and known rate-limit reset headers into cooldown/reset state.**
- [ ] **Step 3: 429 -> depleted until reset; 402 -> billing blocked; 401/403 -> auth blocked; repeated 5xx/network -> temporary unhealthy/open circuit.**
- [ ] **Step 4: Integrate eligibility before routing and outcome updates after calls.**
- [ ] **Step 5: Replace process-lifetime depletion as the sole source of truth; retain compatibility where required.**
- [ ] **Step 6: Run persistence/failover regressions; commit `feat(mesh): persist quota and provider health`.**

### Task 5: Deterministic Execution Ledger

**Files:**
- Create: `src/alinacoder/runtime/__init__.py`
- Create: `src/alinacoder/runtime/ledger.py`
- Modify: `src/alinacoder/desktop/workbench.py`
- Test: `tests/test_execution_ledger.py`

**Interfaces:**
- `ExecutionLedger(path)` with SQLite WAL/FULL.
- `record_observation(...) -> str`, `record_modification(...) -> str`, `record_command(...) -> str`.
- `invalidate_paths(paths, cause) -> tuple[str, ...]`.
- `reusable_read(command, repo_state) -> LedgerCommand | None`.
- `repeated_failed_strategy(strategy_key, repo_state) -> bool`.
- `inform(repo_state, limit=...) -> LedgerSummary`.

- [ ] **Step 1: Implement deterministic digests and observation validity.**
- [ ] **Step 2: Mutation invalidates affected observations unless content digest proves unchanged.**
- [ ] **Step 3: Exact read-only command under unchanged state may be reused; failed mutation repetition becomes a replan signal.**
- [ ] **Step 4: Instrument DesktopWorkbench file writes, tests and git actions with ledger records without adding model calls.**
- [ ] **Step 5: Run focused + desktop regressions; commit `feat(runtime): add deterministic execution ledger`.**

### Task 6: CognitiveState, dependency graph and causal correction

**Files:**
- Create: `src/alinacoder/cognitive/__init__.py`
- Create: `src/alinacoder/cognitive/models.py`
- Create: `src/alinacoder/cognitive/state.py`
- Create: `src/alinacoder/cognitive/dependencies.py`
- Test: `tests/test_cognitive_kernel.py`

**Interfaces:**
- `CognitiveState` contains only operational fields from the approved spec.
- `CognitiveStateStore(StateStore, session_id)` loads/updates a `cognitive` subdocument with event-backed revisions.
- `DependencyGraph.add(node_id, kind, depends_on=...)` and `invalidate_descendants(changed, reason) -> set[str]`.

- [ ] **Step 1: Implement backwards-compatible empty cognitive state initialization.**
- [ ] **Step 2: Persist intent/plan/ledger/memory versions, requirements, constraints, prohibitions, uncertainties, facts, route and verification point.**
- [ ] **Step 3: Implement transitive descendant invalidation while preserving unrelated nodes.**
- [ ] **Step 4: Bind invalidation results to stale facts/plan nodes rather than deleting them.**
- [ ] **Step 5: Run restart/reconstruction tests; commit `feat(cognitive): add canonical state and causal invalidation`.**

### Task 7: Intent Compiler v2 and information-gain clarification controller

**Files:**
- Create: `src/alinacoder/conversation/intent.py`
- Create: `src/alinacoder/conversation/control.py`
- Modify: `src/alinacoder/conversation/__init__.py`
- Modify: `src/alinacoder/conversation/advanced.py`
- Test: `tests/test_cognitive_kernel.py`
- Test: `tests/test_conversation_replay_v2.py`

**Interfaces:**
- `IntentEnvelope` with raw/meaning/primary/alternatives/references/requirement deltas/constraints/prohibitions/result/continuation/confidence/uncertainty/source turns.
- `IntentCompiler.compile(...) -> IntentEnvelope` is deterministic-first and accepts optional model proposal as untrusted interpretation evidence.
- `ControlAction`: ACT, INSPECT, SANDBOX_PROBE, VERIFY, ESCALATE_MODEL, CALL_COUNCIL, ASK_USER, BLOCK.
- `UncertaintyController.decide(...) -> ControlDecision`.

- [ ] **Step 1: Implement deterministic parsing of explicit continuation, correction, cancellation, prohibitions and selected artifact references.**
- [ ] **Step 2: Preserve RAW + MEANING and current conversation invariants.**
- [ ] **Step 3: Implement decision order inspect -> sandbox -> best reversible assumption -> highest-information question -> block.**
- [ ] **Step 4: Ensure low confidence alone never forces a question.**
- [ ] **Step 5: Wire user corrections into the causal dependency graph.**
- [ ] **Step 6: Run existing LOT06 + new replay tests; commit `feat(conversation): add intent compiler and uncertainty control`.**

### Task 8: Hierarchical plan-memory coupling and adaptive context folding

**Files:**
- Create: `src/alinacoder/cognitive/planning.py`
- Create: `src/alinacoder/memory/adaptive.py`
- Modify: `src/alinacoder/memory/retrieval.py`
- Modify: `src/alinacoder/memory/context.py`
- Modify: `src/alinacoder/memory/__init__.py`
- Test: `tests/test_cognitive_kernel.py`

**Interfaces:**
- `PlanNodeV2` includes phase/subtask/dependencies/evidence predicate/blast radius/tools/status/attempts/failures/memory query intent.
- `PlanGraph.replan_affected(...)` preserves independent completed nodes.
- `RetrievalContext` carries goal/phase/subtask/paths/failures/constraints/repo state.
- `PhaseAwareRetriever.search(...)` ranks lexical, graph, phase, freshness, authority, evidence validity, diversity, failure relevance and context cost.
- `ContextFolder.fold(...) -> FoldedContext` preserves source event ids and never deletes lossless history.

- [ ] **Step 1: Add structured plan nodes and targeted replanning.**
- [ ] **Step 2: Add phase-aware scoring on top of existing stores without removing project/freshness gates.**
- [ ] **Step 3: Add proactive fold summaries with decisions/evidence/rejected hypotheses/open questions/verification/source ids.**
- [ ] **Step 4: Fail closed when mandatory anchors exceed budget.**
- [ ] **Step 5: Run memory/planner regressions; commit `feat(cognitive): couple planning memory and context`.**

### Task 9: Verification authority, independent critic and verified learning

**Files:**
- Create: `src/alinacoder/verification/kernel.py`
- Create: `src/alinacoder/orchestration/critic.py`
- Modify: `src/alinacoder/memory/skillbook.py`
- Modify: `src/alinacoder/verification/__init__.py`
- Test: `tests/test_cognitive_kernel.py`

**Interfaces:**
- `VerificationKernel.invalidate_for_paths(...)`, `.certify(...)` accepts only fresh state-bound evidence.
- `CriticPacket` contains task contract/evidence/proposed result and excludes private reasoning.
- `CriticPolicy.should_call(...)` reuses `CouncilPolicy` value logic plus criticality/uncertainty/repeated failure/blast radius.
- `ExperienceCard` gains problem signature, scope, strategy, failed alternatives, evidence ids, commit binding, revalidation and outcome statistics with backward-compatible defaults.
- `SkillBook.observe_outcome(...)` and `.quarantine(...)` retain poor skills but exclude them from active search.

- [ ] **Step 1: Implement verification invalidation by repository state/path dependency.**
- [ ] **Step 2: Implement critic packet redaction and lineage independence check.**
- [ ] **Step 3: Extend SkillBook schema through additive migration and verified promotion rules.**
- [ ] **Step 4: Quarantine repeatedly poor skills without deletion.**
- [ ] **Step 5: Run verification/orchestration/skill regressions; commit `feat(assurance): add verified critic learning loop`.**

### Task 10: Deterministic 1,000-case conversation replay campaign

**Files:**
- Create: `src/alinacoder/evaluation/conversation_replay.py`
- Modify: `src/alinacoder/evaluation/torture.py`
- Test: `tests/test_conversation_replay_v2.py`

**Interfaces:**
- `ReplayCase(case_id, category, turns, expected)`.
- `ConversationReplayCorpus.generate(seed=...) -> tuple[ReplayCase, ...]` deterministically produces >=1,000 retained cases.
- `ConversationReplayRunner.run(...) -> ReplayReport` reports total/pass/fail/category failures and keeps stable failure IDs.

- [ ] **Step 1: Generate categories for corrections, pronouns, multi-selection ambiguity, continuation, negation, priority/scope, interruption, partial ASR, noisy French, mixed technical language, stale references, restarts, messages during work, stop scope, undo, 100+ turn retention, false-memory rejection and causal invalidation.**
- [ ] **Step 2: Ensure deterministic case IDs and no external model/network dependency for release tests.**
- [ ] **Step 3: Add failures as stable regression fixtures.**
- [ ] **Step 4: Integrate summary into TortureLab/readiness.**
- [ ] **Step 5: Run campaign; commit `test(conversation): add thousand-case replay gate`.**

### Task 11: Desktop cognitive/route observability

**Files:**
- Modify: `src/alinacoder/desktop/activity.py`
- Modify: `src/alinacoder/desktop/workbench.py`
- Modify: `src/alinacoder/desktop/core.py`
- Modify: `src/alinacoder/desktop/app.py`
- Test: `tests/test_cognitive_kernel.py`
- Test: existing desktop live-activity tests

**Interfaces:**
- Safe activity kinds include `intent_updated`, `plan_updated`, `ledger_updated`, `route_selected`, `quota_failover`, `critic_called`, `verification_updated`.
- Current run exposes goal/phase/next action/blocker/verification/provider/model/task class/route reason/zero-cost verdict only.

- [ ] **Step 1: Persist concise operational state and route provenance.**
- [ ] **Step 2: Render Activity/Run Inspector without credentials, prompts-as-telemetry or hidden reasoning.**
- [ ] **Step 3: Preserve inference-only background-thread rule and Tk main-thread StateStore writes.**
- [ ] **Step 4: Add semantic UI capabilities/actions for cognitive status where needed.**
- [ ] **Step 5: Run all desktop/source-contract tests; commit `feat(desktop): expose cognitive and routing trace`.**

### Task 12: Acceptance/release gates and final proof

**Files:**
- Modify: `src/alinacoder/release/acceptance.py`
- Modify: `docs/release/acceptance-coverage-v0.2.json`
- Modify: `docs/release/traceability-v0.2.json`
- Modify: `scripts/generate_release_metadata.py` only if current metadata lacks the new proof fields.
- Modify: `docs/USER_GUIDE.md`
- Create: `docs/audits/2026-09-10-cognitive-kernel-frontier-mesh-final-audit.md`
- Test: `tests/test_cognitive_release_gate.py`

**Interfaces:**
- Add acceptance cases for anonymous Kilo safety, measured capability routing, quota persistence/reset, execution-ledger invalidation, causal correction, phase-aware memory, adaptive folding, critic independence, verified learning quarantine, 1,000-case replay and cognitive desktop trace.

- [ ] **Step 1: Extend acceptance matrix and exact coverage catalog without removing prior cases.**
- [ ] **Step 2: Extend traceability domains if needed; every new code surface maps to an executable test.**
- [ ] **Step 3: Generate final audit with RED run, implementation commits, focused/full tests, replay count, provider-safety verdicts and remaining non-blocking limitations.**
- [ ] **Step 4: Run full GitHub Actions matrix on exact final SHA; require Python 3.12 + 3.13 core success and Windows package success.**
- [ ] **Step 5: Require publish workflow success on the same final SHA when configured for automatic v0.2 publication.**
- [ ] **Step 6: Fetch artifact metadata/attestation evidence and verify SHA binding.**
- [ ] **Step 7: Only then mark implementation complete and update this plan’s checkboxes in a final documentation commit if that does not invalidate release SHA binding; otherwise leave release-bound audit as the source of truth.**

## Self-review

- Spec coverage: all approved sections are mapped to Tasks 2-12; Experiential extension is explicitly preserved.
- Placeholder scan: no implementation decisions are delegated to TODO/TBD placeholders.
- Type consistency: routing uses existing `CapabilityRequirement`/`ModelRoute` plus additive profile/quota contracts; cognitive state uses existing `StateStore`; learning extends `ExperienceCard` with backward-compatible defaults.
- Execution strategy: inline execution in this session is selected because the user explicitly requested uninterrupted completion and no subagent runtime is available in this harness.
