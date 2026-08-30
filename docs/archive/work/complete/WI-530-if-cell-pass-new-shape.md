+++
id = "WI-530"
title = "The cell pass on the new shape: each definition into its owner's header, channel confirmed, data written (OI-67 slice 3)"
workstream = "architecture"
sr_refs = ["SR-159"]
needs = ["WI-528", "WI-529"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Every interface definition lives beside the code. Record:
[../../../log.d/2026-08-29-wi530-cell-pass.md](../../../log.md#2026-08-29--wi-530-the-cell-pass-on-the-new-shape-oi-67-slice-3);
the four-worker round whole at
[../../../reviews/2026-08-29-oi67-slice3/](../../../reviews/2026-08-29-oi67-slice3/README.md).

132 of 136 rows state their contract in the owner's header and carry no legacy
`contract` cell; every `Contracts:` marker declares exactly the registry's rows
for its file (50 markers trimmed, 6 headers and 5 READMEs created); 7 channels
and 4 far sides corrected from the seed; 14 moot reason cells deleted; the
reference reads 68 sources / 132 seams / 132 stated; the owner-exact check
warns on one row. Not done, stated: `IF-031` (a `#` header on a CSV breaks
five loaders — slice 6 fixes the loaders) and the three `external:`-owned rows
(the home for our reading of an external surface is slice 6's rule) keep
their legacy cell, counted by the advisory. The split worklist and the two
latent defects are in the fragment.
