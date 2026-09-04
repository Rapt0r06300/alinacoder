# AlinaCoder v0.2 — Dual Executable Contracts, Verifier Co-Evolution, Architecture Immunity & Safe Core Evolution Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment strengthens AlinaCoder against a class of failures that remains possible even with strong models, deterministic tool gates, evidence-bound completion and transactional execution: **the system can remain locally correct while gradually becoming globally inconsistent, architecturally eroded, verifier-gamed, dependency-blind, or self-modified beyond the reach of its own safety boundary.**

It is additive to the existing v0.2 baseline and every approved amendment. Where this amendment introduces stricter controls for executable specifications, specification-path invariance, verifier co-evolution, architecture quality, dependency evolution, self-modifying harnesses and long-term maintainability, the stricter rule has precedence.

The central principle is:

> **AlinaCoder SHALL maintain an executable model of what the system must be structurally and behaviorally, continuously challenge the quality of its own verification, detect degradation across repeated changes, ground dependency evolution in live upstream evidence, and keep the authority that governs self-evolution outside the mutable substrate being evolved.**

The target is not merely “code that passes tests”. The target is a repository that remains:

- faithful to the active contract;
- structurally coherent;
- behaviorally correct;
- resilient to evolving specifications;
- resistant to verifier gaming;
- maintainable after many future modifications;
- dependency-aware;
- auditable under self-improvement;
- recoverable if its own core evolution fails.

---

# Part I — Living Contract Ledger

## 2. LivingContractLedger

AlinaCoder SHALL maintain a `LivingContractLedger` derived from the compiled normative specification and the active `IntentContract`.

Every material requirement SHALL have a stable identity independent of wording and conversation position.

Minimum fields:

```text
contract_atom_id
origin
scope
polarity
status
introduced_at
last_changed_at
supersedes
superseded_by
depends_on
implemented_by
verified_by
```

## 3. Contract atom status

Allowed states SHALL include at minimum:

```text
ACTIVE
SUPERSEDED
CANCELLED
NARROWED
EXTENDED
DEFERRED
CONDITIONAL
UNRESOLVED
```

## 4. Final contract resolution

Before planning or mutating code, AlinaCoder SHALL derive work only from the active resolved contract set.

Historical repetition or salience in the conversation SHALL NOT reactivate superseded obligations.

## 5. Contract revision semantics

User changes such as:

```text
replace
cancel
narrow
extend
invert
reorder
preserve
```

SHALL update contract atoms explicitly rather than merely append new prose to the conversation.

## 6. Contract-to-code binding

A contract atom SHOULD map to relevant modules, interfaces, tests and evidence where known.

This mapping becomes part of the project state and SHALL survive model switching and context condensation.

---

# Part II — Specification Path Invariance

## 7. SpecificationPathInvariance

AlinaCoder SHALL treat **the resolved final contract**, not the path by which the user arrived at it, as the target of implementation.

If two interaction histories resolve to the same final contract, the resulting implementation SHALL be behaviorally equivalent with respect to that contract, subject to normal implementation freedom.

## 8. SpecPath metamorphic evaluation

The evaluation factory SHALL generate contract-equivalent histories such as:

```text
DIRECT
DUPLICATE
OVERRIDE
CANCELLATION
SPLIT_DISCLOSURE
REORDERED_DISCLOSURE
NOISY_CORRECTION
VOICE_SELF_CORRECTION
```

and evaluate whether the same active obligations are realized.

## 9. Path-dependence failure

If a candidate succeeds under a consolidated request but fails under a contract-equivalent history, classify:

```text
SPECIFICATION_PATH_VIOLATION
```

This SHALL be treated as an intent-resolution defect, not a model-style difference.

## 10. Path-invariance metric

Track:

```text
SpecificationPathInvariantRate
```

and condition it on tasks where direct-contract competence has already been demonstrated.

## 11. No history leakage into authority

Old cancelled constraints MAY remain in provenance/history but SHALL NOT retain operational authority simply because they occupy more context tokens than newer corrections.

---

# Part III — Functional Chain Graph

## 12. FunctionalChainGraph

For non-trivial features AlinaCoder SHALL construct an evidence-grounded functional chain describing how the requirement is realized across the repository.

A typical chain is:

```text
user/event input
→ entry point
→ validation
→ domain operation
→ state transition
→ dependency/service boundary
→ persistence or side effect
→ response/output
```

