## 2026-09-03 — WI-587: the verdict row says what the module does, and two stated guards grow detectors

Continuing `docs/reviews/wi-586-adjudicate-llr-207-llr-208/009-ADJUDICATE-082b9e1.md`,
`OUTCOME: RETURN rows=4`, over the `LLR-207` / `TC-205` half of that return. The
other half (`LLR-208` / `TC-206`) is WI-588's and is not touched here. Nothing in
`kitlib/verdict.py`'s behaviour changed: the return was about text that
contradicts the module and guards no fixture drove. The module is byte-identical
to its pre-lane state — the two mutations below were applied and reverted, and
`git diff` over it is empty at this tip.

DONE — the seven findings of the spec's `## Context`, in its order.

1. `LLR-207.detail`, `governing_identity`: "for HEAD or an explicit revision" is
   now "the branch tip or an explicit revision", and the clause states that the
   branch argument is a branch NAME. Re-driven against the module, not inherited:
   the docstring reads "`rev` defaults to the branch tip" (`verdict.py:480`) and
   `format_branch_trailer` gives the reason verbatim — "the peel verifies a
   refresh commit against the branch it names, and `HEAD` matches no refresh
   subject" (`:738-740`).
2. `LLR-207.detail`, `governing_rev`: "until it can peel" was never the
   termination condition. Restated as `IF-175` already frames it — the refresh is
   the walk's PURPOSE, not its terminus. The peel re-seats `rev` and `continue`s
   (`:465-468`); the walk ends at the first commit whose identity differs from
   its parent's (`:473`) or at the absent-parent / `_MAX_GOVERNING_WALK` bounds
   (`:470`, `:398`); a branch with no refresh under it still walks, which is the
   OI-76 fix a literal reading of the old sentence would have undone.
3. The multi-log ambiguity rule now has a detector —
   `test_two_logs_at_one_key_declaring_two_phases_serve_no_round`. Two
   `docs/iteration/wi-401-003-*.log` files at one `(train, ordinal)` declaring
   `REVIEW-A` and `REVIEW-B`, with the fixture asserting both are really
   committed AND that the round file they would otherwise phase is still present
   — so the empty answer is the ambiguity rule and not an empty scan — yield no
   round, beside the single-log arm that yields one.
4. `branch_trailers`' carrier verification now has a detector —
   `test_an_attestation_riding_a_commit_that_changed_the_work_is_not_read`. The
   identical attestation words on a commit that CHANGED the work, asserted in the
   fixture to have really moved the governing identity, are read at neither the
   tree they NAME nor the tree they rode, beside the record-only carrier of the
   same words that IS read.
5. `TC-205.evidence` now reaches `work_tip` / `refresh_attestation`'s refusal
   arms by citing the five `tests/test_integrate_station.py` tests that hold
   them, with a `Method` sentence saying which arms those are and why the station
   suite is where they live (a refresh can be produced there rather than
   hand-written). All five names verified to exist.
6. `TC-205.method`'s identity sentence was made true by the FIXTURE rather than
   by weakening the sentence: `test_the_identity_notices_work_and_notices_docs_work`
   now asserts a changed `docs/work/` spec blob folds DIFFERENT, which is what
   the `Method` always claimed. `_listing` numbers blobs `{:040x}`, so the
   substitution moves the spec entry alone. The pre-existing dropped-entry
   assertion stays beside it and is the weaker claim — a fold that merely counted
   entries would satisfy it.
7. `CMP-006`'s note re-points: `kitlib/station.py` (LLR-182) and
   `kitlib/verdict.py` (LLR-207) are BOTH the package modules not owned there,
   each policed by an interface row — IF-093 for the station, IF-175 for the
   verdict record. Confirmed off the parsed registries: `LLR-207` carries
   `component = "CMP-008"`, and IF-175's owner is `scripts/kitlib/verdict`.

THE TWO GUARDS WERE MUTATION-DRIVEN, because a regression that never fails is
not one. Each mutation was applied to `kitlib/verdict.py`, the module suite run,
and the module restored from a byte copy:

- relaxing `:608` to last-wins (`sorted(ph)[-1] ... if ph`) — the shape that made
  the guard undetected — fails exactly finding 3's test and nothing else:
  `assert [('REVIEW-B', 3, 'APPROVE')] == []`, the REVIEW-B log that never judged
  the round being read as the round's phase. `1 failed, 52 passed`.
- deleting `:802-803`, the `governing_identity(root, branch, sha) != tree` guard,
  fails exactly finding 4's test and nothing else: the forged carrier's
  `('APPROVE', 2)` appears at the tree it names. `1 failed, 52 passed`.

Both previously left `134 passed` across the three modules the return measured.
Unmutated, `tests/test_verdict_record.py` is `53 passed in 24.99s`.

