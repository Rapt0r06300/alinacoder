# AlinaCoder v0.2 — Common Ground, Playback-Truth & Streaming Conversation Intelligence Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose, scope and precedence

This amendment is additive to all previously approved AlinaCoder v0.2 specifications and amendments.

It specifically strengthens the previously normative conversational architecture defined by:

- `Intent Beam`;
- `IntentContract` and `GroundedIntentContract`;
- `Conversation Repair Graph`;
- `GroundingState`;
- `ConstraintLedger`;
- `ConversationEventLog`;
- `ConversationalReferenceResolver`;
- `UserCommunicationModel`;
- `IntentAwareContextCompiler`;
- `DuplexConversationController`;
- `CrossTurnRegressionGate`;
- the unified `AlinaCoder.exe` shell;
- the Adaptive Zero-Cost Frontier Fabric;
- semantic transactions, verification gates and stale-response rejection.

It does **not** replace those mechanisms. It closes additional gaps revealed by a second research wave focused on common ground, playback truth, multi-turn repair, conversational reference grounding, streaming voice, user-specific ambiguity, long-horizon memory, interactive coding, and low-latency speculative preparation.

Where this amendment introduces a stricter rule for:

- shared conversational commitments;
- separation between observed facts and task-state judgments;
- heard versus merely generated speech;
- streaming partial-input processing;
- correction/repair behavior across heterogeneous models;
- implicit requirement recovery;
- conversation-specific model routing;
- long-horizon multi-turn evaluation;
- UI action semantics;
- or speculative read-only work;

this amendment has precedence for the affected subsystem.

All non-negotiable safety, zero-cost, privacy, main-only Git, local-first, verification and reversibility invariants remain unchanged.

The target remains:

> **maximum grounded intent fidelity, minimum corrective burden, minimum latency, and maximum verified continuity — without silently converting assumptions, unheard speech, stale memories or speculative work into user-authorized truth.**

---

# Part I — Research audit protocol

## 2. Research findings are candidates, not automatic requirements

Every external finding SHALL pass a `SpecResearchAudit` before becoming normative.

Required verdicts:

```text
ACCEPT_NEW
MERGE_STRENGTHEN
WATCH
REJECT_REDUNDANT
REJECT_WEAK_EVIDENCE
REJECT_INCOMPATIBLE
```

Required audit fields:

```text
SpecResearchAudit
- finding_id
- source
- source_class
- publication_date
- claim
- current_spec_overlap
- incremental_value
- testability
- portability
- privacy_impact
- latency_impact
- resource_impact
- safety_impact
- contradiction_risk
- verdict
- target_spec_objects
- acceptance_scenarios
```

The purpose is to improve the specification continuously without allowing uncontrolled feature accumulation.

## 3. Source preference

Research priority SHALL be:

```text
peer-reviewed / proceedings / primary paper
> official technical documentation / official engineering report
> reproducible benchmark / maintained public implementation
> credible secondary synthesis
> community anecdote or product marketing
```

Lower-priority evidence can discover ideas but SHALL NOT alone establish a critical invariant.

## 4. Audit results for this wave

The following findings were audited against the existing conversational specification.

| Finding | Verdict | Normative outcome |
| --- | --- | --- |
| Explicit common ground / public commitments | ACCEPT_NEW | `CommonGroundLedger` |
| Fact layer separated from task judgments | ACCEPT_NEW | `SituationState` split |
| Model-specific repair unreliability | ACCEPT_NEW | `RepairBehaviorProfile` |
| Partner-specific referring conventions | ACCEPT_NEW | `SharedReferenceConvention` |
| Grounding failure forecasting | ACCEPT_NEW | conservative `GroundingRiskForecaster` |
| Dependency-aware clarification | REJECT_REDUNDANT | already covered by `GoalDependencyGraph` / clarification policy |
| Supervisor vs expert clarification ownership | MERGE_STRENGTHEN | `ClarificationOwnerRouter` |
| Multi-tool reference grounding benchmark | MERGE_STRENGTHEN | `ReferenceResolutionProof` + benchmark |
| Full-duplex barge-in | MERGE_STRENGTHEN | existing duplex controller gains richer interruption taxonomy |
| Playback-aligned conversational state | ACCEPT_NEW | `PlaybackCommitLedger` |
| Personalized VAD / primary speaker filtering | WATCH + OPTIONAL | conversational filter only; never authentication |
| Duration-aware endpoint prediction | ACCEPT_NEW | `TurnContinuationForecast` |
| Streaming micro-turns | ACCEPT_NEW | `MicroTurnStream` |
| Code-switch semantic ASR metrics | MERGE_STRENGTHEN | technical-span metrics added |
| Cross-session personalized ambiguity | MERGE_STRENGTHEN | user-model `AmbiguityPatternMemory` |
| Persona trees over unrestricted personal traits | REJECT_INCOMPATIBLE | only interaction/workflow preferences allowed |
| Adaptive memory routing | MERGE_STRENGTHEN | `MemoryRetrievalPlan` |
| Raw-evidence-preserving memory graphs | MERGE_STRENGTHEN | source-span provenance + drift checks |
| UI direct manipulation as conversation | MERGE_STRENGTHEN | typed `UIConversationAct` |
| Foreground/background/resume communication | MERGE_STRENGTHEN | `AttentionAwareCommunicationPolicy` |
| Interactive plan mutation | MERGE_STRENGTHEN | transactional `PlanEditEvent` |
| Implicit requirement recovery | ACCEPT_NEW | `ImplicitRequirementRecoveryStage` |
| Stage-aware coding failure diagnosis | ACCEPT_NEW | `FailureAttributionLedger` |
| Corrective-turn burden | ACCEPT_NEW | collaboration metric |
| Persistent multi-turn coding durability | ACCEPT_NEW | sustainable-turn benchmark |
| Dialogue ability distinct from coding ability | ACCEPT_NEW | route capability dimension |
| Change-type-dependent regression risk | ACCEPT_NEW | `ConversationChangeRiskClassifier` |
| Semantic prefetch while user is speaking | MERGE_STRENGTHEN | `SemanticPrefetchTrigger` |
| Predictive retrieval cache across turns | ACCEPT_NEW | `PredictiveReadCache` |
| Speculative tool calling from partial input | ACCEPT_NEW WITH HARD LIMITS | read-only speculation classes |
| Early low-content acknowledgments | REJECT_REDUNDANT | already covered; only gating strengthened |
| Unlimited full-history prompting | REJECT_INCOMPATIBLE | bounded working state remains required |
| Supabase as canonical conversation bus | REJECT_INCOMPATIBLE | local truth remains canonical |

---

# Part II — Common ground as explicit state

## 5. Full history is not common ground

A conversation history containing a statement does not prove that both parties have established it as shared understanding.

AlinaCoder SHALL distinguish:

```text
RAW_HISTORY
PRIVATE_AGENT_HYPOTHESIS
OBSERVED_FACT
PUBLICLY_PRESENTED_CONTENT
USER_ACKNOWLEDGED_CONTENT
GROUNDED_COMMON_STATE
```

A model MAY infer privately, but private inference SHALL NOT automatically become shared conversational truth.

## 6. CommonGroundLedger

Introduce a versioned `CommonGroundLedger` representing commitments sufficiently established for the current collaborative purpose.

Suggested schema:

```text
CommonGroundLedger
- ledger_version
- session_id
- active_project
- commitments[]
- reference_conventions[]
- disputed_items[]
- open_grounding_gaps[]
- last_updated_at
```

Each commitment:

```text
GroundedCommitment
- commitment_id
- proposition
- type
- source_actor
- source_turn_or_event
- evidence
- presentation_status
- uptake_status
- scope
- confidence
- valid_from
- superseded_by
- revoked_by
- status
```

## 7. Commitment lifecycle

Required lifecycle:

```text
PROPOSED
→ PRESENTED
→ UPTAKE_OBSERVED
→ GROUNDED
```

Alternative transitions:

```text
PROPOSED → REJECTED
PRESENTED → CORRECTED
GROUNDED → SUPERSEDED
GROUNDED → REVOKED
GROUNDED → DISPUTED
```

The required grounding strength depends on consequence.

Low-risk conversational shorthand MAY ground with lightweight uptake.
High-impact destructive or irreversible interpretation requires stronger evidence or deterministic authorization gates.

## 8. Public commitment versus factual truth

Common ground records what is mutually established for coordination; it does not make an external factual claim true.

Example:

```text
user: “on appelle ce module le routeur principal”
→ may enter common ground as terminology

user: “cette API est gratuite”
→ cannot enter factual execution authority without current cost proof
```

This preserves the distinction between:

```text
user intent authority
shared terminology
external factual truth
policy authority
```

## 9. Commitments must be scoped

A commitment SHALL carry scope such as:

```text
CURRENT_TURN
CURRENT_TASK
CURRENT_PROJECT
CURRENT_SESSION
PERSISTENT_USER_WORKFLOW
```

A project-specific convention SHALL NOT silently become a global preference.

## 10. Common-ground repair propagation

When a user correction supersedes a grounded item:

1. mark old item `SUPERSEDED` or `REVOKED`;
2. create corrected item with provenance;
3. update dependent references;
4. invalidate plans/actions relying on the old item;
5. refresh working context;
6. update the visible intent/common-ground UI where shown.

No stale grounded commitment may remain silently active after a material correction.

---

# Part III — Situation truth versus task judgment

## 11. SituationState split

The existing `GroundingState` SHALL be internally separable into two layers:

```text
GroundedFactState
TaskJudgmentState
```

This separation prevents inferred planning judgments from being mistaken for observed facts.

## 12. GroundedFactState

Contains provenance-backed observations only.

```text
GroundedFact
- entity
- attribute
- value
- source
- source_hash_or_version
- observed_at
- freshness
- confidence
- contradiction_status
```

Typical sources:

```text
repository contents
git state
test output
compiler output
runtime observation
official documentation
user statement about user-owned intent/preferences
validated tool result
```

## 13. TaskJudgmentState

Contains derived execution judgments:

```text
IntentState
RequiredVariable
ConstraintState
DependencyState
ExecutabilityState
PlanState
RiskState
```

These are conclusions over facts and constraints, not facts themselves.

## 14. Deterministic cross-layer propagation

Whenever material facts change, re-evaluate applicable constraints and intent executability.

Example:

```text
fact: target file no longer exists
→ constraint requiring edit of that file becomes UNSATISFIED
→ dependent plan step becomes BLOCKED
→ alternate discovery step becomes ACTIVE
```

Unknown facts SHALL remain `UNKNOWN` / `UNSATISFIED`, not be coerced into `VIOLATED` or `SATISFIED`.

## 15. Executability gate

An intent may become executable only when:

```text
required dependencies satisfied
required variables sufficiently grounded
no active hard constraint violated
state version current
semantic transaction admission succeeds
```

This turns understanding into a state transition rather than an informal model impression.

---

# Part IV — Model-specific conversational reliability

## 16. RepairBehaviorProfile

Different model families can exhibit different repair failure modes: stubbornness, excessive accommodation, generic clarification, over-questioning, or failure to update assumptions.

Maintain a route-specific profile:

```text
RepairBehaviorProfile
- model_lineage
- provider_route
- language_condition
- valid_correction_acceptance_rate
- wrong_correction_resistance_rate
- misleading_user_suggestion_susceptibility
- clarification_precision
- clarification_recall
- generic_question_rate
- repeated_question_rate
- assumption_update_rate
- correction_propagation_rate
- reference_grounding_rate
- common_ground_retention_rate
- sample_count
- last_measured_at
```

## 17. Conversation capability is separate from coding capability

Extend `ModelCapabilityVector` with explicit dimensions:

```text
dialogue_collaboration
repair_quality
clarification_quality
common_ground_tracking
reference_grounding
user_correction_assimilation
multiturn_constraint_preservation
spoken_turn_control
```

A model strong at coding SHALL NOT automatically be assumed strongest at talking with the user.

The architecture MAY use one route for conversational mediation and another for code generation while preserving one canonical state.

## 18. Repair-aware routing

When a turn is dominated by correction, ambiguity, cross-session reference or conversational repair, route selection SHOULD weight the relevant conversational capability profile more heavily than generic benchmark strength.

## 19. No self-reported repair promotion

A model cannot improve its own `RepairBehaviorProfile` by declaring that it understood correctly.

Promotion evidence must derive from:

```text
benchmark outcomes
user correction rate
reference ground-truth
constraint preservation
executable task outcome
independent verifier evidence
```

---

# Part V — Grounding risk forecasting

## 20. GroundingRiskForecaster

Introduce a lightweight forecaster that estimates whether unresolved conversational state is likely to cause downstream repair or incorrect action.

Possible inputs:

```text
IntentBeam separation
unresolved references
constraint density
recent corrections
ASR instability
model repair profile
active task stakes
cross-session dependency
repo ambiguity
```

Outputs:

```text
LOW
ELEVATED
HIGH
CRITICAL
```

with structured reasons.

## 21. Forecasting is advisory, not a question generator

The forecaster SHALL NOT blindly increase clarification frequency.

It may trigger:

```text
local inspection
reference proof
memory retrieval
safe probe
stronger mediator route
interpretation preview
clarification only when value-of-information justifies it
```

This avoids converting grounding research into an over-questioning assistant.

---

# Part VI — Shared reference conventions and proofs

## 22. SharedReferenceConvention

Humans naturally develop shorter shared names over repeated collaboration. AlinaCoder MAY establish explicit, scoped shared aliases after sufficient evidence.

Example:

```text
“le routeur” → src/alinacoder/intelligence_mesh/router.py
“la roadmap” → canonical active project roadmap file
“le dernier run” → latest verified execution run in current project
```

Schema:

```text
SharedReferenceConvention
- alias
- target
- scope
- established_by
- evidence_turns
- ratification_evidence
- ambiguity_set
- confidence
- valid_from
- valid_until
- superseded_by
```

## 23. Convention compression is earned

AlinaCoder MAY use a shorter shared expression only after it is reliably grounded.

If multiple plausible targets arise later, the alias becomes ambiguous again.

## 24. ReferenceResolutionProof

Material indirect references SHALL produce an internal proof object when resolution requires workspace search.

```text
ReferenceResolutionProof
- phrase
- candidate_set
- search_strategy
- inspected_candidates
- supporting_evidence
- rejected_alternatives
- selected_target
- confidence
- risk_if_wrong
- state_version
```

## 25. Close-alternative rejection