## 13. Chain node classes

Nodes MAY represent:

```text
MODULE
SYMBOL
API
DATA_OBJECT
STATE
EVENT
SIDE_EFFECT
TEST_OBSERVATION
EXTERNAL_INTERFACE
```

## 14. Chain evidence

A chain edge SHALL be grounded by actual repository evidence where the code already exists.

The agent SHALL NOT invent nonexistent functions, APIs or paths merely to make the planned chain appear complete.

## 15. Chain completeness

A feature SHALL NOT be considered architecturally realized if a required functional chain is interrupted even when isolated local handlers pass tests.

## 16. Chain delta

Every implementation pass SHALL compare intended chain versus realized chain and classify:

```text
CHAIN_COMPLETE
MISSING_UNIT
BROKEN_RELATION
BROKEN_DATA_FLOW
UNINTENDED_BYPASS
DEAD_REALIZATION
DUPLICATE_REALIZATION
```

---

# Part IV — Dual Executable Specification Engine

## 17. DualExecutableSpecEngine

Each material functional chain SHOULD compile into two complementary executable specifications:

```text
ArchitectureExecutableSpec
BehaviorExecutableSpec
```

## 18. ArchitectureExecutableSpec

The architecture specification SHALL verify applicable structural properties such as:

- required modules/symbols exist;
- required interfaces/signatures exist;
- dependency directions are respected;
- forbidden dependencies are absent;
- required functional-chain edges are connected;
- expected data flows are structurally realizable;
- legacy mechanisms required to disappear are actually absent;
- architectural ownership is respected.

## 19. BehaviorExecutableSpec

The behavioral specification SHALL verify applicable runtime semantics such as:

- preconditions;
- postconditions;
- boundary cases;
- state transitions;
- persistence semantics;
- error behavior;
- ordering;
- retry behavior;
- cancellation behavior;
- observable output;
- compatibility behavior.

## 20. Complementarity rule

Architecture checks SHALL NOT substitute for behavioral tests.

Behavioral tests SHALL NOT substitute for structural realization checks.

A feature can be behaviorally green yet architecturally wrong, or structurally complete yet behaviorally incorrect.

## 21. Persistent executable constraints

Dual executable specifications SHALL remain active throughout implementation rather than being used only as a planning artifact.

Violations SHOULD be returned as localized feedback to the repair loop.

## 22. Executable spec provenance

Every generated executable specification SHALL link back to the exact contract atom(s) from which it was derived.

If no normative or intent source supports an assertion, that assertion SHALL NOT silently become an oracle.

---

# Part V — Contract Coverage

## 23. ContractCoverage

AlinaCoder SHALL measure the fraction of material contract atoms represented by admissible executable evidence.

Coverage categories:

```text
STRUCTURE_COVERED
BEHAVIOR_COVERED
BOTH_COVERED
PARTIALLY_COVERED
UNCOVERED
NON_AUTOMATABLE_EXPLICIT
```

## 24. Boundary coverage

For component-level contracts AlinaCoder SHOULD explicitly track:

```text
preconditions
postconditions
undefined/error behavior
security boundaries
state invariants
```

## 25. EvidenceGapMiner

Introduce `EvidenceGapMiner` to search for assertions or requirements that lack independent verification.

It SHOULD prioritize gaps by:

- consequence of failure;
- centrality;
- change frequency;
- uncertainty;
- absence of independent evidence;
- historical defect density.

---

# Part VI — Verification Horizon & Co-Evolution

## 26. VerifierCoEvolutionEngine

AlinaCoder SHALL assume that no fixed verifier remains permanently adequate as the generator/harness becomes stronger.

Verification itself is an evolving subsystem.

## 27. Verifier quality dimensions

Each verifier family SHALL be evaluated on:

```text
SCALABILITY
FAITHFULNESS_TO_INTENT
ROBUSTNESS_TO_GAMING
FAILURE_INDEPENDENCE
COST
LATENCY
```

## 28. Verifier versioning

Verifier definitions, tests, rubrics and agentic evaluators SHALL have explicit versions and hashes.

Evidence produced by an old verifier SHALL retain provenance but MAY lose authority when that verifier is later shown exploitable.

## 29. Verifier failure discovery

When a stronger agent discovers a shortcut that passes a verifier without satisfying intent, that failure SHALL be recorded as:

