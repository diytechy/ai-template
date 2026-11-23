# WI-1024 slice 1: the record

The first of the five slices the plan ([plan.md](plan.md), section 4) sets out,
built from the confirmed plan (`40336c427`, D1 to D21 as proposed) on
`maint/wi-1024` at base `bba30552f`, not rebased (D16: `Constrains` joins
`intake.ROUTED_TRACED_CELLS`; the coordinator moves the line at the second
merge with WI-1060). The spec stays in `docs/work/queued/` until slice 5 (D10);
this file stands in for the Deliverable until then.

Slice 1 is the mechanism, the re-cuts except LLR-042 and TC-080, and the
population of CMP-009's 23 interfaces and the four `external:`-owned ones,
all of it for sitting A. Slices 2 to 5 are not started.

## 1. What changed, against the Done-when

| Done-when | Slice 1 |
|---|---|
| 1. The cells | `kitlib.spine.SPINE_TIER_KEYS`: `constrains` on SR, `constrains`, `dimensions`, `out_of_domain` on LLR; `spine_carrier.SPINE_COLUMN` and `migrate_carrier.KEY` (`Constrains` a ref column). Findings in `coherence.constrains_findings`, joining `trace.py --strict`'s interface failure set: a dead, non-interface or example id on either tier; a `dimensions` cell the grammar refuses or naming a strategy outside its three; an `out_of_domain` that is not one line ending in a full stop with no sentence end inside; either companion on a row constraining nothing. An empty list stays the carrier's explicit-empty refusal on read. The warn-first missing-cell line, counted by channel (`coherence.companion_advisories`). The grammar's one parser moved to `kitlib.spine.parse_dimensions`; `gen_cases.parse_spec` calls it. The LLR and SR templates' example rows and the interface registry header (live and template) state the cells; the SR template's `permutations` guidance says system boundary only. Class: `Constrains` traced and routed on SR and LLR, `Dimensions` and `OutOfDomain` accepted. |
| 2. The derived check | `kitlib.spine.interface_reach` (the blast radius); `coherence.interface_coverage`, `coverage_advisories`, `coverage_line`: each interface reaching no test case the harness runs is named, observation-only ones on their own line, one count line by route; the `[checks] interfaces_check` opt-out silences it (D5). Warn-first. |
| 3. The repeat check | `coherence.repeat_findings`, per pair, as worded (D2); reported warn-first, never in the commit hook's integrity check. |
| 4. Every interface reached | CMP-009 and the four `external:` rows: 27 of 239 interfaces now reached through a constraining design row (section 3). Slices 2 to 4 carry the rest. |
| 5. Strict, OI-43 retired | Not in this slice (slice 5). |
| 6. The readers | `kitlib.spine.llr_placement(tcs, ifs, llrs=())` places through `constrains`; every caller passes the design rows: `trace_text.placement_line`, `gen_components.build` (the component view), `traj_parse.placed_llrs` (the dashboard's design-row detail), `intake._placement` (the build brief), `check_trajectory._placed_sr_components` (the knowledge-pack advisory), `assumption_rules.component_srs` (the interface-form gate's fallback, D8). Interface coverage is counted by `coherence.coverage_line`, LLR and SR `constrains` alike. |
| 7. RESYNC | The slice-1 entry, "Requirement rows name the interfaces they constrain, with the behaviour's input set, and interface reach is reported warn-first [since bba30552f]". |
| 8. Checks and tests | Section 2. |

Documents: `PROCESS.md` §4 (the LLR's `dimensions` beside the SR's
`Permutations`; +210 bytes, restamped in the byte-budget skill, both copies),
`docs/registry-machinery-reference.md` (the three cells, the class table,
interface reach). Ratchets re-stamped with reasons: `trace.py` 3784 -> 3801
(wiring only; the console's two count lines moved into `_count_lines` so
`render_console` keeps its cognitive baseline), `intake.py` 1946 -> 1951,
`check_trajectory.py` 1663 -> 1665; the cognitive baseline loses
`gen_cases.parse_spec`'s row (the parser moved to `kitlib.spine` and was
split there under the threshold). The golden report
`tests/golden/offspine.txt` gains the coverage lines. The byte-budget skill's
three copies (`project-trajectory/skills`, `.claude/skills`, `.agents/skills`)
carry the PROCESS.md restamp. The views were regenerated
(`trunk_step.py --regen`): the derived stage's live stage reads
DevStg-LLReqs while the 14 new `Drafted` rows wait (settled stage unchanged).

