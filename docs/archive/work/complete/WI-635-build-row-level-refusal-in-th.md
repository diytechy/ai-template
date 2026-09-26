+++
id = "WI-635"
title = "Build row-level refusal in the snapshot refresh (SR-207)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-207"]
needs = ["WI-642"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Built test-first against SR-207, LLR-245 and TC-240 by a builder session in its
own worktree, reviewed, and squash-merged.

- `baseline_snapshot.refresh_refusal` refuses row by row. For each registry the
  act copies, the rows whose approved text drifted from the recorded copy,
  minus the rows the act flips, minus the rows named by the new
  `intake.py snapshot --reattests <ROW-ID>[,...]`, must be empty. `--approves`
  still records a ref but clears no row. A recorded approved row missing from
  live counts as drifted ("removed from the live registry") and is blessed only
  by naming it. The refusal lists every row and cell, uncapped. The act's
  record stamps the re-attested ids.
- `--reattests` ids are validated against the live rows (and the recorded ones)
  before every copy, including the seed and repair paths. A first signing
  refuses any `--reattests`, since it copies the whole tree and writes no stamp.
- The rule iterates `SNAPSHOT_TIERS`: all eight current tiers, including the
  three sharing `external.toml`, and needs stay outside. The assumption and
  surrogate tiers join when WI-629 adds them. The tests are parametrized from
  the same tuple, and WI-629's Done-when now requires showing that run.
- Prompts (the amendment brief's MEANING aftermath, the first-approval brief),
  the gate-advance skill's three copies and two reference docs now say
  `--reattests`; the prompt catalogue is regenerated. IF-123's contract and
  `data` cover the flag.
- Tests: TC-240's cases in `tests/test_baseline_snapshot.py`, red before the
  build. The two tests pinning the old "any flip authorises the file"
  behaviour change with it, as LLR-245 says, and eight others now name their
  rows.

Review: codex Sol (medium) NOT YET SOUND, 1 blocker (a removed approved row
entered the record unnamed) and 2 major (the seed path skipped validation; the
assumption tiers are not exercised yet). The first two were fixed; the third is
sequenced onto WI-629.

## Context

An approval act refuses while any row outside it has drifted approved text; `--reattests` names re-attested rows, and the act's record names them. The two snapshot tests pinning the old any-flip behaviour change with it. Every caller that builds `--approves` (the adjudication brief, intake's mint prose) is checked against the new meaning. Design rows: LLR-245. Test cases: TC-240. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
