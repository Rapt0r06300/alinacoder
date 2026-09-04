# AlinaCoder v0.2 — Operational Trust, Durable Recovery, Stochastic Verification & Desktop Grounding Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose and precedence

This amendment strengthens AlinaCoder at the boundary between a correct coding agent and a trustworthy long-running Windows product. It is additive to the v0.2 baseline and every previously approved amendment.

Where this amendment introduces stricter requirements for release provenance, secure self-update, crash recovery, stochastic verification, MCP/skill supply-chain integrity, Windows desktop verification, project isolation, resource budgets, or optional Supabase coordination, the stricter rule has precedence.

The central principle is:

> **AlinaCoder SHALL be able to prove what binary is running, recover durable work without duplicating side effects, distinguish stochastic evidence from deterministic proof, distrust mutable extension surfaces, verify its real Windows UI semantically, isolate project state and credentials by construction, and reject performance or operational regressions even when functional tests remain green.**

The target is not merely a source repository that is correct. The target is a complete operational chain:

```text
approved source
→ reproducible/attested build
→ identified artifact
→ trusted distribution
→ verified launch
→ durable task execution
→ evidence-grounded verification
→ safe extension/tool use
→ isolated project state
→ bounded resource use
→ recoverable self-update
```

No layer in this chain may silently substitute for another.

---

# Part I — Executable Release Provenance

## 2. ArtifactIdentity

Every releasable executable artifact SHALL have a stable machine-readable identity.

Minimum fields:

```text
artifact_name
artifact_version
artifact_sha256
source_repo
source_commit_sha
source_tree_sha
build_definition_digest
builder_identity
build_run_id
build_timestamp
platform
architecture
dependency_lock_digest
sbom_digest
provenance_digest
signature_digest
```

For the primary Windows product, the canonical artifact name is:

```text
AlinaCoder.exe
```

Installer/package artifacts SHALL have separate identities rather than inheriting the EXE identity implicitly.

## 3. Source-to-artifact binding

A Git commit SHA alone SHALL NOT be treated as proof that a launched binary corresponds to that commit.

AlinaCoder SHALL preserve a verifiable source-to-artifact chain:

```text
source commit/tree
→ build definition
→ resolved dependencies
→ builder identity
→ produced artifact digest
→ release manifest
→ signature/provenance
→ launched binary digest
```

## 4. SignedReleaseManifest

Each promoted release SHALL contain or be accompanied by a `SignedReleaseManifest`.

Minimum fields:

```text
release_id
version
channel
source_commit_sha
source_tree_sha
artifact_set[]
artifact_sha256[]
sbom_ref
provenance_ref
build_identity
created_at
minimum_supported_state_schema
maximum_supported_state_schema
rollback_compatible_with[]
```

The manifest itself SHALL be integrity-protected.

## 5. Build provenance

Release builds SHOULD emit SLSA-compatible provenance or an equivalent verifiable statement containing at minimum:

- exact source identity;
- builder identity;
- build definition identity;
- resolved dependencies where practical;
- produced artifact digests;
- external build parameters;
- run metadata.

The verifier SHALL reject provenance from an unexpected signer/builder pair.

## 6. Artifact signatures

The release pipeline SHOULD use independent artifact-signing evidence in addition to provenance.

For generic release artifacts, Sigstore/cosign-compatible signing MAY be used.

For Windows production binaries, Authenticode-compatible code signing SHOULD be supported when an appropriate signing identity is available.

## 7. Timestamping

Production Windows signatures SHOULD be timestamped so validity can survive normal certificate expiry according to platform rules.

Timestamp verification SHALL be distinct from artifact hash verification.

## 8. Signature independence rule

The system SHALL distinguish:

```text
SOURCE_IDENTITY
BUILD_PROVENANCE
ARTIFACT_SIGNATURE
DISTRIBUTION_FRESHNESS
RUNTIME_DIGEST
```

A valid artifact signature does not prove the source was correct.

Valid provenance does not prove the downloaded file was not substituted unless the digest matches.

A matching digest does not prove the release is fresh or authorized as current.

## 9. RuntimeArtifactVerifier

Before a newly downloaded or updated core is launched, `RuntimeArtifactVerifier` SHALL check:

```text
manifest validity
artifact digest
provenance identity
expected source repo
expected release channel
signature policy
freshness/update metadata
state-schema compatibility
anti-rollback policy
```

Failure SHALL be fail-closed for the candidate update.

The last-known-good installed version SHALL remain launchable when safe.

---

# Part II — Secure Auto-Update

## 10. UpdateTrustRoot

AlinaCoder SHALL maintain an explicit update trust root independent of ordinary model reasoning.

The LLM SHALL NOT be able to redefine the trusted update root during normal coding work.

## 11. TUF-style update semantics

The updater SHOULD implement TUF-style or equivalent protections for:

```text
root trust
role separation
metadata versioning
expiry
snapshot consistency
target hashes
anti-rollback
freeze-attack resistance
key rotation
```

