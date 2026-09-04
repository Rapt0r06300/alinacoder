# AlinaCoder v0.2 — Conversational Grounding, Human Intent Fidelity, Duplex Voice & Unified Desktop Interface Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Purpose, scope and precedence

This amendment is additive to all previously approved AlinaCoder v0.2 specifications and amendments.

It specifically strengthens and operationalizes the existing:

- `Intent Beam`;
- persistent `IntentContract`;
- `Conversation Repair Graph`;
- dual `RAW + MEANING` speech representation;
- `Semantic Turn Manager`;
- `Ask-or-Infer Controller`;
- `Context Operating System`;
- uncertainty control plane;
- governed memory;
- semantic transactions;
- capability routing and model handoff.

It does **not** replace those mechanisms. It gives them stricter conversational contracts, measurable quality gates, voice behavior, personalization rules, interface semantics and continuous-improvement loops.

Where this amendment introduces a stricter rule for conversational understanding, clarification, correction assimilation, reference grounding, constraint preservation, voice handling, user-model memory, UI steering, progress communication, or conversation evaluation, the stricter rule has precedence.

The primary product goal is:

> **AlinaCoder.exe shall behave as one coherent conversational computer: understand ordinary human French as faithfully as practical, preserve evolving intent across long sessions, ask only when useful, correct itself quickly, make its interpretation inspectable and editable, and execute exactly the verified active intent rather than a stale or guessed approximation.**

---

# Part I — What “perfect understanding” means operationally

## 2. No false guarantee of literal perfection

No probabilistic AI system can honestly guarantee perfect understanding of every possible human utterance.

AlinaCoder SHALL therefore target a stronger engineering objective:

```text
maximum grounded intent fidelity
+ minimum user correction burden
+ zero silent high-impact guessing
+ rapid recovery from misunderstanding
+ measurable preservation of explicit constraints
+ deterministic execution gates around probabilistic interpretation
```

The user-facing experience MAY feel fluid and natural, but the implementation SHALL remain evidence-aware and self-correcting.

## 3. Conversational success definition

A conversation is successful only when all applicable conditions hold:

```text
correct active goal
correct active project
correct referents
critical constraints preserved
prohibitions preserved
superseded instructions removed from authority
new corrections propagated
required ambiguity resolved
unnecessary questions minimized
response/action matches user communication style
execution preserves prior verified behavior
progress claims are accurate
user can inspect/repair the interpretation cheaply
```

## 4. Conversation quality is multidimensional

AlinaCoder SHALL NOT compress conversational quality into one scalar confidence score.

Track at least:

```text
IntentConfidence
ReferenceConfidence
InformationSufficiency
ConstraintCompleteness
EvidenceConfidence
ExecutionConfidence
ConversationContinuityConfidence
ASRSemanticConfidence
```

These signals serve different control decisions.

Example:

```text
IntentConfidence = high
InformationSufficiency = low
→ intent is understood, but required implementation information is missing

IntentConfidence = low
EvidenceConfidence = high
→ facts may be known, but what the user wants remains ambiguous
```

---

# Part II — Conversational Intent Mediation

## 5. ConversationalIntentMediator

Before the main executor acts on a material user turn, the turn SHALL pass through a `ConversationalIntentMediator`.

Canonical pipeline:

```text
RawTurn
→ ReferenceGrounder
→ RepairGraph
→ AmbiguityClassifier
→ IntentBeam update
→ hierarchical goal decomposition
→ constraint extraction
→ conflict/precedence resolution
→ information-sufficiency analysis
→ clarification/retrieval/research decision
→ GroundedIntentContract
→ executor
```

The mediator MAY be implemented with one or more lightweight/strong models plus deterministic logic, but its output contract is model-independent.

## 6. Separation of mediation and execution

The subsystem deciding **what the user means** SHALL be logically separable from the subsystem deciding **how to execute it**.

This prevents an executor from rationalizing its preferred implementation into a distorted interpretation of the request.

## 7. RawTurn

Every user turn SHALL have an immutable or append-only `RawTurn` record.

Suggested schema:

```text
RawTurn
- turn_id
- session_id
- timestamp
- modality: TEXT | VOICE | MIXED | UI_DIRECT_MANIPULATION
- raw_text
- raw_audio_ref_if_available
- attachment_refs
- selected_ui_context
- selected_repo_context
- ASR_hypotheses_if_any
- source_language_hints
- interruption_metadata
```

The raw user wording remains recoverable even after semantic normalization.

## 8. GroundingState

The active shared conversational state SHALL be represented explicitly.

```text
GroundingState
- primary_goal
- active_subgoals
- goal_dependency_graph
- active_project
- active_repository
- active_branch_policy
- explicit_constraints
- explicit_prohibitions
- preferences
- assumptions
- current_referents
- unresolved_references
- unresolved_ambiguities
- superseded_instructions
- completion_criteria
- user_owned_decisions
- agent_inferred_decisions
- evidence_links
- last_user_correction
- last_revalidated_at
```

## 9. GroundedIntentContract

The existing `IntentContract` is extended with fields required for conversational fidelity.

```text
GroundedIntentContract
- literal_request
- normalized_request
- inferred_goal
- active_project
- goal_graph
- ConstraintLedger reference
- forbidden_actions
- preservation_requirements
- non_goals
- assumptions
- unresolved_questions
- referent_bindings
- correction_lineage
- user_model_evidence_used
- repo_evidence_used
- external_evidence_used
- information_sufficiency
- intent_confidence
- semantic_risk_if_wrong
- success_definition
- DoneContract reference
- version
```

## 10. Intent interpretation never silently rewrites history

When the mediator normalizes:

```text
“non attends plutôt le module de contexte, mais garde ce qu’on a dit sur la mémoire”
```

it SHALL preserve:

```text
old goal
repair operation
new priority
preserved portion
superseded portion
```

A clean paraphrase alone is insufficient provenance.

---

# Part III — Hierarchical Intent and Constraint Fidelity

## 11. GoalDependencyGraph

Complex requests SHALL be decomposed into a dependency-aware goal graph rather than a flat checklist.

Node types MAY include:

```text
PRIMARY_GOAL
SUBGOAL
CONSTRAINT
DECISION
QUESTION
VERIFICATION
DELIVERABLE
NON_GOAL
```

Edges MAY include:

```text
REQUIRES
BLOCKS
ENABLES
REFINES
SUPERSEDES
CONFLICTS_WITH
PRESERVES
VERIFIES
```

## 12. Dependency-aware clarification

Independent missing decisions MAY be asked together.

Dependent questions SHALL be sequenced so the user is not forced to decide downstream details before upstream intent is settled.

Example:

```text
Q1 target platform
→ determines
Q2 packaging strategy
→ determines
Q3 installation flow
```

Do not ask all three before Q1 when later answers depend materially on it.

## 13. ConstraintLedger

Every material explicit instruction SHALL enter an externalized `ConstraintLedger`.

Constraint classes:

```text
MUST
MUST_NOT
PREFER
ALLOW
SCOPE_ONLY
PRESERVE
EXAMPLE_NOT_REQUIREMENT
USER_DELEGATED_CHOICE
SUPERSEDED
```

Required fields:

```text
constraint_id
canonical_text
type
source_turn_id
scope
priority
precedence
status
verifier
superseded_by
confidence
```

## 14. Constraint precedence

Default precedence:

```text
current explicit user instruction
> current explicit correction
> active project normative invariant
> prior explicit user instruction still active
> user-approved persistent preference
> evidence-backed recurring user pattern
> agent assumption
```

Safety and system policy remain outside this user-preference precedence chain.

## 15. Latest instruction is not always global replacement

A later instruction overrides an earlier one only over the scope it actually changes.

Example:

```text
Turn 1: “ne supprime rien et améliore le module mémoire”
Turn 8: “finalement utilise SQLite”
```

The SQLite correction does not revoke `ne supprime rien`.

## 16. ConstraintComplianceGate

Before material actions, final answers, commits, pushes or claims of completion, run a `ConstraintComplianceGate`.

Checks include:

```text
all active MUST constraints addressed
no active MUST_NOT violated
preservation requirements verified
scope expansion authorized
delegated choices distinguished from user-fixed choices
superseded constraints excluded
```

## 17. Constraint density escalation

As active constraint count and dependency density grow, AlinaCoder SHOULD increase structured checking rather than relying on model recall.

