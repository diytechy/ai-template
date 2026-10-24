# WI-856 checkpoint sitting at 793f65c

## amendment

Three approved rows moved against their copies, recorded at commit afb57ae33. All three carry one change, the queue-with-edge close on a waiter filed with no `needs` line. The lane's code change (`79be877e3` onward) does exactly that:
- `edged_text` now finds and parses the frontmatter once;
- with no `needs` key, it inserts the line directly after the opening fence, in that fence line's own line ending;
- an existing line is extended as before;
- a missing fence, a frontmatter that does not parse, and a `needs` list spread over several lines are each refused.

The arms map's three gaps are closed at this tip:
- the multi-line `needs` refusal has its own case (`[multi-line-needs-list]`);
- the placement is pinned (`lines.index(inserted) == opening + 1`);
- TC-208's EDGE WRITE now states idempotence, hard and soft.

Checks I ran:
- The edge and needs cases in `tests/test_consolidate.py` pass (17 run), and so do those in `tests/test_consolidate_close.py` (4 run).
- `trace.py --strict` exits 0, with no advisory on these rows.
- A token check finds no code name added to any amended cell. The only new marks are the `needs` key and the `~` prefix, which belong to the specification format a row is written in, not to the implementation.

All three rows changed MEANING, and I would bless all three. The rung is released, so the later act turn re-attests each.

- [MEANING+BLESS] LLR-210 Detail -> before: the consolidation judgement's selection, guards and close transforms, with the edge transform's behaviour on a waiter carrying no `needs` line left unstated. The approved TC-254 read it as a refusal ("lacks a readable needs line ... refuses") -> after: the same, plus:
  - a waiter with no `needs` line gains one holding just the blocker, at the top of the frontmatter, ahead of any table, with every other byte kept;
  - a row with a `needs` line is extended as before, idempotently, so a row already waiting on the blocker, hard or soft, comes back unchanged;
  - a missing fence, an unparseable frontmatter, or a `needs` list not on one line is refused.

  -> not the same: a close the old reading refused now succeeds and writes a line. Ready to bless:
  - each new sentence is an observable input, output or refusal, and matches the code;
  - the placement rule gives its reason in the row's own terms (top-level, ahead of any table);
  - the refusals are fail-closed, since what the transform cannot read it never edits;
  - it adds no `shall` and no symbol, and its approved text is kept verbatim.

  Note, not a finding: the soft arm ("a row already waiting on the blocker ... soft, comes back unchanged") states the transform's existing behaviour, as its prior docstring did. A consolidation verdict asking for a hard edge onto a waiter that already waits softly therefore leaves the dependency soft. That is a pre-existing design choice this amendment documents rather than introduces. A later row could rule whether such a verdict should harden the edge.
- [MEANING+BLESS] TC-208 Method -> before: the selection, population and guard arms of the consolidation judgement, in process -> after: the same, plus THE EDGE WRITE: insertion of a missing top-level `needs` line at the top of the frontmatter, ahead of any table, which parses, with the rest of the specification byte-identical; an existing line extended as before and idempotent, hard and soft; and the three refusals -> not the same: new arms enter the verified set. Ready to bless. Each clause matches an LLR-210 sentence one for one, and every arm now has a passing case. That includes the exact placement, the CRLF parameter and the multi-line refusal, the gap the map left open.
- [MEANING+BLESS] TC-254 Method -> before: on real lanes, a verdict whose later edge target "lacks a readable needs line" refuses before any write -> after: a waiter filed with no `needs` line gains one holding just the blocker, the rest of its specification unchanged; and the before-any-write refusal is for an edge target whose frontmatter or `needs` line "cannot be read" -> not the same: the no-`needs` case moves from refusal to success at the close. Ready to bless. The added clause is driven end to end by `test_queue_with_edge_gives_a_waiter_with_no_needs_line_one`: the close succeeds, the row stays queued with WI-401 as its predecessor, and every other byte is unchanged. The narrowed refusal keeps LLR-312's before-any-write frame, held by `test_a_refused_edge_leaves_the_lane_tree_byte_identical`.

VERDICT: MEANING rows=3

SITTING: JUDGED kinds=amendment