The exact implementation MAY use a compatible library or a simpler equivalent only if the same required security properties are mechanically demonstrated.

## 12. Update candidate lifecycle

A candidate release SHALL move through explicit states:

```text
DISCOVERED
METADATA_VERIFIED
ARTIFACT_DOWNLOADED
ARTIFACT_VERIFIED
STATE_COMPATIBILITY_VERIFIED
CANARY_READY
CANARY_PASSED
STAGED
PROMOTED
ACTIVE
```

Failure states include:

```text
INVALID_SIGNATURE
INVALID_PROVENANCE
HASH_MISMATCH
METADATA_EXPIRED
ROLLBACK_BLOCKED
STATE_INCOMPATIBLE
CANARY_FAILED
POST_LAUNCH_FAILED
QUARANTINED
```

## 13. Atomic update switch

Updating SHALL use an atomic or transactionally equivalent activation sequence.

Canonical sequence:

```text
verify candidate
→ persist current active version
→ persist recovery pointer
→ stage candidate separately
→ canary candidate
→ atomically change active pointer
→ launch smoke probe
→ accept OR revert
```

Overwriting the currently running binary in place SHALL NOT be the preferred design.

## 14. Last-known-good release

At least one verified last-known-good release SHALL remain recoverable after an update attempt, subject to explicit storage policy.

## 15. Update rollback policy

Rollback SHALL be allowed only when all of the following are true:

- target version is explicitly trusted;
- rollback is compatible with current persistent-state schema;
- rollback does not violate a security minimum version;
- required migrations can be reversed or the old runtime can safely read current state.

## 16. Security floor

A `MinimumSafeVersion` or equivalent revocation policy SHALL prevent returning to a known-vulnerable version merely because it remains cryptographically valid.

## 17. No autonomous paid signing dependency

The zero-autonomous-spend policy remains binding.

If a production signing mechanism requires paid infrastructure, AlinaCoder SHALL NOT purchase or enable it autonomously.

The release design SHALL still preserve hashes, provenance and verifiable local build identity where cost-free signatures are unavailable.

---

# Part III — Reproducible Builds, SBOM & Dependency Closure

## 18. ReproducibleBuildComparator

Release engineering SHOULD strive for deterministic or reproducible artifacts where practical.

`ReproducibleBuildComparator` SHALL distinguish:

```text
BYTE_IDENTICAL
SEMANTICALLY_EQUIVALENT_WITH_EXPLAINED_VARIANCE
NON_REPRODUCIBLE_KNOWN_CAUSE
NON_REPRODUCIBLE_UNKNOWN_CAUSE
```

Unknown release variance SHALL block high-trust promotion until resolved or explicitly governed.

## 19. Reproducibility inputs

Where practical, record:

- exact toolchain versions;
- lockfiles;
- build flags;
- locale/timezone assumptions;
- environment variables that affect output;
- packaging versions;
- compression settings;
- generated timestamps;
- source date epoch or equivalent controls.

## 20. SBOM

Every promoted Windows release SHOULD produce an SBOM covering bundled libraries and distributable dependencies.

The SBOM SHALL be content-addressed and linked from the release manifest.

## 21. DependencyDigestClosure

Critical build dependencies that can materially affect output SHOULD be represented by immutable digests or otherwise pinned identities.

Mutable tags such as `latest` SHALL NOT be sufficient for trusted release construction.

## 22. Release drift

A rebuild from the same source that produces a different dependency closure SHALL be classified as:

```text
BUILD_INPUT_DRIFT
```

and SHALL require explanation before being considered equivalent.

---

# Part IV — Durable Execution Journal

## 23. DurableExecutionJournal

Long-running AlinaCoder work SHALL be recoverable across:

```text
process crash
forced termination
machine reboot
power loss
provider disconnect
model failover
application update
```

The runtime SHALL maintain an append-only or equivalently auditable durable execution journal.

## 24. Intent–Effect–Observation protocol

Before a side effect that cannot be safely reconstructed from pure computation, persist an intent record.

Canonical structure:

```text
INTENT_DURABLE
→ EFFECT_ATTEMPT
→ EFFECT_OBSERVED
→ ACK_DURABLE
```

The exact protocol MAY vary by effect class, but the system SHALL always know whether an effect is:

```text
NOT_STARTED
INTENDED_NOT_OBSERVED
OBSERVED_NOT_ACKED
ACKNOWLEDGED
UNKNOWN_REQUIRES_RECONCILIATION
```

## 25. EffectRecord

Minimum fields:

```text
effect_id
task_id
stage_id
effect_type
idempotency_key
precondition_state_version
precondition_hash
intent_payload_digest
attempt_count
external_target
started_at
observed_result_digest
acknowledged_at
recovery_policy
```

## 26. Idempotency keys

Every repeatable externally mutating operation SHOULD use an idempotency key or equivalent operation identity where the destination supports it.

When the destination does not support idempotency, AlinaCoder SHALL use reconciliation before retrying.

## 27. Exactly-once language

