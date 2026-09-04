# AlinaCoder Core Foundations LOT 01–05 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans and superpowers:test-driven-development. Direct commits to `main` are explicitly approved for this project.

**Goal:** Implement the first five Agiflow roadmap lots as a runnable, tested Python 3.12+ foundation for AlinaCoder v0.2.

**Architecture:** A stdlib-first Python package keeps the foundation deterministic and zero-cost. The spec compiler provides fail-closed governance; SQLite-backed event/state/memory stores provide durable canonical state; `/goal` is a persistent objective state machine; security gates mediate effects; repository intelligence and context compilation remain local and provenance-aware.

**Tech Stack:** Python 3.12+, stdlib (`dataclasses`, `sqlite3`, `ast`, `hashlib`, `json`, `pathlib`, `argparse`, `logging`, `urllib.parse`), `unittest`, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-validated-consolidated-spec.md` plus `2026-09-04-alinacoder-v0.2-normative-manifest.json` and all active documents referenced by that manifest.

## Global Constraints

- `MAX_PAID_SPEND_EUR = 0.00`; no paid fallback, auto-upgrade, auto-reload, or automatic credit purchase.
- Canonical Git branch is `main` only.
- Current grounded user intent and owner policy outrank model inference.
- Durable effects require typed admission outside free-form model reasoning.
- Canonical state is versioned; stale writers/responses cannot mutate newer state.
- Completion requires evidence; no self-certified Done.
- Memory is provenance/freshness-aware and project-isolated.
- Crash/recovery must preserve verified progress and prevent duplicate effects.

---

### Task 1: LOT 01 — Bootstrap runtime, Spec Compiler & CI

**Files:** `pyproject.toml`, `.github/workflows/ci.yml`, `src/alinacoder/{__init__,config,cli,logging_setup}.py`, `src/alinacoder/spec/{__init__,compiler}.py`, `tests/test_bootstrap_spec.py`.

**Produces:** importable package, typed constitutional config, manifest/spec compiler, fail-closed conflict/hash checks, CLI smoke command and CI.

- [ ] RED: tests for import/config invariants, manifest hash verification and contradiction rejection.
- [ ] GREEN: implement minimal package/config/compiler/CLI.
- [ ] REFACTOR: isolate Git-blob hashing and compiler result types.
- [ ] VERIFY: full unittest + compileall + CLI spec compile.
- [ ] COMMIT: `feat(core): bootstrap runtime and spec compiler`.

### Task 2: LOT 02 — Canonical State, Event Log, Checkpoints & Recovery Kernel

**Files:** `src/alinacoder/state/{__init__,models,store}.py`, `tests/test_state_recovery.py`.

**Produces:** append-only SQLite event log, versioned canonical session state, checksums, CAS/fencing, evidence receipts, checkpoints, idempotent effect journal and recovery reconciliation.

- [ ] RED: reconstruction, stale-writer rejection, forward restore, duplicate effect and pending-effect recovery tests.
- [ ] GREEN: implement SQLite WAL store with transactional compare-and-set.
- [ ] REFACTOR: centralize canonical JSON/checksum handling.
- [ ] VERIFY: fault-injection style tests and full regression.
- [ ] COMMIT: `feat(state): add durable canonical state and recovery kernel`.

### Task 3: LOT 03 — `/goal` Persistent Objective Engine

**Files:** `src/alinacoder/goal/{__init__,models,engine}.py`, `tests/test_goal_engine.py`.

**Produces:** persistent `GoalContract`, independently mutable plan revision, criterion evidence state, pause/resume/edit/cancel, stagnation/strategy change, strict completion and proven-impossibility rules.

- [ ] RED: crash-safe reload, stale criterion prevents completion, plan replacement preserves verified progress, stagnation causes replan, impossible requires evidence/alternatives.
- [ ] GREEN: implement goal state machine on canonical store.
- [ ] REFACTOR: pure transition functions where possible.
- [ ] VERIFY: multi-step replay tests and full regression.
- [ ] COMMIT: `feat(goal): implement persistent goal autopilot kernel`.

### Task 4: LOT 04 — Policy, Security, Authority, Secrets & Effect Mediation

**Files:** `src/alinacoder/security/{__init__,authority,effects,secrets,tools,egress}.py`, `tests/test_security_kernel.py`.

**Produces:** owner policy ceiling, scoped capability tokens, revocation epochs, instruction privilege/taint checks, secret redaction/broker abstraction, egress allowlist, tool manifest fingerprinting, external effect admission + idempotency.

- [ ] RED: prompt-injection privilege escalation, stale approval, double-effect, secret logging and MCP/tool-rug-pull tests.
- [ ] GREEN: implement deterministic fail-closed gates.
- [ ] REFACTOR: immutable authority/token dataclasses and normalized fingerprints.
- [ ] VERIFY: red-team integration tests + full regression.
- [ ] COMMIT: `feat(security): add authority and external effect mediation`.

### Task 5: LOT 05 — Memory OS, Repository Intelligence Graph & Context Compiler

**Files:** `src/alinacoder/memory/{__init__,store,context}.py`, `src/alinacoder/repo/{__init__,index}.py`, `tests/test_memory_context.py`.

**Produces:** SQLite WAL project-scoped memory, provenance/freshness/supersession, lexical+semantic-lite+graph retrieval, stale-memory rejection, Python AST/symbol/import indexing with incremental hashes, context compiler and forgetting detector.

- [ ] RED: project isolation, stale contradiction, symbol rename/index refresh, bounded context and forgetting tests.
- [ ] GREEN: implement local memory/index/context services.
- [ ] REFACTOR: deterministic scoring and source authority precedence.
- [ ] VERIFY: long-context/project-isolation regression suite.
- [ ] COMMIT: `feat(memory): add governed memory and repository context`.

## Final Core Foundations Gate

- [ ] Run all tests from a clean local workspace.
- [ ] Run `python -m compileall -q src tests`.
- [ ] Validate constitutional config and spec compiler against repository manifest/spec in GitHub CI.
- [ ] Review all files for placeholders, permissive fallbacks, secret leakage and missing project scoping.
- [ ] Verify GitHub `main` HEAD equals final commit and CI is green before marking LOT 01–05 Done.
