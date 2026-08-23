+++
id = "WI-230"
title = "Publish under disjoint dirt: publication proceeds when dirty tracked paths are disjoint from the publish diff (2026-07-18 field finding 1)"
workstream = "unattended"
sr_refs = ["SR-156"]
needs = ["~WI-220"]
buildtier = "strong"
safety_class = "high-risk"
order = 227
+++

## Deliverable

publish_integration replaces the blanket dirty-at-outset defer with a disjointness rule: it intersects the tracked worktree/index dirt (NUL-delimited, rename-split diffs) with the dev_head..target publish diff - an empty intersection proceeds and the checkout syncs via git's own two-way merge (read-tree -m -u), carrying the disjoint edits forward byte-for-byte while git's clobber-refusal backstops the never-reset contract; a non-empty intersection defers exactly as before. The same rule governs the two recovery branches (already-at-target crash window and post-CAS verified sync) with the exact-old reset --hard retained for the mechanically-stale case; no path-name allowlist. Unblocks the owner-scratchpad and generated run-state dirt that previously stranded WI-227's publication. Regressions prove disjoint-proceeds-and-survives, intersecting-defers-untouched, idempotent crash replay, and run-state-alone; publish_integration C901 baseline bumped 17->20 (reviewed, WI-226 absorbs).
