# AlinaCoder v0.2 — Transactional Evidence, Formal Assurance, Provenance & Bayesian Control Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose

This amendment strengthens AlinaCoder beyond ordinary generate-test-revise loops by making evidence, tool effects, concurrency, provenance, uncertainty and termination first-class runtime objects.

It is additive to all previously approved v0.2 specifications and has precedence where it introduces stricter guarantees.

The central principle is:

> **AlinaCoder SHALL not trust a plausible patch, a green log, an LLM reviewer, or its own completion claim when stronger state-bound evidence can be produced. Consequential actions SHALL be transactional, evidence SHALL be bound to exact state, uncertainty SHALL drive verification effort, and privileged effects SHALL be authorized from user intent rather than from untrusted observations.**

---

# Part I — Machine-Checked Assurance

## 2. Assurance Ladder

AlinaCoder SHALL expose an `AssuranceTier` rather than treating all verification as equivalent.

Normative tiers:

1. `A0_STATIC_SANITY`
2. `A1_EXECUTABLE_TESTS`
3. `A2_INDEPENDENT_BEHAVIORAL_VERIFICATION`
4. `A3_ADVERSARIAL_AND_METAMORPHIC_VERIFICATION`
5. `A4_SYMBOLIC_OR_MODEL_CHECKING`
6. `A5_MACHINE_CHECKED_FORMAL_PROOF`

Moving to a higher tier SHALL never waive lower-tier obligations that remain applicable.

## 3. FormalVerificationEscalationPolicy

AlinaCoder SHALL evaluate whether a change merits stronger formal assurance.

Escalation signals include:

- authentication or authorization logic;
- cryptographic logic;
- money, accounting or financial invariants;
- concurrency and synchronization;
- state-machine safety;
- irreversible external effects;
- serialization/deserialization boundaries;
- protocol invariants;
- permission calculations;
- data-loss risk;
- security-critical parsing;
- cross-module invariants with weak executable oracles;
- user-declared critical modules.

The policy SHALL choose the cheapest assurance tier that meets the declared risk contract.

Formal methods SHALL be optional by domain and toolchain, not globally mandatory.

## 4. FormalArtifactContract

When formal verification is used, AlinaCoder SHALL keep implementation and proof obligations coupled.

A `FormalArtifactContract` SHALL identify:

- implementation modules;
- API signatures;
- formal specifications;
- invariants;
- proof obligations;
- trusted axioms;
- admitted/unsafe constructs forbidden by policy;
- proof toolchain version;
- source-state hash;
- proof-state hash.

A proof is invalid if its implementation or formal contract has drifted.

## 5. No-Vacuous-Proof Rule

A proof SHALL NOT count if correctness is obtained by silently weakening the target.

The formal harness SHALL check at minimum:

- target theorem still exists;
- target signature is unchanged unless explicitly amended;
- no forbidden `admit`, `sorry`, equivalent escape hatch, or unchecked axiom was introduced;
- all required obligations remain reachable;
- build/prover kernel accepts the result;
- proof artifact is bound to exact implementation state.

## 6. Formal Audit Counterexample Path

If a formal specification is inconsistent or unsatisfiable, AlinaCoder SHALL be allowed to produce machine-checked negative evidence rather than endlessly attempting a proof.

Possible outcomes:

- `IMPLEMENTATION_INVALID`
- `SPECIFICATION_INVALID`
- `SPECIFICATION_UNSAT`
- `FORMALIZATION_INCOMPLETE`
- `TOOLCHAIN_UNAVAILABLE`
- `PROVED`

No failed proof attempt SHALL be represented as proof of implementation failure without attribution.

---

# Part II — Bidirectional Patch Verification

## 7. BidirectionalPatchVerifier

Every material patch SHOULD be eligible for independent bidirectional verification.

The verifier consists of three stages:

1. `ForwardRepairReconstruction`
2. `BackwardProblemReconstruction`
3. `RepairReconciliation`

## 8. ForwardRepairReconstruction

A verifier separate from the producing trajectory SHALL reconstruct:

