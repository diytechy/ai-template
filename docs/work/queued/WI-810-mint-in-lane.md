+++
id = "WI-810"
title = "MINT in the lane: one allocator, the consumption list and station lanes"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-mint"
sr_refs = ["SR-215", "SR-220"]
needs = ["WI-809", "WI-821", "WI-851", "WI-852", "WI-856"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-mint (ch.4 §3, §4.3, §8, §11; LS6).
`intake._mint` runs in the lane at the lane's refreshed watermark, as the one
allocator. The consumption list enumerates every item a sitting must dispose of,
each getting exactly one of `open-item` (with its WI-790 placeholder row),
`decision`, `successor` or `no-action`; consolidation folds into the same step.
Intake's post-merge arms move before the merge, so the landing carries every mint
and `sweep` retires (README change 6). CLI and idle mints and a coordinator's
filings go through a station lane that mints its own carrier row (README Q-7 (a)).
Owner-owed items never hold the sitting (OI-103 Q2). WI-790's contracts are complete
and dropped from `needs`.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

Ordering (coordinator, 2026-10-04): it needs WI-821, which makes the consolidation
census's commissioning signal section-aware and amends LLR-210 first; this row
folds the census into the mint step on top of that rule.

## Done-when

- An undisposed item refuses the mint.
- `open-item` yields a blocked placeholder row.
- A settled amendment is never minted.
- A merge re-judge is minted in the lane.
- An exhausted lane's upheld findings become its successor's Done-when.
- A minted successor passes the scope critique (ruling 2's two questions,
  rendered by WI-852) before it can be claimed.
- A coordinator's filing lands through a station lane.
- Sequential sittings never collide on an id.
- `adjudicate-consolidate` folds into the MINT brief.
- Each spine row the README matrix gives this row (SR-215, SR-220,
  LLR-153/154/255/264, TC-147/148/248/260, IF-090/229/243, IF-123, IF-228; LLR-246
  shared with WI-800 and WI-807; a new consumption-completeness row; LLR-265,
  TC-261 and IF-244 retired with `sweep`) is amended, added or retired and passes
  in-lane adjudication.
- Its LLR-246 amendment follows WI-851's state rule; it adds no per-writer
  held-status arm.
- The row's test bar: its affected modules' tests (intake, consolidate) plus the
  smoke tier at `-n 2`; no extra bar is named.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; `intake.py sweep` retires and
  idle mints land through station lanes.
