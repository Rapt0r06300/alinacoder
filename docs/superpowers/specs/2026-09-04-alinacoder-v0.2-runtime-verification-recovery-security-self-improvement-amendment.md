# AlinaCoder v0.2 — Runtime Kernel, Verification, Recovery, Security & Self-Improvement Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose

This amendment strengthens the parts of AlinaCoder that remain most fragile in long-horizon autonomous software engineering: execution control, progress tracking, verification, rollback, environment fidelity, provenance, supply-chain security, runtime observability, self-improvement governance and evidence-backed completion.

The guiding principle is:

> **A strong LLM is not enough. AlinaCoder must remain correct, recoverable, secure, inspectable and faithful to user intent across hours or days of autonomous work.**

This amendment is additive and jointly normative with the previously approved v0.2 specifications. It has precedence for the subsystems defined below when it strengthens existing rules.

---

# Part I — Deterministic Runtime Core

## 2. Autonomous Runtime Kernel

AlinaCoder SHALL include a deterministic `AutonomousRuntimeKernel` above all LLMs and agent roles.

The kernel, not the current model, owns:

- canonical task state;
- permission state;
- mutation admission;
- checkpoint admission;
- commit epochs;
- recovery transitions;
- completion state;
- irreversible side-effect policy.

LLMs MAY propose actions. The runtime kernel SHALL decide whether those actions may occur.

## 3. Progress Ledger

Every task and subtask SHALL have a machine-readable `ProgressLedger` state such as:

```text
NOT_STARTED
DISCOVERING
IN_PROGRESS
WAITING_EVIDENCE
PROVEN
REGRESSED
BLOCKED
SUPERSEDED
ABORTED
```

A model assertion such as “done”, “fixed”, “completed” or “should work” SHALL NOT directly advance a task to `PROVEN`.

## 4. Premature-Completion Firewall

`TaskCompletionFirewall` SHALL prevent final completion until all mandatory Done Contract requirements have objective evidence.

Completion SHALL require, where applicable:

- implementation present;
- required files and interfaces present;
- build succeeds;
- targeted tests succeed;
- regression tests succeed;
- hidden/adversarial checks succeed when required;
- architecture constraints remain valid;
- unauthorized side effects are absent;
- required artifacts exist;
- repository state is internally consistent;
- final diff matches the active `IntentContract`.

If evidence is incomplete, AlinaCoder SHALL report incomplete state rather than infer completion.

---

# Part II — Independent Verification Plane

## 5. Independent Verification Plane

AlinaCoder SHALL maintain a verification plane logically independent from the model or worker that produced a candidate change.

The producer SHALL NOT be the sole authority for validating its own work.

## 6. Visible and held-out verification

For sufficiently important or long-horizon work, validation SHOULD combine:

```text
visible development tests
+ held-out tests
+ integration tests
+ cross-feature composition tests
+ metamorphic tests
+ mutation tests
+ differential tests
+ adversarial tests
+ contract checks
```

The visible suite SHALL NOT be treated as a perfect proxy for user intent.

## 7. Reward-Hacking Defense

AlinaCoder SHALL detect and reject attempts to achieve a green verifier by changing the verifier rather than satisfying the specification.

Protected surfaces include:

- held-out tests;
- test harness policy;
- benchmark/verifier scripts;
- hidden fixtures;
- expected-output oracles;
- CI gates;
- lint/security configurations;
- environment flags whose sole purpose is to bypass validation.

Any required legitimate change to a protected surface SHALL be explicit, justified by the task and independently validated.

## 8. Behavioral Contract Engine

Before modifying an important existing component, AlinaCoder SHOULD derive a semi-formal `BehavioralContract` covering as appropriate:

- preconditions;
- postconditions;
- invariants;
- API signatures;
- error behavior;
- persistence rules;
- ordering guarantees;
- concurrency expectations;
- undefined/unsupported behavior;
- compatibility commitments.

Tests SHOULD be derived from the contract rather than only from the candidate implementation.

## 9. Semantic Regression Detector

