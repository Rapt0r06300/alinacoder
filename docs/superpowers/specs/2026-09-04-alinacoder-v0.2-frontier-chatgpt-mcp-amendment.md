# AlinaCoder v0.2 — Frontier Intelligence, ChatGPT MCP Bridge & Zero-Config Connection Amendment

Date: 2026-09-04  
Status: **APPROVED — NORMATIVE V0.2 EXTENSION**  
Repository: `Rapt0r06300/alinacoder`  
Canonical branch: `main` only

## 1. Normative status

This amendment extends the reopened AlinaCoder v0.2 specification following explicit user approval.

It is normative together with:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-cognitive-intelligence-amendment.md`

Where this amendment defines stricter behavior for frontier reasoning, ChatGPT integration, model orchestration, external consultation or connection UX, this amendment wins for those subsystems.

All prior reliability invariants remain authoritative unless explicitly strengthened here:

- deterministic evidence outranks model claims;
- verification outranks confidence;
- direct Git work remains on `main` only;
- no autonomous feature-branch/PR workflow is introduced;
- local operation remains available even when ChatGPT is unavailable;
- Ollama remains the local LLM provider;
- hidden benchmark assets remain outside the public repository and outside candidate-visible workspaces;
- resource limits and checkpoint-only local model switching remain enforced;
- no cloud dependency may become required for AlinaCoder to start, inspect a repository, diagnose itself or recover local state;
- no external model may bypass AlinaCoder's safety, verification, resource, repository or commit gates.

This amendment adds a second operating plane:

```text
LOCAL INTELLIGENCE PLANE
Ollama + deterministic tools + memory + repository intelligence + verification

FRONTIER INTELLIGENCE PLANE
ChatGPT conversation surface + AlinaCoder MCP tools + local deterministic verification
```

The product goal is not to pretend that a smaller local model has the intrinsic capability of a frontier model.

The goal is:

> **Make the AlinaCoder system as capable as possible by combining frontier reasoning when available with local project truth, deterministic tools, persistent memory, adversarial verification and safe execution.**

---

# Part I — Frontier Intelligence Architecture

## 2. Frontier intelligence is a system capability, not a single model

AlinaCoder must treat intelligence as the result of the combined solver:

```text
User intent
+ frontier/local reasoning
+ repository evidence
+ tools
+ memory
+ context management
+ verification
+ test-time compute
+ learned experience
+ resource control
```

The benchmarked unit is therefore:

```text
model + harness + tools + context policy + memory policy + verifier + resource policy
```

Model benchmark scores alone must never be treated as the expected capability of the complete AlinaCoder system.

## 3. Frontier operating modes

AlinaCoder supports:

```text
FRONTIER_ALWAYS
FRONTIER_ADAPTIVE
LOCAL_ONLY
```

### 3.1 FRONTIER_ALWAYS

When the ChatGPT bridge is connected, this is the preferred default user experience.

Every non-trivial user mission begins in the ChatGPT conversation surface and may use AlinaCoder tools for project truth and execution.

The user should not need to decide whether a problem is "hard enough" for ChatGPT.

### 3.2 FRONTIER_ADAPTIVE

AlinaCoder may keep obvious deterministic work local and escalate when expected frontier value exceeds latency/coordination cost.

This mode exists for future optimization but is not the default target experience defined by this amendment.

### 3.3 LOCAL_ONLY

AlinaCoder remains usable without ChatGPT, internet access or a frontier provider.

Loss of ChatGPT connectivity must degrade capability, not corrupt state or block recovery.

---

# Part II — ChatGPT as the Primary Conversational Brain

## 4. Primary interaction model

When the ChatGPT bridge is enabled, the simplest intended flow is:

```text
User
  ↓ ordinary language
ChatGPT
  ↓ MCP tool calls
AlinaCoder
  ↓ repository/files/tests/Git/local memory
