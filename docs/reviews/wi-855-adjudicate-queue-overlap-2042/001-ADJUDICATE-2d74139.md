# ADJUDICATE — WI-855 — queue overlap at 2d741392

Independent adjudication of the 29-row cluster the consolidation census minted
(digests `20424540cd76|1237285c1cff`, unchanged when judged): WI-798 to WI-817
(the S788 rows of the WI-788 design), WI-827, WI-828, WI-832, WI-833, WI-834,
WI-846, WI-847, and WI-848 to WI-854 (the WI-841 retrospective's rows). The
question: does any row contradict the spine, overlap a sibling so that two
lanes would collide, or ask for something already answered? If so, are any of
them one work item under several ids?

Disclosure. Besides the brief I read: the retrospective's queue reconciliation
(`docs/plans/2026-10-07-wi841-retro/PROPOSAL.md` §3 and §8), the WI-788 design's
README change list and ch.2 §2's session-family table, OI-108 to OI-111 in
`docs/requirements/open-items.toml`, `docs/status.md`, WI-834's full spec, the
wave-18 log fragment, and the consolidation close path (`consolidate.py`
`parse_verdict`, `reconcile_refusal` and `edged_text`, and `handback._enact_plan`).
HEAD stayed at 2d741392 throughout.

**Shape 1, contradiction with the spine: none.** No row asks for something a
cited SR forbids. SR-227 is amended by WI-800, WI-802, WI-834, WI-846 and
WI-847. Each amends it in an agreeing direction: retirement across a window, no
retirement on an auth failure, a review class, the store, the families. The
risk is that the amendments run in parallel, not that they disagree (shape 2).
SR-154's three amendments are ordered WI-801, then WI-805, then WI-811, and
WI-852's chain edit is placed before them below. One design-level tension is
recorded as a MAJOR finding rather than a return. Design ch.2 §2 fixes the
[review] family at "every call, fixed in code", and WI-802 builds that table.
WI-847 adds an opt-in dial, shipped off, that resumes the loop's reviewer
within a lane. Off, it agrees with the design. On, it extends the design
without reversing an owner ruling, and the merge-gating review stays fresh.

**Shape 3, already answered: none.** The retrospective's reconciliation of
2026-10-07 (§8.1) already narrowed P2 against WI-808 and WI-809, P5 against
WI-801, and P6 against WI-805, and folded P8 into P5. Every split it made is
honoured by the rows as filed: WI-849 builds the rung and WI-809 the
lifecycle; WI-852 renders and WI-801 launches; WI-853 builds the shared step
and WI-805 the replan. WI-853 and WI-811 both state that a resolved dispute
counts as covered. These are the coordinator's dispute-ruling files and the
loop's sitting record feeding one gate, not one behaviour built twice. No
cluster row is the successor of an earlier consolidation, and every earlier
absorption is marked `(by hand)`.

**Consolidation: none.** The S788 rows are slices deliberately cut from one
approved design, with a filed `needs` graph. The retrospective rows were filed
already narrowed against them. Each row is its own decision. The shared files
and SRs the pre-filter reports are the design's own seams. Where two rows that
can be claimed on the same day would collide, the answer is an edge.

**Shape 2, scope overlap: six unordered collisions get an edge.** Two more
cannot be edged by the machinery and are recorded for the coordinator.

- [MAJOR] WI-846 -> WI-834's part C "authenticates the dedicated home with the
  owner's long-lived token, per WI-846" and reports signed-in "only when the
  configured token is present". Where that token's path is configured is OI-110,
  still pending. WI-834 is ready now and WI-846 is blocked on OI-110. Built
  first, WI-834 would answer the owner's open question in a lane, and the two
  rows would amend SR-227 and LLR-270 in parallel. The reconciliation (§8.2,
  "Sequencing") says to run them one after another, and status says "build
  the token row first or beside it". -> add the edge WI-834 needs WI-846. The
  owner's confirmation of OI-110 (b), already their stated preference,
  releases both.
- [MAJOR] WI-834 -> WI-847 adds a review class to the same keep operation,
  store and lease, and amends SR-227 again. WI-834's part B changes the same
  `keep_for` retirement predicate (the `blackout` reset). §8.2 asks these
  three SR-227 amendments to be serial, each rebased on the last. -> add the
  edge WI-847 needs WI-834.
- [MAJOR] WI-847 -> WI-800 replaces the very store, lease and record WI-834,
  WI-846 and WI-847 each edit: one `out/sessions/store.toml` absorbs
  `out/adjudicator/`, and SR-227 and LLR-270 are shared. WI-800 can become
  ready (WI-798, WI-799, WI-851 then WI-828) while those three still build. ->
  add the edge WI-800 needs WI-847. WI-801 and WI-802 then follow WI-847
  transitively.
- [MAJOR] WI-802 / WI-847 -> design ch.2 §2 gives [review] "No: every call,
  fixed" and "[review] and [judge] are fixed in code". README change 22 retires
  `retain_for`, which WI-847 extends with the review class. With the edge
  above, WI-847 lands first. A WI-802 builder who follows the chapter
  literally would delete WI-847's dial. -> when WI-802 is claimed, its
  Done-when should state that the [review] family carries WI-847's
  within-lane retention dial into `[sessions.review]` (shipped off; the
  merge-gating review always fresh). It should state this rather than pin
  [review] fixed. WI-847's tests must stay green through WI-802. This is a
  text edit for the coordinator or owner; this verdict cannot make it.
- [MAJOR] WI-849 -> WI-851. Both amend LLR-278: WI-849 replaces its approval-act
  actor test, and WI-851 retires its held-CLARITY clause. Both change
  `acceptance_record.merge_approval_refusal` and its `held_reattest_refusal`
  call. Neither waits on the other. WI-849 is ready, and WI-851 is ready once
  WI-828 lands. -> add the edge WI-851 needs WI-849. WI-849 is the one the
  coordinator batches next with WI-848, and WI-808 and WI-809 already wait on
  both.
- [MAJOR] WI-832 -> WI-808's one record check (`_close_record_refusal`,
  LLR-284) reads `record_path(branch)`. WI-832 renames every decisions record
  by work item and moves the existing ones. WI-808 already waits on WI-818 so
  that it reads the post-change key. The same reason holds here. -> add the
  edge WI-808 needs WI-832.
