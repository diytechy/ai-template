+++
id = "WI-571"
title = "The snapshot copies only what the act authorises: copy_live scoped to the flipped registry and the named --approves refs"
workstream = "process"
specref = "docs/plans/2026-09-01-snapshot-copy-scope.md"
buildtier = "medium"
priority = 5
safety_class = "ordinary"
+++

## Context

Filed 2026-09-01 (evening supervised session) from the owner's question on OI-78 and an independent investigation: baseline_snapshot.copy_live mirrors all seven registries on every intake.py snapshot act, so a spine Status flip re-seals whatever off-spine drift is live at that moment (9 of 21 prior snapshot commits did; the wi508 handback merge was not causal). Scope copy_live to the flipped registry plus the registries named by --approves; make --approves a named list; stamp the act's scope; re-read the queued reseal row's stand branch. Read the plan's section 2 before widening - moving the write to the trunk lane is the recorded alternative, not this row.

**Standing constraint (owner ruling 2026-09-01, the approval act is the
adjudicator's):** if this row authors or amends spine rows (SR/LLR/TC), leave
them `Drafted`; do NOT flip any `Status`, and do NOT run `intake.py snapshot`
or write `docs/archive/last_approved/` on this lane — including while testing
the scoped copy, which must be driven on a scaffold, never on this repo's
snapshot. The flip and the snapshot are performed on trunk by the
adjudication arm once it ships.
