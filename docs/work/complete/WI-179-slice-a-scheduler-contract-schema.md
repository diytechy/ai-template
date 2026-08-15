+++
id = "WI-179"
title = "Slice A - scheduler contract + schema + safety classifier"
workstream = "unattended"
sr_refs = ["SR-153", "SR-156"]
needs = ["WI-178"]
buildtier = "strong"
order = 178
+++

## Deliverable

Slice A: scripts/schedule.py (stdlib frontier + deterministic order + pure safety classifier; `ready --explain/--format json` + `simulate --jobs N` CLIs, side-effect-free) + tests/test_schedule.py (20 fixtures = TC-058/059). Optional WI-schema columns Priority/Exclusive/BlockRef/EstTokens/SafetyClass + `blocked` status added to the work-item template; IF-053/054 seams (CMP-004). SR-057/058 Verified (autonomous single-agent review). Meta registry unchanged - schedule reads absent columns as fail-closed defaults (SafetyClass absent => unclassified).
