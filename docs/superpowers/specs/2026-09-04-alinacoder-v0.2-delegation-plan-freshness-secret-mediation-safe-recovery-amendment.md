# AlinaCoder v0.2 — Delegation Authority, Plan Freshness, Secret Mediation & Safe Recovery Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment is additive to the v0.2 baseline and every previously approved amendment. It strengthens AlinaCoder at the boundaries where long-running autonomous execution is most likely to become unsafe despite otherwise-correct model reasoning: durable authorization consumption, multi-agent delegation, history-dependent privilege composition, stale plans, checkpoint/restore, secret use, MCP trust drift, Windows process isolation, context/cache reuse, and optional Supabase coordination.

Where this amendment introduces stricter requirements for authorization consumption, delegation attenuation, plan dependency validation, safe execution edits, secret mediation, continuous tool trust, Windows execution containment, context freshness, or optional Supabase credential handling, the stricter rule has precedence.

The central principle is:

> **Authority is state, not text. Fresh data does not imply a fresh plan. A credential is never a capability merely because the model can use it. Recovery is a forward transition, never an erasure of history.**

The target control chain is:

```text
user intent
→ canonical task authority
→ plan with explicit dependencies
→ delegated attenuated authority
→ composition-aware admission
→ exact action identity
→ durable authorization budget
→ workload/tool trust proof
→ secret-mediated execution
→ external effect
→ causal receipt
→ forward-only recovery / revision
→ verified completion
```

No LLM output, prompt, summary, cache hit, tool manifest, OAuth grant, checkpoint, or recovered context may substitute for the deterministic control-plane evidence required by this amendment.

---

# Part I — Durable Authorization Consumption

## 2. AuthorizationInstance

AlinaCoder SHALL distinguish an authorization decision from any token, approval artifact, retry request, or tool-call identifier that represents it.

A canonical `AuthorizationInstance` SHALL identify the underlying user-authorized action independently of how many execution artifacts are minted for it.

Minimum fields:

```text
authorization_instance_id
principal_id
project_id
task_id
intent_contract_version
canonical_action_digest
resource_set_digest
parameter_constraints_digest
policy_epoch
revocation_epoch
confirmation_evidence_digest
execution_budget_total
execution_budget_reserved
execution_budget_committed
created_at
expires_at
state
```

Possible states:

```text
PROPOSED
AUTHORIZED
PREPARED
COMMITTED
REVOKED
EXPIRED
QUARANTINED
RECONCILIATION_REQUIRED
```

## 3. Semantic replay defense

A new token identifier SHALL NOT create new authority.

Equivalent re-proposals, retries, model replans, sub-agent retries, process restarts, provider failovers, restored checkpoints, and newly generated idempotency identifiers SHALL resolve to the same `AuthorizationInstance` when they represent the same authorized semantic action.

The following anti-pattern is forbidden:

```text
single-use token consumed
→ model retries same authorized action
→ runtime issues fresh single-use token
→ action executes again
```

A token-local replay cache is insufficient because semantic replay can use a new token.

## 4. AuthorizationConsumptionLedger

Every effect-bearing `AuthorizationInstance` SHALL have durable consumption state outside the model runtime.

The ledger SHALL record at minimum:

```text
authorization_instance_id
canonical_action_digest
budget_total
budget_reserved
budget_committed
active_preparations[]
committed_effect_ids[]
revocation_epoch
last_transition_at
```

The ledger is authoritative for how many executions remain admissible.

## 5. Issue–Prepare–Commit protocol

For non-idempotent or high-impact effects, admission SHALL use a durable transition sequence equivalent to:

```text
AUTHORIZED
→ PREPARED
→ EFFECT_ATTEMPT
→ EFFECT_OBSERVED
→ COMMITTED
```

`PREPARED` atomically reserves execution budget before the effect begins.

A second concurrent consumer SHALL fail if no budget remains.

## 6. Atomic preparation

The following condition SHALL be enforced by transactional state, a compare-and-swap primitive, a linearizable local broker, or an equivalently strong mechanism:

```text
sum(active reservations + committed uses) <= execution_budget_total
```

Two concurrent agents SHALL NOT independently observe remaining budget and both proceed.

## 7. Delegation consumes or reserves authority

Delegating an executable authorization to a child context SHALL reserve or transfer part of the parent budget.

Parent and child SHALL NOT both retain independently exercisable copies of the same single-use authority.

Canonical rule:

```text
child_budget <= reserved_parent_budget
```

and the reserved portion is unavailable to the parent until the child is cancelled, expires, or returns unused budget through a deterministic reconciliation path.

## 8. Recovery of prepared actions

A crash after `PREPARED` SHALL NOT automatically mint a new authorization.

Recovery SHALL inspect the existing preparation and classify it:

```text
SAFE_TO_EXECUTE_EXISTING_PREPARATION
EFFECT_ALREADY_COMMITTED
EFFECT_STATUS_UNKNOWN_RECONCILE
PREPARATION_REVOKED
PREPARATION_EXPIRED
```

