## 2026-09-02 — the backlog restructure: WI-579..583 minted, eight rows archived as restructured, the frontier re-sequenced

Executed out of band (owner direction, this date) per
`docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.4 steps
3–7, on top of the vocabulary commits `038a16a7` (the `restructured` terminal
state) and `36395b54` (list-valued `supersedes`) recorded in
`2026-09-02-restructured-vocabulary.md`.

**Step 3 — the mint (`1c0fb2d6`).** Five drafts through `intake._mint`, the
same path every mechanical mint takes: ids from the watermark (WI-579..583;
mark bumped to `WI = 583` by `trace.bump_watermark` in the same commit),
Context written with the registry joins, `supersedes` lists applied. The
absorbed rows' Done-when blocks are quoted verbatim under their old ids in
each successor's Context.

**Step 4 — the moves.** WI-558, 559, 560, 561, 562, 564, 565, 576 moved
`queued/ -> docs/archive/work/restructured/` with `spec_move.py` (links
redirected), a one-line `## Deliverable` naming the successor(s) placed before
`## Context`, and `specref` cleared. The clearing was NOT in the plan's §1.5
text: the strict check errored R-F on all eight rows ("status=restructured
but SpecRef ... is still set — a terminal WI clears the SpecRef"), which is
the same rule every terminal move obeys; §1.5 now says so. No open row
hard-depended on an absorbed id, so `_replace_inbound_edges` had nothing to
re-point.

**Step 5 — the kept rows.** `WI-551` `needs = ["WI-579", "WI-580"]`,
`priority = 7`; `WI-541` `priority = 7`; `WI-545` `needs = ["WI-579",
"WI-580", "WI-581", "WI-551", "WI-583"]`, `priority = 1`.

**Step 6 — verification, real output.**

`schedule.py ready --explain`, open rows only:

```
WI-582     ready     exclusive    rank=0 P4   exclusive:spine;ready
WI-578     ready     exclusive    rank=1 P0   exclusive:adjudication;ready
WI-579     ready     parallel     rank=6 P9   parallel:ordinary;ready
WI-580     ready     parallel     rank=6 P8   parallel:ordinary;ready
WI-551     waiting   parallel     rank=6 P7   waiting:hard-preds-not-done:WI-579,WI-580
WI-541     waiting   parallel     rank=6 P7   waiting:hard-preds-not-done:WI-551
WI-581     ready     parallel     rank=6 P6   parallel:ordinary;ready
WI-570     ready     parallel     rank=6 P5   parallel:ordinary;ready
WI-583     waiting   parallel     rank=6 P5   waiting:hard-preds-not-done:WI-579,WI-570
WI-577     waiting   parallel     rank=6 P4   waiting:open-item-pending:OI-82
WI-557     ready     parallel     rank=6 P3   parallel:ordinary;ready
WI-536     ready     parallel     rank=6 P2   parallel:ordinary;ready
WI-539     ready     parallel     rank=6 P2   parallel:ordinary;ready
WI-556     ready     parallel     rank=6 P2   parallel:ordinary;ready
WI-545     waiting   parallel     rank=6 P1   waiting:hard-preds-not-done:WI-579,WI-580,WI-581,WI-551,WI-583
```

`WI-545` is no longer ready (the §2.1 contradiction). `WI-578` is admitted
first at dispatch (`_judgement_first`); `WI-582` classifies `spine` and will
batch with whatever `WI-578` drafts. The scheduler's total order puts rank-0
spine ahead of rank-1 adjudication, which is the ruled table; the dispatcher's
judgement-first partition is what actually admits.

`check_trajectory.py --strict`: ONE error, pre-existing and now owned by
`WI-582` — `cross-component import scripts/schedule (CMP-008) -> scripts/trace
(CMP-006) has no declared IF-### seam`. The shared-spec-of-record warnings
fell from eight pairs to two (`WI-556/557/579` on open-items.toml,
`WI-580/581` on the 2026-08-31 plan), which are honest: those rows ARE one
ruling each. `trace.py --strict-integrity`: integrity=0, orphans=2 (unchanged).
`docs/status.md` regenerated; zero absorbed ids remain in it.