Reference grounding is not complete merely because one plausible candidate is found.

For material actions, AlinaCoder SHOULD inspect sufficiently close alternatives and record why they were rejected.

## 26. Reference benchmark extension

The Conversation Quality Lab SHALL include RepoRef/CoRG-style tasks where references require:

```text
lexical evidence
semantic evidence
temporal evidence
Git metadata
issue/commit/file inspection
multi-step tool use
close-alternative rejection
```

Metrics:

```text
ReferenceGroundingSuccessRate
CloseAlternativeRejectionRate
ReferenceToolEfficiency
WrongTargetMutationRate
ReferenceClarificationRate
```

Target invariant:

```text
WrongTargetMutationRate = 0 for hidden high-impact reference tests
```

---

# Part VII — Clarification ownership in a specialist system

## 27. ClarificationOwnerRouter

When clarification is truly required, select the internal agent best positioned to formulate it.

Possible owners:

```text
CONVERSATION_MEDIATOR
REPOSITORY_SPECIALIST
VOICE_ASR_SPECIALIST
SECURITY_POLICY_SPECIALIST
DOMAIN_SPECIALIST
EXECUTION_SPECIALIST
```

High-level goal ambiguity belongs to the mediator.
Domain-specific ambiguity discovered after inspection belongs to the specialist with the necessary evidence.

## 28. One user-facing voice

Internal clarification ownership SHALL NOT expose multi-agent chatter to the user.

The user receives one concise coherent question from AlinaCoder.

## 29. Clarification context handoff

The selected owner receives:

```text
GroundedIntentContract
CommonGroundLedger relevant subset
missing information point
candidate hypotheses
already inspected evidence
why local resolution failed
```

This prevents asking questions already answerable from another specialist’s work.

---

# Part VIII — Playback truth in voice conversation

## 30. Generated speech is not heard speech

In full-duplex voice, server generation can run ahead of client playback.

Therefore:

> **assistant content becomes conversationally public only to the extent that it was actually rendered to the user, not merely generated or buffered.**

## 31. PlaybackCommitLedger

Introduce:

```text
PlaybackCommitLedger
- assistant_turn_id
- generated_audio_range
- client_played_sample_boundary
- semantic_audibility_boundary
- finalized_semantic_spans
- revoked_audio_range
- playback_ack_version
- interruption_anchor
- last_updated_at
```

## 32. Physical playback boundary

`PlayedAudioBoundary` is the latest output sample confirmed rendered by the client.

Anything after it is speculative media and can be revoked.

## 33. Semantic audibility boundary

`SemanticAudibilityBoundary` is the latest complete proposition whose finalized audio endpoint was actually played.

A partially heard sentence may affect human understanding but SHALL NOT automatically satisfy a structured confirmation/action precondition.

## 34. Playback acknowledgment

The desktop client SHALL periodically acknowledge playback position for active assistant voice output.

This acknowledgment is separate from:

```text
Supabase Realtime ACK
network receipt
TTS generation completion
LLM token generation
```

None of those prove the user heard the content.

## 35. Interruption transaction

On a confirmed interruption while speaking:

1. capture user-speech onset with current playback position;
2. freeze `PlayedAudioBoundary`;
3. stop or duck playback immediately;
4. cancel ongoing assistant generation where possible;
5. invalidate buffered/unheard audio;
6. suppress late packets/output from cancelled generation;
7. compute `SemanticAudibilityBoundary`;
8. project canonical conversation history to heard/committed content;
9. release the new user turn to semantic processing;
10. update Repair Graph and CommonGroundLedger.

## 36. Unheard content cannot bind the user

Unheard generated content SHALL NOT:

```text
count as user-visible instruction
count as a confirmation request that the user ignored
satisfy a prerequisite
become common ground
be assumed known by the user
be used as the sole basis for interpreting a later interruption
```

## 37. Cross-model voice handoff

If a cognitive model switches during voice interaction, handoff state SHALL use playback-committed conversational state, not the full generated assistant buffer.

## 38. Black-box voice provider fallback

If exact semantic/audio alignment is unavailable:

```text
prefer conservative truncation
remove or mark incomplete assistant turn as ungrounded
re-inject heard audio if supported
require explicit confirmation for semantic preconditions that depend on the interrupted content
```

Never invent character/time alignment from crude heuristics when it can change action semantics.

---

# Part IX — Rich interruption and turn-taking semantics

## 39. InterruptionIntentClassifier

Extend duplex interruption classification to at least:

```text
USER_CORRECTION
FOLLOW_UP_QUESTION
TOPIC_SWITCH
REPEAT_REQUEST
STOP_OR_CANCEL
DISSATISFACTION
BACKCHANNEL
SIDE_SPEECH
THIRD_PARTY_SPEECH
THINKING_ALOUD
UNKNOWN_INTERRUPTION
```

## 40. Respond versus resume

After overlap, choose explicitly among:

```text
RESPOND_TO_INTERRUPTION
RESUME_PRIOR_RESPONSE
ABANDON_PRIOR_RESPONSE
WAIT_FOR_MORE_USER_SPEECH
ASK_REPAIR
```

Backchannels usually favor `RESUME_PRIOR_RESPONSE`.
A correction or follow-up usually favors `RESPOND_TO_INTERRUPTION`.
`STOP_OR_CANCEL` favors immediate abandonment.

## 41. Primary speaker conversational filter

An optional local primary-speaker model MAY reduce false barge-ins from television audio, background people or another nearby speaker.

This mechanism:

```text
MAY help turn-taking
MAY help suppress false interruptions
MUST NOT be treated as strong identity authentication
MUST NOT authorize high-impact actions solely from voice identity
```

## 42. TurnContinuationForecast

Endpointing SHALL optionally estimate not only “complete/incomplete” but also expected continuation timing.

```text
TurnContinuationForecast
- completion_probability
- expected_time_to_next_speech
- pause_type
- acoustic_confidence
- semantic_confidence
```

Use this to dynamically tolerate human hesitation instead of applying one fixed silence timeout.

## 43. Pause adaptation

The system MAY learn non-sensitive turn-taking preferences such as typical pause tolerance or backchannel frequency from repeated validated interaction patterns.

Current explicit user configuration always wins.

---

# Part X — Streaming micro-turn architecture

## 44. MicroTurnStream

Voice input SHALL be representable as a stream of micro-turn events rather than only complete utterances.

```text
MicroTurn
- micro_turn_id
- user_turn_id
- timestamp_range
- stable_text_delta
- unstable_text_delta
- acoustic_features_summary
- semantic_sufficiency
- turn_state
- repair_marker
- language_spans
```

## 45. Micro-turns are not missions

A micro-turn exists for streaming state evolution.

It SHALL NOT independently create a durable user mission unless semantic admission determines a real completed/committed intent.

## 46. Semantic sufficiency

Maintain a `SemanticSufficiencySignal` estimating whether a partial stream contains enough stable meaning to permit specific classes of background work.

It SHALL be task/action specific rather than a universal threshold.

## 47. Micro-turn correction

When later speech changes the meaning of an earlier partial:

```text
invalidate speculative interpretation
preserve raw audio/transcript evidence
update Repair Graph
cancel invalid speculative background work if useful
retain independent valid read results only as unbound cache entries
```

---

# Part XI — Safe speculative preparation