This responds to empirical evidence that instruction adherence deteriorates as the number of simultaneous constraints increases.

---

# Part IV — Interaction Smell Detection

## 18. InteractionSmellDetector

Before generation and after every material answer/action, AlinaCoder SHALL detect common conversational failure patterns.

Required classes:

```text
AMBIGUOUS_INSTRUCTION
INCOMPLETE_INSTRUCTION
MUST_DO_OMISSION
MUST_NOT_VIOLATION
SCOPE_DRIFT
WRONG_PROJECT
WRONG_REFERENT
CROSS_TURN_INCONSISTENCY
SIGNATURE_OR_INTERFACE_MISMATCH
PARTIAL_FUNCTIONALITY_BREAKDOWN
CODE_ROLLBACK
REPETITIVE_NO_PROGRESS
STALE_MEMORY_USAGE
UNSUPPORTED_PROGRESS_CLAIM
OVER_CLARIFICATION
UNDER_CLARIFICATION
MISREAD_CORRECTION
```

## 19. Pre-generation smell gate

If a high-risk smell is detected before execution, the system SHALL resolve it via one of:

```text
local inspection
repository inspection
memory retrieval
external research
clarification
scope restriction
```

It SHALL NOT merely add a warning and continue unchanged.

## 20. Post-generation smell gate

The generated response/action SHALL be checked against the same conversation state that governed generation.

This catches cases where the model correctly parsed a constraint but failed to obey it in output.

## 21. No-progress detection

If a new response is semantically equivalent to an earlier failed/rejected response without new evidence, classify:

```text
REPETITIVE_NO_PROGRESS
```

and force a strategy change, new evidence acquisition, or concise blocker statement.

---

# Part V — Selective Clarification Intelligence

## 22. Specification uncertainty versus model uncertainty

The system SHALL distinguish:

```text
SPECIFICATION_UNCERTAINTY
MODEL_KNOWLEDGE_UNCERTAINTY
ENVIRONMENT_UNCERTAINTY
REFERENCE_UNCERTAINTY
EVIDENCE_CONFLICT
```

Only some of these justify asking the user.

Example:

```text
unknown installed library version
→ inspect environment

unknown preference between two incompatible UX designs
→ retrieve prior decision; if absent and material, ask
```

## 23. ClarificationPolicy

Clarification SHALL be a decision policy, not a fixed confidence threshold.

Estimate:

```text
value_of_question
≈ probability_answer_changes_decision
× consequence_of_wrong_guess
× probability_user_has_unique_information
- interruption_cost
- redundancy_cost
- answerability_by_tools
```

## 24. Clarification actions

Possible decisions:

```text
ANSWER_DIRECTLY
INFER_LOW_RISK
SEARCH_LOCAL_CONTEXT
SEARCH_REPOSITORY
SEARCH_MEMORY
SEARCH_EXTERNAL_EVIDENCE
RUN_SAFE_PROBE
ASK_ONE_TARGETED_QUESTION
ASK_GROUPED_INDEPENDENT_QUESTIONS
DEFER_DECISION_AND_CONTINUE_SAFE_WORK
```

## 25. Ask the smallest useful question

When clarification is required, ask the minimum question that separates the consequential hypotheses.

Bad:

```text
“Peux-tu tout préciser ?”
```

Better:

```text
“Tu veux que cette règle s’applique uniquement au projet actuel ou à tous les projets ?”
```

## 26. Key Question Coverage

Clarification quality SHALL measure whether the question targets a genuinely missing decision-critical fact.

Metrics include:

```text
KeyQuestionCoverage
AverageTurnsToClarity
ClarificationRegret
UnnecessaryClarificationRate
RequiredClarificationMissRate
LateClarificationRate
RepeatedQuestionRate
```

## 27. Respect “continue / utilise ton jugement”

If the user explicitly delegates a choice or asks the system to continue without further questions, AlinaCoder SHALL stop re-asking low-impact ambiguities.

It MAY still ask when a newly discovered ambiguity is both:

```text
high-impact
AND not safely inferable/researchable
```

## 28. Clarification can occur late

Missing information discovered only after repository exploration MAY trigger clarification later in the trajectory.

Clarification is not restricted to the first turn.

## 29. Concrete test-as-question interaction

For coding ambiguity, AlinaCoder MAY surface a small executable example/test to clarify semantics.

Example:

```text
“Pour `merge()`, est-ce que ce cas doit produire A ou B ?”
```

with a compact test/example card.

This is often lower cognitive load than a long abstract question.

---

# Part VI — Correction and Repair Assimilation

## 30. CorrectionAssimilator

Every user correction SHALL be classified before it mutates state.

Classes:

```text
COMMAND_REVISION
FACTUAL_CORRECTION
REFERENCE_CORRECTION
SCOPE_NARROWING
SCOPE_EXTENSION
PRIORITY_CHANGE
CANCELLATION
PREFERENCE_UPDATE
DISAGREEMENT_WITHOUT_NEW_EVIDENCE
CONFIRMATION
```

## 31. User correction is authoritative for user intent

When the user says:

```text
“non je parlais du module X”
```

that correction is authoritative about intended referent unless impossible/inconsistent with safety constraints.

Dependent old plan branches SHALL be invalidated.

## 32. User disagreement is not automatically factual truth

When the user says:

```text
“non, ce fait est faux”
```

AlinaCoder SHALL re-check the evidence rather than reflexively switching to the opposite factual claim.

Distinguish:

```text
intent authority
from
external factual truth
```

## 33. Correction propagation

A correction SHALL propagate through:

```text
IntentBeam
GroundingState
ConstraintLedger
PlanDependencyFence
working context
affected memory candidates
pending actions
semantic transaction
conversation UI
```

## 34. Partial invalidation

Only dependent work SHALL be invalidated when possible.

Independent verified work SHOULD be preserved.

## 35. Correction latency target

For text turns, visible acknowledgment of a material correction SHOULD be immediate enough that the user can tell the system incorporated it before new risky actions occur.

For voice, barge-in/correction handling has stricter real-time rules later in this amendment.

---

# Part VII — Conversational Reference Grounding

## 36. ConversationalReferenceResolver

AlinaCoder SHALL resolve natural references such as:

```text
ça
celui-là
le fichier d’avant
la dernière erreur
ce qu’on avait décidé hier
le commit précédent
le deuxième truc
l’autre module
comme tout à l’heure
```

using multiple evidence channels.

## 37. Reference evidence channels

Required channels include:

```text
lexical recency
semantic similarity
temporal proximity
active goal membership
repository/project membership
current UI selection
recent tool/activity history
memory graph relations
conversation branch position
```

## 38. Reference binding

Resolved referents SHALL be represented explicitly:

```text
ReferenceBinding
- phrase_span
- candidate_entities
- selected_entity
- evidence
- confidence
- risk_if_wrong
- resolution_source
```

## 39. UI selection as high-value indexical context

If the user has selected a file, diff, goal card, plan step, error, message, or branch in `AlinaCoder.exe`, phrases like:

```text
“corrige ça”
“refais-le”
“garde celui-là”
```

SHOULD preferentially ground to the selected object when consistent with the turn.

## 40. Temporal retrieval

References to prior sessions SHALL combine lexical, semantic and temporal retrieval rather than relying only on embedding similarity.

## 41. Material uncertainty preview

When reference ambiguity is material but the likely candidate is strong, AlinaCoder MAY use a lightweight interpretation preview instead of a blocking modal.

Example UI:

```text
Cible comprise : src/router.py > Router.select_model()
[Changer]
```

Low-risk work MAY continue if policy allows; high-impact work waits for sufficient grounding.

---

# Part VIII — Repository-Grounded Intent Enrichment

## 42. RepositoryIntentEnricher

For coding requests that are vague because the user naturally assumes project context, AlinaCoder SHOULD inspect the repository before asking broad questions.

## 43. Read-before-ask principle

Examples:

```text
“corrige le bug de reprise”
→ inspect current failures, recent commits, recovery modules, roadmap

“fais pareil ici”
→ inspect selected file/diff and prior analogous implementation
```

## 44. Enriched problem statement

The system MAY synthesize an internal repository-grounded representation containing:

```text
likely affected components
reproduction evidence
current behavior
expected behavior
relevant conventions
likely scope
cross-file dependencies
candidate tests
unknowns still requiring user input
```

## 45. Original request remains authoritative

