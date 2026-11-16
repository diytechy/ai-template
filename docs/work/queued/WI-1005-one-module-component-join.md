+++
id = "WI-1005"
title = "The module to component join has one home, which gen_components and trajectory_arch both call"
workstream = "process"
sr_refs = ["SR-159", "SR-169"]
specref = "docs/plans/2026-11-11-oi130-rescore/README.md#defects-in-the-live-partition"
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request) from defect 3
of the OI-130 re-score record, the third of the three rows the 2026-11-11a
handoff left unfiled (its owner item 3). Its scope critique is owed before a
claim.

`gen_components.module_components(llrs)` and
`trajectory_arch.module_components(root)` each join the LLR `Component` tags
on `LLR.Module`. Both split with `kitlib.spine.refs` and normalize with
`kitlib.spine.norm_module`, but `trajectory_arch` loads its own rows, drops
example and non-`LLR-` ids and keeps only `CMP-` tags, while `gen_components`
takes the rows it is given and keeps every tag. Only the `trajectory_arch`
copy has a test. `gen_components`' own docstring says a second reconciliation
"would be a second answer waiting to disagree".

The review-churn plan's variant F (phase 3) moves membership onto the
realization. If that lands first it may absorb this row; the critique checks.

## Done-when

- [ ] One function owns the join, both callers use it, and the second copy is
      deleted.
- [ ] Any input on which the two copies disagreed is named in the Deliverable
      with the kept answer, and pinned.
- [ ] The existing test covers the one home, and `gen_components` keeps a pin
      that it calls it.
- [ ] `trace.py --strict` and `check_trajectory.py --strict` are clean, and
      the component view regenerates unchanged or its changes are explained
      in the Deliverable.
