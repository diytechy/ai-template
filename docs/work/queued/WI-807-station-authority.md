+++
id = "WI-807"
title = "The station authority, lane-side claims and cancellation"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-station-authority"
sr_refs = ["SR-170"]
needs = ["WI-799", "WI-800"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-station-authority (ch.4 §2-§3, §11; OI-103
Q1). One fenced lease, `out/station/authority.json` under the primary checkout
(found through the git common directory), is the tool's only way to trunk: a
generation counter, a `[station] authority_ttl_minutes` expiry dial shipped at 120
and renewed per step, and a filesystem that cannot lock refuses (D-016). Every ref
advance re-checks the generation and swaps the ref inside one critical section.
Nothing waits while holding it (README "How the locks and the lease compose").
Claims move lane-side as a create-only ref, `out/integrate.lock` retires into the
authority, and the owner can cancel with `lane_state.py release --reason` (D-025).
The authority is approved as designed, with the landing's hold time a named
iteration point (README A4). The pause file stays the owner's gate (README Q-12
(a)). The writer census belongs to WI-813, the last writer move (D-026).

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- One acquirer wins and the other is refused, with the holder named.
- An expired or cancelled holder cannot advance a ref (the check and the
  `update-ref` swap are one critical section).
- An unlockable filesystem refuses, naming the cause.
- A claim is refused while a landing holds the authority, and succeeds after.
- Nothing that holds the authority waits: a test holds a lease elsewhere and sees
  the holder take a fresh session at once.
- A cancelled sitting is stopped, its usage harvested, and the lane derives
  `PARKED`; its relaunch gets the reconcile note.
- Today's landing (`integrate_one`) takes the authority; `out/integrate.lock` is
  gone; the pre-commit hook's advisory check refuses an owner commit while a holder
  has the authority.
- Each spine row the README matrix gives this row (SR-170, LLR-151, a new authority
  row; LLR-137 shared with WI-800; LLR-246 shared with WI-800 and WI-810) is amended
  or added and passes adjudication of that row, on whichever adjudication path is
  the one path when this row lands.
- The row's test bar: its affected modules' tests (integrate, dispatch, session)
  plus the smoke tier at `-n 2`; no extra bar is named.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; `out/integrate.lock` retires and
  `[station]` is added.
