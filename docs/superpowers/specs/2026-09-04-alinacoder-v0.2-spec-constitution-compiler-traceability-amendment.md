# AlinaCoder v0.2 — Spec Constitution, Compiler, Traceability & Drift-Governance Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose

AlinaCoder v0.2 now contains a large and intentionally cumulative body of approved specifications and amendments. This amendment hardens the **governance of the specification itself** so that implementation/runtime behavior cannot depend on ambiguous precedence, stale provider snapshots, silent contradictions, incomplete implementation coverage or model interpretation of Markdown.

The architectural objective is:

> **One cumulative human-readable specification history, one machine-resolved current contract, one explicit precedence graph, one traceable rule registry, one compiled policy snapshot, and zero silent downgrade of previously approved invariants.**

This amendment is additive and jointly normative with all previously approved v0.2 specifications. It has precedence for specification governance, rule identity, precedence/conflict resolution, volatile-fact handling, compilation, traceability, spec/code drift detection and implementation coverage.

---

# Part I — Normative Manifest

## 2. Canonical manifest

AlinaCoder SHALL maintain a machine-readable:

```text
NormativeManifest
```

that enumerates every specification/amendment participating in the active contract.

## 3. Minimum fields

Each entry SHALL include:

```text
spec_id
path
status
approved_at
scope/domains
precedence_edges
supersedes
superseded_by
contains_volatile_snapshots
source_hash
```

## 4. Runtime rule

`alinacoder.exe` SHALL NOT determine active policy by globbing Markdown files and guessing chronological precedence.

The compiled manifest is the authoritative map of which documents contribute to the current contract.

---

# Part II — Unique Rule IDs

## 5. Stable rule identity

Every normative invariant, gate, prohibition, acceptance requirement and mandatory behavior introduced from implementation time onward SHALL have a stable unique identifier.

Recommended shape:

```text
ALINA.<DOMAIN>.<SUBDOMAIN>.<NUMBER>
```

Examples:

```text
ALINA.COST.ZERO.001
ALINA.GIT.MAIN_ONLY.001
ALINA.INTENT.REVALIDATE.004
ALINA.CONTINUITY.COMMIT_EPOCH.002
ALINA.SPEC.NO_SILENT_DOWNGRADE.001
```

## 6. Rule IDs are immutable identities

The wording of a rule may evolve through explicit supersession, but its identity/history SHALL remain traceable.

## 7. Duplicate semantics

If two amendments independently create materially equivalent rules, the compiler SHALL either:

```text
ALIAS_EQUIVALENT_RULE
MERGE_WITH_PROVENANCE
or
FLAG_CONFLICT
```

Never silently keep both as ambiguous independent authority.

---

# Part III — Explicit Precedence Graph

## 8. Precedence is structural, not inferred

Introduce:

```text
SpecPrecedenceGraph
```

Edges explicitly state when a rule/spec:

```text
STRENGTHENS
SUPERSEDES
NARROWS
EXTENDS
CLARIFIES
CONFLICTS_WITH
DEPRECATES
```

another rule/spec.

## 9. Date alone is insufficient

A newer document SHALL NOT automatically override an older unrelated invariant merely because its timestamp is later.

## 10. Conflict resolution order

When two active rules overlap, resolution SHALL use:

```text
explicit supersession edge
→ domain-specific precedence
→ stronger safety/correctness constraint
→ canonical constitutional invariant
→ unresolved conflict = BLOCK compilation
```

## 11. Unresolved conflict behavior

If two normative rules cannot be reconciled deterministically:

```text
SpecCompiler = FAILED_CONFLICT
```

and affected runtime behavior SHALL NOT be enabled.

---

# Part IV — Spec Conflict Detector

## 12. Mandatory detector

Introduce:

```text
SpecConflictDetector
```

It SHALL detect at minimum:

```text
same entity ACTIVE and RETIRED
same provider/model FREE and PAID under same conditions
ALLOW and FORBID for same action
same rule weakened by later text without supersession
incompatible default modes
conflicting ownership/source-of-truth claims
contradictory acceptance conditions
```

## 13. Semantic conflict classes

