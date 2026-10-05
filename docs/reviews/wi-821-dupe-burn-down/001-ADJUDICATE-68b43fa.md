# 001: ADJUDICATE (independent, Claude Opus), the WI-821 amendments at `68b43fac`

Adjudicator: an independent Claude Opus session. I wrote none of WI-821's code
(Claude Opus builder), none of its rows (GPT Terra), and neither review (Codex
6.1 Sol, rounds 1 and 2). This verdict answers the brief
`review-tmp/wave15/brief-wi821-amend-r1.md`. Is the amendment to LLR-210
(`detail`) and TC-314 (`method`) a change of MEANING or of CLARITY? It also
judges the amended text against the code at `HEAD`, per the coordinator's
lane-specific direction. Dispute 1 (D-001) is ruled in `dispute-1-ruling.md`.

Read: the brief in full; CLAUDE.md; the WI-821 spec in full;
`docs/decisions/wi-821.toml`; `sol-review-r1.md` and `-r2.md`; the
spine-authoring skill; trunk's WI-806 verdicts 003 and 005 and its dispute
ruling (for form). Code read at `68b43fac`:
- `consolidate.py`: `_commissioning_docs`, `_shared_commission`, `_model`,
  `pair_findings`, `clusters`;
- `kitlib/registry.shared_spec`;
- `check_trajectory.queue_conflict_pairs` and `approval_brief_findings`;
- `kitlib/spine.open_items_at`, `open_item_queue`;
- `trace.ruled_open_item_texts`;
- the new tests in `tests/test_consolidate.py` and `tests/test_rule_sync.py`.

## Basis (probed, not trusted)

- **Mutation probes.** I ran 10 single-point mutants on a `git archive` of
  `68b43fac` at `review-tmp/adj821/head` (`mutate.py`). The LLR-210 mutants ran
  against `tests/test_consolidate.py`. The TC-314 mutants ran against the
  `open_items` tests of `tests/test_rule_sync.py` and every other file TC-314
  cites (`test_open_item_readiness.py`, `test_open_item_queue.py`,
  `test_ruling_sync.py`). Before mutating, the base was green: 95, 3 and 41
  passed.
  - L1, the commissioning spec half made anchor-blind again (the before
    behaviour): **killed** by `test_two_sections_of_one_plan_are_two_commissioning_specs`.
  - L2, the commissioning spec half dropped: **killed** by
    `test_one_section_or_a_whole_file_still_pairs_on_the_commissioning_signal`.
  - L3, the open-item half dropped: **killed** by
    `test_a_shared_open_item_edge_is_a_commissioning_signal`.
  - L4, a whole-file specref no longer covering a section: **killed** by
    `test_one_section_or_a_whole_file_still_pairs_on_the_commissioning_signal`.
  - T1 and T2, the shared stage collapsing duplicate ids (last wins, then first
    wins): **killed** by `test_the_open_items_stage_keeps_duplicate_rows_in_sequence`.
  - T4, the brief lint reading only the last row of an id: **killed** (Sol's
    round-1 case).
  - T5 and T6, the ruled-prose reader and the owner queue keeping the first row
    instead of the last: **killed**.
  - **T3 survives every cited test.** In it, the brief lint reads only the
    FIRST row of a duplicated id
    (`pending = list(dict(reversed(pending)).items())[::-1]`). The cited
    duplicate case puts the row that warns first, so first-only and each-row
    agree there. I built the telling case (`t3probe.py`): a CSV registry with
    `OI-001,pending,Unrelated decision` and then
    `OI-001,pending,Approve the [p]-[DevStg-Reqs] batch`. It gives `['OI-001']`
    at `HEAD`, `['OI-001']` at trunk `b27ef5d1` (the before behaviour), and
    `[]` under T3. "The brief lint evaluates each row" is real behaviour that
    no cited test holds.
- **The commissioning spec half now selects nothing the pair producer does not
  already select.**
  - `pair_findings` feeds `queue_conflict_pairs` the same queued rows (`_model`
    passes `SpecRef` through). That producer's shared-SpecRef signal has read
    `kitlib.registry.shared_spec` since before this row: `check_trajectory.py:1654`
    at `b27ef5d1`.
  - The amendment points the commissioning spec half at the same function, so
    both signals now answer the same question on the same inputs.
  - Probe (`redundancy.py`): 400 random four-row queues over 7 specref and 5
    predecessor shapes. 776 pairs share a spec under the commissioning half,
    and **0** of them are missing from the pair producer's
    "share one spec of record" pairs.
  - At the base the half was anchor-blind and wider than the pair producer.
    That is why the before text's "a signal the pair producer cannot carry" was
    true then.
