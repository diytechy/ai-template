## 2026-11-06 — WI-995: the review test set is derived from the row's SRs through the test-file tags

Deferred open items: none.

`integrate.py attest` and `review_brief.py review` lose `--tests`. A new
`review_set.py` derives a lane's set, and `attest`, the loop's draw and the
render all call it; the walk has its one home in `kitlib/spine.py`.

Stamps moved with it:

- `agent_loop.py` 2526 -> 2531: the draw derives the set and compares the
  record against it, and both import sites name `review_set`.
- `integrate.py` 1802 -> 1801: the preflight's named tuple drops the padded
  refusal arms, net of the derive call and the printed set.
- `docs/stack.ini` `max-tests` 3410 -> 3550: the walk module's in-process pins
  and the growth the base already held (3398 collected, not the plan's 3392).

- Round 1's MAJOR: the draw now reaches the step that appends paths and a
  basetemp argument to `[product] test`, so a runner refusing them reds every
  code-touching row. The shipped template and the RESYNC entry state it; the
  placeholder stays the owner's call (wi-995 D-003, high risk).
- Sitting 005 returned LLR-207, TC-333, LLR-367 and TC-414; sitting 006 blessed
  and approved the whole set. Acts under it. Two counted rounds, both gate
  reviewers approve.