## 9. Stable sink identity

Where an external backend supports idempotency keys, the key SHALL be derived from stable semantic effect identity rather than generated afresh after restart.

Preferred binding:

```text
idempotency_key = H(project_id, authorization_instance_id, effect_id, canonical_action_digest)
```

## 10. No literal exactly-once claim without proof

AlinaCoder SHALL NOT claim exactly-once external execution unless the complete path provides that property.

The preferred guarantee remains:

> **Durable single admission + stable effect identity + idempotent or reconciled sink + fail-closed ambiguity.**

---

# Part II — Delegation Authority Chain

## 11. AgenticPrincipalChain

Every delegated autonomous context SHALL have an explicit principal chain rooted in the user/project authority.

Example:

```text
USER
→ ORCHESTRATOR
→ SPECIALIST_AGENT
→ TOOL_ADAPTER
→ EXECUTION_BROKER
```

Each edge SHALL record:

```text
parent_principal
child_principal
parent_authority_digest
child_authority_digest
subtask_digest
resource_scope
operation_scope
parameter_bounds
budget_bounds
issued_at
expires_at
parent_edge_id
```

## 12. Authority attenuation

Delegated authority SHALL narrow monotonically.

For every edge:

```text
child.operations ⊆ parent.operations
child.resources ⊆ parent.resources
child.parameter_domain ⊆ parent.parameter_domain
child.execution_budget <= parent.available_budget
child.expiry <= parent.expiry
```

A child cannot widen itself through prompt text, tool metadata, remembered policy, provider-native state, or model-generated justification.

## 13. Model-independent enforcement

The delegation chain SHALL be enforced outside the LLM.

A fully prompt-injected model SHALL still be unable to exceed the effective authority encoded in the deterministic delegation state.

## 14. Sender-constrained capability

Where practical, remote or cross-process execution capabilities SHOULD bind to the receiving workload identity or secure local channel, not merely to a transferable bearer string.

A stolen execution artifact SHOULD be unusable from an unauthorized process or workload identity.

## 15. Short-lived capability leases

Delegated capabilities SHALL be short-lived relative to task duration when technically practical.

Long-running tasks SHALL renew narrowly scoped capabilities based on current policy and state rather than issuing one broad credential for the entire run.

## 16. Delegation provenance

Every tool effect originating from delegated work SHALL be traceable to the complete principal chain and exact delegated subtask.

A child SHALL NOT present an effect as directly user-authored merely because the chain ultimately roots in the user.

---

# Part III — Composition-Aware Authorization

## 17. Per-action permission is insufficient

AlinaCoder SHALL evaluate dangerous combinations of otherwise-permitted actions.

Example:

```text
READ_PRIVATE_FILE = individually allowed
SEND_EXTERNAL_MESSAGE = individually allowed
READ_PRIVATE_FILE → SEND_EXTERNAL_MESSAGE = may be forbidden
```

A static allowlist for each operation is not sufficient for history-dependent safety.

## 18. CompositionClosureGuard

The deterministic control plane SHALL maintain a session/task-local record of security-relevant actions already exercised.

Minimum state:

```text
exercised_action_types
ordered_action_history
resource_taint_summary
external_destinations_used
secret_scopes_used
delegation_edges_used
```

Before admitting a new action, evaluate it against the prior-action state.

## 19. Prohibited pair constraints

Policy SHALL support forbidden unordered combinations such as:

```text
READ_SECRET + SEND_ARBITRARY_NETWORK
READ_PRIVATE_REPO + PUBLIC_UPLOAD
DECRYPT_CREDENTIAL + UNTRUSTED_PROCESS_EXECUTION
ENABLE_ADMIN_KEY + UNREVIEWED_MCP_TOOL
```

## 20. Prohibited ordered-sequence constraints

Policy SHALL support ordered patterns such as:

```text
RETRIEVE_UNTRUSTED_INSTRUCTION
→ ACCESS_SENSITIVE_DATA
→ EXTERNAL_WRITE
```

or:

```text
INSTALL_UNTRUSTED_PACKAGE
→ LOAD_SECRET
```

## 21. Resource-sensitive composition

The guard SHALL reason about concrete resources and labels, not only operation names.

For example, reading a public README then posting a summary is not equivalent to reading `.env` then posting externally.

## 22. Approval binding

When an action crosses a configured impact threshold, any human approval SHALL bind to:

```text
exact operation
exact material parameters
resource set
external destination
session/task identity
state version
policy epoch
single-use or bounded-use budget
```

Approval of one destination SHALL NOT authorize another destination.

## 23. History cannot launder authority

Repeated appearance of an action in previous tool output, memory, or successful past executions SHALL NOT turn it into current authorization.

Operational history is evidence, never authority.

---

# Part IV — Plan Dependency Freshness

## 24. Fresh memory does not imply fresh plan

AlinaCoder SHALL distinguish:

```text
STATE_FRESHNESS
PLAN_VALIDITY
```

