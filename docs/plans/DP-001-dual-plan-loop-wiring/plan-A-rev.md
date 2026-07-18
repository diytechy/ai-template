| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Add redacted three-hat prompt-map assembly | C2 | IF-041 |  |
| P2 | Implement heterogeneous, budgeted dual-plan session runner | C3; C7 | IF-015; IF-041; IF-044 | P1 |
| P3 | Add coverage checks, report injection, and one-shot author repair | C4 | IF-057; Proposed: `agent_loop` invokes `plan_coverage`; nearest IF-046 has the required coordinator-to-analysis direction but scores review verdicts rather than validating plan structure and coverage | P2 |
| P4 | Enforce critique/revision caps and position-swapped arbitration | C5 | IF-015; IF-041; IF-046 | P3 |
| P5 | Persist round artifacts, verdict summary, and selected WI rows atomically | C6 | Proposed: `agent_loop` writes dual-plan artifacts, `docs/log.md`, and `work-items.csv`; nearest IF-055 connects the coordinator to WI scheduling but does not cover round-result persistence | P4 |
| P6 | Dispatch trigger-declared frontier entries through the dual-plan path | C1 | IF-015; IF-055 | P4; P5 |

## Notes

No goal clauses are excluded.

G1 fixed: former P3 is split into P3’s independently testable coverage/injection/one-repair mechanic and P4’s independently testable capped critique, revision, swapped-arbitration, and paging state machine.

Assumption: the trigger is declarative WI/goal metadata available when `agent_loop` consumes the scheduler result; P6 adds and validates the minimal registry field if absent.

Assumption: P1 proves forbidden self-assessment sources cannot enter planner prompts, including through prompt-map overrides.

Assumption: P2 owns a round-level budget ledger layered over existing per-session limits and records same-family degradation in telemetry.

Assumption: P3 runs coverage after generation and revision, injects each report into the applicable critique and arbiter prompts, permits exactly one exit-1 repair bounce to the author, and returns repeated findings to P4 as a paging condition.

Assumption: P4 defines position-swapping as two arbiter sessions receiving reversed plan ordering and labels; differing selected-plan verdicts, exhausted caps, repeated coverage findings, or budget exhaustion produce the `docs/gate-policy` human outcome.

Assumption: P5 allocates the next `DP-NNN` directory deterministically and updates tracked artifacts, the log summary, and queued WI rows as one recoverable coordinator operation.

Assumption: P6 is the end-to-end wiring step; its acceptance test demonstrates that a trigger-declared ready entry launches two planner sessions and never enters the direct BUILD path.