- the user-visible problem;
- expected behavior;
- root-cause hypothesis;
- intended repair mechanism;
- affected contracts;
- expected regression surface.

This reconstruction MAY use the original task and evidence, but SHALL NOT simply copy the producing model's final narrative.

## 9. BackwardProblemReconstruction

A verifier SHALL independently inspect the patch and relevant execution evidence while withholding the original issue text where practicable.

It SHALL answer:

> **What problem does this patch appear to solve?**

The reconstructed problem SHALL include:

- observed behavior changed;
- scope changed;
- assumptions introduced;
- behaviors removed;
- new side effects;
- security implications;
- compatibility implications.

## 10. RepairReconciliation

The backward reconstruction SHALL be compared with the canonical `IntentContract` and active `BehavioralContract`.

Mismatch categories:

- `MISSED_REQUIREMENT`
- `WRONG_PROBLEM`
- `PARTIAL_REPAIR`
- `OVERBROAD_REPAIR`
- `UNREQUESTED_BEHAVIOR_CHANGE`
- `SECURITY_REGRESSION`
- `COMPATIBILITY_REGRESSION`
- `PATCH_RATIONALE_MISMATCH`

A material mismatch blocks completion until resolved or explicitly accepted by policy.

## 11. Independent-Interpretation Requirement

At least one high-value verification path SHALL be protected from the exact interpretation that produced the patch.

Examples:

- blind backward reconstruction;
- verifier with separate context compiler;
- hidden behavioral tests;
- adversarial contract reviewer;
- formal oracle;
- differential execution against a reference.

Self-review alone SHALL NOT satisfy this rule.

---

# Part III — State-Bound Evidence

## 12. EvidenceIdentity

Every consequential evidence item SHALL be bound to exact source and execution state.

`EvidenceIdentity` SHALL contain when applicable:

- repository HEAD;
- working-tree fingerprint;
- file hashes;
- relevant artifact hashes;
- environment fingerprint;
- dependency lock hash;
- command-set hash;
- policy hash;
- verifier identity/version;
- timestamp;
- producer identity;
- task/stage ID.

## 13. StateBoundEvidenceReceipt

Tests, builds, linters, formal proofs, security scans, benchmarks and verifier decisions SHALL emit `StateBoundEvidenceReceipt` records rather than unstructured claims.

A receipt SHALL be invalid when:

- relevant source changes;
- command configuration changes;
- dependency environment changes materially;
- verifier version changes outside its compatibility declaration;
- required evidence is missing;
- producer is unauthorized;
- receipt integrity check fails.

## 14. Evidence Freshness

Evidence freshness is semantic, not merely temporal.

A one-second-old test result against an earlier tree is stale.

A day-old deterministic proof against an unchanged exact state MAY remain valid if its toolchain and assumptions remain valid.

## 15. EvidenceDependencyGraph

Evidence SHALL form a dependency graph.

Example:

`source state → build → test binary → integration test → completion certificate`

Invalidating an upstream node SHALL invalidate dependent evidence transitively.

## 16. LastKnownGoodEvidenceSet

The runtime SHALL preserve a `LastKnownGoodEvidenceSet` for every accepted checkpoint.

Rejected revisions SHALL NOT destroy or overwrite the latest verified checkpoint.

## 17. No-Stale-Diagnostic Rule

Diagnostic evidence SHALL be bound to the exact state it describes.

A later repair attempt SHALL NOT treat a failing traceback or verifier diagnosis from an older revision as authoritative without checking whether its causal preconditions still exist.

---

# Part IV — Evidence-Carrying Termination

## 18. COMPLETE Is a Privileged State Transition

An LLM MAY propose `COMPLETE` but SHALL NOT directly transition the task to complete.

Only the deterministic runtime may admit completion.

## 19. CompletionCertificate

A task may enter `COMPLETE` only with a valid `CompletionCertificate`.

The certificate SHALL bind:

- active `IntentContract`;
- active `DoneContract`;
- exact repository/workspace state;
- required claims;
- evidence supporting each claim;
- unresolved caveats;
- accepted degradations;
- security state;
- rollback checkpoint;
- verification timestamp.