An executor may possess the latest facts while still following a plan derived from obsolete facts.

## 25. PlanDependencyFence

Every plan that can authorize external effects or repository mutations SHALL declare the material state dependencies from which it was derived.

Minimum fields:

```text
plan_id
plan_version
intent_contract_version
dependency_records[]
dependency_versions[]
dependency_digests[]
control_dependencies[]
produced_at
validity_scope
action_nodes[]
```

## 26. Dependency-scoped pre-action validation

Immediately before an action, AlinaCoder SHALL revalidate the subset of plan dependencies that can affect that action.

If any material dependency changed:

```text
BLOCK
REPLAN_AFFECTED_REGION
or
REVALIDATE_AND_PROVE_EQUIVALENCE
```

Continuing silently is forbidden.

## 27. Repository examples

Material plan dependencies can include:

```text
current HEAD
file blob SHA
lockfile digest
selected test failures
API schema version
build configuration
active branch/ref
user correction
security policy epoch
provider/tool capability version
```

## 28. Online revision handling

When the user revises the task while execution is ongoing, AlinaCoder SHOULD avoid both extremes:

```text
blindly keep all old work
blindly discard all old work
```

Instead it SHALL compute impact through recorded data/control dependencies.

## 29. Revision impact propagation

A revision delta SHALL be intersected with:

```text
plan dependencies
produced artifacts
pending actions
active delegations
cached context projections
verification evidence
```

Affected work SHALL be stopped or invalidated.

Unaffected work MAY be preserved only when its validity is mechanically established.

## 30. Reused work revalidation

Work preserved after a revision SHALL be revalidated before it contributes to a mutation or completion verdict.

Incomplete provenance expands the invalidation set conservatively.

## 31. Stale response rejection remains binding

The existing `ResponseAdmissionGate` remains mandatory.

This amendment extends its responsibility: a response can be state-current but plan-stale. Both dimensions SHALL pass before mutation.

---

# Part V — Safe Checkpoint, Fork, Restore and Merge

## 32. Execution edits are typed security operations

AlinaCoder SHALL model:

```text
CHECKPOINT
FORK
RESTORE
MERGE
REWIND
RESUME
```

as explicit execution edits, not generic state loading.

## 33. ExecutionEditSafetyChecker

Before an execution edit that changes future execution, the runtime SHALL determine what prior actions/evidence the continuation must preserve.

The checker SHALL reject edits that could:

```text
duplicate a consumed authorization
duplicate an external effect
resurrect revoked authority
discard a still-required result
combine mutually inconsistent state
ignore an in-flight operation
silently change a committed branch history
```

## 34. Checkpoint dependency closure

A checkpoint SHALL record enough dependency metadata to establish which security-relevant facts remain valid after restore.

At minimum consider:

```text
canonical session state
repository HEAD and worktree fingerprint
durable effect journal
authorization ledger
policy/revocation epochs
active process identities
active tool/MCP versions
external dependency versions where material
random/nondeterministic decisions material to security
```

## 35. Restore is forward-only

Restoration SHALL create a new successor state whose parent is the current accepted head.

Historical content may be imported as candidate data, but lineage SHALL NOT be truncated.

Canonical model:

```text
CURRENT_HEAD
→ RESTORE_PROPOSAL(reference = historical_checkpoint)
→ VALIDATE
→ NEW_SUCCESSOR_HEAD
```

not:

```text
CURRENT_HEAD
→ pretend history after checkpoint never happened
```

## 36. Authority fields are non-restorable by default

Historical checkpoint restoration SHALL NOT restore old values for:

```text
revocation state
writer epoch
security minimum version
credential validity
consumed approval budget
consumed authorization budget
policy epoch
current user corrections
```

These fields remain current unless an explicitly authorized forward migration says otherwise.

## 37. Authority resurrection prohibition

A token, approval, capability, credential, or delegation that was consumed/revoked after a checkpoint SHALL remain consumed/revoked after restore.

## 38. External-effect mismatch detection

Before resuming from a checkpoint, compare checkpoint assumptions against durable external-effect evidence.

If an effect occurred after the checkpoint and cannot be safely represented in the restored continuation, the runtime SHALL block or construct a forward reconciliation.

## 39. Nondeterministic replay binding

Security-relevant nondeterministic outcomes that were relied upon before the checkpoint SHOULD be recorded and replayed from evidence rather than silently regenerated.

A post-restore model producing a different tool call SHALL NOT automatically be treated as equivalent to the original.

## 40. Replay-or-fork semantics

For irreversible tool calls after restore:

- semantically equivalent previously completed call → replay recorded result when safe;
- semantically different continuation → require a new explicit fork/action identity and fresh authority;
- consumed authority → reject reuse.

## 41. Merge safety

Execution branch merge SHALL NOT merge authority by union.

Effective merged authority is recomputed from current governing state.

External effects from both branches SHALL be reconciled explicitly before a merged branch can become canonical.

---

# Part VI — Secret Capability Mediation

## 42. SecretCapabilityBroker

