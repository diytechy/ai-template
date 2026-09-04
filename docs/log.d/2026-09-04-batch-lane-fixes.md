## 2026-09-04 — Four batch-lane defects, fixed at the root

Measured 2026-09-03 on the lane `wi-589-two-verified-defects-around-th` — a
four-row spine batch (`WI-589;WI-584;WI-587;WI-588`) dispatched as ONE branch
with `--wi 'A;B;C;D'`, plus the WI-586 adjudication merge that preceded it. All
four are specific to a MULTI-ROW lane; a one-row lane hits none of them, and
each fix is written so a one-row lane cannot observe it.

### 1. The walk skipped a row that was built but never closed

`agent_loop.current_assignment_wi` asked one half of the question — is a `WI:`
trailer committed for this row — while `integrate.finished_branches` asked the
other — has every spec left `active/<branch>/`. Session 001 committed WI-589's
build WITH its trailer (`05f6bb26`, `b8e445ae`) and ran out before the C6 close
ritual, so the walk stepped past the row for the remaining ten sessions and the
integrator never counted the branch finished. The lane stranded after its review
round and a supervising session closed the row by hand (`836ccd94`).

The walk now counts a row BUILT only when both halves are true. The tree read
went outward to `integrate.claimed_ids_on_branch`, beside the
`finished_branches` that asks the same tree the same question — two readers of
"has this row left `active/`?" is the defect, so there is now one.
Tests: `test_a_built_but_unclosed_row_is_still_the_walks_next_row`,
`test_a_row_with_both_halves_done_lets_the_walk_move_on`,
`test_a_one_row_lane_answers_its_row_either_way`.

### 2. The DONE handler died on a spec the lane had already moved

`dispatch._close_done_adjudication` calls `handback.close_adjudication` for
every DONE worker whose branch is not finished, and that function read the
claimed set off the TRUNK — which still lists every row of a batch. Reading
WI-584's spec, already in `complete/` by its own close (`9c8b3ce2`), it returned
"cannot read the claimed spec WI-584-… on <branch>", which the dispatcher treats
as `EXIT_PREFLIGHT` and the whole loop exited 2 over a lane that owed nothing.

`handback.open_claimed_specs` is now the one home for the batch filter — the
claimed rows still in `active/<branch>/` on the LANE — and both closes use it,
so "is this an adjudication lane" is decided from the specs that are actually
still claimed. An empty filtered set is the documented NO-OP, never a refusal.
The per-row close moved out to `_archive_one_adjudication_row` so the loop stays
a loop (`close_adjudication` drops off the cognitive-complexity baseline
entirely; its row is deleted, per the ratchet's re-stamp-downward rule).
Tests: `test_the_mechanical_close_no_ops_when_a_batch_row_already_closed`,
`test_an_adjudication_batch_still_closes_the_row_that_is_open`.

### 3. The preflight refused a resumed batch, and the fallout committed residue

On resume the worker's preflight refused three of the four rows: "assigned
WI-584 is already done — a terminal status (done/cancelled); a stale assignment,
so the dispatcher must re-derive the frontier." They were terminal BECAUSE THE
LANE ITSELF closed them, which is the normal state of a partly-finished batch.
`agent_common.stale_terminal_assignment` now asks the question the refusal is
actually about: terminal for some reason OTHER than this branch's own committed
`WI:` trailer over `merge-base(trunk, HEAD)..HEAD`. `trunk_name` and
`default_base` moved from `agent_loop` to `agent_common` for it (re-exported
there) rather than growing a second merge-base rule. A single-checkout attended
run merge-bases to HEAD, reads an empty range, and keeps the refusal exactly —
which is what the existing done/cancelled preflight tests assert.

**The residue rule, decided here.** After the refusal the dispatcher's
partial-close arm committed the lane's uncommitted work as-is (`b0be72c7`,
"the work so far, committed as-is (partial close)") and moved rows to the
TERMINAL `partial/`. Two changes, and the second is a ruling:

