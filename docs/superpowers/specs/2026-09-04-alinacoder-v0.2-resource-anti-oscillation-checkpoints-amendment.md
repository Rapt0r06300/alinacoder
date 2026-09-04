# AlinaCoder v0.2 — Resource Anti-Oscillation, Checkpointed Model Switching and Robust Benchmarking Amendment

Date: 2026-09-04  
Status: Approved normative amendment to AlinaCoder v0.2  
Repository: `Rapt0r06300/alinacoder`  
Canonical development branch: `main` only  
Extends:
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-conversation-and-external-self-improvement-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-research-voice-context-specialists-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-resource-awareness-model-calibration-amendment.md`

## 1. Normative status

This document is an official extension of the AlinaCoder v0.2 specification. It strengthens resource adaptation and local-model calibration by adding four mandatory constraints:

1. resource adaptation must be anti-oscillatory rather than reacting to single noisy measurements;
2. model changes are allowed only at explicit safe checkpoints;
3. model benchmarks must be repeated and variance-aware rather than single-shot;
4. relatively fixed hardware capabilities and dynamic machine load must be represented and reasoned about separately.

All prior v0.2 requirements remain mandatory. This amendment does not reduce autonomy, safety, verification, direct-to-`main` behavior, rollback, context discipline, hidden benchmarks, research requirements or weak-model self-awareness.

---

## 2. Core principle

AlinaCoder must adapt to the machine **without becoming unstable because the machine state fluctuates**.

The governing rule is:

> Measure repeatedly, separate capacity from temporary load, change strategy gradually, and change models only at recoverable checkpoints.

A transient CPU spike, short-lived VRAM pressure or single slow model response must not cause immediate architecture-level strategy changes.

---

## 3. Fixed hardware versus dynamic load

The previous `MachineProfile` concept is split into two first-class state objects.

### 3.1 HardwareProfile

`HardwareProfile` describes relatively stable machine capacity.

Representative fields:

```text
HardwareProfile
- os_version
- cpu_model
- physical_cores
- logical_cores
- cpu_features_if_available
- total_ram
- pagefile_capacity
- gpu_devices[]
- gpu_vendor
- gpu_model
- gpu_vram_total
- gpu_compute_capability_if_available
- storage_devices[]
- storage_type_if_available
- architecture
- ollama_version
- installed_model_digests[]
- fingerprint
- measured_at
```

The profile is rebuilt only when there is evidence of a material configuration change such as:

- GPU added/removed or driver-visible capacity changes;
- RAM capacity changes;
- Ollama version changes materially;
- installed model digest changes;
- OS/hardware fingerprint changes.

Dynamic utilization values must not be stored as intrinsic hardware capability.

### 3.2 DynamicLoadSnapshot

`DynamicLoadSnapshot` represents current transient operating conditions.

Representative fields:

```text
DynamicLoadSnapshot
- cpu_utilization
- cpu_queue_pressure_if_available
- available_ram
- committed_ram
- paging_pressure
- gpu_utilization
- gpu_vram_free
- gpu_vram_used
- thermal_signal_if_available
- storage_free_space
- active_ollama_sessions
- measured_model_latency
- external_process_pressure
- captured_at
```

Snapshots are time-series observations, not durable capability claims.

### 3.3 Why the separation is mandatory

A machine capable of running a model must not be reclassified as incapable merely because another workload temporarily occupies VRAM.

Likewise, a model that performs well under clean conditions is not inherently weak because one benchmark was executed during a transient system load spike.

---

## 4. Resource pressure state machine

Dynamic resource adaptation uses a deterministic pressure state machine.

Required states:

```text
NORMAL
ELEVATED
HIGH
CRITICAL
```

The controller derives pressure from a window of recent `DynamicLoadSnapshot` values.

Pressure is not based on one scalar. It may consider:

- CPU utilization;
- available RAM and paging;
- GPU utilization and free VRAM;
- thermal signals where trustworthy;
- task latency degradation;
- subprocess saturation;
- context growth effects;
- test/build process pressure.

---

## 5. Anti-oscillation policy

### 5.1 No single-sample transitions

A single measurement must never trigger a model switch or major resource-mode change unless it represents an emergency condition such as imminent OOM, severe disk exhaustion or an explicit process failure.

### 5.2 Smoothed observations

The controller must maintain smoothed pressure signals, for example EWMA or bounded moving windows.

The exact implementation may vary, but tests must prove that isolated spikes are ignored while sustained pressure is detected.

### 5.3 Consecutive-evidence requirement

Normal transitions require sustained evidence across multiple samples.

Conceptually:

```text
NORMAL -- sustained upper threshold --> ELEVATED
ELEVATED -- sustained upper threshold --> HIGH
HIGH -- sustained emergency threshold --> CRITICAL
```

### 5.4 Hysteresis

The threshold used to leave a pressure state must be meaningfully different from the threshold used to enter it.

Example concept:

```text
enter HIGH at smoothed pressure >= 0.82
leave HIGH only at smoothed pressure <= 0.68
```

Exact thresholds are configuration/policy values and must be tested, not hard-coded as universal truths.

### 5.5 Minimum dwell time

Once the runtime changes resource mode, it must remain in that mode for a configured minimum dwell period unless an emergency condition requires escalation.

### 5.6 Cooldown

After an expensive adaptation such as model switch or specialist fan-out reduction, a cooldown prevents immediate reversal.

### 5.7 Progress-sensitive adaptation

Resource adaptation must consider current task progress.

If a task is close to completing an atomic verified phase, prefer finishing that phase under safe throttling rather than disrupting it solely for a small efficiency gain.

---

## 6. Resource actions by severity

Resource adaptation should escalate gradually.

### NORMAL

- normal context budget;
- normal test/index concurrency;
- selected model remains resident when appropriate;
- specialists allowed if value estimator approves.

### ELEVATED

Prefer low-disruption actions first:

- reduce background indexing;
- lower nonessential concurrency;
- postpone self-improvement work;
- trim optional context;
- sequence specialists.

### HIGH

Stronger adaptations become eligible:

- shrink context budgets;
- reduce test parallelism;
- suspend noncritical research/indexing;
- avoid specialist fan-out;
- prepare a possible model change at the next checkpoint;
- decompose expensive tasks.

### CRITICAL

Protect machine and recoverability:

- stop new expensive work;
- finish or abort current atomic action safely;
- persist state;
- release optional resources;
- permit emergency fallback at the next safe checkpoint;
- if execution cannot remain safe, enter `FAILED_SAFE` or deferred resume state.

Correctness and verification requirements are never silently reduced.

---

## 7. ModelSwitchCheckpoint

A model is stable within an atomic reasoning/execution phase.

Model changes are allowed only at a `ModelSwitchCheckpoint`.

Required checkpoint classes include:

```text
TASK_START
TASK_END
PLAN_REVISED
RECOVERY_COMPLETED
CONTEXT_CONDENSED
EXPLICIT_SAFE_CHECKPOINT
```

Additional checkpoint classes may be added if they guarantee equivalent consistency.

---

## 8. Forbidden model-switch windows

AlinaCoder must not change the active model:

- while generating an atomic patch;
- between an active hypothesis and its immediate falsification probe;
- during an active shell command;
- during a test execution;
- while applying an atomic file write;
- during Git commit creation;
- during memory transaction persistence;
- during rollback/recovery mutation;
- while an intent fragment is still being resolved into the same atomic mission step;
- in the middle of an unresolved structured tool/action response.

The objective is semantic continuity and reproducibility.

---

## 9. Safe model-switch protocol

At a checkpoint, switching follows:

```text
request switch
→ persist active task/plan/hypotheses
→ flush memory transaction
→ capture Git/workspace state
→ close current reasoning phase
→ record old model + capability profile
→ evaluate eligible replacement
→ switch
→ run bounded smoke probe
→ accept or revert model
→ resume from checkpoint state
```

A failed smoke probe automatically restores the previous viable model when possible.

Model switching itself must emit structured evidence and be resumable after crash.

---

## 10. Pending model switch

Resource pressure or capability evidence may request a model switch before a checkpoint is available.

The controller stores a `PendingModelSwitch` rather than switching immediately.

Representative fields:

```text
PendingModelSwitch
- requested_reason
- requested_at
- preferred_target_model
- urgency
- triggering_evidence
- expiry_or_recheck_policy
```

At the next eligible checkpoint, the request is re-evaluated against fresh load. If the condition has disappeared, the switch may be cancelled.

This avoids reacting to transient pressure.

---

## 11. Repeated model mini-benchmarks

Single-run mini-tests are not reliable enough for model selection.

Each important model probe must execute repeated trials or controlled variants where practical.

Typical policy:

```text
fixture family × 3–5 repetitions
```

The exact repetition count may depend on probe cost, but a single run cannot define a robust capability claim except for deterministic hard failures such as OOM or schema parser rejection under a deterministic response fixture.

---

## 12. Benchmark result statistics

Model probe reports must include at least:

- number of trials;
- success count/rate;
- median quality result where numeric;
- worst acceptable result;
- dispersion/variance estimate;
- structured-output failure rate;
- regression miss rate;
- latency p50;
- latency p95 where enough samples exist;
- peak/representative RAM and VRAM observations where measurable;
- OOM/crash count;
- retry count;
- load conditions during execution.

A model with a very high best run but unstable repeated results must be penalized.

---

## 13. Stability-aware model scoring

Model selection must prefer repeated reliability over isolated peaks.

Conceptually:

```text
robust_score = central_quality
             - instability_penalty
             - regression_penalty
             - schema_failure_penalty
             - resource_failure_penalty
             - unacceptable_tail_penalty
