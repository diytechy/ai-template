+++
id = "WI-1003"
title = "The seam check resolves dotted and relative imports, so edges into kitlib/* and rendering/* are checked"
workstream = "process"
sr_refs = ["SR-159"]
specref = "docs/plans/2026-11-11-oi130-rescore/README.md#defects-in-the-live-partition"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request) from defect 2
of the OI-130 re-score record, the first of the three rows the 2026-11-11a
handoff left unfiled (its owner item 3). Its scope critique is owed before a
claim.

`trajectory_arch._classifiable_edges` resolves each `Imports (internal):`
entry by its bare stem against the inventory, so `kitlib.spine` never matches
`scripts/kitlib/spine`. Every import into `kitlib/*` or `rendering/*` is
skipped, and SR-159's "cross-component import no declared interface covers"
goes unreported for those edges. The record counts 10 such edges with no
interface row; three of them are `check_perf` to `kitlib/spine`,
`check_privacy` to `kitlib/secret_classes` and `rejudge` to
`kitlib/observation`. CMP-006's note says the edges into `kitlib/station` and
`kitlib/verdict` are "policed as an interface row"; this check cannot see
them.

Where the fix sits is the plan's to find: `gen_arch_map` emits the import
lines `_classifiable_edges` reads, so the dotted name may already be lost
there.

## Done-when

- [ ] A dotted import (`import kitlib.spine`, `from kitlib import spine`,
      `from kitlib.spine import x`) and a relative import inside a package
      resolve to their inventory module, and the cross-component rule
      classifies the edge. A bare stem resolves as today; an unknown or
      ambiguous name is still skipped.
- [ ] Each edge this makes visible is covered by an interface row, or is named
      in the Deliverable with the successor row filed for it. The row lands
      with `trace.py --strict` and `check_trajectory.py --strict` clean.
- [ ] CMP-006's note matches what the check now sees.
- [ ] Regressions name each import form above, and the unchanged bare-stem,
      unknown and ambiguous cases.
