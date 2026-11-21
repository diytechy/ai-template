## 2026-11-21 — WI-1014: the README's registry map and the dashboard's lifecycle panel show today's tiers and stage ladder

Deferred open items: none — the one call this row leaves to the operator, the
spine's design depth behind the map's `LLR-### design` label, is the subject
the operator is weighing, not an open item this row raises.

Built on the maintenance branch `maint/wi-1014`, cut from `refactor_again` at
`0d67302bd`, with the commit hooks on.

- **Plan** (`7dbc2d1de`, `docs/plans/WI-1014/plan.md`): the S5 answer. Panel
  1 stops holding a list: its rungs come from `kitlib.ladder.STAGE_ORDER`,
  each rung's tiers from a new `spine_rules.RUNG_TIERS`, and the counts from
  `spine_rules.load_spine`, the rows the derivation reads. One new seam,
  `traj_parse -> spine_rules`, declared as IF-325.
- **The map, first** (`924175359`): `README.md`'s "one map" drops interfaces'
  retired `req_refs` edge and draws every registry and every cross-registry
  link from the current templates, labelled with today's keys: the
  stakeholder, assumption and surrogate tiers (`stakeholder_refs`, `party`,
  `da_refs`, `assumption_refs`, `bridged_by`, `effect_at`, `realized_by`,
  `emulates`), the hats (`hat_refs`, `obstacle_hats`), open items (`needs`),
  `verifies` to IF, `verified_by`, and `Refs` to SR and LLR. A sentence names
  what is not drawn; the intro counts four kinds; the interfaces row loses
  `req_refs` and its stale owner sentence. The `LLR-### design` label is
  unchanged. Recorded as `docs/decisions/maint-wi-1014.toml#D-001`.
- **Rows and tests, red** (`c350f9ba4`): LLR-393 (the table, CMP-006),
  LLR-394 (the panel, CMP-009), TC-455, TC-456 and IF-325, all Drafted under
  SR-168. TC-051's process-tab tests now assert the per-rung rows. Eight
  tests failed at this commit.
- **The panel** (`6c6aeb83a`): `RUNG_TIERS` (SN and STK at Needs; B, DA and
  SUR at Boundary; SR, CMP, LLR, TC; the evidence record at Impl; none at
  Release), held to `spine_stage` by TC-455's driven test rather than run
  from, because the need-coverage arm is not a flat ladder;
  `traj_parse.rung_tiers`; `traj_panels._lifecycle_rows`, extracted from
  `process_panel` when the complexity ratchet held it at 15 (no baseline
  edit), and `process_panel` without its unused `stats` argument. RESYNC
  entry: nothing forced, regenerate `PROJECT_STATE.html`.
- **Golden files:** `tests/golden/dashboard-no-assumptions.html` renders a
  repository with no `docs/stage`, so it has no Process tab and stays
  byte-identical; its test passed. `PROJECT_STATE.html` is regenerated.
- **Tests** on `6c6aeb83a`, 39 modules: the 33 a grep finds importing
  `spine_rules`, `traj_parse`, `traj_panels` or `gen_trajectory`, plus
  `test_derive_stage` (spine-linked to `spine_rules`), `test_traj_status` and
  `test_trajectory_staged` (they run `gen_trajectory`), `test_gen_arch_map`
  (the contracts reference), `test_dogfood_sync` and
  `test_complexity_ratchet`:
  test_acceptance_level, test_assumption_gate, test_baseline_snapshot,
  test_bootstrap, test_check_iterate, test_evidence_partition,
  test_frame_context, test_gen_open_items_render, test_gen_trajectory,
  test_gen_trajectory_splice, test_import_layers, test_kitlib_ladder,
  test_kitlib_stage, test_module_size_ratchet, test_open_item_readiness,
  test_retire_dashboard, test_rule_sync, test_rule_sync_driven,
  test_selection_at_or_above, test_smoke_tier, test_spine_rules,
  test_stage_ladder, test_stakeholders, test_test_evidence,
  test_trace_briefs, test_traj_graph, test_traj_lanes, test_traj_panels,
  test_traj_parse, test_traj_render, test_traj_render_sweeps,
  test_traj_views, test_trajectory, test_derive_stage, test_traj_status,
  test_trajectory_staged, test_gen_arch_map, test_dogfood_sync,
  test_complexity_ratchet:
  <!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n auto tests/<each module above>.py" rev=6c6aeb83a -->
  `1213 passed, 1 skipped in 300.99s`.
- **Deviations from the plan:** the panel's rows moved into
  `_lifecycle_rows` (the complexity ratchet), and LLR-394's `code_symbol`
  names it. No byte-budgeted file changed.
- **Review:** OpenAI Sol (low) reviewed the whole branch alone; Gemini
  Argon was not run (it timed out at 900 seconds on every run in this
  sitting and is skipped, per the operator's 2026-11-21 ruling). Two MINOR
  findings, both fixed in `387df72ce`: the README's interfaces row now
  names `coincident` beside `bridged_by` for a boundary row and links their
  rules to the interfaces template and `INTERFACES.template.md` (PROCESS.md
  §8 states neither); TC-455's `expected` cites LLR-393's detail instead
  of restating it, and its `method` keeps the procedure. The tests reading
  those files (the trace family, `test_evidence_join`, the doc, figure,
  rule-sync, dogfood and watermark checks, `test_spine_rules`), on the
  fix's tree:
  <!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n auto tests/test_trace.py tests/test_trace_rules.py tests/test_trace_coherence.py tests/test_trace_interfaces.py tests/test_trace_golden.py tests/test_trace_briefs.py tests/test_trace_hats.py tests/test_trace_hats_driven.py tests/test_evidence_join.py tests/test_check_docs.py tests/test_check_doc_refs.py tests/test_check_figures.py tests/test_check_figures_rules.py tests/test_rule_sync.py tests/test_status_vocabulary_contract.py tests/test_dogfood_sync.py tests/test_spine_rules.py tests/test_check_test_first.py tests/test_plan_coverage.py tests/test_cell_classes.py tests/test_id_watermark.py" rev=387df72ce -->
  `671 passed, 2 skipped, 18 warnings in 187.83s`.
  Also fixed: the interfaces row's backing claim, which named an SR and a
  contract test, now follows §8 (`c37cef6bc`). Review round 2 (Sol, low,
  narrow over `eab7ae240..2be996ed0`): APPROVE, no findings.
- **Out of scope, noticed:** LLR-051's detail still names "(2) the
  resume-loop panel", which the station cycle replaced earlier.
