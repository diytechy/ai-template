+++
id = "WI-291"
title = "Extract the WI-registry loader shared between schedule.py (CMP-004 decision engine) and check_trajectory.py (CMP-001 validator) into one lower-level primitive - both independently parse work-items.csv and build the predecessor graph with near-identical load_wis (same WI_ID_RE, -000 skip, ~-prefixed hard/soft split, _split_refs), which the dupes census grandfathers as 2 sanctioned blocks (d47d5975c21b, f800f0c60265). The duplication persists DELIBERATELY: schedule stays a pure dependency-free RUNTIME library and IF-053 fixes the arrow (validator consumes scheduler, never the reverse), so neither may import the other. Fix: a small lower-level wi_registry.load() BOTH depend on downward, deleting the census pair without inverting the dependency. Adjacent to WI-280's core-decomposition; surfaced 2026-07-24 clarifying the decision-vs-validation split."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
order = 288
+++

## Deliverable

Resolved by DRIFT GUARD not extraction (owner-directed 2026-07-24): the schedule.py <-> check_trajectory.py load_wis duplication is deliberate (F5 ruling 2026-07-12; schedule stays stdlib-only self-contained, IF-053 fixes the arrow), so NO shared wi_registry.py. tests/test_wi_loader_sync.py (3 cases) locks both parsers to identical shared decisions (WI id set, hard/soft pred split, status, SR-refs, title, blockref) over an edge-case fixture, closing the only real two-parser risk. docs/dupes-allow header documents it.
