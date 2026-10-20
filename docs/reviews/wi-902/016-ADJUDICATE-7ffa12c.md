# WI-902 adjudication 016: dispute on plan critique 2 (at the plan cap)

Range: `41375927d..7965465a0`, which adds the plan, its one revision and its two critiques. The tree at `7ffa12c6f` adds only the findings file. Scope bound: project-trajectory/PROCESS.md §6 "Review threat model", applied with its plausibility test: whether a supported workflow or the kit's own routes reach the scenario. Only finding F1 is before me, and the coordinator holds no position on it.

## Finding F1: P5's record check refuses a supported close whose relink leaves `docs/work/`

**The facts, read at the range:**
- **The record check's test for a close.** P5 recognizes "the machinery's close" by `kitlib.verdict.mechanical_close_attestation(root, rev) is not None` (plan, P5 "What it judges").
- **The attestor refuses any path outside `docs/work/`.** `_closed_wi_ids` (`kitlib/verdict.py`) returns None for any changed path that does not start with `docs/work/`, and the attestor's docstring states this on purpose: "stops a close whose inbound-link relink reached into product or requirement files from being peeled".
- **The real close relinks across the whole repository.** `handback.close_adjudication` archives each row through `_archive_one_adjudication_row`, which calls `spec_move.move_spec`. That ritual redirects and stages every inbound markdown link in the repository.
- **So a genuine machinery close can fail the attestor.** If any file outside `docs/work/` links to the row's active spec by a relative path, the close is still the machinery's own commit under the composed subject, but the attestor refuses it.
- **P5 makes that refusal final.** For an adopting disposition (a requesting spec moved into `complete/`), P5 refuses every close the attestor declines (D6, D7 and D9), at the merge slot and at the hook.
- **The plan's stated recovery does not exist.** P5's "A residual stated, not built against" says "a person re-closes it". P5 itself refuses a hand close that writes a record (`test_a_hand_close_writing_a_record_is_refused`), and P7 removes the hand route from the prompt and recipes. Every later route fails too:
  - reverting the close removes the record, which D8 refuses;
  - the row has left `active/`, so `close_adjudication` will not run again;
  - any route back to the queue is a forbidden hand act.

  The lane is left with no supported way to land.

**Weighing it under §6:**
- **Reachability.** Nothing here needs a compromised host or a forbidden hand act. A relative link from a review file, plan or log fragment to a spec is ordinary repository content. This repository's reviewers write exactly such links: `docs/reviews/2026-09-27-wave5/sol-batchb*.md` and `sol-batchd.md` link the adjudication specs WI-680, WI-681 and WI-708 by `../../../docs/...` paths.
  - An adjudication lane that drafts or adopts a successor owes a review round under the `adjudication_review` dial. LLR-207 records that this round is drawn while the row is still in `active/`, so the review that links the spec lands before the close that relinks it.
  - Frequency: none of the 18 mechanical closes in this history touched a path outside `docs/work/`. The path is rare so far, but a supported workflow does produce it.
- **Impact, and why this differs from WI-925's F1.** Today the same close only loses its peel: the gate asks for one more review, and the lane lands. Under P5 the same close is refused outright, with no route back. I dismissed WI-925's F1 because that miss failed closed into a hold that an ordinary route (a done-when sitting) released. Here the hold has no ordinary release, and the plan claims one that its own steps forbid.
- **Done-when.** The Done-when requires that "the commit check passes the close's own commit". A supported close that the check refuses is a gap in that promise. It is not SUCCESSOR-eligible, because a Done-when gap is convergence-class.
- **The fix is proportionate.** Record admission needs its own close test that admits the close's exact inbound relinks. Trunk now carries one shared, byte-exact reading of a relink (`spec_move.exact_relink`, the oracle WI-925 introduced for the staged Done-when reader). The rest stays as it is: the request and record compare, the parent-tree validation, the one-parent, one-source-branch, paired-moves and composed-subject shape, and the peel itself (the reviewer does not ask to widen it). P5's residual paragraph and its matching risk then go, and the regression the critique names pins the change: a real `close_adjudication` with an inbound link from outside `docs/work/` passes the lane rider and the squash hook, while a hand-written record beside the same relink is still refused.

**Routing note.** At the plan cap only an accepted DISMISS lets the pass record be written (the `coordinator-cycle` recipes). This ruling is therefore the owner's to route, as those recipes direct for anything else.

RULING: F1 FIX P5 accepts a close only through the peel's attestor, which refuses any path outside docs/work/, so a genuine close_adjudication whose spec_move relink reaches a review, plan or log file is refused at the slot and the hook with no supported recovery (its stated "a person re-closes it" is a hand close P5 and P7 forbid), a gap in the Done-when's "passes the close's own commit"; give record admission a close test that admits the close's exact inbound relinks through the shared spec_move.exact_relink reading, keep record/request, parent-tree and close-shape validation and the peel unchanged, and add the real-close regression the critique names