AlinaCoder SHALL NOT claim literal exactly-once semantics for external side effects unless that property is actually guaranteed end to end.

Preferred operational guarantee:

> **at-least-once attempt with idempotent/reconciled effect, or fail-closed ambiguity requiring reconciliation.**

## 28. RecoveryReconciler

On startup after unclean termination, `RecoveryReconciler` SHALL scan incomplete effects and classify each one before further mutation.

Possible actions:

```text
CONFIRM_ALREADY_APPLIED
SAFE_TO_RETRY
ROLL_BACK_LOCAL_INTENT
RECONCILE_REMOTE_STATE
QUARANTINE_AMBIGUOUS
REQUIRE_USER_FOR_IRREVERSIBLE_AMBIGUITY
```

## 29. Git operation recovery

Git recovery SHALL distinguish at minimum:

```text
working-tree edit only
index change
local commit created
remote push attempted
remote push confirmed
branch/ref changed externally
```

A retry SHALL verify repository identity and current HEAD again.

## 30. OrphanProcessReaper

Child processes launched by a task SHALL be recorded with enough identity to determine whether they are still valid after recovery.

The runtime SHALL NOT blindly kill processes based only on executable name.

## 31. BootRecoveryFSM

Startup SHALL enter a recovery finite-state machine before normal autonomous work when an unclean previous session is detected.

Canonical sequence:

```text
load durable state
→ verify state integrity
→ verify repository identities
→ inspect incomplete effects
→ reconcile
→ verify last-known-good checkpoints
→ resume eligible tasks
```

## 32. Crash-injection testing

The test harness SHALL support deterministic crash injection at meaningful boundaries such as:

```text
before intent persistence
after intent persistence
mid-tool call
after external effect
before observation persistence
after observation persistence
before ACK
after ACK
before commit
after commit
before push
after push response loss
mid-update activation
```

Each injection SHALL assert post-restart safety.

---

# Part V — Stochastic Verification Engine

## 33. StochasticTestEvidence

AlinaCoder SHALL distinguish deterministic software checks from stochastic agent/model behavior.

A single stochastic run SHALL NOT automatically establish a stable capability or regression.

## 34. Three-valued stochastic verdict

Stochastic evaluation SHALL support:

```text
PASS
FAIL
INCONCLUSIVE
```

`INCONCLUSIVE` is mandatory when available evidence cannot separate acceptable behavior from noise at the configured confidence level.

## 35. StatisticalTestContract

Minimum fields:

```text
scenario_id
agent_configuration
model_lineage
harness_version
repository_fixture
success_definition
alpha
beta
minimum_effect_size
trial_budget
sequential_test_policy
seed_policy
verdict
confidence_interval
```

## 36. Sequential evidence

Where suitable, sequential testing such as SPRT or an equivalent bounded sequential method SHOULD stop early when evidence becomes decisive.

This reduces unnecessary inference while preserving the declared error bounds.

## 37. Multi-rollout reliability

For stochastic agent benchmarks, reliability metrics SHALL be based on independent complete rollouts rather than the number of unit tests inside a single rollout.

Unit-test count SHALL NOT be misused as independent sample count.

## 38. ReliabilityAtK semantics

If a reliability-at-k metric is used:

```text
n = number of independent full rollouts
c = number of fully successful rollouts
```

Partial unit-test successes inside one rollout SHALL be reported separately.

## 39. BehavioralFingerprint

Agent regression detection SHOULD include compact behavioral fingerprints in addition to terminal pass/fail.

Potential dimensions:

```text
tool sequence class
state-transition pattern
repair count
rollback count
context fold count
model switches
file-touch distribution
verification coverage
completion route
token/latency efficiency
```

## 40. Trace-first offline analysis

Previously recorded immutable traces SHOULD be reused for zero- or low-inference regression checks where no live model call is required.

Offline replay SHALL NOT be treated as a full substitute for live evaluation when enforcement changes subsequent behavior.

## 41. FlakeSignatureRegistry

Repeatedly unstable deterministic tests SHALL receive a `FlakeSignature` rather than being silently retried until green.

Minimum fields:

```text
test_id
failure_signatures
pass_rate
fail_rate
environment_correlation
timing_correlation
resource_correlation
first_seen
last_seen
quarantine_status
```

## 42. Retry integrity

Retries SHALL preserve evidence of all attempts.

A final pass after repeated failures SHALL NOT erase the earlier failures.

## 43. Regression gate

A stochastic regression gate SHALL compare distributions or calibrated confidence intervals rather than raw one-run outcomes when the subject under test is non-deterministic.

## 44. Stable deterministic core

Where a behavior can reasonably be made deterministic through schemas, state machines, typed actions, stable tool selection or deterministic policy checks, AlinaCoder SHOULD prefer deterministic enforcement over spending stochastic trial budget.

---

# Part VI — MCP Protocol & Tool Supply-Chain Integrity

## 45. MCPVersionContract

Every MCP connection SHALL record the protocol revision and negotiated/supported capabilities.