AlinaCoder SHOULD keep high-value long-lived secrets outside model-visible memory and outside ordinary agent process state whenever technically practical.

Preferred pattern:

```text
agent proposes typed operation
→ deterministic gate authorizes exact use
→ broker retrieves/injects secret internally
→ broker performs constrained operation
→ broker redacts secret from outputs/logs
→ capability expires
```

## 43. Secret non-exportability goal

The model SHALL NOT receive secret plaintext merely because it needs an operation that requires the secret.

The system SHOULD expose a non-exportable action capability rather than the underlying credential.

## 44. Forbidden default secret surfaces

Long-lived secrets SHOULD NOT be placed by default in:

```text
prompt/context
model-visible memory
repository files
plaintext config
command-line arguments
untrusted child-process environment
CI logs
tool output
exception text
shell history
```

## 45. Broker-enforced request constraints

A secret-bearing broker invocation SHALL validate:

```text
destination
protocol
method/operation
path/resource
argument schema
parameter bounds
rate/budget
session/task binding
policy epoch
revocation epoch
anti-replay state
```

## 46. Windows local secret storage

For locally persisted provider credentials on Windows, AlinaCoder SHOULD prefer an OS-protected mechanism such as DPAPI/ProtectedData or another appropriate Windows credential facility rather than plaintext configuration.

Default DPAPI scope SHOULD be tied to the current user unless a justified machine-wide requirement exists.

## 47. DPAPI limitation awareness

DPAPI protects stored material but does not make secrets safe after the authorized process has decrypted them.

Therefore DPAPI SHALL be combined with process isolation, least privilege, output redaction, and broker mediation where useful.

## 48. Credential Locker optionality

Windows Credential Locker MAY be used when its application model and roaming semantics fit the credential type.

It SHALL NOT be selected merely because it is convenient.

## 49. In-memory secret minimization

Secret plaintext lifetime SHOULD be minimized.

Buffers SHOULD be released/zeroed where the language/runtime makes that meaningful and practical.

Secrets SHALL NOT be retained in reasoning digests or long-term memory.

## 50. Secret access receipts

Every use of a high-value secret SHOULD generate a metadata-only receipt containing:

```text
secret_handle_id
secret_scope
request_digest
destination
principal_chain_digest
authorization_instance_id
started_at
completed_at
outcome
```

The receipt SHALL NOT contain the secret.

---

# Part VII — Continuous MCP and Tool Trust

## 51. Onboarding is not permanent trust

A tool/MCP server that was benign at enrollment SHALL NOT be assumed benign forever.

AlinaCoder SHALL treat mutable tool definitions, schemas, endpoints, versions and observed behavior as continuously revalidatable state.

## 52. ToolDefinitionTransparencyRecord

At approval/enrollment, record:

```text
server_identity
endpoint_identity
transport
manifest_digest
tool_definition_digests[]
input_schema_digests[]
output_schema_digests[]
version/provenance evidence
approval_time
last_verified_at
```

## 53. Manifest pinning and drift

On reconnect or before material use, compare the current tool surface to the approved record.

Drift classes include:

```text
TOOL_ADDED
TOOL_REMOVED
DESCRIPTION_CHANGED
INPUT_SCHEMA_CHANGED
OUTPUT_SCHEMA_CHANGED
ENDPOINT_CHANGED
AUTH_SCOPE_CHANGED
VERSION_CHANGED
UNEXPLAINED_BEHAVIOR_CHANGED
```

Material drift SHALL cause revalidation before privileged use.

## 54. TrustShiftDetector

AlinaCoder SHOULD detect servers that behave benignly during onboarding but later change runtime behavior without a corresponding approved contract change.

Signals MAY include:

```text
new network destinations
new filesystem access
changed response semantics
changed downstream tool induction
changed latency/resource signature
new data classes returned
scope expansion
unexpected redirects
```

Behavioral detection is supplementary; hard policy boundaries remain primary.

## 55. InvocationAttestationLease

For high-impact remote tools where infrastructure support exists, execution admission SHOULD bind the authorization to the expected current workload identity and freshness evidence at invocation time.

Connect-time OAuth authorization alone SHALL NOT be interpreted as proof that the same trusted workload executes every later invocation.

## 56. Invocation-scoped binding

A protected invocation lease SHOULD be capable of binding:

```text
expected workload identity
freshness deadline
operation
object/resource
parameter bounds
downstream constraints
receipt obligations
sender identity
single-use/budget state
```

## 57. Tool output is data, not authority

Tool results can propose information and candidate actions but SHALL NOT directly authorize new effects.

Historical recurrence of a tool-suggested action SHALL NOT promote it to trusted instruction.

## 58. CrossToolInformationFlowPolicy

AlinaCoder SHALL track sensitive data crossing tool boundaries.

Minimum relationship:

```text
SOURCE_TOOL
→ DATA_CLASSIFICATION
→ TRANSFORMATION
→ SINK_TOOL
→ DESTINATION
```

