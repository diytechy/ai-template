+++
id = "WI-634"
title = "Build the assumption gate's boundary, release and architecture steps (SR-205, SR-206, SR-212)"
workstream = "scripts"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-205", "SR-206", "SR-212"]
needs = ["WI-630", "WI-632"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

Restructured into WI-638.

## Context

Three built-in check steps behind one `[checks] assumption_gate` setting (absent reads off), advisory when off. Enabling the gate in this repository is the C5 act, taken after C4's approvals, not part of this item. Design rows: LLR-242, LLR-243, LLR-244. Test cases: TC-237, TC-238, TC-239. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

**OI-88 ruled (c), 2026-09-27** (`docs/log.d/2026-09-27-owner-ruling-oi88.md`): SR-212 gains a Boundary-rung arm that judges each boundary-referencing requirement against the frame's crossings (`B-##` in `external.toml`): coincident with the crossing, or bridged by an assumption the requirement cites whose `effect_at` names that crossing. Its Arch-rung arm over IF rows stays as approved. This item holds amendment authority over SR-212, LLR-244 and TC-239 for that arm: amend in place, status left Approved, no adjudication filed by the builder; the coordinator's spine-acts batch judges the amendment.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- SR-212, LLR-244 and TC-239 state the Boundary arm over crossings beside the Arch arm over IF rows (OI-88 (c)), and TC-239 drives both arms red then green.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