```text
VERIFIER_EXPLOIT_CLASS
```

and become input to verifier hardening.

## 30. VerificationFlywheel

Canonical cycle:

```text
generator becomes stronger
→ new failure/exploit appears
→ capture trajectory
→ classify proxy gap
→ strengthen verifier
→ confirm legitimate solutions still pass
→ hidden/adversarial validation
→ promote verifier
→ repeat
```

## 31. No unreviewed verifier self-replacement

A verifier SHALL NOT approve the mutation that changes its own trusted acceptance logic without independent external evidence.

---

# Part VII — Hacker–Fixer–Solver Hardening

## 32. VerifierHacker

A dedicated adversarial role SHOULD attempt to satisfy an evaluation surface without solving the intended task.

Allowed in isolated evaluation only.

Targets MAY include:

- visible tests;
- build scripts;
- timing measurements;
- file-path assumptions;
- permissive mocks;
- weak assertions;
- static scans;
- benchmark harnesses.

## 33. VerifierFixer

A separate role SHALL propose defenses against confirmed exploit classes.

## 34. LegitimateSolverGuard

A third solver/verifier SHALL confirm that hardening did not make valid solutions impossible.

## 35. Three-way requirement

The loop is:

```text
HACKER finds exploit
→ FIXER closes exploit
→ SOLVER proves legitimate path remains usable
→ hidden stronger-hacker evaluation
```

A hacker/fixer loop without the solver guard is insufficient because a verifier can become over-restrictive.

## 36. SharedDefensePool

General verifier defenses discovered on one task MAY be promoted to a shared defense library when their transferability is demonstrated.

---

# Part VIII — Reward-Hacking Gap

## 37. RewardHackingGap

AlinaCoder SHALL distinguish visible optimization success from held-out compositional correctness.

Define conceptually:

```text
RewardHackingGap = VisibleValidationSuccess - HeldOutCompositionalSuccess
```

## 38. Compositional holdouts

Hidden tests SHOULD combine individually specified features instead of merely adding unrelated requirements.

Examples:

- two independently working features sharing one state representation;
- authentication + retry + persistence;
- parser feature combinations;
- ordering plus cancellation;
- migration plus backwards compatibility.

## 39. Proxy saturation warning

When visible tests saturate but hidden compositional performance does not, AlinaCoder SHALL treat the visible suite as a weak proxy, not proof of correctness.

## 40. Evaluator integrity

Critical evaluators and hidden test assets SHALL be outside ordinary mutation authority where feasible.

Changing a verifier to obtain green results is not a repair unless the verifier change is separately justified by the specification and independently validated.

---

# Part IX — Semantic Mutation Testing of Specifications

## 41. SpecificationMutationTesting

The evaluation factory SHALL mutate compiled contracts or agent policies with plausible semantic faults to prove the verifier suite detects them.

Mutation classes MAY include:

```text
ALLOW↔DENY
remove authorization check
remove rollback requirement
weaken exact-zero-cost constraint
invert boundary condition
remove preservation invariant
skip required tool
change ordering requirement
silently resurrect cancelled requirement
remove architectural boundary
```

## 42. Mutation activation

A mutation SHALL count only if an activation probe confirms that the mutated artifact can actually change behavior.

## 43. Mutation score

Track verifier sensitivity to activated semantic mutations, not merely source-code mutation count.

---

# Part X — Unknown-Unknown Exploration

## 44. UnknownUnknownExplorer

A bounded portion of verification effort SHOULD search for failures not explicitly predicted by the current plan.

## 45. Exploration strategies

May include:

- property-based testing;
- fuzzing;
- differential execution;
- adversarial input synthesis;
- state-machine exploration;
- random sequence perturbation;
- model-generated counterexamples;
- dependency failure injection;
- race amplification.

## 46. Independence

The explorer SHOULD receive less of the producing trajectory's explanation than ordinary self-review so that it can discover unanticipated failure modes.

---

# Part XI — Semantic Perturbation Robustness

## 47. SemanticPerturbationLab

AlinaCoder SHALL measure whether its coding performance is robust to semantics-preserving repository transformations.

Transformation families MAY include:

```text
identifier renaming
control-flow equivalent rewrite
dead/unreachable distractor insertion
equivalent test rewrite
file-local refactor
formatting/layout variation
API wrapper indirection without semantic change
```

## 48. Robustness objective