- `close_partial` skips rows already terminal on the branch, so a batch that
  hit its session ceiling mid-way closes only the rows still open and leaves
  the rest with the outcome the lane itself declared. The report-immutability
  rung was hoisted ABOVE the filter (`_existing_report_refusal`, asked over the
  whole claimed set before anything is written) so a SECOND close of a row
  already in `partial/` still refuses rather than passing as a no-op.
- **`EXIT_PREFLIGHT` leaves `dispatch._WORKER_OUTCOMES`.** A preflight refusal
  is the worker saying it could not START — a config conflict, an unreadable
  assignment, a frontier the dispatcher derived wrongly — so it is evidence
  about the LAUNCH and never about the work. Recording a terminal outcome and
  committing a tree nobody read, on a failure the lane could not have caused, is
  the shape this whole contract exists to prevent. Such a lane is now parked
  exactly like a CRASHED one: the claim stays in `active/`, the next cycle
  resumes it, and a worker that keeps refusing is bounded by the stall guard.
  The alternative — keep handing back, but only after the preflight is proved
  the lane's own fault — needs a fault attribution nothing can compute here.

Tests: `test_a_row_this_branch_closed_is_not_a_stale_assignment`,
`test_a_single_checkout_worker_keeps_the_terminal_refusal`,
`test_a_partial_close_skips_a_row_the_lane_already_closed`,
`test_a_partial_close_with_every_row_already_terminal_is_a_no_op`,
`test_a_preflight_refusal_parks_the_lane_instead_of_committing_its_residue`.

### 4. The mechanical close staled the round it had just been given

On an adjudication lane owing a round (`[attestation] adjudication_review =
"when-minting"`), the loop draws the round and the DONE handler's mechanical
close then moves the spec `active/` -> `complete/`. `docs/work/` is IN the
non-record tree identity, deliberately, so that move staled the APPROVE that had
just judged the row: `integrate._verdict_gate` found no logged round naming its
tree and refused, and the supervisor hand-compiled a legacy rollup (WI-586;
`docs/reviews/WI-586-REVIEW-A.md` on trunk, and again for this lane at
`4d7a92b8`).

**Approach chosen: compose the identity with a mechanical-close peel**, not
re-sequence the close. The re-sequencing option — close before the round is
scheduled — moves a trunk-side machinery act (`close_adjudication` reads the
trunk's claimed set and drives the lane worktree) into the middle of a lane
session, makes the branch read as FINISHED while it still owes a round, and
leaves a CHANGES-REQUESTED verdict reworking a row already in `complete/`. The
peel is strictly smaller and rests on the argument the refresh peel already
made: the close commit is machine-authored end to end, its subject is composed
by the new `station.mechanical_close_subject` (one home, writer and verifier),
and the `## Deliverable` it inserts is a fixed literal — nothing a reviewer could
conclude differently about enters the tree, and the row's own `## Dispositions`,
which is what the verdict judged, passes through unchanged.

`kitlib.verdict.mechanical_close_attestation` verifies it against git, not off
the message: the subject must be exactly the composed one, the commit must have
exactly ONE parent, and every path it changed must be under `docs/work/` — which
is what stops a close whose inbound-link relink reached into product or
requirement files from being peeled. Each check fails toward MORE review.
`governing_rev` asks `_peel_target`, the one home for both disposable commits, so
the walk is unchanged in shape and the two peels compose.
Tests: `test_the_mechanical_close_does_not_stale_the_round_it_follows`,
`test_only_the_machinerys_own_close_subject_peels`,
`test_a_close_that_reached_outside_docs_work_does_not_peel`.

### Ratchets

`agent_loop.py` re-stamped DOWNWARD (2587 -> 2579); `agent_common.py`
1314 -> 1338 and `integrate.py` 1354 -> 1363 are reviewed bumps, both of them
paying for lines `agent_loop` shed — reasons at the entries.
`handback.close_adjudication` leaves the cognitive-complexity baseline (16 ->
below threshold) and `agent_common.preflight` re-stamps 34 -> 33, both downward.

Deferred open items: none — each defect is fixed at the reader that held the
wrong rule, with a regression test that fails on the pre-fix code, and no arm of
any of the four was left for a successor.
