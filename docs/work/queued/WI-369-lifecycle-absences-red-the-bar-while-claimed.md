+++
id = "WI-369"
title = "The declared-absence honesty test deadlocks the §2.3 parallel-claims model: docs/declared-absences lists docs/work/active/ (and docs/work/pause) whose own reasons say the path legally EXISTS during a lifecycle state ('holds per-branch claim directories only while work is claimed'; 'present only while a pause is DECLARED') - but tests/test_dogfood_sync.py::test_scaffold_omissions_list_is_current fails on ANY declared entry that exists, so the full suite AND every composed-tree bar the integrator runs red 'SCAFFOLD_OMISSIONS entries now materialized: docs/work/active' the moment any claim is outstanding. With two claims open, no branch can merge (each candidate contains the other's claim dir), which is a deadlock of exactly the concurrency the queue exists to serve. First hit 2026-07-30 with WI-366 + WI-368 claimed concurrently. Fix: give the declared-absences format an explicit lifecycle marker - a reason beginning 'LIFECYCLE:' declares a path whose PRESENCE is a legal, documented state - exempt such entries from the materialize-guard (the retired-surface guard stays exact for everything else), tag the two lifecycle rows, document the marker in the file header, and add a bite test proving the exemption is marker-scoped. check_doc_refs.py needs no change (reasons are opaque text consulted only when the path is absent)."
workstream = "scripts"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
+++
