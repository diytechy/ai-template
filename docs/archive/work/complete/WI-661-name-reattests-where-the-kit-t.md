+++
id = "WI-661"
title = "Name --reattests where the kit tells a user to re-copy a drifted approved row"
workstream = "docs"
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

Every message and shipped template that tells a user how to re-copy a row
now prescribes a command the kit accepts. There is no behaviour change.

- **Where the id is known, it is printed.** `pending.py` prints the row in
  its drift line, and `acceptance_record.py` in its amend-without-flip warning.
- **The refusal picks its remedy by status.** `intake.py`'s flip refusal
  (`_flip_remedy`) now tells a Drafted row to take a reviewed Status approval
  plus a snapshot, and gives a Founded (amended) row `--reattests <id>`.
- **The mirror findings prescribe a repair that works.** They say to restore
  the blessed copy or take a fresh act, `--approves "<stem>=<REF>"
  --reattests …`. The stem is a token the resolver accepts for both TOML and
  CSV carriers.
- **The census names every copy trigger truthfully.** A row moving into
  approval or arriving approved, `--approves`, or `--reattests`; a de-approval
  never copies.
- **The brief header and the open-items footer** name `--reattests
  <ROW-ID>`.
- **The shipped last-approved README template** describes one writer with
  two acts and no longer describes the retired mechanical flip.

- **Evidence:** the changed tests were red first in
  `test_intake`, `test_baseline_snapshot`, `test_trace_briefs`,
  `test_gen_open_items`, `test_gen_trajectory_pending` and
  `test_trajectory_staged`. The resolver test parses the prescribed
  `--approves` argument for both carriers.
- **Review:** Sol took three rounds (arbitration rulings 9 and 12, the second
  correcting the coordinator's own ruling on the printed remedy). The last
  finding was a missing citation, which the integrator added.
- **Integration:** the brief header merged WI-577's scoping with this item's
  `--reattests` clause.

## Context

Since row-level refusal landed, `intake.py snapshot` refuses a drifted
approved row that the act neither flips nor names with
`--reattests <ROW-ID>`. Several messages still tell a user only to "run
`intake.py snapshot`" for a drifted row, which now refuses: `pending.py`,
`acceptance_record.py`, `trace.py` and `gen_open_items.py`. The shipped
`registries/last-approved-README.template.md` still describes the retired
mechanical flip inside `intake.py adjudicate`.

IN SCOPE: make each such message name `--reattests <ROW-ID>` (with the row
where the message knows it), and rewrite the template README's description of
how the record is written. NOT IN SCOPE: any behavior change.

## Done-when

- No user-facing message or shipped template tells a user to run
  `intake.py snapshot` for a drifted row without naming `--reattests`.
- The tests that pin these messages are updated, and the commit bar passes.
