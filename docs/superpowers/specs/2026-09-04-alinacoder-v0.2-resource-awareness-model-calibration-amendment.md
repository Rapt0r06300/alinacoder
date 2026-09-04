# AlinaCoder v0.2 — Resource Awareness, Real Machine Model Calibration and Reliability-First Execution Amendment

Date: 2026-09-04  
Status: Approved normative amendment to AlinaCoder v0.2  
Repository: `Rapt0r06300/alinacoder`  
Canonical development branch: `main` only  
Extends:
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-conversation-and-external-self-improvement-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-research-voice-context-specialists-amendment.md`

## 1. Normative status

This document is an official extension of the AlinaCoder v0.2 specification. It strengthens machine-awareness, model selection, resource control, reliability calibration, weak-model adaptation and task decomposition without weakening any existing v0.2 invariant.

The following invariants remain mandatory:

1. Full autonomy is retained.
2. Canonical Git development remains direct to `main`.
3. Ollama remains the local model provider.
4. Windows-first and Python 3.12+ remain the primary implementation target.
5. Deterministic execution evidence outranks model claims.
6. Safety, regression and evaluator-integrity floors cannot be traded away for speed or apparent intelligence.
7. Checkpoint, rollback, resume, BestKnownState and external self-improvement remain mandatory.
8. Specialist-agent activation, when supported, remains conditional and measured.
9. Reliability and verifiability take precedence over maximal task breadth.

This amendment introduces five mandatory capabilities:

- automatic machine resource discovery and continuous adaptation;
- a global resource controller for CPU, GPU, RAM, wall-clock time and context budgets;
- model selection based on real mini-tests executed on the target machine rather than VRAM heuristics alone;
- explicit weak-model strategy adaptation;
- calibrated uncertainty, including the ability to say that a task is not currently reliable enough and to replace it with a simpler or more verifiable decomposition.

---

## 2. Core reliability principle

AlinaCoder must optimize for the **most reliable solution the current machine and model can prove**, not for the largest or most ambitious solution it can attempt.

The default priority order is:

```text
Safety
→ Correctness
→ Verifiability
→ Regression resistance
→ Architectural fit
→ Machine compatibility
→ Simplicity
→ Efficiency
→ Breadth / ambition
```

A smaller solution that can be strongly verified is preferred over a larger solution whose correctness cannot be established confidently on the current hardware/model.

---

## 3. Machine Resource Discovery

At startup and when resource conditions materially change, AlinaCoder must build a `MachineProfile` from actual local observations.

Representative fields:

```text
MachineProfile
- os_version
- cpu_model
- physical_cores
- logical_cores
- cpu_frequency_if_available
- total_ram
- available_ram
- pagefile_state
- gpu_devices[]
- gpu_vendor
- gpu_model
- gpu_vram_total
- gpu_vram_free
- gpu_compute_capability_if_available
- active_gpu_load
- active_cpu_load
- storage_free_space
- storage_type_if_available
- ollama_version
- installed_models[]
- model_digests[]
- power_mode
- thermal_signals_if_available
- current_resource_pressure
- discovery_timestamp
```

Discovery should use native, deterministic local mechanisms where possible, such as Windows APIs, PowerShell/CIM, Ollama metadata and vendor tools already present on the machine.

Missing telemetry is represented explicitly as `UNKNOWN`; it must not be fabricated.

---

## 4. Dynamic Resource Awareness

Resource detection is not a one-time install check.

AlinaCoder must periodically observe whether the machine state has changed enough to require adaptation, including:

- free RAM drops significantly;
- another GPU workload starts;
- VRAM pressure increases;
- sustained CPU saturation appears;
- thermal throttling is detected where observable;
- available disk space becomes unsafe;
- Ollama model availability changes;
- model latency changes materially;
- context length creates paging or severe slowdown.

A material change triggers `resource.profile_changed` and may cause:

- model reselection;
- context reduction;
- lower concurrency;
- delayed noncritical indexing;
- smaller specialist-agent fan-out;
- task decomposition;
- test scheduling adaptation;
- safe suspension of expensive background work.

---

## 5. Global Resource Controller

Add a deterministic `ResourceController` as a first-class runtime component.

Suggested conceptual architecture:

```text
src/alinacoder/
├─ resources/
│  ├─ discovery.py
│  ├─ controller.py
│  ├─ budgets.py
│  ├─ pressure.py
│  ├─ scheduler.py
│  └─ telemetry.py
├─ providers/
│  ├─ ollama.py
│  ├─ model_probe.py
│  └─ model_selector.py
├─ intelligence/
│  ├─ reliability.py
│  ├─ task_decomposer.py
│  └─ capability_policy.py
└─ ...
```

The controller enforces at least five independent budgets.

### 5.1 CPU budget

Configurable ceilings for:

- average CPU utilization attributable to AlinaCoder;
- maximum concurrent subprocesses;
- indexing/parser workers;
- test parallelism;
- background research/indexing concurrency.

The target is not a brittle exact percentage but a bounded policy with pressure-aware backoff.

### 5.2 GPU budget

Control:

- maximum model concurrency;
- model residency strategy;
- context size based on observed VRAM use;
- specialist-agent parallelism;
- fallback to sequential reasoning under pressure;
- optional unloading/switching of models when required.

### 5.3 RAM budget

Control:

- repository index size;
- context caches;
- retained model outputs;
- concurrent test/build processes;
- memory-map or on-disk fallback for large indexes;
- SQLite/cache compaction.

AlinaCoder must preserve an OS safety margin rather than consuming all available memory.

### 5.4 Wall-clock/time budget

Every mission, task, benchmark, tool call and specialist session may have a bounded time budget.

The controller distinguishes:

- user-facing latency budget;
- task-level execution budget;
- verification budget;
- self-improvement benchmark budget;
- background maintenance budget.

Time budget exhaustion is evidence that strategy may need simplification or decomposition; it is not automatically a task failure.

### 5.5 Context budget

Context is a machine/model resource.

The controller must track:

- model context capacity;
- observed latency as context grows;
- token budget per reasoning phase;
- evidence packet size;
- recent working memory size;
- number and size of specialist contexts;
- condensation overhead.

AlinaCoder must prefer selective retrieval and condensation over pushing the model near an unstable or inefficient context limit.

---

## 6. Resource Profiles

Support at least these runtime profiles:

```text
CONSERVATIVE
BALANCED
PERFORMANCE
AUTO
```

`AUTO` is the default and chooses budgets from observed machine capacity and pressure.

The profile controls ceilings, not correctness requirements. A performance profile may use more resources but cannot weaken verification or safety.

---

## 7. Real Machine Model Selection

Model selection must **not** be based primarily on parameter count, marketing labels or available VRAM.

VRAM/hardware fit is a feasibility signal only.

The selector must evaluate installed candidate models using real bounded mini-tests executed on the actual machine.

Canonical flow:

```text
Discover installed models
→ reject clearly infeasible candidates
→ run capability mini-tests
→ run latency/resource mini-tests
→ score reliability + fit
→ choose primary model
→ cache result by model digest + machine profile
```

---

## 8. Mandatory Model Mini-Test Suite

The exact fixtures may evolve, but selection must measure real behavior across several dimensions.

### 8.1 Structured output compliance

Can the model reliably return required typed/JSON action structures?

Measure:

- parse success rate;
- schema violation rate;
- recovery after correction prompt.

### 8.2 Instruction adherence

Give a short task with explicit constraints and verify whether the model respects them.

Examples:

- do not edit specified file;
- preserve public signature;
- return only requested fields;
- distinguish evidence from assumption.

### 8.3 Code localization

Provide a small repository fixture and ask the model to identify the most relevant file/symbol from evidence.

### 8.4 Code reasoning

Use a bounded bug or logic fixture requiring causal reasoning rather than syntax completion.

### 8.5 Patch quality

Measure whether a candidate can propose a minimal correct change that passes hidden local fixture tests.

### 8.6 Regression awareness

Test whether the model uses impacted pass-to-pass evidence and notices a candidate fix that breaks previously valid behavior.

### 8.7 French conversational understanding

Include short, imperfect French and contextual references.

### 8.8 Noisy/ambiguous instruction handling

Measure whether it gathers evidence or expresses uncertainty instead of inventing certainty.

### 8.9 Long-context use

Run a bounded context-use probe that requires retrieving the relevant fact from distributed evidence.

### 8.10 Resource/latency fit

Measure locally:

- first-token latency where observable;
- tokens/second or completion latency;
- peak VRAM/RAM where observable;
- failure/OOM rate;
- responsiveness under representative context size.

---

## 9. Model Capability Profile

Mini-tests produce a persisted `ModelCapabilityProfile` keyed by:

```text
(model_digest, machine_fingerprint, ollama_version, probe_suite_version)
```

Representative dimensions:

```text
ModelCapabilityProfile
- schema_reliability
- instruction_adherence
- localization_score
- reasoning_score
- patch_correctness
- regression_awareness
- french_understanding
- ambiguity_handling
- context_use
- latency
- resource_cost
- stability
- confidence_calibration
- recommended_context_budget
- recommended_task_complexity
- measured_at
```

The profile is invalidated when the model digest, probe suite, important machine resources or Ollama version changes materially.

---

## 10. Model Selection Objective

The selector should maximize a reliability-adjusted utility, not raw capability.

Conceptually:

```text
utility = correctness_reliability
        + instruction_adherence
        + regression_awareness
        + context_use
        + language_fit
        - instability_penalty
        - resource_pressure_penalty
        - latency_penalty_when_material
