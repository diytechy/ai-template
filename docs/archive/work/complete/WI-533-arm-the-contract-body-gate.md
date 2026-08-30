+++
id = "WI-533"
title = "Arm the gate: a missing contract body is a strict finding, retired columns are schema findings (OI-67 slice 6)"
workstream = "architecture"
sr_refs = ["SR-159"]
needs = ["WI-530", "WI-531", "WI-532"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

The gate is armed. Record:
[../../../log.d/2026-08-29-wi533-arm-the-gate.md](../../../log.d/2026-08-29-wi533-arm-the-gate.md).

`check_trajectory.contract_body_findings` fails, under `--strict`, a row its
owner declares but does not state, an `external:`-owned row no far-side kit
module states, and a source declaring another owner's row;
`trace.interface_findings` fails a row still carrying any of the five retired
cells, and the legacy `contract` advisory, the schema key, the carrier map,
the template and the shipped docs all drop the cell. The four rows slice 3
could not place are placed: one comment-skipping CSV reader in `kitlib.spine`
lets `performance-budgets.csv` declare `IF-031` in its own header, and the
three `external:`-owned rows are stated by their far-side module — the rule
this slice sets. All 154 rows stated; reference 74 / 154 / 154; the kit's
tree clean under the armed gate and a planted violation fires on it. Sixteen
reason cells trimmed; `gen_okf`'s HTML-comment skip fixed; the slice-4
cross-family round dispositioned (six applied, five deferred with reasons).
Owed, stated in the fragment: this slice's own cross-family round, and the
undeclared-owner case, which stays the reverse check's warn by decision.
