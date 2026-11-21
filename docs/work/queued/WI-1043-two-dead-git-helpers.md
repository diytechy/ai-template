+++
id = "WI-1043"
title = "Two history helpers nothing calls are removed from the kit's scripts"
workstream = "process"
sr_refs = []
needs = []
specref = "docs/reviews/2026-11-history-readers/README.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, which
found two helpers that read git history and have no caller anywhere in the
repository: `integrate._last_commit_time` and `traj_parse._git` (checked by
grep at `a0ca15d3f`, compiled caches aside). Dead history readers invite a
later caller to recompute a decision from history.

## Done-when

- [ ] Both functions are deleted, with any import only they used; a grep of
      the repository shows no remaining reference.
- [ ] The test modules importing `integrate` and `traj_parse` pass, with
      `test_import_layers` and `test_module_size_ratchet`; a RESYNC entry is
      added if the commit checks ask for one.
