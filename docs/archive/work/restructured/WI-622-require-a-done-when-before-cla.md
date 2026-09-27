+++
id = "WI-622"
title = "Require a Done-when before claim, and flag a lane that changes its own Done-when at merge (S13)"
workstream = "unattended"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#37-who-plans-who-builds-who-reviews-note-3"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Deliverable

Restructured into WI-621.

## Context

Ruled by the owner 2026-09-24 (sister plan S13, §3.7; review pack B3): two
rules, and no new role.

On 2026-09-24, 11 of the 18 open work items had no identifiable Done-when.
Across all history, builders edited their own Done-when in 14 commits in 10
work items, and three of those changed its meaning (WI-120, WI-228, WI-580).
Ticking with evidence is the normal convention, so the comparison strips ticks
and trailing evidence. The precedent: amended approved spine text mints an
adjudication row at merge (`intake.py:607-625`, `:718-744`). If S11's plan
moves the claim off trunk, "at claim" means the spec at the lane's fork
point.

## Done-when

- A work item without a `## Done-when` is not claimable: warn-first until the
  open items lacking one are backfilled, then the claim refuses by name.
- At merge, each Done-when item's text at claim is compared with its text at
  merge, ticks and trailing evidence stripped, and any change is flagged to the
  reviewer and the adjudicator.
- Tests: a tick with evidence does not flag; a reworded item does; a work item
  with no Done-when warns (and later refuses).
