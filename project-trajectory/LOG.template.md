# Project Log — Append-only history

The durable record for the gated process (see [process.md](process.md) §5):
gate sign-offs, review verdicts, ratified decisions, and session notes append
here, **newest last**, and are never rewritten. The working surface — what to
do *next* — lives in [status.md](status.md), which points here; this file is
**evidence, never normative**: a rule or requirement belongs in the process
doc or a registry, not in a log entry. Entries here and in status.md cite
**stable ids** (OI-n, gate names, dates), never iteration-branch commit SHAs —
sync scrub/collation may rewrite those (process-options.md "Agent iteration
branch & sync").

---

## Gate Sign-offs

Add columns for any active domain hats. Drop the `G-Release` row for a one-off
deliverable.

| Gate | Stakeholder | UX/Docs | System Eng | Test Eng | Human |
|---|---|---|---|---|---|
| G1 — Requirements/UX/Constraints | PENDING | PENDING | PENDING | n/a | PENDING |
| G2 — Decomposition & Test Coverage | n/a | n/a | PENDING | PENDING | PENDING |
| G3 — Implementation | n/a | n/a | PENDING | PENDING | PENDING |
| G-Release — Release readiness | n/a | n/a | n/a | PENDING | PENDING |
| G-Final — Acceptance | PENDING | n/a | n/a | (evidence) | PENDING |

## Decisions log

_Ratified or executed decisions only — the call, the alternatives passed over,
why (one bullet each; cite ids). A decision still **awaiting** a human is an
Open item in [status.md](status.md), not a log entry._

## Audit log

<!-- Append verdict blocks here per process.md §5. Newest at the bottom. -->

### DRIVER — G1 — Round 1 — <YYYY-MM-DD>
Scaffolding created. Starting G1.
