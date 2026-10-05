# 002 — ADJUDICATE (independent, Claude Opus) — WI-803 plan gate, landed rows at `2a64d0b5`

Adjudicator: independent Claude Opus. I am the judge of verdict 001 and
authored none of WI-803's code or rows. Verdict 001 (`001-ADJUDICATE-eec8ac3.md`)
returned LLR-069, TC-069 and IF-153, and named an owed IF-161 amendment. This
verdict rules the text that landed for them in `2a64d0b5`, against the same anchors:
`docs/archive/last_approved/` for LLR and TC, and trunk `883b3edf` for IF.

## Basis (probed, not trusted)

- **Byte-exact landing.** Each landed row parses equal, cell for cell, to
  verdict 001's replacement text: LLR-069 `detail`, TC-069 `expected` and
  `evidence`, IF-153 `data` and IF-161 `consumers`. I compared them as parsed
  TOML against a scratch copy carrying 001's texts. TC-069 `expected` moved from
  a `"""` string to a `"` string, which is the same value, so this is encoding
  and not content. `eec8ac3c..2a64d0b5` changes no other registry row: LLR
  touches only LLR-069, TC only TC-069, IF only IF-153 and IF-161.
- **Lane bar**: `pytest tests/test_plan_coverage.py tests/test_plan_coverage_step.py
  tests/test_dual_plan_round.py` gives **41 passed**. `trace.py --strict` shows no
  finding or advisory on LLR-069, TC-069, IF-153 or IF-161; the one form finding
  is the pre-existing LLR-292. `check_trajectory.py --strict` is clean.
- **Mutation re-probe** on the landed code and tests, run against TC-069's landed
  `evidence`. Six mutants: unknown ref accepted (M3), cycle undetected (M4), a
  table-less plan exits 1 (M8), an absent SR registry becomes a finding (M10), a
  TC verifying a non-item SR enters the diff (M13), and a row citing nothing is
  accepted (M19). **All six are killed.** In 001, M3–M10 survived the narrowed
  evidence and M13/M19 survived everything. The whole-file evidence and the two
  new tests close those gaps.

## Rulings

- [MEANING] LLR-069 detail -> approved: rival plan tables only; resolves clause/SR/IF coverage and validates dependencies; uncovered clauses are report payload; findings (bad refs or plan graphs) exit 1, malformed inputs exit 2, an absent registry notes -> landed: one grammar for a DUAL goal run and a SINGLE item run; it also resolves TC refs and validates reasoned `Excludes:`; an unexplained clause gap is a finding in either run; a SINGLE run also fails an uncited item SR, or a TC verifying an item SR that no row names nor excludes, and an item SR cannot be excluded; findings (those gaps, and bad references, plan graphs or exclusions) exit 1; malformed input, including an item with no Done-when, exits 2; an absent registry notes -> not the same: a pre-gate implementation passes a gapped DUAL plan with exit 0, and the landed text requires exit 1. It also has no SINGLE run at all. Each clause is true of `plan_coverage.py` (`_check_one`, `spine_diff`/`diff_findings`, `check_excludes`, `load_item`, `_malformed`), and the old "bad refs or plan graphs exit 1" classification is restored. I would bless this text.
- [MEANING] TC-069 expected -> approved: clean plans emit pairwise coverage; findings exit 1; malformed inputs exit 2; absent registries note -> landed: a reasoned exclusion passes and clean plans emit per-plan and pairwise coverage; a bad reference or plan graph, an unexplained clause gap in either run, an undeclared or reasonless exclusion, an uncited item SR (even if excluded), or a TC verifying an item SR that no row names nor excludes exits 1 by name; malformed input, a missing Done-when included, exits 2; DUAL report bytes unchanged; absent registries note -> not the same: the pre-gate DUAL fixture's oracle moves from exit 0 to exit 1 with the report bytes held, and the SINGLE and exclusion cases are new. `method` (dual and single coverage, reference, graph, exclusion, SR/TC-diff, absent-registry and malformed-input cases) matches `expected`. Its `evidence` (all of `tests/test_plan_coverage.py`, plus the step module's single-plan-gap node) holds a test for every clause, as the mutants above show. I would bless this text.

Not ruled here, and owing no act: IF-153 `data` and IF-161 `consumers`
landed as 001 gave them and are true of the code (`format_report` writes
the pairwise diff over two or more plans, and `verifying_tcs` reads
`docs/test/test-cases.toml`). Both rows are `Drafted`, so neither has an
attestation to drift from.

## Aftermath

LLR and TC sit on a rung that `human_approval_through = "DevStg-Boundary"`
releases. Both MEANING rows are ones I would bless, so I re-attest them myself
in the lane's act: `intake.py snapshot --approves
"low-level-requirements.toml=WI-803;test-cases.toml=WI-803" --reattests
LLR-069,TC-069 --verdict docs/reviews/wi-803-plan-gate/002-ADJUDICATE-2a64d0b.md`.
The act is its own commit, separate from this verdict.

VERDICT: MEANING rows=2
