Reviewed: 75e836b6463acaf6788ed0bb8d4776b575282f26

### REVIEW-B (Claude Opus stand-in) — WI-994 full-lane review — 2026-11-04

**Verified.** Hunted first: a tag dropping out with no word (fail-open), an unreadable file reading as "no tags", a fixture string read as a tag, and source-side reads changing. None of those was reachable on the spec's declared shapes, apart from finding 3.

Driven through the real `read_test_tags` and `tc_tag_findings`: CRLF, BOM, NUL byte, bad indent, a trailing backslash, 3.12-only syntax, `.sh`, `.ps1`, `.js`, `.sql` and `.cmd` files, and a CSV TC carrier, which reads and drops `-000` correctly. `tc_tag_findings` over this repository gives 0 findings in 3.06 s on a loaded box.

Twenty mutants of the reader and the surface ran in an exported copy, and 19 were killed by the lane's tests. The survivor is the sticky `after_tag` one, recorded in the notes below. It first showed as killed only because the scaffold test errors in that partial copy; rerun over `tests/test_gen_arch_map.py` alone, it survives. The tip's `tests/test_gen_arch_map.py` run against the pre-fix `gen_arch_map.py` (566d0ec43) fails 6 tests, among them the comma-and-`and`-led wrap cases and the opening-rule test, so those regressions are red before the fix. The 6 ERRORs in that run are environment errors of the partial copy, not verdicts.

Retirement is deletion (PROCESS.md, "A retired spine row is deleted"), so reading every non-example row as live is correct, and the deleted-row case is covered in `test_a_draft_tc_is_clean_and_an_absent_one_is_refused`.

Done-when map:
- Reader and signatures: `test_the_code_side_readers_keep_their_output_over_the_scripts_tree`, `test_backlink_ids_applies_the_tag_readers_opening_rule`.
- Grammar: `test_the_tag_reader_reads_each_python_read_position`, `test_tags_at_both_levels_union_and_a_repeat_is_clean`, `test_a_non_python_test_file_is_read_at_file_level`, `test_each_misplaced_shape_is_named`, `test_each_malformed_shape_is_named`, `test_a_tag_naming_no_live_tc_is_unknown`, `test_a_file_that_cannot_be_read_is_refused`.
- Surface: `test_tag_findings_warn_plain_and_error_under_strict`, `test_the_tag_check_is_vacuous_with_no_tests_root_or_no_registry`, `test_the_tag_check_on_a_bootstrapped_scaffold`. Its wall-time clause is UNCOVERED (finding 2).
- Regressions: each listed case has its test.
- One home in text: PROCESS.md §3, AGENTS.template.md, EXAMPLE.md §5, the registry reference and the enforcement audit all carry it. Bytes are 9,992 / 98,912 / 4,565, matching the stamped baselines.
- Spine: present, with finding 1 against LLR-365's text.
- RESYNC entry: present, in the anchor shape the preceding entries use.
- Not in this row: the RESYNC half is present; the log half is UNCOVERED (finding 2).
- Coverage bound: stated in LLR-365.
- WI-997: filed in `docs/work/queued`, needing WI-994 and OI-125.
- Review bar A+B: this round.

Rubric: K2 holds, since no SN or SR cell changed and LLR-365 names no code. K3 holds: `read_test_tags` and `tc_tag_findings` each carry SR-157 and LLR-365, both modules and both symbols sit in the row, no approved row changed and no Status flipped.

Requirement/interface record:
- Changed side IF-131 `data` adds `read_test_tags`. Counterpart: the `Contract IF-131` text in `gen_arch_map.py`, carried. `requestors` retained, because `check_trajectory` stays the row's consumer through the rule surface it re-exports from `trajectory_arch`, as for the row's other entries.
- Changed side IF-263 `data` adds test-file tags. Counterpart: the `Contract IF-263` text in `trajectory_arch.py` and the `check_trajectory.py` contract, carried.
- SR-157 retained: its text already covers every declared spine rule violation with row-level attribution, and the new child adds a rule without changing that contract.
- LLR-204 retained: `backlink_ids` behaviour is unchanged, shown by the frozen regression.

Decomposition: one LLR under SR-157. TC-404 read positions, TC-405 misplaced, TC-406 malformed, TC-407 unknown, TC-408 unreadable and TC-409 surface each verify an independent arm; a further LLR split would repeat one grammar and add no independent decision.