A sink call SHALL be denied when the source-to-sink flow violates project policy, even when both tools are individually authorized.

## 59. Network-level observation

For high-risk third-party local tool execution, AlinaCoder SHOULD support host-observable egress telemetry when feasible.

The goal is to detect runtime behavior invisible in MCP descriptions and normal tool output.

## 60. Egress deny-by-default for untrusted tool execution

Where technically practical, newly enrolled or low-trust tool servers SHOULD start with restricted network egress.

Required hosts/ports are explicitly granted from observed and reviewed needs.

---

# Part VIII — Windows Execution Envelope

## 61. WindowsExecutionEnvelope

Each local autonomous process tree launched by AlinaCoder SHALL have an explicit execution envelope describing:

```text
process identity
parent task/stage
working directory
filesystem access level
network policy
secret access policy
CPU budget
memory budget
wall-clock budget
child-process policy
termination policy
sandbox level
```

## 62. Job Object control

On supported Windows environments, AlinaCoder SHOULD use Windows Job Objects or an equivalent robust mechanism to manage spawned process trees as a unit.

The controller SHOULD be able to enforce or observe:

```text
process-tree lifetime
CPU limits
memory limits
process count
termination on cancellation where appropriate
```

## 63. Child-process escape prevention

A process launch policy SHALL account for descendants.

Killing only the direct shell process while leaving grandchildren running SHALL be treated as incomplete cancellation.

## 64. AppContainer tier

For compatible workloads requiring stronger Windows isolation, AlinaCoder MAY use AppContainer-based isolation or another supported OS sandbox mechanism.

Compatibility and required capabilities SHALL be measured rather than assumed.

## 65. Sandbox levels

Canonical local execution levels:

```text
LEVEL_0_READ_ONLY_ANALYSIS
LEVEL_1_RESTRICTED_PROCESS
LEVEL_2_SANDBOXED_TEST
LEVEL_3_TRUSTED_PROJECT_BUILD
LEVEL_4_PRIVILEGED_HOST_OPERATION
```

Transitions between levels require deterministic admission.

## 66. Network and filesystem are separate capabilities

Permission to execute a process SHALL NOT imply:

```text
arbitrary filesystem write
arbitrary network access
secret access
registry mutation
service installation
```

Each is independently granted.

## 67. Resource exhaustion defense

Local tools/models/builds SHALL be governed by bounded resource policies so a malformed or hostile workload cannot indefinitely consume the host.

Pressure signals already used by the ResourceController SHALL feed execution admission and cancellation.

## 68. Process identity on recovery

Recovered sessions SHALL identify child processes using durable process metadata stronger than executable name alone.

The runtime SHALL NOT kill unrelated user processes merely because they share a filename.

---

# Part IX — Context, Cache and Long-Horizon Continuity

## 69. Context is an execution substrate

Context assembly SHALL be treated as a governed runtime operation, not append-only prompt concatenation.

## 70. ContextQueryPlanner

For each model invocation, AlinaCoder SHOULD compile context from structured sources using an explicit plan:

```text
BIND required state
→ PLAN candidate sources
→ FILTER by authority/freshness/sensitivity
→ OPTIMIZE ordering/cache locality/token budget
→ MATERIALIZE working view
→ EXECUTE
→ RECORD feedback
```

## 71. Lossless Event Log

Compaction SHALL NOT destroy the authoritative historical record.

A durable append-only or equivalently lossless event log SHALL retain exact addresses to prior evidence, tool results, decisions, corrections and effects.

## 72. Working view vs ground truth

AlinaCoder SHALL distinguish:

```text
LOSSLESS_GROUND_TRUTH
DERIVED_WORKING_VIEW
```

Eviction from the working view does not delete ground truth.

## 73. Typed session namespace

Large tool outputs and derived state SHOULD be stored as typed objects/variables referenced by stable identities rather than repeatedly serializing their full content into every prompt.

Only the projection needed for the current inference SHOULD enter the model context.

## 74. CacheValidityBeforeLocality

Prompt/KV cache locality is an optimization only after validity.

The following priority is mandatory:

```text
correct current state
> valid current plan
> policy/privacy constraints
> required evidence
> cache hit
```

A cache hit SHALL NOT justify preserving stale content.

## 75. Cache dependency manifest

Reusable cached prompt segments SHOULD expose the state they depend on.

When a dependency changes, the segment is invalidated or rebuilt.

## 76. Compaction validity

A summary that omits a constraint SHALL NOT silently replace the original constraint.

Critical constraints, authority, unresolved failures, external effects and rollback state SHALL be pinned or independently reconstructible.

## 77. Eviction landmarks

When large historical regions are evicted, maintain compact landmarks pointing to exact event-log ranges so AlinaCoder can rehydrate relevant evidence without rescanning the entire history.

---

# Part X — Optional Supabase Hardening

## 78. Supabase remains optional

The local continuity/control plane remains canonical.

Loss, outage, removal, rate limiting or configuration of Supabase SHALL NOT prevent AlinaCoder from operating locally within its core guarantees.

