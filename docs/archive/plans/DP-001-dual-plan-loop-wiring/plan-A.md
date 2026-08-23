> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Add redacted three-hat prompt-map assembly | C2 | IF-041 |  |
| P2 | Implement heterogeneous, budgeted dual-plan session runner | C3; C7 | IF-015; IF-041; IF-044 | P1 |
| P3 | Implement coverage-repair, critique, revision, and swapped-arbiter state machine | C4; C5 | IF-015; IF-046; IF-057; Proposed: `agent_loop` invokes `plan_coverage`; nearest IF-046 has the required agent-loop direction but covers review scoring rather than structural plan validation | P2 |
| P4 | Persist round artifacts, verdict summary, and selected WI rows atomically | C6 | Proposed: `agent_loop` writes dual-plan artifacts, `docs/log.md`, and `work-items.csv`; nearest IF-055 connects the coordinator to WI scheduling but does not authorize these persistence operations | P3 |
| P5 | Dispatch trigger-declared frontier entries through the dual-plan path | C1 | IF-015; IF-055 | P3; P4 |

## Notes

No goal clauses are excluded.

Assumption: the trigger is declarative WI/goal metadata available when `agent_loop` consumes the scheduler result; P5 adds and validates the minimal registry field if it does not already exist.

Assumption: P1’s tests prove forbidden self-assessment sources cannot enter planner prompts, including through prompt-map overrides.

Assumption: P2 owns one round-level budget ledger layered over existing per-session limits and records same-family degradation explicitly in telemetry.

Assumption: P3 treats `plan_coverage.py` exit 1 as eligible for exactly one author repair; repeated findings, cap exhaustion, swapped-verdict disagreement, and budget exhaustion produce the gate-policy human outcome.

Assumption: P4 allocates the next `DP-NNN` directory deterministically and updates tracked artifacts, the log summary, and queued WI rows as one recoverable coordinator operation.

Assumption: P5 is the end-to-end wiring step; its acceptance test demonstrates that a trigger-declared ready entry launches two planner sessions and never enters the direct BUILD path.