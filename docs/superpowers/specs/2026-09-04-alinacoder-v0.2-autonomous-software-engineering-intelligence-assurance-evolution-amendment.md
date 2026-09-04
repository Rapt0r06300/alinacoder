# AlinaCoder v0.2 — Autonomous Software Engineering Intelligence, Assurance & Evolution Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment is additive to the current AlinaCoder v0.2 specification stack.

It does **not** replace the existing:

- `IntentContract`, `GroundedIntentContract`, `ConstraintLedger` and Common Ground mechanisms;
- Repository Intelligence Graph;
- hypothesis-driven debugging;
- Done Contracts, regression gates, hidden holdouts and BestKnownState;
- Adaptive Zero-Cost Frontier Fabric, capability vectors, task affinity and switching hysteresis;
- Continuity Spine and stale-response rejection;
- unified `AlinaCoder.exe` conversation/workbench shell;
- local-first, zero-autonomous-spend, direct-to-`main`, safety, privacy and reversibility invariants.

It strengthens those mechanisms after a new research wave focused on:

1. coding intelligence and implicit requirement recovery;
2. executable specifications and architecture preservation;
3. causal debugging and self-correction;
4. long-horizon planning and localized replanning;
5. multi-model routing under drift;
6. memory integrity and long-lived authorization;
7. prompt-injection and context-privilege security;
8. anti-reward-hacking verification;
9. tool operability and recoverable execution;
10. speed, context efficiency and parallelism;
11. human steerability and `AlinaCoder.exe` observability;
12. safe self-evolution from verified project experience.

Where this amendment defines a stricter mechanism for these areas, it has precedence for the affected subsystem.

The governing objective becomes:

> **Understand the real requirement, materialize it into verifiable contracts, preserve architecture and prior guarantees over long horizons, diagnose failures causally, repair only what evidence justifies, route intelligence adaptively, and never let tests, memory, context, tools or autonomy silently become a false source of authority.**

---

# Part I — Cumulative research audit

## 2. Research is evidence, not automatic product scope

All findings in this amendment were audited against current normative mechanisms using the existing `SpecResearchAudit` verdicts:

```text
ACCEPT_NEW
MERGE_STRENGTHEN
WATCH
REJECT_REDUNDANT
REJECT_WEAK_EVIDENCE
REJECT_INCOMPATIBLE
```

A paper result does not become a runtime claim. It becomes a design candidate whose value must later be verified on AlinaCoder-specific hidden evaluations.

## 3. Accepted / merged research findings

### Coding intelligence and specification

| Finding | Source | Audit verdict | Normative consequence |
|---|---|---|---|
| Implicit requirement recovery remains a major bottleneck in repository coding agents | SWE-RPG, arXiv 2608.09072 | ACCEPT_NEW | Add `RequirementRecoveryGraph` and stage-specific requirement coverage before mutation |
| Architecture and behavior should both be executable specifications | CodeSpec, arXiv 2607.26777 | ACCEPT_NEW | Add `DualExecutableSpec`: architecture realization + behavior realization |
| Implicit assumptions can produce working-but-wrong code and should be linked to affected AST regions | AssumptionMiner, arXiv 2607.22898 | ACCEPT_NEW | Add `AssumptionLedger` with evidence, scope and code dependencies |
| Long-horizon agents need an explicit project state rather than a purely textual trajectory | long-horizon project-state / specification-faithfulness research | ACCEPT_NEW | Add semantic/structural project twin and drift checks |
| Repository pre-exploration improves vague issue understanding | CodeScout-style repository exploration research | MERGE_STRENGTHEN | Strengthen existing `RepositoryIntentEnricher`; no duplicate subsystem |
| Project history can teach repository-specific intent-to-code patterns | MemCoder, arXiv 2603.13258 | MERGE_STRENGTHEN | Strengthen validated project-history memory, never copy blindly |

### Debugging and self-correction

| Finding | Source | Audit verdict | Normative consequence |
|---|---|---|---|
| Runtime traces + causal analysis + rollback improve repair | TraceCoder, arXiv 2602.06875 | ACCEPT_NEW | Add causal instrumentation and repair frontier |
| Diagnosis and reproduction-test generation should be separated | DPIAgent, arXiv 2608.23341 | ACCEPT_NEW | Add typed diagnosis→reproduction-test handoff |
| Failing tests should be semantically purified before instrumentation | DebugRepair, arXiv 2604.19305 | ACCEPT_NEW | Add `FailureSlice` and bounded instrumentation |
| Minimal causal context reduces debugging noise | CausalRepair, arXiv 2608.10613 | ACCEPT_NEW | Add test-side + execution-side causal slicing |
| Patch self-review shares the same interpretation failure; reverse reconstruction adds independent signal | RETRACE, arXiv 2608.08950 | ACCEPT_NEW | Add `BidirectionalPatchVerifier` |
| File localization should carry actionable diagnosis, dependencies and test impact | SHERLOC, arXiv 2606.24820 | MERGE_STRENGTHEN | Strengthen repository localization output schema |
| Reusable failure memories should be written only after executable verification | ERRORPROBE, ACL Findings 2026 | MERGE_STRENGTHEN | Add verified-before-write debugging lesson gate |
| Not every intermediate multi-agent artifact has equal causal value | CAM, arXiv 2602.02138 | WATCH | Use evidence-value pruning only after AlinaCoder benchmark proof |

### Planning and tool execution

| Finding | Source | Audit verdict | Normative consequence |
|---|---|---|---|
| Holistic and stepwise planning fail differently; extra reflection can hurt short-horizon execution | Agent Planning Benchmark, arXiv 2606.04874 | ACCEPT_NEW | Route critique effort by planning level |
| Long-horizon planning needs local constraints plus global consistency | DEEPPLANNING, ACL 2026 | ACCEPT_NEW | Add global constraint sentinel |
| Recovery should escalate local→alternate→subgraph→global | HECG, arXiv 2603.08388 | ACCEPT_NEW | Add hierarchical recovery ladder |
| DAG subtask isolation prevents unrelated replanning and can reduce context cost | Task-Decoupled Planning, arXiv 2601.07577 | ACCEPT_NEW | Node-scoped execution contexts |
| Valid regions should be frozen and only the smallest affected subgraph repaired | Atomic Task Graph, arXiv 2607.01942 | ACCEPT_NEW | Add minimal affected subgraph repair |
| Structural plan verification catches dependency/type failures hidden by fluent narration | GNNVerifier, arXiv 2603.14730 | ACCEPT_NEW | Deterministic graph checks first; learned verifier optional |
| Tool composition improves when input/output/effect schemas form an explicit graph | HyperAgent, arXiv 2608.02650 | ACCEPT_NEW | Add `ToolSchemaGraph` and subgoal effect proof |
| Strategic monitoring and context curation should be separate from tactical execution | COMPASS, ACL 2026 | MERGE_STRENGTHEN | Strengthen existing critic/context-manager roles; avoid permanent agent proliferation |

### Routing, speed and model selection