BOTH MUTATIONS WERE RE-DRIVEN AT THE CLOSING TIP, on a detached `git worktree` of
`6ffa8056` rather than by editing the live module — so the run that proves the
regressions could not itself leave residue in the tree being closed, and so the
claim is the tip's and not an earlier commit's. The worktree baselined
`53 passed in 47.30s` (slower than the figure above only because the unfiltered
suite was running beside it), then each mutation reproduced its recorded failure
exactly: `1 failed, 52 passed` in both directions, on
`assert [('REVIEW-B', 3, 'APPROVE')] == []` and on
`assert [('APPROVE', ...'APPROVE', 2)] == [('APPROVE', 1)]` respectively. The
worktree was removed and `git status` is clean.

AN EIGHTH FINDING, IN THE SAME CELL — spotted while driving finding 7, and FIXED
rather than deferred. The note's parenthetical enumerating kitlib's CMP-006
members read "config.py/git.py/registry.py/__init__.py via LLR-181, ladder.py via
LLR-184, stage.py via LLR-185, secret_classes.py via LLR-205" — omitting
`evidence.py` (LLR-192) and `spine.py` (LLR-197), both Approved and both CMP-006,
so a list phrased as complete was not. Both names are now in it, in row order.

The causation is NOT finding 7's, and the record should not blur them: nothing
this row does makes the parenthetical false — it was false before this act and
would have stayed false after. It is fixed anyway, on three grounds. This row
already AMENDS this exact cell, so the fix costs one edit rather than a lane; the
falsehood is two sentences from the sentence finding 7 rewrites and has the same
subject (which kitlib modules sit at which component), so a reader of the amended
cell would hit it immediately; and the spec's own `## Context` records that these
cells "have not changed byte since `3c7764c5`", which is why three rereads ruled
on identical text — leaving a known-false clause in a cell being amended invites
the fourth. The narrower reading (defer anything this act did not cause) is what
the return faulted in the OTHER direction at finding 7, where a caused error was
filed as pre-existing; it does not oblige leaving an uncaused one standing in a
cell already open.

Re-derived at close by the complementary route — enumerating rows by their
`Module` path rather than by component, and checking the answer against the
directory listing — all eleven modules in `project-trajectory/scripts/kitlib/`
are claimed by an LLR row: nine at CMP-006 (LLR-181 over four modules, LLR-184,
LLR-185, LLR-192, LLR-197, LLR-205) and exactly two at CMP-008, `station.py`
(LLR-182 and LLR-189, two rows on one module) and `verdict.py` (LLR-207). The
cell's two enumerations now partition those eleven with nothing left over, which
is the check the old parenthetical failed. `check_trajectory` is `clean` on the
amended cell — the added names cost no byte-budget breach.

THE FULL UNFILTERED SUITE, which the close commit deferred and which a session
reaped mid-run left owing. Driven at the closing tip (`cf1d36a8`):
`2 failed, 3367 passed, 24 skipped in 632.76s`. NEITHER failure is a green to
claim, and the two are NOT the same kind of thing, so each was driven to a
verdict rather than waved through:

- `tests/test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans` —
  INHERITED, not this lane's. The orphan is `docs/handoff-2026-09-03.md`,
  committed by `f1cc2767` and absent from this branch's delta
  (`git diff 794de60..HEAD --name-only` names no handoff doc). Driven at the
  INTEGRATION BASE on a detached worktree, where it fails identically
  (`1 failed`, same orphan, 730 docs there against 733 here) — so the base is
  red on this node before this lane exists. It is an owner-authored doc outside
  this row's scope; this lane neither fixes nor adopts it.
- `tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current` —
  CAUSED by this lane and BENIGN, the known close-ritual trap. It PASSES at the
  integration base, so this branch moved it. Driven BOTH WAYS on a regenerated
  worktree of the tip: RED before `derive_stage.py`, GREEN after. What moved is
  only the fingerprint and its as-of sha — `stage = DevStg-LLReqs`,
  `stage-ord = 4`, `stage-of = 8` and `drafted = 13` are BYTE-IDENTICAL across
  the regeneration, so no rung and no drafted count changed; the fingerprint
  tracks the tip commit, and this lane committed.

`docs/stage` is therefore NOT regenerated into this branch. It is a derived
artifact the trunk lane regenerates after each merge (concurrency-restructure
§5.2), and committing it here would be stale again at the very next commit —
the fingerprint embeds the as-of sha, so this row's own trailer commit would
re-red it. Leaving it is the correct lane behaviour, not an unpaid debt.

Both verification worktrees were removed and `git worktree list` shows only the
lane; `git status` carries nothing but the loop's own iteration logs.

NOT ON THIS LANE — the approval. `LLR-207` and `TC-205` stay `Drafted`; no
`docs/archive/last_approved/` write, no `intake.py snapshot`.