If a task is solvable before an invariant transformation, success SHOULD remain stable after that transformation within calibrated tolerance.

## 49. Jagged robustness

Robustness SHALL be modeled as a property of:

```text
model × harness × repository/workload
```

not of the model alone.

## 50. HarnessRobustnessMatrix

Maintain pairwise measurements across relevant model/harness/task configurations so routing can avoid a model that is nominally strong but brittle under the current harness/repository family.

---

# Part XII — Architecture Erosion Control

## 51. ArchitectureErosionBudget

AlinaCoder SHALL track long-term structural quality, not only functional correctness.

Recommended signals:

- cyclomatic complexity concentration;
- maximum function complexity;
- duplicated logic;
- redundant code;
- dependency cycles;
- fan-in/fan-out extremes;
- forbidden layer crossings;
- oversized modules;
- repeated feature-specific branches;
- parallel abstractions serving the same purpose;
- dead compatibility paths;
- unused APIs.

## 52. ArchitectureFitnessTrajectory

Quality SHALL be evaluated as a trajectory across project checkpoints.

A repository that remains green while complexity/duplication/coupling monotonically worsen SHALL be classified as structurally degrading.

## 53. No prompt-only quality control

Long-term architecture quality SHALL NOT rely solely on telling the model “write clean code”.

Quality constraints SHOULD be enforced by deterministic or semi-deterministic fitness functions where possible.

## 54. StructuralErosionState

Possible states:

```text
HEALTHY
WATCH
ERODING
CRITICAL_EROSION
RECOVERY_REQUIRED
```

## 55. Erosion debt

When a functional change consumes architecture budget, the cost SHALL become explicit technical debt rather than disappearing into history.

---

# Part XIII — Minimal Patch Pressure

## 56. MinimalPatchPressure

For repair/maintenance work, AlinaCoder SHOULD prefer the smallest change that fully satisfies the active contract and architecture requirements.

## 57. Patch surface metrics

Track when meaningful:

```text
files_touched
symbols_touched
contract_atoms_affected
new_dependencies
new_abstractions
lines_added_vs_removed
blast_radius
```

## 58. No minimality absolutism

Minimal patch pressure SHALL NOT force a local hack when the correct solution requires an architectural change.

The goal is **minimum sufficient semantic change**, not minimum line count.

## 59. Overengineering detector

Flag candidates that introduce disproportionate frameworks, abstractions or code volume without corresponding contract value.

---

# Part XIV — Whole-System Migration Audit

## 60. MigrationCompletenessContract

Migration/refactor tasks SHALL include a non-behavioral proof that the requested migration actually occurred.

## 61. WholeSystemMigrationAudit

Before completion, verify applicable conditions such as:

- forbidden old dependencies removed;
- legacy runtime path unreachable or deleted;
- wrapper/FFI shortcut does not preserve the technical debt that was supposed to disappear;
- new target technology is genuinely responsible for behavior;
- obsolete configuration/build paths removed;
- all targeted call sites migrated.

## 62. No-do-nothing success

A migration SHALL NOT receive completion merely because the original implementation still passes behavioral tests.

## 63. DifferentialBehaviorHunter

For behavior-preserving migrations, independent verifiers SHOULD actively search for inputs where:

```text
old_system(input) != new_system(input)
```

Fixed tests alone are not sufficient for high-risk migrations.

---

# Part XV — Long-Term Maintainability Done Contract

## 64. LongTermMaintainabilityDoneContract

For large features/refactors, completion SHALL include maintainability constraints in addition to functional correctness.

Possible gates:

```text
architecture fitness within budget
no unexplained duplication growth
no forbidden dependency cycle
no critical complexity concentration
no orphaned compatibility path
contract traceability intact
technical debt ledger updated
```

## 65. Functional complete vs engineering complete

A change may be:

```text
FUNCTIONALLY_COMPLETE
ENGINEERING_INCOMPLETE
```

until maintainability obligations are satisfied or explicitly accepted as debt.

---

# Part XVI — Quality Debt Ledger

## 66. QualityDebtLedger

Temporary compromises SHALL be explicit structured objects.

Minimum fields:

```text
debt_id
introduced_by
reason
scope
risk
expected_cleanup
expiry_or_review_condition
blocking_level
evidence
```

## 67. NoPermanentTemporaryFix

A workaround SHALL NOT become permanent architecture merely because it survived multiple commits.

