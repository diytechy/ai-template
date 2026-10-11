# ADJUDICATE — WI-900 — queue overlap at e71b776

Independent adjudication of the 29-row cluster the consolidation census minted
(digests `7dd6770f2f97|5db3bfb6e636`, unchanged when judged; HEAD stayed at
e71b7760a throughout).

Disclosure. Besides the brief I read WI-875's verdict
(`docs/reviews/wi-875-adjudicate-queue-overlap-4214/001-ADJUDICATE-6fe2f8b.md`),
which judged 24 of these 29 rows on 2026-10-09; the trunk log since it landed
(5f5f77629..e71b7760a); decisions D-008, D-010, D-012 and D-015 in
`docs/decisions/coordinator-2026-10-10.toml`; OI-113; and the keep-warm and
binding sites in `session_service.py`, `session_keep.py`,
`adjudicate_brief.py` and `coordinator_adjudicate.py`. I checked the state of
every prerequisite the new rows name: WI-828 closed partial; WI-834, WI-846,
WI-847, WI-848, WI-849, WI-852, WI-853, WI-854, WI-859, WI-881 and WI-884 are
complete.

**What changed since WI-875.** WI-875's edges are in the files. WI-847 landed
only its step 1; the owner split step 2 out (D-008), and the coordinator split
it again into WI-884 (complete) and WI-887 (D-012), moving WI-858's need to
WI-887. WI-828 closed partial; its shared walk re-homed to WI-892 and its
hand-merge path to WI-893 behind OI-113 (D-015), with WI-833, WI-850 and
WI-851 re-pointed at WI-892. Six rows are new to a census: WI-878, WI-887,
WI-892, WI-893, WI-895, WI-897. WI-875's judgement of the rest stands and I do
not re-litigate it; this sitting judges the new rows, and the rows whose text
the 2026-10-10 splits left behind.

**Shape 1, contradiction: one.** WI-802's Done-when still carries WI-855's
finding 4 as written on 2026-10-08, before the owner's 2026-10-10 ruling, and
no later commit reconciled it (its file was last touched by WI-855).

- [BLOCKER] WI-802 -> its bullet "The [review] family carries WI-847's
  within-lane retention dial into `[sessions.review]` (shipped off; the
  merge-gating review is always fresh) ... and WI-847's tests stay green"
  contradicts the owner's ruling D-008 (coordinator-2026-10-10.toml), which
  WI-887 builds: "the final reviewer is configurable, either a fresh session
  or a persisted independent final reviewer", fresh only by default. WI-887
  also amends SR-227 "to cover the review class and the final reviewer's
  configuration", and WI-802 lands after it (WI-802 -> WI-801 -> WI-800 ->
  WI-858 -> WI-887), so a WI-802 lane built and reviewed against its own row
  would pin the gating review fresh and remove the owner's persisted mode,
  against the SR as amended. Its referents are also stale: WI-847 landed with
  no retention dial and no retention tests; both are WI-887's. -> return
  WI-802 to draft. Its Done-when names WI-887's two dials (within-lane review
  retention, and the final reviewer's mode with its own persisted scope) as
  what `[sessions.<family>]` carries, states which family's reset terms the
  persisted final reviewer takes, and replaces "WI-847's tests" with WI-887's.
  Its needs on WI-887 is already transitive; a direct edge would make the
  dependency legible.

**Shape 3, already answered: none.** WI-878's defect is live: the `.requested`
binding still holds only brief, kinds and outcome (`adjudicate_brief.bind_pending`).
WI-895's swallow is live (`session_service.py:1284`,
`except BaseException` in `KeepWarmer._ping`). WI-892 and WI-893 carry
WI-828's scope forward rather than repeat a landed one. WI-897 repeats no
row. No cluster row is an earlier consolidation's successor, and every earlier
absorption is marked `(by hand)`.

**Consolidation: none.** WI-892 and WI-893 share SR-140 and the walk, but one
is a behaviour-free structural move that lands now and the other waits on the
owner's OI-113; folding them would hold the move behind the ruling, which
D-015 split them to avoid.

**Shape 2, scope overlap.** The return above is this sitting's outcome, so no
edge is enacted. The following are recorded for the coordinator and for the
next census, which re-judges the cluster once WI-802's return changes the
queue sha:

- [MINOR] WI-878 -> WI-801 deletes `coordinator_adjudicate.py` and moves the
  entry point's callers and tests to the adjudicate kind; WI-878 adds the
  findings-file record to the binding that entry point writes at reservation.
  WI-878 is ready and WI-801 deep, so the order will almost surely hold, but
  nothing states it. -> the edge WI-801 needs WI-878, so `ask` carries the
  record and WI-878's tests move rather than drop.
- [MINOR] WI-878 -> WI-811's bullet makes a builder-disputed, adjudicator-
  resolved finding count as covered for WI-853's gate, citing the
  resolution; WI-878 changes how the gate shows that a cited ruling ruled
  that finding (the binding's findings file, not a sibling scan). -> the edge
  WI-811 needs WI-878, so the loop's dispute sitting writes and reads the
  same record.
- [MINOR] WI-808 -> its Done-when still names "the shared lane-commit walk
  (WI-828)"; WI-828 closed partial and the walk is WI-892's (D-015). The
  order holds through WI-851 -> WI-892. -> when WI-808 is next edited, point
  it at WI-892. OI-113's option (b), a squash landing carrying a trailer
  naming its archived lane tip, is WI-808's `Lane-Tip:` trailer; if the owner
  rules (b), WI-893's Done-when should reuse that trailer and need WI-808.
- [MINOR] WI-833, WI-851 -> their Done-when bullets judge the hook "on a
  squash or merge landing"; WI-892 builds the squash path and the merge
  slot, and the hand-merge path is WI-893's behind OI-113. Their re-home
  notes say so, and WI-892's one walk with a rider tuple means a rider added
  first rides the hand-merge path when WI-893 adds it, so the order does not
  matter. No edge. A builder should read "merge landing" as WI-893's.
- [MINOR] WI-895 -> WI-887 and WI-858 are both near the keep-warm code
  (WI-887: keep-warm never pings a reviewer record; WI-858: the keep-warm
  skip under contention). Those changes sit in `session_keep`
  (`_warm_candidates`, `take_warm_lease`), WI-895's in
  `session_service.KeepWarmer._ping` and the dispatcher's tick, and LLR-270
  states no ping error handling, so WI-895 amends traced cells at most. A
  textual collision a rebase resolves; no edge.

WI-897 (the guard hook's imports and matcher) and WI-858 (the guard's lock
sites) touch different code in `coordinator_guard.py`. WI-892 and WI-799 both
edit `integrate.py`, both ready; WI-892 is a quick structural move whose
rebase is mechanical. WI-827 lands on trunk by the owner and collides with
nothing.

OUTCOME: RETURN-TO-DRAFT needs=- absorbs=-