```

Mandatory floors remain separate from ranking.

Example:

```text
Model A: 100, 20, 100
Model B: 88, 90, 89
```

If both satisfy feasibility constraints, Model B should normally be preferred for autonomous coding because its reliability is substantially higher.

---

## 14. Benchmark load normalization

Because dynamic load can distort latency/resource metrics, every trial records its contemporaneous `DynamicLoadSnapshot`.

The benchmark system distinguishes:

- capability/correctness result;
- machine-fit resource result;
- transient-load contamination.

When load contamination exceeds a configured limit, a trial may be marked `CONTAMINATED` and repeated later rather than permanently damaging the model's capability profile.

Correctness failures that are clearly independent of system load remain valid failures.

---

## 15. ModelCapabilityProfile identity

The durable capability profile is keyed primarily by stable factors:

```text
model_digest
HardwareProfile.fingerprint
ollama_version
probe_suite_version
```

Dynamic load is stored as benchmark metadata and runtime history, not as part of the stable capability identity.

This prevents excessive profile fragmentation.

---

## 16. Benchmark refresh policy

Re-probing is triggered when:

- model digest changes;
- probe suite changes materially;
- HardwareProfile fingerprint changes;
- Ollama version changes materially;
- long-term runtime evidence significantly contradicts stored probe conclusions;
- repeated failures indicate model degradation or corruption.

Transient machine load alone does not invalidate the entire profile.

---

## 17. Model-switch decision gate

At a checkpoint, a model switch requires evidence that expected benefit exceeds switching cost and risk.

The decision considers:

- task capability requirement;
- current model capability profile;
- replacement model capability profile;
- current pressure state;
- task phase;
- context migration cost;
- expected latency/resource benefit;
- expected quality benefit;
- cooldown state;
- previous recent switch history.

Repeated switching without measurable benefit is itself a failure signal.

---

## 18. Switch budget and oscillation detection

The runtime tracks model-switch frequency.

Signals of pathological oscillation include:

- alternating between the same two models repeatedly;
- repeated switch requests cancelled shortly afterward;
- switches with no improvement in resource pressure or task progress;
- more than a configured number of switches per mission/task window.

When detected:

- increase switch cooldown;
- pin the best-known viable model temporarily;
- prefer task decomposition/context reduction over further switching;
- emit `model.oscillation_detected`.

---

## 19. Weak-model behavior under checkpoint constraints

If the current model is judged insufficient mid-phase, AlinaCoder does not abruptly switch.

It must first:

1. stop broadening the task;
2. avoid unsafe mutation;
3. gather deterministic evidence if cheap;
4. reach the nearest safe checkpoint;
5. persist state;
6. evaluate whether to switch models or decompose the task.

If no stronger feasible model exists, task decomposition remains the preferred fallback.

---

## 20. Resource-aware task decomposition

When sustained resource pressure makes a broad task unreliable, decomposition should reduce simultaneous resource demand.

Possible decompositions include:

- architecture mapping separate from mutation;
- one module migration at a time;
- characterization tests before implementation;
- per-component indexing rather than whole-repo indexing;
- sequential specialist roles rather than concurrent roles;
- targeted test batches rather than unrestricted parallel test execution.

Machine constraints may change task shape but not correctness requirements.

---

## 21. Self-improvement benchmark robustness

The external self-improvement supervisor must also use repeated robust benchmarks.

Before/after comparisons require:

- multiple trials for stochastic model-driven metrics;
- hidden holdout cases;
- distributional summaries rather than best-run comparison;
- stability/regression floors;
- resource metrics split into hardware capability and dynamic-load observations;
- matched or load-normalized conditions where practical.

A candidate may not be promoted because of one lucky benchmark run.

---

## 22. Hidden benchmark protection extension

Hidden evaluation must include cases for:

- resource values oscillating around thresholds;
- transient GPU pressure that disappears before checkpoint;
- repeated high/low pressure samples;
- model-switch requests during forbidden atomic phases;
- unstable model with strong best-case performance;
- stable model with slightly lower peak performance;
- benchmark trials contaminated by external load;
- repeated model switching with no progress;
- task decomposition outperforming model churn.

The agent must not see hidden-case details during self-improvement.

---

## 23. Required structured events

Add at least:

```text
hardware.profile_discovered
hardware.profile_changed
load.snapshot_recorded
resource.pressure_transition_requested
resource.pressure_transitioned
resource.hysteresis_hold
resource.cooldown_active
model.switch_requested
model.switch_deferred
model.switch_checkpoint_reached
model.switch_completed
model.switch_reverted
model.switch_cancelled
model.oscillation_detected
model.benchmark_trial_started
model.benchmark_trial_finished
model.benchmark_trial_contaminated
model.benchmark_summary_updated
```

---

## 24. Required metrics

Add at least:

- pressure-state transition count;
- false transition count on synthetic oscillating fixtures;
- model switches per task/mission;
- cancelled pending switches;
- switch success rate;
- switch rollback rate;
- oscillation detections;
- median dwell duration;
- benchmark trial variance;
- contaminated trial rate;
- model ranking stability across repeated runs;
- task success rate after decomposition versus repeated model switching.

---

## 25. Acceptance scenarios

Implementation is not complete until automated tests demonstrate at least:

1. a single CPU/GPU spike does not trigger a pressure transition;
2. sustained pressure does trigger escalation;
3. hysteresis prevents immediate de-escalation near the threshold;
4. minimum dwell time prevents rapid mode ping-pong;
5. model switching is rejected/deferred during atomic patch generation;
6. model switching is rejected/deferred during tests and Git commit;
7. a pending switch is executed at the next checkpoint if still justified;
8. a pending switch is cancelled when transient load has disappeared;
9. failed smoke probe restores the prior viable model;
10. repeated benchmark trials penalize an unstable model;
11. stable repeated performance outranks a higher but erratic best score;
12. dynamic-load contamination does not mutate fixed HardwareProfile capability;
13. HardwareProfile changes only on stable configuration changes;
14. model capability profile does not fragment on every load snapshot;
15. repeated switching between two models triggers oscillation protection;
16. resource pressure can cause task decomposition without lowering Done Contract requirements;
17. self-improvement promotion rejects a candidate whose apparent gain is not robust across repeated hidden trials.

---

## 26. Explicit anti-patterns

AlinaCoder must not:

1. switch models because of one noisy telemetry sample;
2. switch models in the middle of an atomic reasoning/execution phase;
3. equate temporary VRAM pressure with permanent machine incapability;
4. update `HardwareProfile` from transient utilization values;
5. rank models using one lucky benchmark result;
6. ignore repeated variance or worst-tail failures;
7. switch back immediately after a model change without cooldown unless safety requires it;
8. run repeated model switching instead of decomposing a task when switching produces no progress;
9. invalidate all capability history because of temporary system load;
10. silently weaken verification when pressure is high.

---

## 27. Final amended contract

Resource adaptation in AlinaCoder v0.2 must be **stable, checkpointed and evidence-based**.

The system must know the difference between:

- what hardware the machine fundamentally has;
- what load the machine is under right now;
- what a model can reliably do across repeated trials;
- whether the current task actually requires a different model;
- whether it is safe to change models at the current phase.

The governing implementation principle is:

> **Separate capacity from load, smooth before reacting, require hysteresis before reversing, benchmark repeatedly, and only change models at explicit recoverable checkpoints.**
