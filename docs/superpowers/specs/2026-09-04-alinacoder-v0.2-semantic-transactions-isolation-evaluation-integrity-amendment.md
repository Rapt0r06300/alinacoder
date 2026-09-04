# AlinaCoder v0.2 — Semantic Transactions, Isolation, Evaluation Integrity & Adaptive Windows Containment Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment is additive to every previously approved v0.2 specification and amendment. It hardens AlinaCoder at the boundary between intelligent reasoning and durable autonomous execution.

It introduces normative requirements for:

- semantic transactions;
- shadow workspaces and delayed external effects;
- semantic-resource isolation across long-running tasks;
- lease/fencing-based ownership of resumable work;
- conflict-aware concurrent execution;
- evaluation integrity and anti-reward-hacking controls;
- contamination-aware capability measurement;
- adaptive Windows containment;
- stronger discovery of zero-cost coding-capable model routes;
- queue semantics that never overclaim exactly-once effects.

Where this amendment introduces a stricter rule for speculative effects, semantic resource versions, hidden evaluation, ownership, Windows isolation, free-route proof, or queue consumption, the stricter rule has precedence.

The central principle is:

> **Reason speculatively, expose effects transactionally, preserve semantic assumptions explicitly, and trust capability only when it survives adversarial evaluation.**

Canonical high-level execution shape:

```text
intent
→ semantic environment snapshot
→ speculative reasoning/work
→ shadow artifacts
→ deterministic verification
→ hidden/compositional verification where applicable
→ authorization/effect admission
→ atomic visibility decision
→ canonical effects
→ durable evidence
```

---

# Part I — Semantic Transactions

## 2. SemanticTransactionContext

Every non-trivial autonomous task SHOULD execute inside a `SemanticTransactionContext`.

For effect-bearing tasks it SHALL contain at minimum:

```text
transaction_id
project_id
task_id
intent_contract_version
canonical_state_version
base_repo_head
base_worktree_fingerprint
semantic_environment_id
policy_epoch
authorization_epoch
owner_lease_id
owner_fencing_token
shadow_workspace_id
outbox_id
created_at
state
```

Allowed states:

```text
OPEN
PREPARING
VERIFYING
READY_TO_COMMIT
COMMITTING
COMMITTED
ABORTING
ABORTED
RECONCILIATION_REQUIRED
QUARANTINED
```

## 3. Speculative work is not canonical work

LLM plans, patches, generated files, tool outputs, candidate memory updates, benchmark scores, and proposed external writes are speculative until admitted by the deterministic commit path.

A successful model response does not commit anything by itself.

## 4. ShadowWorkspace

Mutating coding work SHALL preferentially occur in a `ShadowWorkspace` or equivalent isolated staging area.

A shadow workspace SHALL provide:

```text
base_repo_head
base_file_digests
candidate_file_tree
candidate_deletions
candidate_renames
candidate_generated_artifacts
test_outputs
static_analysis_outputs
provenance
```

It SHALL NOT become canonical merely because visible tests pass.

## 5. EffectOutbox

External side effects that can be delayed SHALL be represented first as durable `EffectOutbox` entries.

Minimum fields:

```text
effect_id
transaction_id
authorization_instance_id
effect_type
canonical_action_digest
parameters_digest
destination_digest
idempotency_key
required_preconditions
semantic_environment_id
status
```

Statuses:

```text
STAGED
AUTHORIZED
PREPARED
DISPATCHED
OBSERVED
COMMITTED
CANCELLED
UNKNOWN_RECONCILE
```

## 6. Outbox-before-effect rule

For non-idempotent or high-impact remote actions, durable outbox state SHALL be written before dispatch whenever technically possible.

The effect SHALL NOT be reconstructed from model memory after a crash.

## 7. Transaction commit gate

A semantic transaction MAY commit only when all required conditions are true:

```text
IntentContract current
PlanDependencyFence valid
semantic environment compatible
owner fencing token current
authorization budget reserved
policy current
required tests passed
required hidden/compositional checks passed
no unresolved conflict
no stale in-flight response
no unresolved external effect
rollback/recovery checkpoint available when required
```

## 8. Atomic visibility

AlinaCoder SHALL distinguish:

```text
candidate success
canonical visibility
```