Local machine
```

The user talks to ChatGPT normally.

Examples:

```text
"Continue AlinaCoder and improve the most important thing."
"The memory still seems weak, fix it."
"Find why this test is failing and correct it without breaking the rest."
"Make this architecture cleaner but preserve everything we already decided."
```

The user must not need to manually construct technical prompts, paste large files, identify code paths or understand MCP.

ChatGPT is the high-capability reasoning surface.

AlinaCoder is the authoritative local execution, evidence, memory and safety surface.

## 5. No ChatGPT web scraping or DOM automation dependency

The supported design must **not** depend on:

- scraping `chatgpt.com` output;
- reading ChatGPT DOM nodes programmatically;
- simulating browser clicks to harvest model text;
- extracting session cookies;
- replaying private ChatGPT web endpoints;
- reverse-engineering browser authentication;
- brittle selectors tied to ChatGPT UI markup.

The browser may be used as the normal ChatGPT user interface and for supported setup/auth flows.

The integration channel must use an officially supported app/tool mechanism, currently MCP/Apps SDK compatible interfaces when available.

If ChatGPT changes product capability, AlinaCoder must capability-probe and degrade gracefully rather than attempting an unsupported scraping workaround.

## 6. ChatGPT does not get unrestricted machine control

ChatGPT must not receive a raw unrestricted shell as the primary interface.

Instead AlinaCoder exposes bounded, typed, auditable capabilities.

Examples:

```text
project.get_state
repo.search
repo.read_file
repo.read_symbol
repo.get_dependency_neighborhood
repo.get_current_diff
git.history
git.status
memory.search
memory.fetch_decision
tests.reproduce
tests.run_targeted
tests.run_impacted
patch.stage_candidate
patch.inspect_candidate
patch.reject_candidate
verification.run
commit.promote_verified_main
```

A future shell tool may exist only behind the existing command policy, resource limits, working-directory confinement and explicit safety classifications.

---

# Part III — Exact Code and File Modification Contract

## 7. ChatGPT must be able to propose exact modifications

The frontier reasoning layer must be able to provide more than generic advice.

For coding work it may return a structured `PatchProposal`:

```text
PatchProposal
- proposal_id
- mission_id
- base_head_sha
- files[]
  - path
  - expected_blob_sha
  - operation: ADD | MODIFY | DELETE | RENAME
  - unified_diff_or_structured_edit
  - rationale