When its expiry/review condition occurs, it SHALL be surfaced for repayment, redesign or explicit acceptance.

## 68. Debt propagation

Tasks touching indebted components SHOULD receive relevant debt context before planning.

---

# Part XVII — Architecture Immune System

## 69. ArchitectureImmuneSystem

AlinaCoder SHOULD continuously observe repository graph deltas rather than repeatedly scanning the whole repository indiscriminately.

## 70. Trigger conditions

Architecture review MAY activate on:

- new dependency edge;
- cycle creation;
- layer crossing;
- centrality spike;
- schema/API mutation;
- complexity-budget breach;
- duplicate subsystem creation;
- public interface growth;
- dependency version migration;
- security-boundary modification.

## 71. Delta-first review

The immune system SHOULD inspect the changed node and relevant upstream/downstream neighborhood first, expanding context only when evidence requires it.

## 72. Repair mode

The default output is a review finding or candidate patch evaluated through normal transaction and evidence gates; the immune system SHALL NOT bypass standard authority because it detected the problem itself.

---

# Part XVIII — Dependency Evolution Intelligence

## 73. DependencyEvolutionIntelligence

Dependency upgrades SHALL be treated as cross-repository evidence problems, not ordinary local compiler errors.

## 74. Live upstream evidence

Before significant dependency adaptation, AlinaCoder SHOULD retrieve current authoritative evidence such as:

- official release notes;
- official migration guides;
- API diffs;
- deprecation notices;
- changelogs;
- security advisories;
- official package registry metadata.

## 75. StructuredUpstreamEvidence

Raw upstream documentation SHOULD be filtered into structured evidence relevant to actual repository usages.

Fields MAY include:

```text
old_api
new_api
version_range
breaking_change_class
affected_usage_pattern
required_migration
security_notes
source_authority
source_freshness
```

## 76. UsageLocator

Map upstream changes to actual consumer call sites before patch generation.

## 77. Long-tail uncertainty

If the relevant API migration is rare or poorly evidenced, uncertainty SHALL increase rather than allowing the model to confidently hallucinate a replacement API.

## 78. LiveDependencyRiskOracle

“Latest” SHALL NOT mean “best”.

Version selection SHOULD consider:

```text
known vulnerabilities
malware/supply-chain status
breaking-change magnitude
maintenance status
license constraints
compatibility
actual project need
```

## 79. Registry reality gate

A dependency/version recommended by a model SHALL be verified against an authoritative registry before installation.

---

# Part XIX — Reusable Migration Rules

## 80. ReusableMigrationRuleLibrary

When a dependency breaking change is repaired successfully, AlinaCoder MAY generalize the repair into a reusable transformation rather than remembering only the project-specific patch.

## 81. Rule forms

Possible representations:

- AST transformation;
- codemod;
- structured symbol rewrite;
- schema migration recipe;
- configuration transformation;
- executable migration skill.

## 82. Promotion gate

A reusable rule SHALL be tested against multiple compatible usages or replay fixtures before being promoted as general.

Project-specific success alone does not prove transferability.

## 83. Version bounds

Every reusable migration rule SHALL declare exact source/target version applicability or a verified compatibility range.

---

# Part XX — Self-Evolution Supervisor Boundary

## 84. CoreEvolutionSupervisor

AlinaCoder's mutable harness SHALL be supervised by a smaller authority boundary that is **not writable through ordinary self-improvement paths**.

## 85. ImmutableGovernanceKernel

The supervisor SHALL own or independently enforce at minimum:

```text
startup/recovery authority
panic-stop
zero-spend ceiling
governance/spec verification
candidate-core boot selection
health checks
rollback to last-known-good core
protected credential boundary
promotion authorization
```

## 86. Mutable vs protected substrate

Conceptual split:

```text
PROTECTED SUPERVISOR
    ↓ controls
MUTABLE ALINACODER CORE
    ↓ operates on
EXTERNAL PROJECT WORKSPACES
```

The core being evolved cannot be the sole authority deciding that its own new version is safe.

## 87. Governance-file protection

Constitutional manifests, hard spend limits, recovery metadata and supervisor policy SHOULD be protected from ordinary core write tools.

Changes require a stronger reviewed evolution pathway.

## 88. Panic path independence

Emergency stop/rollback SHALL remain usable even if the newly promoted AlinaCoder core fails to initialize correctly.