Candidate artifacts MUST NOT be advertised as completed work before the canonical visibility transition succeeds.

## 9. Abort semantics

Abort SHALL:

- revoke uncommitted candidate visibility;
- cancel staged outbox effects when still cancellable;
- preserve audit evidence;
- preserve already-committed effects;
- never pretend committed history disappeared;
- mark ambiguous effects for reconciliation.

## 10. Irreversible-effects exception

Some external effects cannot be delayed until the end of a task.

Such effects SHALL use the existing durable authorization prepare/commit protocol and then become explicit committed dependencies of the ongoing semantic transaction.

A later transaction abort cannot erase those effects.

## 11. ProgressFrontierCommitGate

When a result depends on multiple concurrent branches, AlinaCoder SHALL track a `ProgressFrontier`.

A joined effect SHALL not become canonical until every required predecessor has reached a compatible verified state.

Example:

```text
branch A verified
branch B still speculative
→ merged external effect forbidden
```

## 12. No implicit distributed transaction claim

AlinaCoder SHALL NOT claim ACID or atomic cross-provider transactions when external systems do not support them.

Preferred truth statement:

> **Atomic local admission plus idempotent/reconciled external effects.**

---

# Part II — Semantic Resource Isolation

## 13. Why state checkpoints are insufficient

A durable task can preserve data while silently changing the resources that give the data meaning.

Material semantic resources include:

```text
model route/model version
system prompt
project prompt
policy bundle
tool schema
tool implementation identity
MCP manifest
retrieval corpus generation
embedding model
vector index generation
reranker
protocol adapter
structured-output schema
memory retrieval policy
context compiler version
```

## 14. SemanticEnvironmentManifest

Every durable task SHALL bind to a `SemanticEnvironmentManifest`.

Minimum fields:

```text
semantic_environment_id
resource_bindings[]
compatibility_constraints[]
created_at
source_provenance
```

Each binding SHALL include:

```text
resource_type
logical_name
immutable_identity_or_digest
provider
version_or_generation
compatibility_group
freshness_policy
migration_policy
```

## 15. Semantic Snapshot Isolation

For material resources, the preferred execution mode is `SEMANTIC_SNAPSHOT_ISOLATION`.

A task SHALL either:

1. continue using the semantically compatible resource snapshot it began with; or
2. execute an explicit verified semantic migration.

Silent alias drift is forbidden.

## 16. Semantic anomalies

AlinaCoder SHALL detect at least:

```text
SEMANTIC_READ_SKEW
COMPATIBILITY_SKEW
CONTEXT_ESCAPE
MERGE_SKEW
```

### 16.1 Semantic read skew

A logical resource name resolves to a different semantic version during the same durable task.

### 16.2 Compatibility skew

Two independently updated resources are each valid but mutually incompatible.

Example:

```text
new embedding model + old vector index
```

### 16.3 Context escape

A child/subtask runs without required inherited semantic bindings.

### 16.4 Merge skew

Parallel branches produced under incompatible semantic environments are merged without migration or proof.

## 17. CompatibilityGraph

Resource compatibility SHALL be represented explicitly.

Examples:

```text
embedding_model_v3 ↔ index_generation_81
protocol_adapter_v5 ↔ tool_schema_generation_17
policy_epoch_44 ↔ approval_contract_generation_44+
```

Timestamp proximity SHALL NOT be treated as compatibility proof.

## 18. SemanticMigrationPlan

Changing a material semantic resource mid-task SHALL create a migration decision containing:

```text
source_environment
target_environment
changed_resources
compatibility_evidence
state_reinterpretation_risk
artifacts_to_revalidate
branches_to_invalidate
memory_to_recompile
required_canaries
migration_verdict
```

Possible verdicts:

```text
SAFE_EQUIVALENT
SAFE_AFTER_REVALIDATION
REQUIRES_REPLAY
REQUIRES_REPLAN
INCOMPATIBLE
QUARANTINE
```

## 19. Model failover interaction

A provider host failover within the same proven model lineage MAY preserve most semantic bindings.

A cognitive model-family switch SHALL be treated as a semantic-resource change and evaluated with the existing Continuity Spine plus this amendment's compatibility requirements.

## 20. Prompt versioning

System/project prompts used to produce effect-bearing decisions SHALL be content-addressed or immutable-versioned.