Repository enrichment is evidence, not permission to silently expand the user's request.

The original wording and active `ConstraintLedger` remain visible to the mediator.

## 46. Exploration budget

Intent enrichment SHALL use a bounded, targeted repository exploration rather than flooding context with unrelated files.

Escalate only when evidence remains insufficient.

---

# Part IX — User Communication Model and Personalized Ambiguity Adaptation

## 47. UserCommunicationModel

AlinaCoder MAY learn recurring, non-sensitive communication patterns that help interpret future requests with less friction.

Possible evidence-backed patterns:

```text
preferred response brevity
preferred language
common project terminology
habitual shorthand
recurrent omitted-but-stable coding convention
usual meaning of a project nickname
preferred explanation depth
common voice/code-switch pattern
preferred confirmation style
```

## 48. No sensitive inference

The user model SHALL NOT infer/store sensitive personal traits merely to improve conversation.

## 49. Evidence threshold

A one-off behavior SHALL NOT automatically become a persistent preference.

Persistent personalization requires repeated or explicit evidence.

## 50. Resolved-session learning

Prior sessions where an ambiguity was explicitly resolved MAY teach a recurring interpretation pattern.

Use only when:

```text
same user
same semantic pattern
sufficient repeated evidence
no current contradictory instruction
no stale/superseded evidence
```

## 51. HistoryGate

Before applying a learned ambiguity pattern, run a `HistoryGate`.

Output:

```text
USE_PRIOR_PATTERN
USE_AS_WEAK_PRIOR
INSUFFICIENT_HISTORY
CURRENT_TURN_OVERRIDES
CONTRADICTORY_HISTORY
```

## 52. Current explicit instruction always dominates personalization

A stored preference cannot override the user's current explicit command.

## 53. UserModelGraph

Store user communication preferences as evidence-linked graph nodes rather than unqualified flat facts.

Suggested edges:

```text
SUPPORTED_BY
CONTRADICTED_BY
SUPERSEDED_BY
APPLIES_TO_PROJECT
APPLIES_TO_MODALITY
VALID_DURING
```

## 54. PreferenceEvidenceGraph

Each learned preference SHALL retain:

```text
source turns/sessions
support count
contradiction count
confidence
scope
valid_from
valid_to
last_revalidated_at
```

---

# Part X — Conversation Memory and Intent-Aware Context Folding

## 55. ConversationEventLog

The complete local conversation/activity event log SHALL remain append-only/canonical enough to reconstruct semantic history.

Working prompts do not need the entire raw log.

## 56. IntentAwareContextCompiler

At each material turn, compile a compact working context conditioned on current intent.

Inputs:

```text
GroundingState
ConstraintLedger
active plan
recent high-fidelity turns
relevant tool evidence
relevant memory
relevant repository state
relevant semantic environment
```

## 57. Full history retained, working view compressed

Do not permanently discard information merely because it is omitted from the current prompt.

The canonical log remains available for retrieval/recompilation.

## 58. Dynamic context folding

Context folding SHALL track:

```text
current goals
how goals evolved
active constraints
superseded constraints
pending decisions
unresolved questions
important evidence
failed hypotheses
current todo list
```

instead of producing a generic prose summary.

## 59. Tool log extraction

Large tool outputs SHOULD be dynamically filtered to retain only fields relevant to active goals while preserving raw source pointers for later recovery.

## 60. Phase-shift refresh

When the task shifts phase, re-evaluate working memory.

Examples:

```text
research → implementation
implementation → debugging
debugging → verification
verification → packaging
conversation → recovery
```

Preserve stable goals/constraints; refresh phase-specific evidence.

## 61. ContextCapsule

Users MAY explicitly save selected conversation/context units as reusable `ContextCapsule`s.

Types MAY include:

```text
PROJECT_RULES
DECISION
STYLE
WORKFLOW
DEBUGGING_LESSON
REFERENCE_SET
```

Capsules require visible provenance and edit/delete controls.

## 62. Branch-aware context

Conversation branches SHALL inherit context up to their branch anchor by default while excluding sibling branch exploration unless explicitly merged.

## 63. No accidental sibling contamination

A rejected experimental branch SHALL not silently influence the mainline answer merely because it exists in session history.

---

# Part XI — Claims, Consistency and Calibrated Confidence

## 64. AssertionGraph

Important assistant claims SHALL be tracked as evidence-linked assertions.

Examples:

```text
“test X passes”
“main HEAD is SHA Y”
“module Z is unaffected”
“provider route is free”
```

Fields:

```text
assertion_id
claim
scope
supporting_evidence
contradicting_evidence
freshness
status
```

Statuses:

```text
SUPPORTED
WEAK
CONTRADICTED
STALE
SUPERSEDED
UNVERIFIED
```

## 65. Cross-turn consistency

Before repeating or relying on a material prior claim, re-check whether its evidence remains fresh.

## 66. Confidence is not authority

Raw model self-confidence SHALL NOT authorize action.

Confidence can route verification effort but not replace evidence.

## 67. User-facing uncertainty language

The ordinary UI SHOULD use understandable state descriptions instead of fake precision.

Examples:

```text
Compris
À vérifier
Ambiguïté importante
Preuve insuffisante
Bloqué par une décision
```

Avoid displaying uncalibrated percentages as if they were probabilities.

## 68. Self-correction policy

Self-correction SHALL be:

```text
targeted
verifier-driven
bounded
evidence-seeking
```

not endless self-reflection.

## 69. Correction after contradiction

When internal/external evidence contradicts a prior claim, update the `AssertionGraph`, explain the corrected conclusion succinctly, and propagate dependent invalidation.

---

# Part XII — Duplex Voice Conversation

## 70. Voice is a first-class interface

Voice SHALL not be implemented as “record whole sentence → transcribe → send as text” only.

The architecture SHOULD support incremental duplex interaction.

## 71. DuplexConversationController

Required high-level states:

```text
LISTENING
USER_SPEAKING
USER_PAUSED
POSSIBLE_COMPLETION
SEMANTICALLY_INCOMPLETE
THINKING
SYSTEM_SPEAKING
USER_BARGE_IN
BACKCHANNEL
SIDE_SPEECH
REPAIRING
INTERRUPTED
```

## 72. SpeechHypothesis

Incremental ASR output SHALL distinguish stable and unstable spans.

```text
SpeechHypothesis
- segment_id
- partial_text
- stable_prefix
- unstable_suffix
- token/segment confidence when available
- language spans
- timing
- acoustic quality
- completion_likelihood
```

## 73. No action from unstable speech alone

An unstable ASR suffix cannot authorize an irreversible or high-impact action.

## 74. Semantic endpointing

Turn completion SHOULD fuse:

```text
silence/acoustics
lexical completeness
syntactic completion
semantic completion
prosody where available
repair markers
conversation state
```

VAD silence alone is insufficient.

## 75. Barge-in

When the user begins a genuine interruption while AlinaCoder is speaking:

1. stop/duck TTS immediately;
2. preserve already emitted semantic output in the transcript;
3. capture the new user speech;
4. classify whether the interruption is:
   - correction;
   - cancellation;
   - new request;
   - backchannel;
   - side speech;
5. update the Repair Graph;
6. cancel or preserve backend work according to semantic dependency.

## 76. Backchannel detection

Short utterances such as:

```text
oui
mhm
ok
vas-y
je vois
```

SHALL not automatically become new standalone missions.

## 77. Side-speech protection

If speech appears directed to another person or is acoustically/semantically inconsistent with the active dialogue, classify as `SIDE_SPEECH` or uncertain rather than executing blindly.

## 78. Fast acknowledgment versus semantic commitment

AlinaCoder MAY emit low-risk early acknowledgments such as:

```text
“Oui.”
“D’accord.”
“Je vois.”
```

while deeper reasoning continues.

It SHALL NOT prematurely verbalize a high-impact conclusion that may change moments later.

## 79. Speculative backend work during speech

Safe operations MAY begin before final turn completion:

```text
local context prefetch
repository index lookup
memory retrieval
candidate reference resolution
provider readiness check
```

These speculative results are discardable.

No durable effect is allowed before stable intent/action admission.

---

# Part XIII — ASR Semantic Safety and French Robustness

## 80. ASR transcript is evidence, not truth

ASR systems can hallucinate plausible but unspoken content, especially under incomplete/noisy speech.

Therefore transcription SHALL carry uncertainty/provenance into semantic interpretation.