---

# Part XXI — Failure-Batch Directed Evolution

## 89. FailureBatchEvolution

Self-improvement SHOULD begin from concrete recurring failure evidence rather than open-ended “make yourself smarter” prompts.

A batch MAY contain:

- failed missions;
- regressions;
- repeated verifier findings;
- routing failures;
- context-loss incidents;
- performance pathologies;
- user corrections;
- crash/recovery failures.

## 90. Evolution hypothesis

Each core mutation SHALL state:

```text
failure class
causal hypothesis
predicted improvement
predicted non-regression areas
rollback plan
evaluation set
```

## 91. Experience-driven evolution

Ordinary project work MAY surface harness defects, but those observations become explicit maintenance candidates before self-modification.

---

# Part XXII — Evolution Trial Workers

## 92. EvolutionTrialWorkers

A candidate AlinaCoder core SHALL be evaluated in ephemeral isolated workers before promotion.

## 93. Required trial categories

As applicable:

```text
replay original failure batch
replay last-known-good tasks
hidden holdout
security regression
recovery test
provider failover test
spec-path invariance test
architecture-quality trajectory test
```

## 94. Multiple trials for stochastic behavior

Non-deterministic agent behavior SHOULD be tested across sufficient repeated trials to distinguish true improvement from luck.

## 95. Candidate image isolation

The candidate SHALL NOT overwrite the running known-good core merely to be tested.

---

# Part XXIII — Promotion, Canary and Automatic Rollback

## 96. BestKnownCore

Maintain an explicit last-known-good/best-known core artifact and its evaluation evidence.

## 97. Core promotion

Promotion requires:

- candidate build succeeds;
- failure batch improves or is fixed;
- protected regressions do not worsen beyond policy tolerance;
- governance invariants pass;
- recovery is proven;
- candidate identity/hash is recorded.

## 98. CanaryRuntime

A promoted core SHOULD first operate under heightened monitoring and reduced autonomy where practical.

## 99. HealthProbeGatedRollback

Repeated health failures, crash loops, state corruption, governance failures or major regression during canary SHALL trigger automatic rollback by the supervisor.

## 100. Self-evolution lineage

Core versions SHALL form an auditable lineage with before/after evidence, not an opaque in-place mutation history.

---

# Part XXIV — Project Evolution Benchmark

## 101. ProjectEvolutionBenchmark

AlinaCoder SHALL be evaluated on projects that repeatedly extend **its own previous implementation output** across many checkpoints.

Clean-reset single-task benchmarks are insufficient for long-term architecture quality.

## 102. Evolution scenarios

A benchmark SHOULD include coordinated sequences such as:

```text
feature add
constraint tightening
feature interaction
API change
cancellation
refactor
breaking dependency upgrade
performance requirement
security requirement
migration
```

## 103. Trajectory metrics

Track per checkpoint:

```text
functional pass
contract faithfulness
structural integration
architecture erosion
verbosity/duplication
technical debt
regression count
recovery success
context/spec-path invariance
```

## 104. Compounding-cost requirement

The agent SHALL experience consequences of its own earlier architectural decisions rather than receiving a human-cleaned repository before every checkpoint.

---

# Part XXV — Architecture Quality as Routing Evidence

## 105. Model/harness route learning

Routing outcome learning SHOULD include long-term code-quality effects, not only immediate task completion.

A model/harness combination that solves tasks but systematically increases erosion, duplication or architectural shortcuts SHALL lose route quality for architecture-sensitive work.

## 106. Quality-delayed credit

Architecture effects discovered several checkpoints later MAY assign delayed negative credit to earlier decisions when causal evidence is sufficient.

---

# Part XXVI — Optional Supabase Durability Layer

## 107. Local-first remains canonical

All critical execution, policy and recovery state SHALL remain locally operable without Supabase.

Supabase is an optional mirror/coordination layer only.

## 108. PGMQ use

If Supabase is configured, `pgmq` MAY back durable queues for non-secret asynchronous work such as:

```text
verifier_hardening_jobs
spec_path_replays
semantic_perturbation_jobs
dependency_evidence_refresh
architecture_immune_reviews
evolution_trial_jobs
failure_batch_replays
```

## 109. Queue semantics

Consumers SHALL use visibility-timeout semantics and explicit delete/archive behavior rather than assuming exactly-once business effects.