## 20. Claim-to-Evidence Coverage

Every required completion claim SHALL map to one or more admissible evidence objects.

A claim with no evidence yields:

`UNSUPPORTED_COMPLETION_CLAIM`

and blocks completion.

## 21. Deterministic Replay of Verifiable Claims

Where a claim can be re-derived deterministically, the completion gate SHALL prefer replay over narrative assertion.

Examples:

- file exists;
- SHA equals expected value;
- command exits zero;
- artifact hash matches;
- migration exists;
- generated file contains required schema;
- branch HEAD equals committed SHA.

## 22. Completion Outcomes

Allowed terminal outcomes:

- `COMPLETE_VERIFIED`
- `COMPLETE_WITH_EXPLICIT_DEGRADATION`
- `BLOCKED_WITH_EVIDENCE`
- `SAFE_STOP`
- `CANCELLED_BY_USER`

There SHALL be no generic successful `DONE` state without evidence semantics.

---

# Part V — Agentic ACID Transactions

## 23. AgenticTransaction

A logical work unit that can mutate durable state SHALL execute as an `AgenticTransaction`.

It SHALL reinterpret ACID as:

- `SemanticAtomicity`
- `SemanticConsistency`
- `SemanticIsolation`
- `SemanticDurability`

## 24. SemanticAtomicity

A dependency-related set of operations SHALL either:

- become accepted together;
- remain staged;
- or be aborted/compensated according to the transaction contract.

Partial durable publication that violates the intended semantic unit is forbidden.

## 25. SemanticConsistency

A transaction SHALL be validated against:

- user intent;
- current spec snapshot;
- repository contracts;
- safety policy;
- environment invariants;
- evidence requirements;
- zero-spend policy;
- resource/permission constraints.

## 26. SemanticIsolation

Concurrent agents SHALL NOT publish combinations of changes that are incompatible with the declared isolation policy.

Isolation SHALL cover more than files:

- prompts;
- memory;
- artifacts;
- tool budgets;
- external side effects;
- task assumptions;
- dependency versions;
- route ownership.

## 27. SemanticDurability

Accepted committed state SHALL survive:

- model switch;
- application restart;
- provider failure;
- process crash;
- context condensation;
- recovery.

Durability depends on canonical runtime state, not model memory.

---

# Part VI — Transactional Tool Effects

## 28. ToolEffectClass

Every mutating tool action SHALL declare one of:

- `BUFFERABLE`
- `REVERSIBLE`
- `COMPENSATABLE`
- `IRREVERSIBLE`
- `UNKNOWN_EFFECT`

Unknown effects default to the strictest policy.

## 29. ToolEffectOutbox

Externally visible effects SHOULD be staged in a `ToolEffectOutbox` when the tool semantics permit it.

Examples include:

- outbound notifications;
- Git remote mutation;
- releases;
- deployments;
- issue changes;
- external API writes.

The outbox is released only after transaction validation.

## 30. ShadowState

Bufferable local mutations SHOULD be performed in transaction-scoped shadow state or an equivalent isolated view before publication.

Subsequent reads inside the same transaction SHALL observe the speculative state consistently.

## 31. CompensationGraph

Every reversible or compensatable external action SHALL register an inverse or mitigation procedure when feasible.

`CompensationGraph` SHALL encode dependency ordering.

Abort compensations execute in reverse dependency order.

## 32. Irreversible Effect Gate

An irreversible action SHALL be delayed until the latest safe point and SHALL require:

- current authority;
- intent support;
- provenance support;
- transaction validation;
- no stale state;
- appropriate approval class;
- evidence that prerequisite reversible work succeeded.

## 33. EffectAuditRecord

Every externalized effect SHALL record:

- intent;
- origin;
- arguments;
- authority;
- transaction ID;
- pre-state if available;
- post-state if available;
- compensation status;
- irreversibility status.

---

# Part VII — Progress Frontiers and Commit Ordering

## 34. TransactionEpoch

Every transaction SHALL have a monotonic epoch within its governed resource domain.