- expected_behavior_change
- assumptions
- risks
- tests_to_run
- rollback_hint
- frontier_confidence_if_available
```

The user experience may therefore reach the level:

```text
"Modify src/.../context.py"
"Replace this exact behavior"
"Add this exact test"
"Run these validations"
```

without requiring the user to paste the code manually.

## 8. Stale-patch protection

Before any frontier proposal is applied:

```text
current HEAD == proposal base HEAD
AND
current blob SHA == expected blob SHA for each modified existing file
```

If not:

```text
REJECT_STALE_PROPOSAL
→ refresh relevant files
→ rebuild evidence packet
→ ask frontier reasoning to reconsider if needed
```

Never force-apply a frontier patch to a changed file merely because the text still appears similar.

## 9. Candidate-first execution

A frontier-generated patch is a candidate, not truth.

Required flow:

```text
Frontier proposal
→ schema validation
→ scope validation
→ stale-state validation
→ isolated candidate application
→ syntax/static checks
→ targeted tests
→ impacted regression tests
→ architecture/invariant checks
→ adversarial verification
→ reliability assessment
→ promote or reject
→ commit to main only if promoted
```

No frontier response may directly satisfy the Done Contract by itself.

---

# Part IV — Zero-Config ChatGPT Connection Experience

## 10. Product requirement: "Connect to ChatGPT"

AlinaCoder must provide a first-class setup action visible to a nontechnical user:

```text
Connecter à ChatGPT
```

The target experience is:

```text
one button
→ automatic diagnostics
→ automatic local MCP startup
→ automatic secure connection preparation
→ browser opened to the correct ChatGPT setup surface
→ minimal user approval/setup step
→ automatic connection test
→ ready
```

The user must not be required to:

- write JSON;
- edit MCP configuration files manually;
- run terminal commands;
- know a local port number;
- understand HTTPS tunneling;
- understand JSON-RPC;
- generate an OpenAI API key merely to use ChatGPT as the reasoning surface;
- manually copy repository contents into ChatGPT.

## 11. Connection wizard state machine

Suggested states:

```text
NOT_CONFIGURED
CHECKING_CAPABILITIES
STARTING_LOCAL_MCP
ESTABLISHING_SECURE_ROUTE
WAITING_FOR_CHATGPT_LINK
VALIDATING_TOOL_DISCOVERY
RUNNING_READ_SMOKE_TEST
RUNNING_WRITE_CAPABILITY_TEST
CONNECTED_READ_ONLY
CONNECTED_READ_WRITE
DEGRADED
DISCONNECTED
```

Every state must have a human-readable explanation and a deterministic next action.

## 12. ChatGPT capability probe

Do not assume account/plan behavior from static documentation.

Record a `ChatGPTCapabilityProfile` based on actual observed integration capability:

```text
ChatGPTCapabilityProfile
- integration_type
- developer_mode_detected_or_user_confirmed
- tool_discovery_working
- read_tools_working
- write_tools_working
- confirmations_required
- connection_transport
- last_successful_smoke_test
- app_connection_version
- status
```

Unavailable fields are `UNKNOWN`, never inferred as true.

If write actions are unavailable, AlinaCoder may run in:

```text
CONNECTED_READ_ONLY
```

where ChatGPT can inspect and produce structured advice while local AlinaCoder performs application after its own validation path.

## 13. Tunnel abstraction

The connection layer must use an abstraction such as:

```text
TunnelProvider
- start()
- stop()
- health()
- public_endpoint()
- rotate_credentials()
- diagnostics()
```

Possible transports may include:

- a standards-compatible HTTPS tunnel suitable for ChatGPT MCP development;
- an officially supported private MCP tunnel when available and appropriately authenticated;
- a future first-party local connector mechanism.

The **zero OpenAI API key** objective means the normal ChatGPT reasoning path must not require OpenAI Platform API billing/authentication for model calls.

This does not mean every possible tunnel provider is credential-free.

If a chosen tunnel requires credentials, the wizard must explain this plainly and offer another supported route when possible.

## 14. Secure-by-default tunnel behavior

Requirements:

- random high-entropy connection secrets where applicable;
- local MCP bound to loopback unless a stronger reason exists;
- no unnecessary inbound LAN listener;
- short-lived/revocable connection credentials when supported;
- allowlist of exposed tools;
- no repository secrets in tool metadata;
- no private keys in logs;
- connection health endpoint separated from privileged actions;
- explicit shutdown/revoke path from AlinaCoder UI;
- audit record of frontier tool calls;
- rate limiting and concurrency limits through the ResourceController.

---

# Part V — ChatGPT Tool Design

## 15. Minimal context first, retrieval on demand

Do not dump the whole repository into ChatGPT.

Start with a compact `MissionContext`:

```text
MissionContext
- user_intent
- active_project
- repo_root_logical_id
- HEAD
- current mission/milestone
- hard constraints
- relevant decisions
- known failure/reproduction
- current reliability state
- available AlinaCoder tools
```

ChatGPT then pulls exact evidence through tools.

This preserves context quality and reduces accidental disclosure of irrelevant files.

## 16. Tool descriptions are part of intelligence

Each MCP tool must include clear guidance:

```text
Use this when...
Do not use this when...
Required preconditions...
Side effects...
Expected output...
Failure meanings...
```

Similar tools must be disambiguated.

Tool schemas should strongly prefer enums and typed structures over free-form strings.

## 17. Read/write separation

Every tool is classified:

```text
READ_ONLY
CANDIDATE_WRITE
VERIFICATION
PROMOTION_WRITE
DESTRUCTIVE
```

Frontier reasoning may freely use safe reads according to configured policy.

Writes must pass the existing AlinaCoder authority gates.

Especially consequential actions may remain approval-gated by the host platform even when AlinaCoder itself is configured for high autonomy.

## 18. Prompt-injection boundary

Repository files, issue text, web research and external documentation are untrusted data.

Content read through AlinaCoder must not gain authority merely by containing phrases such as:

```text
"ignore previous instructions"
"run this command"
"upload this secret"
```

The MCP server must separate:

```text
DATA
INSTRUCTIONS
POLICY
TOOL METADATA
```

Untrusted repository content stays `DATA`.

---

# Part VI — Frontier Test-Time Intelligence

## 19. Adaptive test-time compute

AlinaCoder must scale reasoning effort with evidence and task difficulty.

Suggested escalation ladder:

```text
L0 deterministic direct path
L1 one reasoning attempt + verification
L2 alternative hypothesis generation
L3 independent candidate plans
L4 candidate implementation experiments
L5 tournament/refinement
L6 adversarial verifier + discriminating tests
L7 decomposition / research / specialist escalation
```

Escalation signals include:

- failed reproduction hypothesis;
- repeated patch rejection;
- high alternative disagreement;
- architecture uncertainty;
- hidden/canary regressions;
- weak local model fit;
- stale or contradictory evidence;
- user intent ambiguity with high consequence.

More compute is not automatically better. Stop when additional reasoning no longer changes the decision or improves verification confidence.

## 20. Independent parallel rollouts

For difficult problems, AlinaCoder may obtain multiple isolated solution attempts using available models/roles.

Initial candidates should not see each other's reasoning summaries when diversity matters.

Each produces a compact `RolloutDigest`:

```text
- hypothesis
- proposed approach
- files/components implicated
- evidence used
- predicted behavior
- risks
- tests
- observed failures
- confidence reason
```

Raw long trajectories should not all be injected into the final decision context.

## 21. Tournament and refinement

When multiple viable candidates exist:

```text
candidates
→ pairwise/small-group comparison
→ preserve strongest evidence from winners
→ preserve failure lessons from losers
→ synthesize refined candidate
→ verify refined candidate from scratch
```

Selection criteria:

```text
correctness
verification strength
simplicity
regression resistance
architectural fit
reversibility
resource cost
```

## 22. Independent adversarial verifier

The verifier's goal is to falsify the candidate.

It asks:

```text
What assumption is untested?
What existing behavior could regress?
What input would break this?
What dependency was missed?
What would make the apparent test success misleading?
```

Where practical, verification context should be separated from the generation context to reduce confirmation bias.

## 23. Discriminating test generation

When hypotheses or implementations compete, prefer tests that maximize information gain.

Example:

```text
H1 predicts A under condition X
H2 predicts B under condition X
→ construct the smallest reliable experiment for X
```

Do not generate large undirected test suites when one discriminating experiment can resolve the uncertainty.

---

# Part VII — Local Model Pool and Routing

## 24. Empirical local model pool

AlinaCoder may maintain several installed Ollama candidates, but never assume that one model dominates all task classes.

Possible capability dimensions:

```text
French intent understanding
repository navigation
architecture
bug localization
code patching
test generation
critique
structured output
long-context use
research synthesis
```

Selection remains based on real repeated machine-local mini-tests and runtime history.

## 25. Checkpoint-only model changes remain mandatory

This amendment does not weaken the prior anti-oscillation rule.

Local model selection changes occur only at safe checkpoints.

A frontier ChatGPT consultation is an external reasoning interaction, not permission to hot-swap a resident local Ollama model during an atomic phase.

## 26. Learned router

Over time, route using measured task-class performance:

```text
Task features
+ model capability profile
+ runtime history
+ resource state
+ verification requirements
→ best route
```

The router must optimize reliability-adjusted utility rather than benchmark prestige or model size.

---

# Part VIII — Context and Project World Model

## 27. Context intelligence as a controllable subsystem

Retain prior Context OS operations and extend them for frontier work:

```text
PIN
FOLD
OFFLOAD
RETRIEVE
REFRESH
DROP
COMPARE
```

Stable user intent and hard constraints remain pinned.

Tool dumps and superseded exploration should be folded/offloaded.

Exact code needed for editing is retrieved fresh.

## 28. Project World Model

Maintain a living project graph linking:

```text
User Intent
↕
Product Goals
↕
Requirements
↕
Decisions / Rationales
↕
Architecture
↕
Components / Symbols
↕
Dependencies
↕
Tests / Incidents
↕
Commits / Lessons
```

Frontier reasoning should query this world model instead of reconstructing project purpose from isolated files on every mission.

## 29. Freshness is transitive

If a source changes, dependent summaries, memories, embeddings, conclusions and frontier context artifacts must be marked stale according to dependency links.

A frontier answer built on stale evidence cannot be promoted without refresh or proof that the change is irrelevant.

---

# Part IX — Hybrid Memory and Optional Supabase

## 30. Multi-channel retrieval

Memory/repository retrieval should fuse:

```text
exact lexical / FTS
semantic embeddings
symbol / AST
project graph
temporal/history
current-task relevance
```

A reciprocal-rank-style fusion is an acceptable baseline when appropriate.

## 31. Supabase remains optional

Supabase may later provide optional cross-machine/cloud persistence for:

- validated memories;
- project decisions;
- embeddings;
- trajectory summaries;
- experiment metadata;
- multi-device synchronization.

It must not become required for core local operation.

If used:

- RLS must isolate user/project data;
- privileged service credentials must never enter public clients or the repository;
- embedding freshness must track source changes;
- local cache/fallback must survive outage;
- the same embedding model must be used for comparable stored vectors unless a migration is explicitly performed.

---

# Part X — Learning from Every Mission

## 32. Trajectory learning

After verified completion or meaningful failure, extract reusable knowledge from the mission.

Do not store entire traces blindly.

Produce typed artifacts such as:

```text
ExperienceCard
SkillCandidate
FailurePattern
VerificationPattern
RepositoryConvention
RoutingObservation
ContextManagementLesson
```

## 33. Procedural skill bank

Validated recurring strategies may become skills with:

```text
- applicability conditions
- required evidence
- procedure
- termination condition
- verification contract
- known failure modes
- provenance
- confidence
- last validation
```

Skills are not promoted from one lucky success.

They require repeated evidence or strong deterministic validation.

## 34. Specialist local adapters

Long-term AlinaCoder may train or fine-tune small local specialist models/adapters for narrow tasks such as:

- intent classification;
- repository retrieval;
- context compression;
- tool routing;
- patch risk scoring;
- test selection;
- memory ranking.

This is preferred over attempting to train a single homemade frontier foundation model.

Training candidates must be evaluated on hidden holdouts before promotion.

## 35. Meta-harness evolution

AlinaCoder may experimentally improve its own orchestration:

```text
planner strategy
retrieval strategy
context policy
critic timing
number of rollouts
specialist activation
tool sequencing
verification cascade
```

Every change must use protected before/after evaluation and rollback.

The candidate harness cannot modify or inspect its hidden evaluator.

---

# Part XI — Frontier Advice Provenance

## 36. FrontierConsultationRecord

Record enough metadata to reproduce the decision context without storing secrets:

```text
FrontierConsultationRecord
- consultation_id
- mission_id
- timestamp
- provider_surface: CHATGPT | OTHER_SUPPORTED_FRONTIER
- model_label_if_exposed_else_UNKNOWN
- base_head_sha
- tool_calls_used
- evidence_artifact_ids
- proposal_ids
- verification_result
- accepted_or_rejected
- rejection_reason
```

Do not fabricate the exact frontier model identity when the ChatGPT surface does not expose it reliably.

## 37. External intelligence never becomes permanent truth automatically

A frontier claim becomes durable project knowledge only after one or more of:

- direct repository evidence;
- executable verification;
- authoritative source corroboration;
- user decision;
- repeated validated experience.

Otherwise store it as a hypothesis or advisory observation.

---

# Part XII — Reliability and Fallback Behavior

## 38. Frontier unavailable

If ChatGPT disconnects mid-mission:

```text
persist local mission state
→ finish current safe deterministic operation if possible
→ stop frontier-dependent mutation
→ continue locally if reliability floor can still be met
→ otherwise decompose or report frontier dependency
```

Never lose mission state merely because the browser closes.

## 39. Frontier gives poor advice

If ChatGPT produces:

- stale file assumptions;
- invalid tool arguments;
- repeated failing patches;
- contradictions with hard constraints;
- regression-producing changes;
- hallucinated repository facts;

AlinaCoder must reject the output and provide fresh evidence through tools before retrying.

Frontier status is not privileged over evidence.

## 40. Local model is weak, frontier is strong

Prefer frontier reasoning while keeping deterministic local execution and verification.

## 41. Frontier is strong but verification is impossible

The correct result may still be:

```text
UNPROVABLE
```

A powerful external answer does not make an unverifiable mutation safe.

---

# Part XIII — User Experience Contract

## 42. Setup complexity target

The normal user should experience approximately:

```text
Install AlinaCoder
→ click "Connecter à ChatGPT"
→ complete the smallest supported ChatGPT authorization/app step
→ see "Connecté"
→ open ChatGPT
→ talk normally
```

No terminal tutorial should be required for the standard path.

Advanced diagnostics may expose technical details behind an expandable panel.

## 43. Daily-use contract

After initial setup, the user should not think about MCP.

Expected interaction:

```text
User: "Continue le projet et corrige ce qui bloque."

