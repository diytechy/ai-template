+++
id = "WI-633"
title = "Build the assumption approval brief, the stage's tier reading and the per-need view (SR-203, SR-204, SR-218)"
workstream = "scripts"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-203", "SR-204", "SR-218"]
needs = ["WI-628", "WI-632"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

The approval brief's assumption section and `assumptions` scope; the stage reading the assumption, surrogate and stakeholder tiers from each tier's first approval; and the dashboard's per-need assumption view. Design rows: LLR-240, LLR-241, LLR-258. Test cases: TC-235, TC-236, TC-251. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