- **Lane checks.** Every evidence node of TC-314 and of the ten traced TC rows
  (69 nodes) exists as a `def` in its file. Run in the lane
  (`pytest -p no:cacheprovider -n 4 --basetemp
  C:/Projects/ai-template.wt/review-tmp/adj821/bt-ev <the 69 nodes>`): **261
  passed in 28.36s**. The lane stayed clean.
- **The replacement text was checked.** I applied the cells below to the scratch
  export (`repl.py`). `trace.py --strict` output there is byte-identical before
  and after (form-findings 1, the pre-existing LLR-292; paraphrase-advisories 3;
  integrity 0).

## Verdicts

- [MEANING] LLR-210 detail -> before: the census widens the pair producer with a commissioning signal that pairs two queued rows whose SpecRefs name one plan DOCUMENT (the file, whatever section each names) or that share an open-item edge -> after: the commissioning signal's spec half pairs two rows only when `kitlib.registry.shared_spec` says they name one spec of record, so two sections of one document do NOT pair, while the same section, or a whole-file reference beside any section, does -> not the same: a correct implementation of the before text (anchor-blind, mutant L1) fails the after text's two-sections case, so a selection case was removed.
- [MEANING] TC-314 method -> before: the method drives citation integrity, the SpecRef rules, the one projection and per-item staleness, and says nothing about duplicate open-item ids -> after: the same, plus a case: rows sharing an id keep carrier order in the shared status filter, the brief lint evaluates every such row, and by-id readers keep the last -> not the same: a test suite that satisfies the before method can lack the duplicate-id case entirely, so a test case was added.

## Ruling on the text: both rows RETURNED (not blessed as written)

LLR and TC sit on a rung the declared gate authority has released, so a MEANING
row I would bless is mine to re-attest. I would not bless either as written.

### LLR-210 `detail`: one clause is untrue of the code

- The after text says the census is "widened by two signals the pair producer
  cannot carry: rows commissioned by one spec of record or one open-item edge,
  ...". It then defines "one spec of record" by `kitlib.registry.shared_spec`.
- That is the rule the pair producer's own shared-SpecRef signal reads. The
  same sentence's "the same three signals" already includes it.
- So the spec half widens nothing: 776 of 776 probed pairs were already pairs
  of the producer's. Only the open-item edge is a commissioning signal the pair
  producer cannot carry.
- The row now contradicts itself, and a reader would believe the census selects
  by spec something the validator does not.
- The code is what the spec's Done-when asks for ("one rule rather than a
  second reading beside it"; same-section and whole-file rows "still do" pair
  on it). So the fix is to the text, not the code.

Replacement `detail`, byte-exact. Only the second sentence's signal list
changes, and two sentences are added after it. Every other byte is the lane's.