```text
EXACT_CONTRADICTION
SCOPE_OVERLAP_CONFLICT
TEMPORAL_SNAPSHOT_CONFLICT
PRECEDENCE_AMBIGUITY
SILENT_DOWNGRADE
DUPLICATE_RULE
UNRESOLVED_REFERENT
```

## 14. CI/release gate

`EXACT_CONTRADICTION`, `PRECEDENCE_AMBIGUITY` or `SILENT_DOWNGRADE` on active normative rules SHALL block a release.

---

# Part V — Durable Rules vs Volatile Facts

## 15. Mandatory classification

Every specification assertion SHALL be classifiable as:

```text
DURABLE_NORMATIVE_RULE
VOLATILE_RUNTIME_FACT
HISTORICAL_SNAPSHOT
RESEARCH_PRIOR
EXAMPLE_ONLY
```

## 16. Provider/model data are volatile by default

Concrete claims such as:

```text
model X is currently free
provider Y is currently active/retired
quota = N
price = P
model catalog contains Z
trial expires at date D
```

SHALL NOT be treated as durable normative truth.

## 17. Existing provider snapshots

All concrete provider/model/pricing/quota/availability claims already embedded in earlier v0.2 documents SHALL be interpreted as:

```text
HISTORICAL_SNAPSHOT / RESEARCH_PRIOR
```

unless a durable rule explicitly describes **how to verify** the fact rather than asserting the current fact itself.

This rule supersedes any prior interpretation that allowed a concrete snapshot in Markdown to authorize runtime provider admission.

## 18. Runtime authority

Current provider/model availability, price, quota, retirement status and entitlement SHALL come from the existing live evidence architecture (`LiveFreeModelOracle`, billing/funding proofs, source authority, account state and runtime probes), not from static Markdown snapshots.

---

# Part VI — Stale Fact Detector

## 19. Introduce

```text
StaleFactDetector
```

## 20. Responsibilities

It SHALL identify static facts whose freshness window has expired or whose current live evidence contradicts their stored snapshot.

## 21. Result states

```text
CURRENT
STALE_PENDING_REFRESH
STALE
SUPERSEDED
CONTRADICTED_BY_LIVE_EVIDENCE
UNPROVABLE
```

## 22. No stale authorization

A stale fact may remain useful for history/research but SHALL NOT authorize a provider, payment decision, security action, dependency assumption or deployment choice.

---

# Part VII — Canonical Provider Tombstones

## 23. Provider tombstone registry

Introduce a machine-readable:

```text
ProviderTombstoneRegistry
```

for providers/endpoints/features proven unavailable, retired, forbidden or superseded.

## 24. Tombstone semantics

A tombstone SHALL contain:

```text
entity_id
state
reason
evidence
observed_at
recheck_policy
superseded_routes
```

## 25. Re-entry

A previously tombstoned provider/model may re-enter only through the normal discovery/requalification pipeline with fresh authoritative proof.

Old specs cannot resurrect it by being re-read.

---

# Part VIII — Spec Compiler

## 26. Machine-resolved contract

Introduce:

```text
SpecCompiler
```

Its output SHALL be a deterministic machine-readable contract consumed by `alinacoder.exe`.

## 27. Compiler inputs

```text
NormativeManifest
RuleRegistry
SpecPrecedenceGraph
approved Markdown sources
constitutional invariants
volatile-fact schemas
```

## 28. Compiler outputs

At minimum:

```text
CompiledPolicyBundle
CanonicalCurrentSpec
RuleIndex
PrecedenceResolutionReport
ConflictReport
SpecificationSnapshotID
TraceabilitySkeleton
```

## 29. Markdown is provenance, compiled policy is runtime input

Human-readable specs remain authoritative provenance/design documents.

Runtime SHALL consume the compiled deterministic representation rather than asking an LLM to reinterpret all Markdown from scratch for every mission.

## 30. Determinism

Identical approved inputs SHALL produce an identical compiled policy hash.

---

# Part IX — Canonical Current Spec

## 31. Generated current view

Introduce a generated:

```text
CanonicalCurrentSpec
```

which presents the currently active rules after supersession/conflict resolution.

## 32. No provenance loss

Generation SHALL NOT delete or rewrite historical amendments.

The current view references original provenance for every active rule.

## 33. Human usability

The generated view SHALL make it possible for a developer/reviewer to understand the current active contract without manually reading every historical amendment in chronological order.

