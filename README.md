# AlinaCoder

AlinaCoder is a Windows-first, Python 3.12+, Ollama-only autonomous coding agent designed to understand large repositories, plan work, edit code, run tests, detect regressions, recover from failures, learn from project history, adapt to the local machine, and work directly on `main` under deterministic safety and verification gates.

## Frozen v0.2 specification

The primary normative implementation contract is now:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-final-design.md`

Status: **FROZEN FOR IMPLEMENTATION**.

The frozen spec consolidates the full v0.2 architecture, including:

- natural conversational French and context-aware intent resolution;
- noisy/hesitant voice understanding with corrections and changes of mind;
- repository intelligence, dependency reasoning and history-aware planning;
- reliable internet research with grouped, provenance-backed sources;
- alternative-solution exploration, self-critique and regression detection;
- conditional specialist reasoning only when measured to improve results;
- external self-improvement with protected before/after hidden benchmarks and rollback;
- automatic machine resource discovery and global CPU/GPU/RAM/time/context budgets;
- fixed `HardwareProfile` separated from dynamic `DynamicLoadSnapshot`;
- anti-oscillation through smoothing, hysteresis, dwell time and cooldown;
- local model selection from repeated real mini-tests on the actual machine;
- model switching only at explicit safe checkpoints;
- weak-model detection, honest uncertainty and verifiability-first task decomposition;
- full autonomy retained and direct commit/push to `main` retained.

## Design history

Historical design/audit documents remain available for provenance:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.1-design.md`
- `docs/audits/2026-09-04-v0.1-critical-intelligence-audit.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-conversation-and-external-self-improvement-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-research-voice-context-specialists-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-resource-awareness-model-calibration-amendment.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-resource-anti-oscillation-checkpoints-amendment.md`

New major product capabilities should target v0.3 unless v0.2 is explicitly reopened.