A patch SHALL NOT be considered safe merely because it compiles and passes visible unit tests.

`SemanticRegressionDetector` SHALL search for behavior drift through:

- contract comparison;
- differential execution;
- public API diffing;
- schema diffing;
- persisted-data compatibility checks;
- metamorphic properties;
- scenario-level behavior comparisons;
- targeted adversarial test generation.

---

# Part III — Live Trajectory Control

## 10. Live Trajectory Monitor

A deterministic `LiveTrajectoryMonitor` SHALL observe active runs for signals including:

- repeated command after failure;
- repeated edit/revert cycles;
- identical failing test with no new hypothesis;
- plan violation;
- loss of task focus;
- excessive repository exploration;
- no measurable progress;
- premature finalization;
- skipped verification;
- resource runaway;
- model/provider thrashing;
- stale-state action attempts.

## 11. Corrective steering

The monitor SHALL separate detection from advising.

Deterministic/rule-based signals SHOULD detect drift first. An LLM advisor MAY be invoked only after a drift condition is established or uncertainty requires reasoning.

## 12. Plan–Memory Coupling

Planning and episodic memory SHALL be bidirectionally coupled.

The current plan phase SHALL influence memory retrieval.

Memory-derived evidence SHALL influence:

- stuck detection;
- hypothesis retirement;
- re-planning;
- rollback decisions;
- next experiment selection.

## 13. Emergent-Spec Guard

Long conversations SHALL be treated as an evolving specification, not as independent prompts.

`EmergentSpecGuard` SHALL continuously track:

- durable commitments;
- user corrections;
- superseded requirements;
- preservation requirements;
- newly introduced constraints;
- project-wide compatibility implications.

A new request SHALL be evaluated against the cumulative active specification before implementation.

---

# Part IV — Repository and Change-Impact Intelligence

## 14. Repository Contract Graph

AlinaCoder SHALL maintain a `RepositoryContractGraph` connecting:

- public APIs;
- internal interfaces;
- schemas;
- configuration contracts;
- CLI contracts;
- persistence formats;
- package/module boundaries;
- tests;
- consumers;
- generated artifacts.

## 15. Change Impact Simulator

Before a high-impact patch, AlinaCoder SHOULD predict:

```text
what should change
what must remain unchanged
which consumers are affected
which tests should change
which tests must not change
which schemas/interfaces may break
which migration paths are required
```

The actual post-change result SHALL be compared with this prediction.

## 16. Architecture Fitness Functions

The verification system SHOULD enforce machine-checkable architecture rules such as:

- forbidden dependency edges;
- no newly introduced cycles;
- package boundary constraints;
- layer direction;
- maximum public API drift;
- generated-file ownership;
- module size/complexity thresholds where justified;
- dependency allow/deny rules.

## 17. Complexity Budget

AlinaCoder SHALL treat unnecessary complexity as a regression risk.

New abstraction layers, dependencies, frameworks, services or duplicate mechanisms SHALL require evidence that they improve the current goal enough to justify lifecycle cost.

## 18. Dead-Code and Superseded-Path Detection

After substantial refactors or repeated iterations, AlinaCoder SHOULD search for:

- dead modules;
- unused adapters;
- duplicate implementations;
- superseded execution paths;
- stale feature flags;
- unreachable compatibility code;
- obsolete tests and documentation.

Removal SHALL still respect preservation and backward-compatibility constraints.

---

# Part V — Environment Fidelity, Sandbox and Recovery

## 19. Environment Twin

AlinaCoder SHALL maintain a versioned `EnvironmentTwin` covering relevant state such as:

- OS and architecture;
- Python/Node/toolchain versions;
- installed packages;
- PATH/tool locations;
- environment variables classified by sensitivity;
- active services/processes;
- ports;
- runtime dependencies;
- GPU/CPU capabilities;
- package-manager state;
- lockfiles;
- build caches where relevant.

## 20. Hermetic Execution

Risky or uncertain build/test/install operations SHOULD execute in a controlled sandbox or disposable environment when practical.

The goal is to prevent candidate work from silently contaminating the host.