## 81. ASRSemanticRiskGate

Before acting from speech, estimate risk using at least:

```text
ASR uncertainty
× semantic impact of uncertain span
× action consequence/irreversibility
```

## 82. Critical speech slots

Uncertain spans involving critical fields deserve stronger handling:

```text
negations
file/path names
branch/repository names
numbers
commit SHAs
commands
URLs
package names
model/provider names
“supprime / ne supprime pas”
“commit / ne commit pas”
```

## 83. Confirmation strategy for critical slots

If a critical span is uncertain and materially changes execution, AlinaCoder SHALL:

```text
re-run/compare ASR
use contextual vocabulary biasing
inspect local candidates
or ask a concise confirmation
```

## 84. No hallucinated completion of truncated speech

If audio ends or is interrupted mid-command, AlinaCoder SHALL NOT fill in a plausible continuation and execute it.

## 85. French-first benchmark

AlinaCoder SHALL maintain an ASR and spoken-intent benchmark specifically for real French interaction.

Include:

```text
France French
regional accents where relevant
fast casual speech
hesitations
false starts
fillers
background noise
microphone variation
technical vocabulary
code and file names
French-English code-switching
```

## 86. Code-switching

French developers naturally embed English technical terms.

The ASR/understanding system SHALL preserve language spans rather than forcing the entire utterance into one language/script.

## 87. Semantic speech metrics

ASR route selection SHALL not rely only on Word Error Rate.

Track at least:

```text
WER/CER
semantic preservation error
critical-slot error rate
named-entity/path error rate
negation error rate
code-switch error rate
downstream intent error rate
latency
hallucination insertion rate
```

## 88. Per-condition ASR capability profile

There is no assumed universal best ASR engine.

Maintain route capability by condition:

```text
clean French
noisy French
French-English technical speech
long dictation
short commands
streaming partials
```

Select the strongest zero-cost eligible route for the current condition.

## 89. Local-first voice resilience

Basic voice interaction SHALL remain possible without mandatory cloud/Supabase dependency when a capable local route is available.

---

# Part XIV — Conversation-Aware Coding Maintenance

## 90. Every coding turn is an evolution step

A later coding request SHALL be treated as a patch to an evolving specification, not as an isolated prompt.

## 91. CrossTurnRegressionGate

After each material code change, verify that active requirements from earlier turns still hold.

## 92. LastKnownGoodConversationCheckpoint

Maintain a checkpoint coupling:

```text
code state
IntentContract version
ConstraintLedger version
test evidence
conversation state
```

## 93. Regression-triggered retry

If a new turn satisfies its new requirement but breaks previously validated requirements:

1. reject candidate promotion;
2. restore/compare against last known good candidate;
3. reapply the current requirement with explicit preserved constraints;
4. retest old + new behavior.

## 94. No code rollback to rejected state

A previously rejected/known-bad implementation SHALL not re-enter canonical state merely because a later model forgot the failure.

## 95. Turn-level preservation suite

Tests generated/validated during earlier turns become part of the active preservation suite until superseded or proven obsolete.

## 96. User-approved examples as executable intent

When the user validates an example/test, store it as a strong executable interpretation artifact linked to the constraint it clarifies.

---

# Part XV — Unified `AlinaCoder.exe` Product Shell

## 97. Single-shell principle

The intended normal workflow SHALL occur inside `AlinaCoder.exe`.

The app is not merely a chat window wrapping a CLI.

It is the canonical local human–AlinaCoder interaction shell.

## 98. Everyday capabilities inside the app

The `.exe` SHALL aim to contain:

```text
conversation
voice
projects/repositories
sessions/threads
intent and constraints
plans/tasks
repository browsing
file/diff inspection
tests/evidence
runtime activity
model/provider routing status
memory/context management
provider enrollment status
settings
permissions/approvals
logs/diagnostics
recovery/resume
```

## 99. External escape hatch

Only workflows that genuinely require another trusted surface MAY leave the app, for example:

```text
OS-native credential prompt
provider official OAuth/browser enrollment
external legal/terms page
```

After completion, AlinaCoder SHALL resume inside the `.exe` with continuity preserved.

## 100. Desktop architecture principle

The UI SHALL be a view/controller over canonical local state, not the canonical authority itself.

Closing/reopening the window SHALL not destroy task state.

---

# Part XVI — Primary Interface Layout

## 101. Three-panel default layout

Recommended primary layout:

```text
┌────────────────┬────────────────────────────────┬──────────────────────┐
│ Projects       │ Conversation                   │ Context / Work       │
│ Sessions       │                                │                      │
│ Threads        │ user + assistant turns         │ Intent               │
│                │ cards / diffs / tests          │ Constraints          │
│                │ voice transcript               │ Plan                 │
│                │ approvals / status             │ Files / Diff         │
│                │                                │ Tests / Evidence     │
│                │                                │ Activity             │
└────────────────┴────────────────────────────────┴──────────────────────┘
                         Composer / Voice / Stop
```

The right panel SHALL be collapsible so ordinary conversation can remain visually simple.

## 102. Left panel

Functions:

```text
project switch
session history
conversation branches
pinned sessions
search
recent activity
```

The active project shall be visually unambiguous.

## 103. Center conversation panel

Conversation remains the primary interaction surface.

It SHOULD support rich typed cards for:

```text
text answers
code snippets
diffs
test results
plans
clarification questions
intent previews
provider/model status
recovery summaries
action receipts
warnings
```

## 104. Right Context / Work panel

Tabs or sections SHOULD include:

```text
INTENT
CONSTRAINTS
PLAN
CONTEXT
FILES
DIFF
TESTS
EVIDENCE
ACTIVITY
MODEL
MEMORY
```

Progressive disclosure is mandatory: do not expose all detail at once.

## 105. Bottom composer

The composer SHOULD support:

```text
text input
microphone / push-to-talk or hands-free mode
file/image/log attachments
repo/file selection chips
command palette
send
stop/pause
```

## 106. Universal Stop

A prominent `STOP`/cancel affordance SHALL remain available while autonomous work is active.

Stopping speech output and stopping task execution are separate operations when useful.

## 107. Pause

`PAUSE` SHALL capture a durable checkpoint and stop new actions without losing context.

## 108. Takeover

The user SHALL be able to take over a plan step or task, make manual changes, then return control to AlinaCoder with those changes incorporated as new evidence.

---

# Part XVII — Visible Intent and Goal Tracking

## 109. Intent should be inspectable, not noisy

The UI SHOULD expose a concise interpretation when useful, not repeat every obvious user sentence.

Example:

```text
Compris : améliorer le routeur sans supprimer les fallbacks locaux.
```

with an edit/control affordance.

## 110. Goal cards

Active goals MAY appear as compact cards with states:

```text
ACTIVE
IN_PROGRESS
BLOCKED
NEEDS_USER
VERIFIED
COMPLETED
SUPERSEDED
CANCELLED
```

## 111. Goal provenance

Selecting a goal SHOULD reveal:

```text
source user phrase
current normalized goal
constraints
progress evidence
supersession history
```

## 112. User locks

The user MAY lock an important goal/constraint to signal that it must not be auto-merged away by future inferred goal consolidation.

Explicit later user corrections can still supersede it.

## 113. Progress is evidence-backed

A goal SHALL not be marked complete merely because the model says it is complete.

Completion is driven by its `DoneContract` and verification evidence.

## 114. Goal progression visualization

For long conversations, the interface MAY provide a timeline/tree showing:

```text
added
merged
replaced
completed
cancelled
```

goals over time.

This assists recovery from context drift without forcing the user to reread long transcripts.

---

# Part XVIII — Conversation Branches and Context Manipulation

## 115. Conversation is a tree, not only a log

Users SHALL be able to branch from an earlier turn without destroying the current path.

## 116. Branch operations

Supported concepts SHOULD include:

```text
BRANCH_FROM_HERE
RETURN_TO_MAINLINE
SET_MAINLINE
COMPARE_BRANCHES
MERGE_VERIFIED_RESULT
ARCHIVE_BRANCH
DELETE_LOCAL_BRANCH_CONTEXT
```

These are conversation/context branches, not necessarily Git branches.

## 117. Mainline isolation

Sibling branch exploratory conclusions are excluded from mainline reasoning until explicitly merged or cited as evidence.

## 118. Context include/exclude

Users MAY directly include/exclude conversation units from the active working context.

