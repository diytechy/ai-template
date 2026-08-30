## 2026-08-30 — WI-508 review round 010: the snapshot BLOCKER, confirmed in part and refuted in part with driven evidence

Deferred open items: none — the residue is a generator-vocabulary gap the
supervisor's decisions file carries to the owner, not a ruling.

Round 010 (`docs/reviews/wi508-architectural-remap/010-REVIEW-A-085de8d.md`,
gpt-5.6-terra, cross-family) returned one BLOCKER: the round-1 rework
(`4824c0ba`) rewrote `docs/archive/last_approved/docs/test/test-cases.toml`
by hand when it demoted `TC-199`/`TC-200` from `Approved` to `Drafted`, so the
regenerated brief renders both rows "Drafted, never approved" although
`580df781` had approved and snapshotted them — "a false attestation record".

**Confirmed:** the snapshot file was edited by hand in `4824c0ba`. PROCESS.md
§4 names `intake.py snapshot` as the snapshot's only writer, and the hand
edit was the wrong instrument even where its bytes were right.

**Refuted, with the instrument run:** the claim that the record is false.
Driven on this branch at `ed3e976b`:

- `intake.py --root . snapshot` — the kit's own wholesale writer — copies
  seven registries and leaves `git status --porcelain` EMPTY: the hand-edited
  snapshot is byte-identical to what the approval-act writer produces from
  the live registries. Nothing was laundered; the file holds exactly the text
  the kit would have written.
  <!-- fig: cmd="python project-trajectory/scripts/intake.py --root . snapshot && git status --porcelain" rev=ed3e976b -->
- The approval and its reversal are both trunk-reachable history on this
  branch, not a rewrite: `580df781` (four rows `Drafted -> Approved`, snapshot
  taken) and `4824c0ba` (two rows `Approved -> Drafted`, the reviewer's own
  round-1 finding executed, recorded in
  `2026-08-30-wi508-rework-review-a-changes-requested.md`). The demotion is an
  auditable state by construction — `git log -p -- docs/test/test-cases.toml`
  shows both moves.
- Restoring the `580df781` snapshot while live reads `Drafted` was tried and
  rejected: it violates the same §4 sentence the finding cites ("a snapshot
  file must always equal its live counterpart"), and the brief STILL renders
  "Drafted, never approved", because that label is derived from the live
  `Status`, not from the snapshot — `trace.py --approve modified` has no
  vocabulary for "approved, then demoted". That wording gap is the true
  residue, and it is a generator finding for the owner, outside WI-508's
  scope.

**Why demotion rather than re-approval was right:** the two TCs stood as
evidence for `SR-163`'s full file-to-requirement join, which their own LLRs
record as undischarged (round 003, findings 1–2). An `Approved` TC on that
obligation was a false green; the rows were minted `Drafted` on 2026-08-25
and never reached trunk as `Approved` — the lane's own flip was the error and
the lane corrected it before merging. `LLR-203`/`LLR-204` stay `Approved`;
`SR-163`'s verification reads honestly UNSCHEDULED in the archived Deliverable.

**Deviations from spec:** none — a review-round record.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** not re-run for a record-only commit; the trunk-lane bar on
this tree read PASS on every step but `derived-stage`, which the station
refresh regenerates before its own bar.