| Finding | Source | Audit verdict | Normative consequence |
|---|---|---|---|
| Execution-grounded routing memory reduces cumulative regret | Agent-as-a-Router / ACRouter, arXiv 2606.22902 | MERGE_STRENGTHEN | Existing delayed-credit router gains explicit routing-regret metric |
| Task-level affinity and terminal reward matter | TRACE-Router, arXiv 2607.22465 | REJECT_REDUNDANT | Already normative through `TaskAffinityLease` + delayed terminal credit |
| Capability-vector routing decoupled from model IDs | HyDRA, arXiv 2605.17106 | REJECT_REDUNDANT | Already normative through requirement/capability vectors + shortfall matching |
| Nonstationary workloads require rolling drift evidence and shadow audits | Drift-Aware Sparse Routing, arXiv 2609.00662 | ACCEPT_NEW | Add `RouterDriftWindow` and safe `ShadowAuditStream` |
| Output length predicts latency/resource cost | FLARE, ACL 2026 | ACCEPT_NEW | Add `OutputEnvelopePredictor`; cannot override quality/safety floors |
| Routing should compute only signals relevant to active decisions | vLLM Semantic Router, arXiv 2603.04444 | ACCEPT_NEW | Add demand-driven routing signal budget and early termination |
| Same-function provider routing should not trade bad quality for low latency | LQM-ContextRoute, arXiv 2605.14241 | MERGE_STRENGTHEN | Host routing treats latency as capacity after quality equivalence |
| Lightweight task ontology can predict task type/difficulty/reasoning mode/output length | SCX Router, arXiv 2609.02292 | WATCH | Candidate local router only after French/project-specific hidden evaluation |

### Verification and anti-gaming

| Finding | Source | Audit verdict | Normative consequence |
|---|---|---|---|
| Visible tests can be saturated while held-out composed behavior fails; gap worsens with system size | SpecBench, arXiv 2605.21384 | ACCEPT_NEW | Add anti-reward-hacking assurance and composition oracles |
| Existing hidden holdouts and anti-gaming are necessary but too evaluation-centric | current v0.2 final design | MERGE_STRENGTHEN | Extend anti-gaming into ordinary code promotion, not only self-improvement |
| Tests alone cannot prove semantic/architectural faithfulness | CodeSpec + SpecBench + long-horizon benchmarks | ACCEPT_NEW | `GREEN_TESTS != DONE` becomes explicit invariant |

### Security, memory and authority

| Finding | Source | Audit verdict | Normative consequence |
|---|---|---|---|
| Harness context assembly can elevate low-privilege content into higher message/scope authority | Context Privilege Escalation, arXiv 2609.01222 | ACCEPT_NEW | Add instruction privilege labels and non-escalation gate |
| Persistent memory can invent authorization absent from source history | Endogenous Authorization Laundering, arXiv 2609.01836 | ACCEPT_NEW | Add source-backed authorization event ledger |
| Persistent agents benefit from information-flow labels across planning/execution/state reuse | SPA, arXiv 2608.27234 | ACCEPT_NEW | Add confidentiality/integrity labels to artifacts and effect flows |
| Raw tool/RAG outputs should not directly contaminate privileged long-horizon context | AGENTSYS, arXiv 2602.07398 | ACCEPT_NEW | Add isolated observation workers + typed return bridge |
| Destination allowlists and capability isolation can outperform surface prompt-injection filters | Framing Gap, arXiv 2608.27092 | ACCEPT_NEW | Add egress allowlists and planner/reader capability separation |
| Tool exposure should follow least privilege | adaptive capability-governance research | MERGE_STRENGTHEN | Add deterministic `CapabilityExposureMask`; learned governor remains optional |
| Simply removing a memory tool can open another attack path | persistent-memory defense research, arXiv 2605.08442 | ACCEPT_NEW | Security changes require whole attack-graph regression tests |

### Human interface, autonomy and operability

| Finding | Source | Audit verdict | Normative consequence |
|---|---|---|---|
| Valid tool calls are insufficient if the agent cannot tell whether effects committed or resume after failures | Agent-First Tooling / AFT-Bench, arXiv 2608.23628 | ACCEPT_NEW | Add `ToolOperabilityContract` with durable invocation/effect/postcondition semantics |
| Direct manipulation complements natural language and encourages incremental, inspectable edits | Direct Manipulation + Natural Language Programming, arXiv 2608.26359 | MERGE_STRENGTHEN | Strengthen existing `UIConversationAct` with structured edit operations |
| Developers benefit from breakpoint/step/replay views for agent trajectories | AgentStepper, arXiv 2602.06593 | ACCEPT_NEW | Add optional `RunInspector` diagnostic mode inside `AlinaCoder.exe` |
| Oversight preference can evolve across tasks | Dynamic Autonomy for Coding Agents, arXiv 2605.11495 | MERGE_STRENGTHEN | Add adaptive interruption policy, but never auto-expand hard authority |
| Human control and autonomous performance can coexist in a shared workbench | ResearStudio, EMNLP demos 2025 | MERGE_STRENGTHEN | Reinforce pause/resume/takeover/live artifact model already normative |

## 4. Findings deliberately not promoted as mandatory architecture

The following remain non-normative unless future AlinaCoder-specific evidence justifies promotion:

- mandatory RL-trained capability governance;
- mandatory GNN planner/verifier;
- mandatory multi-agent fan-out for every task;
- exposing private model chain-of-thought in the UI;
- replacing deterministic tests with LLM judges;
- replacing local canonical memory with Supabase;
- relying on alpha Supabase Vector Buckets;
- routing based on public leaderboards without project-specific evidence;
- globally replanning after every local failure;
- treating every generated assumption as user-approved truth;
- treating every passing agent-generated test as proof of correctness.

---

# Part II — Executable intent and project truth

## 5. Requirements must become machine-checkable where possible

Natural-language intent remains authoritative, but long-horizon coding SHALL compile the active requirement set into structured, versioned, evidence-linked artifacts.

Canonical flow:

```text
User wording
→ GroundedIntentContract
→ RequirementRecoveryGraph
→ AssumptionLedger
→ FunctionalChainGraph
→ DualExecutableSpec
→ implementation candidates
→ independent assurance
```

This compilation is a projection of the user's intent, not a replacement for it.

## 6. RequirementAtom

Every implementation-critical requirement SHOULD be represented as:

```text
RequirementAtom
- requirement_id
- normalized_statement
- source_type
- source_pointer
- status
- confidence
- explicit_or_implicit
- supersedes
- depends_on
- conflicts_with
- observable_effects
- architecture_constraints
- validation_routes
- user_locked
```

Statuses:

```text
EXPLICIT_CONFIRMED
EXPLICIT_ACTIVE
INFERRED_SUPPORTED
AMBIGUOUS
CONFLICTED
SUPERSEDED
VERIFIED
UNVERIFIABLE
```

An `INFERRED_SUPPORTED` atom does not gain the authority of an explicit user instruction.

## 7. RequirementRecoveryGraph

Before medium/high-impact repository mutation, AlinaCoder SHALL recover implementation-critical requirements from:

- current user wording;
- GroundedIntentContract and ConstraintLedger;
- tests and fixtures;
- public interfaces and schemas;
- repository architecture and patterns;
- current specification files;
- recent corrections;
- verified project-history evidence;
- explicit examples approved by the user;
- known non-functional requirements when evidenced.

Edges include:

```text
SUPPORTED_BY
IMPLIES
REQUIRES
CONFLICTS_WITH
SUPERSEDES
OBSERVED_IN
VALIDATED_BY
AFFECTS
```

The graph must preserve source provenance so inferred implementation detail can never masquerade as user authority.

## 8. AssumptionLedger

Every material design choice that is neither explicit nor mechanically forced SHOULD be recorded when it can change externally visible behavior or architecture.

Fields:

```text
assumption_id
statement
alternatives_considered
basis
confidence
scope
risk_if_wrong
affected_symbols
affected_requirements
status
```

Statuses:

```text
TENTATIVE
SUPPORTED
USER_CONFIRMED
REJECTED
SUPERSEDED
INVALIDATED
```

Important rules:

1. assumptions are inspectable evidence, not hidden model commitments;
2. low-impact conventional assumptions may proceed reversibly;
3. high-impact uncertain assumptions trigger targeted evidence gathering or concise clarification;
4. a changed assumption invalidates only the code/tests/plans that depend on it;
5. extracted assumptions must be benchmarked because extraction itself is imperfect.

## 9. ArchitectureBeliefGraph

The existing Repository Intelligence Graph describes observed code structure. A separate `ArchitectureBeliefGraph` SHALL represent what AlinaCoder currently believes the repository architecture *means* and which invariants it is expected to preserve.

Node examples:

```text
component
boundary
responsibility
public contract
data owner
lifecycle
extension point
invariant
feature entry point
observable effect
```

Evidence state per belief:

```text
OBSERVED
INFERRED
VERIFIED
STALE
CONTRADICTED
SUPERSEDED
```

No belief may silently outrank live repository evidence.

## 10. SemanticStructuralProjectTwin

Maintain two synchronized but non-identical project views:

```text
SemanticProjectState
= active goals + requirements + architecture intent + user decisions + invariants

StructuralProjectState
= files + symbols + dependencies + schemas + tests + builds + runtime topology
```

`ProjectDriftDetector` compares them after material changes.

Important drift classes:

```text
BEHAVIOR_MISSING
ARCHITECTURE_CHAIN_BROKEN
STALE_IMPLEMENTATION
UNINTENDED_NEW_SURFACE
ORPHAN_IMPLEMENTATION
CONSTRAINT_VIOLATION
SPEC_IMPLEMENTATION_DIVERGENCE
```

## 11. FunctionalChainGraph

For cross-component feature work, derive a traceable chain:

```text
requirement
→ entry point
→ participating components
→ data/control transitions
→ state changes
→ external/observable effect
→ verification point
```

Every transition SHOULD retain repository evidence.

This is particularly important for features that pass isolated unit tests yet fail when components must work together.

## 12. DualExecutableSpec

For medium/high-complexity feature development, AlinaCoder SHOULD compile complementary executable contracts:

### Architecture executable spec

Checks structural realization such as:

- required symbol/interface exists;
- required call/dependency chain exists;
- expected extension point is used;
- prohibited coupling is absent;
- schema/interface relationship remains valid;
- feature path reaches required component boundary.

### Behavior executable spec

Checks observable behavior such as:

- fail-to-pass scenario;
- happy path;
- edge/error path;
- state transition;
- output/effect;
- cross-feature composition;
- regression behavior.

Neither contract alone is enough for high-risk long-horizon feature work.

## 13. Spec derivation is itself verified

Generated executable specs SHALL be checked against:

```text
original user wording
active RequirementAtoms
repository evidence
known interfaces/invariants
existing tests
contradictions
```

A faulty generated test or architecture check must not become self-authorizing simply because AlinaCoder wrote it.

---

# Part III — Causal debugging and bounded self-correction

## 14. Debugging is diagnosis before repair

Canonical nontrivial debug loop:

```text
symptom
→ reproduce
→ purify failing condition
→ localize
→ hypotheses
→ discriminate
→ minimal causal context
→ repair candidate
→ verify target
→ verify regressions
→ independent patch alignment
→ promote / reject / rollback
```

## 15. FailureEvidencePacket

A failure packet MAY contain:

```text
symptom
reproduction command
failing assertions
stack/error output
baseline state
relevant runtime values
execution path
changed files
recent related commits
active requirements
known-good checkpoint
```

Raw output remains accessible, but the working diagnostic context should contain only evidence relevant to the failure.

## 16. TestSemanticPurifier

When a failing test contains multiple unrelated scenarios/assertions, isolate the minimal failing semantics before using it to guide repair.

The purified representation records which initialization and dependencies are required so simplification does not accidentally change the failure.

## 17. MinimalCausalContextBuilder

Construct the smallest useful causal debugging context from:

```text
purified failing test
static dependency slice
dynamic execution trace
data/control dependencies
relevant state transitions
nearest boundary contracts
contradicting evidence
```

Static over-approximation alone is insufficient when dynamic evidence is available.

## 18. InstrumentationPlanner

For failures not explained by existing evidence, AlinaCoder MAY insert temporary diagnostic probes.

Instrumentation rules:

- bounded scope;
- semantics-preserving where practical;
- no production promotion with accidental debug probes;
- capture only values/events relevant to active hypotheses;
- record inserted locations;
- automatically remove/revert after diagnosis;
- treat instrumentation output as evidence, not truth.

## 19. DiagnosticHypothesisLedger

Strengthen the existing hypothesis mechanism with:

```text
hypothesis_id
root_cause_claim
predicted_observation
discriminating_probe
support
disconfirmation
causal_scope
status
failed_repair_attempts
```

Statuses:

```text
OPEN
SUPPORTED
FALSIFIED
SUPERSEDED
CONFIRMED_ENOUGH_TO_PATCH
```

## 20. Diagnosis→reproduction-test protocol

Bug reproduction and bug repair SHALL not collapse into one opaque generation loop.

For difficult bugs:

```text
DiagnosisArtifact
→ ReproductionTestPlan
→ failing reproduction proof
→ RepairPlan
```

The reproduction test must fail on the relevant pre-fix state and pass on the accepted post-fix state when technically possible.

## 21. RepairAttemptGraph

Repair attempts SHALL retain lineage:

```text
candidate
parent_state
hypothesis
patch_scope
verification_vector
new_failures
regressions
lesson
```

A failed child does not overwrite a superior parent.

## 22. BestKnownStateFrontier

The existing BestKnownState becomes a frontier rather than a single naive score.

Lexicographic priority remains:

```text
safety
→ target behavior
→ prior regression preservation
→ architecture/spec alignment
→ build/static/type health
→ verification independence
→ patch risk/surface
→ unresolved uncertainty
```

Passing one extra unrelated test cannot outrank a cleaner candidate that preserves critical invariants.

## 23. Debug stagnation and session reset

If repair cycles repeat without information gain:

```text
same location edits
same failure
same rejected hypothesis
no verification-vector improvement
trace contradiction
context pollution
```

then AlinaCoder SHALL stop patch-churn and choose among:

```text
NEW_PROBE
WIDEN_LOCALIZATION
ALTERNATIVE_HYPOTHESIS
RESET_DEBUG_REASONING_FROM_CANONICAL_EVIDENCE
MODEL_SPECIALIST_SWITCH_AT_CHECKPOINT
RESTORE_BEST_KNOWN_STATE
```

A reset preserves verified facts and rejected lessons but discards polluted speculative reasoning.

## 24. BidirectionalPatchVerifier

For medium/high-risk patches, add an independent alignment signal:

### Forward reconstruction

```text
original requirement + verified evidence
→ intended repair responsibilities
```

### Backward reconstruction

Using the candidate patch and relevant execution evidence **without the original request text**:

```text
patch
→ infer which problem / behavior this patch appears to address
```

### Reconciliation

Compare:

```text
intended problem
vs
problem implied by patch
```

Possible verdicts:

```text
ALIGNED
PARTIAL
WRONG_PROBLEM
OVERBROAD
UNDERBROAD
ARCHITECTURE_MISMATCH
INSUFFICIENT_EVIDENCE
```

The backward verifier must not receive the original wording that could anchor it to the same interpretation failure.

## 25. Verified-before-write debugging memory

A debugging lesson may enter durable reusable memory only after evidence such as:

- reproducible failure;
- falsified/confirmed hypothesis;
- accepted patch;
- regression outcome;
- relevant scope.

Unverified model explanations remain ephemeral.

---

# Part IV — Executable task graphs and localized replanning