This operation creates structured context metadata; it does not silently erase the canonical event log.

## 119. Edit interpretation versus edit history

Users MAY correct an interpreted goal/constraint without rewriting the raw historical utterance.

The UI SHALL show that this is a semantic correction/supersession.

## 120. Undo last interpretation

Provide a first-class operation:

```text
UNDO_LAST_INTERPRETATION
```

This is different from:

```text
UNDO_CODE_CHANGE
GIT_ROLLBACK
UNDO_EXTERNAL_EFFECT
```

## 121. Search and locate

The context map/timeline SHOULD support search and direct navigation between:

```text
message
intent node
constraint
plan step
file change
test result
activity event
```

---

# Part XIX — Interactive Planning and Co-Execution

## 122. Plan cards

Long-running work SHALL have an inspectable plan representation when a plan materially improves steerability.

Plan step states:

```text
PENDING
READY
RUNNING
WAITING_FOR_USER
BLOCKED
VERIFYING
DONE
FAILED
CANCELLED
SUPERSEDED
```

## 123. Editable plan

The user SHALL be able to:

```text
edit step
reorder safe-independent steps
add step
remove step
pause step
assign step to self
return step to AlinaCoder
```

Changes update the PlanDependencyFence and GroundingState.

## 124. Co-planning and co-execution

Planning and execution MAY interleave.

Execution discoveries can legitimately revise later plan steps while preserving the user's active goal.

## 125. Scoped steering actions

On visible objects, offer actions such as:

```text
FOCUS
IGNORE
ELABORATE
RETRY
VERIFY
COMPARE
STOP
```

These create explicit structured steering events.

## 126. Direct manipulation is conversation

A click/edit/selection that changes intent or task state SHALL enter the `ConversationEventLog` as a semantic user action.

Natural language is not the only conversational modality.

---

# Part XX — Diff, Tests and Evidence Inside the Conversation

## 127. Code evidence cards

When coding, the chat SHOULD surface compact cards rather than dumping giant logs.

Example:

```text
3 fichiers modifiés
12 tests passés
0 régression détectée
[Voir le diff] [Voir les tests]
```

## 128. Progressive disclosure

Default:

```text
summary
→ expanded evidence
→ raw tool output
```

The user should not need to read raw logs unless desired.

## 129. Diff interaction

The user MAY select lines/hunks/files and speak/type commands referring to them.

Those selections become high-confidence referents.

## 130. Test-driven clarification card

When a generated test is used to clarify intent, display it in a readable semantic form first, with code detail expandable.

## 131. No raw private chain-of-thought

The interface SHALL NOT expose private model chain-of-thought.

It MAY expose:

```text
intent
plan
assumptions
constraints
evidence
predictions
verification results
action summaries
short decision rationale
```

This provides useful transparency without pretending raw hidden reasoning is a reliable audit surface.

---

# Part XXI — Activity, Oversight and Rapid Resumption

## 132. ActivityTimeline

Maintain an append-only user-visible activity timeline for material actions.

Examples:

```text
read file
searched repo
ran test
created candidate patch
changed model host
recovered from failure
committed SHA
```

## 133. Foreground versus background communication

When the user is actively watching, provide richer progress context.

When the app is backgrounded, provide only low-distraction status signals and actionable alerts.

## 134. Ambient state

Optional compact status states:

```text
THINKING
CODING
TESTING
WAITING
BLOCKED
DONE
RECOVERING
```

No fake progress percentages unless based on a real bounded plan.

## 135. Rapid resumption summary

When the user returns after autonomous work, show:

```text
what changed
what is verified
what failed
what remains
whether anything needs user input
resume point
```

## 136. Key-action replay

For GUI-heavy or long-running tasks, the UI MAY provide a lightweight replay/timeline of important state changes rather than forcing transcript reconstruction.

## 137. Error traceability

If AlinaCoder gets stuck or recovers from a soft error, the user SHOULD be able to locate the relevant action/evidence quickly.

---

# Part XXII — Model/Provider Switching Without Conversation Breakage

## 138. Provider switching is implementation detail by default

Ordinary users should not need to manage model changes manually.

## 139. Small status, deep diagnostics

Default conversation UI MAY show:

```text
Moteur : Nemotron 3 Ultra — gratuit vérifié
État : stable
```

Detailed route evidence belongs in diagnostics.

## 140. Conversation continuity across switch

Before a cognitive model switch, persist:

```text
GroundingState
IntentContract
ConstraintLedger
AssertionGraph
active plan
current branch
working context digest
recent raw turns
unresolved ambiguities
last user correction
```

## 141. Post-switch understanding proof

The target model SHALL reconstruct the active task from canonical state and pass a machine-checkable `ContinuityProof` before receiving effect authority.

The user SHALL NOT need to re-explain the conversation.

## 142. Host failover should be invisible

Same-lineage provider failover SHOULD not disrupt speech or conversation beyond unavoidable latency.

## 143. Cognitive switch should preserve voice state

If a model family changes while voice is active, the duplex controller remains a stable outer layer so turn-taking behavior does not reset with the model.

---

# Part XXIII — Conversation Latency and Performance

## 144. ConversationLatencyBudget

Track latency as multiple user-perceived stages:

```text
speech_to_stable_partial
end_of_turn_detection
turn_to_grounding
turn_to_first_safe_visual_response
turn_to_first_safe_audio_response
turn_to_useful_answer
turn_to_action_start
barge_in_to_tts_stop
correction_to_state_update
failure_to_recovery_signal
```

## 145. Optimize latency without semantic recklessness

Fast is valuable only if early output is safe to revise.

Do not trade semantic correctness for premature commitment.

## 146. Parallel prefetch

During interpretation, run independent low-risk operations concurrently when useful:

```text
memory retrieval
repo symbol lookup
active-file lookup
provider health check
context compilation
```

## 147. Lightweight mediator routes

Obvious low-risk turns MAY use a fast local/lightweight mediator only after benchmark evidence proves sufficient conversational fidelity.

Escalate ambiguity/complexity to stronger routes.

## 148. Caching

Cache only semantically safe reusable layers.

Cache keys SHALL include material environment/context versions when required.

## 149. Async folding

Conversation/context folding MAY run after each turn or during idle time so it does not block the next user input.

The canonical raw event log remains available if folding fails.

---

# Part XXIV — Optional Supabase Role

## 150. Supabase remains optional

No part of basic conversation, voice, memory, routing, or coding requires Supabase.

## 151. Optional memory mirror

If enabled, Supabase MAY mirror non-secret structured conversation-memory metadata using:

```text
Postgres FTS / tsvector
pgvector
Reciprocal Rank Fusion
RLS
```

Local canonical state remains authoritative.

## 152. Optional Realtime UI sync

Supabase Realtime Broadcast MAY synchronize ephemeral status across trusted app clients when explicitly configured.

Examples:

```text
plan status
presence
activity summary
non-secret progress events
```

## 153. Broadcast is not canonical authority

Realtime messages are delivery/UX events, not authoritative task state.

## 154. Private channels

Any optional cloud conversation/activity sync SHALL use authenticated private channels and appropriate RLS.

## 155. ACK semantics

A Realtime Broadcast ACK proves server receipt, not successful execution of the semantic action represented by the message.

## 156. Replay semantics

Replay can help UI resumption, but canonical local history remains the source of truth.

---

# Part XXV — Continuous Conversation Quality Lab

## 157. ConversationQualityLab

AlinaCoder SHALL continuously improve conversational behavior using local, privacy-aware evaluation artifacts.

## 158. Interaction signals

Useful local signals include:

```text
user correction
user rephrase
“non” / “attends” repair
undo interpretation
branch abandonment
plan edit
plan rejection
clarification response
repeated question
user interruption
scope correction
wrong-reference correction
code rollback
must/must-not violation
unsupported progress claim
successful first-turn completion
```

## 159. ConversationFailureCard

Normalize significant failures into:

```text
ConversationFailureCard
- failure_type
- raw_user_turn_ref
- interpreted_intent
- correct_intent_if_known
- missing_constraint
- wrong_referent
- clarification_decision
- memory_used
- route/model
- resulting_cost
- correction_turns
- repair_success
- reusable_lesson
```

## 160. Privacy

Raw private conversations SHALL NOT be sent to remote training/evaluation services merely to improve AlinaCoder without explicit user authorization.

## 161. Replay lab

