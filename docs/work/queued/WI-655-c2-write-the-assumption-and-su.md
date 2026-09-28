+++
id = "WI-655"
title = "C2: write the assumption and surrogate rows, and each boundary interface's bridged_by or coincident"
workstream = "requirements"
specref = "docs/plans/2026-09-20-validation-gap-and-the-assumption-tier.md#11-staging"
needs = ["WI-643", "WI-616"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Context

The assumption-tier plan's step C2 (plan §11; the briefing's step 2; the C1 package's deferrals): write the DA and surrogate rows derived from the person-facing needs, each a new Drafted claim; give every SR `da_refs` or `coincident`; re-point the SRs' `boundary_refs` to the redrawn frame's bundles (the C1 package defers that to C2 so each SR is touched once); and give each boundary interface its `bridged_by` or `coincident`. Warn-only, arms off. The mockup's eight DAs and three surrogates are the starting draft. SN-041's first acceptance sentence (a reader new to the code, spine map D5) becomes an assumption row with a sampled test here.

Filed 2026-09-26 as the condition of OI-94's ruling: the owner accepted making SR-211's bridging report vacuous "as long as" queued work returns to close the gap. C2 was a plan step with no queued item until now. C3 (evidence) and C4 (activation) follow it and are not filed here.

## Done-when

- The assumptions registry holds the drafted DA and surrogate rows, each landing on a declared crossing (`effect_at`).
- Every SR carries `da_refs` or `coincident`; every boundary interface carries `bridged_by` or `coincident`, and the bridging report (WI-654) is clean or each remaining advisory is named in the log.
- The rows go to adjudication through the normal route; nothing is approved by this item; the commit bar and `trace.py --strict` pass.