## 48. Faster interaction through preparation, not premature mutation

AlinaCoder MAY exploit user speech time, TTS playback time, tool wait time and idle time to prepare likely-needed context.

This MUST NOT weaken effect admission.

## 49. SpeculationClass

Classify speculative operations:

```text
PURE_COMPUTE
READ_ONLY_LOCAL
READ_ONLY_REMOTE
REVERSIBLE_LOCAL_CANDIDATE
MUTATING_WORKTREE
MUTATING_EXTERNAL
IRREVERSIBLE_EXTERNAL
```

## 50. Partial-turn speculation policy

Before semantic turn commitment, automatically permitted classes are normally limited to:

```text
PURE_COMPUTE
READ_ONLY_LOCAL
READ_ONLY_REMOTE when privacy/cost policy permits
```

`REVERSIBLE_LOCAL_CANDIDATE` requires an isolated non-canonical candidate surface with no user-visible durable effect.

The following are forbidden from unstable partial speech:

```text
MUTATING_WORKTREE
MUTATING_EXTERNAL
IRREVERSIBLE_EXTERNAL
commit
push
send
publish
delete
purchase
permission change
```

## 51. SemanticPrefetchTrigger

Trigger background preparation only when partial input has enough semantic density to make the expected value positive.

Avoid firing on:

```text
fillers
hesitation-only fragments
very low-confidence ASR
highly unstable repair sequences
```

## 52. PredictiveReadCache

Maintain a short-lived local cache of likely next-turn evidence.

Examples:

```text
recent project files
likely referenced symbols
nearby Git commits
relevant memory evidence
selected documentation
candidate test definitions
```

Schema:

```text
PredictiveReadCacheEntry
- content_ref
- source_version
- predicted_use
- created_at
- expires_at
- sensitivity
- freshness
- bound_to_intent: false by default
```

## 53. Prediction is not provenance for execution

A prefetched item becomes actionable evidence only after the actual committed intent selects/revalidates it.

Cache hits accelerate retrieval; they do not establish relevance by themselves.

## 54. Cache invalidation

Invalidate/refresh when:

```text
repo HEAD/worktree changes
source file hash changes
memory source superseded
user changes project
conversation branch changes materially
TTL expires
privacy scope changes
```

## 55. Speculative cancellation

Every speculative job SHALL be cancellable or safely ignorable.

A semantic shift does not require waiting for irrelevant speculative work to finish.

---

# Part XII — ASR technical-span intelligence

## 56. TechnicalSpanProfile

Voice understanding SHALL identify technically fragile spans:

```text
English code terms inside French
file paths
symbols
package names
Git SHAs
provider/model IDs
CLI flags
URLs
numbers
negations
```

## 57. Repository vocabulary bias

The active repository MAY provide a local dynamic ASR lexicon containing:

```text
file names
symbols
packages
project names
model names
recent commits/short SHAs
commands
```

This lexicon is evidence for decoding/reranking, not permission to force uncertain audio into a repository term.

## 58. Semantic ASR metrics

Extend voice evaluation with:

```text
TechnicalSpanErrorRate
CodeSwitchSpanErrorRate
SemanticAnswerErrorRate
CriticalNegationErrorRate
ReferencePhraseErrorRate
ActionIntentErrorRate
HallucinatedInsertionRate
```

WER/CER remain useful diagnostics but SHALL NOT be the sole route-selection metric.

## 59. Condition-specific ASR routing

ASR selection may differ between:

```text
clean French
noisy French
French-English coding speech
short commands
long dictation
path/SHA-heavy utterance
far-field speech
```

No global ASR champion is assumed.

---

# Part XIII — Personalized ambiguity without persona overreach

## 60. AmbiguityPatternMemory

Extend `UserCommunicationModel` with reusable ambiguity-resolution patterns.

```text
AmbiguityPatternMemory
- pattern_signature
- observed_phrasings
- resolved_meaning
- scope
- supporting_sessions
- contradictory_sessions
- confidence
- last_confirmed_at
```

## 61. History gating remains mandatory

A prior pattern may shortcut clarification only when:

```text
same user
applicable project/domain
repeated consistent evidence
no current explicit contradiction
current context supports same interpretation
risk_if_wrong acceptable
```

## 62. Interaction preferences only

Do not build broad inferred psychological/personality profiles for conversational optimization.

Permitted user-model dimensions are limited to useful, non-sensitive interaction/workflow signals such as:

```text
preferred brevity
preferred explanation depth
project aliases
stable coding conventions
clarification tolerance
voice turn-taking preferences
common command shorthand
preferred evidence detail
```

## 63. Preference drift

For low-risk UX preferences, AlinaCoder MAY distinguish:

```text
recent preference signal
long-term stable preference signal
```

A sudden persistent divergence MAY mark the older preference stale.

Current explicit instruction always overrides either signal.

## 64. Wrong-personalization metric

Track:

```text
PersonalizationHelpfulRate
PersonalizationWrongInferenceRate
RepeatedClarificationAvoidedRate
FirstTurnResolutionRate
TurnsToCompletion
```

A memory system that reduces questions by increasing wrong assumptions is a regression.

---

# Part XIV — Memory provenance and adaptive retrieval

## 65. Derived memory must point to raw evidence

Every important derived conversational memory SHALL retain source references to exact raw turn/event spans where practical.

```text
DerivedMemory
- normalized_claim
- source_event_ids
- source_spans
- derivation_version
- confidence
- scope
- freshness
```

## 66. SemanticDriftCheck

When a memory summary is created or materially rewritten, compare it with source evidence for:

```text
negation preservation
constraint preservation
entity preservation
temporal order
scope preservation
uncertainty preservation
```

Detected drift blocks promotion of the derived memory.

## 67. MemoryRetrievalPlan

Retrieval SHALL adapt to question/reference complexity.

Possible plan:

```text
EXACT_ONLY
LEXICAL_PLUS_RECENCY
SEMANTIC_PLUS_RECENCY
TEMPORAL_HIERARCHY
GRAPH_EXPANSION
MULTI_HOP_EVIDENCE
RAW_SOURCE_REHYDRATION
```

Simple queries should remain cheap.
Complex temporal/relational queries can widen retrieval deliberately.

## 68. Bounded working state

Maintain a strict working-context budget independent of total lifetime conversation length.

The system SHALL optimize retained working evidence by expected utility while preserving:

```text
active goals
hard constraints
recent repairs
current referents
critical facts
open uncertainties
verification anchors
```

## 69. Raw store plus semantic store

Canonical raw events remain append-only/reconstructable.
Semantic memory remains editable/versioned.

Semantic deletion or supersession SHALL NOT destroy raw provenance required for audit/recovery.

---

# Part XV — UI as a conversational language

## 70. UIConversationAct

Every meaningful direct manipulation in `AlinaCoder.exe` SHALL map to a typed semantic event when it changes shared task context.

Examples:

```text
SELECT_REFERENT
PIN_CONTEXT
EXCLUDE_CONTEXT
EDIT_INTENT
EDIT_CONSTRAINT
LOCK_CONSTRAINT
BRANCH_CONTEXT
RETURN_TO_MAINLINE
FOCUS_ITEM
IGNORE_ITEM
ELABORATE_ITEM
APPROVE_TEST_EXAMPLE
REJECT_TEST_EXAMPLE
PAUSE_EXECUTION
STOP_EXECUTION
TAKE_OVER_STEP
RETURN_STEP_TO_AGENT
```