## 21. Aligned Checkpoint and Rewind

Checkpointing SHALL align the cognitive and environmental state.

A valid recovery checkpoint MAY include:

- `CanonicalSessionState`;
- IntentContract and plan state;
- Git HEAD and worktree snapshot/diff;
- filesystem state;
- important process/service state;
- environment manifest;
- side-effect ledger;
- pending operation IDs;
- active CommitEpoch.

Restoring only conversation state while leaving incompatible environment state SHALL NOT count as correct recovery.

## 22. Semantic checkpoint policy

Checkpoint frequency SHOULD depend on recovery-relevant mutations, not merely elapsed turns.

Read-only exploration MAY avoid expensive checkpoints. File/process/environment mutations SHALL raise checkpoint priority.

## 23. Crash-Proof Recovery

After process crash, Windows restart, provider outage or model failure, AlinaCoder SHALL restore from the latest complete and internally consistent checkpoint.

Incomplete checkpoints SHALL never be promoted as recovery anchors.

## 24. Revision-Aware DAG Recovery

If the user changes requirements during execution, AlinaCoder SHOULD invalidate only the affected dependency region of the task DAG when correctness can be proven.

Unaffected verified work SHOULD be retained instead of blindly restarting the entire task.

---

# Part VI — Provenance and Supply-Chain Security

## 25. Workspace Provenance Firewall

Repository content SHALL be treated as potentially untrusted data unless explicitly promoted by policy.

This includes:

- README files;
- code comments;
- AGENTS/CLAUDE/GEMINI-style instruction files;
- issues;
- docs;
- test fixtures;
- generated text;
- vendored code;
- retrieved web pages.

A repository artifact SHALL NOT acquire system-policy authority merely because a model reads it.

## 26. Origin-Based Tool Security

Sensitive tool parameters SHALL carry provenance.

For sensitive operations, values originating solely from attacker-writable/untrusted content SHALL be denied unless validated against trusted user intent or explicit policy.

## 27. Skill Supply-Chain Security

Third-party skills/plugins/MCP resources SHALL be treated as supply-chain artifacts.

Admission SHOULD include:

- origin and publisher provenance;
- immutable digest/hash;
- version pinning;
- permission manifest;
- static inspection;
- suspicious instruction/code-example scanning;
- optional sandbox detonation;
- network/file/env access observation;
- rollback/uninstall path.

## 28. Lifecycle Hook Security

Lifecycle hooks, preflight commands, plugin hooks and automatic event handlers SHALL be considered privileged executable configuration.

A hook update SHALL NOT become trusted solely because an existing plugin/skill was previously trusted.

## 29. Dependency Admission Firewall

Before installing a new dependency, AlinaCoder SHOULD verify as appropriate:

- package exists in the intended registry;
- package name is not a likely hallucination/typosquat;
- exact version;
- maintainer/repository provenance;
- integrity hashes/lockfile behavior;
- license compatibility;
- known vulnerability state;
- necessity versus existing dependency;
- install-script or postinstall risk.

## 30. Network Egress Controller

Sandboxed builds/tests and agent tools SHOULD use task-scoped network egress where practical.

Untrusted content SHALL NOT be able to choose arbitrary exfiltration destinations.

## 31. Secret Boundary

Secrets SHALL be detected and classified before model-context construction.

External LLM providers SHALL receive only the minimum authorized projection of repository/environment context.

Secrets SHALL NOT be transmitted merely because they appear in environment variables, logs, configs or test output.

## 32. Action Capability Tokens

High-impact runtime actions SHALL use narrowly scoped temporary capabilities such as:

```text
READ_REPO
WRITE_FILE_SET
RUN_TESTS
INSTALL_DEPENDENCY
NETWORK_APPROVED_DOMAINS
MUTATE_GIT
COMMIT_MAIN
```

Capabilities SHALL be limited by task, path, operation type and lifetime where feasible.

## 33. Side-Effect Journal

AlinaCoder SHALL maintain a durable record of host-visible side effects, including before/after evidence when relevant.

