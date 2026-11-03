+++
id = "WI-992"
title = "OI-120's ruling: re-draft and file P8's rows (the review gate's scoped test set)"
workstream = "process"
sr_refs = ["SR-146"]
specref = "docs/requirements/open-items.toml"
needs = ["OI-120"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-11-02 (attended) with OI-120, as the queued placeholder
row a pending open item is filed with (OI-102): it carries the owner's
decision to the queue. P8 is the review-churn plan's item 13 phase-1 row
(the test-file TC tag and its one reader, the derived review test set and
its refusals, the strict-mark commit check). Its drafts were lost with leg
06's scratch root, so the rows are re-drafted from the plan after the
ruling (coordinator-2026-11-02 D-005).

## Done-when

- [ ] The owner rules OI-120, and the ruling commit replaces this list with
      the work the ruling routes (OI-102): planner sub-agents re-draft P8's
      rows under the ruled calls, each row is filed on trunk owing its scope
      critique, and this row closes citing the filing.
