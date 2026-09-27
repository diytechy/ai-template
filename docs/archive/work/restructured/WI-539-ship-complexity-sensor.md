+++
id = "WI-539"
title = "Ship the complexity sensor's opt-in layer, structural-move commit rule and deep-module-design skill (OI-68 phase 3)"
specref = "docs/plans/2026-08-29-complexity-sensor-plan.md#phase-3--ship-it-downstream"
workstream = "process"
sr_refs = []
needs = ["WI-538"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Restructured into WI-657.

## Context

Phase 3 of the complexity-sensor plan (specref), minus what has shipped.
WI-639 (`2fd49811`) put `scripts/check_complexity.py` in `bootstrap.MAPPING`,
with its README kit-contents row and a RESYNC_PACK.md entry, and ships the
complexity measure report-only through the template's active
`[step:readability]`, in place of the commented `[step:complexity]` the plan
drafted.

IN SCOPE, the plan's phase-3 items 3 to 5, which are still absent:

- `PROCESS_OPTIONS.md` gains the "Complexity ratchet" opt-in layer and its
  Applies-when index row, in document order (plan §1.6), pointing at the
  shipped report step and census rather than the commented step the plan
  drafted.
- `PROCESS.md` §3 gains "A structural move is its own commit", after the 0→A→B
  bullet and before Thin orchestrators (plan §1.7).
- A `deep-module-design` skill under `project-trajectory/skills/`
  (`scope: kit`, `domains: [any]`, under 4 KB), with `INDEX.csv` regenerated
  and, if this repo dogfoods it, byte-identical copies under `.claude/skills/`
  and `.agents/skills/` (plan §1.8).
- The RESYNC_PACK.md entry for the layer and the skill (plan §1.9).

NOT IN SCOPE: the MAPPING row, the README row and the template step (shipped),
and arming or retiring any sensor in this repo.

## Done-when

- `PROCESS_OPTIONS.md` has the "Complexity ratchet" section and its
  Applies-when index row in document order, and the section names the shipped
  report step and census as the way to arm it.
- `PROCESS.md` §3 has the structural-move bullet between the 0→A→B bullet and
  Thin orchestrators, and both watched docs' byte deltas are flagged with a
  reason and re-stamped in `byte-budget-guard` (source and tracked copies).
- The `deep-module-design` skill is under `project-trajectory/skills/`,
  `INDEX.csv` is regenerated, `gen_skills_index.py --check-agents` passes, and a
  scaffold bootstrapped from the kit carries the skill byte-identical to its
  source.
- `RESYNC_PACK.md` has an entry for the layer and the skill, and the commit bar
  passes.
