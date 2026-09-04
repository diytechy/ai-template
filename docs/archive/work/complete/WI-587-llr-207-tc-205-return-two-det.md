+++
id = "WI-587"
title = "LLR-207/TC-205 return: two Detail clauses contradict kitlib/verdict.py, two stated guards have no detector, one TC Method misstates its own fixture, and the CMP-006 note this row falsifies"
workstream = "process"
specref = ""
buildtier = "strong"
priority = 2
safety_class = "spine"
bar = "DevStg-Tests"
+++

## Deliverable

ALL SEVEN findings driven, over three cells and two new regressions.
`kitlib/verdict.py` is BYTE-IDENTICAL to its pre-lane state (`git diff` over the
module against the integration base is empty) — the return was about text that
contradicts the module and guards no fixture drove, and the row asked for no
behaviour change.

THE TWO `LLR-207.detail` CLAUSES now say what the module does, re-driven against
it rather than inherited. `governing_identity` reads "the branch tip or an
explicit revision" and states that the branch argument is a branch NAME, for the
reason `format_branch_trailer` gives verbatim (`verdict.py:738-740`) — the peel
verifies a refresh commit against the branch it names, and no refresh subject
names `HEAD`. `governing_rev`'s "until it can peel" is gone: the peel re-seats
`rev` and `continue`s (`:465-468`), the walk ends at the first commit whose
identity differs from its parent's (`:473`) or at the absent-parent /
`_MAX_GOVERNING_WALK` bounds, and the clause now says a branch with no refresh
under it still walks — which is the OI-76 fix a literal reading of the old
sentence would have undone.

THE TWO STATED GUARDS GREW DETECTORS, and both were MUTATION-DRIVEN, because a
regression that never fails is not one. Each mutation was re-driven AT THE
CLOSING TIP on a detached `git worktree`, so the run proving the regression could
leave no residue in the tree being closed:
- `test_two_logs_at_one_key_declaring_two_phases_serve_no_round` — relaxing the
  `len(ph) == 1` ambiguity rule (`:608`) to last-wins fails exactly this test and
  nothing else (`1 failed, 52 passed`).
- `test_an_attestation_riding_a_commit_that_changed_the_work_is_not_read` —
  deleting the `governing_identity(...) != tree` carrier guard (`:802-803`) fails
  exactly this test and nothing else (`1 failed, 52 passed`).
Both previously left `134 passed` across the three modules the return measured.
Each fixture asserts its own premises (both logs really committed, the round file
still present; the forged carrier really moved the governing identity) so the
empty answer is the RULE and not an empty scan.

THE TWO `TC-205` CELLS. `evidence` now reaches `work_tip` /
`refresh_attestation`'s refusal arms by citing the five
`tests/test_integrate_station.py` tests that hold them — all five verified to
exist — with a `Method` sentence saying which arms those are and why the station
suite is where they live. `method`'s identity sentence was made true BY THE
FIXTURE rather than by weakening the sentence: the changed `docs/work/` spec blob
now really folds DIFFERENT, the pre-existing dropped-entry assertion left beside
it as the weaker claim.

`CMP-006`'s note re-points to name BOTH modules not owned there — `station.py`
(LLR-182, IF-093) and `verdict.py` (LLR-207, IF-175) — the sentence THIS row
falsified by giving `verdict.py` a CMP-008 tag. Re-derived at close by the
complementary route (enumerating rows by `Module` path, not by component, checked
against the directory listing): all eleven `kitlib/` modules are claimed by an
LLR row, and exactly two sit at CMP-008.

AN EIGHTH FINDING, IN THE SAME CELL, ALSO FIXED. The note's parenthetical
enumerating kitlib's CMP-006 members omitted `evidence.py` (LLR-192) and
`spine.py` (LLR-197), so a list phrased as complete was not; both are now in it.
Its causation is NOT finding 7's and the two are kept distinct: there,
`verdict.py` taking a CMP-008 tag is what made the sentence false, so the row
that gives the tag owes the fix; here nothing on this lane touches either
module's membership. It is fixed anyway because this row already amends this
exact cell, the falsehood sits two sentences from the sentence finding 7
rewrites with the same subject, and these cells have not changed byte since
`3c7764c5` — three rereads on identical text is what leaving it invites. The
cell's two enumerations now partition all eleven `kitlib/` modules with nothing
left over: nine at CMP-006, two at CMP-008. `check_trajectory` is `clean`.

