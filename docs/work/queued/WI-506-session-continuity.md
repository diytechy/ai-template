+++
id = "WI-506"
title = "Session continuity: the template review, the resume-pack ritual, and the investigated context-restart trigger (OI-57 ruled (b), 2026-08-22)"
specref = "docs/requirements/open-items.toml#OI-57"
workstream = "process"
sr_refs = ["SR-177"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes OI-57 (b), with (c)'s trigger investigated in the same row:

1. **The review**: the twelve templates under project-trajectory/prompts/
   read side by side for the owner's split question — what the ADJUDICATOR
   is told versus what the WORKER is told about the same lane state —
   against the sessions the recent grinds actually ran; drift between what
   templates promise and what workers do filed as findings.
2. **The resume-pack ritual**: the worker template gains a standing-state
   contract — the fragment section + lane-spec Context written BEFORE
   heavy verification, so an interruption at any point leaves a resumable
   record (the pattern all seven of this week's successful interruption
   recoveries used) — and the loop relaunches a died session from that
   record.
3. **The trigger, investigated not assumed**: adopt a proactive ~66%-
   context restart ONLY where a provider exposes real context accounting;
   never the guesswork heuristic alone. Record per-provider findings
   either way.

Adopter-facing template changes carry RESYNC entries; the prompt catalog
regenerates.

**Orphan fold-in (owner-directed 2026-08-22):** this row's telemetry
investigation DISCHARGES the decomposition debt on `SR-177` (fan-out
utilisation reported from the run's own telemetry — mint its LLR/TC while
in that surface), and the template review mints the missing TC for
`LLR-164` (the generated prompt catalogue + freshness gate), which this
row regenerates anyway.
