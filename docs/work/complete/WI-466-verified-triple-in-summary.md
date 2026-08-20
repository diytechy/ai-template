+++
id = "WI-466"
title = "trace.py's summary line hides the whole verified-mechanized/demonstrated/attested triple when the demonstrated and attested sets are both empty: the guard at the triple's print site conditions on `(demonstrated_verified or attested_verified)`, so a still-true nonzero mechanized count stops printing the moment the other two legs drain to zero. Driven live at re-tier v2 S3 (log 2026-08-16e): SR-034 (Analysis) and SR-036 (Inspection) were the registry's only two demonstrated-verified rows, both flipped Modified by the R2 reword, and the summary line silently lost the triple — the attested-vs-mechanized split the gate-advance skill reports now renders as nothing. Fix: print the triple whenever ANY leg is nonzero (or always, zeros included — decide against the surrounding line's conventions); add the regression test the current shape lacks (mechanized>0, demonstrated=0, attested=0 must still print). Display-only — no gating logic touches this value."
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Fixed `trace.py`'s summary-line print guard (`render_console`, ~:4195) so
the verified-mechanized/demonstrated/attested triple prints whenever ANY
leg is nonzero — a nonzero mechanized-only count (the common shape) was
previously hidden the moment the other two legs drained to zero, exactly
as happened live at re-tier v2 S3. Regression test
`test_verified_triple_prints_when_only_mechanized_is_nonzero` added; the
golden fixtures verified unaffected (offspine already printed under both
guards; clean/orphan have all-zero legs and omit identically under both).
trace.py's ratchet baseline re-stamped 4510 → 4515 with the reason in
place. The repo's own run now shows `verified-mechanized=69
verified-demonstrated=3 verified-attested=0` live — the attested-vs-
mechanized split the gate-advance skill requires reporting is visible
again. test_trace.py 82 passed; smoke 1209/5; integrity 0.

## Context

Found by the re-tier v2 S3 rewording session (2026-08-16): the amend-flip
discipline drained the demonstrated-verified set to zero and the summary
regression surfaced. The counts themselves are computed correctly; only the
print guard is wrong. The gate-advance skill's attested-vs-mechanized
reporting reads this line, which is why a hidden nonzero count matters more
than a cosmetic quirk.
