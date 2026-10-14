+++
id = "WI-871"
title = "Owner ruling: how interface rows join the adjudicated spine"
workstream = "process"
specref = ""
needs = ["OI-112"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

CANCELLED (owner, 2026-10-14): OI-112, the ruling this placeholder waited on, is ruled from the review-churn plan's variant F (`docs/plans/2026-10-11-review-churn/README.md`, the revision 35 rulings): an interface is approved through the sitting of the row it serves, judging payload compatibility; a requirement names the interface it constrains through its optional `constrains` cell; option (c) is declined. The work is item 11's phase-3 interface-approval slice, which files its own row in the plan's order; keeping this row would have made it claimable now, ahead of that order.

## Context

Filed by hand by the coordinator on 2026-10-08, as the queued placeholder that
puts OI-112 on the owner's surface: an open item is filed together with the
queued row that cites it. The owner raised it after learning that no IF row has
ever been approved: "Technically, all SRs should be built up over interfaces,
the SR would be transform definition, the interfaces are on the measureable
input / output, but right now the IF checks are quite light." It may be heavy,
so it waits on the owner's ruling.

The ruling of OI-112 writes this row's Done-when in the same commit, as the rule
for citing rows requires.