```text
The queue-overlap pre-filter's judgement half, as a producer of one adjudication row rather than a warn. `clusters` selects the candidate set from `check_trajectory.queue_conflict_pairs` — the same three signals reported at PAIR grain so a caller reads edges instead of parsing warn sentences — widened by two signals the pair producer cannot carry: rows commissioned by one open-item edge, and rows whose SR-Refs reach the same design-row `Module` or whose own body names the same source file. A pair's commissioning finding names every open-item edge the two rows share and the spec of record they share, if any. Two specrefs name one spec of record under the shared-spec rule the validator reads (`kitlib.registry.shared_spec`): two sections of one document are two specs, and a specref with no section covers the whole document. That rule is also the pair producer's shared-SpecRef signal, so a shared spec of record adds its name to the finding and selects no pair the pair producer does not already select. The population is the queued work rows (`queued_work`): a judgement row is never a candidate, and the `-000` example row is never one either. `census_draft` returns the row that cluster would mint, carrying its scope in the typed `Adjudicates` cell and its recursion guard in the typed `Digests` cell (a queue sha over the sorted id/title/needs/safety_class of the queued work rows, and a spine sha over the three spine registries). Three refusals, all over typed cells and recorded verdicts: none while a judgement is active, while another consolidation row is queued, while a queued judgement's `Adjudicates` names a row of the candidate set, or while a queued judgement sorts at or before the row this census would mint in `schedule.evaluate`'s own order (the would-be row at its priority, with an id above every id on file), each naming that judgement, and a queued judgement that does neither refuses nothing; none for a queue sha a consolidation row already carries in ANY status, terminal included; and a row an earlier consolidation judgement minted neither seeds a cluster nor may be re-absorbed. That row is read from the judgement that ENACTED the absorption (`enacted_absorbs`): a `done` consolidation row whose own spec records a `## Consolidation` outcome of `consolidate` (`parse_verdict`) and whose `## Dispositions` draft supersedes a `restructured` row (`absorbed_ids`); its successor is the row whose `Supersedes` names that row. A consolidation row that queued, edged or returned its rows, one cancelled, or one whose scope alone names them enacted nothing, and a hand consolidation leaves no such row, so neither makes a successor: the host seeds clusters and may be absorbed. The brief's prior-consolidation lines read every absorption from the successors' `Supersedes` (`prior_absorbs`), keeping an absorption after its successor is itself absorbed, and mark each absorbed row as judged, naming the judging row, or by hand (`prior_line`, `HAND_LABEL`), so a mixed absorption is marked row by row. `parse_verdict` and `close_refusal` read the verdict's typed outcome block and refuse by name for any row it moves that is not queued; `restructured_text`, `returned_text` and `edged_text` are the pure transforms the two call sites write back, and `archive_absorbed` performs the absorbed rows' move to the fourth terminal folder at the mint, where the successor's id exists.
```

The other cells stand. `code_symbol` adds `_commissioning_docs` and
`_shared_commission`, both defined in `consolidate.py` and both tagged
`Implements: SR-220, LLR-210`. `title`, `sr_refs`, `module`, `rationale` and
`test_refs` (TC-208) are unchanged.

### TC-314 `method`: one clause is not held by a cited test

- "The brief lint evaluates each row" is true of the code. Mutant T3 (first row
  only) survives every node TC-314 cites. The cited duplicate case only checks
  a registry whose warning row comes first.
- The fix is a test, plus one wording point. "retain the last row as before"
  is a receipt: it answers the version it replaced (skill §6, "a cell is not a
  receipt"). The rule needs no "as before".

Replacement `method`, byte-exact. It drops " as before" from the last sentence
and nothing else:

```text
Drive open-item and work-item registries in temporary repositories. An uncited pending item is an error with no work rows at all and without --strict, and a citer that is only deferred does not cite it, while a queued placeholder carrying only a title, a safety class, its needs token and a SpecRef to its item's registry record passes every check under --strict and is blocked. A registry SpecRef whose anchor names an item the row's needs do not cite is reported. A row keeping a registry SpecRef, under the TOML or the CSV spelling, is reported once none of its cited items is pending, whether the row is queued or deferred, and so is a row citing no item, while a cited item missing from the registry leaves it unreported. Cited cards, the uncited notice and the status snapshot read one projection. Backlog staleness clocks a registry SpecRef per cited item: filing an unrelated item stales no placeholder, and editing its own item does. Where duplicate open-item rows share an id, the shared status filter preserves their carrier order: the brief lint evaluates each row, while readers that require a by-id value retain the last row.
```

Replacement `evidence`, byte-exact. It appends the owed test:

```text
tests/test_open_item_readiness.py::test_an_uncited_pending_item_is_an_error_even_with_no_work_items; tests/test_open_item_readiness.py::test_a_ruled_items_row_may_not_keep_the_registry_as_its_specref; tests/test_open_item_readiness.py::test_a_placeholder_row_passes_every_check_and_is_blocked; tests/test_open_item_readiness.py::test_a_registry_specref_must_name_an_item_the_row_cites; tests/test_open_item_readiness.py::test_the_csv_carriers_registry_specref_is_judged_too; tests/test_open_item_readiness.py::test_specref_integrity_judges_every_open_row; tests/test_open_item_readiness.py::test_a_cited_item_missing_from_the_registry_is_not_ruled; tests/test_open_item_readiness.py::test_a_registry_specref_on_a_row_citing_no_item_is_reported; tests/test_open_item_queue.py::test_an_uncited_pending_item_is_a_notice_not_a_card; tests/test_open_item_queue.py::test_the_status_snapshot_lists_the_same_projection; tests/test_ruling_sync.py::test_a_registry_specref_is_clocked_per_cited_item; tests/test_rule_sync.py::test_the_open_items_status_filter_is_one_home; tests/test_rule_sync.py::test_the_open_items_readers_answer_by_value; tests/test_rule_sync.py::test_the_open_items_stage_keeps_duplicate_rows_in_sequence; tests/test_rule_sync.py::test_the_brief_lint_reports_a_duplicate_row_in_either_position
```

## Owed to the builder (a test gap, not row truth)

- **One test in `tests/test_rule_sync.py`, named exactly
  `test_the_brief_lint_reports_a_duplicate_row_in_either_position`.**
  - Write a CSV open-items registry holding two `pending` rows that share
    `OI-001`. The FIRST row's `OneLine` is `Unrelated decision`. The SECOND
    row's is `Approve the [p]-[DevStg-Reqs] batch` (no hierarchy-view link).
  - Assert that `check_trajectory.approval_brief_findings` returns one finding,
    for `OI-001`. The case with the order reversed is already in
    `test_the_open_items_stage_keeps_duplicate_rows_in_sequence`; the new test
    may parametrize over both orders.
  - It must be red under T3: in `approval_brief_findings`, after the
    `open_items_at` line, add
    `pending = list(dict(reversed(pending)).items())[::-1]`.
    `review-tmp/adj821/t3probe.py` is a working sketch.
  - TC-314's replacement `evidence` cites this exact name, so the test lands
    before or with that text, never after it.

## A separate finding (not a RETURN cause; for the coordinator to file)

**The commissioning signal's spec half is now a second copy of the pair
producer's shared-SpecRef signal.**

- For every pair of rows that share a spec, the census emits two finding lines
  for the same edge: "were commissioned by the same <spec>" and "share one spec
  of record (<spec>)".
- The spec asked for exactly this ("rows naming the same section, or one naming
  the whole file, still do [pair on it]"), so it is no defect of the build.
- A smaller design would drop the spec half and keep the commissioning signal
  to open-item edges alone. The selected clusters would be unchanged (probed
  above: 0 of 776). That fits WI-810, which folds consolidation into the mint
  step. If it is taken, LLR-210's replacement text above loses its last
  sentence.

## Traced cells (the other amended approved rows): true of the code, no act owed

`intake._amendment_drafts` mints no adjudication for these. I checked them
because the coordinator asked.

- **LLR `code_symbol`.** I used `traced.py`, which reads each symbol's
  `Implements:` declaration sites through `gen_arch_map.declaration_sites`
  over the row's `module` files. I also ran the kit's
  `trajectory_arch.codesymbol_crosscheck_findings`.
  - Every symbol the lane ADDED exists in its row's module and carries that
    row's tag:
    - LLR-124 `_source_doc_cmd` (`trunk_step.py:457`);
    - LLR-133 `_cited_cells` (`trace_text.py:785`);
    - LLR-137 `_spec_move` (`trunk_step.py:312`);
    - LLR-145 `expected_rebase` (`spec_move.py:300`);
    - LLR-181 `read_toml_text` (`kitlib/config.py`), and `plan_table_rows`,
      `_table_cells` and `_plan_header` (`kitlib/registry.py`);
    - LLR-197 `clip_line` (`kitlib/spine.py:447`);
    - LLR-299 `open_items_at` (`kitlib/spine.py`).
  - Every symbol the lane REMOVED is gone from the module: LLR-069 `_cells` and
    `_plan_header` (now `kitlib.registry`'s), and LLR-299 `_pending_items`.
  - Every symbol in each of the eight cells exists in its row's modules
    (`exist.py`, an AST name walk).
  - Some pre-existing symbols carry no `Implements:` line for their row. The
    list is identical at `b27ef5d1` and at `HEAD`, so this lane neither added
    nor removed that gap:
    - LLR-069 `parse_goal`, `parse_plan`, `check_plan`, `find_cycle`,
      `format_report`;
    - LLR-124 `REGEN_STEPS`;
    - LLR-137 `ordered_fragments`, `rebase_links`;
    - LLR-145 `move_spec`, `expected_relink`, `archive_dest`;
    - LLR-181 `first_declared_line`, `read_spec_rows`, `git_out`;
    - LLR-197's sixteen pre-existing names.

    The kit's crosscheck runs from a tag to its symbol, so it does not report
    them. Its one finding on these rows is also pre-existing at the base:
    LLR-210's tag on `_order_refusal`, which is absent from its `code_symbol`.
    I raise neither as a finding against this lane.
- **TC `evidence`.** Every node added to TC-016, -060, -126, -130, -139,
  -151, -176, -190, -193 and -208 exists and passes, in the 261-pass run above.
- **No act is owed for these rows.** A traced cell is not approved text, as
  with LLR-298 at WI-806, so none of them goes in `--reattests`. No snapshot
  was attempted (see Aftermath), so I have no refusal text to report.

## Dispositions

As the coordinator directed for this in-lane cycle (the owner's S11
direction), I am writing no `## Dispositions` block into the spec. The
replacement cells and the owed test above are the whole corrective work:

- the authoring lane applies the three cells byte-exact in their own text
  commit;
- the builder adds the test;
- a fresh verdict on the landed text comes before any act.

## Aftermath (not taken)

No snapshot was run. Both rows are returned, and I took no act on a returned
row. After the text and the test land:

- a fresh verdict rules LLR-210 and TC-314;
- if it blesses them, the act is
  `python project-trajectory/scripts/intake.py snapshot --reattests LLR-210,TC-314`.

No `--verdict` is needed, because the LLR and TC rungs are released.

VERDICT: MEANING rows=2
