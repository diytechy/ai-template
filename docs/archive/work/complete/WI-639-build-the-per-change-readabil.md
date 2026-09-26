+++
id = "WI-639"
title = "Build the per-change readability report over declared measures (SR-216)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-216"]
needs = ["WI-642"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

Built test-first against the approved chain SR-216 (for SN-041), LLR-256,
TC-249, by a builder session in its own worktree, and reviewed before merge.

- `check_readability.py`: reads `[readability]` from the stack profile
  (`measures`, `gating`); `MEASURES` maps each name to an adapter that runs that
  measure's own comparison over the changed parts only. The complexity adapter
  reuses `check_complexity`'s census, baseline reader and comparison: the census
  loop was extracted as `check_complexity.functions`, not copied.
  `changed_parts` reads the index against HEAD, or merge-base to tip on a claimed
  branch. `worsened_findings` prints one line per worsening naming the measure,
  the part and the delta. The exit is 1 only for a worsening in a gating
  measure: an unknown or undeclared name prints a WARN, an unreadable change a
  SKIP, and both exit 0.
- `[readability]` and `[step:readability]` in the stack-profile template and in
  `docs/stack.ini`. This repository measures `complexity` with no gating, since
  `[step:complexity]` already enforces the same baseline. The complexity measure
  covers the profile's `[paths]` source and test roots only, so an adopter's
  vendored kit is not measured.
- `check_complexity.py` now ships to adopters: the shipped report must reuse it,
  and a shipped script may not import an unshipped one.
- Seams: IF-187 (the step's exit code), IF-188 (`check_complexity` called by the
  report), IF-189 (`agent_common.default_base` for a claimed branch), cited by
  TC-249's `verifies` (a traced pointer cell).
- Tests: `tests/test_check_readability.py` (TC-249, registered slow), 15 cases,
  each seen failing before its code. The claimed-branch case is mutation-checked
  against both wrong readings (the previous commit, and trunk's tip).

Review: codex Sol (medium) NOT YET SOUND, 1 blocker (the exit rule must be
LLR-256's "nonzero only for a worsening in a gating measure"; the code was
conformed rather than the row amended) and 1 major (the merge-base proof), both
fixed.

## Context

`check_readability.py`, a `[readability]` section of the stack profile, and adapters that reuse each measure's own comparison; complexity is the first measure, admitted because it can name the part it worsened. Design rows: LLR-256. Test cases: TC-249. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
