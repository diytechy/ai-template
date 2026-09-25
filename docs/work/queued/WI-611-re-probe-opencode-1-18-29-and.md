+++
id = "WI-611"
title = "Re-probe opencode 1.18.29 and record the version actually tested in agents.toml (review pack C7)"
workstream = "tooling"
specref = "docs/plans/2026-09-24-owner-review-pack.md#part-c--defects-found-along-the-way"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++

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
