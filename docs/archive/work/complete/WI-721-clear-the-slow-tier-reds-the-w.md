+++
id = "WI-721"
title = "Clear the slow-tier reds the wave-5 close found: retire.py's live-id reader misses non-TOML registries, the skills-index freshness test trips the description floor, and measure the full suite's wall time"
workstream = "process"
specref = ""
sr_refs = ["SR-226"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

The four real slow-tier failures are fixed, and the full unfiltered suite
is green.

- **`retire.live_ids`** now reads every spine tier through `spine_carrier`,
  the one registry reader `trace.py` uses (IF-102, reused), so every carrier
  form counts as live. That covers TOML, and the legacy CSV and Markdown.
  - `tests/test_retire.py::test_legacy_registry_rows_are_live_and_only_a_spent_id_is_reported`
    shows no advisory for a live legacy-carrier row, and still names a spent
    id.
  - The three trace goldens pass without the false advisory, and no golden
    was regenerated.
  - One behaviour change: a registry that exists but does not parse now
    raises, as every other spine reader does, instead of reading as zero
    rows.
- **LLR-286 `detail`** is amended in place (status left Approved, for the
  next spine-acts batch). It now reads "a live row of its tier's registry,
  in whichever carrier form the kit's registry reader resolves", where it
  said "TOML registry". TC-299's `evidence` lists the new test, and the
  IF-102 docstring's caller list matches its row.
- **`test_skills_index_step_reds_when_a_skill_is_added`** plants a
  132-character description, above the 100-character floor, so it pins
  STALE again. The floor is unchanged.
- **The full unfiltered suite** passes. It ran on trunk e86cae4f with this
  lane squashed in and the views regenerated, as a temporary detached
  commit in a throwaway worktree, while WI-723's builder and reviewers
  shared the box. The command was `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt
  python -m pytest -q -n auto -p no:cacheprovider --durations=30`:

```
============================ slowest 30 durations =============================
1160.63s call     tests/test_traj_graph.py::test_meta_knowledge_and_when_wires_avoid_unrelated_boxes
392.72s call     tests/test_traj_graph.py::test_fallback_dag_and_sw_graph_wires_avoid_unrelated_boxes
291.05s call     tests/test_prereq_toolchain.py::test_a_gate_closed_run_announces_itself_at_both_ends
99.72s call     tests/test_traj_graph.py::test_deep_chain_renders_without_recursionerror
93.88s call     tests/test_dispatch.py::test_the_dispatcher_mints_the_consolidation_row_for_an_overlapping_queue
50.72s call     tests/test_agent_loop_review.py::test_winstay_biases_the_next_review_draw_over_the_weighted_baseline
49.17s call     tests/test_traj_graph.py::test_t8_no_wire_passes_through_an_unrelated_node_box
48.41s call     tests/test_dispatch.py::test_drive_end_to_end_claims_builds_merges_and_drains
47.82s call     tests/test_dispatch.py::test_a_red_handback_is_reverted_to_a_bar_inert_artefact_and_merges
45.94s call     tests/test_old_kit_resync.py::test_node_adopter_upgrade_preserves_populated_owner_content
45.93s call     tests/test_traj_panels.py::test_meta_spine_renders_the_knowledge_graph_at_real_scale
44.58s call     tests/test_conftest_isolation.py::test_a_module_importing_kitlib_collects_on_its_own
43.12s call     tests/test_check_privacy.py::test_meta_repo_tree_passes_the_secrets_floor
40.54s call     tests/test_dispatch.py::test_a_needs_human_worker_hands_back_and_the_run_keeps_going
40.41s call     tests/test_check_harness.py::test_smoke_tier_runs_only_smoke_and_skips_coverage_gate
38.75s call     tests/test_check_harness.py::test_the_default_stage_comes_from_the_derived_stage_file
38.67s call     tests/test_dispatch.py::test_drive_stops_on_a_red_refresh_bar
38.47s call     tests/test_dispatch.py::test_empty_frontier_rung_one_mints_gap_rows_then_drives_them
38.03s call     tests/test_integrate_station.py::test_claim_build_and_integrate_end_to_end
36.19s call     tests/test_check_harness.py::test_minimal_project_is_green
34.51s call     tests/test_integrate_unload.py::test_the_queue_exits_nonzero_when_a_merged_branch_stays_held
34.00s call     tests/test_check_harness.py::test_failing_test_fails_the_harness
33.98s call     tests/test_integrate_unload.py::test_the_queue_gcs_a_clean_worker_worktree_end_to_end
33.04s call     tests/test_dispatch.py::test_residue_settled_at_barrier_open_is_counted_in_the_drained_banner
32.99s call     tests/test_agent_loop_review.py::test_reviewer_outage_parks_review_owed_then_resume_draws_the_round
32.85s call     tests/test_verdict_record.py::test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel
32.06s call     tests/test_check_harness.py::test_unmarked_test_runs_in_full_tier
30.78s call     tests/test_agent_loop_review.py::test_review_unparseable_verdict_cools_and_reroutes_same_phase
30.29s call     tests/test_agent_loop_review.py::test_escalation_tiers_up_after_swap
29.26s call     tests/test_bootstrap.py::test_domain_skills_require_matching_explicit_opt_in
4816 passed, 15 skipped, 18 warnings in 4998.50s (1:23:18)
```

- **The wall time:** 83 minutes under load, down from the 111 minutes the
  close measured, and against about 10 minutes recorded earlier.
  - One test is most of the critical path:
    `test_meta_knowledge_and_when_wires_avoid_unrelated_boxes` takes 1160 s,
    and its fallback-graph sibling 393 s.
  - Both route wires over graphs built from this repository's live
    registries ("same spine, same scale"). The router has not changed since
    2026-09-06, so the cost grows with the spine rather than with a code
    change.
  - Filed as its own row (see the log).
- **Review:** Sonnet reviewed the lane in two rounds.
  - [Round 1](../../../reviews/2026-09-28-wave6/sonnet-wi721-r1.md): SOUND
    at 3496344e, with one major (LLR-286's "TOML").
  - [Round 2](../../../reviews/2026-09-28-wave6/sonnet-wi721-r2.md): SOUND
    at d7c43118.

## Context

The wave-5 close ran the full unfiltered suite once, at bc3310f3
(`python -m pytest -q -n auto`): **5 failed, 4810 passed, 15 skipped in
6683.90 s (1:51:23)**. One failure was an untracked handoff not yet linked,
cleared at the close. The other four are real, and every lane missed them
because each ran only its named slow modules:

- **`tests/test_trace_golden.py`, all three goldens (clean, offspine,
  orphan).**
  - The cause: `retire.live_ids` parses only the four TOML registries at
    fixed paths (`retire.TIERS`). The golden scaffolds keep their spine in
    the legacy CSV and Markdown forms, which `trace.py` still reads through
    the kit's registry reader.
  - The effect: every live row reads as a spent id with no retirement
    record, for example "4 spent spine id(s) have no retirement record ...:
    SN-001, SR-001, LLR-001, TC-001" on a spine where all four are live.
  - The advisory is warn-only, but it is false. It would reach any adopter
    whose registries `live_ids` cannot parse.
  - The fix reads live ids through the one registry reader that `trace.py`
    uses (0->A->B), not a second parser. The goldens must not be
    re-stamped over a false advisory.
- **`tests/test_generated_freshness_wiring.py::test_skills_index_step_reds_when_a_skill_is_added`.**
  - The test plants a skill with a 32-character description and expects
    `gen_skills_index --check` to report STALE.
  - The generator now reports SHORT first, against its 100-character
    description floor.
  - The fix is the test fixture's description, so the test again pins
    STALE. The floor stays.
- **The wall time.** The same suite was recorded at about 10 minutes on a
  quiet box and 3–4× that under load. This run took 111 minutes, with only
  light read-only commands beside it. The cause is unmeasured.

## Done-when

- `retire.live_ids` (or its replacement) reads every registry form the
  kit's registry reader supports. A test on a CSV-registry scaffold shows
  no advisory for a live row, and still names a spent id with no record.
- The three trace goldens pass without the retirement advisory, and no
  golden is regenerated to absorb it.
- `test_skills_index_step_reds_when_a_skill_is_added` pins STALE again with
  a fixture description above the floor. The floor is unchanged.
- The full unfiltered suite's slowest tests are measured
  (`--durations=30`) and recorded in the log fragment with the total wall
  time. A regression large enough to explain the jump is fixed or filed.
- The full unfiltered suite passes, and its real output is pasted in the
  log fragment.
