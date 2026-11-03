+++
id = "WI-992"
title = "OI-120's ruling: re-draft and file P8's rows (the review gate's scoped test set)"
workstream = "process"
sr_refs = ["SR-146"]
specref = "docs/specs/WI-992.md"
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

OI-120 ruled 2026-11-02 (a) on each call (coordinator-2026-11-02 D-006).

- [ ] Planner sub-agents re-draft P8's three rows from the review-churn
      plan's item 13 under the ruled calls: (1) the test-file TC tag on the
      existing `Implements:` line and its one reader; (2) the review test set
      derived from the tags and the row's SRs, refusing an empty or partial
      set and refusing a code-touching row that names no SR (never falling
      back to the whole bar); (3) the strict-mark commit check, with
      `[bars] red_mark` a required key. Each draft re-measures the counts
      the 2026-10-20 drafts gave.
- [ ] Rows (1) and (3) each carry a RESYNC entry naming its forced adopter
      migration (tagging test files; adding `[bars] red_mark`).
- [ ] Each row is filed on trunk owing its scope critique, and this row
      closes citing the filing.
