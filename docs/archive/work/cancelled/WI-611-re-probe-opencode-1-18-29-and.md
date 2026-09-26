+++
id = "WI-611"
title = "Re-probe opencode 1.18.29 and record the version actually tested in agents.toml (review pack C7)"
workstream = "tooling"
specref = ""
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

CANCELLED as MERGED into WI-606 (backlog audit, owner go-ahead 2026-09-26).

One of the four pathway checks this row would re-run is final-text-only
stdout, and WI-606 switches that same opencode route to `run --format json`,
so probing first would record a pathway WI-606 then replaces. WI-606 now
re-runs the checks on the changed route and records the version actually
tested.

## Context

Found by the 2026-09-23 telemetry research; filed by the owner from the
review pack's Part C.

`docs/agents.toml`'s OPENCODE notes record the pathway as tested on 1.17.18;
1.18.29 is installed. The recorded checks were stdin prompt delivery, the
global `--auto` flag, final-text-only stdout, and auth. Bumping the number
alone would claim a test nobody ran.

## Done-when

- The notes' pathway checks are re-run on the installed version, and their
  output is quoted in the log fragment.
- `docs/agents.toml` records the version actually tested, with the date.
- If a check fails, the route is disabled or the failure is filed; the
  version is not bumped over a failure.
