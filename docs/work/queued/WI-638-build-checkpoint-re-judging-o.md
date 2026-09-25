+++
id = "WI-638"
title = "Build checkpoint re-judging of observation tests at merge and release (SR-215)"
workstream = "unattended"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-215"]
needs = ["WI-632", "WI-612"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

`rejudge.py` decides from a digest of each observation test case's declared inputs; intake files one re-judge item per due case at a work-item merge, and a release subcommand plus a required release-checklist item cover release preparation. Filing runs through the mint path, so its staging must stage and restore only what it wrote first. Design rows: LLR-254, LLR-255. Test cases: TC-247, TC-248. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
