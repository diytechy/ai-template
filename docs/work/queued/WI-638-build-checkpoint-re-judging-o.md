+++
id = "WI-638"
title = "Assumption build, remaining: checkpoint re-judging of observation tests (SR-215), then the gate's boundary, release and architecture steps with SR-212's Boundary arm (SR-205, SR-206, SR-212)"
workstream = "unattended"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#3-plan-coverage"
sr_refs = ["SR-215"]
needs = ["WI-632", "WI-612", "WI-630"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
supersedes = "WI-634"
+++

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-634 (Build the assumption gate's boundary, release and architecture steps (SR-205, SR-206, SR-212)). The two remaining build items of the assumption plan, one builder: both wire new checks into merge and release, both carry the same D31 tier and `bootstrap.MAPPING` duties, and WI-634 now carries OI-88's amendment. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

State at consolidation: `build/wi-638` holds 32aa17bc and f40373e3 on base b37dbbb1, with rulings 19 and 22 of `docs/reviews/2026-09-26-wave3/ARBITRATION.md` still to address. Rebase it onto trunk, finish those, then build WI-634's scope. Amendment authority (coordinator grant): SR-215, LLR-254 and TC-247 (ruling 19), LLR-233 and TC-228 (ruling 22), and SR-212, LLR-244 and TC-239 (OI-88 (c)) are amended in place, status left `Approved`, no adjudication filed by the builder; ruling 19's other arm, declaring `inputs` and `max_age` on TC-036, TC-055, TC-209, TC-210 and TC-211, is open to the builder instead.

`rejudge.py` decides from a digest of each observation test case's declared inputs; intake files one re-judge item per due case at a work-item merge, and a release subcommand plus a required release-checklist item cover release preparation. Filing runs through the mint path, so its staging must stage and restore only what it wrote first. Design rows: LLR-254, LLR-255. Test cases: TC-247, TC-248. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-634 (Done-when, verbatim)

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- SR-212, LLR-244 and TC-239 state the Boundary arm over crossings beside the Arch arm over IF rows (OI-88 (c)), and TC-239 drives both arms red then green.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