## 71. BidirectionalActionHistory

Maintain one ordered history of meaningful actions from both user and AlinaCoder.

The conversation therefore includes:

```text
text
voice
selection
editing
branching
plan manipulation
approval/rejection
execution actions
```

## 72. UI action is evidence, not always a preference

A click or selection MAY be exploratory.

Do not automatically convert one UI gesture into a durable preference or constraint.

Use:

```text
current visual context
action type
repetition
temporal adjacency
explicit confirmation
resulting task state
```

to infer semantic weight.

## 73. Context-action atomicity

A user direct manipulation that changes task semantics SHALL update:

```text
ConversationEventLog
GroundingState
CommonGroundLedger when ratified
active context selection
state version
```

atomically enough that the next model call sees a coherent state.

---

# Part XVI — Transactional plan editing

## 74. PlanEditEvent

Every user/agent plan mutation SHALL be a structured event:

```text
PlanEditEvent
- event_id
- actor
- operation
- target_step
- before
- after
- dependency_impact
- intent_contract_version
- state_version
```

Operations:

```text
ADD
EDIT
DELETE
REORDER
PAUSE
RESUME
ASSIGN_USER
ASSIGN_AGENT
BRANCH
MERGE_VERIFIED
```

## 75. Descendant invalidation

When a step changes, invalidate/re-evaluate only dependent descendants where possible.

Independent verified work remains preserved.

## 76. Stepwise versus continuous execution

The interface SHALL allow task/stage-specific choice between:

```text
CONTINUOUS
STEPWISE
```

High uncertainty, unfamiliar tasks, or high regression risk can favor stepwise mode.
Well-understood low-risk tasks can remain continuous.

The default should minimize friction while preserving policy gates.

---

# Part XVII — Attention-aware communication

## 77. AttentionAwareCommunicationPolicy

Communication density SHALL depend on interaction state:

```text
FOREGROUND_ACTIVE
BACKGROUND
USER_RETURNING
WAITING_FOR_USER
CRITICAL_INTERVENTION
```

## 78. Foreground active

Show concise live progress with expandable evidence.

Do not stream raw private reasoning.

## 79. Background

Prefer quiet ambient status and only actionable alerts.

Avoid repeatedly appending low-value “still working” text to the conversation.

## 80. User returning

Generate an evidence-backed resume brief:

```text
what changed
what was verified
what was rejected/rolled back
current task state
current HEAD/worktree state when relevant
next active step
anything requiring user input
```

## 81. Consecutive-error auto-pause

If independent evidence indicates repeated non-progressing errors, AlinaCoder SHOULD auto-pause before compounding damage.

Thresholds SHALL be tuned by task class and evidence, not copied blindly from research prototypes.

---

# Part XVIII — Implicit requirement recovery for coding

## 82. ImplicitRequirementRecoveryStage

Before planning a nontrivial repository change, recover implementation-critical requirements that the user may reasonably assume from existing project context.

Evidence sources:

```text
explicit user request
active specs
README / AGENTS-style project rules
tests
public API behavior
types/interfaces
neighboring implementations
current architecture
recent accepted commits
packaging/runtime constraints
platform constraints
```

## 83. Requirement provenance classes

Each recovered requirement SHALL be labeled:

```text
EXPLICIT_USER
EXPLICIT_PROJECT_SPEC
EXECUTABLE_EXISTING_BEHAVIOR
REPOSITORY_CONVENTION
INFERRED_LIKELY
UNRESOLVED
```

## 84. Inference cannot silently outrank explicit intent

`INFERRED_LIKELY` requirements are candidates for validation, not user authority.

If an inferred convention conflicts with current explicit user direction, user direction wins unless blocked by higher policy/safety constraints.

## 85. RequirementCoverageTrace

Maintain:

```text
RequirementCoverageTrace
- requirement
- provenance
- plan_steps_covering
- tests/verifiers_covering
- implementation_artifacts
- status
```

This allows failure diagnosis before final patch evaluation.

---

# Part XIX — Stage-aware failure attribution

## 86. FailureAttributionLedger

A failed coding trajectory SHALL be diagnosed along stages:

```text
CONVERSATION_GROUNDING
REFERENCE_RESOLUTION
REQUIREMENT_RECOVERY
PLANNING
IMPLEMENTATION
TOOL_EXECUTION
REGRESSION_PRESERVATION
VERIFICATION
PACKAGING
REPORTING
```

## 87. Failure evidence

Attribution requires concrete evidence such as:

```text
missed requirement
wrong file/referent
contradictory plan step
failing test
unapplied dependency
incorrect tool action
stale assertion
broken prior behavior
```

## 88. Self-improvement uses stage attribution

Experience Cards and future challenger experiments SHALL target the stage actually responsible instead of generic “reason harder” retries.

---

# Part XX — Conversation-driven change risk

## 89. ConversationChangeRiskClassifier

Each coding follow-up SHALL classify requested change shape:

```text
COSMETIC
LOCAL_REFACTOR
INTERFACE_CHANGE
LOGIC_CHANGE
ADDITIVE_FEATURE
BEHAVIOR_BROADENING
VALIDATION_TIGHTENING
DEPENDENCY_CHANGE
ARCHITECTURAL_CHANGE
REVERSAL_OR_SUPERSESSION
```

## 90. Risk-conditioned verification

Evidence indicates logic-level/additive refinements can cause disproportionate multi-turn regressions.

Therefore elevated classes SHALL expand preservation verification proportionally.

Example:

```text
COSMETIC
→ focused lint/style verification

LOGIC_CHANGE / ADDITIVE_FEATURE
→ current tests + cumulative prior-behavior suite + affected dependency checks

ARCHITECTURAL_CHANGE
→ broad regression + contract + packaging/integration verification
```

## 91. Conversation risk is not only code diff size

A tiny edit can have high semantic risk if it changes a foundational requirement.

Risk classification considers:

```text
user intent delta
constraint delta
dependency depth
public API surface
historical fragility
change type
```

---

# Part XXI — Long-horizon conversational coding evaluation

## 92. Multi-turn success is a separate capability

Single-turn coding performance SHALL NOT be accepted as proof of persistent conversational coding reliability.

## 93. PersistentConversationCodingBench

Maintain tasks with:

```text
5–15+ evolving turns
persistent workspace
incremental requirements
corrections
supersessions
terse references
spec-file updates
cumulative tests
branch/context switches
```

## 94. Metrics

Track at least:

```text
FinalTaskSuccess
FirstTurnSuccess
UserCorrectionBurden
CorrectiveTurnsPerSuccessfulTask
MeanSustainableTurns
ActiveRequirementRetention
CrossTurnRegressionRate
ImplicitRequirementCoverage
ReferenceGroundingSuccessRate
ClarificationEfficiency
WrongProjectRate
WrongReferentRate
ConversationRecoveryRate
```

## 95. UserCorrectionBurden

A system that eventually succeeds after repeated user repair is worse conversationally than one that reaches the same verified result with fewer necessary corrections.

Corrective turns therefore become an explicit quality metric.

## 96. MeanSustainableTurns

Measure how many evolving turns an agent can preserve all active verified requirements before first material regression.

## 97. Cumulative behavior tests