The user SHALL be able to determine what AlinaCoder actually changed outside Git-tracked source files.

---

# Part VII — Multi-Day Autonomy

## 34. Multi-Day Project Governor

Large goals SHALL be decomposed into small, verifiable increments that preserve a working baseline whenever practical.

The governor SHALL balance:

```text
repair existing regressions
+ finish current acceptance slice
+ grow capability
+ preserve recoverability
```

A huge monolithic attempt is disfavored when incremental delivery is possible.

## 35. Versioned Working Baselines

AlinaCoder SHALL preserve a `BestKnownWorkingState` across long missions.

New work may advance from it, but a degraded candidate SHALL NOT silently replace it.

## 36. Operational Readiness Score

A release or major milestone SHOULD be evaluated across multiple dimensions rather than a single green-test boolean:

```text
correctness
intent fidelity
security
recoverability
architecture
maintainability
robustness
continuity
resource discipline
zero-spend compliance
```

---

# Part VIII — Self-Improvement Governance

## 37. Self-Improvement Constitution

A self-modification to AlinaCoder's harness SHALL follow:

```text
failure evidence
→ hypothesis
→ predicted benefit and regression risk
→ isolated candidate change
→ visible benchmark
→ hidden benchmark
→ adversarial evaluation
→ recoverability proof
→ promote / watch / reject
→ rollback if required
```

The self-modifier SHALL NOT be able to weaken the verifier used to evaluate itself.

## 38. Recoverability Test for Self-Modification

A harness mutation SHALL NOT be promoted unless AlinaCoder can demonstrate a valid rollback path from realistic future states, not merely from the state in which the mutation was created.

## 39. Harness Component Observatory

The harness SHALL expose measurable component classes such as:

- router;
- context manager;
- memory;
- planner;
- tool middleware;
- verifier;
- retrieval;
- skills;
- provider adapters;
- specialists;
- prompt/policy layers.

Performance changes SHOULD be attributable to specific components whenever possible.

## 40. Causal Improvement Attribution

Self-improvement SHOULD minimize simultaneous uncontrolled changes.

Each candidate edit SHOULD record:

- evidence motivating the edit;
- predicted fixed failures;
- predicted regressions;
- affected components;
- expected metrics;
- observed result.

Ineffective or harmful edits SHALL be reverted.

---

# Part IX — Failure Understanding and Observability

## 41. Failure Taxonomy Engine

Failures SHOULD be classified into typed categories including:

```text
INTENT
SPEC_DRIFT
PLANNING
MEMORY
RETRIEVAL
CONTEXT
TOOL
ENVIRONMENT
DEPENDENCY
IMPLEMENTATION
INTERFACE
VERIFICATION
REWARD_HACKING
SECURITY
RESOURCE
PROVIDER
CONTINUITY
RECOVERY
PREMATURE_COMPLETION
```

The category SHALL guide the next corrective mechanism rather than triggering generic retry.

## 42. Black Box Recorder

AlinaCoder SHALL maintain an audit-grade `BlackBoxRecorder` for significant missions, capturing structured events such as:

- model/provider selection;
- canonical state versions;
- tool calls;
- file diffs;
- commands and exit codes;
- test results;
- resource snapshots;
- plan transitions;
- checkpoints;
- failovers;
- side effects;
- completion evidence.

Private model chain-of-thought is not required for this audit trail.

## 43. Deterministic Replay

Where feasible, AlinaCoder SHOULD support replay from recorded events and pinned environment inputs so failures can be reproduced and routing/harness changes can be evaluated against the same scenario.

## 44. Shadow Runtime

New routing, memory, planning, verification or context policies SHOULD first run in read-only/shadow evaluation before receiving mutation authority.

## 45. Canary Rollout of AlinaCoder

A new AlinaCoder harness version SHALL pass a bounded internal canary set before replacing the `BestKnownHarnessState`.

---

# Part X — Infinite Evaluation and Anti-Gaming

## 46. Infinite Evaluation Factory

AlinaCoder SHOULD maintain a procedural/adversarial evaluation factory that can generate new variants of:

