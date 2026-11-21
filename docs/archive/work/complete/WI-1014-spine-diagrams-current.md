+++
id = "WI-1014"
title = "The spine diagrams show today's tiers and stage ladder: the README's registry map and the dashboard's lifecycle panel"
workstream = "docs"
sr_refs = ["SR-168"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Deliverable

Both spine diagrams now draw today's tiers and stage ladder: the README's
registry map from the current templates, and the dashboard's Process-tab
panel 1 from the ladder and the stage derivation's own table. Built on the
maintenance branch `maint/wi-1014`, cut from `refactor_again` at `0d67302bd`.
Review: pending (the coordinator).

**Against the Done-when:**

1. **The map.** `README.md`, "The registries & trace artifacts — one map":
   every registry under `project-trajectory/registries/` and the work-item
   folder is a node, and every cell naming another registry's row is an
   edge labelled with its key as the template spells it. Interfaces' retired
   `req_refs` edge is gone (and so is the interfaces table row's `req_refs`
   and its stale "owner is a design or requirement id" sentence). Added:
   STK, DA and SUR in a subgraph of their own (SN `stakeholder_refs`, STK
   `party` to EXT, SR `da_refs`, TC `assumption_refs`, IF `bridged_by`, DA
   `effect_at` to B, `realized_by` to SUR, SUR `emulates` to EXT), the hats
   (SR and LLR `hat_refs`, DA `obstacle_hats`), open items (WI `needs`),
   TC `verifies` to IF (and SR to TC in the spine), IF `verified_by`, and PB
   and ASSET `Refs` to both SR and LLR. A sentence under the map names what is not drawn
   (same-registry links, path cells, a case's observation cells) and the
   arrow conventions; the intro counts four kinds; a table section covers
   the tiers read from their first acceptance; an open-items row joins the
   optional table. The scope reading is recorded as
   `docs/decisions/maint-wi-1014.toml#D-001`.
2. **The panel.** One row per rung of `kitlib.ladder.STAGE_ORDER`,
   `DevStg-Release` included, after the Vision row. Each row names the tiers
   `spine_rules.RUNG_TIERS` gives its rung (SN and STK at Needs; B, DA and
   SUR at Boundary; SR, CMP, LLR, TC; the evidence record at Impl; none at
   Release, which shows its `STAGE_DESC`) and counts the rows
   `spine_rules.load_spine` returns for each, so the counts stay live. The
   row at the recorded stage is `now`. The S5 answer, in
   `docs/plans/WI-1014/plan.md`: the panel reads the ladder and the table
   rather than a hand list, and so gains one input, `traj_parse ->
   spine_rules`, declared as IF-325 with its `Contract IF-325:` block.
   `RUNG_TIERS` is a table beside `spine_stage`, not one it runs from (its
   need-coverage arm is not a flat ladder); TC-455 holds the two together by
   driving `spine_stage` tier by tier and by matching the table's keywords
   to the function's parameters.
3. **Golden files and tests.** TC-051's two process-tab tests assert the
   per-rung rows; TC-455 (2 tests) and TC-456 (3 tests) are new.
   `PROJECT_STATE.html` is regenerated. The stored golden page
   (`tests/golden/dashboard-no-assumptions.html`) renders a repository with
   no `docs/stage`, so it has no Process tab and stays byte-identical; its
   test passed in the run below.
4. **The map's `LLR-### design` label** is unchanged: the operator has not
   ruled on the spine's design depth.

**Commits:** `7dbc2d1de` the plan; `924175359` the README map; `c350f9ba4`
LLR-393, LLR-394, TC-455, TC-456 and IF-325 (all Drafted, under SR-168) with
the tests, red at that commit (8 failed); `6c6aeb83a` the code
(`spine_rules.RUNG_TIERS`, `traj_parse.rung_tiers`,
`traj_panels._lifecycle_rows`, `process_panel` without its unused `stats`
argument), the RESYNC entry and the decisions record.

**Tests.** Every module importing `spine_rules`, `traj_parse`,
`traj_panels` or `gen_trajectory`, with `test_import_layers`,
`test_module_size_ratchet`, `test_dogfood_sync` and `test_complexity_ratchet`
(39 modules), on `6c6aeb83a`:
<!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n auto tests/<each of the 39 modules the log entry lists>.py" rev=6c6aeb83a -->
`1213 passed, 1 skipped in 300.99s`.

**Amendments for the operator:** none. LLR-051 and TC-051 (Accepted) already
say the panel is drawn from the live registries and `docs/stage` with
per-tier counts; their text is unchanged. The five new rows await the
operator's acceptance.

**Left:** nothing in the Done-when. Not done, out of scope: LLR-051's detail
still names "(2) the resume-loop panel", which the station cycle replaced
before this row.

## Context

Filed by hand on 2026-11-21 at the operator's direction, after a check of
the two diagrams that draw the spine (HANDOFF §12.6, 2026-11-20).

**The README's registry map** (`README.md`, "The registries & trace
artifacts — one map"):

- it draws `IF -- req_refs --> SR`, a cell interfaces retired
  (`migrate_carrier.IF_RETIRED`);
- it has no assumption tier: `DA-###` and `SUR-###` in
  `assumptions.toml`, reached by SR `da_refs`, TC `assumption_refs` and IF
  `bridged_by`, with DA `effect_at` landing on a `B-##` crossing, DA
  `realized_by` naming a surrogate and SUR `emulates` naming an `EXT-###`;
- it has no stakeholders (`STK-###`, reached by SN `stakeholder_refs`,
  `party` naming an `EXT-###`), hats (SR `hat_refs`, DA `obstacle_hats`)
  or open items.

**The dashboard's Process tab, panel 1** ("Artifact lifecycle × the stage
ladder", `rendering/traj_panels.py`):

- it has no `DevStg-Release` row, and its comment says nothing derives that
  rung; `derive_stage` derives it from the harness verdict
  (`kitlib.stage.evidence_passed`, WI-500);
- it places only SR at `DevStg-Boundary` and only SN at `DevStg-Needs`,
  while `spine_rules` holds Boundary on the frame's crossings and on an
  active assumption or surrogate tier with a Drafted row, and Needs on an
  active stakeholder tier too.

The operator is weighing how much design the spine should carry (an LLR
pins `Module` and `CodeSymbol`). The map's "LLR design" label waits on that;
everything above does not.

**Two deliverables, kept together on purpose.** The README map and panel 1
could each land alone; they are one row because both answer the same
question, which tiers and links today's spine has, and one review reads
them against the same templates. The map lands first (prose only), then the
panel, its golden files and tests.

## Done-when

- [x] The README map draws every registry and link above from the current
      templates, and no retired cell.
- [x] Panel 1 shows each rung the derivation can return, `DevStg-Release`
      included, with the tiers that hold it, and its counts stay live.
- [x] The dashboard's golden files and tests follow the panel.
- [x] The map's LLR label is left as it is unless the operator has ruled on
      the spine's design depth by the time this row is built.

## Critique dispositions

Round 1 (OpenAI Sol, low, 2026-11-21; Gemini Argon timed out, so Sol
reviewed alone; `docs/reviews/2026-11-21-scope-critiques/WI-1014.md`):
CHANGES-REQUESTED, two findings.

- **S4 (MAJOR), `planmode` missing: adopted as `planmode = "single"`.** Panel
  1 promises a row for every rung the derivation can return and its tiers,
  with live counts, so a short plan names where the rungs and each rung's
  tiers are read from before the renderer changes
  (`docs/plans/WI-1014/plan.md`). That plan answers the S5 question: whether
  the panel reads the ladder and `spine_rules` rather than a hand list, and
  so gains an input.
- **S1 (MINOR), two landable deliverables with no order: adopted.** Context
  now keeps the map and the panel together on purpose and lands the map
  first.
