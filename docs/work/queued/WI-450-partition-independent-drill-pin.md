+++
id = "WI-450"
title = "Make the WI-435 drill-port test pin partition-independent: tests/test_traj_views.py hardcodes a component id (data-to=cmp:CMP-008, formerly CMP-004) AND an arity (2 ports, formerly 3), so it re-breaks at every re-partition — but the invariant it defends (one connector circle per edge, distinct cy per shared port) is partition-independent and should be asserted over whatever components exist. Surfaced by the WI-441 adoption build, which had to touch the pin. Also fold in the latent flake WI-449's builder observed: two test_traj_views tests read the REAL repo's docs/architecture.md rather than a tmp_path fixture, so a concurrent regeneration can fail them — point them at a fixture tree."
specref = "docs/requirements/open-items.toml#OI-14"
workstream = "lock-program"
sr_refs = ["SR-054"]
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++
