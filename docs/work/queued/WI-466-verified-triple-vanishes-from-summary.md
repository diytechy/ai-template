+++
id = "WI-466"
title = "trace.py's summary line hides the whole verified-mechanized/demonstrated/attested triple when the demonstrated and attested sets are both empty: the guard at the triple's print site conditions on `(demonstrated_verified or attested_verified)`, so a still-true nonzero mechanized count stops printing the moment the other two legs drain to zero. Driven live at re-tier v2 S3 (log 2026-08-16e): SR-034 (Analysis) and SR-036 (Inspection) were the registry's only two demonstrated-verified rows, both flipped Modified by the R2 reword, and the summary line silently lost the triple — the attested-vs-mechanized split the gate-advance skill reports now renders as nothing. Fix: print the triple whenever ANY leg is nonzero (or always, zeros included — decide against the surrounding line's conventions); add the regression test the current shape lacks (mechanized>0, demonstrated=0, attested=0 must still print). Display-only — no gating logic touches this value."
specref = "docs/log.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Found by the re-tier v2 S3 rewording session (2026-08-16): the amend-flip
discipline drained the demonstrated-verified set to zero and the summary
regression surfaced. The counts themselves are computed correctly; only the
print guard is wrong. The gate-advance skill's attested-vs-mechanized
reporting reads this line, which is why a hidden nonzero count matters more
than a cosmetic quirk.