## 2. Red first, and the tests run

**Red first.** The new and extended tests, run against the base code (the
build's `project-trajectory/` changes stashed, the tests kept):

```
21 failed, 1 passed in 7.28s
```

The one that passed is `test_the_interface_check_opt_out_silences_coverage`,
which asserts an absence the base code also satisfies. The same set against
the build: `22 passed in 10.52s`. TC-533's test
(`test_the_guard_reads_its_caller_and_root_from_the_agent_tools_environment`)
characterizes behaviour that already existed and LLR-423 newly states, so it
is green against the base too.

**The tests run** (builder rule 5):

- Every test module importing a changed module (`kitlib.spine`, `coherence`,
  `trace`, `trace_text`, `gen_cases`, `spine_carrier`, `migrate_carrier`,
  `acceptance_record`, `intake`, `check_trajectory`, `gen_components`,
  `traj_parse`, `assumption_rules`, `coordinator_guard`, `gen_trajectory`),
  the modules holding every touched TC's tests, and the four named ratchet and
  sync modules: 125 modules, `-n 6`, on a loaded box:
  `1 failed, 4501 passed, 18 skipped, 18 warnings in 6947.30s (1:55:47)`. The
  one failure, `tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`,
  was the committed stage before the views were regenerated; after
  `trunk_step.py --regen`: `31 passed in 215.20s`.
- The commit hook's cognitive-complexity step then refused four new
  functions over the threshold and `render_console`'s growth; they were
  decomposed outward (behaviour unchanged) and the affected modules rerun:
  `tests/test_constrains.py`, `test_gen_cases.py`, `test_llr_trace_cells.py`,
  `test_gen_components.py`, `test_if_owner_component.py`,
  `test_trace_golden.py`, `test_complexity_ratchet.py`,
  `test_module_size_ratchet.py`, `test_import_layers.py`,
  `test_coordinator_guard.py`: `1 failed, 209 passed in 57.84s`, the failure
  the size ratchet's `trace.py` stamp (3797 -> 3801), re-stamped with its
  reason: `4 passed in 1.76s`.
- `trace.py --root . --strict`: exit 0, `Traceability: SN=31 SR=141 LLR=363
  TC=434 orphans=0 integrity=0 ... interfaces=239 interface-findings=0`.
- `check_trajectory.py --root . --strict`: `check_trajectory: clean (1060
  work item(s), 932 done (88%), 37 cancelled, graph acyclic).`
- `check_docs.py --root .`: `check_docs: OK - 3677 doc(s), 3832 intra-repo
  link(s), 0 broken.`; `scripts/check_resync.py`: `check_resync: OK, 17
  shipped path(s) changed; entry anchored at bba30552f...`.
- `run_menu.py smoke`, once, after the build commit, exit 0:
  `3786 passed, 3 skipped, 18 warnings in 183.17s (0:03:03)`; `smoke budget:
  CPU 742.4 s vs 540 s cpu-seconds; wall 183.9 s vs 600 s wall-seconds; meter
  windows-job; 24 logical CPUs -> OVER`, a warning the checks do not fail on
  (the known over-budget tier, re-tier row WI-1039).

The full importer run preceded the behaviour-preserving decomposition the
hook asked for; after it, the modules holding the decomposed functions' tests
and the smoke tier ran, not the 125 again.

## 3. The population

Every slice-1 interface reaches a test case the harness runs through a
constraining design row. One row per interface; a row constraining several
interfaces of one surface constrains them all. "Link" means the row's text
already stated the behaviour and named no code, so only `constrains` changed;
"amended" means rule 1 scrubbed its inherited code names too (D9), meaning
unchanged except where a clause no test drove was cut (named in the line).

| Interface | Channel | Constraining row | Change | Clause-to-test |
|---|---|---|---|---|
| IF-011 | exit-code | LLR-130 | amended `detail` | stale and current: TC-079 `test_check_passes_fresh_and_trips_stale`; missing: `test_check_missing_html_is_stale`; stamp excluded: `test_asof_stamp_from_git_and_excluded_from_check`; outside git: `test_no_git_means_no_stamp_and_stays_deterministic` |
| IF-012, IF-149 | exit-code, file | LLR-039 | amended `detail` | one file per row with links and indexes and the specification pin: TC-042 `test_bundle_generates_typed_linked_concepts`; deterministic, stale after a registry edit, current after regeneration: `test_generation_is_deterministic_and_check_gates_staleness`; writes-if-changed, prune, extra file: `test_write_mode_prunes_and_check_flags_extras`; guides: `test_process_guides_emit_with_derived_summaries`, `test_process_guides_skip_absent_docs`, `test_process_guides_absent_on_vacuous_scaffold`; opt-out: `test_opt_out_silences`; example rows only: `test_placeholder_only_scaffold_is_vacuous`. Cut, no test drove them: the duplicated-loaders clause (a retired rule), the legacy sentinel file, "a missing bundle file" and "a document edit". |
| IF-014 | bytes | LLR-010 | amended `detail` | harness passes out of the box: TC-010 `tests/test_bootstrap.py`; the toolchain open item, its queued placeholder and the marks: `tests/test_profile.py::test_the_scaffolded_oi3_is_filed_with_its_queued_placeholder` |
| IF-017 | stdout | LLR-024 | link | grammar and case set: TC-024 `tests/test_gen_cases.py` (pairwise, boundary corners, interior points, the TOML and CSV forms) |
| IF-018 | file | LLR-033 | link | the checklist and its budgets section: TC-033 `test_release_checklist_lists_perf_budgets` |
| IF-019 | file | LLR-025 | link | the index from the skills' frontmatter: TC-025 `tests/test_skills_index.py` (`test_index_row_count_matches_skill_dirs`, `test_every_skill_frontmatter_is_valid`); "a drifted index is detectable" has no named test in that file (file-level evidence only) |
| IF-029 | file | LLR-013 | amended `detail` | malformed fails: TC-013 `test_missing_section_fails`, `test_diagram_without_ids_fails`, `test_unknown_id_fails`; conformant passes: `test_real_flow_with_known_ids_passes`; the default document: `test_fresh_scaffold_template_section_passes`. Cut, no test drove it: the re-homing sentence |
| IF-030 | file | LLR-012 | amended `detail` | dead link: TC-012 `test_broken_file_link_fails`, `test_broken_anchor_fails`; vision tag: `test_missing_vision_tag_fails`; clean set: `test_clean_scaffold_passes`; built-in step from DevStg-Reqs: `test_harness_runs_doc_navigability_at_g1`, `test_harness_wires_stale_into_doc_navigability`; orphans: `test_orphan_warns_by_default_and_fails_when_strict`; the allowlist: `test_declared_class_suppresses_expected_orphan`; staleness only warns: `test_staleness_prints_hint_not_warn` |
| IF-032 | git | LLR-017 | link | staged diff: TC-017 `test_staged_key_and_token_shapes`; message: `test_message_mode_scans_a_commit_message_file`; range: `test_range_mode_catches_history_and_messages`; independent of the privacy toggle: `test_secrets_floor_runs_with_privacy_off` |
| IF-035 | file | LLR-279 | amended `detail` | the copy: TC-289 `test_a_multi_file_skill_materializes_whole_and_passes_the_drift_check`; the inventory: `test_the_delivery_inventory_lists_a_skills_companion_file` |
| IF-036 | bytes | LLR-022 | link | drift and match: TC-022 `test_drift_warns_and_strict_fails`, `test_matching_copy_is_ok` |
| IF-039 | bytes | LLR-171 | amended `detail` | non-Python scaffold passes the integrity and schema checks: TC-165 `test_every_profile_permutation_scaffolds_and_passes`; the token scan: `tests/test_language_neutral_scheme.py` |
| IF-041 | cli | LLR-026 | amended `detail`, `rationale` | prompt on standard input and the no-wedge invariant: TC-026 `tests/test_agent_loop.py`; the tree kill, idle deadline, interruption, uncontainable child, the 10 s bound, an unopenable member, an ordinary launch error: TC-026 and TC-374 `test_session_stdin` and `test_kitlib_winjob` tests by name. The Codex last-message capture is driven only at file level |
| IF-048, IF-157, IF-158 | stdout, cli, exit-code | LLR-047 | amended `detail`, `rationale` | list form, direct launch and exit passthrough, unknown name 2, piped and closed standard input, absent section 1: TC-047 `tests/test_run_menu.py` tests by name; the interpreter's directory and the POSIX shims: `test_a_capabilitys_python_is_the_menus_own_interpreter`, `test_the_posix_shim_runs_exactly_the_interpreter_it_names`; the launchers' search, the readiness call, the direct and list forms: TC-342 `tests/test_run_devsetup.py` tests by name. Cut, no test drove them: parsing without interpolation, keeping a name's case, dropping an orphan description or an empty command |
| IF-074 | file | LLR-118 | amended `detail` | each section and its order: TC-123 `tests/test_gen_open_items.py`, `test_open_item_queue.py`, `test_a_claimed_citer_is_a_card_and_on_the_blocked_list`, the verdict audit tests; the assumption cards: TC-448 `tests/test_open_items_assumptions.py` tests by name |
| IF-088 | call | LLR-198 | amended `detail`, `rationale` | the typed model: TC-194 `test_the_typed_model_kinds_every_pending_item`; cards less the pause: `test_operator_cards_is_pending_items_minus_the_pause`; the block: `test_the_block_renders_exactly_the_model`; three readers: `test_the_dispatcher_reads_the_model_not_the_render_facade`, `test_the_operator_surface_reads_the_model_not_the_render_facade`; the former names: `test_facade_reexports_pending_compatibility_names`; the pause: `test_pause_projection_is_deterministic`, `test_malformed_pause_still_projects_fail_closed` |
| IF-139, IF-140 | exit-code, file | LLR-199 | re-cut (section 4) | TC-195 tests by name, and `test_a_design_row_sits_where_the_interface_it_constrains_is_owned` (new) |
| IF-164 | file | LLR-124 | amended `detail` | regenerated on the trunk and stale-checked: TC-060 `tests/test_trunk_step.py`, `tests/test_gen_trajectory.py` (file level) |
| IF-227 | call | LLR-258 | amended `detail` | each clause: TC-251 `tests/test_traj_views.py` (file level) |
| IF-254 | exit-code | LLR-281 | amended `detail`, `rationale` | under the floor refused by name and at the floor passing, after the index is written: TC-291 `test_check_refuses_a_description_under_the_floor`. "Called first" cut (no test drives the order) |
| IF-277 | env | LLR-423 (new) | new, Drafted | the session variable and no other: TC-533 `test_the_guard_reads_its_caller_and_root_from_the_agent_tools_environment`; the root given, else the variable, else the working directory: the same test |
| IF-292, IF-293 | cli, exit-code | LLR-320 | amended `detail` | report first, offers only at a terminal, menu input kept, exit by the handed interpreter, standalone check read-only: TC-343 `tests/test_run_devsetup.py` tests by name |

Why LLR-423 is new rather than LLR-300 amended: LLR-300 (4,556 characters,
about 25 clauses and many code names) names the session variable inside its
claim-refusal clause, and nothing states the root default. Linking it would
have meant rewriting the whole coordinator-guard row under rule 1 for one
interface. LLR-423 states the reading of both variables. LLR-300's clause
overlaps it and could cite it when that row is next amended (section 6).

**By channel** (the warn-first line at the tip; every pair is "without"):

| Channel | Constrained pairs | With both companion cells | Without |
|---|---:|---:|---:|
| bytes | 3 | 0 | 3 |
| call | 2 | 0 | 2 |
| cli | 3 | 0 | 3 |
| env | 1 | 0 | 1 |
| exit-code | 6 | 0 | 6 |
| file | 9 | 0 | 9 |
| git | 1 | 0 | 1 |
| stdout | 2 | 0 | 2 |

No slice-1 row carries `dimensions` or `out_of_domain` (D21): no existing test
drives an out-of-domain behaviour for any of them. The grammar does fit the
input of four: LLR-130 (the committed dashboard: current, stale, missing),
LLR-281 (a description under or at the floor), LLR-320 (the handed
interpreter and a terminal) and LLR-024 (the strategy and output form). Each
needs a test of its out-of-domain behaviour before both cells can be written.

The tip's lines: `placement: 131 design row(s) placed, 232 unplaced`;
`interface coverage: 239 interface(s): 27 through a constraining design row,
0 through a constraining requirement, 118 through a naming test case, 0 by
observation alone, 94 unreached`; no repeated name is reported.
<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev="1422d9b6a" -->

## 4. The re-cuts

LLR-199, TC-195, LLR-403, TC-480, SR-249, SR-211 (rationale) and LLR-244 (one
clause), as the plan's section 7 writes them. One deviation: TC-195's method
keeps its other sentences, and only its JOIN sentence, "--check" and "-000"
change. LLR-042 and TC-080 wait for slice 5.

## 5. Acts owed to sitting A

**Amended accepted rows** (text-only, `Accepted` kept, drifted), by id and
cell; "routed" marks the `constrains` cell, a routed traced change:

| Row | Accepted cells amended | Routed traced change |
|---|---|---|
| LLR-010 | `detail` | `constrains` IF-014 |
| LLR-012 | `detail` | `constrains` IF-030 |
| LLR-013 | `detail` | `constrains` IF-029 |
| LLR-017 | none | `constrains` IF-032 |
| LLR-022 | none | `constrains` IF-036 |
| LLR-024 | none | `constrains` IF-017 |
| LLR-025 | none | `constrains` IF-019 |
| LLR-026 | `detail`, `rationale` | `constrains` IF-041 |
| LLR-033 | none | `constrains` IF-018 |
| LLR-039 | `detail` | `constrains` IF-012, IF-149 |
| LLR-047 | `detail`, `rationale` | `constrains` IF-048, IF-157, IF-158 |
| LLR-118 | `detail` | `constrains` IF-074 |
| LLR-124 | `detail` | `constrains` IF-164 |
| LLR-130 | `detail` | `constrains` IF-011 |
| LLR-171 | `detail` | `constrains` IF-039 |
| LLR-198 | `detail`, `rationale` | `constrains` IF-088 |
| LLR-199 | `detail`, `rationale` | `constrains` IF-139, IF-140 |
| LLR-244 | `detail` | none |
| LLR-258 | `detail` | `constrains` IF-227 |
| LLR-279 | `detail` | `constrains` IF-035 |
| LLR-281 | `detail`, `rationale` | `constrains` IF-254 |
| LLR-320 | `detail` | `constrains` IF-292, IF-293 |
| LLR-403 | `title`, `detail`, `rationale` | none |
| SR-211 | `rationale` | none |
| SR-249 | `title`, `requirement`, `rationale`, `acceptance_criteria` | none |
| TC-195 | `method` | none (its `evidence` regenerated, traced and not routed) |
| TC-480 | `method`, `expected` | none (`evidence` regenerated) |

27 rows: 23 design rows, 2 requirements, 2 test cases; 21 routed `constrains`
changes, 5 of them on rows whose text did not change (LLR-017, LLR-022,
LLR-024, LLR-025, LLR-033). TC-466's `evidence` gained a test (traced, not
routed): no act owed.