A prompt edited while a task is paused SHALL NOT silently change the interpretation of already-produced state.

## 21. Tool semantic versioning

Tool name stability is insufficient.

A tool binding SHALL include behaviorally relevant identity such as:

```text
schema digest
implementation/version digest
permission profile
provider endpoint generation
known side-effect contract
```

## 22. Retrieval semantic versioning

A retrieval result SHALL retain provenance to:

```text
corpus generation
index generation
embedding model identity
reranker identity
query transformation identity when material
```

This prevents a remembered citation/result from being treated as reproducible after the retrieval stack changes.

---

# Part III — Durable Ownership, Fencing and Concurrency

## 23. CheckpointedOwnershipLease

Resumable tasks SHALL have a current ownership lease independent of model identity.

Minimum fields:

```text
lease_id
task_id
owner_runtime_id
owner_principal_id
fencing_token
issued_at
expires_at
heartbeat_at
state
```

## 24. Monotonic fencing token

Every ownership transfer SHALL increment a monotonic fencing token.

Effect-bearing writes SHALL carry the current token.

An old worker that resumes after losing its lease SHALL be rejected even if its previous lease token still appears locally valid.

## 25. Lease expiry alone is insufficient

TTL prevents indefinite ownership but does not itself prevent a paused/zombie worker from writing after a new worker takes over.

Therefore:

```text
lease + monotonic fencing validation
```

is required for authoritative writes.

## 26. Heartbeats do not grant authority

Heartbeats prove liveness, not correctness, permission, or plan freshness.

## 27. ConflictNotificationPlane

Concurrent work SHOULD use conflict-aware invalidation instead of global cancellation.

A conflict record SHALL identify:

```text
resource/file/entity
base version
writer versions
semantic overlap
control dependency overlap
possible merge class
```

Merge classes:

```text
DISJOINT_SAFE
MECHANICALLY_MERGEABLE
SEMANTIC_REVIEW_REQUIRED
MUTUALLY_EXCLUSIVE
STALE_WRITER
```

## 28. Revision-preserving concurrency

When the user changes one part of the task, independent verified work MAY continue only if dependency analysis proves it is unaffected.

The user correction always dominates conflicting old work.

## 29. Stale writer rejection

A writer with stale:

```text
fencing token
repo HEAD dependency
IntentContract version
semantic environment
policy epoch
```

cannot commit.

---

# Part IV — Evaluation Integrity

## 30. Passing visible tests is not completion proof

Visible test success is necessary evidence but can be gamed or overfit.

For long-horizon or capability-promotion evaluations, AlinaCoder SHALL distinguish:

```text
VISIBLE_VALIDATION
HIDDEN_COMPOSITIONAL_HOLDOUT
TRUSTED_REFERENCE_EVALUATION
```

## 31. EvaluationIntegrityEnvelope

Every capability-promotion benchmark SHALL declare an `EvaluationIntegrityEnvelope` containing:

```text
evaluation_id
candidate_identity
visible_artifacts
withheld_artifacts
forbidden_paths
forbidden_network_targets
evaluator_digest
test_generation_digest
workspace_policy
file_access_policy
search_policy
feedback_policy
trusted_score_path
```

## 32. Evaluator immutability

The candidate agent SHALL NOT be able to modify the trusted evaluator used for promotion.

If a user task legitimately requires editing tests, the promotion evaluator SHALL remain external/pristine.

## 33. Hidden-data isolation

Hidden tests, answer keys, labels, gold patches, benchmark generator seeds, and trusted reference evaluators SHALL be inaccessible to the candidate task runtime.

Access attempts SHALL be logged.

## 34. Reported score is not trusted score

Where evaluation code is mutable, AlinaCoder SHALL compute a trusted score outside candidate control.

Record:

```text
reported_score
trusted_score
score_delta
tamper_evidence
leakage_evidence
integrity_verdict
```

## 35. CompositionalHoldoutVerifier

Hidden tests SHOULD combine features already required by the public specification rather than merely repeat isolated visible checks.

Example:

```text
visible:
  routing
  headers
  chunking
  error handling

hidden:
  routing + headers + UTF-8 + chunking + error path
```

## 36. RewardHackingGap

For compatible benchmark structures, track:

```text
reward_hacking_gap = visible_pass_rate - hidden_compositional_pass_rate
```

