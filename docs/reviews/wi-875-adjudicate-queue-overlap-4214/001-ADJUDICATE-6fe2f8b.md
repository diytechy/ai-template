# ADJUDICATE — WI-875 — queue overlap at 6fe2f8b9

Independent adjudication of the 30-row cluster the consolidation census minted
(digests `42148aa80898|2868eb7d03d5`, unchanged when judged).

Disclosure. Besides the brief I read WI-855's three sittings
(`docs/reviews/wi-855-adjudicate-queue-overlap-2042/001`–`003`), which judged
26 of these 30 rows eight days of queue ago; WI-866's closed spec;
`consolidate.edged_text`; `tests/test_conftest_isolation.py`; the
`StoreBusy` sites in `session_keep.py`; and the design's ch.2 §3 step 2 and
ch.4's actor-independence row
(`docs/plans/2026-10-04-wi788-design/4-adjudication-mint-landing.md`). I
checked the state of every row the cluster's `needs` name: WI-797, WI-803,
WI-806, WI-818, WI-821, WI-835, WI-846, WI-849, WI-852, WI-860 and WI-865 are
complete. HEAD stayed at 6fe2f8b9 throughout.

**What changed since WI-855.** Its edges are in the files (WI-834 needs
WI-846, WI-847 needs WI-834, WI-800 needs WI-847, WI-851 needs WI-849, WI-808
needs WI-832, WI-801 needs WI-852, WI-798 and WI-848 its hand edges and
Done-when bullets, WI-833 needs WI-828 and WI-832). WI-811 lost its WI-805
edge by the owner's ruling of 2026-10-08 and gained WI-865, now complete. Four
rows are new: WI-856, WI-857, WI-858, WI-859. WI-855's judgement on the other
26 stands, and I do not re-litigate it. This sitting judges the new rows
against the rest, and the orderings that the released prerequisites have
made claimable together.

**Shape 1, contradiction with the spine: none.** WI-858's lockless durable
marker could look like a breach of SR-227's "write the retention state only
whole, by one writer at a time". It is not one. The record is still written
whole under the store lock. The marker is a separate file, written whole,
applied by the next locked read: the tombstone protocol LLR-270 already
states. WI-856 inserts a frontmatter line and keeps the waiter's scope text
byte-identical, which SR-220 permits. WI-857 extends SR-178's chain as WI-849
left it. WI-859 cites no SR.

**Shape 3, already answered: none.** WI-866 (complete) made the close write
every edge on one waiter. It did not widen `edged_text`, which still returns
None at `consolidate.py:1425` for a row with no `needs` line, so WI-856 is
still owed. WI-859's defect is live: the test still takes
`out.strip().splitlines()[-1]` as the summary (`test_conftest_isolation.py:52`).
WI-858 is the owner's 2026-10-08 move of WI-846's dropped release marker, and
no closed row built it. No cluster row is an earlier consolidation's
successor, and every earlier absorption is marked `(by hand)`.

**Consolidation: none.** Each new row is its own decision. WI-857 and
WI-809 build one actor test from two directions. The owner split WI-857 out
of WI-849 as its own row, and WI-809 is the whole S788 sitting. Folding the
smaller row into the larger would undo a deliberate cut and make the design's
largest slice larger. Ordering them is the answer.

**Shape 2, scope overlap: five unordered collisions get an edge.**

- [MAJOR] WI-858 -> WI-834, WI-847 and WI-858 all change the retained
  session's lease and its retirement in `session_keep` (`keep_for`,
  `keep_bookkeep`, the store lock) and amend LLR-270. WI-834's blackout
  retires lazily at the first `keep_for` after the window. WI-847 adds a
  review class to the same keep operation and lease. WI-858 orders a pending
  release before "any expired-lease retirement" on every path. WI-858 and
  WI-834 are both claimable today (WI-846 and WI-835 are complete), and
  nothing orders WI-858 against either. WI-855 ruled the SR-227 and LLR-270
  amendments serial, each rebased on the last. -> add the edge WI-858 needs
  WI-847 (and, through WI-847's own edge, WI-834). WI-858's "every
  release-only path" then covers the review class's lease and the blackout
  retirement as landed, rather than a store two lanes are both changing.
- [MAJOR] WI-858 -> WI-800 replaces the store WI-858 changes (one
  `out/sessions/store.toml` absorbs `out/adjudicator/`, and LLR-270 is
  shared). WI-858 says its rule "moves with the store" if WI-800 lands first.
  That leaves the order to whichever lane gets there first, and a store
  rewrite built beside an open protocol change can drop the guarantee without
  a gate noticing. -> add the edge WI-800 needs WI-858. WI-800 then carries
  the durable release into the new store, and its RESYNC store reset covers
  the marker files.
- [MAJOR] WI-857 -> WI-809's sitting refuses "an act by a session that ch.2's
  judged-scope table makes ineligible", which ch.4's actor-independence row
  defines as "a different session from every build, plan and author-review
  session of those rows". WI-809 also says "with no second actor test". WI-857
  builds that test on the same rung (WI-849's verdict-backed approval act):
  the binding records the judging session, authoring calls leave a session
  record, and an act backed by an authoring session's verdict is refused.
  Nothing orders them. WI-857 needs WI-849 and WI-801, and WI-809 waits on
  WI-801 only transitively, so both can be claimable together. Built in
  parallel, the rung gains two actor tests over two records of who authored
  what. -> add the edge WI-809 needs WI-857. WI-809's ch.2 eligibility
  condition then extends WI-857's session records and refusal, and WI-809's
  "no second actor test" binds to WI-857's test.
- [MINOR] WI-856 -> WI-810 folds the consolidation step into MINT
  (`adjudicate-consolidate` into the MINT brief) over the same close path
  (`consolidate.py`, `handback`, LLR-210's transforms). WI-856 widens
  `edged_text` and amends LLR-210's detail. WI-856 is ready and small, and
  WI-810 is deep in the graph, so a same-day claim is unlikely, but nothing
  orders them. -> add the edge WI-810 needs WI-856, so the fold carries the
  widened transform.
- [MINOR] WI-853 -> WI-811's Done-when has a resolved dispute count as
  covered "for WI-853's findings gate", which WI-853 builds. WI-811's path to
  WI-853 ran through WI-805, and the owner dropped that edge on 2026-10-08,
  so nothing now orders WI-811 after the gate it extends. -> add the edge
  WI-811 needs WI-853.
- [MINOR] WI-848 -> its review-steps bullet holds rules 2 and 3 as procedure
  "until WI-865 lands", and WI-865 is now complete. Its reconcile bullet
  ("reconciled with every row landed since 2026-10-07") already covers this,
  so the skill should describe WI-865's landed dispute path, not the interim
  one. No edge or text change is needed. Recorded for the builder.

WI-859 shares only a generic specref (`docs/work/README.md`) with WI-858 and
collides with nothing. WI-850 and WI-851 both add a rider to WI-828's
lane-commit walk. Their spine rows differ, and their collision is textual,
which a rebase resolves. WI-809 already waits on both.

OUTCOME: QUEUE-WITH-EDGE needs=WI-858;WI-800;WI-809;WI-810;WI-811 absorbs=-
