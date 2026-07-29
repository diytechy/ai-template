+++
id = "WI-040"
title = "Trajectory freshness at commit - hook step (F2)"
workstream = "unattended"
sr_refs = ["SR-019", "SR-038"]
needs = ["WI-022", "WI-031"]
order = 39
+++

## Deliverable

THREAD_52_REVIEW.md F2 - the shipped pre-commit hook runs check.py --run-step trajectory-map (vacuous for a non-adopter, ~0.2s measured), so a registry edit that stales the dashboard blocks at commit, not first in CI; the hook-vs-CI freshness rule stated once in the hook.
