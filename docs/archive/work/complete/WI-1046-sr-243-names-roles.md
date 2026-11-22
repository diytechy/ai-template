+++
id = "WI-1046"
title = "SR-243 names the author, critic and REVIEW-A roles, not the models that fill them"
workstream = "docs"
sr_refs = ["SR-243"]
needs = ["WI-1044"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1046`, cut from `refactor_again` at
`660805e62`, with the commit hooks on. The specref (WI-1037's archived spec)
is cleared at close, as a terminal row's is.

- `e8969307a`: SR-243's two cells and the regenerated views.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**SR-243** (Accepted; text only). Its requirement now ends "and provide the
sole launch route for author, critic and REVIEW-A calls" (was "the sole Sol
or Terra launch route"), and its acceptance criteria say published
coordinator guidance "names the coordinator-call route as the only launch
path for author, critic and REVIEW-A calls" (was "the only Sol or Terra
launch path"). Both take TC-385's phrase after WI-1044 ("the only launch
path for author, critic and REVIEW-A calls"). Its status and every other
cell are unchanged, `hat_refs` included: the hook's advisory that the row's
substance moved while its hats stayed put is answered by the spec ("No other
cell changes"), since naming roles for models moves no lens. The regenerated
views are `docs/ratify/CURRENT.md` (SR-243's own two cells now listed
beside TC-385's), `PROJECT_STATE.html`, `docs/open-items.html` and
`docs/stage` (its fingerprint and as-of line only).

**Pins:** none. No test names SR-243 or quotes either old phrase; the
grep over `tests/` for "Sol or Terra", "sole Sol", "launch route" and
"launch path" finds no pin on the requirement registry's text.

**Tests.**

- The modules reading the live requirement registry, TC-385's chain or the
  generated views, and the whole-tree tests: `test_prompts`,
  `test_spine_rules`, `test_cell_classes`, `test_rule_sync`,
  `test_rule_sync_driven`, `test_evidence_join`, `test_baseline_snapshot`,
  `test_check_test_first`, `test_trace`, `test_trace_rules`,
  `test_trace_briefs`, `test_trace_hats`, `test_trace_golden`,
  `test_spine_carrier`, `test_adjudicate_brief`, `test_text_then_act`,
  `test_hats`, `test_check_harness`, `test_csv_header`,
  `test_dogfood_widening`, `test_external_frame`, `test_frame_system`,
  `test_kitlib_stage`, `test_plan_pass`, `test_ruled_open_item_cover`,
  `test_seam_resolution`, `test_trajectory_forward_only`,
  `test_trajectory_specs`, `test_generated_freshness_wiring`,
  `test_acceptance_record`, `test_ac_advisory`, `test_parent_first`,
  `test_registry_checks`, `test_dogfood_sync`, `test_import_layers`,
  `test_module_size_ratchet`:
  `1150 passed, 3 skipped, 18 warnings in 984.28s (0:16:24)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto <the 36 modules listed>" rev="e8969307a (its tree before the commit)" -->
- The commit checks, `run_menu.py smoke`:
  `3714 passed, 3 skipped, 18 warnings in 288.04s (0:04:48)`. Its budget
  line reads CPU 866.3 s against 540, a WARN only, not charged to the lane.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="e8969307a (its tree before the commit)" -->
- `trace.py --root . --strict`: `orphans=0 integrity=0`.
  `check_trajectory.py --strict`: clean. `scripts/check_resync.py`: "OK, no
  shipped path changed". The build commit passed the hook (29 steps, all
  PASS).

**Byte deltas** (none budgeted or watched):
`docs/requirements/system-requirements.toml` 319,846 -> 319,896 (+50, +25
in each cell).

**Acts owed:** SR-243's drift, for automated adjudication. Its requirement
and acceptance criteria changed under an unchanged `Accepted` status; the
hook reports the amendment, and `docs/ratify/CURRENT.md` lists the SR-243
chain under "Waiting for automated adjudication", now with SR-243's own
cells beside TC-385's. This branch takes no act.

## Context

Filed on trunk on 2026-11-21 from WI-1044's build. SR-243 (Accepted) still
names models where it means roles: its requirement says the coordinator call
capability shall "provide the sole Sol or Terra launch route", and its
acceptance criteria say published guidance "names the coordinator-call route
as the only Sol or Terra launch path". The operator's rule behind WI-1037:
which model fills a role is a setting (`codex_call.py`'s role routes over
the enabled roster).

WI-1044 brings TC-385, which verifies SR-243, to the skill's own phrase,
"author, critic and REVIEW-A". It left SR-243 alone, since amending an
accepted SR was outside its critiqued scope. This row takes the SR to the
same words. The amended text drifts for automated adjudication.

## Done-when

- [x] SR-243's requirement and acceptance criteria name the coordinator-call
      route as the only launch route for the author, critic and REVIEW-A
      calls, in TC-385's words after WI-1044 (text only; its status
      unchanged). No other cell changes.
- [x] The Deliverable lists SR-243's drift as the act owed for automated
      adjudication.