**New `Drafted` rows owed a first acceptance:** LLR-417, LLR-418, LLR-419,
LLR-420, LLR-423; TC-527, TC-528, TC-529, TC-530, TC-533. Ten rows.

**Held out of sitting A (D11):** LLR-421, LLR-422, TC-531 and TC-532 stay
`Drafted` until slice 5, when their warn-first sentence becomes the strict one.

Sitting A's total: 37 rows. Ids: LLR-417 to LLR-423 and TC-527 to TC-533,
watermark raised to LLR 423 and TC 533; the population used one LLR and one
TC id, so LLR-424 up (56) and TC-534 up (26) remain.

## 6. For the coordinator, before slice 2

1. **Large code-named rows.** Rule 1 on every touched row rewrote 18 rows'
   text here; five were large (LLR-026, LLR-039, LLR-047, LLR-118, LLR-198).
   Where the obvious row is that large and states the interface's behaviour
   in one clause among many (LLR-300 for IF-277), this slice wrote a new
   focused `Drafted` row instead (LLR-423). Confirm that pattern for slices
   2 to 4, or ask for the large row's rewrite.
2. **Clauses with file-level evidence only.** Several kept clauses map to a
   test file rather than a named test (LLR-025's drift detection, LLR-026's
   last-message capture, LLR-124, LLR-258). Sitting
   A shows whether the judge accepts file-level evidence; if it returns them,
   slices 2 to 4 cut such clauses or add named tests.
3. **No companion cells yet.** None of slice 1's rows has an out-of-domain
   behaviour any existing test drives, so none carries `dimensions`. Writing
   them means adding an out-of-domain test per row; say whether slices 2 to 4
   should, or leave the counts as the evidence for the later strictness call.
4. **LLR-300's overlap with LLR-423** (the session variable) is left for that
   row's next amendment.