Idempotency remains required at the AlinaCoder application layer for consequential operations.

## 110. Archive/replay

PGMQ archives MAY preserve completed evaluation jobs for replay/audit while local state remains authoritative.

## 111. Cron use

`pg_cron` MAY schedule low-priority refresh/evaluation work, but jobs SHALL be observable, bounded and nonessential to local startup.

## 112. Supabase drift awareness

Supabase-related implementation SHALL consult current documentation/changelog before changes because service behavior and extension support evolve.

Current 2026 considerations include, among others:

- Management API `logs.all` removal on 2026-09-23;
- extension version pinning being ignored in favor of platform default versions;
- Realtime schema modification lockdown;
- Vector Buckets remaining alpha and therefore not canonical storage;
- upgrade-specific extension/cron caveats.

These are volatile operational facts, not permanent constitutional truths.

---

# Part XXVII — Acceptance Scenarios

## 113. Contract history invariance

1. User reaches final requirement C directly.
2. A second run reaches the same C through cancellation and override history.
3. Both resolve to the same active contract atoms.
4. Behavioral realization remains equivalent.
5. A divergence is flagged as `SPECIFICATION_PATH_VIOLATION`.

## 114. Architecture-vs-behavior mismatch

1. Feature tests pass.
2. Required architecture chain routes around the intended service boundary.
3. ArchitectureExecutableSpec fails.
4. Completion is blocked despite green feature tests.

## 115. Behavior-vs-architecture mismatch

1. Required modules and interfaces exist.
2. Runtime state transition is wrong.
3. BehaviorExecutableSpec fails.
4. Structural completeness alone cannot complete the task.

## 116. Verifier exploit

1. Candidate special-cases visible tests.
2. Visible suite passes.
3. Hidden compositional suite fails.
4. RewardHackingGap rises.
5. exploit is recorded and verifier hardening begins.

## 117. Over-hardened verifier

1. Hacker reveals exploit.
2. Fixer blocks it but also blocks correct solutions.
3. LegitimateSolverGuard fails.
4. verifier patch is rejected/revised.

## 118. Architecture erosion

1. Ten successive features remain functionally green.
2. Complexity concentration and duplication worsen each checkpoint.
3. ArchitectureFitnessTrajectory reaches `CRITICAL_EROSION`.
4. future feature completion requires structural recovery or explicit debt acceptance.

## 119. Dependency hallucination

1. Model recommends nonexistent/new package version.
2. authoritative registry cannot verify it.
3. install is denied.
4. route confidence decreases for dependency reasoning.

## 120. Breaking dependency update

1. dependency upgrade breaks several call sites.
2. current release notes/API diff are filtered into structured evidence.
3. UsageLocator identifies affected sites.
4. patch is generated against that evidence.
5. reusable migration rule may be proposed only after sufficient transfer tests.

## 121. Migration blindness

1. requested task is to replace old stack A with B.
2. candidate keeps A behind a wrapper and passes behavior tests.
3. WholeSystemMigrationAudit detects A remains authoritative.
4. task is rejected.

## 122. Self-evolution regression

1. AlinaCoder core proposes a routing improvement.
2. isolated trial improves one visible benchmark.
3. recovery/security holdout regresses.
4. protected supervisor rejects promotion.
5. existing core remains active.

## 123. Candidate crash after promotion

1. candidate passed trials and enters canary.
2. repeated health checks fail on startup/recovery.
3. protected supervisor rolls back to BestKnownCore.
4. user state remains intact.

## 124. Stale Supabase queue job

1. optional remote queue delivers an old evolution job after local state advanced.
2. job state/version preconditions fail.
3. result may be archived as evidence but cannot mutate current core.

---

# Part XXVIII — Conceptual Modules

## 125. Proposed modules

`src/alinacoder/contracts/`

- `living_contract_ledger.py`
- `spec_path_invariance.py`
- `functional_chain.py`
- `dual_executable_spec.py`
- `contract_coverage.py`
- `evidence_gap_miner.py`

`src/alinacoder/verification/`

- `verifier_coevolution.py`
- `verifier_hacker.py`
- `verifier_fixer.py`
- `legitimate_solver_guard.py`
- `reward_hacking_gap.py`
- `spec_mutation.py`
- `unknown_unknown_explorer.py`
- `semantic_perturbation.py`

`src/alinacoder/architecture/`