A high visible score with a large hidden gap SHALL reduce capability confidence.

## 37. Architectural integrity checks

Long-horizon promotion SHALL include properties not reducible to one scalar test count where relevant:

```text
shared state coherence
cross-feature invariants
real end-to-end flows
regression preservation
resource cleanup
error-path composition
idempotency
restart/recovery behavior
```

## 38. VerifierRedTeamLoop

Important evaluators SHOULD be adversarially hardened using separated roles:

```text
HACKER
→ attempts shortcut without solving task
FIXER
→ patches verifier against discovered exploit
LEGITIMATE_SOLVER
→ confirms valid solutions still pass
```

The loop SHALL stop on budget, convergence, or safety threshold.

## 39. DefensePool

Verifier defenses that generalize across tasks MAY enter a reviewed `DefensePool`.

Examples:

```text
subprocess isolation
immutable evaluator path
network deny rules
gold-artifact deny rules
workspace reset
trusted-score recomputation
```

A transferred defense SHALL still be tested against legitimate solvers.

## 40. BlindEvidenceSlices

Independent reviewers SHOULD receive raw evidence without prior reviewer conclusions when feasible.

This reduces anchoring and sycophantic confirmation.

## 41. Independent reviewer protocol

Preferred flow:

```text
same raw evidence
→ reviewer A independent verdict
→ reviewer B independent verdict
→ optional reviewer C independent verdict
→ deterministic aggregation / adjudication
```

not:

```text
reviewer A conclusion
→ reviewer B asked whether A is right
```

## 42. Verification diversity

Verifier diversity SHALL be measured by independent evidence paths, not merely different persona names.

Examples of genuine diversity:

```text
execution tests
static invariants
property-based tests
metamorphic tests
independent model review
manual/user-defined acceptance contract
```

---

# Part V — Contamination-Aware Capability Measurement

## 43. BenchmarkContaminationRecord

Every model/route capability observation used for promotion SHOULD record contamination status.

Minimum taxonomy:

```text
DIRECT
DERIVATIVE
TEMPORAL
DISTRIBUTIONAL
ACQUIRED_DURING_EVALUATION
UNKNOWN
```

## 44. Acquired contamination

For agents with web/repository search, contamination can be acquired during the run.

Therefore the record SHALL capture:

```text
search_enabled
queries_or_query_digests
visited_source_provenance
benchmark_artifact_hits
answer/gold-patch exposure evidence
```

## 45. Search-time contamination control

Capability benchmarks SHALL isolate or control web access where retrieval could expose benchmark answers.

For research-capability benchmarks where web use is itself required, retain complete search provenance and use private/dynamic target instances where possible.

## 46. FreshTaskCanaryStream

The capability calibration system SHOULD continuously add fresh or newly generated tasks after likely model training cutoffs/public benchmark exposure.

Fresh tasks are used as a confidence check, not as a single absolute truth.

## 47. Benchmark generation secrecy

Dynamic task generation SHOULD keep material seeds/hidden combinators unavailable to the candidate model during evaluation.

## 48. Cross-context contamination probe

When contamination is suspected, AlinaCoder MAY run independent context-isolated attempts and compare solution diversity, reasoning paths, and artifact similarity.

This signal is diagnostic, not sufficient alone to declare contamination.

## 49. Promotion score tuple

A route SHOULD be promoted using a tuple including:

```text
terminal_task_success
hidden_compositional_success
regression_success
integrity_verdict
contamination_confidence
structured_output_reliability
tool_reliability
handoff_reliability
latency/resource profile
zero-cost eligibility
```

Leaderboards remain priors only.

---

# Part VI — Adaptive Windows Containment

## 50. WindowsContainmentBackend

AlinaCoder SHALL abstract Windows isolation behind one policy-driven interface instead of hard-coding one sandbox technology.

Candidate backends include:

```text
JOB_OBJECT
LOW_INTEGRITY_PROCESS
APPCONTAINER
LPAC
CREATE_PROCESS_IN_SANDBOX_WHEN_SUPPORTED
MXC_PROCESS_ISOLATION_WHEN_SUPPORTED
MXC_SESSION_ISOLATION_WHEN_SUPPORTED
WINDOWS_SANDBOX
MICRO_VM_WHEN_SUPPORTED
```

