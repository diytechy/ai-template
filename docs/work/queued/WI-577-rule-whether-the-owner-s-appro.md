+++
id = "WI-577"
title = "Rule whether the owner's approval brief narrows to the held rungs, then apply the ruling to trace --approve"
workstream = "process"
needs = ["OI-82"]
specref = "docs/archive/work/complete/WI-574-spot-check-the-clean-close-of.md"
buildtier = "medium"
priority = 4
safety_class = "ordinary"
+++

## Context

Drafted by WI-574 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

Gated on the owner's ruling by construction: the `open_item` cell above makes
`intake._inject_open_item` mint a `pending` OI at this row's merge and land its
id in THIS row's `needs`, so the successor parks `waiting:open-item-pending`
until the ruling lands (OI-73 exit (B) — there is no standalone OI exit). IN
SCOPE once ruled: apply the ruling to `trace.py`'s `--approve modified`
population and to whatever `docs/ratify/CURRENT.md` renders, reading the dial
through the EXISTING `agent_common.human_approves_spine` — a third copy of the
rung table is the exact defect WI-572's round-1 MAJOR was about — plus the
PROCESS_OPTIONS.md §2a table row that describes the owner's surface, which is
unsatisfied prose until this lands either way. EXPLICITLY NOT IN SCOPE: the
adjudication-side filter (shipped and correct), and any change to
`SPINE_APPROVAL_RUNGS` itself.

Advisory registry joins (WI-388; never gating):

### Pending open items whose WI-Refs touch this row's kin (premise risk)
- OI-82 (pending): WI-572 moved the first-approval act to the adjudicator and filtered the minted population by the human-approval dial at both adjudication ends (intake's mint a…
