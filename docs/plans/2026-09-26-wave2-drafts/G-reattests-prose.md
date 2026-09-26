+++
id = "WI-@G@"
title = "Name --reattests where the kit tells a user to re-copy a drifted approved row"
workstream = "docs"
specref = "project-trajectory/scripts/baseline_snapshot.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 4
+++

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
