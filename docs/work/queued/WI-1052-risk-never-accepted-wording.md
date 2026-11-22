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

- [ ] The advisory and the release gate say a risk no acceptance act names
      has never been accepted (and how to accept it), and keep "reopened"
      for a risk an act accepted, each from the reading `accepted_risk_state`
      already returns.
- [ ] Tests pin both wordings at both sites.
- [ ] Any row whose accepted text words this message (LLR-239 first) is
      checked against the new wording; an amendment it needs is text only
      and listed as owed to adjudication.
