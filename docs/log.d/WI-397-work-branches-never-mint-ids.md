## 2026-08-01 — WI-397: a work branch never mints a work-item id

**Summary.** Owner ruling **R1** (2026-08-01,
[backlog-plan-2026-08-01.md](../backlog-plan-2026-08-01.md) §R1) executed:
minting a work-item id is a **serial trunk-side act only**. A new work item
takes `max(existing id) + 1`, a lane can only see its own tree, and the
arithmetic does the rest — on 2026-08-01 two lanes independently minted
`WI-392`, and three rows lived only on the unmerged `wi-391` branch while
trunk's max sat *below* them, so a trunk mint in that window would have
re-collided. The two coordinating answers (a reservation table in the
dispatcher, lane-namespaced ids renumbered at merge) manage that state; this
one **deletes** it. An id a branch cannot create cannot collide, and the
id-reservation question leaves WI-381's scope before that row is built.

**Deliverable.** `integrate._minted_id_refusal`: at the merge slot, a finished
branch whose `docs/work/` delta — `merge-base(trunk, branch)` to tip — **ADDS**
a spec file carrying an id outside its claimed set is refused, naming the
foreign id(s), the path(s), the claimed set, and the rule. It is
`_claim_refusal`'s shape at the other end of the lane's life, and it sits in
`_merge_refusal` beside the outcome read it belongs with, cheapest-first.

- **Trunk-side minting is untouched by construction, not by exemption.**
  Whatever trunk did is in the merge **base**, so it never appears in the
  branch's delta: the claim's bookkeeping commit, WI-388's coming adjudication
  mint and a human trunk commit stay exactly as free as they are today. The
  claimed set is trunk's own `active/<branch>/` read (`_claimed_wi_ids`) — the
  reader that was already there.
- **Adds only, spec filenames only.** That is what leaves every allowed move
  alone without a second policy engine to describe them: a terminal-outcome
  move and a handback's return both re-ADD a file whose id the branch already
  holds claimed; an edit to a claimed row is an `M`; a handback's bar-inert
  `docs/work/handback/<branch>.patch` carries no spec filename at all.
- **`--no-renames` is load-bearing, and it is measured.** With rename detection
  on, git pairs the minted spec with the DELETE side of the branch's own close
  (spec files are short and near-identical) and the mint arrives as one `R`
  record with **no add left to see** — the only `A` remaining is the legitimate
  close. `tests/test_integrate.py` drives that exact topology and asserts the
  trap before asserting the rung sees through it, so the flag has a reason on
  file rather than a habit.

**How it is tested.** Five tests in
[`tests/test_integrate.py`](../../tests/test_integrate.py), all constructing
their own git topologies. One builder (`_mint_repo`) makes the refused and the
admitted case the *same* branch minus one file, so a rung that refused
everything could not pass both. The admission is driven twice — the helper
returns `None`, and the whole slot gets past it to the next refusal — because a
rung tested only through its own function proves nothing about where it was
wired. The three admitted shapes are the two terminal folders and a handback's
`queued/` return with its `.patch`.

**Deviations from spec, and what they cost.**

- **The Decisions entry is written on the TRUNK, not by this branch.**
  `## Decisions log` is one of `trunk_step.RESERVED_HEADINGS`: a fragment may
  not claim it, and fragments append to the log's end rather than splicing into
  its structural sections. Every prior ruling in that section arrived as a
  direct trunk commit (`72c5b756` is the four 2026-07-31 rulings), so this
  follows the convention that exists rather than inventing one. The row's
  DONE-WHEN is met by that commit, which the post-merge bar covers.
- **Three deduplications inside the scope guard.** The guard says *one rung, no
  general `docs/work/` diff-policy engine* — and none of these is engine. The
  ratchets asked for each one by name: `check_dupes` convicted the
  `--name-status` walk I had copied out of `_abandoned_claim` (`_name_status`
  deletes the copy rather than censusing it), the complexity ratchet put
  `integrate_one` at C901 11 (`_merge_refusal` is the extraction it prefers over
  a bigger number — the `_drop_abandoned` precedent from WI-387), and `_spec_id`
  is the filename→id read the rung and the claimed set have to agree on.
- **`integrate.py` re-stamped 1733 → 1890**, reason at the entry in
  [`tests/test_module_size_ratchet.py`](../../tests/test_module_size_ratchet.py).
  The rung is ~25 lines of code under ~55 of docstring; that ratio is the
  entry's argument, since the *why* is what a successor would otherwise have to
  rediscover from the collision. Re-stamp DOWN with WI-390.
- **No byte-budgeted file was touched** (`AGENTS.template.md`, `PROCESS.md`,
  `PROCESS_OPTIONS.md` unchanged). No spine row changed: the standing ruling is
  that spine work waits and batches, and this rung adds no module.

**Findings recorded as prose (no id minted — this row's own rule).**

1. **Claiming a row that a plan doc links to reds trunk's `doc-navigability`
   until the branch merges.** The claim moves the spec `queued/ →
   active/<branch>/`, and
   [backlog-plan-2026-08-01.md](../backlog-plan-2026-08-01.md) links every row
   in its execution table by path — so `check_docs` convicted the WI-397 link
   the moment the claim landed, on trunk, with no branch to blame. This branch
   repairs it by hand (the link now names `complete/`, where the spec ends up),
   but the same break will happen on each of the remaining nine rows in that
   table. It is the link-aware move ritual **WI-393** exists to restore, now
   with a driven instance: the ritual is owed at *claim* time, not only at
   archival.
2. **The mint rung reads spec FILES, so a lane can still record an id-shaped
   claim in prose.** Stated as the bound, not as a gap to close: nothing here
   reads a file that is not a spec, and the remedy for the accidental case is
   the ruling's own — findings are recorded as prose and take an id at or after
   merge. Closing the deliberate case would need a check of exactly the shape
   the governing principle argues against.
