+++
id = "WI-554"
title = "Approval-brief renderer defects: a Drafted row shown approved, a changed Method cell truncated (OI-71)"
specref = "docs/requirements/open-items.toml#OI-71"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Round 019 of the wi508 lane returned three MAJORs; two are defects of
`trace.py --approve modified` ON TRUNK, not of the lane (`OI-71`; decision 20
of `docs/decisions-for-review-2026-08-31.md`), and they will reproduce on ANY
lane that regenerates the re-attestation brief — which is why `OI-71`'s
ruling files them ahead of the wi508 close and its successor:

1. a `Drafted` row renders as "approved — re-attestation owed"; related,
   decision 9 banked that the generator has no vocabulary for "approved, then
   demoted" (a lane-local approval reverted before reaching trunk reads as
   "never approved");
2. a changed `Method` cell is truncated in the brief, so the adjudicating
   reader cannot see what actually changed.

## Done-when

Both defects are reproduced as failing tests against the brief renderer,
fixed, and a regenerated brief shows a `Drafted` row as Drafted and a changed
cell whole; the "approved, then demoted" vocabulary gap is either fixed
alongside or explicitly banked with a pointer to its own future row.
