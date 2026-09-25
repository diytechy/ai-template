+++
id = "WI-632"
title = "Build observation records, the evidence level, the falsification worklist and accepted-risk triggers (SR-199..SR-202)"
workstream = "scripts"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-199", "SR-200", "SR-201", "SR-202"]
needs = ["WI-631", "WI-635"]
buildtier = "strong"
safety_class = "ordinary"
priority = 4
+++

## Context

`kitlib/observation.py` and `record_observation.py`, the evidence level derived from current results under the cumulative tier contract, the falsification worklist, and the accepted risk anchored to its approval act (LLR-239 reads the act record WI-635 adds). Design rows: LLR-234, LLR-235, LLR-236, LLR-237, LLR-238, LLR-239. Test cases: TC-229, TC-230, TC-231, TC-232, TC-233, TC-234. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