## 35. ResourceFrontier

Each governed resource SHALL maintain a progress frontier describing which earlier operations are known terminal.

## 36. FrontierCommitGate

A transaction may commit only when all resources it touches satisfy the configured progress predicate.

This prevents a later speculative branch from committing while an earlier conflicting branch can still publish work.

## 37. Split-Brain Protection

A route/model/agent that loses ownership of the active `CommitEpoch` SHALL be unable to publish a mutation even if its response arrives later.

Late results MAY be retained as non-authoritative evidence.

---

# Part VIII — Multi-Agent Concurrency Control

## 38. ReadSnapshot

Every agent read of mutable repository state SHALL record the version/hash of relevant resources.

## 39. OptimisticWriteAdmission

Before an agent write is admitted, the runtime SHALL verify that the assumptions represented by its read snapshot remain valid.

If stale:

- reject the write;
- return updated relevant state;
- return the minimal diff/version delta;
- identify stale dependencies;
- request localized re-plan.

## 40. LocalStateConsistency

An agent does not require the entire repository to remain frozen.

It does require the subset of state on which its proposed mutation semantically depends to remain valid until admission.

## 41. SemanticConflictDetector

Conflict detection SHALL go beyond same-file or same-line overlap.

It SHOULD detect conflicts involving:

- public signatures;
- schema changes;
- protocol messages;
- shared invariants;
- ownership assumptions;
- config contracts;
- dependency constraints;
- concurrency assumptions;
- duplicated migrations;
- incompatible test semantics.

## 42. IntentBeforeMutation

Parallel agents SHALL declare a structured mutation intent before governed writes.

The declaration SHOULD include:

- base state;
- expected files/resources;
- contracts affected;
- expected operations;
- dependencies;
- contingent scope;
- risk class.

## 43. DynamicScopeAmendment

Agents SHALL be allowed to discover legitimate additional scope without silently expanding authority.

Newly discovered mutation scope SHALL be classified as one of:

- `BOUNDED_LOCAL_EXTENSION`
- `NEW_DEPENDENCY`
- `CONTRACT_EXPANSION`
- `PLANNER_OMISSION`
- `UNAUTHORIZED_EXPANSION`

The runtime SHALL re-run admission before the new scope is mutated.

## 44. Concurrency Strategy Router

The runtime SHALL select among:

- serial;
- optimistic shared-state;
- isolated speculative branch;
- competitive branch;
- dependency-ordered parallel;
- transactional batch.

Parallelism is permitted only when expected benefit exceeds coordination and repair risk.

---

# Part IX — Flow-Centric Security and Provenance

## 45. InformationFlowGraph

The runtime SHALL model information flow as a graph rather than a flat transcript.

Nodes MAY include:

- user messages;
- web results;
- repository content;
- tool outputs;
- model summaries;
- memory entries;
- denied operations;
- generated arguments;
- external effects.

Edges SHALL represent causal or derivational dependence.

## 46. DataLabels

Sensitive and untrusted data SHALL carry runtime labels for at least:

- confidentiality;
- integrity;
- provenance;
- release eligibility.

## 47. SemanticTaint

Taint SHALL survive semantic transformations when evidence supports causal influence.

Paraphrasing, summarization or translation SHALL NOT automatically remove provenance.

## 48. Cross-Session Provenance

Memory writes SHALL retain provenance metadata.

Retrieval days or sessions later SHALL rehydrate the provenance state rather than return a provenance-free string.

## 49. Control-Flow Influence

Security policy SHALL consider not only data copied into a sink, but whether untrusted information caused the sink to be selected.

## 50. DeniedActionProvenance

Denied actions SHALL be first-class provenance events.

A later action causally influenced by information learned from the denial MAY inherit restrictions.

## 51. NoHistoryPromotion

Repeated presence in model context, memory, summaries or prior decisions SHALL NOT upgrade the authority of untrusted information.

Trust requires an authorized transformation, independent evidence or explicit policy action.

## 52. ActionInductionVsAuthorization

