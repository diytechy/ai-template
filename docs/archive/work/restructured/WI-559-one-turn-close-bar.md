+++
id = "WI-559"
title = "A close a lane can finish: the one-turn close bar, review rounds after ADJUDICATE, honest banners (OI-76 / plan 2.1+2.4)"
specref = ""
workstream = "process"
sr_refs = []
needs = ["~WI-552"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Restructured into WI-579, WI-580.

## Context

Two queue-blockers from the 2026-08-31 run (plan sections 2.1 and 2.4,
commissioned by `OI-76`'s ruling). The worst outcome measured: `WI-540`'s
three sessions each verified their rework, started the ~11-minute full
suite, could not wait on it inside a turn, and were killed — three NO-COMMIT
sessions read as a C1 stall, so the dispatcher closed a FINISHED row
`partial` and the quarantine reverted 3876 lines. Separately, adjudication
lanes exit DONE claiming "review round approved" with no round drawn —
scheduling exists after a committing BUILD only. Section 2.3 (the close
ritual in every adjudicator brief) is OWNED BY `WI-552` Done-when 1 and is
deliberately not duplicated here; the soft edge orders this row behind that
rework where the scheduler can manage it.

## Done-when

1. The close ritual names a bar a worker can complete in ONE turn: the
   commit bar (smoke + budget + docs) at close, with the full unfiltered
   suite run by the lane's refresh inside the slot (which already runs the
   declared bar outside any session's turn) or a declared batched form. A
   close instruction that cannot execute in one turn is treated as the
   stall generator it measurably is.
2. A committing ADJUDICATE session schedules its review round exactly as a
   committing BUILD does, and no exit banner claims a round that was never
   drawn.
3. Tests drive the false-partial class (built-and-verified lane, long
   suite) and the adjudicate round scheduling on a scaffold.