```

No single scalar should override mandatory floors.

A model that is faster but repeatedly violates structured actions or misses regressions is not preferred for autonomous coding.

---

## 11. Weak Model Detection

AlinaCoder must explicitly detect when the selected local model is too weak for a task or task phase.

Signals may include:

- mini-test capability below required task threshold;
- repeated schema failures;
- repeated incorrect localization;
- hypothesis churn without new evidence;
- high disagreement between independent passes;
- critic repeatedly finding basic mistakes;
- inability to preserve constraints;
- regression miss rate above floor;
- context saturation;
- tool misuse;
- low confidence calibration;
- poor hidden/canary performance for similar task classes.

Weakness is task-relative. A model may be acceptable for a narrow mechanical change and inadequate for a broad architecture migration.

---

## 12. Task Capability Requirement

Before a nontrivial mission, AlinaCoder derives a `TaskCapabilityRequirement`.

Example dimensions:

```text
TaskCapabilityRequirement
- minimum_reasoning_level
- localization_complexity
- dependency_depth
- context_requirement
- language_understanding_requirement
- regression_risk
- architecture_risk
- required_confidence
- required_verification_strength
- estimated_resource_cost
```

The runtime compares this requirement with the current `ModelCapabilityProfile` and `MachineProfile`.

---

## 13. Strategy Adaptation When Model Is Weak

If capability is marginal, AlinaCoder must adapt strategy before giving up.

Allowed adaptations include:

1. reduce task scope;
2. split one broad task into smaller independently verifiable tasks;
3. retrieve more deterministic evidence before model reasoning;
4. replace broad generative reasoning with repository graph queries;
5. create a deterministic reproduction first;
6. use stronger targeted tests as guidance;
7. use shorter context packets;
8. reduce simultaneous hypotheses;
9. require isolated alternative passes;
10. enable conditional specialist roles only if measured to improve the task class;
11. execute steps sequentially rather than concurrently;
12. use history-derived precedents;
13. prefer an existing project pattern over inventing a new architecture;
14. choose a smaller reversible patch;
15. increase verification relative to generation complexity.

The principle is:

> **Compensate for model weakness with better structure, evidence, decomposition and verification before increasing autonomy risk.**

Autonomy remains active; strategy becomes more conservative and evidence-driven.

---

## 14. Reliability Calibration

AlinaCoder must distinguish:

- model confidence;
- system confidence;
- evidence strength.

Model self-confidence is never sufficient.

A task-level `ReliabilityAssessment` is derived from:

```text
- reproduction strength
- deterministic test evidence
- impacted regression coverage
- dependency/architecture understanding
- model capability fit
- alternative-design agreement/disagreement
- critic findings
- unresolved assumptions
- context freshness
- resource pressure
- historical performance on similar tasks
```

Suggested output classes:

```text
PROVEN
STRONG
ADEQUATE
MARGINAL
UNRELIABLE
UNPROVABLE
```

---

## 15. Explicit Right to Say “I Don't Know”

AlinaCoder must be able to state clearly when available evidence and local capability are insufficient.

Examples of valid user-facing conclusions:

```text
Je ne sais pas encore quelle est la cause avec assez de fiabilité.
```

```text
Le modèle local et les preuves disponibles ne sont pas assez fiables pour modifier cette partie directement.
```

```text
Je ne peux pas prouver que cette migration est sûre dans l'état actuel.
```

This is not considered a failure of autonomy. It is correct uncertainty handling.

AlinaCoder must not fabricate certainty merely to continue.

---

## 16. Reliability-First Fallback

When reliability is below the required floor, AlinaCoder must try to transform the task.

Canonical fallback:

```text
Unreliable broad task
→ identify uncertain dimensions
→ derive smaller subproblems
→ rank by observability/verifiability
→ execute the highest-confidence subproblem
→ gather evidence
→ update capability/reliability
→ continue or stop honestly
```

Example:

```text
“Refactor the entire persistence architecture”
```

may become:

```text
1. map current persistence interfaces;
2. add characterization tests;
3. isolate one adapter boundary;
4. migrate one consumer;
5. verify pass-to-pass behavior;
6. only then evaluate wider migration.
```

The user should not have to provide this decomposition.

---

## 17. Verifiability-First Task Decomposition

The task decomposer scores candidate subtasks by:

- deterministic observability;
- testability;
- regression blast radius;
- dependency depth;
- reversibility;
- required context;
- model capability fit;
- resource cost.

Prefer the next subtask that maximizes information gain and verification strength while minimizing irreversible scope.

---

## 18. Machine-Aware Planning

The planner must include machine constraints as planning evidence.

Examples:

- avoid full-repo mutation testing on a weak CPU when targeted impact analysis is sufficient;
- avoid loading a giant local model when a smaller measured model performs better on the actual task class;
- avoid parallel specialist sessions under VRAM pressure;
- schedule expensive repository indexing incrementally;
- cap context rather than triggering paging;
- sequence large test suites if parallel execution would exhaust RAM;
- postpone noncritical background self-improvement while user-facing work is resource-constrained.

Machine adaptation changes strategy and scheduling, never the correctness floor.

---

## 19. Resource-Aware Specialist Routing

If specialist agents are available under the prior v0.2 amendment, the `AgentValueEstimator` must now include resource cost.

A specialist is activated only when:

```text
expected_quality_gain
> resource_cost + latency_cost + coordination_risk
```

and the current machine has sufficient headroom.

Under resource pressure, prefer:

- sequential specialist passes;
- one high-value specialist rather than several;
- deterministic tools over extra model calls;
- single-agent reasoning with stronger verification.

---

## 20. Resource-Aware Internet Research

External research can also be resource-budgeted.

The research engine should stop expanding source breadth when:

- claims are sufficiently corroborated;
- marginal new evidence is low;
- time budget is reached;
- a primary authoritative source resolves the question;
- research no longer affects the decision.

Do not spend machine/time budget collecting redundant sources with no decision value.

---

## 21. Context Scaling Strategy

For weak or resource-constrained models, AlinaCoder must not respond by blindly maximizing context.

Use:

- hierarchical summaries;
- exact evidence packets;
- graph neighborhood retrieval;
- retrieval by current plan phase;
- condensed history;
- artifact pointers;
- narrow hypothesis-specific context.

If a task requires more simultaneous context than the model can reliably use, decompose by architecture boundary or causal question.

---

## 22. Real-World Performance Memory

AlinaCoder should learn how each model actually performs on this machine over time.

Persist aggregate runtime observations by task class:

```text
ModelRuntimeHistory
- task_class
- success_rate
- regression_rate
- average_retries
- deadlock_rate
- schema_failure_rate
- mean_latency
- resource_pressure_events
- average_context_size
- critic_rejection_rate
- rollback_rate
```

This history informs later model selection and strategy adaptation.

Historical performance is evidence, not an immutable rule; model updates invalidate stale conclusions.

---

## 23. Adaptive Primary/Secondary Model Policy

If several local models are installed, AlinaCoder may maintain:

- one primary model for general autonomous work;
- optional secondary model candidates for narrow task classes where measured mini-tests and runtime history show a meaningful advantage.

This is capability routing, not permanent multi-agent complexity.

A secondary model may be selected for a bounded reasoning phase only when it is both machine-feasible and empirically superior for that phase.

If v0.2 remains configured for one active model at a time, switching is sequential and resource-controlled.

---

## 24. Reliability Gate Before Mutation

For medium/high-risk changes, AlinaCoder evaluates whether it is sufficiently reliable **before broad mutation**.

A broad edit is disallowed when:

- task/model fit is `UNRELIABLE`;
- key dependencies remain unidentified;
- reproduction is required but unavailable and no equivalent evidence exists;
- context cannot be represented reliably;
- resource pressure makes verification incomplete;
- required test envelope cannot run;
- critical assumptions remain untested.

The fallback is evidence collection or task decomposition, not blind editing.

---

## 25. Reliability Gate Before Commit/Push

Existing Done Contracts are strengthened with machine/model reliability evidence.

A commit/push requires:

1. mandatory safety checks pass;
2. acceptance evidence is sufficient;
3. no newly introduced impacted regression remains;
4. required verification completed under a resource state that did not invalidate results;
5. reliability is above the task's minimum floor;
6. critical model capability limitations were either mitigated or rendered irrelevant by deterministic evidence;
7. unresolved uncertainty is documented and noncritical;
8. no test was skipped solely because of resource pressure unless an explicitly approved equivalent verification exists.

Resource limits may delay or decompose work; they cannot silently lower the Done Contract.

---

## 26. Self-Improvement Evaluation Extension

The external self-improvement supervisor must evaluate resource behavior as part of before/after benchmarking.

Add metrics for:

- CPU cost;
- GPU/VRAM cost;
- RAM peak;
- context efficiency;
- task latency;
- OOM/failure rate;
- resource-pressure recovery;
- model-selection quality;
- weak-model adaptation quality;
- calibrated abstention quality;
- decomposition success.

An “improvement” that raises benchmark correctness slightly but causes unacceptable resource instability is rejected.

---

## 27. Hidden Benchmark Additions

The hidden/canary benchmark suite should include cases where:

1. the largest model is **not** the best choice on the actual machine;
2. VRAM fit alone predicts the wrong model;
3. a weak model must detect its own limits;
4. a broad task should be decomposed rather than attempted directly;
5. excessive context worsens performance;
6. resource pressure appears mid-task;
7. parallel specialists cause harmful VRAM contention;
8. a fast model misses a regression that a slower measured model catches;
9. a model is highly confident but deterministically wrong;
10. available evidence is genuinely insufficient and correct behavior is `UNPROVABLE`/honest uncertainty.

These hidden cases must remain protected from self-improvement overfitting under the prior amendment.

---

## 28. Acceptance Scenarios

Implementation is not complete until automated fixtures/E2E tests demonstrate at least:

1. machine CPU/RAM/GPU resources are discovered without fabricated values;
2. resource-profile changes trigger policy adaptation;
3. CPU/process concurrency stays within configured controller policy;
4. RAM pressure causes safe backoff instead of uncontrolled growth;
5. GPU pressure reduces model/specialist concurrency;
6. context budget shrinks under measured pressure;
7. two installed models are compared using real mini-tests;
8. a model with more parameters/VRAM demand loses selection when its measured reliability-adjusted score is worse;
9. capability profile is invalidated after model digest/probe-suite change;
10. a weak model is detected for a complex task;
11. the complex task is automatically decomposed into more verifiable subtasks;
12. AlinaCoder explicitly reports insufficient reliability when evidence remains inadequate;
13. no broad mutation occurs under `UNRELIABLE` task/model fit;
14. machine constraints alter scheduling without weakening verification;
15. hidden self-improvement benchmark rejects a change that improves visible score but harms resource stability;
16. resource-aware specialist routing avoids harmful parallelism;
17. runtime history improves future model/strategy selection;
18. commit/push remains direct to `main` only after reliability-aware Done Contract passes.

---

## 29. New Structured Events

Emit at least:

```text
machine.profile_discovered
machine.profile_changed
resource.pressure_detected
resource.budget_adjusted
resource.task_throttled
model.probe_started
model.probe_finished
model.selected
model.rejected
model.capability_stale
model.capability_insufficient
reliability.assessed
reliability.insufficient
task.decomposition_requested
task.decomposed
context.budget_adjusted
specialist.resource_rejected
```

---

## 30. Metrics

Add at least:

- model-selection accuracy on hidden fixtures;
- structured-output failure rate per model;
- task/model capability mismatch rate;
- OOM/resource-crash rate;
- resource-pressure recovery success;
- average CPU/GPU/RAM cost by task class;
- context tokens per accepted task;
- weak-model successful decomposition rate;
- incorrect-certainty rate;
- correct abstention rate;
- `UNPROVABLE` precision;
- decomposition-to-success conversion rate;
- verification completeness under pressure;
- resource-related rollback rate.

The target is not zero abstentions. The target is **low incorrect certainty and high useful completion**.

---

## 31. Explicit anti-patterns

AlinaCoder must not:

1. choose a model solely because it fits in VRAM;
2. assume the biggest installed model is the best;
3. benchmark only synthetic throughput while ignoring coding correctness;
4. consume all available RAM/VRAM because it is technically possible;
5. run maximum parallelism by default;
6. increase context blindly when reasoning fails;
7. claim certainty because the model sounds confident;
8. attempt a broad high-risk task when task/model fit is unreliable;
9. lower tests because the machine is slow;
10. use resource constraints as an excuse to commit incompletely verified code;
11. repeatedly retry a model that has demonstrated task-class inadequacy without changing strategy;
12. hide uncertainty from the user;
13. turn every weak-model situation into multi-agent fan-out;
14. optimize benchmark performance at the cost of machine stability;
15. confuse hardware capacity with reasoning capability.

---

## 32. Final amended design contract

AlinaCoder v0.2 is not only repository-aware and context-aware; it is also **machine-aware and capability-aware**.

It must know:

- what resources the current machine actually has;
- what resources are currently available;
- how much CPU/GPU/RAM/time/context a strategy is consuming;
- which installed model performs best on real local coding mini-tests;
- what the selected model is good and bad at;
- whether a task exceeds current model/machine reliability;
- how to simplify or decompose the task when needed;
- when deterministic evidence can compensate for model weakness;
- when it genuinely cannot establish a reliable answer.

The governing principle is:

> **Use the machine you actually have, measure the model you actually run, choose the smallest strategy that can be verified, and never replace uncertainty with invented confidence.**

Autonomy remains total, but autonomy is now explicitly **calibrated to evidence, machine capability and verifiability** rather than raw ambition.