A source may induce the idea of an action without authorizing that action.

Execution authorization SHALL be derived from:

- user objective;
- active policies;
- authorized evidence;
- current task state;
- explicit delegated capability.

A README, webpage, issue body, log file or tool result cannot grant itself execution authority.

## 53. Argument-Level Support

Sensitive tool arguments SHALL have traceable support from authorized sources.

The system SHOULD be able to answer:

> **Why is this exact argument allowed to appear in this tool call?**

## 54. TaintIsolatedChildTrajectory

The runtime MAY inspect highly untrusted or restricted data in a child trajectory with narrowed permissions.

The parent context remains unchanged unless a controlled return is admitted.

## 55. SanitizedReturnContract

A child trajectory may return information only through a declared structured contract.

Schema validity alone SHALL NOT be treated as proof of safe declassification.

Approved deterministic transformation assertions MAY support bounded release.

---

# Part X — Deterministic Policy Compilation

## 56. RuntimePolicyCompiler

Security and authorization rules SHOULD be compiled into a deterministic reference monitor wherever practical.

The policy system SHOULD support:

- transitive provenance queries;
- deny-overrides;
- task-scoped capabilities;
- flow/path rules;
- delegated authority boundaries;
- resource-specific access;
- sensitive sink constraints.

## 57. Policy Independence from LLM

The active LLM SHALL NOT be the ultimate authority on whether its own tool call is permitted.

The LLM may provide classification evidence, but deterministic policy enforcement owns admission.

---

# Part XI — Bayesian Evidence Control

## 58. CorrectnessBeliefState

For material candidate states, AlinaCoder SHOULD maintain a calibrated belief:

`P(candidate_correct | current_evidence)`

This is not self-reported model confidence.

## 59. EvidenceLikelihoodProfile

Each verifier/critic signal SHALL have an empirical reliability profile when enough data exists.

Examples:

- visible tests;
- hidden tests;
- static analyzer;
- mutation score;
- LLM critic;
- backward reconstruction;
- formal proof;
- integration smoke;
- user validation.

## 60. BayesianEvidenceController

At decision checkpoints, the controller MAY choose among:

- gather another diagnostic;
- run a verifier;
- request an independent critic;
- refine the candidate;
- regenerate;
- escalate assurance tier;
- branch competing hypotheses;
- accept;
- defer;
- safe-stop.

Selection SHOULD maximize expected terminal utility under the project's risk and resource constraints.

## 61. ValueOfEvidence

Verification effort SHALL be adaptive.

If a cheap near-oracle exists, run it rather than adding elaborate critics.

If verification is expensive and critics are informative but imperfect, aggregation MAY reduce unnecessary verifier calls.

## 62. Abstention and Deferral

Low calibrated confidence SHALL be actionable.

The system SHALL be able to:

- abstain from a destructive mutation;
- gather missing information;
- escalate to a stronger LLM;
- escalate to deterministic analysis;
- request user clarification when ambiguity is materially unresolvable;
- retain last-known-good state.

## 63. No Universal Confidence Metric

No raw entropy, token probability, self-score or single critic SHALL be considered universally calibrated.

Calibration is task-, model-, harness- and evidence-family-specific.

---

# Part XII — Uncertainty-Adaptive Compute

## 64. SemanticUncertaintySensor

The runtime SHOULD estimate uncertainty at meaningful task boundaries, including:

- ambiguous intent;
- unclear root cause;
- competing patch strategies;
- unstable tool evidence;
- OOD task detection;
- verifier disagreement;
- environment uncertainty.

## 65. ComputeRegimes

At minimum:

- `DIRECT`
- `BRANCH`
- `REFINE_UNCERTAINTY`
- `ESCALATE_SPECIALIST`
- `ADVERSARIAL_VERIFY`

## 66. InfluenceBasedRollback

When a downstream failure occurs, AlinaCoder SHOULD localize the upstream decision most likely to have caused it rather than restarting the entire trajectory.

Successful independent work SHALL be preserved when its premises remain valid.

## 67. Online Calibration