A server SHALL NOT be treated as permanently compatible merely because a previous session succeeded.

## 46. MCPCompatibilityHandshake

Before a server becomes eligible for mutating work, the client SHALL verify:

```text
server identity
protocol version
capabilities
tools/resources/prompts exposed
tool schemas
auth mode
transport
critical extension declarations
```

## 47. ToolManifestFingerprint

For each connected MCP server, generate a canonical fingerprint over the exposed tool manifest.

The fingerprint SHOULD include:

```text
tool name
description digest
input schema
output schema if declared
annotations/capabilities
protocol version
server identity/version
```

## 48. MCPManifestDriftGate

If the server manifest changes since the last trusted observation, classify the change before allowing ordinary mutating calls.

States:

```text
UNCHANGED
ADDITIVE_NON_PRIVILEGED
SCHEMA_COMPATIBLE_CHANGE
BREAKING_SCHEMA_CHANGE
CAPABILITY_EXPANSION
PRIVILEGE_EXPANSION
TOOL_REMOVED
IDENTITY_CHANGED
UNKNOWN_DRIFT
```

Breaking, privilege-expanding or unknown changes SHALL fail closed until re-canarying.

## 49. Schema generation lease

Tool schemas SHALL have a generation identifier.

A tool call prepared against generation `g` SHALL NOT be sent after the manifest has advanced to incompatible generation `g+1`.

## 50. MCPLeastCapabilityProjection

AlinaCoder SHOULD expose to a model only the subset of MCP tools needed for the active task/stage.

Tool discovery MAY be broad, but model-visible capability SHOULD be minimal.

## 51. MCPConformanceCanary

New or changed servers SHOULD pass read-only or sandboxed canaries for:

- schema validity;
- error semantics;
- timeout behavior;
- cancellation;
- auth failure;
- malformed argument rejection;
- deterministic postconditions where applicable.

## 52. MCP response taint

Data returned by untrusted or lower-trust MCP sources SHALL retain provenance/taint when later used to form sensitive tool calls.

Untrusted content SHALL NOT silently become authority.

---

# Part VII — Skill, Hook & Agent Configuration Supply Chain

## 53. SkillBundleIdentity

Every loaded skill, agent manifest, hook and executable configuration bundle SHALL have an identity including:

```text
origin
scope
version_or_commit
content_digest
trust_class
permissions
introduced_at
last_verified_at
```

## 54. SignedSkillBundle

Where a signed upstream artifact exists, AlinaCoder SHOULD verify it.

Unsigned local skills MAY still be used, but SHALL have explicit local provenance and digest.

## 55. SkillLineageTaint

If one skill/configuration is generated or materially transformed using untrusted instructions, the derived artifact SHALL inherit the relevant taint until independently reviewed/validated.

Rewriting text does not erase provenance.

## 56. RecursiveSkillQuarantine

A skill later classified as malicious or unsafe SHALL trigger a search for descendants and dependent configurations influenced by it.

Potential descendants SHALL be marked:

```text
TAINTED_BY_ANCESTOR
```

until revalidated.

## 57. LifecycleHookIntegrityFirewall

Hooks that execute automatically during session startup, pre-tool, post-tool, commit, push, shutdown or recovery SHALL be treated as executable supply-chain components.

A model SHALL NOT gain broader authority merely by editing a hook file.

## 58. Hook mutation policy

A hook change SHALL require:

```text
explicit diff
capability delta
permission delta
tests
recovery behavior
provenance update
```

## 59. Prompt/config injection boundary

Repository content that resembles agent instructions SHALL be treated as project data unless it is located in an explicitly trusted instruction surface and passes applicable trust rules.

---

# Part VIII — Windows Desktop Semantic Oracle

## 60. DesktopSemanticOracle

AlinaCoder SHALL verify its real Windows desktop product using semantic OS state whenever available rather than relying primarily on screenshot coordinate guessing.

Canonical perception ladder:

```text
Windows UI Automation (UIA)
→ stable semantic control identity
→ MSAA/Win32 accessibility fallback
→ application-specific native API if explicitly allowed
→ vision/OCR augmentation
→ raw coordinates only as last resort
```

## 61. Semantic-first rule

If a target control exposes a reliable semantic action such as:

```text
Invoke
Toggle
Value
SelectionItem
RangeValue
ExpandCollapse
Scroll
```

AlinaCoder SHOULD prefer that action over mouse-coordinate simulation.

## 62. StableUIRef

A UI reference SHALL be re-resolvable against live state.

Potential identity signals:

```text
window HWND/process
AutomationId
RuntimeId
control type
accessible name
structural path
bounding rectangle
```

A stale UI object SHALL NOT be reused blindly after the interface changes.

## 63. Observe–Act–Verify loop

Every material UI interaction SHALL follow:

```text
observe live semantic state
→ select target
→ verify preconditions
→ act
→ observe again
→ verify concrete postcondition
```

Reporting that an invoke/click API returned success is not sufficient evidence that the intended UI state changed.