- [MINOR] WI-852 -> WI-801's Done-when reads "the coordinator's briefs reach
  `ask` as WI-852's rendered prompt files", and both amend SR-154's chain. No
  path in the graph orders them. -> add the edge WI-801 needs WI-852. It also
  puts WI-852's SR-154 edit ahead of the WI-801, WI-805, WI-811 sequence.
- [MAJOR] WI-828 and WI-832 -> WI-833 requires that "on a hand squash or merge
  landing, the ruling sync also judges each folded-in commit through the
  shared lane-commit walk (WI-828)", yet it does not wait on WI-828, as WI-850
  and WI-851 do. It also amends SR-225's chain (LLR-283) and
  `kitlib/decisions.py` from the same dispute ruling as WI-832, whose record
  move a disclosure-binding check must not misread as an edit under a verdict.
  WI-833's frontmatter has no `needs` line. `consolidate.edged_text` returns
  None for such a row, so `handback._enact_plan` would refuse any edge with
  WI-833 as the waiter, and with it this whole verdict. -> NOT enacted here.
  The coordinator gives WI-833 `needs = ["WI-828", "WI-832"]` by hand before
  claiming WI-828, WI-832 or WI-833.
- [MINOR] machinery -> a queue-with-edge verdict cannot edge a waiter filed
  without a `needs` line. WI-828, WI-833, WI-848, WI-849, WI-852, WI-853 and
  WI-854 here have none, so an adjudicator must pick around a correct edge. ->
  separate row: `edged_text` inserts a `needs` line into the frontmatter when
  none exists (the row's Context and Deliverable stay untouched), with a test.

OUTCOME: QUEUE-WITH-EDGE needs=WI-834;WI-847;WI-800;WI-851;WI-808;WI-801 absorbs=-