The uncertainty controller MAY self-calibrate from verifier outcomes, but parameter changes SHALL be subject to the self-improvement governance already defined in previous amendments.

---

# Part XIII — Test Impact Intelligence

## 68. TestImpactGraph

AlinaCoder SHALL maintain or derive relationships from production code to tests.

Edges MAY come from:

- direct naming conventions;
- imports;
- call graph;
- coverage;
- dynamic traces;
- symbol references;
- historical co-change;
- explicit ownership metadata.

## 69. PreChangeTestImpactAnalysis

Before committing a patch, AlinaCoder SHOULD identify tests likely affected by the planned change.

The output SHALL distinguish evidence confidence.

## 70. TestExecutionStrategy

Targeted tests MAY be used for fast feedback, but final completion requirements SHALL determine when broader suites are required.

Targeted testing is an optimization, not permission to ignore global regression risk.

## 71. TestEvolutionEngine

Changes SHALL be evaluated for three distinct test-evolution needs:

- `TEST_BREAKING`
- `TEST_STALE`
- `TEST_MISSING`

A passing test MAY still require modification if it no longer validates the intended behavior.

## 72. TestIntentReasoner

AlinaCoder SHOULD reason about what tests are meant to prove, not just whether they execute.

## 73. Generated-Test Independence

Tests written by the same trajectory as the implementation SHALL receive lower independence weight than pre-existing, hidden, adversarial or independently generated tests unless additional evidence demonstrates equivalent reliability.

---

# Part XIV — Repository Data-Flow Intelligence

## 74. RepositoryViewCompiler

AlinaCoder SHOULD support reusable repository views tied to exact commits/workspace generations.

Recommended views:

- lexical index;
- symbol index;
- AST index;
- import graph;
- call graph;
- inheritance graph;
- code-test graph;
- data-flow graph;
- semantic/vector index;
- historical change graph.

## 75. ViewFreshness

Every derived view SHALL declare the source state it represents.

A stale index SHALL never silently masquerade as current repository truth.

## 76. IncrementalViewMaintenance

Views SHOULD update only affected regions where equivalence with a rebuild can be established or confidence is sufficient under the view contract.

## 77. OnDemandDataFlowSlicer

AlinaCoder SHOULD expose a query primitive capable of tracing definitions and uses relevant to a variable or expression.

Directions:

- backward;
- forward;
- both.

## 78. SliceGrounding

LLM-proposed dependency edges SHALL be grounded against actual repository symbols before admission.

Non-existent functions and external-library symbols SHALL NOT be silently inserted into the internal repository graph.

## 79. RetrievalPrecisionOverVolume

The context system SHALL prefer small, source-grounded evidence packets over indiscriminate whole-file/whole-repository dumping when quality is not reduced.

Long context capacity is not permission to inject irrelevant evidence.

---

# Part XV — Verifier Dependence and Security-Aware Correctness

## 80. VerifierDependenceGraph

Verifier diversity SHALL be measured by failure independence, not names or model families alone.

Two checks depending on the same observable or assumption do not constitute fully independent evidence.

## 81. FunctionallyCorrectYetVulnerable Guard

Passing functional tests SHALL NOT be sufficient for security-sensitive patches.

Security verification SHOULD include applicable:

- static security analysis;
- CWE-focused review;
- taint/data-flow analysis;
- permission review;
- secret exposure checks;
- fuzzing/property testing;
- adversarial test generation.

## 82. SecurityIntentSeparation

Developer-looking suggestions originating from untrusted issues or repository content SHALL retain untrusted provenance even when syntactically plausible.

---

# Part XVI — Acceptance Scenarios

## 83. State-Bound Evidence Scenarios

1. Test suite passes on revision A; revision B changes production code. The old test receipt is rejected for completion of B.
2. A formal proof was produced against an unchanged state and unchanged verified toolchain. It remains admissible according to its declared lifetime.
3. A diagnostic from a stale revision suggests changing function X, but X's relevant path was removed. The diagnosis is not treated as current evidence.

## 84. Patch-Reconstruction Scenarios