## 79. Current platform-change awareness

Any implementation using Supabase SHALL consult the current Supabase changelog and documentation before relying on API behavior.

Breaking changes SHALL be represented in compatibility tests rather than remembered as permanent assumptions.

## 80. Publishable vs secret keys

Client/desktop-visible Supabase integrations SHALL use publishable keys where appropriate.

`service_role` and modern secret keys SHALL NOT be embedded in `AlinaCoder.exe`, public source, browser code, model context, logs, or untrusted child-process environments.

## 81. Secret key backend confinement

Supabase secret keys bypass Row Level Security and SHALL be treated as high-impact backend credentials.

If used at all, they SHALL remain behind a trusted local/server broker and be split by component where practical for independent rotation.

## 82. Vault status and optionality

Supabase Vault MAY be used for optional remote secret storage when its risk/feature status is acceptable.

Because Vault is currently documented as a public-alpha feature, it SHALL NOT become a mandatory dependency for AlinaCoder’s root trust or local secret availability.

## 83. Vault access boundary

Access to decrypted Vault views/functions SHALL be governed as secret access.

A role able to query decrypted secret material is privileged regardless of encryption at rest.

## 84. RLS and exposed schemas

Any AlinaCoder table exposed through the Supabase Data API SHALL have explicit Row Level Security and ownership/tenant predicates appropriate to the data model.

`TO authenticated` alone is not authorization.

## 85. Security-invoker views

Views containing user/project-scoped data SHOULD use `security_invoker` on supported Postgres versions or otherwise be placed behind correct privilege controls.

## 86. Queue usage

If Supabase Queues/`pgmq` are used for optional remote coordination:

- basic/durable queues are preferred for work that must survive restart;
- unlogged queues SHALL NOT carry authoritative task/effect state;
- queue visibility timeouts SHALL be reconciled with authorization consumption to avoid duplicate effects;
- exposing queues through PostgREST requires deliberate permissions and RLS on queue tables.

## 87. Realtime is notification, not authority

Supabase Realtime/Broadcast MAY signal that state changed.

A Realtime event SHALL NOT itself authorize a mutation.

Receivers SHALL fetch or validate canonical state/version before acting.

## 88. Supabase key rotation

Where Supabase keys are used, independent named keys and staged rotation SHOULD be preferred over shared long-lived secrets.

Key rotation SHALL have a compatibility window and explicit revocation evidence.

---

# Part XI — New Verification Scenarios

## 89. Authorization-consumption tests

The evaluation suite SHALL include at minimum:

1. single-use authorization followed by identical retry;
2. single-use authorization followed by semantically equivalent retry with a new request ID;
3. eight concurrent consumers competing for budget one;
4. parent and child attempting to consume the same delegated budget;
5. crash after preparation before effect;
6. crash after effect before commit receipt;
7. restored checkpoint attempting fresh token issuance for consumed authority;
8. confirmation replay after action already committed.

Expected invariant:

```text
committed_effects <= authorized_execution_budget
```

## 90. Composition tests

Test at minimum:

- individually allowed read + individually allowed external send but forbidden combination;
- safe public read + safe send remains allowed;
- sensitive read transformed through summary retains taint;
- prior history cannot promote a forbidden action to allowed;
- sequence constraints survive model/provider switch.

## 91. Delegation tests

Test:

- child attempts scope widening;
- child attempts resource widening;
- child attempts longer expiry;
- stolen capability from wrong workload;
- revoked parent invalidates dependent descendants;
- shared child with an independent valid parent retains only independently rooted authority.

## 92. Plan freshness tests

Test:

- dependency changes after planning but executor sees latest memory;
- unrelated record changes and plan remains valid;
- user correction invalidates only affected plan region;
- preserved unaffected work is revalidated before commit;
- incomplete dependency provenance expands invalidation conservatively.

## 93. Execution-edit tests

Test:

- restore before already-completed external effect;
- restore resurrecting consumed approval;
- restore with stale tool manifest;
- merge branches with conflicting external effects;
- fork from checkpoint after policy epoch change;
- checkpoint with in-flight mutation;
- nondeterministic post-restore call differs materially from original.

## 94. Secret mediation tests

Test:

- model requests raw secret and is denied;
- broker can perform allowed operation without returning secret;
- broker rejects destination drift;
- broker rejects argument-schema drift;
- logs contain handle metadata but no secret plaintext;
- untrusted test process cannot inherit high-value credential;
- revoked credential handle fails immediately.

## 95. MCP trust tests

Test:

- manifest description drift;
- schema drift;
- newly added privileged tool;
- server remains benign during onboarding then changes destination;
- response attempts to induce unrelated privileged tool call;
- cross-tool sensitive source-to-external-sink flow;
- OAuth remains valid but workload attestation becomes stale.

## 96. Windows envelope tests

Test:

- child tree termination on cancellation;
- process count limit;
- memory/CPU pressure response;
- no secret inheritance at restricted sandbox level;
- network denial independent of process execution;
- recovery does not kill unrelated same-name process.