## 64. Vision fallback

Vision/OCR SHALL be used when semantic accessibility data is absent, incomplete or inconsistent.

Visual detections SHOULD be reconciled against semantic controls to avoid duplicate/conflicting targets.

## 65. Coordinate fallback

Coordinate actions SHALL include a confidence/provenance marker and SHOULD re-ground the target immediately before actuation.

## 66. DPIAndDisplayFingerprint

Desktop tests SHALL record relevant display state:

```text
DPI awareness mode
monitor topology
scaling factors
window bounds
resolution
session type
```

Coordinate-based assertions without DPI awareness SHALL be considered weak evidence.

## 67. DesktopSessionGuard

The runtime SHALL detect whether UI automation is attached to the intended interactive Windows session.

Session-0/non-interactive execution SHALL be explicit rather than silently producing empty windows or screenshots.

## 68. Background-first execution

Where semantic APIs allow it, desktop QA SHOULD avoid stealing the user's foreground input.

Foreground input SHALL be an explicit fallback for controls that require it.

## 69. IsolatedDesktopExecution

For destructive or interference-prone UI tests, AlinaCoder SHOULD support an isolated desktop/VM/test session when feasible.

The user’s active desktop SHALL not be assumed to be an uncontested test fixture.

## 70. AccessibilityContract

The product UI SHOULD expose stable accessible names, roles and automation identifiers for critical controls.

Accessibility metadata becomes both a user-quality requirement and an agent-testability contract.

## 71. UI visual regression

Semantic success SHALL NOT eliminate visual verification entirely.

For layout/rendering-sensitive changes, maintain visual snapshots/diffs with appropriate tolerance and stable environment controls.

---

# Part IX — Project, Tenant, Memory & Credential Isolation

## 72. ProjectScopeIdentity

Every active work context SHALL have a stable scope identity including:

```text
project_id
repo_host
repo_owner
repo_name
canonical_remote
workspace_root
source_tenant
sensitivity_class
```

## 73. ProjectMemoryNamespace

Every project-specific memory SHALL be namespaced at write time.

A memory without a known scope SHALL NOT automatically enter global recall.

## 74. Recall boundary

Default recall SHALL search:

```text
CURRENT_PROJECT_SCOPE
+ EXPLICIT_SHARED_SCOPE
```

It SHALL NOT search arbitrary other project scopes and rely on embedding rank to hide them.

## 75. CrossProjectPromotionGate

A lesson learned in one project MAY become shared only through an explicit promotion event.

Promotion SHALL record:

```text
source project
source evidence
generalized statement
applicable stack/library
counterexamples/limits
promotion reason
confidence
```

## 76. CrossTenantIsolationWall

Tenant isolation is a security boundary, not a relevance heuristic.

Cross-tenant memory recall SHALL be impossible by construction unless an explicitly governed shared tenant scope exists.

## 77. CrossTenantLeakProbe

The evaluation suite SHALL seed distinct secrets/facts into isolated scopes and prove they cannot be recalled from another tenant/project context.

Any leakage is a security failure.

## 78. RepoIdentityFence

Before mutations such as commit/push, AlinaCoder SHALL revalidate that the active workspace resolves to the intended repository identity.

Raw user/model-supplied remote URLs SHALL NOT bypass the resolved target policy.

## 79. CredentialNamespace

Credentials SHALL be scoped to the minimum repository/provider target that requires them.

A credential for repository A SHALL NOT be a fallback credential for repository B.

## 80. Credential exposure

Where implementation architecture permits, highly privileged credentials SHOULD remain outside the inherited environment visible to untrusted model-executed child processes.

## 81. Use-time credential resolution

Sensitive credentials SHOULD be resolved as close as practical to the trusted operation that needs them rather than loaded wholesale into long-lived model-visible process state.

## 82. PrePushTargetAssertion

Immediately before a push, trusted code SHALL verify that the resolved remote target still equals the intended repository.

Mismatch SHALL block the push.

---

# Part X — Performance & Resource Constitution

## 83. NonFunctionalContract

Functional correctness is insufficient if AlinaCoder becomes progressively unusable.

The spec SHALL treat key non-functional properties as executable contracts.

## 84. Baseline metrics

Track at minimum where measurable:

```text
cold_start_ms
warm_start_ms
time_to_usable_ui_ms
idle_ram_mb
peak_ram_mb
idle_cpu_percent
peak_cpu_percent
local_vram_mb
ui_action_latency_ms
recovery_latency_ms
local_model_load_ms
local_tokens_per_second
remote_ttft_ms
end_to_end_task_latency
build_latency
test_latency
context_compile_latency
```

Energy MAY be measured when sufficiently reliable instrumentation exists.

## 85. PerformanceTrajectory

Store metrics across released versions rather than comparing only the latest candidate to one baseline.

This exposes slow architectural creep.

## 86. Regression verdict

Noisy resource metrics SHALL use repeated samples and statistical or robust-distribution comparisons rather than one measurement.

