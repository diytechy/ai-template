# 002: ADJUDICATE (independent, Claude Opus), the WI-821 amendments at `e50e3116`

Adjudicator: an independent Claude Opus session, the adjudicator of 001 and
`dispute-1-ruling.md`. I wrote none of WI-821's code or rows. This is the fresh
ruling 001 required, on the landed text of LLR-210 (`detail`) and TC-314
(`method`, plus its traced `evidence`), from the same brief
(`review-tmp/wave15/brief-wi821-amend-r1.md`). The lane is still on trunk
`b27ef5d1`, which has not moved (`git merge-base --is-ancestor` exits 0).

## Basis (probed, not trusted)

- **The landed text is 001's, byte for byte.** I parsed both registries at
  `HEAD` with tomllib. LLR-210 `detail`, TC-314 `method` and TC-314 `evidence`
  each equal the matching file in `review-tmp/adj821/replacements/`. They also
  equal the three fenced blocks of `001-ADJUDICATE-68b43fa.md`, which a regex
  pulled out of the committed file. Both rows' `status` still reads `Approved`.
- **No other cell moved.** I compared every row and every key of the
  low-level-requirement, test-case, system-requirement, stakeholder-need and
  interface registries at `e525ebbd` (001's commit) and at `HEAD`. The only
  cells that differ are LLR-210 `detail`, TC-314 `method` and TC-314
  `evidence`. `git diff --stat e525ebbd..HEAD` shows only those two registries
  and `tests/test_rule_sync.py` (+20). No script under `project-trajectory/`
  changed, so the code 001 judged is the code this text describes.
- **The owed test landed** (`2afb29d9`), named exactly as 001 asked:
  `test_the_brief_lint_reports_a_duplicate_row_in_either_position`.
  - It writes a CSV registry with two `pending` rows sharing `OI-001`. It runs
    the warning row in second position, then in first, and asserts one
    `OI-001` finding from `approval_brief_findings` each time.
  - The node id is exact; I checked the diff.
- **Mutation rerun.** I ran the same 10 mutants (`mutate.py`) on a fresh
  `git archive` of `e50e3116` at `review-tmp/adj821/head`. The TC-314 set now
  selects `-k "open_items or brief_lint"`. Before mutating, the base was green:
  95, 4 and 41 passed. **10 of 10 killed**, each by a cited node:
  - L1 (anchor-blind spec half): by
    `test_two_sections_of_one_plan_are_two_commissioning_specs`;
  - L2 (spec half dropped) and L4 (whole file no longer covers a section): by
    `test_one_section_or_a_whole_file_still_pairs_on_the_commissioning_signal`;
  - L3 (open-item half dropped): by
    `test_a_shared_open_item_edge_is_a_commissioning_signal`;
  - T1, T2, T4, T5 and T6: by
    `test_the_open_items_stage_keeps_duplicate_rows_in_sequence`;
  - **T3** (the brief lint reads only the first row of an id), which survived
    in 001, now dies by the new
    `test_the_brief_lint_reports_a_duplicate_row_in_either_position`.
- **The new LLR-210 sentences are true of the code.**
  - `_shared_commission` returns the open-item ids both rows wait on, plus the
    spec `shared_spec` gives, and the finding joins them. So "names every
    open-item edge the two rows share and the spec of record they share, if
    any" holds.
  - I reran the `redundancy.py` probe at `e50e3116`: 776 spec pairs, 0 outside
    the pair producer's shared-SpecRef pairs. So "selects no pair the pair
    producer does not already select" holds.
  - `test_the_commissioning_spec_half_is_the_shared_spec_rule` pins the spec
    half to `shared_spec` over every pairing shape.
- **Checks in the lane:**
  - TC-314 and TC-208 evidence: `pytest -p no:cacheprovider -n 4 --basetemp
    C:/Projects/ai-template.wt/review-tmp/adj821/bt2 <the cited nodes>` gives
    **73 passed in 3.34s**.
  - `check_trajectory.py --strict` is clean (exit 0).
  - `trace.py --strict`: integrity 0, form-findings 1 (the pre-existing
    LLR-292), paraphrase-advisories 3. These are the counts 001 recorded.
  - The lane stayed clean.

## Verdicts

- [MEANING] LLR-210 detail -> before: the census widens the pair producer with a commissioning signal that pairs two queued rows whose SpecRefs name one plan DOCUMENT (the file, whatever section each names) or that share an open-item edge -> after: the signals the pair producer cannot carry are an open-item edge and the module overlap; a pair's commissioning finding also names the spec of record two rows share under `kitlib.registry.shared_spec`, so two sections of one document do NOT pair on it, while the same section, or a whole-file reference beside any section, does; that rule is the pair producer's own, so the spec half adds a name to the finding and selects no extra pair -> not the same: a correct implementation of the before text (anchor-blind, mutant L1) fails the after text's two-sections case.
- [MEANING] TC-314 method -> before: the method drives citation integrity, the SpecRef rules, the one projection and per-item staleness, and says nothing about duplicate open-item ids -> after: the same, plus a case: rows sharing an id keep carrier order in the shared status filter, the brief lint evaluates every such row, and by-id readers keep the last -> not the same: a test suite that satisfies the before method can lack the duplicate-id case entirely, so a test case was added.

## Ruling on the text: both rows BLESSED

- **LLR-210.** Every clause is true of the code at `e50e3116`, and a cited
  node in TC-208 holds each clause.
  - Up: SR-220 is the parent, and the row decomposes its census into the
    selection, the guards and the memory, as before.
  - Sideways: the spec-of-record rule is now stated once, by reference to
    `kitlib.registry.shared_spec`, the validator's own rule (LLR-160's pair
    producer). It is a reference, not a second reading.
  - Down: TC-208 cites the four new consolidate tests, and they kill L1 to L4.
  - What 001 returned the row for, "a signal the pair producer cannot carry"
    applied to the spec half, is now stated as the code behaves.
- **TC-314.** Every clause of the method is true of the code. Since T3 dies,
  each clause of the new duplicate-id sentence is held by a cited node. The
  receipt phrase " as before" is gone.

LLR and TC sit on a rung the declared gate authority has RELEASED. Both rows are
MEANING and both are rows I would bless, so the re-attestation is mine to take,
by `--reattests`. No `--verdict` is owed, because the rule that requires one
applies only to a held rung.

## Traced cells

The ten traced TC `evidence` cells and eight LLR `code_symbol` cells that 001
confirmed are unchanged since 001. Their code is unchanged too, so 001's
confirmation stands. They owe no act.

## Aftermath (the act, in the lane, uncommitted, for the coordinator to commit)

The act re-anchors exactly LLR-210 and TC-314, and changes no `Status`:

`python project-trajectory/scripts/intake.py snapshot --reattests LLR-210,TC-314`

VERDICT: MEANING rows=2
