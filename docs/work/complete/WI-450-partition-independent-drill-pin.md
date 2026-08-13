+++
id = "WI-450"
title = "Make the WI-435 drill-port test pin partition-independent: tests/test_traj_views.py hardcodes a component id (data-to=cmp:CMP-008, formerly CMP-004) AND an arity (2 ports, formerly 3), so it re-breaks at every re-partition — but the invariant it defends (one connector circle per edge, distinct cy per shared port) is partition-independent and should be asserted over whatever components exist. Surfaced by the WI-441 adoption build, which had to touch the pin. Also fold in the latent flake WI-449's builder observed: two test_traj_views tests read the REAL repo's docs/architecture.md rather than a tmp_path fixture, so a concurrent regeneration can fail them — point them at a fixture tree."
workstream = "lock-program"
sr_refs = ["SR-054"]
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Completed 2026-08-13. The drill-port pin now asserts the partition-independent
invariant (any component with >=2 same-side edges renders one connector circle
per edge with distinct cy; a vacuity guard fails loudly if none qualifies)
instead of a hardcoded component id and arity, so re-partitions stop breaking
it. The two top-view tests read an atomic tmp_path snapshot of the real repo's
inputs instead of the live ROOT, closing the observed concurrent-regeneration
flake while still testing actual meta-repo content. Module 39 passed; smoke
1052 passed / 2 skipped. Merge note for the Part B slice: the snapshot helper
names components.csv/interfaces.csv explicitly and is generalized to the
surviving carrier when those convert.