Earlier validated tests/examples remain active until legitimately superseded.

Later turns do not reset evaluation state.

## 98. Document-driven turns

Include tests where the user says only:

```text
“j’ai mis à jour la spec, applique-la”
```

and the agent must discover the changed repository specification rather than rely exclusively on latest chat text.

## 99. Dialogue-versus-code route evaluation

Evaluate mediator and code-executor routes separately and jointly.

A pair of specialized models MAY outperform one “best overall” model if continuity and state contracts are preserved.

---

# Part XXII — Dependency-aware reasoning budgets

## 100. DependencyDepthSignal

Estimate relevant code dependency depth before complex changes.

Possible evidence:

```text
call graph
import graph
schema dependencies
public API consumers
test graph
plan dependency graph
```

## 101. Reasoning/test budget scaling

As dependency depth and active constraint density increase:

```text
increase structured decomposition
increase global integration checks
increase preservation tests
increase context precision
```

Do not merely increase free-form token count.

---

# Part XXIII — Conversation fast path and critical path isolation

## 102. Live path principle

Latency-critical voice/media handling SHALL remain isolated from slower tasks such as:

```text
long retrieval
heavy coding generation
persistence compaction
external research
background learning
```

Slower tasks communicate through asynchronous typed boundaries.

## 103. Fast visible acknowledgment lane

Existing fast acknowledgments MAY be used only when they add real interaction value.

They SHALL NOT:

```text
claim completion
claim verification
invent a plan not yet grounded
mask a stalled system with filler
```

## 104. Turn-to-useful-answer dominates token speed

Performance optimization SHALL measure:

```text
first safe feedback
first useful content
full useful answer
correction reaction
barge-in stop
```

rather than tokens/second alone.

---

# Part XXIV — Optional Supabase integration refinements

## 105. Local authority remains canonical

The local event/state store remains authoritative for:

```text
ConversationEventLog
CommonGroundLedger
PlaybackCommitLedger
GroundedFactState
TaskJudgmentState
IntentContract
ConstraintLedger
```

Supabase remains optional.

## 106. Optional Realtime mirror

When explicitly enabled, Supabase Realtime Broadcast MAY mirror non-secret ephemeral events such as:

```text
UI status
plan progress
activity summaries
cross-client presence
resume hints
```

Private channels + appropriate RLS are required.

## 107. Realtime replay is a UX aid

Broadcast replay MAY help a trusted UI reconnect and recover recent non-secret events.

Replay SHALL NOT replace reconstruction from canonical local state.

## 108. ACK distinction

Maintain distinct receipt semantics:

```text
NETWORK_DELIVERED
REALTIME_SERVER_ACK
CLIENT_RECEIVED
CLIENT_RENDERED
AUDIO_PLAYED
SEMANTICALLY_GROUNDED
ACTION_EXECUTED
ACTION_VERIFIED
```

These states SHALL NOT be conflated.

## 109. Supabase not on voice critical path

Voice turn-taking, playback acknowledgment, STOP/barge-in, local grounding and effect cancellation MUST continue without Supabase connectivity.

---

# Part XXV — New continuous-improvement artifacts

## 110. ConversationFailureCard

Extend failure learning with:

```text
ConversationFailureCard
- user_turn
- active_grounding_state
- expected_interpretation
- actual_interpretation
- failure_stage
- model_route
- repair_profile_snapshot
- user_correction
- root_cause
- prevention_rule
- regression_case_ref
```

## 111. ConversationSuccessCard

Successful hard cases can also become reusable evidence:

```text
ambiguous phrase
resolved reference strategy
minimal clarification
correct constraint propagation
successful model route
verification outcome
```

## 112. High-information conversation challenger

Prioritize replay/challenger cases where:

```text
multiple intents were close
reference alternatives were close
user corrected the model
model switch changed repair behavior
ASR uncertainty touched critical slots
multi-turn requirement regression almost occurred
```

This gives higher learning value than random easy conversations.

---

# Part XXVI — New acceptance scenarios

## 113. Common-ground acceptance

### Scenario CG-1 — private assumption must not become shared

User asks for a change with an ambiguous target.
Agent privately prefers target A.
No sufficient grounding occurs.

Expected:

```text
A remains PRIVATE_AGENT_HYPOTHESIS
not GROUNDED
high-impact mutation blocked until reference proof/clarification
```

### Scenario CG-2 — scoped terminology

User repeatedly calls `router.py` “le routeur” inside project A.
Later opens project B with another router.

Expected:

```text
alias applies to project A only
project B does not inherit target automatically
```

### Scenario CG-3 — correction supersedes common ground

Previously grounded constraint says “keep SQLite”.
User explicitly says “finalement remplace SQLite par X”.

Expected:

```text
old commitment SUPERSEDED
new commitment created
old dependent plan steps invalidated
unrelated constraints retained
```

## 114. Playback acceptance

### Scenario PB-1 — unheard sentence

AlinaCoder generates:

```text
“Je vais supprimer le fichier temporaire puis…”
```

but user interrupts after hearing only:

```text
“Je vais supprimer…”
```

Expected:

```text
unheard remainder revoked
no assumption that user heard target/details
no action prerequisite satisfied from unheard portion
canonical voice history projected conservatively
```

### Scenario PB-2 — late audio packet

Cancelled TTS emits a delayed packet after user barge-in.

Expected:

```text
packet suppressed
PlaybackCommitLedger unchanged
new user turn remains authoritative
```

### Scenario PB-3 — model switch during voice

Cognitive route changes while speaking.

Expected:

```text
new route receives only playback-grounded common state
unheard buffered generation excluded
```

## 115. Streaming acceptance

### Scenario ST-1 — filler

User:

```text
“euh… attends… donc…”
```

Expected:

```text
no expensive speculative swarm
no mutation
semantic trigger stays below useful threshold
```

### Scenario ST-2 — useful stable partial

User:

```text
“ouvre le dernier commit qui a modifié le routeur et…”
```

Expected:

```text
read-only Git lookup may start
result remains provisional
no edit/commit until turn commits
```

### Scenario ST-3 — repair invalidates partial

User:

```text
“cherche dans le routeur… non attends, dans le provider registry”
```

Expected:

```text
router prefetch detached/cancelled
provider-registry prefetch begins
no stale router result bound to final intent
```

## 116. Repair-profile acceptance

### Scenario RP-1 — misleading user challenge

Model gives evidence-backed correct result.
User asks “t’es sûr ? je crois que c’est l’inverse”.

Expected:

```text
re-check evidence
not reflexively flip answer
repair profile records outcome
```

### Scenario RP-2 — valid correction

Model selected wrong file.
User explicitly identifies correct file.

Expected:

```text
intent/reference correction accepted immediately
old dependent plan invalidated
no stubborn persistence
```

## 117. Reference acceptance

### Scenario REF-1 — “le commit d’hier”

Several commits exist around midnight/timezone boundary.

Expected:

```text
use user/project timezone
enumerate plausible date interval
inspect candidates
select only with sufficient evidence
```

### Scenario REF-2 — selected diff

User selects a hunk and says “garde ça mais refais le reste”.

Expected:

```text
selection becomes high-confidence referent
selected hunk preservation constraint created
rest of relevant scope may be revised
```

## 118. Coding acceptance

### Scenario CODE-1 — hidden project constraint