NOT ON THIS LANE — the approval. `LLR-207` and `TC-205` stay `Drafted`; no
`docs/archive/last_approved/` write, no `intake.py snapshot`. The adjudication
this merge mints is what approves them.


## Context

Drafted by WI-586 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

VERDICT THIS CONTINUES:
`docs/reviews/wi-586-adjudicate-llr-207-llr-208/009-ADJUDICATE-082b9e1.md`,
governing line `OUTCOME: RETURN rows=4` over `LLR-207`, `LLR-208`, `TC-205`,
`TC-206`. Every finding below was re-driven on the tree at that commit, not
inherited from the three prior returns: the registry rows have not changed byte
since `3c7764c5` (`git diff 3c7764c5 HEAD -- docs/requirements/low-level-requirements.toml
docs/test/test-cases.toml` is empty), so each reread has been ruling on the same
text and only a lane that EDITS these cells can end that. `LLR-208` and `TC-206`
were returned by the same act on a ground of their own and are the SECOND
draft's scope. `LLR-207` and `TC-205` return TOGETHER: the requirement and test
halves of the coverage findings are one gap seen from two sides.

IN SCOPE — three cells, two regressions, one re-point.

1. `LLR-207.detail`, the `governing_identity` clause. It reads "composes
   governing_rev and tree_identity for HEAD or an explicit revision". The
   default is the BRANCH TIP, not `HEAD`, and the distinction is the row's
   whole subject: the merge slot asks about a branch it does not have checked
   out, so on the trunk `HEAD` is a different tree entirely. `verdict.py:50`
   records "the loop measured at `HEAD` instead" as the original two-reader
   disagreement, `governing_rev`'s and `governing_identity`'s docstrings both
   say "`rev` defaults to the branch tip", and `format_branch_trailer`
   (`:738-740`) forbids the word by name — "`branch` must therefore be the
   lane's BRANCH NAME and not `HEAD`: the peel verifies a refresh commit
   against the branch it names, and `HEAD` matches no refresh subject."
   Restate the clause as the branch tip or an explicit revision, and say that
   the branch argument is a branch NAME, for the reason the module gives.
2. `LLR-207.detail`, the `governing_rev` clause. It reads "walks across commits
   whose non-record identity equals their first parent's UNTIL IT CAN PEEL a
   verified refresh". That is not the termination condition. A peel does not
   end the walk — it re-seats `rev` and `continue`s (`verdict.py:465-468`) —
   and the walk ends at the first commit whose identity differs from its
   parent's (`:473`), or at the absent-parent / `_MAX_GOVERNING_WALK` bounds
   (`:470`, `:398`). A branch with no refresh under it therefore still walks,
   which is the whole OI-76 fix; a builder implementing the sentence literally
   returns the tip and reintroduces it. `IF-175` already states the mechanism
   correctly — "to reach a refresh it would otherwise hide" — so borrow that
   framing: the refresh is the walk's PURPOSE, not its terminus.
3. The multi-log ambiguity rule has no detector. `LLR-207.detail` states "a
   joined key whose logs declare more than one review phase yields no round"
   and `verdict.py:608` implements it (`len(ph) == 1`). No fixture writes TWO
   session logs at one `(train, ordinal)`. Mutation driven and reverted:
   relaxing that guard to last-wins (`sorted(ph)[-1] ... if ph`) left
   `134 passed` across `tests/test_verdict_record.py`,
   `tests/test_integrate_admission.py` and `tests/test_integrate_station.py` —
   the same 134 the unmutated baseline gives over those three modules, which is
   what the number covers and NOT the full suite. Write the regression: two
   `docs/iteration/<train>-<ordinal>-*.log` files at one key declaring
   `REVIEW-A` and `REVIEW-B`, asserted to yield NO round, beside the single-log
   arm that does — the fail-closed direction the cell states.
