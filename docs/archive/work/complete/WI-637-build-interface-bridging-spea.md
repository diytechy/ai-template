+++
id = "WI-637"
title = "Build interface bridging, a perspective's speaks_for and obstacle perspectives (SR-211, SR-213, SR-214)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-211", "SR-213", "SR-214"]
needs = ["WI-628", "WI-629"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

- The interface tier's `bridged_by` (traced) and the shared `coincident`
  cell; `assumption_rules.interface_bridge_findings` over boundary interfaces
  only: an undeclared assumption fails the interface class, a boundary row
  with neither cell is an advisory (43 here, the worklist SR-211 describes;
  its missing "until adopted" clause is OI-94).
- `assumption_rules.obstacle_hat_findings`: each `ObstacleHats` entry
  resolved against the roster, every one failing with no roster.
- `hats.py`'s optional `speaks_for`; `load_hat_names` returns
  `(names, speaks_for)` and `hat_findings` resolves it against the declared
  stakeholders.
- IF-208 (Drafted) carries both rules. The report counts hat findings
  whenever any exists, so a no-roster failure reaches the summary; checker-level
  regressions drive `trace.analyze` to `exit_code` and the report, each shown
  to red when its wiring is removed.
- No approved-row cell changed.

## Context

The interface's `bridged_by` and `coincident` cells and their findings, the roster's optional `speaks_for`, and an assumption's `obstacle_hats`. Design rows: LLR-250, LLR-251, LLR-252. Test cases: TC-244, TC-245, TC-246. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
