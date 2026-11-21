+++
id = "WI-1014"
title = "The spine diagrams show today's tiers and stage ladder: the README's registry map and the dashboard's lifecycle panel"
workstream = "docs"
sr_refs = ["SR-168"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

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

- [ ] The README map draws every registry and link above from the current
      templates, and no retired cell.
- [ ] Panel 1 shows each rung the derivation can return, `DevStg-Release`
      included, with the tiers that hold it, and its counts stay live.
- [ ] The dashboard's golden files and tests follow the panel.
- [ ] The map's LLR label is left as it is unless the operator has ruled on
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