---

# Part X — SpecificationSnapshotID

## 34. Immutable policy snapshot

Every compiled contract receives:

```text
SpecificationSnapshotID = hash(compiled_policy_bundle)
```

## 35. Mission binding

Every non-trivial mission/run SHALL record the snapshot under which it began.

## 36. Mid-run policy change

If the spec changes while work is active:

```text
compare old/new policy
→ determine affected domains
→ if safety/intent/commit rules changed: safe checkpoint + revalidation
→ otherwise continue under explicit lease or upgrade at checkpoint
```

No invisible policy switch mid-mutation.

---

# Part XI — Golden Invariant Tests

## 37. Constitutional test suite

Introduce:

```text
GoldenInvariantSuite
```

## 38. Mandatory invariants

At minimum prove automatically that compiled policy cannot authorize:

```text
paid autonomous inference above €0
PAYG fallback
silent wallet/credit reload
non-main canonical Git workflow
mutation without current CommitEpoch/ownership fence
stale response mutation
IntentContract bypass
unsafe provider admission from stale Markdown
provider resurrection from tombstoned snapshot
silent weakening of newer safety rules
unverified Done claim
```

## 39. Golden tests are release-blocking

A compiled contract failing a constitutional invariant SHALL NOT ship.

---

# Part XII — Acceptance Scenario → Test Generator

## 40. Structured acceptance scenarios

Existing and future acceptance scenarios SHALL become parseable test specifications where feasible.

## 41. Introduce

```text
AcceptanceTestGenerator
```

## 42. Output classes

```text
UNIT_TEST
PROPERTY_TEST
METAMORPHIC_TEST
INTEGRATION_TEST
CHAOS_TEST
E2E_TEST
MANUAL_EVIDENCE_REQUIRED
```

## 43. No fake automation

If a requirement cannot be automatically verified, the system SHALL mark it `MANUAL_EVIDENCE_REQUIRED`, not pretend test coverage exists.

---

# Part XIII — Spec Coverage Checker

## 44. Introduce

```text
SpecCoverageChecker
```

## 45. Every normative rule gets implementation status

```text
NOT_IMPLEMENTED
PARTIALLY_IMPLEMENTED
IMPLEMENTED_UNTESTED
IMPLEMENTED_TESTED
VERIFIED_E2E
DEFERRED_WITH_REASON
```

## 46. Coverage metrics

Track:

```text
normative_rules_total
implemented_rules
rules_with_tests
rules_with_e2e_proof
orphaned_rules
orphaned_code
```

## 47. No completion inflation

A feature SHALL NOT be considered “done” merely because its module exists if required rules remain unimplemented or untested.

---

# Part XIV — Implementation Traceability Matrix

## 48. Mandatory traceability

Introduce:

```text
ImplementationTraceabilityMatrix
```

Mapping:

```text
RuleID
→ module/symbol
→ test(s)
→ runtime evidence
→ Done Contract
→ release version
```

## 49. Bidirectional navigation

Reviewers SHALL be able to answer both:

```text
Which code implements rule X?
Which normative rules justify code symbol Y?
```

## 50. Untraced critical code

Safety/payment/Git/authorization code without a normative trace SHALL trigger review.

---

# Part XV — Spec Drift Detector

## 51. Introduce

```text
SpecDriftDetector
```

## 52. Detect

```text
rule changed but implementing code/tests unchanged
code changed in governed subsystem but linked rule not reviewed
test removed while rule remains active
rule marked implemented but symbol missing
runtime behavior contradicts compiled rule
```

## 53. Drift result

```text
NO_DRIFT
EXPECTED_DRIFT_PENDING_IMPLEMENTATION
UNEXPLAINED_DRIFT
REGRESSION_RISK
BLOCK_RELEASE
```

---

# Part XVI — Source-of-Truth Hierarchy

## 54. Canonical hierarchy

For operational decisions, use:

```text
1. current repository/worktree facts and deterministic runtime evidence
2. current CompiledPolicyBundle / SpecificationSnapshotID
3. current authoritative live provider/account evidence
4. verified project memory / evidence graph
5. external research evidence
6. model opinion/inference
```

## 55. Important nuance

Runtime facts cannot override constitutional policy.