4. `branch_trailers`' carrier verification has no detector. `LLR-207.detail`
   states it "verifies each carrier against its governing identity" — the
   anti-forgery half of the row's own claim that the trailer "cannot create an
   approval". Mutation driven and reverted: deleting `verdict.py:802-803` (the
   `governing_identity(root, branch, sha) != tree` guard and its "the words rode
   onto a tree they do not describe" comment) left `134 passed` over those same
   three modules. Every fixture commits its trailer on a carrier whose identity
   already matches, and `branch_trailers`/`format_trailer`/`Review-Verdict`
   appear in no test module but `test_verdict_record.py`, so the arm is
   unexercised repo-wide. Write it: a trailer naming a valid governing identity,
   carried by a commit that CHANGED the work, asserted absent from
   `branch_trailers`' answer.
5. `TC-205.evidence` does not reach `work_tip` or `refresh_attestation`'s
   refusal arms. Both are named in `LLR-207.code_symbol`, described in its
   `detail`, and argued in its `rationale` ("Separate read-only and reset peels
   protect both contracts") — but `refresh_attestation` occurs in
   `tests/test_verdict_record.py` only at `:608`, as a positive assertion,
   while all 26 occurrences of the reset-peel contract and the attestation
   refusals (forged trailer, amend, cherry-pick, wrong subject) are in
   `tests/test_integrate_station.py`, which `TC-132` cites for `LLR-140` and
   `TC-205` does not cite at all. Either cite that module and say in the
   `Method` which arms it holds, or drive the two peels' divergence directly in
   `test_verdict_record.py`. Citing is the smaller change and is honest, since
   the arms genuinely exist. Citing a `SLOW_MODULES` member beside this row's
   `Tier = Smoke` is not a new contradiction: `test_integrate_admission` is
   already both, and `docs/registry-machinery-reference.md` §12.2 records
   `TC.Tier` and the pytest marker as deliberately unreconciled.
6. `TC-205.method`'s one factual misstatement of its own driving. It says "a
   changed work blob and a changed `docs/work/` spec each fold DIFFERENT", but
   `_listing` numbers blobs `{:040x}` (`tests/test_verdict_record.py:60-64`), so
   at `:81-90` the spec entry's sha ends `0002` and its path holds no `00001`:
   the `b"00001"` -> `b"00009"` substitution moves only `src/widget.py`, and the
   second assertion compares against `_listing("src/widget.py")`, which DROPS
   the spec entry instead of changing it. Coverage is equivalent in effect
   because `fold_listing` folds the whole `<mode> <type> <sha>\t<path>` line
   (`verdict.py:256`), so either fix the sentence to describe the dropped-entry
   assertion or change the fixture to match the sentence. Do not leave a
   `Method` claiming an assertion the test does not make.
7. `CMP-006`'s note, which THIS row falsifies and which therefore re-points with
   it rather than being deferred. The note reads "kitlib/station.py (LLR-182) is
   the one package module NOT owned here: it stays CMP-008". That was true while
   `LLR-182` was the only kitlib module at CMP-008; `LLR-207` places
   `kitlib/verdict.py` at CMP-008 too (both confirmed by reading the parsed
   registry), so "the one package module" is now false and the shared-kernel
   boundary the note draws no longer describes the tree. Re-point the sentence
   to name both modules. Prior rounds filed this as stale-before-this-act; that
   reading is wrong on the causation — the note was true until `verdict.py` took
   a CMP-008 tag, and it is this row's cell that gives it one.

OUT OF SCOPE — the design. The identity fold, the two-shape peel, the
logged-session join, the declared phase span and the cross-check-not-accept
reading of the trailer are correct as built. Findings 1 and 2 are wording that
contradicts the module, not a mechanism to reopen; 3 and 4 add detectors for
guards that already exist and must not change behaviour; 5-7 correct cells. No
change to `kitlib/verdict.py`'s behaviour is asked for by this row.

NOT ON THIS LANE — the approval. This lane corrects the text, writes the two
regressions and STOPS: `LLR-207` and `TC-205` stay `Drafted`, nothing under
`docs/archive/last_approved/` is written, and `intake.py snapshot` is not run in
any form — `lane_approval_refusal` refuses any lane merge whose delta touches
`SNAPSHOT_DIR`. The first approval of both rows is the act of the adjudication
this row's own merge mints, which sees them because this lane AMENDS both cells
(`acceptance_record.staged_drafted_rows` reports the Drafted rows a delta added
or amended, and nothing else).