- `erosion_budget.py`
- `fitness_trajectory.py`
- `minimal_patch_pressure.py`
- `architecture_immune_system.py`
- `quality_debt.py`
- `migration_audit.py`
- `differential_behavior_hunter.py`

`src/alinacoder/dependencies/`

- `evolution_intelligence.py`
- `upstream_evidence.py`
- `usage_locator.py`
- `dependency_risk_oracle.py`
- `migration_rule_library.py`

Protected/out-of-core conceptual boundary:

`supervisor/`

- `governance_kernel.py`
- `core_boot_selector.py`
- `panic_stop.py`
- `core_health.py`
- `core_rollback.py`
- `evolution_promotion.py`

`src/alinacoder/self_improvement/`

- `failure_batch.py`
- `evolution_trial_worker.py`
- `project_evolution_bench.py`
- `core_candidate_manifest.py`

---

# Part XXIX — Canonical Long-Horizon Loop Extension

## 126. Feature/change loop

```text
User turn
→ Repair Graph / IntentContract
→ LivingContractLedger update
→ active contract atoms
→ repository evidence
→ FunctionalChainGraph
→ ArchitectureExecutableSpec
→ BehaviorExecutableSpec
→ plan / mutation transaction
→ implementation
→ targeted evidence
→ contract coverage
→ architecture fitness delta
→ independent verification
→ hidden/compositional checks as required
→ EvidenceGapMiner
→ CompletionCertificate
→ architecture/debt update
→ commit main
```

## 127. Verifier co-evolution loop

```text
new exploit or proxy gap
→ capture exact state/trajectory
→ classify verifier weakness
→ adversarial hacker replay
→ fixer candidate
→ legitimate solver guard
→ hidden stronger-hacker test
→ verifier version promotion
→ invalidate/discount affected old verifier evidence as required
```

## 128. Self-evolution loop

```text
failure batches / measured harness weakness
→ causal hypothesis
→ candidate core mutation
→ protected snapshot
→ isolated EvolutionTrialWorkers
→ original failure replay
→ hidden regressions
→ governance checks
→ recovery proof
→ candidate promotion decision by protected supervisor
→ canary
→ health monitoring
→ accept OR automatic rollback
```

---

# Part XXX — New Non-Negotiable Invariants

## 129. Invariants

AlinaCoder SHALL NOT:

1. treat conversation history salience as stronger than resolved contract status;
2. call a feature complete when its required functional chain is structurally interrupted;
3. substitute architecture checks for behavioral verification or vice versa;
4. assume visible-test success proves compositional correctness;
5. permit the generator to be the sole authority over the verifier that rewards it;
6. treat verifier hardening as successful if legitimate solutions no longer pass;
7. allow long-term structural degradation to remain invisible behind green tests;
8. treat minimum line count as more important than semantic correctness;
9. call a migration complete when the old forbidden mechanism remains authoritative;
10. install or migrate to a dependency version that cannot be grounded in current authoritative evidence;
11. treat “latest dependency” as automatically safest or best;
12. promote project-specific migration logic as universally reusable without transfer evidence;
13. allow the mutable AlinaCoder core to be the sole authority approving its own replacement;
14. allow self-evolution to overwrite the last-known-good core before isolated verification;
15. make optional Supabase state necessary for local recovery or constitutional enforcement;
16. allow stale remote evaluation jobs to mutate newer canonical state;
17. ignore architecture-quality delayed effects when learning which model/harness is best.

All previous zero-spend, safety, continuity, transaction, evidence, spec-governance and main-only Git invariants remain binding.

---

# Part XXXI — Definition of the Stronger System

## 130. Target behavior

The intended system after this amendment is:

> **A coding agent that resolves the active contract independently of conversational path, converts important requirements into persistent executable architecture and behavior checks, detects when its own verifier can be gamed, searches for unknown failures, tracks architecture quality across repeated evolution, grounds dependency changes in current upstream reality, and can improve its own harness only through an externally protected trial-and-rollback supervisor.**

The desired trajectory is no longer:

```text
feature works today
```

but:

```text
feature is faithful today
+ architecture remains coherent
+ verifier remains trustworthy
+ future changes remain feasible
+ dependency reality remains grounded
+ core self-improvement remains governed
```

The long-term objective is:

> **AlinaCoder should become more capable over time without becoming less understandable, less maintainable, less verifiable, or less governed.**