## 26. ExecutableTaskGraph

Long-running work SHALL be represented as a typed DAG when dependency structure materially matters.

Each node records:

```text
node_id
local_goal
input_contract
output_contract
preconditions
expected_effects
tool_capability_requirements
verification_contract
risk_class
status
upstream_dependencies
downstream_consumers
```

## 27. Node-scoped context

A node receives:

```text
active local goal
required upstream outputs
relevant constraints
relevant project state
local evidence/history
```

It SHOULD NOT inherit unrelated sibling traces merely because they occurred earlier.

Global invariants remain pinned separately.

## 28. ToolSchemaGraph

Tool discovery SHALL model more than tool names/descriptions.

Each tool route records:

```text
required input schema
output schema
side effects
idempotency class
permissions
external dependencies
failure semantics
resume semantics
verification hooks
```

Edges represent producer→consumer schema/effect compatibility.

This supports structural tool planning rather than repeated semantic guessing.

## 29. PlanStructuralVerifier

Before execution of a material DAG region, deterministic checks SHOULD validate where applicable:

```text
missing prerequisites
schema/type mismatches
cycles where forbidden
unbound inputs
invalid effect ordering
permission mismatch
unreachable required output
contradictory constraints
```

An optional learned/GNN verifier may add evidence later, but cannot replace deterministic checks until measured superior on hidden AlinaCoder cases.

## 30. SubgoalEffectProof

A successful tool/API process exit does not necessarily mean the subgoal succeeded.

A node becomes `DONE` only when its expected output/effect is evidenced.

Examples:

```text
file write call succeeded != desired content verified
push request returned != remote main HEAD verified
process started != service healthy
migration command exited 0 != schema state verified
email/send API accepted != semantic delivery assumptions proven
```

## 31. Hierarchical recovery ladder

On failure, choose the smallest sufficient correction scope:

```text
L0 RETRY_TRANSIENT
L1 LOCAL_ACTION_CORRECTION
L2 ALTERNATIVE_TOOL_OR_METHOD
L3 NODE_REPLAN
L4 MINIMAL_AFFECTED_SUBGRAPH_REPLAN
L5 GLOBAL_REPLAN
L6 BLOCK / USER_DECISION_ONLY_IF_MATERIAL_AMBIGUITY_REMAINS
```

Do not jump to global replanning because one leaf failed.

## 32. MinimalAffectedSubgraphReplanner

When a node or assumption changes:

1. identify causal upstream cause;
2. compute affected downstream closure;
3. freeze verified unaffected nodes;
4. repair/recompute only affected region;
5. revalidate boundary interfaces;
6. reintegrate into main DAG.

## 33. GlobalConstraintSentinel

Parallel/local execution can be individually correct yet globally inconsistent.

Maintain continuous checks for:

```text
active user constraints
resource ceilings
repository invariants
version compatibility
cross-node state consistency
conflicting outputs
ordering constraints
Done Contract completeness
```

## 34. Reflection budget by planning level

Use deliberate critique where it has expected value.

```text
holistic/high-level plan
→ stronger structural critique and alternative checking

short local execution step with fresh feedback
→ minimal reflection unless anomaly evidence exists
```

Endless self-reflection is forbidden.

## 35. Safe parallel graph execution

Nodes MAY execute concurrently only if their read/write/effect sets are proven sufficiently independent.

Before parallel execution determine:

```text
file overlap
shared mutable state
tool/provider quota interactions
Git/worktree collision risk
external side-effect conflicts
verification dependency
```

Otherwise serialize.

---

# Part V — Verification beyond visible tests

## 36. Green tests are necessary evidence, not semantic authority

New invariant:

> **`VISIBLE_TESTS_GREEN` is not equivalent to `DONE`.**

The Done Contract must consider whether the implementation genuinely composes the required behavior and preserves architecture/intent.

## 37. TestAuthorityLevel

Verification artifacts SHALL carry provenance/authority:

```text
REPO_PREEXISTING
USER_CONFIRMED
SPEC_DERIVED
AGENT_GENERATED
METAMORPHIC
DIFFERENTIAL
MUTATION
COMPOSITION
VALIDATION_HOLDOUT
HIDDEN_HOLDOUT
EXTERNAL_STANDARD
```

No single level is universally sufficient.

## 38. AntiRewardHackingGate

For long-horizon or high-impact code, detect patterns including:

```text
hardcoded visible test inputs
special-casing test harness behavior
disabling/skipping validation
weakening assertions
rewriting tests instead of implementation
mocking away required integration
feature implementations that do not share required state
fake success paths
benchmark-specific shortcuts
modifying verifier configuration
```

## 39. Composition assurance

When multiple features/subsystems must interoperate, validation SHALL include composed behavior rather than only isolated feature tests.

Examples:

```text
A works
B works
C works
```

does not prove:

```text
A + B + C work together under the real state/lifecycle
```

## 40. Independent oracle diversity

Depending on task risk, combine independent evidence such as:

- existing repository tests;
- hidden/held-out tests;
- generated reproduction tests;
- architecture checks;
- behavior contracts;
- metamorphic relations;
- differential reference behavior;
- mutation testing;
- static/type/schema checks;
- runtime postconditions;
- backward patch reconstruction.

Independence matters more than merely running more checks derived from the same mistaken interpretation.

## 41. Verifier integrity boundary

Mandatory verifier assets SHALL be protected from ordinary candidate mutation.

Sensitive examples:

```text
hidden tests
promotion evaluator
safety policy
Git ownership checks
cost policy
permission policy
benchmark scoring
```

If modification is legitimately required, it becomes a separate explicit task with stronger review/evidence.

## 42. RewardHackingGap metric

For internal benchmarks where visible and held-out suites exist:

```text
RewardHackingGap = visible_proxy_score - independent_holdout_score
```

Track by:

```text
model
agent policy
task horizon
LOC/change size
feature count
repair iteration count
```

Promotion SHOULD penalize large positive gaps even when visible score is perfect.

---

# Part VI — Routing intelligence under drift

## 43. Existing capability routing remains canonical

Do not replace:

```text
CapabilityRequirementVector
ModelCapabilityVector
ShortfallMatcher
TaskAffinityLease
SwitchUtilityCalculator
DelayedCreditAssigner
CostProofReceipt
```

This amendment adds dynamic efficiency and drift control around them.

## 44. RouterDriftWindow

Maintain a rolling evidence window over route outcomes so old capability observations do not dominate after:

```text
model update
provider behavior change
quantization change
endpoint change
load regime shift
prompt/harness change
benchmark distribution drift
```

Evidence records include both long-term prior and recent-window posterior.

## 45. RoutingDriftDetector

Detect statistically/practically material changes in:

```text
terminal success
schema validity
tool-call validity
regression misses
latency
quota failures
context failures
handoff continuity
French intent fidelity
```

A drift alert does not instantly demote a model; it triggers conservative remeasurement.

## 46. ShadowAuditStream

A small bounded fraction of **safe** cases MAY evaluate multiple eligible routes to maintain fresh comparative evidence.

Allowed:

```text
synthetic tasks
hidden benchmark tasks
read-only replay
already-completed tasks
non-mutating candidate inference
```

Forbidden:

```text
duplicate live writes
duplicate external effects
extra paid calls
secret-bearing prompts to ineligible providers
rate-limit abuse
```

## 47. RoutingSignalBudget

Signal extraction itself has cost/latency.

Only compute routing signals referenced by currently viable decisions.

Preferred ordering:

```text
cheap deterministic exclusions
→ privacy/cost/capability hard gates
→ high-information lightweight signals
→ expensive learned signal only if choice remains ambiguous
```