Potential verdicts:

```text
PASS
REGRESSION
IMPROVEMENT
INCONCLUSIVE
ENVIRONMENT_DRIFT
```

## 87. Resource budget

Each metric MAY have:

```text
hard_limit
soft_budget
warning_slope
minimum_sample_count
environment_fingerprint
```

Hard-limit violations block promotion when the metric is trustworthy and safety/reliability relevant.

## 88. Environment normalization

Performance comparisons SHALL record relevant environment attributes such as:

```text
CPU
GPU
RAM
OS build
power mode
background load
model residency
network class
```

## 89. Efficiency dominance

Among equally correct candidates, AlinaCoder SHOULD prefer lower latency/resource complexity when the improvement is material and does not weaken resilience or maintainability.

## 90. Diminishing-return compute

Additional agentic reasoning, parallel rollouts or debate SHALL stop when expected quality gain no longer justifies latency/resource/quota cost under the active zero-spend constraints.

---

# Part XI — Optional Supabase Coordination Hardening

## 91. Supabase remains optional

Local state remains canonical for boot, recovery, safety decisions and offline operation.

Supabase MAY act as:

```text
optional mirror
remote coordination surface
telemetry/evidence store
queue transport
cross-device synchronization layer
```

It SHALL NOT be a mandatory authority for safe local startup.

## 92. Supabase maturity gate

Before a Supabase feature becomes trust-critical, AlinaCoder SHALL check its current feature maturity and changelog/docs.

Alpha or preview features SHOULD NOT become sole canonical safety substrates without an explicit exception and local fallback.

## 93. RLS by construction

Every exposed table containing scoped AlinaCoder data SHALL use Row Level Security with explicit policies.

`TO authenticated` alone is not authorization.

Ownership/project/tenant predicates SHALL be explicit.

## 94. Service-role prohibition in clients

`service_role`, secret keys or equivalent RLS-bypass credentials SHALL NOT be exposed to the desktop client or model-visible public surfaces.

## 95. Realtime channels

Production Realtime channels SHOULD be private and authorized when carrying scoped project information.

Topic names SHOULD encode a scope identity.

## 96. Realtime non-authority

Realtime delivery SHALL be treated as notification/coordination, not durable canonical state.

Lost WebSocket messages SHALL be recoverable from durable state.

## 97. Queue semantics

If PGMQ or equivalent queues are used, durable workers SHOULD prefer visibility-timeout read/ack semantics over destructive pop when processing must survive worker failure.

## 98. QueueMessageContract

Minimum fields:

```text
message_id
project_scope
task_id
effect_id
idempotency_key
state_version
payload_digest
enqueued_at
attempt_count
```

## 99. Queue idempotency

Queue delivery semantics do not remove the need for application-level idempotency.

Repeated delivery SHALL be safe or reconciled.

## 100. Queue health

Track:

```text
queue_length
oldest_message_age
newest_message_age
read_count_distribution
dead_letter/quarantine count
processing_latency
```

## 101. RLS testing

Database authorization tests SHALL include negative cross-project and cross-tenant cases, not only happy-path reads.

## 102. Supabase degradation

If optional Supabase connectivity fails, local work MAY continue when all required local safety guarantees remain satisfied.

The UI SHALL expose synchronization degradation without treating it as local-state corruption.

---

# Part XII — Unified Trust Receipts

## 103. TrustReceipt

Critical state transitions SHOULD emit a compact immutable `TrustReceipt` linking the evidence that justified them.

Examples:

```text
RELEASE_ADMISSION
UPDATE_PROMOTION
RECOVERY_RESUME
MCP_SERVER_ADMISSION
SKILL_ADMISSION
PROJECT_SCOPE_BINDING
STOCHASTIC_BENCHMARK_VERDICT
DESKTOP_UI_VERIFICATION
PERFORMANCE_PROMOTION
```

## 104. Common receipt fields

```text
receipt_id
type
subject_id
state_before
state_after
policy_version
evidence_refs[]
verifier_versions[]
created_at
result
```

## 105. No self-authored proof shortcut

An LLM statement that an operation is safe or successful SHALL NOT itself satisfy a receipt's deterministic evidence requirement.

---

# Part XIII — Acceptance & Adversarial Evaluation

## 106. Release provenance acceptance

The evaluation suite SHALL include at minimum:

1. Valid release manifest + correct binary hash → admitted.
2. One-byte binary modification after signing → rejected.
3. Provenance from wrong repository → rejected.
4. Provenance from unexpected builder identity → rejected.
5. Valid old release below security floor → rejected.
6. Expired/frozen update metadata → rejected.
7. Downloaded candidate fails launch smoke → previous active version restored.
8. Candidate requires unsupported state schema → blocked before activation.
9. Missing SBOM does not masquerade as present.
10. Rebuild dependency drift is surfaced explicitly.

## 107. Durable recovery acceptance