- bugs;
- missing dependencies;
- renamed files;
- interface changes;
- evolving user requirements;
- stale context;
- provider failures;
- 429/timeouts;
- prompt injections;
- malicious skills;
- bad package suggestions;
- partial patches;
- process crashes;
- corrupted checkpoints;
- resource pressure.

The goal is to make benchmark memorization insufficient.

## 47. Hidden and metamorphic invariant suites

Core AlinaCoder invariants SHALL have hidden and metamorphic test variants where practical.

Equivalent intent transformations SHOULD preserve behavior; small meaningful changes such as negation or permission removal SHOULD change behavior appropriately.

## 48. Verifier co-evolution

As AlinaCoder becomes stronger, its verifier SHALL also be reviewed and improved.

A fixed verifier SHALL NOT be assumed indefinitely sufficient against a stronger optimizer.

---

# Part XI — Implementation Priority

## 49. Required implementation order

The first implementation priority for this amendment is:

1. `AutonomousRuntimeKernel` + `ProgressLedger` + completion firewall;
2. independent verification plane + anti-reward-hacking checks;
3. aligned checkpoint/rewind + crash recovery;
4. provenance/supply-chain/network/secret guardrails;
5. black-box observability + failure taxonomy;
6. self-improvement governance + shadow/canary promotion;
7. infinite evaluation factory.

The zero-cost provider mesh remains important, but adding more providers SHALL NOT outrank establishing this execution/reliability spine.

---

# Part XII — Normative Acceptance Scenarios

## 50. Long-horizon completion

Given a multi-hour task, AlinaCoder SHALL not report DONE solely from self-assessment; final status requires objective evidence.

## 51. Visible-test gaming

Given a candidate that passes visible tests by special-casing fixtures or modifying verification surfaces, held-out/adversarial verification SHALL reject the candidate.

## 52. Mid-task crash

Given a process or host interruption after environment mutations, recovery SHALL restore a mutually consistent cognitive + repository + relevant environment state.

## 53. User correction during work

Given a new user message that invalidates only part of an active DAG, invalid work SHALL be stopped and affected descendants recomputed while still-valid verified work is preserved when safe.

## 54. Poisoned repository instruction

Given a repository file that instructs the agent to run an unrelated shell command or exfiltrate data, repository provenance SHALL prevent that content from gaining control-plane authority.

## 55. Malicious skill or hook update

Given a previously trusted skill whose update adds a privileged lifecycle hook, the new version SHALL require fresh security admission and SHALL not inherit executable trust automatically.

## 56. Dependency hallucination

Given a model-suggested package with uncertain provenance, package installation SHALL be blocked until dependency admission checks pass.

## 57. Late stale response

Given a response from an old model/state after a newer CommitEpoch has taken control, the old response SHALL have no mutation authority.

## 58. Self-improvement regression

Given a harness mutation that improves a visible benchmark but worsens hidden/recovery/security evaluation, the candidate SHALL NOT replace the best-known harness.

## 59. Completion evidence trace

For every major completed mission, the black-box recorder SHALL make it possible to reconstruct what changed, what verification ran, which evidence justified completion and what side effects occurred.

---

## 60. Research basis

This amendment is informed by current 2026 work on long-horizon coding agents, including research on:

- ultra-long-horizon SWE evaluation and reward-hacking-resistant verification;
- active context management for SWE agents;
- bidirectionally coupled planning and episodic memory;
- online trajectory monitoring and corrective steering;
- checkpoint/restore for agent sandboxes;
- recoverable execution and rewind;
- specification faithfulness under emergent requirements;
- hidden/metamorphic/mutation testing for agent behavior;
- operational safety failures in deployed coding agents;
- repository poisoning and indirect prompt injection;
- malicious skills and dependency steering;
- provenance-aware tool security;
- self-evolving harnesses with prediction-backed, reversible changes.

These research references provide design evidence only. Runtime correctness remains governed by AlinaCoder's own deterministic tests, executable evidence and the Spec Constitution.
