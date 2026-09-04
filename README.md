# AlinaCoder

AlinaCoder is a Windows-first, Python 3.12+, Ollama-only autonomous coding agent designed to understand large repositories, plan work, edit code, run tests, detect regressions, recover from failures, learn from project history, and work directly on `main` under deterministic safety and verification gates.

## Current design specification

The current architecture is defined by:

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-conversation-and-external-self-improvement-amendment.md`

The amendment is normative and extends v0.2 with:

- natural conversational interaction in French, including short, imperfect and non-technical requests;
- intent inference from conversation, memory, Git, roadmap, code, architecture, tests and project history;
- autonomous intent-to-mission compilation and technical planning;
- project mental-model and contextual reference resolution;
- external self-improvement with benchmark-before / benchmark-after evaluation;
- isolated candidate evaluation;
- automatic rejection or rollback when an improvement is worse;
- protected evaluator integrity;
- full autonomy retained;
- direct commit/push to `main` retained.

## Design history

- `docs/superpowers/specs/2026-09-04-alinacoder-v0.1-design.md`
- `docs/audits/2026-09-04-v0.1-critical-intelligence-audit.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-design.md`
- `docs/superpowers/specs/2026-09-04-alinacoder-v0.2-conversation-and-external-self-improvement-amendment.md`
