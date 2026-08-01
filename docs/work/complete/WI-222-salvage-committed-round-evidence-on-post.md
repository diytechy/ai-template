+++
id = "WI-222"
title = "Salvage committed round evidence on post-commit disposition resets (WI-220 review finding 1)"
workstream = "unattended"
sr_refs = ["SR-063", "SR-066"]
needs = ["~WI-220"]
buildtier = "medium"
safety_class = "high-risk"
order = 219
+++

## Deliverable

_salvage_round_evidence now also scans git diff --name-only <reset-target> -- docs/plans (files still on disk pre-reset), so error resets salvage DP-* evidence already committed past the reset target - closing the dual-plan CAS-stale gap where a committed round vanished with a clean porcelain; _reset_failed_disposition forwards the target it already holds, no call-site changes, best-effort contract intact. Regression drives a real SELECT whose integration ref an external actor moves mid-round: the disposition errors and the committed round survives under out/dispatch/salvage/<train> (failing pre-fix). LLR-064 Detail amended.