Availability SHALL be detected at runtime.

## 51. Risk-based containment selection

Containment strength SHALL depend on action risk, required compatibility, data sensitivity, and code trust.

Example policy:

```text
known trusted read-only tooling
→ lightweight containment

model-generated build/test command
→ constrained process/AppContainer class

untrusted external code/package execution
→ stronger isolated session/sandbox

secret-bearing or highly adversarial workload
→ strongest available compatible boundary
```

## 52. Default-deny resource access

For isolated execution, access SHOULD be granted explicitly for:

```text
filesystem paths
network destinations
environment variables
registry scope
clipboard/UI
devices
process handles
```

## 53. Environment scrubbing

Sandboxed child processes SHALL NOT inherit the complete parent environment by default.

Only explicit safe variables SHALL be injected.

This protects secrets accidentally present in environment variables.

## 54. Handle inheritance restriction

Child processes SHOULD inherit only explicitly required handles.

## 55. Network policy

Model-generated code SHALL not receive arbitrary network access merely because the host has internet access.

Allowed destinations SHOULD be task-scoped where technically feasible.

## 56. UI/session isolation

Background coding tasks that do not require GUI access SHOULD be denied unnecessary desktop, clipboard, and interactive-session access.

## 57. Containment capability profile

Each machine SHALL record which isolation primitives are available and verified.

A claimed backend SHALL pass a containment smoke suite before being marked eligible.

## 58. Fail-closed degradation

If the policy requires a stronger containment level than the machine can provide, AlinaCoder SHALL:

```text
choose a safe alternative
ask for explicit user action when truly required
or refuse the unsafe execution path
```

It SHALL NOT silently downgrade containment.

## 59. Experimental API caution

Experimental Windows sandbox APIs or preview MXC functionality SHALL be capability-probed and version-gated.

Preview availability SHALL NOT become a hard runtime dependency for v0.2.

## 60. Local compatibility fallback

Existing compatible sandbox methods remain valid fallbacks so AlinaCoder continues to function on machines without newer Windows features.

---

# Part VII — Zero-Cost Route Discovery Expansion

## 61. OpenCode Zen candidate adapter

The autonomous frontier discovery system SHALL add `OpenCode Zen` as a discovery candidate, not as a trusted-free provider by default.

Current official documentation exposes multiple model routes, including explicitly free-labelled coding-capable routes at the time of this amendment.

## 62. Zen hard-zero admission

A Zen route is eligible only when all are proven at call time or within a sufficiently short proof TTL:

```text
exact route/model ID
input price = 0
output price = 0
cache-read/write price = 0 or unused
account entitlement permits zero-cost call
no required paid balance for that exact route
no automatic paid fallback
auto-reload/top-up cannot create autonomous spend
privacy/use-scope compatible
quota available
```

## 63. Temporary-free classification

Routes described as free "for a limited time" SHALL receive a short evidence TTL and status such as:

```text
PROMOTIONAL_NON_BILLABLE_HARD_CAP
```

They SHALL be automatically quarantined on stale pricing evidence.

## 64. Gateway free does not imply provider-independent diversity

When Zen/Kilo/OpenRouter route the same underlying model lineage, these routes can improve hosting resilience but SHALL NOT be counted as independent cognitive votes.

## 65. New discovery lead policy

Third-party directories may surface additional candidates such as new gateways/providers.

They remain leads until verified against first-party price, entitlement, privacy, and API documentation.

## 66. Trial/credit providers

Providers offering finite credits, one-time trials, or billing-capable grants SHALL NOT enter the standing autonomous zero-cost pool unless a deterministic hard-zero policy prevents spend after the grant ends.

## 67. OpenCode Zen billing hazard

Because Zen also supports paid models, credit balances, and billing controls, the adapter SHALL maintain an explicit paid-route denylist/price gate independent of model naming.

The suffix/name `Free` is evidence to inspect, not sufficient proof.

---

# Part VIII — Queue Semantics and Optional Supabase Coordination

## 68. Local canonical control remains mandatory

Local durable state remains canonical for AlinaCoder v0.2.

Supabase coordination is optional and SHALL NOT be required for basic offline operation.

## 69. Queue visibility semantics

When using PGMQ/Supabase Queues, AlinaCoder SHALL understand visibility timeout semantics correctly.