Short-circuit once the routing outcome is stable enough.

## 48. OutputEnvelopePredictor

Estimate per candidate:

```text
expected_output_tokens
expected_context_growth
expected_latency
local VRAM/RAM pressure
likely tool-call count
likely stage duration
```

Use these only among candidates that already satisfy hard safety/capability/zero-cost gates.

A fast weak route cannot win by predicting shorter output.

## 49. Same-function host selection

When multiple routes are cognitively equivalent enough for hosting failover:

1. establish acceptable quality equivalence;
2. then optimize health, latency, throughput, cache locality and quota survival.

Latency is a service-capacity factor, not permission to select an inferior answer route.

## 50. Routing regret

Track:

```text
terminal routing regret
switch regret
missed-specialist regret
premature-switch regret
stale-route regret
```

Use verified task outcomes, not model self-ratings.

---

# Part VII — Context, memory and authorization security

## 51. Every context item has provenance and privilege

A context item SHALL carry:

```text
source
scope
integrity_label
confidentiality_label
instruction_privilege
freshness
persistence_scope
```

The context compiler must preserve these labels across summaries, memories, handoffs and model switches.

## 52. InstructionPrivilegeLattice

At minimum distinguish:

```text
SYSTEM_POLICY
USER_EXPLICIT
USER_DERIVED_CONFIRMED
PROJECT_TRUSTED_POLICY
PROJECT_DATA
TOOL_RESULT_TRUSTED_STRUCTURED
TOOL_RESULT_UNTRUSTED
WEB_UNTRUSTED
MEMORY_DERIVED
MODEL_GENERATED
```

Lower-privilege content cannot become a higher-privilege instruction merely because it was summarized or moved into a different message field.

## 53. ContextPrivilegeNonEscalationGate

Before compiling model context, reject or downgrade transformations that:

- copy web/tool data into system/developer authority;
- turn retrieved prose into an executable command;
- persist temporary attacker-controlled instructions across scopes;
- treat assistant-generated summaries as user authorization;
- strip provenance from a sensitive rule;
- merge conflicting privilege levels into an unlabeled summary.

## 54. UntrustedObservationWorker

Raw untrusted web/RAG/tool content SHOULD be processed in an isolated, non-effect-authorized worker context when practical.

The privileged orchestrator receives only a schema-constrained result such as:

```text
facts
source pointers
confidence
requested fields
validation status
```

not arbitrary instruction-bearing prose unless the task explicitly requires inspection.

## 55. SchemaConstrainedObservationBridge

Before untrusted observations enter privileged working context:

1. predeclare expected fields/types;
2. extract only those fields;
3. validate schema;
4. retain raw source pointer outside privileged context;
5. reject malformed or instruction-smuggling output;
6. allow bounded re-extraction/sanitization;
7. fail safely when uncertainty persists.

## 56. MemoryWriteTrustGate

Durable memory write requires:

```text
provenance
scope
trust classification
conflict check
sensitivity check
instruction-content check
freshness policy
```

Memories containing external instructions are quarantined as data unless independently authorized.

## 57. AuthorizationEventLedger

Permissions, prohibitions, approvals and revocations SHALL NOT be represented only as free-form memory summaries.

Maintain bounded event sourcing:

```text
AuthorizationEvent
- event_id
- principal
- capability
- scope
- action
- source
- explicitness
- effective_from
- effective_until
- supersedes
- signature/provenance where available
```

Authorization actions:

```text
GRANT
DENY
REVOKE
LIMIT
CONFIRM
EXPIRE
```

## 58. No authorization laundering

A summary such as:

```text
"the user usually lets me commit"
```

cannot create permission to commit.

Only valid source-backed authorization events and hard project policy determine effect authority.

Current explicit user instruction may narrow/override according to governing policy, but derived memory cannot silently broaden authority.

## 59. CrossScopePersistenceGate

Before carrying information across:

```text
turn → task
session → session
project → project
user → global
worker → orchestrator
model → replacement model
```

check whether its persistence scope permits the transfer.

## 60. CapabilityExposureMask

Even when AlinaCoder is broadly autonomous, a given task/stage SHOULD expose only tools relevant to that scope.

Examples:

```text
research stage: read/search tools, no destructive Git
planning stage: inspect/graph tools, no external effect
coding stage: workspace-limited write/test tools
verification stage: mostly read/test/postcondition tools
commit stage: Git effect tools only after Done Contract
```

Hard capability policy is deterministic.

A learned policy may later reduce unnecessary interruptions/tool exposure, but SHALL NOT independently grant stronger authority than hard policy permits.

## 61. Egress and destination policy

Network/external-effect tools SHOULD support deterministic destination restrictions:

```text
allowed hosts/domains
allowed protocols
allowed repositories
allowed accounts/projects
blocked private/local network ranges where relevant
```

Untrusted content cannot authorize a new destination.

## 62. Whole-attack-graph regression

Security hardening can change behavior in unexpected ways.

When disabling/removing a capability or memory route, test whether another path becomes more dangerous.

Security evaluation must cover alternate pathways rather than assuming “less capability = always safer.”

---

# Part VIII — Tool operability and recoverable effects

## 63. Callability is not enough

Every important tool should expose enough operational state for the agent to know what actually happened.

## 64. ToolOperabilityContract

Tool metadata SHOULD include:

```text
capability_id
input_schema
output_schema
side_effect_class
idempotency
invocation_id_support
resume_support
durable_state_support
commit_semantics
postcondition_check
permission_scope
retriable_errors
unknown_outcome_policy
```

## 65. Effect states

Canonical effect lifecycle:

```text
PROPOSED
ADMITTED
STARTED
COMMITTED
POSTCONDITION_VERIFIED
FAILED_NO_EFFECT
FAILED_EFFECT_UNKNOWN
ROLLED_BACK
```

A response timeout after `COMMITTED` must not be treated like `FAILED_NO_EFFECT`.

## 66. Idempotency and duplicate-effect protection

For side-effecting tools:

- use stable invocation/idempotency keys when supported;
- persist invocation state before execution;
- after response loss, query/reconcile world state before retrying;
- never blindly retry an unknown-effect mutation.

## 67. Resumable invocation

Long-running tools SHOULD expose durable handles/checkpoints where technically possible.

`resume` and `restart` are different operations and must be represented separately.

## 68. PostconditionVerifier

Terminal claims about tool actions require external/world-state evidence where available.

Examples:

```text
Git push → remote ref check
file write → content/hash check
build → artifact check
server start → health check
migration → schema inspection
```

## 69. Selective capability discovery

Large tool catalogs SHOULD be searched dynamically rather than placed entirely into every prompt.

Discovery uses:

```text
task capability requirement
stage
schema compatibility
permission scope
prior tool reliability
```

This reduces context pollution and attack surface simultaneously.

---

# Part IX — Fast intelligence without reckless shortcuts

## 70. Speed architecture

Optimize user-perceived speed through parallelism and precomputation outside semantic commitment paths.

Preferred mechanisms:

```text
incremental repository indexing
stage-scoped context
predictive read-only prefetch
selective tool discovery
demand-driven router signals
parallel independent DAG nodes
incremental impacted-test ordering
cached deterministic analysis keyed by state hash
event-boundary memory consolidation
provider/local-model warm readiness
```

## 71. Critical-path separation

Keep latency-critical conversation/UI work separate from slow background operations where possible.

```text
critical path:
input → grounding → safe first response/status → action admission

async paths:
index refresh
memory consolidation
shadow routing audit
non-urgent research enrichment
artifact projection
```

