## 2026-09-04 — WI-595: LLR-207/TC-205 return and LLR-208/TC-206 amendment

The verdict rows describe every mechanism that now holds them. Two cells
returned by `docs/reviews/wi-590-adjudicate-llr-207-llr-208/004-ADJUDICATE-774ef35.md`
(`OUTCOME: RETURN rows=4`), plus round 011's MAJOR against two rows that act
approved. No new mechanism and no regression to write: every arm named below
already exists, passes, and was simply absent from the record.

**Re-drove the spec's four claims before editing anything.** All four hold on
this tree:

- `_peel_target` (`kitlib/verdict.py:431-442`) peels TWO classes, not one —
  `refresh_attestation` and `mechanical_close_attestation` (`:376-428`).
- `work_tip` calls `refresh_attestation` DIRECTLY (`:466`), never
  `_peel_target`, so the reset path peels only the refresh. The asymmetry is
  deliberate and was invisible in `LLR-207.detail`.
- `mechanical_close_attestation` is an `__all__` export (`:141`) and
  `grep -rn 'mechanical_close' docs/requirements/ docs/test/` returns ZERO
  rows — `LLR-207` is not one of several possible homes for it, it is the only
  one.
- `gen_verdict_rollup._off_trunk_refusal` (`:227-249`) refuses a direct write
  off the trunk with exit 2 (`main`, `:268-272`); `trunk_step.py:591` passes
  `--trunk-step` as the one allowed off-trunk caller.

### What changed

`LLR-207.detail` — the `governing_rev` clause said the walk peels "any verified
refresh it meets". Restated to name both disposable classes, the ONE property
that admits them (machine-authored, and the tree moves without the lane
changing what it claims), the verification each is admitted by, and the
fail-toward-review direction. Added the `work_tip` asymmetry explicitly: the
destructive reset path peels only the refresh.

`LLR-207.code_symbol` — added `mechanical_close_attestation` beside
`refresh_attestation`. `_peel_target` deliberately left out: private, and the
two attestation readers are the named surface.

`TC-205.method` / `.evidence` — `THE PEEL` enumerated the refresh arm alone and
neither cell held the string "mechanical". Added the second class in the same
idiom the rest of the cell uses — the positive and BOTH refusals — and cited
the three tests that already drive it and that no test case anywhere cited:
`test_the_mechanical_close_does_not_stale_the_round_it_follows`,
`test_only_the_machinerys_own_close_subject_peels`,
`test_a_close_that_reached_outside_docs_work_does_not_peel`. The positive also
drives the two peels COMPOSING (a refresh stacked on a close), which the cell
now states.

`TC-205.tier` — re-tiered `Smoke` -> `Full`, and the basis is recorded in
`Method` so the reading is not left open. Ruled rather than deferred: 8 of the
row's 49 citations live in `test_integrate_admission` / `test_integrate_station`,
both in `tests/conftest.py` `SLOW_MODULES` and so excluded from `-m smoke`.
`Full` is the smallest tier at which the WHOLE cited set runs, `Smoke` claimed
cheap-gate coverage for a set the cheap gate only partly runs, and sibling
`TC-132` already reads `Full` while citing the same station module. The Tier
field and the pytest marker remain a known unreconciled pair
(`docs/registry-machinery-reference.md` §12.2); this edit does not reconcile
them, it stops this row from misreporting on the side §12.2 names as the
harmful one.

`LLR-208.detail` (AMENDMENT to an Approved cell, §A5.2) — the cell said regen-set
membership "is the only thing that makes the exclusive-writer clause above
true". False since `7ea3cce7`. Amended to state BOTH mechanisms and keep them
distinct: `_off_trunk_refusal` is what ENFORCES the clause, regen-set membership
is what keeps the artifact FRESH. Neither substitutes for the other — a refusal
with no regenerator leaves the artifact written by nobody, and a regenerator
with no refusal is the state that shipped the WI-590 round 005 defect.

`LLR-208.code_symbol` — added `_off_trunk_refusal` (the row already names the
private `_extra`, so this matches its own convention).

`TC-206.method` / `.evidence` — stated the refusal arm and cited
`tests/test_verdict_record.py::test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`.

### Not inherited, not widened

WI-586's findings were re-driven and are all DISCHARGED (the spec's `## Context`
records the re-drive). NOT taken: the module docstring's contract paragraph and
`work_tip`'s docstring (`:448-455`), which still claims "`governing_identity`
measures code-time here" — false since `governing_identity` calls
`governing_rev`. That is a source-comment defect in a code lane's scope, not a
spine cell, and this return did not widen into it.

### Bar

`DevStg-Tests`, strong tier. Results in the close commit.
