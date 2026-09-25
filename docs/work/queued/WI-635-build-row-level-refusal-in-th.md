+++
id = "WI-635"
title = "Build row-level refusal in the snapshot refresh (SR-207)"
workstream = "scripts"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-207"]
needs = ["WI-642"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

An approval act refuses while any row outside it has drifted approved text; `--reattests` names re-attested rows, and the act's record names them. The two snapshot tests pinning the old any-flip behaviour change with it. Every caller that builds `--approves` (the adjudication brief, intake's mint prose) is checked against the new meaning. Design rows: LLR-245. Test cases: TC-240. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