Consolidation: `_continues_tag_list` was compared with `_refuse_ambiguous_continuation`. They differ in id family, scope and outcome (a one-line predicate against a paragraph-wide raise), so it is no repeat. `_tests_dir`, `_walk_roots`, `spine_carrier.load` and `IMPLEMENTS_RE` are reused, and no other test-file predicate exists in the scripts.

Status: `docs/status.md` is not in this diff, so no prose/policy check arises. PROCESS.md §5 workaround question: not applicable, since LLR-365 is new and preserves no unsuitable row.

**Notes (no severity, not counted).**
- Coverage extensions the change fails closed on: a `test*` method of a unittest class not named `Test*` is refused as misplaced though pytest collects it by default; a tests root overlapping the source root refuses source declarations; a `.cmd` file has no tag form; a JS `node_modules` under the tests root is walked, since only dot and `__pycache__` parts are skipped.
- Rare and not filed: a finding's line runs one short in a `"""\` continuation docstring (driven: reported 3, physical 4) and one long after a form feed in a docstring (driven: reported 4, physical 3). No test file here uses the continuation form.
- Test gap, outside the Done-when: the sticky `after_tag` mutant survives, so "only that line" in `_read_text_tags` has no pin.
- `[paths] tests` holding two space-separated roots reads as vacuous, but `trace.py` and `check_trajectory.py` both treat the value as one root and the template declares one, so this is not a supported shape.
- Finding 2 rests on count-only greps of the log fragment and of the range's log diff; the fragment itself was not read, per the brief.

**Commands.**
- `git rev-parse HEAD` -> 75e836b6463acaf6788ed0bb8d4776b575282f26
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2b/wi-994 tests/test_gen_arch_map.py tests/test_trajectory_arch.py tests/test_trajectory.py tests/test_bootstrap.py` -> 354 passed, 1 skipped in 212.09s (the skip is the posix-shell gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (994 work item(s), 881 done (89%), 34 cancelled, graph acyclic). Exit 0.
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=138 LLR=331 TC=363 orphans=0 integrity=0 ... interface-findings=0. Exit 0.
- `python -m pytest -q -p no:cacheprovider --basetemp .../r2b/ratchet tests/test_module_size_ratchet.py` -> 4 passed in 2.09s
- `r2b/mutate.py`, 20 mutants over an exported copy -> 19 killed; the sticky `after_tag` mutant survives (97 passed, 6 environment errors, on rerun)
- tip `tests/test_gen_arch_map.py` over `gen_arch_map.py` at 566d0ec43, in the exported copy -> 6 failed, 91 passed, 6 errors
- `r2b/probe1.py`, `p3.py`, `p4.py`, `p5.py` -> the driven cases above

**Findings.**
- [MINOR] docs/requirements/low-level-requirements.toml:1564 -> K1: LLR-365 defines malformed only as "a declaration whose list is not test-case ids only", but the code also refuses two shapes that text does not reach: a read-position line whose token follows prose and names a test case, which is no declaration under the grammar, and a next line continuing a valid list, whose declaration line is TC ids only. TC-406 verifies a refusal its LLR does not state, and the Done-when's Spine and Grammar items ask the row to state the rule and these shapes -> amend the `detail` cell, through in-lane adjudication, to name both shapes as malformed -> @owner
- [MINOR] docs/log.d/WI-994-test-files-tag-their-tcs.md:1 -> two Done-when clauses are UNCOVERED at this tip: the Surface item says the bar's added wall time is "measured and stated in the log", and the Not-in-this-row item says the exclusions are stated in "the RESYNC entry and the log". Count-only greps of the fragment find 0 lines for `wall`, a seconds figure, `measured` or `smoke`, and 0 for `WI-997`, `red_mark`, `evidence column` or `Not in this row` -> add the measured figure and the exclusions to the fragment before landing -> @owner
- [MINOR] project-trajectory/scripts/gen_arch_map.py:2020 -> a `test*`-named `@pytest.fixture` is read as a test, so its tag maps a node pytest cannot run, with no finding; the spec closes fixture docstrings as misplaced and "never silently ignored". Driven: `@pytest.fixture def test_client()` tagged TC-1 returns `{'TC-1': ['tests/test_a.py::test_client']}` and no finding, and a method-level fixture does the same. It is rare: 0 such fixtures in this repository, and tagging one is a builder's mistake, but WI-995 would then select that node -> treat a def decorated `fixture` or `pytest.fixture` as no read position and add a `test_each_misplaced_shape_is_named` case; this stays a check because the AST carries no collection result, so the non-test cannot be made unrepresentable without running pytest's collector, which this reader must not do -> @owner

VERDICT: CHANGES-REQUESTED findings=3
