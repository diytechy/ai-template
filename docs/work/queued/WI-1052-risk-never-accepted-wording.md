+++
id = "WI-1052"
title = "An unproven risk no act ever accepted is reported as never accepted, not as reopened"
workstream = "process"
sr_refs = ["SR-202"]
needs = []
specref = "docs/archive/work/complete/WI-1041-unanchored-risk-said.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, from
WI-1041's build (noted in the queue-drill hand-off, not filed until now).
WI-1041 made a risk that no acceptance act names read unanchored, so it
reads unproven. Two messages then word every unproven risk the same way:
the advisory in `assumption_rules.py` ("assumption {}'s accepted risk has
reopened, and it reads unproven until the risk is accepted again", line
1509) and the release gate's line ("its accepted risk has reopened", line
1759). "Reopened" and "accepted again" are true for a risk an act accepted
and a later change undid; for a risk no act ever accepted they tell the
reader something that never happened.

## Done-when

- [ ] The advisory and the release gate word an unproven risk by what the
      reading `accepted_risk_state` already returns, in three cases: a risk
      an act accepted and a later change or failed sample undid reads
      "reopened" and "accepted again"; a risk no act in the readable
      acceptance record names reads as never accepted, with how to accept
      it; and a risk whose acceptance history cannot be read (an unreadable
      ledger, history the clone lacks) keeps the reading's own reason and
      claims neither. The promise is bounded to the record and registries as
      the kit writes them.
- [ ] Tests pin each of the three wordings at both sites.
- [ ] Any row whose accepted text words this message (LLR-239 first) is
      checked against the new wording; an amendment it needs is text only
      and listed as owed to adjudication.