Example:

```text
provider allows payment
≠ AlinaCoder may spend money
```

Policy still forbids it.

## 56. Model confidence never outranks source truth

LLM output is advisory evidence unless independently verified.

---

# Part XVII — No Silent Downgrade

## 57. Constitutional rule

Introduce:

```text
ALINA.SPEC.NO_SILENT_DOWNGRADE.001
```

A later change SHALL NOT weaken an active safety/correctness/intent/zero-cost/continuity invariant unless:

```text
explicit supersession is declared
reason is documented
risk impact is evaluated
required tests are updated
approval provenance exists
```

## 58. Compiler behavior

Unexplained weakening = `SILENT_DOWNGRADE` = compilation/release failure.

---

# Part XVIII — Spec Release Audit

## 59. Mandatory pre-release audit

Introduce:

```text
SpecReleaseAudit
```

## 60. It SHALL check

```text
manifest completeness
RuleID uniqueness
precedence graph cycles
unresolved conflicts
stale volatile facts masquerading as normative
orphaned rules
orphaned tests
traceability gaps
golden invariant failures
provider tombstone conflicts
unexplained spec/code drift
coverage regression
```

## 61. Release evidence

Audit emits an immutable report associated with the SpecificationSnapshotID and Git commit.

---

# Part XIX — Implementation Order: Prove the Spine First

## 62. Architecture-before-breadth rule

Before attempting broad support for dozens of remote providers, AlinaCoder SHALL prove one complete vertical execution spine.

## 63. Required first vertical slice

Minimum end-to-end path:

```text
ordinary user request
→ IntentContract
→ CanonicalSessionState
→ CompiledPolicyBundle
→ one local model
→ one external zero-cost provider adapter
→ route selection
→ canonical inference envelope
→ repo read
→ controlled candidate edit
→ test execution
→ verifier
→ CommitEpoch / mutation fence
→ commit to main
→ process interruption
→ recovery
→ continued task with preserved intent/state
```

## 64. Why

Provider breadth SHALL NOT mask weakness in the orchestration spine.

One fully verified route pair is more valuable initially than thirty adapters connected to an unproven core.

## 65. Expansion gate

Additional providers/features SHOULD be added after the core slice demonstrates:

```text
state integrity
intent retention
zero-cost enforcement
mutation safety
verification
rollback
continuity
repeatable recovery
```

---

# Part XX — Constitutional Layers

## 66. Three-layer specification model

The active contract SHALL be conceptually divided into:

### Layer A — Constitution

Very stable invariants:

```text
zero paid autonomous spend
main-only canonical Git workflow
IntentContract authority
verification-before-Done
rollback/recovery
secret protection
mutation fencing
```

### Layer B — Architecture Policy

Evolving but normative mechanisms:

```text
routing
memory
continuity
resource controller
provider fabric
specialists
verification topology
```

### Layer C — Volatile Runtime Evidence

Never permanent normative truth:

```text
current provider catalog
current model availability
current prices
current quotas
current promotions
current endpoint health
current account entitlement
```

## 67. Layer precedence

```text
Constitution > Architecture Policy > Volatile Runtime Evidence > model opinion
```

with runtime facts constrained by higher layers.

---

# Part XXI — Machine-readable governance artifacts

## 68. Target artifacts

Implementation SHOULD converge toward:

```text
spec/
  normative-manifest.yaml
  rules.yaml
  precedence.yaml
  volatile-fact-schema.yaml
  provider-tombstones.yaml
  generated/
    canonical-current-spec.md
    compiled-policy.json
    rule-index.json
    traceability.json
    conflict-report.json
    spec-release-audit.json
```

Exact filenames may change without weakening semantics.

## 69. Generated artifacts rule

Generated artifacts SHALL be reproducible from authoritative sources and clearly marked generated.

## 70. Human edits

Humans/agents edit source specs/registries; generated files SHALL be regenerated rather than manually drifted.

---

# Part XXII — Acceptance Scenarios

## 71. Contradictory provider snapshot

1. Old amendment says provider/model is active/free.
2. Another approved source says it is retired/not free.
3. Both are classified volatile snapshots.
4. SpecCompiler does not choose either as runtime authorization.
5. LiveFreeModelOracle/current authoritative evidence determines present runtime state.
6. No contradiction remains in durable policy.