11. Crash after durable intent but before effect → safe retry/reconciliation.
12. Crash after effect but before ACK → no duplicate effect.
13. Lost push response after remote push → recovery detects remote state before retry.
14. Crash mid-update → last-known-good remains recoverable.
15. Machine reboot during a long task → task resumes from durable boundary, not raw stale model context.
16. Ambiguous irreversible effect → quarantined rather than guessed.
17. Orphan process belongs to another task/user → not killed by name-only cleanup.

## 108. Stochastic verification acceptance

18. One lucky successful rollout after many failures → not classified stable PASS.
19. One isolated failure in a historically stable stochastic scenario → may become INCONCLUSIVE rather than immediate regression.
20. Multi-rollout estimator uses independent runs, not unit-test count.
21. Sequential sampler stops early when evidence is decisive.
22. All retry outcomes remain visible in evidence.
23. Known flaky deterministic test cannot become green by retry laundering.
24. Behavioral fingerprint detects a major trajectory shift despite unchanged terminal pass rate.

## 109. MCP/skill acceptance

25. MCP tool schema changes after discovery → stale prepared call rejected.
26. MCP server silently adds privileged tool → capability expansion quarantined.
27. Server identity changes behind same friendly name → re-admission required.
28. Malformed tool output → cannot satisfy a deterministic state transition.
29. Untrusted MCP content attempts prompt injection → remains tainted and non-authoritative.
30. Malicious skill creates derived skill → descendant retains taint until independent validation.
31. Hook broadens permissions without declared capability delta → blocked.

## 110. Desktop acceptance

32. Critical button moves on screen but retains AutomationId → semantic action still succeeds.
33. UIA tree stale after navigation → ref is re-resolved before action.
34. UIA unavailable for custom canvas → vision fallback activates explicitly.
35. DPI scaling changes → coordinate-only baseline is not trusted blindly.
36. UI action API reports success but postcondition absent → operation fails verification.
37. Process runs in wrong Windows session → desktop test blocks with explicit session error.
38. Background semantic operation available → physical user cursor is not stolen.

## 111. Isolation acceptance

39. Memory written in project A cannot be retrieved in project B unless promoted shared.
40. Tenant A seeded secret cannot surface in tenant B recall.
41. Shared library lesson can be explicitly promoted and then retrieved cross-project with source attribution.
42. Repository remote changes between plan and push → push blocked.
43. Credential for repo A cannot fallback to repo B.

## 112. Resource/Supabase acceptance

44. Functional tests pass but idle RAM doubles beyond hard contract → release blocked/inconclusive according to calibrated gate.
45. Noisy memory measurement produces overlapping confidence interval → INCONCLUSIVE, not fabricated certainty.
46. Optional Supabase outage → local canonical state still boots/recoverable.
47. Cross-project RLS read attempt → denied.
48. Queue message redelivered after visibility timeout → idempotent processing prevents duplicate durable effect.
49. Realtime notification lost → durable state reconciliation restores correctness.
50. Supabase feature maturity changes in current docs → trust-critical eligibility is re-evaluated.

---

# Part XIV — Conceptual Module Map

## 113. New conceptual modules

```text
src/alinacoder/release_trust/
    artifact_identity.py
    release_manifest.py
    provenance_verifier.py
    artifact_signature.py
    runtime_artifact_verifier.py
    secure_update.py
    update_trust_root.py
    rollback_policy.py
    reproducible_build.py
    sbom_policy.py

src/alinacoder/durability/
    execution_journal.py
    effect_record.py
    idempotency.py
    recovery_reconciler.py
    boot_recovery_fsm.py
    orphan_process.py
    crash_injection.py

src/alinacoder/evaluation/
    stochastic_evidence.py
    sequential_test.py
    reliability.py
    behavioral_fingerprint.py
    flake_registry.py
    resource_regression.py

src/alinacoder/extensions/
    mcp_compatibility.py
    tool_manifest_fingerprint.py
    mcp_drift_gate.py
    capability_projection.py
    mcp_taint.py
    skill_identity.py
    skill_lineage.py
    hook_integrity.py

src/alinacoder/desktop/
    semantic_oracle.py
    stable_ui_ref.py
    hybrid_perception.py
    desktop_session_guard.py
    post_action_verifier.py
    visual_regression.py

src/alinacoder/isolation/
    project_scope.py
    memory_namespace.py
    promotion_gate.py
    tenant_wall.py
    repo_identity_fence.py
    credential_namespace.py

src/alinacoder/performance/
    nonfunctional_contract.py
    performance_trajectory.py
    environment_fingerprint.py
    resource_budget.py

src/alinacoder/optional_supabase/
    maturity_gate.py
    scoped_mirror.py
    realtime_coordination.py
    durable_queue.py
    queue_health.py
```

These are conceptual boundaries, not a mandate to create all files immediately. Implementation MAY consolidate modules when cohesion remains strong and contracts stay independently testable.

---

# Part XV — Canonical Operational Loops

## 114. Trusted release loop