A consumed message can become visible again when its visibility timeout expires if it was not durably removed/archived.

## 70. Queue delivery is not external-effect exactly-once

A queue's consumer-delivery guarantee does not prove exactly-once execution of an external side effect.

The external effect path SHALL still use:

```text
AuthorizationConsumptionLedger
stable effect identity
fencing token
idempotency key where supported
EffectOutbox
reconciliation on ambiguity
```

## 71. QueueConsumerReceipt

Optional distributed consumers SHALL record:

```text
queue_name
message_id
read_count
consumer_id
fencing_token
transaction_id
effect_id
processing_started_at
processing_completed_at
archive/delete_receipt
```

## 72. Visibility renewal

Long-running message processing SHOULD renew visibility before expiry when the queue supports it, but renewal never replaces fencing/idempotency.

## 73. Duplicate delivery handling

A duplicate queue delivery SHALL resolve to an existing semantic action/effect record and SHALL NOT mint new authority.

## 74. Supabase RLS

If any optional coordination tables or exposed queue APIs are reachable through Supabase Data API, RLS SHALL be enabled and authorization SHALL be explicit.

`service_role`/secret keys SHALL never be exposed to the desktop UI or LLM context.

## 75. Supabase restore/freshness implication

Remote coordination recovery SHALL never roll back current local revocation/authority epochs.

A recovered Supabase mirror is evidence to reconcile, not permission to overwrite newer canonical local security state.

## 76. Supabase changelog compatibility

Supabase integration code SHALL monitor breaking changes relevant to used features.

As of this amendment, examples requiring awareness include changing Management API log endpoints and locked-down `realtime` schema behavior.

---

# Part IX — Observability and Evidence

## 77. SemanticTransactionTrace

Record at least:

```text
transaction_id
intent_contract_version
semantic_environment_id
base_repo_head
candidate_tree_digest
owner_fencing_token
verification_bundle_digest
hidden_eval_digest_or_reference
outbox_effect_ids
commit_verdict
abort_reason
canonical_commit_sha_if_any
```

## 78. SemanticEnvironmentTrace

Record:

```text
resource binding changes
compatibility decisions
migration decisions
resource freshness violations
merge-skew detections
```

## 79. EvaluationIntegrityTrace

Record:

```text
visible score
hidden score
reward_hacking_gap
trusted evaluator digest
forbidden-access attempts
network/search contamination events
verifier red-team findings
legitimate-solver regressions
```

## 80. ContainmentTrace

Record:

```text
requested risk class
selected backend
capabilities granted
filesystem grants
network grants
environment variables injected by key name only
exit status
containment violations
fallback decisions
```

Never log secret values.

---

# Part X — Proposed Conceptual Modules

## 81. Transaction modules

```text
src/alinacoder/transactions/
  semantic_transaction.py
  shadow_workspace.py
  effect_outbox.py
  progress_frontier.py
  transaction_commit_gate.py
```

## 82. Semantic isolation modules

```text
src/alinacoder/semantic_isolation/
  environment_manifest.py
  compatibility_graph.py
  anomaly_detector.py
  migration_planner.py
  resource_binding.py
```

## 83. Coordination modules

```text
src/alinacoder/coordination/
  ownership_lease.py
  fencing_token.py
  conflict_plane.py
  queue_consumer_receipt.py
```

## 84. Evaluation-integrity modules

```text
src/alinacoder/evaluation_integrity/
  integrity_envelope.py
  hidden_holdout.py
  compositional_verifier.py
  contamination_record.py
  verifier_redteam.py
  blind_review.py
  fresh_task_canary.py
```

## 85. Windows containment modules

```text
src/alinacoder/sandbox/
  windows_backend.py
  risk_classifier.py
  capability_probe.py
  environment_scrubber.py
  network_policy.py
  containment_receipt.py
```

## 86. Frontier discovery adapter

```text
src/alinacoder/intelligence_mesh/providers/
  opencode_zen.py
```

This module remains gated by `CostProofReceipt` and provider-data-policy checks.

---

# Part XI — Acceptance Tests

## 87. Semantic transaction tests