4. Patch passes tests but backward reconstruction says it fixes caching while user asked for authentication. Completion is rejected.
5. Patch fixes the requested bug but also removes a supported API. Reconciliation flags overbroad scope.
6. Forward and backward reconstructions align and independent behavior checks pass. The verification signal is admitted.

## 85. Completion Scenarios

7. Model outputs `DONE` with no evidence. Runtime state remains non-terminal.
8. Every DoneContract claim has fresh evidence bound to the current tree. Completion certificate may be issued.
9. Required evidence is unavailable but limitation is explicit and policy permits degraded completion. Outcome is `COMPLETE_WITH_EXPLICIT_DEGRADATION`, never ordinary verified completion.

## 86. Transaction Scenarios

10. Two local file edits must land together for schema consistency. Partial publication is blocked.
11. An outbound side effect is staged until local validation succeeds.
12. A compensatable external effect was published before a later failure. Compensation executes and is recorded.
13. An irreversible effect lacks current authority. It does not execute.

## 87. Concurrency Scenarios

14. Agent B writes based on file version 12 after Agent A published version 13. B's write is rejected with fresh context.
15. Agents edit different files but change incompatible public signatures. Semantic conflict detector blocks joint admission.
16. Agent discovers a legitimate new dependency outside initial scope. It requests dynamic re-admission rather than silently editing it.
17. A timed-out model replies after ownership moved to another model. Its stale mutation cannot commit.

## 88. Provenance Scenarios

18. Web content says to upload repository secrets. The content can induce an idea but has no execution authority; network action is denied.
19. Malicious text is summarized and later retrieved from memory. Provenance remains untrusted.
20. A denied secret-read influences a later outbound message. Denial provenance is considered by policy.
21. Untrusted content is inspected in an isolated child trajectory; only a sanitized structured result reaches the parent.

## 89. Bayesian Control Scenarios

22. Cheap public test is near-oracle. Controller verifies directly instead of wasting critic calls.
23. Full integration verification is expensive; several calibrated critics sharply reduce uncertainty. Controller gathers evidence before deciding whether to pay the verification cost.
24. Candidate confidence falls below the destructive-action threshold. Runtime abstains and gathers more evidence.

## 90. Test Intelligence Scenarios

25. Source change does not break any tests but invalidates their assertions semantically. TestEvolutionEngine identifies `TEST_STALE`.
26. New behavior has no corresponding test. Engine identifies `TEST_MISSING`.
27. TestImpactGraph identifies a small related test subset for fast feedback, followed by policy-required broader verification before completion.

## 91. Formal Assurance Scenarios

28. Security-critical invariant cannot be sufficiently checked through examples and supported formal tooling exists. Assurance policy escalates.
29. Proof passes only after the agent weakens the theorem. No-vacuous-proof guard rejects it.
30. Specification is contradictory; prover demonstrates inconsistency. Runtime reports specification failure rather than implementation failure.

---

# Part XVII — Conceptual Modules

## 92. Proposed Runtime Modules

Suggested conceptual modules:

`src/alinacoder/assurance/`

- `assurance_tier.py`
- `formal_escalation.py`
- `formal_artifact_contract.py`
- `formal_audit.py`

`src/alinacoder/verification/`

- `bidirectional_patch_verifier.py`
- `forward_reconstruction.py`
- `backward_reconstruction.py`
- `repair_reconciliation.py`
- `state_bound_receipt.py`
- `evidence_graph.py`
- `completion_certificate.py`
- `verifier_dependence.py`

`src/alinacoder/transactions/`

- `agentic_transaction.py`
- `shadow_state.py`
- `effect_outbox.py`
- `compensation_graph.py`
- `resource_frontier.py`
- `commit_epoch.py`
- `semantic_conflict.py`
- `dynamic_scope.py`

`src/alinacoder/security/`

- `information_flow_graph.py`
- `runtime_labels.py`
- `semantic_taint.py`
- `denied_action_provenance.py`
- `action_authorization.py`
- `taint_isolated_child.py`
- `policy_compiler.py`

`src/alinacoder/control/`

