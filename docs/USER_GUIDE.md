# AlinaCoder v0.2 — User Guide

AlinaCoder is a Windows-first autonomous software-engineering workbench. Daily operation is designed to happen inside `AlinaCoder.exe`.

## Installation and first run
1. Launch `AlinaCoderSetup.exe`.
2. The installer analyzes the Windows version, architecture, RAM, available disk, GPU/VRAM, Git, Ollama and installed Ollama models.
3. It installs only missing or incompatible prerequisites from allow-listed official GitHub releases. Downloaded installers are SHA-256 checked and Windows executables must pass Authenticode validation before execution.
4. It selects a local model that fits the machine. The default policy is versioned in `prerequisites-v0.2.json`; low-resource/CPU-only machines can use `qwen3:0.6b` instead of receiving an oversized model.
5. It starts/checks Ollama on `127.0.0.1:11434`, pulls the selected model when needed, and performs a real local inference before installation is considered ready.
6. Launch `AlinaCoder.exe`, select/open a repository, then use normal French conversation or `/goal <objectif>` for a persistent objective.

An existing compatible Git/Ollama installation is treated as user-owned (`pre_existing`). Normal AlinaCoder uninstall never removes it or its user models. Dependencies installed by AlinaCoder are tracked separately as `managed_by_alinacoder` with provenance receipts.

If the network is unavailable, Setup fails closed instead of announcing success. `--offline` records what is missing; `--deferred-prerequisites` installs only the AlinaCoder application and records the runtime as not ready. Re-running Setup can resume the bootstrap.

## Setup lifecycle
`AlinaCoderSetup.exe` supports install, `--repair`, `--upgrade`, provenance-bound `--rollback`, and `--uninstall`. Rollback is allowed only when AlinaCoder owns the prerequisite and has the exact prior official URL and SHA-256. No arbitrary downgrade is attempted.

## Controls
- **Pause** preserves the run and stops new scheduling.
- **Resume** continues from canonical persisted state.
- **STOP** stops current execution; future effects require a new run/resume decision.
- **Takeover** gives control to the user without discarding verified state.

## `/goal`
A goal remains active until falsifiable acceptance criteria are verified or external impossibility is evidenced. Provider switch/restart must not require reconstructing the conversation.

## Privacy and cost
Local state is canonical. Supabase is optional and non-secret. Ollama is a replaceable local provider, not a canonical state store. Autonomous paid LLM spend is disabled.