A slow background component SHALL NOT block STOP, PAUSE, user correction or intent updates.

## 72. Evidence-aware incremental verification

Verification may order checks for fastest useful feedback:

```text
syntax/schema
→ directly affected tests
→ fail-to-pass
→ pass-to-pass impact set
→ architecture/behavior contracts
→ composition/metamorphic/holdout where required
→ broader suite
```

Early failure can cancel unnecessary downstream work, but final promotion still requires the full task-specific Done Contract.

## 73. Cache safety

Cache keys for semantic/engineering artifacts SHALL include relevant versions such as:

```text
repo HEAD/worktree fingerprint
requirement version
spec version
tool schema version
model/profile generation
dependency lock state
```

Stale cached evidence cannot authorize mutation.

## 74. Event-boundary memory consolidation

Prefer consolidation after meaningful events:

```text
subtask complete
requirement changed
failure localized
patch accepted/rejected
plan revised
commit verified
```

rather than repeatedly summarizing every token/turn.

---

# Part X — Adaptive autonomy without authority drift

## 75. Full autonomy remains the product default

This amendment does not convert AlinaCoder into an approval-heavy assistant.

The intended normal behavior remains:

```text
understand
→ investigate
→ plan
→ execute reversible/authorized work
→ verify
→ recover
→ commit main when contract is green
```

without unnecessary interruptions.

## 76. AutonomyEnvelope

Every task/stage has an inspectable envelope:

```text
allowed capability classes
workspace scope
network scope
maximum side-effect class
required evidence gates
check-in triggers
rollback availability
```

The envelope is derived from hard policy + explicit user authorization + current task scope.

## 77. Adaptive check-in policy

User interaction history MAY tune *when to interrupt* for familiar low-risk decisions.

It MAY learn:

```text
which reversible edits usually proceed silently
which design choices the user repeatedly rejects
which status updates the user wants
which paths/components deserve extra caution
```

It SHALL NOT learn new legal/security authority merely from repeated behavior.

## 78. Check-in sources remain distinct

UI diagnostics distinguish:

```text
POLICY_REQUIRED
MODEL_UNCERTAINTY
MATERIAL_INTENT_AMBIGUITY
PLAN_DEVIATION
SECURITY_BOUNDARY
EXTERNAL_ENROLLMENT
```

so the user can tell why autonomy paused.

## 79. Intervention becomes immediate canonical evidence

When the user edits a plan, diff, file, constraint, selected object or tool action inside `AlinaCoder.exe`, the event immediately updates canonical state and invalidates stale in-flight candidates.

No model may continue from the pre-intervention state version.

---

# Part XI — `AlinaCoder.exe` workbench improvements

## 80. One product surface remains canonical

Normal conversation, voice, coding, plans, files, diffs, tests, evidence, activity, model routing, memory and recovery SHALL remain inside `AlinaCoder.exe` except unavoidable trusted external enrollment/OS surfaces.

## 81. Progressive interface modes

The same `.exe` SHOULD expose three levels without creating separate products:

```text
CONVERSATION
WORK
DIAGNOSTIC
```

### Conversation

Minimal, natural chat/voice.

### Work

Plan, files, diffs, tests, active constraints, evidence.

### Diagnostic

Detailed execution timeline, tool invocations, effect states, routing/recovery/security evidence.

## 82. RunInspector

Diagnostic mode MAY provide debugger-like controls over **agent execution state**, not private model chain-of-thought:

```text
pause at semantic checkpoint
step to next material event
resume
inspect action inputs/outputs
inspect pre/postconditions
inspect intermediate diff
compare checkpoints
edit plan/constraint
replace/cancel pending action before commitment
```

## 83. Semantic breakpoints

Useful breakpoints include:

```text
BEFORE_MUTATION
AFTER_MUTATION
BEFORE_EXTERNAL_EFFECT
AFTER_EFFECT_BEFORE_VERIFICATION
ON_TEST_FAILURE
ON_PLAN_DEVIATION
ON_MODEL_SWITCH
BEFORE_COMMIT
ON_SECURITY_BLOCK
```

These are optional user controls; normal autonomous operation does not stop at every breakpoint.

## 84. ActionReceiptCard

Every material action card SHOULD answer succinctly:

```text
What did AlinaCoder try?
What actually happened?
Was there a side effect?
How was it verified?
Can it be resumed/retried/rolled back?
```

Example states:

```text
Running
Committed — verification pending
Verified
Failed — no effect
Outcome uncertain — reconciling
Rolled back
```

## 85. LiveDiffTimeline

For long coding tasks, allow the user to inspect how code changed between semantic checkpoints without reading a giant final diff.

Rejected/rolled-back candidates remain visually separated from canonical accepted state.

## 86. Direct manipulation uses a shared edit language

Natural language and UI editing SHOULD compile into common structured operations where possible:

```text
SELECT_TARGET
SET_CONSTRAINT
REPLACE_PLAN_NODE
ACCEPT_HUNK
REJECT_HUNK
REORDER_SAFE_NODES
PIN_REQUIREMENT
ROLLBACK_CHECKPOINT
FOCUS_EVIDENCE
```

This prevents text commands and mouse actions from creating divergent hidden meanings.

## 87. Fast resumption

After returning to the app, show a bounded summary:

```text
current goal
last verified checkpoint
what changed
what is still running
what failed/recovered
whether external effects occurred
what remains
what needs user attention, if anything
```

---

# Part XII — Memory and self-evolution from verified software history

## 88. ProjectExperienceUnit

Verified reusable software experience SHOULD be structured as:

```text
trigger/problem pattern
repository context
requirements involved
root cause or design rationale
action strategy
verification evidence
failure modes
applicability scope
staleness conditions
source commits/turns
```

## 89. Human-validated history is strong but not universal

Past merged/verified project solutions are useful priors for repository conventions.

Before reuse, check:

```text
same architecture generation
same dependency regime
same requirement pattern
no superseding design decision
no known regression
```

## 90. VerifiedExperiencePromotion

Experience promotion requires positive external evidence.

```text
MODEL_SUGGESTED
→ OBSERVED
→ VERIFIED_INSTANCE
→ REPEATED_OR_STRONG_SINGLE_CASE
→ REUSABLE_SCOPED_EXPERIENCE
```

No self-authored narrative jumps directly to durable policy.

## 91. History-to-benchmark factory

Repository history MAY produce safe self-improvement/evaluation tasks using a three-state reconstruction:

```text
healthy_before
→ task/problem state
→ verified_restored_after
```

Generated cases must be checked for leakage, determinism and valid oracle reconstruction before entering evaluation.

## 92. Self-improvement cannot optimize only proxy tests

Promotion of AlinaCoder changes SHALL compare:

```text
visible development score
hidden/holdout score
reward-hacking gap
regression rate
security floors
conversation quality
routing stability
resource cost
```

## 93. BenchmarkDriftDetector

The self-improvement lab SHALL detect when benchmarks become stale because:

```text
repository architecture changed
provider/model generation changed
known cases leaked
success saturates without real-world improvement
failure distribution shifted
```

Stale benchmarks are replaced or supplemented without deleting historical evidence.

---

# Part XIII — Optional Supabase role

## 94. Supabase remains optional and non-canonical

Local SQLite/event logs remain the canonical source for basic execution, conversation, authorization and recovery.

If configured, Supabase MAY mirror non-secret analytical/evaluation data.

## 95. Hybrid retrieval mirror

For eligible mirrored knowledge:

```text
Postgres FTS / tsvector + GIN
+ pgvector / HNSW
+ Reciprocal Rank Fusion
```

