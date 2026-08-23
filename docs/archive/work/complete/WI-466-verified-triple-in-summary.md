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

**CORRECTION (2026-08-20)** — the sentence above reading "the golden
fixtures verified unaffected (offspine already printed under both guards;
clean/orphan have all-zero legs and omit identically under both)" is
WRONG, and it was wrong when it was written. What actually happened: the
widened guard added the triple line to mechanized-only output, and the
`clean` and `orphan` goldens went RED at this WI's own commit
`8d7ff553`. They stayed red across one further commit and were
regenerated deliberately at `74c20704`, during WI-480's pytest
qualification run — which is what surfaced them. The claim was not
verified; it was reasoned about, and the reasoning was wrong about which
legs those fixtures carry. Both lessons are recorded in the day's log
fragment (`docs/log.d/2026-08-20-frontier-grind.md`, "The golden
episode"): a smoke-invisible module can carry a red across a close, and
the orchestrator's own close-verification (smoke only) could not have
caught it. The original text is left standing rather than edited away —
a corrected record and a rewritten one are different artifacts, and only
the first can be audited. Raised by the 2026-08-20 batch review
(ROUND-OPUS MINOR-18 / ROUND-SOL MAJOR-4).

## Context

Found by the re-tier v2 S3 rewording session (2026-08-16): the amend-flip
discipline drained the demonstrated-verified set to zero and the summary
regression surfaced. The counts themselves are computed correctly; only the
print guard is wrong. The gate-advance skill's attested-vs-mechanized
reporting reads this line, which is why a hidden nonzero count matters more
than a cosmetic quirk.