1. Candidate patch passing visible tests but failing a required hidden check SHALL NOT commit.
2. Aborted candidate files SHALL NOT appear in the canonical workspace.
3. An outbox effect SHALL survive process restart without being regenerated from the prompt.
4. A committed irreversible external effect SHALL remain recorded after transaction abort.
5. A transaction with unresolved effect status SHALL enter reconciliation rather than retry blindly.
6. Two concurrent branches SHALL not expose a merged effect before required predecessors verify.

## 88. Semantic isolation tests

7. Changing a prompt alias during a paused task SHALL trigger semantic-resource drift detection.
8. An old index queried with a new incompatible embedding model SHALL be rejected.
9. A child task missing a required semantic binding SHALL fail context inheritance.
10. Two branches with incompatible policy/resource generations SHALL not merge silently.
11. A verified compatible model-host failover SHALL preserve continuity without unnecessary cognitive reset.
12. A model-family switch SHALL produce a new semantic-environment/migration record.

## 89. Ownership tests

13. A stale worker with an expired lease but old process still running SHALL fail writes after a higher fencing token exists.
14. Heartbeat freshness alone SHALL NOT override stale plan or stale semantic environment.
15. User revision affecting one branch SHALL invalidate that branch while preserving mechanically proven disjoint work.

## 90. Evaluation integrity tests

16. Candidate modification of visible tests SHALL not alter the trusted hidden evaluator.
17. Candidate attempt to read hidden tests SHALL be denied and logged.
18. A solution that hardcodes visible inputs SHALL fail fresh/compositional hidden cases.
19. A verifier patch that blocks an exploit but breaks a legitimate solver SHALL not be promoted.
20. Independent reviewers SHALL not receive prior conclusions in blind mode.
21. A large visible-hidden reward-hacking gap SHALL reduce capability confidence.

## 91. Contamination tests

22. Web search retrieving a gold patch during a capability benchmark SHALL mark acquired contamination.
23. A benchmark result with unknown contamination SHALL not be treated as clean evidence.
24. Fresh post-cutoff canary tasks SHALL be tracked separately from static public benchmark results.

## 92. Windows containment tests

25. Generated process SHALL not inherit unrelated secret environment variables.
26. Headless constrained task SHALL not receive clipboard/UI access unless required.
27. A required stronger containment class unavailable on the machine SHALL fail closed or choose a proven safe alternative.
28. Containment smoke tests SHALL verify filesystem and network deny behavior before backend eligibility.
29. Experimental/preview backend failure SHALL not break basic supported sandbox fallback.

## 93. Free-route tests

30. OpenCode Zen paid route SHALL remain ineligible even if the gateway account also exposes free routes.
31. A temporary free route with expired cost proof SHALL be quarantined before inference.
32. A `Free`-named route with nonzero official price SHALL be denied.
33. Auto-reload or paid fallback capability that cannot be hard-disabled SHALL make the route ineligible for autonomous use.

## 94. Queue tests

34. A PGMQ message delivered again after visibility expiry SHALL not create a second semantic authorization.
35. Duplicate queue delivery SHALL resolve to the same stable effect identity.
36. Stale consumer fencing token SHALL block authoritative effect commit.
37. Queue archive/delete success SHALL be recorded separately from external effect success.
38. Optional Supabase unavailability SHALL not corrupt local canonical state.

---

# Part XII — Source Audit and Integration Decisions

## 95. High-confidence sources retained

The design direction in this amendment is grounded primarily in:

- recent research on semantic isolation for durable AI workflows;
- recent reward-hacking and benchmark-integrity research for long-horizon coding agents;
- Windows/Microsoft documentation and announcements for AppContainer, LPAC, sandbox APIs, MXC and containment direction;
- official OpenCode Zen model/pricing documentation;
- official Supabase Queues/PGMQ and security documentation.

## 96. Third-party free-provider directories

Third-party free-LLM directories are retained only as discovery leads.

They SHALL NOT establish zero-cost eligibility.

## 97. Rejected overclaim: every advertised free API is standing-free

Rejected.

Some services expose trial credits, evaluation grants, temporary free routes, account-specific allowances, or paid fallback.

## 98. Rejected overclaim: visible tests prove implementation correctness

Rejected.

Visible tests can be overfit, gamed, or fail to exercise feature composition.

## 99. Rejected overclaim: more reviewers always improve verification

Rejected.