Filters for project/user/scope/security metadata SHOULD be enforced inside the query/RPC path rather than after a limited vector result set.

## 96. RLS

Exposed Supabase tables containing user/project data require appropriate RLS.

Service-role credentials are never shipped in `AlinaCoder.exe` client code.

## 97. No alpha dependency

Supabase Vector Buckets are alpha as of the current 2026 documentation and SHALL NOT become a mandatory storage layer for v0.2.

## 98. Realtime

Realtime MAY mirror low-risk UI/status events for explicitly configured trusted clients.

Realtime ACK/replay does not replace canonical effect/postcondition verification.

---

# Part XIV — New conceptual modules

## 99. Specification and repository intelligence

```text
src/alinacoder/specification/
├─ requirement_atom.py
├─ requirement_recovery_graph.py
├─ assumption_ledger.py
├─ architecture_belief_graph.py
├─ project_twin.py
├─ functional_chain.py
├─ executable_architecture_spec.py
├─ executable_behavior_spec.py
└─ drift_detector.py
```

## 100. Debugging and assurance

```text
src/alinacoder/debugging/
├─ failure_evidence.py
├─ test_semantic_purifier.py
├─ causal_context.py
├─ instrumentation.py
├─ hypothesis_ledger.py
├─ reproduction_protocol.py
├─ repair_attempt_graph.py
└─ debug_reset.py

src/alinacoder/verification/
├─ bidirectional_patch_verifier.py
├─ test_authority.py
├─ composition.py
├─ anti_reward_hacking.py
└─ verifier_integrity.py
```

## 101. Planning and tools

```text
src/alinacoder/planning/
├─ executable_task_graph.py
├─ structural_verifier.py
├─ affected_subgraph.py
├─ recovery_ladder.py
└─ global_constraint_sentinel.py

src/alinacoder/tools/
├─ schema_graph.py
├─ operability.py
├─ invocation_state.py
├─ effect_semantics.py
└─ postconditions.py
```

## 102. Security

```text
src/alinacoder/security/
├─ privilege_lattice.py
├─ context_non_escalation.py
├─ taint_labels.py
├─ observation_worker.py
├─ observation_bridge.py
├─ memory_write_gate.py
├─ authorization_ledger.py
├─ persistence_gate.py
├─ capability_mask.py
└─ egress_policy.py
```

## 103. Routing and autonomy

```text
src/alinacoder/intelligence_mesh/
├─ router_drift.py
├─ shadow_audit.py
├─ routing_signal_budget.py
└─ output_envelope.py

src/alinacoder/autonomy/
├─ envelope.py
├─ checkin_policy.py
└─ intervention_gate.py
```

## 104. Desktop diagnostics

```text
desktop_shell/
├─ run_inspector/
├─ action_receipts/
├─ live_diff_timeline/
└─ semantic_breakpoints/
```

Names are conceptual; implementation may co-locate files if responsibility boundaries and tests remain clear.

---

# Part XV — Canonical end-to-end engineering loop

## 105. New canonical coding loop

```text
User turn / voice / UI action
→ conversational grounding
→ GroundedIntentContract
→ RequirementRecoveryGraph
→ AssumptionLedger
→ SemanticStructuralProjectTwin
→ FunctionalChainGraph if cross-component
→ DualExecutableSpec when warranted
→ ExecutableTaskGraph
→ capability + security + zero-cost routing gates
→ node-scoped context
→ tool schema support path
→ action admission
→ tool invocation with durable effect semantics
→ postcondition observation
→ incremental verification
→ causal debug loop on failure
→ minimal affected subgraph repair
→ anti-reward-hacking / composition assurance
→ BidirectionalPatchVerifier when warranted
→ Done Contract
→ direct-to-main commit/push
→ remote/workspace reconciliation
→ verified experience promotion
→ memory/context fold
```

## 106. Failure loop

```text
failure
→ classify transient / operational / semantic / planning / code / security
→ reconcile real effect state
→ restore best known valid boundary if needed
→ build minimal failure evidence
→ causal localization
→ smallest recovery level
→ repair candidate
→ verify target + preserved requirements
→ independent alignment check
→ accept or reject
```

## 107. Security context loop

```text
external content
→ source + privilege + confidentiality/integrity labels
→ isolated observation handling
→ schema-constrained bridge
→ privileged context non-escalation gate
→ action plan
→ capability/egress/authorization gate
→ effect execution
→ postcondition verification
→ controlled memory write
```

## 108. Routing loop

```text
requirements/stage
→ cheap hard eligibility gates
→ demand-driven routing signals
→ capability shortfall
→ recent + long-term route evidence
→ drift check
→ task affinity
→ route
→ terminal verified outcome
→ delayed credit/regret update
→ optional safe shadow audit
```

---

# Part XVI — Acceptance and hidden evaluation expansion

## 109. Coding/specification acceptance

Implementation SHALL eventually prove fixtures where:

1. an implicit requirement is recovered from repository evidence;
2. an unsupported inferred requirement remains explicitly uncertain;
3. an assumption is linked to affected code and changing it invalidates only dependent scope;
4. semantic intended state and structural repository state diverge and drift is detected;
5. a cross-component feature passes architecture + behavior executable specs;
6. an architecture chain omission is caught despite green isolated unit tests;
7. a superseded requirement is not reintroduced from old memory.

## 110. Debugging acceptance

8. a noisy failing test is reduced to the relevant scenario;
9. instrumentation discriminates two plausible hypotheses;
10. a falsified hypothesis is not retried as if new;
11. a dynamic causal slice excludes irrelevant unexecuted code;
12. a repair regression restores/retains the superior known state;
13. debug stagnation triggers a new probe/reset rather than endless patching;
14. a reproduction test proves fail-before/pass-after;
15. backward patch reconstruction detects a patch that solves the wrong problem.

## 111. Planning acceptance

16. plan structural verifier catches a missing prerequisite;
17. schema mismatch between tool outputs/inputs blocks execution before a bad call;
18. one failed leaf replans only its affected subgraph;
19. verified sibling nodes remain frozen;
20. global constraint conflict is detected across individually successful nodes;
21. parallel nodes with overlapping write sets are serialized;
22. successful tool return without required effect does not mark subgoal done.

## 112. Anti-gaming acceptance

23. agent cannot pass by hardcoding visible test inputs;
24. weakening/skipping verifier assets is rejected;
25. isolated feature tests green + failed composition keeps task not-DONE;
26. hidden holdout remains unavailable to candidate;
27. reward-hacking gap is measured in self-improvement evaluation;
28. an agent-generated weak test cannot become the sole acceptance oracle.

## 113. Routing/speed acceptance

29. stale route quality is down-weighted after verified drift;
30. transient noise does not cause false drift demotion;
31. shadow challenger never duplicates live side effects;
32. unused expensive routing signals are skipped;
33. output-length/resource prediction influences only otherwise eligible candidates;
34. same-lineage host failover prefers healthy/fast equivalent routes without lowering quality floor;
35. cached context/evidence is invalidated by worktree/spec version change.

## 114. Security acceptance

36. web prompt injection remains low-privilege data after summarization;
37. tool output cannot become a user instruction through context assembly;
38. attacker-controlled memory cannot grant authority;
39. revoked authorization remains revoked after memory consolidation;
40. cross-project memory cannot flow without permitted scope;
41. raw untrusted tool output is isolated and only typed fields cross the bridge;
42. untrusted content cannot create a new outbound destination;
43. removing a capability runs alternate-path security regression tests;
44. model switch preserves context privilege labels;
45. secrets do not enter ineligible remote model context.

## 115. Tool operability acceptance

