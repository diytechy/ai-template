+++
id = "WI-1041"
title = "An accepted risk no acceptance act names is reported as unanchored, rather than anchored to a commit found in history"
workstream = "process"
sr_refs = ["SR-202"]
needs = []
specref = "docs/reviews/2026-11-history-readers/README.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, class (c)
site 2 (`docs/reviews/2026-11-history-readers/README.md`).

An assumption's accepted risk is bound to the acceptance act that accepted
it. When no act names the assumption, the reader falls back to walking the
live registry's history to the first commit at which `accepted_risk` held
its current value, and anchors the risk there. That recomputes a decision
nobody recorded (PROCESS.md §3; the review-churn plan's item 2). The audit
marks it borderline: in that case no record exists, so the fix is to stop
deriving an anchor and say so; the function's own message already tells the
reader to accept the risk in an act.

LLR-239 (Accepted, under SR-202) states the fallback, so this row amends its
text, which drifts for automated adjudication (queue-drill HANDOFF §3.3 N4).

## Done-when

- [ ] With no act naming the assumption, the reader reports the risk as
      unanchored, naming the assumption and telling the operator to accept
      it in an act; it walks no history. The promise covers supported
      workflows and the ledger and registry as the kit writes them; a hand
      edit of either is outside it.
- [ ] LLR-239's text says so (text only; its status is unchanged), and a
      test that fails on today's code shows the new outcome.
- [ ] The Deliverable lists LLR-239's drift as the act owed; the audit
      note's site 2 is marked resolved by this row.
