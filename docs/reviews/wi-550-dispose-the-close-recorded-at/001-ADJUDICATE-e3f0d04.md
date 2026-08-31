# WI-550 — adjudication of the WI-540 partial close

Close report: `docs/handbacks/WI-540-wi-540-adjudicator-retention-layer.md`
Commit range: `9abdb5d982..a83418f58c`
Judged at: HEAD `e3f0d04`

## What actually happened (established from the commits, not the report)

The lane did not merely crash on entry. It passed BUILD (`df5a2863`), stood up
`adjudicator_session.py` (736 lines) + tests (742 lines) + the `[adjudicator]`
dial + spine amendments, ran a full REVIEW-A that returned **CHANGES-REQUESTED,
findings=6** (`002-REVIEW-A-bb31d58.md`), and reworked all six in `223cd88a`
(route-keyed store, template-fed governing hash, OPENAI/OPENCODE telemetry
wiring). The lane then stalled at the DESIGN-CHECK gate — ERROR (`6210a254`)
then TIMEOUT (`f060a6f5`) — and the worker exited 4. The dispatcher committed
the work as-is (`a83418f5`) and closed partial (`d3fadb42`).

A §A3 red-close handback (`ee13eb37`) then reverted every product commit back to
`9abdb5d982` because the §A2 refresh bar refused (exit 1), preserving the failing
diff as `docs/work/handback/wi-540-adjudicator-retention-layer.patch`. A second
handback (`10f789ff`) restored the burned mark IF=174 and regenerated the
approval brief so the inert artefact could merge. It merged at `9bb80db9`.

## Verification performed for this ruling

- `git diff 9abdb5d982 HEAD -- project-trajectory/scripts tests/test_adjudicator_session.py` → empty. Trunk product code is byte-identical to the pre-work base.
- `grep -rln adjudicator_session project-trajectory/scripts tests` → no dangling references.
- `python -m pytest -q -n auto -m smoke` → **1427 passed, 6 skipped in 31.49s**. Trunk is bar-inert and green.

## Findings

- [MINOR] The report's "Not delivered" ("nothing can be assumed met") undersells real, reviewed progress -> true of trunk STATE but the diff passed BUILD and a full REVIEW-A round whose six findings were reworked in `223cd88a`; treating this as a from-scratch loss would waste ~3800 lines of review-addressed work -> the successor picks up the preserved patch, it does not rebuild -> @owner
- [MINOR] The keep/discard split in the report is empty (`keep_commits=[] discard_commits=[]`, `split_decided_by="adjudicator"`) -> by design for a crashed-worker close the dispatcher had no view, so the split was DEFERRED to this row, not negligently omitted; the danger this rung guards (red left on trunk) did NOT occur — the §A3 handback already reverted all product commits and I verified trunk byte-identical to base + smoke green -> RULING: DISCARD every product commit in the range (already reverted); KEEP the close report, the preserved `.patch`, and the burned-mark(IF=174)/approval-brief bookkeeping -> @owner
- [MAJOR] The proximate blocker was the DESIGN-CHECK gate (ERROR `6210a254`, then TIMEOUT `f060a6f5`), not a defect the REVIEW-A rework left open -> a successor that only re-applies the patch and re-runs the bar will hit the same wall that exited the worker 4 -> the successor MUST first reproduce and resolve the DESIGN-CHECK error/timeout, then re-run the §A2 refresh bar to green, before re-landing -> @owner
- [MINOR] IF-174's id is burned (id-watermark IF=174) while its interface row was reverted out of `interfaces.toml` -> a from-scratch rebuild that re-mints the seam under a new IF id would strand the spent 174 and desync the patch's LLR-163/TC-157/IF-064 amendments -> the successor MUST re-land via the preserved patch so IF-174 and its spine amendments re-appear against their already-allocated marks -> @owner

## Ruling

Outcome PARTIAL is correct: real progress exists and is preserved as a patch,
but no Done-when is met on trunk and the layer is still wanted (WI-541 in
`queued/` blocks on it). Not COMPLETE (nothing shipped), not CANCELLED (the
program still needs the layer). One successor drafted in this row's
`## Dispositions`, superseding WI-540, re-landing the patch inert at dial 0.
The design is fully settled (plan §2–§5 + OI-69 a–e), so this is a build/repair,
not a design fork — no dual planmode. Remaining scope (re-land a 3876-line diff
across the live agent_loop/dispatch seams + resolve the gate failure that
crashed the worker) is strong-tier, above the report's suggested `medium`.

OUTCOME: PARTIAL successors=1