## 72. Safety downgrade attempt

1. New amendment accidentally says paid fallback is allowed.
2. Existing constitutional rule forbids it.
3. No explicit supersession/approval exists.
4. SpecConflictDetector reports `SILENT_DOWNGRADE`.
5. compilation/release fails.

## 73. Missing implementation

1. Rule exists requiring stale-response rejection.
2. No implementation symbol/test is traced.
3. SpecCoverageChecker marks `NOT_IMPLEMENTED`.
4. release/feature Done status cannot claim complete coverage.

## 74. Code drift

1. CommitEpoch implementation changes.
2. Linked tests/spec trace unchanged.
3. SpecDriftDetector requires review/reverification.

## 75. Historical amendments preserved

1. New rule supersedes old rule.
2. Old Markdown remains in repository.
3. CanonicalCurrentSpec shows only active rule text plus provenance link.
4. History remains auditable.

## 76. Snapshot-bound mission

1. Task begins under SpecificationSnapshotID A.
2. Spec changes to B during a patch.
3. No mid-patch silent policy replacement occurs.
4. At safe checkpoint, affected-domain diff is evaluated.
5. task either revalidates and upgrades or continues under explicit safe lease.

---

# Part XXIII — Metrics

## 77. Governance metrics

Track:

```text
active_rule_count
RuleID_duplicate_count
unresolved_conflict_count
silent_downgrade_count
stale_normative_fact_count
orphaned_rule_count
orphaned_code_count
traceability_coverage_pct
test_coverage_by_rule_pct
e2e_coverage_by_rule_pct
spec_drift_incidents
canonical_compile_success_rate
```

## 78. Hard targets

```text
RuleID_duplicate_count = 0
unresolved_conflict_count = 0
silent_downgrade_count = 0
stale volatile facts authorizing runtime = 0
constitutional golden-test failures = 0
```

---

# Part XXIV — Recommended implementation sequence

## 79. Phase S1

Implement schemas/parsers for:

```text
NormativeManifest
RuleRegistry
SpecPrecedenceGraph
rule classification
```

## 80. Phase S2

Implement:

```text
SpecConflictDetector
StaleFactDetector
ProviderTombstoneRegistry
```

## 81. Phase S3

Implement deterministic:

```text
SpecCompiler
SpecificationSnapshotID
CanonicalCurrentSpec generator
```

## 82. Phase S4

Implement:

```text
GoldenInvariantSuite
AcceptanceTestGenerator
SpecCoverageChecker
ImplementationTraceabilityMatrix
SpecDriftDetector
```

## 83. Phase S5

Prove the first complete vertical slice defined in this amendment before broad provider expansion.

---

# Part XXV — Non-negotiable governance invariants

## 84. AlinaCoder SHALL NOT

- infer normative precedence purely from filename/date order;
- use stale provider/model/pricing snapshots as runtime authorization;
- allow two contradictory active rules to compile silently;
- weaken a constitutional invariant without explicit supersession and approval;
- claim full feature implementation without traceability/coverage evidence;
- allow generated current-spec files to drift manually from source specs;
- erase historical amendments to make current policy easier to read;
- make an LLM the final arbiter of normative conflicts when deterministic resolution is possible;
- silently change the SpecificationSnapshotID governing an in-flight mutation;
- expand to dozens of providers before proving the core execution/recovery spine.

## 85. Final target behavior

```text
Human-readable cumulative spec history
        ↓
NormativeManifest + RuleRegistry
        ↓
SpecPrecedenceGraph
        ↓
SpecConflictDetector + StaleFactDetector
        ↓
SpecCompiler
        ↓
CompiledPolicyBundle + SpecificationSnapshotID
        ↓
CanonicalCurrentSpec
        ↓
ImplementationTraceabilityMatrix
        ↓
GoldenInvariantSuite + generated acceptance tests
        ↓
SpecDriftDetector
        ↓
alinacoder.exe runtime
```

The intended end state is:

> **AlinaCoder may become extremely intelligent and dynamically connected to many interchangeable LLMs, but its intelligence must operate inside one deterministic, compiled, traceable and contradiction-free constitution. The models may change continuously; the meaning of the rules must not.**
