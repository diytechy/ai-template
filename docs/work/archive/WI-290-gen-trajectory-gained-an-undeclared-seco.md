+++
id = "WI-290"
title = "gen_trajectory gained an UNDECLARED second cross-CMP sibling import at WI-284 - the Ready-frontier feature added `import schedule` (CMP-002 gen_trajectory -> CMP-004 schedule) directly, but IF-056 declares check_trajectory as gen_trajectory's ONE sanctioned sibling import (the dashboard derives THROUGH the validator so rules live in one home), and no IF-### seam is declared for the schedule edge - so check_trajectory --strict reds the G3 trajectory gate (pre-existing at 3033b57, surfaced by the 2026-07-24 gate run; the loop never ran the full G3 check.py, only the smoke bar). Fix (design call): either route the frontier derivation THROUGH check_trajectory (which already imports schedule per IF-053, preserving the single-sanctioned-sibling architecture) OR declare schedule as a justified second seam in interfaces.csv with the right SR-Refs. NOT a drive-by - it revisits WI-284's architecture."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
order = 287
+++

## Deliverable

Option B (owner-chosen 2026-07-24): declared IF-071 (gen_trajectory Consumes schedule - the frontier DECISION seam IF-053 already named for 'the dashboard') and reworded IF-056 to name it the DERIVATION-loader seam distinct from the frontier seam. check_trajectory --strict no longer flags the CMP-002->CMP-004 edge. Hand-applied.