Failure cards MAY be replayed offline/read-only against:

```text
current mediator
challenger mediator
new model routes
new clarification policy
new ASR routes
new context compiler
new memory retrieval policy
```

## 162. Hidden conversational holdout

Promotion SHALL use held-out scenarios so the system does not merely memorize known conversation failures.

## 163. Fresh conversation canaries

Continuously generate fresh paraphrases and multi-turn variants from validated intent specifications.

## 164. Metamorphic conversation tests

Equivalent meaning expressed differently SHOULD preserve the same intent.

Transformations include:

```text
formal French ↔ casual French
punctuated ↔ unpunctuated
clean ↔ typo-heavy
single sentence ↔ fragmented turns
explicit nouns ↔ natural pronouns with context
French ↔ French-English technical code-switch
voice-like fillers inserted
order-preserving paraphrase
```

## 165. Negative metamorphic tests

Small meaning changes that matter SHALL change the contract.

Examples:

```text
“supprime” vs “ne supprime pas”
“uniquement ce fichier” vs “tout le dossier”
“commit” vs “ne commit pas encore”
```

---

# Part XXVI — Spec Evolution Audit Loop

## 166. SpecEvolutionCandidate

Research findings SHALL not enter the normative spec automatically.

Each finding becomes a candidate:

```text
finding_id
source
source_quality
claim
novelty_vs_current_spec
contradictions
engineering_value
testability
safety_fit
zero_cost_fit
implementation_cost
status
```

## 167. Candidate statuses

```text
DISCOVERED
DUPLICATE
WEAK_EVIDENCE
PROMISING
BENCHMARK_REQUIRED
ACCEPTED_FOR_SPEC
REJECTED
WATCH
```

## 168. Audit pipeline

```text
research
→ source quality check
→ compare with existing spec
→ deduplicate
→ identify contradiction
→ derive testable mechanism
→ assess safety/latency/resource implications
→ acceptance scenario
→ normative integration
```

## 169. Prefer mechanisms over slogans

Do not integrate claims such as:

```text
“use empathy”
“be smarter”
“use more context”
```

unless translated into observable behavior and tests.

## 170. Research does not self-authorize code

The runtime MAY propose spec improvements in the future, but normative public-spec changes still require the user-authorized project governance path.

## 171. Preserve rejected findings

Important rejected/Watch findings SHOULD retain a concise audit reason so later research does not repeatedly reintroduce them without new evidence.

---

# Part XXVII — Conversational Benchmarks

## 172. Conversational coding benchmark suite

AlinaCoder SHALL evaluate not only static coding success but interactive collaboration.

Include categories inspired by current research such as:

```text
underspecified coding tasks
missing goals
missing premises
ambiguous terminology
multi-round user refinement
mid-course corrections
constraint accumulation
reference resolution
cross-session personalized ambiguity
novice/intermediate/expert communication styles
```

## 173. Correction burden metric

Track:

```text
CorrectiveFeedbackTurnsPerSuccessfulTask
```

Lower is better, subject to maintaining task correctness.

## 174. First-turn alignment

Track success when enough information was already available without asking unnecessary questions.

## 175. Collaboration efficiency

Metrics SHALL include both:

```text
final repository correctness
interaction effort
```

## 176. User-stratified communication

Benchmark different communication styles rather than assuming every user writes like an expert software specification.

## 177. No benchmark overfitting

Conversational benchmarks follow the evaluation-integrity and contamination rules from the semantic-transactions/evaluation-integrity amendment.

---

# Part XXVIII — Core Metrics

## 178. Grounded Intent Accuracy

Does the selected `GroundedIntentContract` match the verified intended task?

## 179. Critical Constraint Recall

Fraction of active critical constraints represented and enforced.

## 180. Prohibition Violation Rate

For machine-checkable prohibitions, target:

```text
0
```

## 181. Reference Resolution Accuracy

Correct resolution of pronouns, temporal references, selected UI objects and historical referents.

## 182. Repair Success Rate

How often a correction/revision successfully updates all affected state without stale intent surviving.

## 183. Clarification metrics

```text
UnnecessaryClarificationRate
RequiredClarificationMissRate
AverageTurnsToClarity
ClarificationRegret
RepeatedQuestionRate
```

## 184. Intervention metrics

```text
user corrections per successful task
user stop/undo events
plan rejection count
manual takeover count
```

These are not inherently failures; interpret them with outcome/context.

## 185. Cross-turn adherence

```text
MustDoOmissionRate
MustNotViolationRate
CrossTurnRegressionRate
CrossTurnInconsistencyRate
```

## 186. Memory metrics

```text
StaleMemoryUseRate
WrongPersonalizationRate
UsefulPriorPatternRate
MemoryCorrectionPropagationRate
```

## 187. Voice metrics

```text
CriticalSlotASRErrorRate
SemanticActionErrorRate
ASRHallucinationRate
BargeInStopLatency
FalseEndpointRate
MissedEndpointRate
BackchannelMisclassificationRate
CodeSwitchSemanticErrorRate
```

## 188. Interface metrics

```text
TimeToLocatePriorDecision
TimeToCorrectMisinterpretation
ContextBranchRecoverySuccess
UserRetypingBurden
ProgressClaimAccuracy
TaskResumptionTime
```

## 189. Continuity metrics

```text
FailoverIntentRetention
FailoverConstraintRetention
FailoverReferenceRetention
UserReExplanationRequiredRate
```

Target for user re-explanation due solely to model/provider failover:

```text
0
```

---

# Part XXIX — Acceptance Scenarios

## 190. Natural French understanding

1. A casual typo-heavy French request SHALL yield the same material intent as its clean equivalent.
2. Missing punctuation SHALL not materially alter clear constraint scope.
3. Fillers such as `euh`, repetitions and false starts SHALL not become duplicate goals.
4. `non attends` SHALL reopen and repair the current turn.
5. A late `mais garde X` SHALL preserve X while revising the targeted portion.

## 191. Negation and scope

6. `ne supprime aucun fichier` SHALL create a machine-visible prohibition.
7. Later instructions unrelated to deletion SHALL not remove that prohibition.
8. `en fait tu peux supprimer uniquement temp.json` SHALL narrow/override only the relevant scope.
9. A model output proposing another deletion SHALL fail the compliance gate.

## 192. Pronouns and references

10. `corrige ça` with a selected failing test SHALL bind to that test/context.
11. `le fichier d’avant` SHALL use conversation/activity chronology.
12. `comme hier` SHALL retrieve temporal project context rather than global semantic nearest-neighbor only.
13. Material unresolved reference ambiguity SHALL trigger preview/clarification rather than a high-impact guess.

## 193. User corrections

14. `non je parlais de router.py` SHALL invalidate wrong-file work before commit.
15. Independent verified work SHALL survive when dependency analysis proves it unaffected.
16. `tu as tort` on a factual claim SHALL trigger evidence re-check, not automatic factual reversal.
17. A corrected constraint SHALL supersede stale personalized memory immediately.

## 194. Clarification

18. A missing installed package version SHALL be resolved from environment before asking the user.
19. A decision-critical aesthetic/product preference with no prior evidence MAY trigger one targeted question.
20. Independent missing preferences MAY be grouped in one concise turn.
21. Dependent decisions SHALL be asked in logical order.
22. After `utilise ton jugement`, repeated low-impact clarification SHALL be considered a failure.
23. A high-impact ambiguity discovered after code exploration MAY still trigger a late clarification.

## 195. Constraint accumulation

24. After 20 turns, an early active MUST_NOT constraint SHALL still be enforced.
25. An early requirement explicitly superseded at turn 15 SHALL no longer constrain turn 20.
26. A newly added feature SHALL not break earlier validated behavior.
27. A regression SHALL trigger the CrossTurnRegressionGate and repair from a known-good checkpoint.

## 196. Personalization

28. One isolated shorthand use SHALL not become a permanent preference.
29. Repeated resolved use of the same project nickname MAY create a scoped pattern.
30. Current explicit wording SHALL override the stored nickname mapping if they conflict.
31. Contradictory prior sessions SHALL weaken the HistoryGate rather than force an inference.

## 197. Context folding

32. A long conversation SHALL keep exact active prohibitions even after history folding.
33. Superseded constraints SHALL remain auditable but excluded from active prompt authority.
34. An omitted raw tool field SHALL remain recoverable from the canonical source pointer.
35. A phase shift from research to implementation SHALL refresh irrelevant working memory without losing goals.

