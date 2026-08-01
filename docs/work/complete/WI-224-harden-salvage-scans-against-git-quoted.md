+++
id = "WI-224"
title = "Harden salvage scans against git-quoted DP-* paths (WI-220 review finding 3)"
workstream = "unattended"
sr_refs = ["SR-063", "SR-066"]
needs = ["WI-222"]
buildtier = "quick"
safety_class = "ordinary"
order = 221
+++

## Deliverable

Both salvage discovery commands now request NUL-delimited output (status --porcelain=v1 -z and diff --name-only -z), eliminating core.quotepath C-quoting and parsing rename/copy destination records without an arrow heuristic. Malformed/failed scans remain best-effort and non-raising. A core.quotepath=true regression proves a non-ASCII DP-004-café round is salvaged through both the untracked porcelain and committed-diff paths.
