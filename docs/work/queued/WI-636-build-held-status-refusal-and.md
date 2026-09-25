+++
id = "WI-636"
title = "Build held off-spine status refusal, the loop provenance trailer and its history check (SR-208..SR-210)"
workstream = "unattended"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-208", "SR-209", "SR-210"]
needs = ["WI-642"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

`kitlib/provenance.py` and `kitlib/authority.py`; the loop marker set in-process; the trailer on every loop writer; the held-status refusal at every loop writer and at the merge slot; and the history advisory for a loop commit that changed a held status. Hooks are opt-in, so the merge-slot re-check is the enforcement in a checkout without `core.hooksPath`. Design rows: LLR-246, LLR-247, LLR-248, LLR-249. Test cases: TC-241, TC-242, TC-243. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
