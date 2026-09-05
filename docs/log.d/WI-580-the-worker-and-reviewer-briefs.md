## 2026-09-04 — WI-580 the worker and reviewer briefs: batch assignment block, one-turn close bar, rows under review, scratch home

**Session.** Worker lane `wi-580-the-worker-and-reviewer-briefs`, base
`1af07567`. One reviewed diff of two shipped prompt templates plus the two
functions that fill them — the consolidation the row was minted for (three
absorbed rows, WI-559/560/562, each adding a line or a block to
`worker.template.md`, plus the batch finding of plan §0).

**What changed.**

1. **`{assignment_block}`, and an opening sentence that is true for a batch**
   (Done-when 2). `agent_loop.assignment_block` renders EVERY row the lane was
   claimed with — id, title, SpecRef — each tagged `this session's focus` /
   `built` / `not started`, and `worker_prompt` gained an `assigned` parameter
   the `session_body` call site fills from `worker["assigned"]`. The block is
   **empty for a one-row lane**, so the single-row render is what it was except
   for the opening sentence, which now names the branch and this session's
   focus row instead of asserting "ONE work item". The state vocabulary is the
   walk's own evidence (`train_evidence`), not a fourth opinion about doneness.
2. **`{wis}` in the reviewer brief** (Done-when 3). `reviewed_rows_block`
   renders the lane's claimed rows, id + title, so a round can map Done-when
   items to coverage instead of inferring scope from the diff. Filled by
   `str.replace` like the C7 slots, so an operator override without the slot
   renders unchanged; unlike those it renders even with no worker, because a
   literal `{wis}` in a brief that was actually sent is worse than an honest
   "not declared" line.
3. **The one-turn close bar** (Done-when 1, WI-559 item 1 as written). The
   close ritual now states that the close bar IS the commit bar — fast tier +
   wall budget + docs staleness, as `docs/stack.ini` declares them — that the
   full unfiltered suite is the lane REFRESH's job (in the merge slot, outside
   any session's turn, attested by its `Bar-Green:` trailer), and that ending a
   turn to await a suite is the measured stall generator that closed WI-540
   `partial`.
4. **Amended approved cells stale the approval brief too** (Done-when 4,
   WI-560 item 2). The regeneration clause now names an amendment of an
   already-approved cell alongside a mint, with the WI-538/LLR-206 measurement.
5. **The scratch home** (Done-when 5, WI-562 item 2). One rule bullet: scratch
   lives outside the worktree, never under `out/` (the unload refuses an
   undeclared file there by name), never as a stray untracked file.

**A note on "byte-identical".** Done-when 2's byte-identity clause is scoped to
the assignment mechanism — items 1, 4 and 5 add prose to the same template by
construction. What the test pins is the mechanism's own claim: for a one-row
lane `assignment_block` contributes nothing.

**Bar.** (recorded at close)