```text
source main
→ verified source state
→ pinned build inputs
→ build
→ SBOM
→ provenance
→ artifact digest/signature
→ release manifest
→ update metadata
→ candidate download
→ runtime verification
→ compatibility check
→ canary
→ atomic activation
→ post-launch smoke
→ ACTIVE or rollback
```

## 115. Durable task loop

```text
IntentContract
→ task/stage checkpoint
→ before external mutation: durable intent
→ perform effect
→ observe reality
→ persist observation
→ durable ACK
→ verifier evidence
→ next boundary
```

On crash:

```text
restart
→ BootRecoveryFSM
→ inspect incomplete effects
→ reconcile reality
→ restore canonical state
→ resume from verified boundary
```

## 116. MCP/skill admission loop

```text
discover extension
→ identify origin/version
→ hash manifest/content
→ protocol/capability check
→ permission delta
→ canary
→ trust classification
→ minimum capability projection
→ eligible
```

On drift:

```text
manifest/content changed
→ invalidate old generation lease
→ classify drift
→ re-canary if needed
→ re-admit or quarantine
```

## 117. Desktop verification loop

```text
launch actual Windows artifact
→ identify target session/window
→ read semantic UI tree
→ resolve stable control
→ verify precondition
→ semantic action
→ re-observe
→ verify postcondition
→ visual check if layout-sensitive
→ receipt
```

## 118. Performance promotion loop

```text
candidate
→ fixed environment profile
→ repeated measurements
→ compare against trajectory/budget
→ PASS / REGRESSION / INCONCLUSIVE / ENVIRONMENT_DRIFT
→ promotion decision
```

---

# Part XVI — Non-Negotiable Invariants

## 119. Release invariants

- No binary is trusted solely because its filename/version string looks correct.
- No downloaded update is launched before artifact verification.
- No stale but valid release bypasses an explicit security floor.
- No model may redefine update trust roots during ordinary work.
- No autonomous paid upgrade/signing purchase is allowed.

## 120. Durability invariants

- No ambiguous external side effect is blindly replayed.
- No retry erases earlier evidence.
- No raw stale conversation state outranks durable canonical state after recovery.
- No push retry occurs without rechecking repository/remote state.

## 121. Verification invariants

- No stochastic capability is declared stable from one lucky run.
- No deterministic flake is hidden by retry-until-green behavior.
- No unit-test count is treated as independent rollout count.
- `INCONCLUSIVE` is a valid and required outcome when evidence is insufficient.

## 122. Extension invariants

- No stale MCP schema remains authoritative after manifest drift.
- No new privileged capability is silently accepted.
- No skill loses taint merely because another model rewrote it.
- No hook becomes a privilege-escalation shortcut.

## 123. Desktop invariants

- No coordinate click is preferred over a reliable semantic control action.
- No UI action is accepted without checking the intended postcondition.
- No empty UI tree from the wrong Windows session is interpreted as application absence without session diagnosis.

## 124. Isolation invariants

- No project memory crosses scopes accidentally.
- No tenant boundary is implemented only as vector-ranking preference.
- No repository credential falls back across repository identities.
- No push occurs after a target mismatch.

## 125. Resource invariants

- Functional correctness does not waive hard resource budgets.
- Noisy metrics do not justify fabricated precision.
- Increased intelligence compute must remain bounded by diminishing-return controls.

## 126. Supabase invariants

- Supabase is optional, never the sole local recovery authority.
- Exposed scoped tables use RLS.
- RLS-bypass secrets never live in the desktop/public client.
- Queue redelivery remains application-idempotent.
- Realtime is not durable truth.
- Current docs/changelog govern feature eligibility, not stale assumptions.

---

# Part XVII — Operational Definition of Done

## 127. Release-level Done Contract

A future production release of `AlinaCoder.exe` SHALL NOT be called operationally complete until applicable evidence demonstrates:

```text
source identity known
artifact digest known
build provenance recorded
release manifest valid
signature policy satisfied
state-schema compatibility proven
update/rollback path exercised
crash recovery exercised
MCP/skill drift handling exercised
Windows semantic UI smoke exercised
project isolation probes pass
performance budgets pass or are explicitly inconclusive
zero autonomous monetary spend preserved
```

## 128. Product-level target behavior

The intended user experience remains simple:

```text
Open AlinaCoder.exe
→ AlinaCoder proves it is an admitted build
→ recovers unfinished durable work if needed
→ binds to the correct project
→ selects eligible zero-cost intelligence
→ uses only current trusted tool/skill generations
→ works autonomously
→ verifies code and the real desktop product
→ survives crashes/reboots without duplicate side effects
→ updates itself only through verified artifacts
→ remains fast and resource-bounded over time
```

The complexity belongs inside the system, not in the user's daily workflow.

## 129. Final strengthening

The v0.2 objective is strengthened from “an autonomous coding agent that can improve itself” to:

> **a self-improving coding system whose source, binary, updates, side effects, tests, extension surfaces, desktop actions, memories, credentials and resource trajectory remain independently governable and auditable across time.**

This amendment is normative for future implementation planning.