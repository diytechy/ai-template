+++
id = "WI-1042"
title = "The test-first check reads when each row was accepted from the act ledger instead of replaying registry history"
workstream = "process"
sr_refs = ["SR-217"]
needs = []
specref = "docs/reviews/2026-11-history-readers/README.md"
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, class (c)
site 3 (`docs/reviews/2026-11-history-readers/README.md`). Its two calls
serve one decision, so one row covers both (the coordinator's ruling at
WI-1036's review).

The test-first check needs to know when each requirement was first accepted,
and when each pair of a test case and a requirement it names first read
accepted. Today it replays every first-parent commit touching the
registries and applies the acceptance-act rule to each commit and its
parent. That recomputes a recorded decision (PROCESS.md §3; the review-churn
plan's item 2). The record exists: each act-ledger entry lists the rows it
accepted and re-accepted, its commit is the one that added it, and the
snapshot copy at that commit holds the accepted rows, test cases' `verifies`
cells included.

**Open at filing, for this row's scope critique to settle:**

- Acceptances before the ledger's first entry (seq 1, 2026-09-27) have no
  entry. The replay dates them today; the ledger alone would not. The row
  must state how they are read (the module's existing "at or before"
  reading is one shape).
- Whether every flip to Accepted since 2026-09-27 carries a ledger entry
  has not been checked; the row checks it before the ledger is trusted, and
  files any gap.

SR-217 and LLR-257 (both Accepted) state the replay, so this row amends
LLR-257's text, which drifts for automated adjudication.

## Done-when

- [ ] The ledger's completeness since its first entry is checked, and the
      result quoted; any gap is filed, not patched over.
- [ ] Both readings come from the ledger and the snapshot copies, with the
      pre-ledger rule the critique settles; no first-parent replay remains.
- [ ] The check's verdicts on this repository are unchanged, or each change
      is explained; a test that fails on today's code shows a ledger-read
      date.
- [ ] LLR-257's text says so (text only); the Deliverable lists its drift as
      the act owed, and the audit note's site 3 is marked resolved.
