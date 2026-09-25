+++
id = "WI-628"
title = "Build the stakeholder list and the needs' source pointer (SR-189, SR-190)"
workstream = "scripts"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-189", "SR-190"]
needs = ["WI-642"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

The `[stakeholder.STK-##]` tier in the needs file, each need's `stakeholder_refs`, the `source` pointer column exempt from the provenance rule, their findings and the STK id space. The rows themselves are written in the C1 sitting commit (WI-643). Design rows: LLR-215, LLR-216, LLR-217. Test cases: TC-215, TC-216. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
