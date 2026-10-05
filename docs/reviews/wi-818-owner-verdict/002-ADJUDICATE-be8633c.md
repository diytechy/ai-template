# 002: ADJUDICATE (independent, Claude Opus), the WI-818 amendments at `be8633c0`

Adjudicator: an independent Claude Opus session, the author of
`dispute-1-ruling.md` and `001-ADJUDICATE-be8633c.md`. I wrote none of WI-818's
code or rows. Brief: `review-tmp/wave15/brief-wi818-amend-r2.md`, read in full.
The amended rows are SR-225, LLR-283, LLR-284, TC-293, TC-294 and TC-313. The
anchor is `docs/archive/last_approved`: system requirements copied at
`8868537c`, low-level requirements and test cases at `e81c43d1`.

## Basis (probed, not trusted)

- **SR-225's requirement is the ruling's text.** I parsed the registry at
  `HEAD` with tomllib. SR-225 `requirement` equals the fenced block of
  `dispute-1-ruling.md`, byte for byte, and its `status` reads `Approved`.
- **The mutants**, on a fresh `git archive` of `be8633c0` (base 228 passed;
  details in 001):
  - **L6** (the overruled list not ordered) and **L7** (`citing_rows` skipping
    the archive): killed by the two new `test_decisions_to_review.py` nodes.
    TC-293 cites that file whole.
  - **L11** (the session note losing "set no owner key"): killed by the new
    assertion in `test_the_session_note_names_the_path_only_under_a_recording_dial`.
  - **L1 to L5, L9, L10, L12 to L16**: killed.
  - **L8** (`citing_rows` counting a `-000` spec) survives. No amended cell
    claims that behaviour.
  - **R1 to R6 and R8** (the dispute change): killed, by the alphabet test, the
    no-record test, `test_decision_record.py`'s path test and TC-294's new
    `test_a_branch_name_no_record_can_carry_is_refused`.
  - **R7** (the rung's `if owed` arm) survives. It is equivalent inside the
    merge ladder (see 001).
  - **P1b and P2** (the path listing read quoted, or decoded lossily): kill
    TC-313's two new nodes. `kitlib/git.py` has not changed since that probe.

## Verdicts

- [MEANING] SR-225 requirement and acceptance ->
  - before: where the dial asks for a record, a delegated run is held to it: a
    close without it is refused, malformed entries are reported, and entries
    not marked reviewed are listed;
  - after: whatever the dial, malformed entries are reported, unseen and
    overruled entries are listed with their open work, and an overrule is
    refused unless its change files or amends open work citing the entry, with
    a migration of the retired key and a fail-closed parse; where the dial asks
    for a record, a close without it is refused;
  - not the same: a correct implementation of the old text has no verdict key,
    no overrule coupling and no migration.

  **Blessed.** Every acceptance clause is true of the code and held by a cited
  node. The requirement is the one-`shall` cell the ruling gave, with the
  overrule refusal outside the dial's scope.
- [MEANING] LLR-283 detail and title ->
  - before: `record_path` maps `/`; a `reviewed` key with a case-folded
    vocabulary; a queue of entries not marked reviewed;
  - after: `record_path` maps `/` only and raises for `#` or a git-refused
    character; the exact `owner` vocabulary; the retired key as a finding;
    unseen and overruled lists; citations; the transition reader;
    `missing_record_refusal`; and the owner surface's overruled heading with
    citing work;
  - not the same: new functions and new findings.

  **Blessed.** Each sentence is true of `kitlib/decisions.py`, `pending.py` and
  `gen_open_items.py` at `be8633c0`, and each is held (R1 to R3, R5, R6, R8,
  L1 to L7 and L9 to L16 are killed). `missing_record_refusal` is in its
  `code_symbol` and carries the back-link.
- [MEANING] LLR-284 detail ->
  - before: an absent record path is refused when owed;
  - after: the same, plus a branch name `record_path` refuses is an absent
    record, refused through `missing_record_refusal` naming the branch and the
    reason;
  - not the same: a correct implementation of the old text crashes on, or
    folds, such a name.

  **Blessed.** True of `integrate._decision_record_refusal`, and held by
  TC-294's new node (R1, R4 and R5 are killed).
- [MEANING] TC-293 expected and method ->
  - before: the reviewed-value defects and the queue of entries not marked
    reviewed;
  - after: the owner-verdict defects, the unseen and overruled lists, and the
    note naming the owner vocabulary with the key left unset;
  - not the same: different cases.

  **Blessed.** Clause (i)'s "owner unset", which no test held at `b31498e2`, is
  now asserted. TC-293 cites its two files whole, so the new nodes are cited.
- [MEANING] TC-294 method ->
  - before: cases (a) to (e);
  - after: the same plus (f), a `#` branch carrying another name's record is
    refused, naming the branch and `#`, not the file;
  - not the same: a case was added.

  **Blessed.** (f) is exactly what
  `test_a_branch_name_no_record_can_carry_is_refused` asserts, and the node is
  in its `evidence`.
- [MEANING] TC-313 method ->
  - before: the ruling transitions through to the merge-ladder case;
  - after: the same, plus a citing row git would quote is judged at both
    admission points, and a non-UTF-8 citing row is refused by name;
  - not the same: a case was added.

  **Blessed.** True and held: P1b kills the quote node and P2 kills the
  non-UTF-8 node.

VERDICT: MEANING rows=6

## Aftermath

LLR, SR and TC sit on rungs the declared gate authority has RELEASED. All six
rows are MEANING, and all six are rows I would bless, so the re-attestation is
mine (`--reattests`). No `--verdict` is owed, since that applies only to a held
rung.

The act is NOT taken in this sitting. 001 returns TC-319 and TC-320 for their
`method` cells, and the coordinator's direction is no act while anything is
returned: the act is the lane's last commit. The fix touches none of these six
rows. If it lands without moving any of their cells, this verdict stands, and
the one act is:

`python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-818;docs/test/test-cases.toml=WI-818" --reattests SR-225,LLR-283,LLR-284,TC-293,TC-294,TC-313`