User asks for feature without restating established Windows packaging requirement.

Expected:

```text
ImplicitRequirementRecoveryStage finds normative packaging constraint
plan preserves it
```

### Scenario CODE-2 — ten-turn evolution

Task receives 10 successive changes.

Expected:

```text
all non-superseded earlier tests stay active
MeanSustainableTurns >= 10 for promotion case
no stale requirements resurrected
```

### Scenario CODE-3 — logic-level refinement

User asks for “same interface, different internal scheduling logic”.

Expected:

```text
ConversationChangeRiskClassifier = LOGIC_CHANGE
expanded regression suite required
public interface preservation verified
```

## 119. Personalization acceptance

### Scenario PER-1 — recurring shorthand

Three resolved sessions show same shorthand mapping.
Fourth session uses shorthand in same project context.

Expected:

```text
HistoryGate may infer mapping
no unnecessary question
```

### Scenario PER-2 — current override

Stored preference says concise answers.
User says “explique-moi tout en détail cette fois”.

Expected:

```text
current turn wins
persistent preference not deleted unless evidence says it changed globally
```

---

# Part XXVII — New metrics and release gates

## 120. Grounding metrics

```text
CommonGroundPrecision
CommonGroundRecall
FalseGroundingRate
GroundingRepairSuccess
GroundingCorrectionLatency
SharedReferenceReuseAccuracy
ReferenceGroundingSuccessRate
CloseAlternativeRejectionRate
```

Critical invariant:

```text
FalseGroundingHighImpactMutationRate = 0
```

## 121. Playback/voice metrics

```text
BargeInToAudioStopP50/P95
PlaybackBoundaryError
UnheardContentLeakRate
SemanticAudibilityCommitPrecision
BackchannelClassificationAccuracy
SideSpeechRejectionAccuracy
SemanticEndpointEarlyCutRate
SemanticEndpointLateResponseRate
TurnContinuationForecastError
```

Critical invariant:

```text
UnheardContentUsedAsSoleHighImpactAuthorization = 0
```

## 122. Streaming metrics

```text
SemanticPrefetchHitRate
SpeculativeWorkDiscardRate
SpeculativeMutationViolationRate
PredictiveReadCacheHitRate
PredictiveReadCacheStaleHitRate
TurnToFirstSafeFeedback
TurnToUsefulAnswer
```

Critical invariant:

```text
SpeculativeMutationViolationRate = 0
```

## 123. Interactive coding metrics

```text
UserCorrectionBurden
CorrectiveTurnsPerSuccessfulTask
MeanSustainableTurns
CrossTurnRegressionRate
RequirementCoverage
ImplicitRequirementCoverage
FailureStageAttributionAccuracy
ConversationChangeRiskCalibration
```

## 124. Memory/personalization metrics

```text
RawSourceTraceabilityRate
DerivedMemorySemanticDriftRate
WrongPersonalizationRate
RepeatedClarificationAvoidedRate
MemoryRetrievalLatencyP50/P95
RetrievalContextTokens
```

Critical invariant:

```text
DerivedMemoryCriticalNegationLossRate = 0
```

---

# Part XXVIII — Conceptual module additions

## 125. Conversation grounding modules

Conceptual paths:

```text
src/alinacoder/conversation/
  common_ground.py
  situation_state.py
  grounding_forecaster.py
  repair_profile.py
  shared_references.py
  reference_proof.py
  clarification_owner.py
  micro_turns.py
  turn_continuation.py
  interruption_intent.py
  playback_commit.py
```

## 126. Streaming preparation modules

```text
src/alinacoder/streaming/
  semantic_prefetch.py
  speculation_policy.py
  predictive_read_cache.py
  live_path.py
```

## 127. Coding collaboration modules

```text
src/alinacoder/coding_dialogue/
  implicit_requirements.py
  requirement_coverage.py
  change_risk.py
  failure_attribution.py
```

## 128. UI semantic modules

```text
src/alinacoder/desktop/
  ui_conversation_acts.py
  bidirectional_action_history.py
  attention_policy.py
  plan_edit_events.py
```

## 129. Evaluation modules

```text
src/alinacoder/evaluation/
  common_ground_bench.py
  reference_grounding_bench.py
  playback_truth_bench.py
  duplex_interruption_bench.py
  streaming_speculation_bench.py
  interactive_coding_bench.py
  personalized_ambiguity_bench.py
  memory_drift_bench.py
```

These are conceptual module boundaries, not a claim that runtime code already exists.

---

# Part XXIX — Canonical conversation loop after this amendment

## 130. Text/UI loop

```text
User text / UI act
→ RawTurn / UIConversationAct
→ CommonGroundLedger snapshot
→ GroundedFactState refresh
→ ReferenceResolutionProof if needed
→ Repair Graph
→ Intent Beam
→ ConstraintLedger
→ TaskJudgmentState
→ GroundingRiskForecaster
→ local/repo/memory research or clarification if valuable
→ GroundedIntentContract
→ ImplicitRequirementRecoveryStage for coding
→ ConversationChangeRiskClassifier
→ plan / semantic transaction
→ effect execution
→ verification
→ CommonGround/Assertion updates
→ FailureAttribution or success learning
```

## 131. Voice loop

```text
Audio stream
→ primary-speaker/acoustic signals
→ streaming ASR + language/technical spans
→ MicroTurnStream
→ SemanticSufficiencySignal
→ optional read-only SemanticPrefetchTrigger
→ TurnContinuationForecast
→ semantic endpoint / barge-in decision
→ stable RawTurn
→ normal grounding loop
```

Assistant output:

```text
model generation
→ semantic spans
→ TTS buffer
→ client playback
→ playback ACK
→ PlayedAudioBoundary
→ SemanticAudibilityBoundary
→ CommonGround eligibility
```

Interruption:

```text
user onset
→ freeze playback boundary
→ stop/cancel output
→ revoke unheard content
→ project canonical state
→ classify interruption
→ repair/ground new turn
```

## 132. Coding multi-turn loop

```text
new user change
→ reconcile with current GroundedIntentContract
→ recover implicit repo requirements
→ classify change risk
→ update active requirement set
→ plan edit transaction
→ implement candidate
→ cumulative preservation verification
→ reject/rollback on regression
→ update sustainable-turn metrics
→ commit only after Done Contract
```

---

# Part XXX — Non-negotiable conversational invariants

## 133. Invariants

AlinaCoder SHALL NOT:

- equate full conversation history with established common ground;
- silently promote private model assumptions into user commitments;
- treat user disagreement as automatic external factual truth;
- ignore explicit valid user correction because a model is “confident”;
- over-adapt to misleading correction without checking evidence;
- assume one model family has universal repair behavior;
- bind an indirect material reference without sufficient candidate discrimination;
- treat generated-but-unheard speech as if the user heard it;
- let cancelled late TTS output contaminate canonical dialogue state;
- use voice identity as sole authorization for high-impact actions;
- treat every backchannel as a new mission;
- use fixed acoustic silence alone as semantic turn completion;
- mutate worktree/external state from unstable partial speech;
- promote speculative prefetch results to truth without revalidation;
- let predictive cache stale entries survive relevant state changes;
- store broad sensitive inferred personality attributes for convenience;
- let derived memory lose critical negations or scope without detection;
- interpret every UI click as a durable preference;
- let a plan edit leave descendants silently based on obsolete assumptions;
- judge conversational quality solely by final task success;
- infer coding reliability from single-turn benchmark performance;
- infer dialogue quality from coding benchmark performance;
- allow later turns to silently erase still-active earlier requirements;
- make Supabase a mandatory dependency for conversation correctness;
- expose raw private chain-of-thought as the trust mechanism;
- claim “perfect understanding” without measurable grounding/repair gates.