## 97. Context/cache tests

Test:

- cached prompt segment invalidated by dependency change;
- working-view eviction can rehydrate exact source evidence;
- compaction preserves pinned authority/constraints;
- fresh state plus stale plan is rejected;
- cache locality never overrides privacy or policy incompatibility.

## 98. Supabase optionality tests

When Supabase integration is enabled, test:

- complete local operation during Supabase outage;
- secret key never appears in client artifact;
- RLS denies cross-project reads;
- queue redelivery cannot duplicate committed effect;
- Realtime duplicate/out-of-order notifications do not create duplicate actions;
- Vault unavailability does not destroy local root trust.

---

# Part XII — Observability

## 99. AuthorityDecisionTrace

For every high-impact action, record:

```text
authorization_instance_id
principal_chain_digest
plan_id
plan_dependency_verdict
composition_guard_verdict
policy_epoch
revocation_epoch
budget_before
budget_after
secret_handle_id_if_any
tool/workload trust proof
state_version
final effect receipt
```

## 100. RecoveryDecisionTrace

For restore/fork/merge operations, record:

```text
execution_edit_id
edit_type
source_checkpoint
current_head
historical_effects_after_checkpoint
consumed_authorities_after_checkpoint
stale_dependencies
safe_continuation_set
selected_continuation
reconciliation_actions
```

## 101. ToolTrustTrace

For MCP/tool use, record:

```text
server_identity
manifest_digest
approved_manifest_digest
drift_class
behavior_baseline_version
invocation_lease_id
network destination summary
cross_tool_flow_verdict
```

## 102. SecretUseTrace

Secret use telemetry SHALL identify that a capability was used without logging the secret itself.

---

# Part XIII — Conceptual Modules

## 103. Authorization modules

Conceptual additions:

```text
src/alinacoder/authority/
  authorization_instance.py
  consumption_ledger.py
  consumption_fsm.py
  delegation_chain.py
  capability_lease.py
  composition_guard.py
  approval_binding.py
  revocation_graph.py
```

## 104. Planning and revision modules

```text
src/alinacoder/planning/
  plan_dependency_manifest.py
  plan_dependency_fence.py
  revision_impact.py
  validity_reuse.py
```

## 105. Recovery modules

```text
src/alinacoder/recovery/
  execution_edit.py
  execution_edit_safety.py
  forward_restore.py
  replay_or_fork.py
  external_effect_reconciler.py
```

## 106. Secret modules

```text
src/alinacoder/security/
  secret_capability_broker.py
  windows_secret_store.py
  secret_redactor.py
  secret_use_receipt.py
```

## 107. Tool trust modules

```text
src/alinacoder/tool_trust/
  manifest_transparency.py
  manifest_drift.py
  trust_shift.py
  invocation_attestation.py
  cross_tool_flow.py
  egress_policy.py
```

## 108. Windows execution modules

```text
src/alinacoder/windows_runtime/
  execution_envelope.py
  job_object_controller.py
  sandbox_level.py
  process_identity.py
```

## 109. Context modules

```text
src/alinacoder/context/
  context_query_planner.py
  event_log.py
  typed_namespace.py
  cache_dependency.py
  eviction_landmarks.py
```

## 110. Evaluation additions

```text
src/alinacoder/evaluation/
  semantic_replay_bench.py
  composition_closure_bench.py
  delegation_attenuation_bench.py
  stale_plan_bench.py
  execution_edit_bench.py
  secret_broker_bench.py
  mcp_trust_drift_bench.py
  windows_envelope_bench.py
  context_cache_validity_bench.py
```

---

# Part XIV — Canonical Runtime Integration

## 111. Updated action path

```text
User turn
→ Repair Graph
→ IntentContract
→ CanonicalSessionState
→ Task/Stage plan
→ PlanDependencyManifest
→ CapabilityRequirementVector
→ model/provider routing
→ candidate semantic action
→ state/version admission
→ PlanDependencyFence
→ AgenticPrincipalChain authority
→ CompositionClosureGuard
→ AuthorizationInstance lookup/create
→ AuthorizationConsumptionLedger
→ tool/workload trust proof
→ SecretCapabilityBroker if needed
→ WindowsExecutionEnvelope / remote execution envelope
→ PREPARE durable budget
→ ExternalEffectGate
→ effect
→ causal observation/receipt
→ COMMIT authorization consumption
→ verification
→ memory/experience proposal
→ pre-persistence governance
→ completion
```

## 112. Updated recovery path

```text
crash / rollback request / rewind / fork / merge
→ freeze new mutations
→ load durable journal
→ load current authority ledger
→ enumerate external effects since candidate checkpoint
→ validate policy/revocation epochs
→ ExecutionEditSafetyChecker
→ construct safe continuation set
→ forward restore/fork/merge successor
→ revalidate plan dependencies
→ reconcile prepared effects
→ resume with current authority, never historical authority
```

## 113. Updated MCP path

