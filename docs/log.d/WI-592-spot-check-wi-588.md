## 2026-09-04 — WI-592: spot-check of the clean close of WI-588

Sample-tier `complete_review` (`docs/process.toml [attestation] complete_review =
'sample'`) on a GREEN close. Nothing was alleged and nothing is reversed; the
close stands. The one question asked: does what shipped answer what the row
asked for?

VERDICT — **it does.** All three items WI-588's row asked for shipped, and the
one that mattered is genuinely DRIVEN rather than merely written down.

### Why this was re-driven rather than read

WI-588's whole subject was a registry cell that read TRUE while nothing drove
it. Reading its three deliverables off the cells would therefore have repeated
the exact error it was sent to correct. So the mutation was re-derived at THIS
tip (`2a978d11`), applied and reverted; `git diff` over
`project-trajectory/scripts/trunk_step.py` is empty and `git status` clean.

BASELINE — `tests/test_trunk_step.py`: `18 passed in 2.32s`.

MUTATION — the whole `verdict-rollup` tuple deleted from
`trunk_step.REGEN_STEPS`, leaving the module valid with **zero**
`verdict-rollup` occurrences in it. Under it:

- `tests/test_trunk_step.py`: `1 failed, 17 passed`. The single red is
  `test_regen_really_writes_the_verdict_rollup`, and it reds on the arm that
  names the step that stopped running — `assert "regen — verdict-rollup ok" in
  captured.out`, whose failure text is the printed step list with that step
  absent. Bidirectional, and the file is no longer blind end to end.
- `TC-206`'s four PRE-EXISTING cited evidence nodes
  (`test_the_rollup_is_generated_and_its_check_has_two_answers`,
  the two `test_generated_freshness_wiring` nodes, and
  `test_every_declared_freshness_step_is_skipped`): `4 passed`. They stay blind
  exactly as WI-588 stated — the deliverable's account of what the mutation
  leaves green is accurate.

CELLS — `TC-206.method` carries the arm ("THE TRUNK WIRING IS DRIVEN, NOT READ
BACK OFF THE TABLE THAT DECLARES IT"), `TC-206.evidence` cites the node, and
`LLR-208.detail` names all four elements the row asked for: the
`verdict-rollup` id, the `docs/reviews/` arming guard, the LEAF position, and
membership-in-the-set as contract rather than accident.

Both rows now read `Approved` where WI-588's deliverable said `Drafted` — that
is the adjudication minted at its merge doing its job, not drift.

NOT A FINDING, recorded so the next reader does not re-derive it: the live
tuple is `_cmd("gen_verdict_rollup.py", "--trunk-step")`, where WI-588's spec
quoted it without the flag. `--trunk-step` arrived in `7ea3cce7` (2026-09-04,
the exclusive-writer enforcement), which is NOT an ancestor of WI-588's close
`6f274193`. The quotation was accurate at its own tip.

### One residual — surfaced as a successor draft, not fixed here

WI-588's amendment to `LLR-208.detail` added the clause "armed by the presence
of `docs/reviews/` and **skipped with a printed notice** wherever that
directory is absent". That clause is TRUE — driven by hand here, `regen()` on a
bare tree prints `trunk_step: regen — skipping verdict-rollup (docs/reviews/
absent).` — but **no test asserts it.** Both arms that could
(`test_regen_skips_absent_artifact_families` and
`test_regen_runs_in_declared_dependency_order`) enumerate a SAMPLE of five step
names — `okf`, `derived-stage`, `trajectory`, `status`, `open-items` — and
neither includes `verdict-rollup`.

This is the same class of gap WI-588 existed to close, one scale smaller and
introduced by its own amendment: a cell clause that reads true with nothing
driving it. It is small on its own, and the interesting part is not this step —
it is that the sampling means EVERY regen step added since those two arms were
written, and every one added next, inherits the same silence. The remedy is a
generalization (assert over the whole `REGEN_STEPS` table), not another arm,
which is why it is a successor rather than a one-line follow-on. Drafted in the
spec's `## Dispositions`.

### Harness

Full unfiltered suite driven at the close tip; result recorded with the close
commit. No source file was changed by this WI — the only tree delta is this
fragment and the spec's own close edits.