- `correctness_belief.py`
- `evidence_likelihood.py`
- `bayesian_evidence_controller.py`
- `uncertainty_sensor.py`
- `compute_regime.py`
- `influence_rollback.py`

`src/alinacoder/repository_intelligence/`

- `test_impact_graph.py`
- `test_evolution.py`
- `repository_view_compiler.py`
- `view_freshness.py`
- `dataflow_slicer.py`

---

# Part XVIII — Canonical Control Loop Extension

## 93. Verification-Aware Execution Loop

Canonical extension:

```text
IntentContract
→ active Spec Snapshot
→ BehavioralContract
→ risk / AssuranceTier
→ task and dependency graph
→ acquire authorized evidence
→ plan transaction
→ declare mutation intent
→ concurrency admission
→ execute in shadow/staged state where possible
→ targeted tests / diagnostics
→ patch candidate
→ state-bound evidence receipts
→ bidirectional patch verification
→ security / provenance verification
→ BayesianEvidenceController
    gather more evidence
    refine
    branch
    escalate assurance
    or proceed
→ transaction validation
→ effect outbox release / commit
→ broad regression verification as required
→ completion claim mapping
→ CompletionCertificate
→ COMPLETE_VERIFIED
```

## 94. Failure Loop

```text
failure or verifier disagreement
→ bind failure to exact state
→ classify root cause
→ identify earliest influential uncertain decision
→ preserve LastKnownGood checkpoint
→ rollback only affected transaction/subgraph
→ invalidate dependent evidence
→ refresh repository views
→ update correctness belief
→ choose repair / branch / escalate / defer
```

## 95. Concurrency Loop

```text
agent reads resources + versions
→ declares intent
→ receives authority scope
→ works concurrently
→ attempts write
→ validate read snapshot + semantic dependencies
→ current? admit atomically
→ stale? reject with delta
→ local re-plan
→ retry
```

## 96. Security Loop

```text
source enters system
→ attach provenance/confidentiality/integrity labels
→ propagate through tools/memory/derived artifacts
→ LLM proposes action
→ separate action induction from authorization
→ trace argument support
→ evaluate transitive and denial provenance
→ reference monitor
→ stage if consequential
→ transaction-level validation
→ release or deny
```

---

# Part XIX — Non-Negotiable Invariants

## 97. Invariants

The following remain mandatory:

1. `MAX_PAID_SPEND_EUR = 0.00` remains binding.
2. No LLM self-report may directly create a verified lifecycle state.
3. No evidence may outlive the state it actually proves unless its contract explicitly remains valid.
4. No stale agent/model owns mutation authority after a newer CommitEpoch is active.
5. No untrusted source can grant itself tool authority.
6. No repeated summarization or memory persistence automatically upgrades trust.
7. No functional green status alone proves security correctness.
8. No formal proof is accepted if the target was weakened or proof obligations were silently removed.
9. No concurrent write is admitted against known-invalid assumptions.
10. No test-impact optimization may weaken the final DoneContract.
11. No verifier plurality is counted as independence without considering shared failure modes.
12. No irreversible effect is released earlier than required.
13. The canonical state remains owned by AlinaCoder, never by the active LLM.
14. All prior safety, spec-governance, provider-fabric, continuity and zero-spend requirements remain in force.

---

# Part XX — Definition of Stronger AlinaCoder

## 98. Target Behavior

After this amendment, the intended AlinaCoder architecture is not merely:

> generate code → run tests → retry.

It is:

> understand intent → formalize behavioral obligations → estimate risk and uncertainty → plan a governed transaction → preserve provenance → execute with least authority → bind evidence to exact state → independently reconstruct what the patch actually does → test affected and global behavior appropriately → escalate to formal assurance when justified → publish effects only after transaction validation → issue completion only with an evidence certificate → learn from calibrated outcomes without corrupting the last-known-good state.

The design goal is:

> **high autonomy without epistemic, transactional or security looseness.**

A stronger model may improve proposals. The AlinaCoder control plane SHALL determine what becomes truth, what becomes durable state, and what may be called complete.