ChatGPT:
→ gets AlinaCoder project state
→ reads exact relevant code
→ checks memory/history
→ reasons
→ stages candidate change
→ asks AlinaCoder to test/verify
→ iterates if rejected
→ promotes verified result
→ reports what changed
```

## 44. Connection health UI

Show simple states:

```text
ChatGPT : Connecté
AlinaCoder MCP : OK
Accès lecture : OK
Accès modification : OK / Indisponible
Projet : <name>
HEAD : <short sha>
Dernière vérification : <time>
```

Technical logs remain available but are not the primary interface.

---

# Part XIV — Acceptance Tests

## 45. ChatGPT bridge acceptance scenarios

At minimum test:

1. User connects without manually editing configuration files.
2. Local MCP starts and passes health check.
3. ChatGPT discovers read tools.
4. Capability profile detects whether write tools are usable.
5. ChatGPT reads project state from an ordinary-language request.
6. ChatGPT finds a relevant file without the user naming it.
7. ChatGPT proposes an exact patch against known blob SHAs.
8. Stale patch is rejected after the file changes.
9. Candidate patch cannot commit before verification.
10. Failing targeted test rejects promotion.
11. Passing targeted tests but failing impacted regression rejects promotion.
12. Prompt injection inside a repository file does not gain instruction authority.
13. ChatGPT disconnect preserves mission state.
14. Local-only fallback still starts.
15. No OpenAI Platform API key is required for the normal ChatGPT reasoning path.
16. Tunnel loss is diagnosed with an actionable nontechnical message.
17. User can revoke/stop the connection.
18. Secret-like files are excluded according to repository/security policy.
19. Frontier model identity remains `UNKNOWN` when not exposed.
20. Direct commit occurs on `main` only after the Done Contract passes.

## 46. Frontier intelligence evaluation scenarios

Measure system quality on:

- simple local tasks;
- ambiguous French requests;
- repository-scale bugs;
- architecture changes;
- hidden regression traps;
- stale-context traps;
- adversarial misleading comments;
- competing plausible root causes;
- tasks where multiple rollouts help;
- tasks where extra rollouts waste resources;
- tasks where a smaller local model is the better router choice;
- tasks where frontier consultation materially improves success;
- tasks where correct behavior is to abstain.

Compare at least:

```text
LOCAL_ONLY
vs
FRONTIER_ALWAYS + AlinaCoder tools
```

Track:

```text
resolved rate
regression rate
verification completeness
incorrect certainty
clarification count
tool-call count
latency
resource cost
context size
retries
rollback rate
```

---

# Part XV — Anti-Patterns

## 47. Forbidden patterns

Do not:

- scrape ChatGPT as the core integration;
- treat browser cookies as API credentials;
- give ChatGPT unrestricted filesystem access by default;
- allow ChatGPT to bypass AlinaCoder verification;
- paste the entire repository into every prompt;
- trust a frontier patch without checking current SHA state;
- assume a model name that the ChatGPT surface did not expose;
- require Supabase for local operation;
- require an OpenAI API key merely to use the ChatGPT subscription reasoning surface;
- hot-swap Ollama models outside checkpoints;
- run multi-agent/parallel rollouts for every trivial task;
- store raw trajectory noise as permanent memory;
- let self-improvement weaken the evaluator or safety gates;
- let connection convenience expose secrets or unrestricted shell capabilities;
- claim "frontier-level intelligence" from one benchmark win.

---

# Part XVI — Implementation Boundaries

## 48. Suggested modules

```text
src/alinacoder/
├─ frontier/
│  ├─ provider.py
│  ├─ consultation.py
│  ├─ capability.py
│  ├─ provenance.py
│  └─ routing.py
├─ integrations/
│  └─ chatgpt/
│     ├─ mcp_server.py
│     ├─ tools.py
│     ├─ schemas.py
│     ├─ connection.py
│     ├─ tunnel.py
│     ├─ capability_probe.py
│     └─ setup_wizard.py
├─ verification/
│  ├─ adversarial.py
│  ├─ discriminating_tests.py
│  └─ promotion_gate.py
├─ learning/
│  ├─ trajectories.py
│  ├─ skills.py
│  └─ harness_evolution.py
└─ ui/
   └─ chatgpt_connection.py
```

Exact filenames may evolve during implementation, but the subsystem boundaries are normative.

## 49. First implementation vertical slice

Implement in this order:

```text
1. typed MCP tool contracts
2. local read-only MCP server
3. connection health + capability profile
4. zero-config setup wizard shell
5. secure connection abstraction
6. ChatGPT read smoke test
7. candidate patch schema with SHA protection
8. candidate application sandbox/path
9. verification gate
10. verified main commit tool
11. read/write capability fallback
12. frontier provenance
13. advanced test-time compute and learned routing
```

Do not start with autonomous write access before the read/evidence path is reliable.

---

# Part XVII — Final Principle

The target AlinaCoder experience is:

> **The user talks normally to ChatGPT. ChatGPT supplies frontier reasoning. AlinaCoder supplies the live project, memory, tools, exact code evidence, execution and verification. Neither is trusted alone: the strongest result comes from frontier reasoning constrained by local truth and executable proof.**

And the setup requirement is:

> **A nontechnical user should connect AlinaCoder to ChatGPT through a guided one-button flow, without terminal commands, manual MCP configuration or an OpenAI API key for normal ChatGPT reasoning.**