46. response loss after committed effect does not cause duplicate effect;
47. unknown-effect state triggers reconciliation before retry;
48. resumable invocation survives process-local interruption when adapter supports it;
49. durable execution state is distinct from in-memory process state;
50. terminal action claim is rejected when world-state postcondition disagrees.

## 116. Interface/autonomy acceptance

51. STOP/PAUSE remains responsive during slow background work;
52. user plan edit invalidates stale in-flight candidate;
53. direct-manipulation action and equivalent natural-language action produce the same structured semantic operation;
54. diagnostic timeline distinguishes proposed/committed/verified effects;
55. user can inspect intermediate diffs without confusing rejected candidates with canonical code;
56. adaptive check-in history reduces nuisance interruptions but cannot broaden hard authority;
57. app restart restores goal, last verified checkpoint, effect state and pending work coherently.

## 117. Self-evolution acceptance

58. only verified failure lessons enter durable reusable memory;
59. historical experience is rejected when architecture generation is incompatible;
60. generated history-based benchmark is rejected if oracle reconstruction is ambiguous;
61. candidate improvement that raises visible score but worsens holdout/reward-hacking gap is rejected;
62. benchmark drift triggers refresh without deleting historical results.

---

# Part XVII — New observability metrics

## 118. Software intelligence metrics

Track where meaningful:

```text
implicit_requirement_coverage
unsupported_requirement_inference_rate
assumption_reversal_rate
architecture_drift_detection_rate
functional_chain_completeness
spec_implementation_divergence
wrong_problem_patch_rate
minimal_patch_surface
```

## 119. Debugging metrics

```text
reproduction_success
fault_localization_precision
causal_context_size
hypothesis_information_gain
repair_attempts_to_success
repeated_failed_strategy_rate
rollback_recovery_rate
bidirectional_alignment_failure_rate
```

## 120. Planning metrics

```text
plan_dependency_validity
subgoal_effect_verification_rate
localized_replan_ratio
global_replan_avoidance
verified_work_reuse
parallelism_efficiency
constraint_preservation
```

## 121. Assurance/security metrics

```text
reward_hacking_gap
composition_failure_rate
verifier_tamper_attempts
context_privilege_escalation_rate
cross_scope_privilege_escalation_rate
unauthorized_memory_grant_rate
untrusted_context_leak_rate
unknown_effect_reconciliation_rate
duplicate_effect_rate
```

Hard target for autonomous paid calls remains:

```text
paid_autonomous_calls = 0
```

Hard security targets for hidden tests SHOULD aim at:

```text
unauthorized_effects = 0
false_authorization_from_memory = 0
privilege_escalation_from_untrusted_context = 0
```

## 122. Human collaboration metrics

```text
corrective_turns_per_success
user_override_cost
steering_latency
resume_context_recovery_time
unnecessary_checkin_rate
stale_action_rejection_rate
intervention_to_state_update_latency
```

---

# Part XVIII — Research source register

## 123. Primary/high-value sources used for this amendment

The research audit used current 2026 primary papers/official technical material including:

- CodeSpec — `https://arxiv.org/abs/2607.26777`
- AssumptionMiner — `https://arxiv.org/abs/2607.22898`
- SWE-RPG — `https://arxiv.org/abs/2608.09072`
- TraceCoder — `https://arxiv.org/abs/2602.06875`
- DPIAgent — `https://arxiv.org/abs/2608.23341`
- DebugRepair — `https://arxiv.org/abs/2604.19305`
- CausalRepair — `https://arxiv.org/abs/2608.10613`
- RETRACE — `https://arxiv.org/abs/2608.08950`
- SHERLOC — `https://arxiv.org/abs/2606.24820`
- Agent Planning Benchmark — `https://arxiv.org/abs/2606.04874`
- DEEPPLANNING — ACL 2026
- GNNVerifier — `https://arxiv.org/abs/2603.14730`
- Task-Decoupled Planning — `https://arxiv.org/abs/2601.07577`
- Atomic Task Graph — `https://arxiv.org/abs/2607.01942`
- COMPASS — ACL 2026
- HyperAgent — `https://arxiv.org/abs/2608.02650`
- Agent-as-a-Router — `https://arxiv.org/abs/2606.22902`
- TRACE-Router — `https://arxiv.org/abs/2607.22465`
- HyDRA — `https://arxiv.org/abs/2605.17106`
- Drift-Aware Sparse Routing — `https://arxiv.org/abs/2609.00662`
- FLARE — ACL 2026
- SCX Router — `https://arxiv.org/abs/2609.02292`
- vLLM Semantic Router — `https://arxiv.org/abs/2603.04444`
- SpecBench — `https://arxiv.org/abs/2605.21384`
- Context Privilege Escalation — `https://arxiv.org/abs/2609.01222`
- Endogenous Authorization Laundering — `https://arxiv.org/abs/2609.01836`
- SPA — `https://arxiv.org/abs/2608.27234`
- Framing Gap — `https://arxiv.org/abs/2608.27092`
- AGENTSYS — `https://arxiv.org/abs/2602.07398`
- persistent-memory defense study — `https://arxiv.org/abs/2605.08442`
- Agent-First Tooling — `https://arxiv.org/abs/2608.23628`
- Direct Manipulation + Natural Language Programming — `https://arxiv.org/abs/2608.26359`
- Dynamic Autonomy for Coding Agents — `https://arxiv.org/abs/2605.11495`
- AgentStepper — `https://arxiv.org/abs/2602.06593`
- MemCoder — `https://arxiv.org/abs/2603.13258`
- official current Supabase documentation/changelog — `https://supabase.com/changelog.md`

Third-party summaries were used only as discovery leads where a primary source was available.

---

# Part XIX — Non-negotiable synthesis

## 124. What “more intelligent” means for AlinaCoder

AlinaCoder SHALL NOT equate intelligence with:

```text
more tokens
more agents
more reflection
bigger model
more tools
more remembered text
more autonomous mutations
```

Operational intelligence means:

```text
better grounded requirement recovery
better architecture understanding
more discriminating evidence gathering
stronger causal diagnosis
smaller justified edits
better preservation of prior behavior
better global constraint consistency
better route selection for the actual stage
less context/tool noise
faster safe recovery
independent verification
resistance to proxy gaming
secure authority handling
lower corrective burden for the user
```

## 125. Final governing contract

`AlinaCoder.exe` is intended to become a continuously improving software-engineering partner whose intelligence comes from both the strongest eligible models and a rigorous external cognitive architecture.

It must:

- understand what the user actually means;
- recover implicit engineering requirements without pretending guesses are explicit commands;
- know what it assumed;
- understand both current code structure and intended architecture;
- turn important intent into executable architecture/behavior contracts;
- reason over task dependencies explicitly;
- act with the minimum required capabilities;
- treat external content as data according to provenance/privilege;
- diagnose bugs from causal evidence rather than patch churn;
- preserve the best verified state;
- repair only the affected scope;
- detect when green tests are gaming a proxy rather than implementing the system;
- independently check what a patch actually does;
- route among free models using fresh verified outcomes under drift;
- expose durable, resumable, postcondition-verifiable tool semantics;
- stay responsive and steerable inside one `AlinaCoder.exe` surface;
- learn only from verified experience;
- improve itself without weakening its evaluator, security floor or zero-cost contract;
- commit/push directly to `main` only after the complete active Done Contract is satisfied.

Final principle:

> **The perfect coding agent is not the one that acts most, talks most or uses the largest model. It is the one that most faithfully preserves human intent while converting uncertainty into evidence, evidence into minimal verified action, and verified outcomes into safer future intelligence.**