## 198. Conversation branching

36. A branch exploring solution B SHALL not pollute mainline solution A until merged.
37. User SHALL be able to return to an earlier branch without losing its local context.
38. `UNDO_LAST_INTERPRETATION` SHALL not modify Git state.
39. Deleting a visual branch SHALL not falsify the immutable activity/audit history required for recovery.

## 199. Voice

40. Mid-sentence pause after `je veux que tu…` SHALL not mark semantic completion.
41. User barge-in SHALL stop TTS promptly.
42. `mhm` during system speech SHALL be classified as a possible backchannel, not automatically cancel the task.
43. Uncertain `ne supprime pas` SHALL never become `supprime` through transcript normalization.
44. Truncated `committe et…` audio SHALL not automatically commit.
45. French speech containing `router`, `commit`, `fallback`, file names and model IDs SHALL preserve technical terms as well as practical ASR allows.
46. Noisy speech with low critical-slot confidence SHALL request/derive confirmation before effect.

## 200. Provider failover

47. Same-lineage host failover SHALL not require user re-explanation.
48. Cognitive model switch SHALL preserve active goals, prohibitions and last correction.
49. A target model failing ContinuityProof SHALL not receive mutation authority.
50. Voice turn state SHALL survive model routing changes at the outer controller layer.

## 201. UI

51. User SHALL be able to see active project/session at a glance.
52. User SHALL be able to inspect/edit active goal without scrolling the full transcript.
53. User SHALL be able to locate the source phrase of a constraint.
54. User SHALL be able to stop autonomous work from the main window.
55. User SHALL be able to inspect changed files and verification evidence inside the app.
56. Routine use SHALL not require opening a terminal.
57. Provider status SHALL be visible without dominating the conversation.
58. Raw secrets SHALL never be rendered in normal conversation/activity views.
59. Long logs SHALL default to summaries with progressive disclosure.
60. The right context panel SHALL be collapsible.

## 202. Progress truthfulness

61. A plan step SHALL not show DONE without its verification contract.
62. A failed hidden test SHALL prevent “terminé” even if visible tests pass.
63. A background recovery SHALL explain what was preserved and where execution resumed.
64. A model/provider switch SHALL not be misreported as restarting the user task from zero.

---

# Part XXX — Adversarial French Conversation Suite

## 203. Required stress patterns

Include test cases with:

```text
typos
missing accents
missing punctuation
slang
spoken fillers
self-corrections
nested negation
pronouns
ambiguous “ça”
multiple simultaneous goals
reordering
cancellation
partial cancellation
scope changes
quoted logs mixed with commands
code snippets mixed with prose
English technical terms
file/path names
numbers and SHAs
sarcastic wording where factual command remains explicit
interruptions
unfinished speech
```

## 204. Quoted-text boundary

A pasted log containing phrases such as:

```text
DELETE ALL FILES
```

SHALL not become a user command merely because it appears in input text.

The mediator SHALL distinguish quoted/artifact content from instruction content.

## 205. Example versus instruction

Text introduced as an example SHALL be classified `EXAMPLE_NOT_REQUIREMENT` unless context proves otherwise.

## 206. Multi-command repair

Input:

```text
“fais A puis B… non finalement pas B, fais C avant A mais garde la vérification de B”
```

SHALL produce an explicit dependency/reorder/cancel/preserve structure rather than a flattened sentence.

---

# Part XXXI — Conceptual Modules

## 207. Conversation modules

```text
src/alinacoder/conversation/
  intent_mediator.py
  grounding_state.py
  constraint_ledger.py
  ambiguity_classifier.py
  clarification_policy.py
  correction_assimilator.py
  reference_resolver.py
  interaction_smell.py
  assertion_graph.py
  conversation_event_log.py
  intent_context_compiler.py
  user_communication_model.py
  preference_evidence_graph.py
```

## 208. Voice modules

```text
src/alinacoder/voice/
  duplex_controller.py
  streaming_asr.py
  semantic_endpointing.py
  barge_in.py
  backchannel_classifier.py
  side_speech.py
  asr_semantic_risk.py
  french_voice_bench.py
  tts_controller.py
```

## 209. UI modules

Conceptual desktop components:

```text
src/alinacoder/ui/
  app_shell.py
  project_sidebar.py
  conversation_view.py
  context_work_panel.py
  composer.py
  goal_view.py
  constraint_view.py
  plan_view.py
  context_tree.py
  diff_view.py
  test_evidence_view.py
  activity_timeline.py
  model_status.py
  voice_status.py
  recovery_view.py
```

Exact framework choice is deferred to implementation planning and machine/runtime compatibility analysis.

## 210. Evaluation modules

```text
src/alinacoder/evaluation/
  conversation_grounding_bench.py
  clarification_bench.py
  reference_resolution_bench.py
  correction_bench.py
  cross_turn_constraint_bench.py
  conversational_coding_bench.py
  user_pattern_bench.py
  french_noise_bench.py
  voice_turn_bench.py
  failover_conversation_bench.py
  ui_resumption_bench.py
```

## 211. Self-improvement modules

```text
src/alinacoder/self_improvement/
  conversation_failure_card.py
  conversation_replay_lab.py
  interaction_smell_miner.py
  spec_evolution_candidate.py
  research_audit.py
```

---

# Part XXXII — Research Audit: Integrated Findings

## 212. Clarification research retained

Integrated because multiple 2026 lines of work converge on:

- distinguishing ambiguity/underspecification from model uncertainty;
- asking only high-value questions;
- measuring clarification efficiency, not just willingness to ask;
- supporting clarification throughout a task trajectory;
- structuring dependent clarification questions logically.

Relevant sources include:

- ClarEval (2026): clarification efficiency for code agents;
- uncertainty-aware software-engineering agents (2026);
- Prism (2026): dependency-aware intent clarification;
- recent structured uncertainty / value-of-information clarification research.

## 213. Interactive coding research retained

Integrated because real coding sessions are iterative and corrective.

Sources include:

- SWE-Together (2026): repository correctness + corrective feedback turns;
- Talk2Code (AAAI 2026): user-stratified multi-turn coding interaction;
- CAPA (2026): cross-session personalized ambiguity adaptation;
- CodeScout (ACL Findings 2026): repository-grounded query refinement;
- interaction-smell research (2026);
- regression accumulation in multi-turn programming (2026);
- TICODER: executable tests as intent-disambiguation artifacts.

## 214. Memory/context research retained

Integrated concepts:

- dynamic intent-aware context folding;
- full-history retention plus compact working view;
- evidence-backed user preferences;
- temporal supersession and forgetting;
- working-memory refresh after task phase shifts.

Relevant recent systems include U-Fold, HyMEM and temporal/personalized memory research.

## 215. Voice research retained

Integrated concepts:

- full-duplex/overlap-aware turn taking;
- barge-in;
- semantic endpointing instead of VAD-only completion;
- ASR uncertainty propagation;
- real-world/noisy/code-switched speech evaluation;
- semantic downstream metrics beyond WER.

Recent evidence includes WildASR (2026), French/accent corpora such as CEREALES, code-switching benchmarks including French-English, and multilingual ASR evaluations.

## 216. HCI/interface research retained

Integrated concepts:

- visible/editable goal tracking;
- branching context;
- mixed-initiative context manipulation;
- interactive plans/co-execution;
- rapid resumption and activity awareness;
- progressive disclosure.

Relevant systems include:

- OnGoal (UIST 2025);
- Conversation Progress Guide (2025);
- Contextify / Mixed-Initiative Context (2026);
- Branchat (CHI 2026);
- Cocoa;
- DuetUI;
- AdaLens (2026);
- Sidekick (2026).

## 217. Supabase findings retained narrowly

Official Supabase documentation supports optional:

- hybrid lexical + vector retrieval with rank fusion;
- authenticated private Realtime Broadcast;
- low-latency UI/status synchronization;
- replay for some Broadcast-from-database events.

These remain optional mirrors/transport mechanisms, not canonical conversation authority.

---

# Part XXXIII — Research Audit: Rejected or Restricted Findings

## 218. Rejected: “more memory always improves understanding”

Reason:

More raw history can introduce stale facts, distraction and intent drift.

Replacement:

```text
full canonical history
+ intent-aware retrieval/folding
+ temporal validity
```

## 219. Rejected: “ask whenever uncertain”

