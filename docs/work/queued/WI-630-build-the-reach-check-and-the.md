+++
id = "WI-630"
title = "Build the reach check, the mediates cell and the need-frame gap advisory (SR-188, SR-195)"
workstream = "scripts"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-188", "SR-195"]
needs = ["WI-628", "WI-629"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

The frame entity's `mediates` cell, the need-by-need reach check for assumptions, and the advisory for a need met in operation with no operation crossing. Design rows: LLR-214, LLR-226, LLR-227. Test cases: TC-214, TC-223. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
