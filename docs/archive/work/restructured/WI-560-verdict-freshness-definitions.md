+++
id = "WI-560"
title = "One freshness definition for verdicts, and the approval brief's two staleness traps (OI-76 / plan 2.2+2.5)"
specref = "docs/plans/2026-08-31-verdict-record-and-queue-blockers.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Restructured into WI-579, WI-580, WI-581.

## Context

Commissioned by `OI-76`'s ruling (plan sections 2.2 and 2.5). The C2
review-owed derivation and the merge slot disagree about which commits can
invalidate a verdict, so the loop's own telemetry commits re-owed a round
and two identical APPROVEs were drawn on one lane. The approval brief went
red twice for staleness no lane caused: an AMENDMENT of an approved cell
stales it exactly as a mint does but the worker brief only names
mint/re-status, and the brief's history-derived provenance line goes stale
on trunk the moment a lane's fresh copy merges. `WI-558`'s tree-identity
trailer dissolves the verdict half at the gate; the C2 derivation and the
brief traps remain.

## Done-when

1. ONE shared definition of "the last commit that could invalidate a
   verdict" (excluding `docs/reviews`, `docs/log.d`, `docs/iteration`) is
   used by both the merge slot and the C2 review-owed derivation; the
   double-identical-round class becomes unrepresentable on a scaffold.
2. The worker brief names the approval-brief regeneration for a lane that
   AMENDS an approved cell, not only one that mints or re-statuses.
3. The trunk step regenerates the approval brief (`CURRENT.md`) after a
   merge that touched it, the same way the trunk lane owns every other
   generated artifact — a following lane is never redded by staleness it
   did not cause.
4. Tests drive all three.
