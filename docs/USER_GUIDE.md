# AlinaCoder v0.2 — User Guide

AlinaCoder is a Windows-first autonomous software-engineering workbench. Daily operation is designed to happen inside `AlinaCoder.exe`.

## First run
1. Launch `AlinaCoder.exe`.
2. Select/open a repository.
3. Configure an eligible zero-cost remote provider or a local model runtime. Paid fallback is disabled.
4. Use normal French conversation or `/goal <objectif>` for a persistent objective.
5. Inspect Plan, Context, Diff, Tests, Git, Receipts, Run Inspector and Timeline from the workbench.

## Controls
- **Pause** preserves the run and stops new scheduling.
- **Resume** continues from canonical persisted state.
- **STOP** stops current execution; future effects require a new run/resume decision.
- **Takeover** gives control to the user without discarding verified state.

## `/goal`
A goal remains active until falsifiable acceptance criteria are verified or external impossibility is evidenced. Provider switch/restart must not require reconstructing the conversation.

## Privacy and cost
Local state is canonical. Supabase is optional and non-secret. Autonomous paid LLM spend is disabled.