Reviewers exposed to upstream conclusions can anchor or become sycophantically confirmatory.

Independent evidence views are preferred where practical.

## 100. Rejected overclaim: queue exactly-once equals effect exactly-once

Rejected.

Queue delivery semantics and end-to-end effect semantics are separate.

## 101. Rejected hard dependency on MXC

Rejected for v0.2.

MXC is promising and directly aligned with agent isolation, but preview/platform availability means the architecture SHALL use it opportunistically behind a stable containment interface.

---

# Part XIII — Canonical Combined Control Flow

## 102. Updated mutation flow

```text
User turn
→ Repair Graph
→ Intent Beam
→ IntentContract
→ SemanticEnvironmentManifest
→ PlanDependencyFence
→ CapabilityRequirementVector
→ zero-cost/privacy/tool eligibility
→ TaskAffinityLease
→ SemanticTransactionContext
→ OwnershipLease + fencing token
→ governed context/memory
→ shadow workspace
→ model/tool work
→ stale-response admission
→ visible verification
→ hidden/compositional verification when required
→ EvaluationIntegrityEnvelope verdict
→ authorization/effect preparation
→ transaction commit gate
→ canonical workspace/effect commit
→ delayed credit + experience update
→ final evidence
```

## 103. Updated failure flow

```text
failure
→ classify technical/capability/semantic/authorization/effect failure
→ transient? safe retry under same semantic action
→ host failure? same-lineage host failover
→ semantic-resource drift? migrate/replay/replan
→ stale owner? reject by fencing token
→ ambiguous effect? reconciliation
→ capability failure? compute cognitive switch utility
→ switch only from verified checkpoint
→ rehydrate canonical state
→ continue in new semantic environment only after proof
```

## 104. Updated evaluation flow

```text
candidate route/model/skill
→ clean workspace
→ visible task evidence
→ hidden compositional tests
→ trusted evaluator
→ contamination checks
→ optional verifier red-team
→ independent blind review where useful
→ terminal outcome
→ delayed route credit
→ promote / specialist / probation / reject
```

---

# Part XIV — Non-Negotiable Invariants

## 105. Transaction invariants

- speculative output is not canonical state;
- external effects require explicit admission;
- abort never erases committed history;
- ambiguous effects fail into reconciliation;
- no fake distributed-transaction guarantee.

## 106. Semantic-isolation invariants

- stable name does not prove stable meaning;
- model, prompt, tool, policy and retrieval resources are versioned semantic dependencies;
- incompatible branches do not merge silently;
- children inherit required semantic bindings;
- migration is explicit.

## 107. Evaluation invariants

- visible green tests do not alone prove completion;
- hidden evaluation cannot be mutable by the candidate;
- benchmark access/leakage is auditable;
- contamination status accompanies capability claims;
- independent reviewers should not be anchored by prior verdicts;
- genuine end-to-end behavior dominates proxy optimization.

## 108. Windows invariants

- generated code gets least privilege;
- secrets are not inherited implicitly;
- unavailable required containment does not silently downgrade;
- preview Windows features are optional backends, not assumptions.

## 109. Zero-cost invariants

- no autonomous monetary spend;
- exact route proof, not provider reputation;
- temporary free status uses short TTL;
- free label is not proof;
- gateway hosting diversity is not cognitive diversity.

## 110. Queue invariants

- duplicate delivery never creates new authority;
- visibility timeout semantics are explicit;
- queue delivery does not prove external-effect exactly-once;
- local canonical safety state survives optional cloud failure.

---

# Part XV — Final Target Behavior

The resulting design target is:

```text
Open AlinaCoder.exe
→ user speaks/writes normally
→ AlinaCoder understands and binds the real intent
→ it chooses the strongest eligible zero-cost intelligence
→ it performs risky work in governed speculative state
→ it freezes or migrates semantic assumptions explicitly
→ concurrent workers cannot become stale writers
→ generated code is contained according to risk
→ tests cannot be gamed into false completion
→ hidden/compositional evidence validates real behavior
→ external effects become visible only through durable admission
→ crashes/retries do not duplicate authority or effects
→ the canonical repo advances only with evidence
```

The goal remains:

> **Maximum verified intelligence, minimum cognitive discontinuity, exact zero autonomous monetary cost — with transactional effects and adversarially trustworthy verification.**
