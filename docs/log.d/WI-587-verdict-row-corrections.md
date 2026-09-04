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

SPOTTED, NOT FIXED — one finding in the same `CMP-006` cell, deferred on the
return's own causation test. The note's parenthetical enumerating kitlib's
CMP-006 members ("config.py/git.py/registry.py/__init__.py via LLR-181, ladder.py
via LLR-184, stage.py via LLR-185, secret_classes.py via LLR-205") omits
`evidence.py` (LLR-192) and `spine.py` (LLR-197), both Approved and both CMP-006,
so the list reads as complete and is not. Unlike finding 7, nothing this row does
causes it — it was already false before this act and stays false after — so it is
recorded here rather than fixed inline. The sentence this row DID rewrite is true
independent of it: `LLR-182`/`LLR-189` and `LLR-207` are the only CMP-008 kitlib
rows.

NOT ON THIS LANE — the approval. `LLR-207` and `TC-205` stay `Drafted`; no
`docs/archive/last_approved/` write, no `intake.py snapshot`.
