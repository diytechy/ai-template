+++
id = "WI-629"
title = "Build the assumptions registry, surrogates, requirement classification and form (SR-191..SR-194, SR-196)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-191", "SR-192", "SR-193", "SR-194", "SR-196"]
needs = ["WI-642"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

- `docs/requirements/assumptions.toml` (assumption and surrogate tiers, keyed
  `DA-###` / `SUR-###`) with its shipped template and scaffold mapping; the
  requirement tier's `da_refs`, `coincident` and `form` cells; carrier maps
  both ways; DA and SUR in the id watermark, the snapshot's compared tiers and
  the approval act.
- `assumption_rules.py` behind one entry point (IF-190): frame-class row
  failures, integrity-floor surrogate and form failures, and the
  classification, form, uncited and falsifier advisories. The tier is silent
  with no declared crossing; `sr_form_findings(srs)` is the one-argument pure
  rule LLR-224 names, and the entry point asks no form until a real
  assumption row exists.
- A registry missing from the signed record is always reported, except the
  assumptions registry (`baseline_snapshot.FIRST_COPY_AT_APPROVAL`) while no
  live row of it claims approval.
- Each new cell's traced-or-approved class in the amendment classifier; TC-222
  moved to the slow module `tests/test_cell_classes.py`.
- Amended, status left Approved, for the joint adjudication: TC-222 `tier`
  Smoke -> Full (arbitration ruling 1). Traced pointer moved: TC-222
  `evidence`.
- Ships empty here: this repository's trace output is unchanged.

## Context

`docs/requirements/assumptions.toml` with its assumption and surrogate tiers, template, scaffold mapping, DA and SUR id spaces and acceptance-record tiers; the requirement's `da_refs`, `coincident` and `form` cells; the classification, form, uncited and falsifier findings; `assumption_rules.py`; and every new cell's traced-or-approved class (LLR-225). Ships empty in this repository: assumption rows are C2 content, written after this lands. Design rows: LLR-218, LLR-219, LLR-220, LLR-221, LLR-222, LLR-223, LLR-224, LLR-225, LLR-228. Test cases: TC-217, TC-218, TC-219, TC-220, TC-221, TC-222, TC-224. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
- TC-240's snapshot cases (`tests/test_baseline_snapshot.py`, parametrized from `baseline_snapshot.SNAPSHOT_TIERS` at collection, WI-635) run for `DA-ID` and `SUR-ID` once LLR-220 adds those tiers, and the run is recorded: until then TC-240's assumption and surrogate clause has no evidence.