Reason:

It produces inefficient interrogators and high user cognitive load.

Replacement:

```text
value-of-information clarification
+ autonomous evidence acquisition first
```

## 220. Rejected: “never ask because autonomy”

Reason:

High-impact missing user-only information cannot always be inferred safely.

Replacement:

Selective clarification only when necessary.

## 221. Rejected: “user correction is always factual truth”

Reason:

User intent authority and external factual truth are different.

Replacement:

Corrections to intent are authoritative; factual disagreement triggers evidence review.

## 222. Rejected: raw model confidence as a decision gate

Reason:

Self-confidence is not reliably calibrated.

Replacement:

Separate uncertainty dimensions + evidence + deterministic gates.

## 223. Rejected: VAD-only voice endpointing

Reason:

Silence does not equal semantic completion; natural speech contains pauses and repairs.

Replacement:

Acoustic + lexical + semantic + prosodic endpointing.

## 224. Rejected: transcript-as-ground-truth

Reason:

Real-world ASR can hallucinate plausible unspoken content.

Replacement:

RAW audio/ASR evidence + semantic-risk gate + critical-slot checks.

## 225. Rejected: one universal ASR winner

Reason:

Performance changes by language, accent, noise, code-switching and latency need.

Replacement:

Per-condition capability calibration and zero-cost routing.

## 226. Rejected: faster always means better conversation

Reason:

Premature semantic commitment creates retractions/misactions.

Replacement:

Fast safe acknowledgments + delayed material commitment.

## 227. Rejected: linear transcript as the only session model

Reason:

Long work benefits from revisitation, branching and explicit context scoping.

Replacement:

Simple linear center view + optional structural tree/context map.

## 228. Rejected: expose raw chain-of-thought for transparency

Reason:

Raw hidden reasoning is not the appropriate audit/control surface.

Replacement:

Expose intent, plan, evidence, constraints, actions, predictions and verification.

## 229. Rejected: mandatory always-visible complexity

Reason:

A power-user cockpit can become cognitively expensive.

Replacement:

Progressive disclosure; right panel collapsible; ordinary chat remains simple.

## 230. Rejected: Supabase as required conversation backend

Reason:

Violates local-first/offline resilience and introduces unnecessary dependency.

Replacement:

Optional authenticated mirror/sync only.

## 231. Rejected: conversation branch equals Git branch

Reason:

The user requires canonical Git development on `main`, while conversational exploration still benefits from context branches.

Replacement:

Conversation/context branch is a semantic/session object, not a Git branch.

## 232. Rejected: perfect-understanding marketing claim

Reason:

Not falsifiable or honest.

Replacement:

Measurable intent-fidelity targets, adversarial benchmarks, safe residual ambiguity handling and repair.

---

# Part XXXIV — Source Ledger

## 233. Primary/research sources consulted in this research pass

The research audit included, among others:

```text
SWE-Together: Evaluating Coding Agents in Interactive User Sessions (2026)
https://arxiv.org/html/2606.29957

ClarEval: Clarification Skills of Code Agents under Ambiguous Instructions (2026)
https://arxiv.org/html/2603.00187

Fewer Clarifications, Better Code / CAPA (2026)
https://arxiv.org/html/2607.26611

How Coding Agents Fail Their Users (2026)
https://arxiv.org/html/2605.29442

Regression Accumulation in Multi-Turn LLM Programming Conversations (2026)
https://arxiv.org/html/2607.01855

IntentCoding / Intent-Amplified Code Generation (ACL Findings 2026)
https://aclanthology.org/2026.findings-acl.1662/

CodeScout (ACL Findings 2026)
https://aclanthology.org/2026.findings-acl.2032.pdf

Talk2Code (AAAI 2026)
https://ojs.aaai.org/index.php/AAAI/article/view/40730

OnGoal (UIST 2025)
https://doi.org/10.1145/3746059.3747746

Branchat (CHI 2026)
https://doi.org/10.1145/3772363.3798792

Mixed-Initiative Context / Contextify (2026)
https://arxiv.org/pdf/2604.07121

AdaLens (2026)
https://arxiv.org/html/2608.17834

U-Fold (ACL Findings 2026)
https://aclanthology.org/2026.findings-acl.897.pdf

Hybrid Self-evolving Structured Memory / HyMEM (ACL Findings 2026)
https://aclanthology.org/2026.findings-acl.549.pdf

WildASR (2026)
https://arxiv.org/html/2603.25727

CEREALES — Quebec French accented speech (Interspeech 2025)
https://www.isca-archive.org/interspeech_2025/maison25_interspeech.pdf

Open ASR Leaderboard (2025/2026)
https://arxiv.org/html/2510.06961

Pantagruel French text/speech encoders (2026)
https://arxiv.org/html/2601.05911
```

Official Supabase documentation and changelog were also consulted for optional hybrid retrieval and Realtime behavior.

## 234. Source quality rule

No single paper or prototype becomes normative merely because it reports an improvement.

The spec integrates mechanisms only when they are:

```text
relevant to AlinaCoder
compatible with project invariants
testable
not contradicted by stronger evidence
implementable without violating zero-cost/safety policy
```

---

# Part XXXV — Canonical Conversational Loop

## 235. Text/mixed input loop

```text
User turn / UI action
→ RawTurn
→ Repair Graph
→ ReferenceResolver
→ AmbiguityClassifier
→ Intent Beam
→ GroundingState
→ ConstraintLedger update
→ HistoryGate / user-model prior if useful
→ repository/context enrichment if useful
→ information sufficiency
→ Ask / Infer / Retrieve / Research / Probe
→ GroundedIntentContract
→ ContextCompiler
→ route strongest eligible zero-cost intelligence
→ candidate response/plan/action
→ InteractionSmellDetector
→ ConstraintComplianceGate
→ semantic transaction / execution
→ verification
→ AssertionGraph update
→ progress/evidence UI
→ ConversationEventLog
→ ConversationQualityLab signal
```

## 236. Voice loop

```text
microphone stream
→ acoustic/VAD evidence
→ streaming ASR hypotheses
→ language/code-switch spans
→ RAW speech record
→ semantic endpointing
→ Repair Graph
→ critical-slot ASR risk
→ ReferenceResolver
→ Intent Beam
→ GroundedIntentContract
→ safe early response if possible
→ deeper reasoning/execution
→ TTS stream
↘ user barge-in at any time
   → stop TTS
   → classify repair/backchannel/cancel/new request
   → update active contract
```

## 237. Correction loop

```text
user correction
→ CorrectionAssimilator
→ update Repair Graph
→ update GroundingState
→ supersede affected constraints
→ invalidate dependent plan branches
→ cancel stale speculative effects
→ preserve independent verified work
→ recompile context
→ resume from valid checkpoint
```

## 238. Long-session loop

```text
full event log retained locally
→ intent-aware fold after each turn/phase
→ active constraints pinned
→ stale memory filtered
→ user model used only as evidence prior
→ context branches isolated
→ current working context stays compact
```

---

# Part XXXVI — Final Product Target

## 239. Desired lived experience

```text
Open AlinaCoder.exe
→ speak or type ordinary French
→ use shorthand, corrections, pauses and technical English naturally
→ AlinaCoder understands the active project and references
→ it researches the repo instead of asking obvious questions
→ it asks only when your answer genuinely changes an important decision
→ it visibly preserves your MUST / MUST_NOT constraints
→ you can correct its interpretation in one click or one phrase
→ voice can be interrupted naturally
→ goals, plan, changes and tests are inspectable without leaving the app
→ the model/provider may change invisibly without losing the thread
→ earlier validated requirements do not disappear after later turns
→ progress claims correspond to real evidence
→ every misunderstanding becomes training/evaluation evidence for the local quality lab
→ the next interaction becomes measurably better without silently changing your authority
```

## 240. Final invariant

The system's conversational contract is:

> **Never make the user repeatedly reconstruct context that AlinaCoder can recover; never let a model’s guess silently outrank the user’s active intent; never let personalization override a current instruction; never turn uncertain speech into a dangerous action; and never call a task complete until the implementation and conversation contracts are both satisfied.**

## 241. Product objective

The unified target for AlinaCoder v0.2 becomes:

> **Maximum verified intelligence + maximum human-intent fidelity + minimum conversational friction + seamless zero-cost model continuity + local-first control, all through one coherent AlinaCoder.exe interface.**