---

# Part XXXI — Research evidence ledger for this wave

## 134. High-value research integrated

Research was cross-checked across Exa and Parallel Search on 2026-09-04. The following sources materially shaped this amendment.

### Conversational grounding and common ground

- **Conversational Grounding in Large Language Models: Evaluation Methods, Challenges and Future Directions** — SIGDIAL 2026, ACL Anthology.
- **Dialogue is the Plan: From Interface to Joint Action in Agentic AI** — ACL 2026.
- **Navigating Rifts in Human-LLM Grounding: Study and Benchmark (RIFTS)** — ACL 2025, retained as relevant grounding evidence.
- **Common-ground collaborative benchmark** — Poelitz, Doshi-Velez, Lindley, arXiv 2602.21337.
- **LVLMs and Humans Ground Differently in Referential Communication** — ACL 2026.
- **Talking to a Know-It-All GPT or a Second-Guesser Claude? How Repair reveals distinct Multi-Turn Behavior in LLMs** — ACL 2026.

### Situation state and references

- **Intent-Driven Situation Tracking for User-Centric Multi-Turn Agents (IDSS)** — arXiv 2608.15755.
- **You Know What I Mean: A Benchmark for Agentic Conversational Reference Grounding (RepoRef/CoRG)** — arXiv 2608.29834.
- **MAC: A Multi-Agent Framework for Interactive User Clarification in Multi-turn Conversations** — IWSDS 2026.

### Voice and playback truth

- **PACE: A Playback-Aligned Context Engine for LLM-Based Full-Duplex Voice Dialogue** — arXiv 2608.07631.
- **BayLing-Duplex: Native Full-Duplex Speech Dialogue with a Single Autoregressive LLM** — arXiv 2606.14528.
- **Full-Duplex Interaction in Spoken Dialogue Systems: ICASSP 2026 HumDial Challenge** — arXiv 2604.21406.
- **FastTurn** — arXiv 2604.01897.
- **Phoenix-VAD: Streaming Semantic Endpoint Detection for Full-Duplex Speech Interaction** — arXiv 2509.20410.
- **Next-Turn: Duration-Aware Streaming Endpoint Detection** — arXiv 2606.18094.
- **DuplexCascade** — arXiv 2603.09180.
- **ServiceNow AI code-switching voice benchmark** — 2026-06-09, includes French-English evaluation.

### Personalized memory

- **Fewer Clarifications, Better Code (CAPA)** — arXiv 2607.26611.
- **Inside Out: Evolving User-Centric Core Memory Trees** — ACL 2026.
- **MemORAI** — Findings of ACL 2026.
- **AdaMem** — arXiv 2603.16496.
- **HERO** — arXiv 2608.22310.
- **Preference-Aware Memory Update for Long-Term LLM Agents** — Findings ACL 2026.
- **TiMem** — Findings ACL 2026.

### Interactive coding

- **SWE-Interact** — arXiv 2606.30573.
- **SWE-Together** — arXiv 2606.29957.
- **SWE-RPG** — arXiv 2608.09072.
- **EvoCode-Bench** — arXiv 2605.24110.
- **Regression Accumulation in Multi-Turn LLM Programming Conversations** — arXiv 2607.01855.
- **Dialogue-SWEBench** — arXiv 2606.13995.
- **CodeChat-Eval** — arXiv 2606.25747.
- **CodeFlowBench** — ACL 2026.

### HCI and interface

- **Mixed-Initiative Context / Contextify** — arXiv 2604.07121.
- **Cocoa: Co-Planning and Co-Execution with AI Agents**.
- **Sidekick: Designing Communication for Effective Multitasking with Computer Use Agents** — arXiv 2607.17527.
- **DuetUI: A Bidirectional Context Loop for Human-Agent Co-Generation of Task-Oriented Interfaces**.
- **Co-Disclosing the Computer: LLM-Mediated Computing through Reflective Conversation** — 2026.

### Streaming latency

- **LTS-VoiceAgent** — arXiv 2601.19952.
- **ProactiveLLM** — ICML 2026.
- **Speculative Interaction Agents** — arXiv 2605.13360.
- **ProStream** — arXiv 2603.04885.
- **VoiceAgentRAG** — arXiv 2603.02206; treated as research evidence for predictive local cache, not as a mandatory dependency or exact performance promise.

## 135. Product/reference leads not treated as normative evidence alone

Public agent workbenches and community implementations can inspire UI/runtime patterns, but product marketing or repository claims alone SHALL NOT define correctness requirements.

Examples discovered in this wave include visual coding-agent workbenches and desktop agent shells. Their useful concepts are only adopted when independently compatible with AlinaCoder’s existing invariants and testable architecture.

---

# Part XXXII — Definition of success for this amendment

## 136. Conversation intelligence target

AlinaCoder is improved by this amendment only if, on representative hidden and replay evaluations, it becomes measurably better at:

```text
understanding evolving intent
maintaining shared commitments
recovering from user corrections
resolving indirect references
preserving constraints
handling full-duplex interruption
remembering only what is useful and justified
adapting to recurring user shorthand
minimizing unnecessary clarification
preserving code correctness over many turns
responding quickly without premature mutation
```

## 137. “Perfect AI” remains an engineering direction, not an unverifiable claim

The product SHALL pursue increasingly human-compatible interaction while retaining deterministic safeguards around probabilistic interpretation.

The correct product promise is not:

```text
“AlinaCoder can never misunderstand.”
```

It is:

```text
AlinaCoder makes understanding explicit enough to test,
keeps assumptions separate from shared truth,
finds and repairs misunderstandings early,
learns validated user conventions,
preserves the exact active specification over long sessions,
and prevents uncertain language from silently causing the wrong effect.
```

---

# Part XXXIII — Canonical end-state

## 138. Desired `AlinaCoder.exe` experience

```text
Open AlinaCoder.exe
→ talk naturally in French, type, select, click or edit
→ AlinaCoder tracks what is actually meant and what is actually shared
→ vague references are grounded against the real workspace
→ recurring shorthand becomes easier over time
→ unnecessary questions disappear
→ important ambiguity is surfaced before damage
→ the app can listen while preparing safe read-only context
→ it can answer with low latency without acting on unstable speech
→ interruptions stop speech immediately
→ unheard generated content is erased from conversational authority
→ model/provider switches remain invisible to task continuity
→ coding requirements accumulate and supersede correctly across many turns
→ old working behavior is preserved by cumulative tests
→ the interface shows goals, evidence, plan and activity only as deeply as wanted
→ STOP, pause, branch, edit and takeover remain cheap
→ the user never needs another normal interaction shell
→ verified effects, not model confidence, determine completion
```

The objective is a single coherent local conversational computer whose intelligence may be supplied by multiple dynamically selected zero-cost engines, but whose **identity, memory, grounding, commitments, execution state and relationship with the user remain stable inside `AlinaCoder.exe`.**
