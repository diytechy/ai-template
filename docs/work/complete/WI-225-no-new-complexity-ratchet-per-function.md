+++
id = "WI-225"
title = "No-new-complexity ratchet: per-function C901 baseline test (review-18 H-02 slice A)"
workstream = "quality"
buildtier = "medium"
safety_class = "ordinary"
order = 222
+++

## Deliverable

tests/test_complexity_ratchet.py pins the per-function C901 census of project-trajectory/scripts to a committed 52-entry (file, function)->complexity baseline with the threshold (10) pinned in the invocation: growth or a new over-limit function fails naming the function and demanding simplification (a deliberate bump is a reviewed baseline edit with a logged reason), and an improvement fails until the entry is re-stamped downward in the same commit, so the ratchet only tightens by default. Skips without ruff (dev dependency), mirroring the suite's needs-git guards. Both failure directions verified live and reverted; WI-226 pays the debt down.