```text
discover server
→ official/provenance checks
→ manifest fingerprint
→ static/security evaluation
→ capability handshake
→ constrained canary
→ enroll
→ before material use: re-fetch manifest
→ detect drift
→ establish invocation lease
→ composition + information-flow checks
→ constrained execution
→ observe network/tool behavior
→ update trust evidence
```

## 114. Updated secret path

```text
model requires credentialed operation
→ model emits typed action without secret
→ deterministic policy gate
→ secret capability broker loads protected secret
→ broker validates exact destination/operation/parameters
→ broker executes
→ broker redacts response
→ secret-use receipt
→ secret handle expires
```

---

# Part XV — Non-Negotiable Invariants

## 115. Authorization invariants

```text
NEW_TOKEN != NEW_AUTHORITY
RETRY != NEW_AUTHORITY
RESTORE != AUTHORITY_RESET
DELEGATION_CAN_ONLY_NARROW
COMMITTED_EFFECT_COUNT <= AUTHORIZED_BUDGET
```

## 116. Plan invariants

```text
FRESH_STATE != VALID_PLAN
MATERIAL_DEPENDENCY_CHANGE => REVALIDATE_OR_REPLAN
UNKNOWN_DEPENDENCY_PROVENANCE => CONSERVATIVE_INVALIDATION
```

## 117. Recovery invariants

```text
RESTORE_IS_FORWARD_TRANSITION
HISTORICAL_AUTHORITY_CANNOT_BE_RESURRECTED
EXTERNAL_EFFECTS_ARE_NOT_UNDONE_BY_LOCAL_ROLLBACK
MERGE_DOES_NOT_UNION_AUTHORITY
```

## 118. Secret invariants

```text
NEED_TO_USE_SECRET != NEED_TO_REVEAL_SECRET
MODEL_CONTEXT_IS_NOT_A_SECRET_STORE
UNTRUSTED_CHILD_PROCESS_GETS_NO_STANDING_SECRET
SECRET_USE_REQUIRES_CURRENT_AUTHORITY
```

## 119. Tool trust invariants

```text
ONCE_APPROVED != FOREVER_TRUSTED
OAUTH_CONNECTED != CURRENT_WORKLOAD_ATTESTED
TOOL_OUTPUT != EXECUTION_AUTHORITY
INDIVIDUALLY_ALLOWED_TOOLS != ALLOWED_DATA_FLOW
```

## 120. Context invariants

```text
CACHE_HIT < VALIDITY
SUMMARY != GROUND_TRUTH
EVICTED != LOST
COMPACTION_CANNOT_DROP_BINDING_CONSTRAINTS
```

## 121. Supabase invariants

```text
SUPABASE_OPTIONAL = true
LOCAL_CORE_DEPENDS_ON_SUPABASE = false
SECRET_KEY_IN_DESKTOP_BINARY = forbidden
REALTIME_EVENT_IS_AUTHORITY = false
```

---

# Part XVI — Research Basis

## 122. Research directions incorporated

This amendment incorporates design lessons from current 2026 work on:

- durable authorization consumption and semantic replay across retries/replans;
- multi-agent authorization propagation and attenuation;
- history-dependent composition closure;
- task-scoped authorization and operand provenance;
- workload-bound invocation leases for remote MCP execution;
- stale-plan execution despite fresh shared memory;
- validity-guided online revision recovery;
- safe checkpoint/fork/restore/merge semantics;
- semantic rollback and authority resurrection;
- forward-only transactional continuity kernels;
- MCP tool poisoning, rug pulls, trust-shift attacks and network-observable tool supply-chain behavior;
- long-horizon context as a structured execution environment;
- database-inspired context assembly and prompt-cache dependency management;
- Windows Job Objects, AppContainer isolation and OS-protected credential storage;
- current Supabase API-key, Vault, RLS, Queues and Realtime semantics.

Research evidence is an input to design, not runtime authority. All safety-critical guarantees above remain defined as deterministic AlinaCoder contracts that must be tested independently.

---

# Part XVII — Final Target Behavior

## 123. Desired user experience

The user should be able to speak or write ordinary French while the runtime silently preserves the stronger semantics:

```text
User asks AlinaCoder to act
→ AlinaCoder understands the current intent
→ picks the strongest eligible zero-cost intelligence
→ creates/updates a dependency-aware plan
→ delegates only the minimum authority needed
→ never hands raw credentials to the model when a broker can act instead
→ prevents individually safe tools from composing into an unsafe flow
→ rejects stale plans even when memory is fresh
→ survives retry/crash/rewind without duplicating authority or effects
→ detects MCP/tool drift after onboarding
→ contains local process trees on Windows
→ preserves exact historical evidence while optimizing context/cache
→ verifies the final result
→ commits/pushes only when all current contracts still hold
```

The goal is not maximal autonomy by granting maximal standing privilege.

The goal is:

> **maximum autonomous capability inside a mechanically narrow, durable, replay-resistant and continuously revalidated authority envelope.**
