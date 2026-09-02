# WI-572 — REVIEW-A rollup

Compiled by the supervising session (2026-09-02) from the round files under
`docs/reviews/wi-572-the-approval-act-is-the-adjudi/`, time-ordered, governing
line last. Eight rounds were mechanized (Terra and Opus alternating under the
loop's escalation policy, two Sol/Opus design-checks between them); the last
two were drawn by the supervisor through an independent Opus reviewer with a
hostile brief after the loop's resume cycle stalled (the DESIGN-CHECK session
024 performed the round-023 rework itself, so three BUILD sessions found
nothing to commit and no round was scheduled — the C6 shape again). The
verdict gate requires this per-WI rollup and nothing in the kit writes it
yet, so it is compiled by hand.

### Supervisor note — NOT a round, does not govern

Every CHANGES-REQUESTED round on this row found a real hole in the new
first-approval arm rather than churn: the brief's dial filter, the terminal
instruction that let an APPROVE stop before the flip, the demotion that
stranded a row, the brief scoping itself to the whole Drafted backlog, the
`--approves` join/quoting/mixed-batch derivation, the exemption's bounds,
and the refusal's tier coverage. The lane touched no snapshot file and moved
no Status; it amended three registry rows' text (LLR-136, LLR-158, IF-091),
which correctly mints an amendment adjudication at this merge under the arm
this row ships. It also fixed the drained-trunk `wi_convert` README defect
(kit finding 10 of the 2026-09-01 evening entry) because its own close
drains `active/`. One supervisor deviation is recorded in the fragment: the
merge refusal covers the stakeholder-needs tier as well as SR/LLR/TC (the
owner-held tier is spine; off-spine approval stays with OI-30 D3).

### Round 3 — OPENAI-TERRA — tip b25660e — VERDICT: CHANGES-REQUESTED findings=1
The first-approval brief re-rendered every Drafted chain without re-checking
`human_holds`, so a held SR could be offered beside released rows.

### Round 5 — OPENAI-TERRA — tip 26ad36a — VERDICT: APPROVE findings=0
The dial filter verified.

### Round 7 — OPENAI-TERRA — tip 66d0d31 — VERDICT: CHANGES-REQUESTED findings=1
The brief's terminal instruction told the adjudicator to commit only the
verdict and stop, so an APPROVE could leave every row Drafted.

### Round 10 — OPENAI-TERRA — tip 9f3790c — VERDICT: CHANGES-REQUESTED findings=1
An `Approved` → `Drafted` withdrawal was neither a lane act (correct) nor fed
to the first-approval trigger, stranding the row with no actor.

### Round 12 — ANTHROPIC-OPUS — tip 76efc1e — VERDICT: CHANGES-REQUESTED findings=5
The brief's population came from `reattest_model` over the whole repo, not
the merge delta; the smoke tier red at the tip (the drained-trunk README
defect surfacing); the refusal wording on deletions; two clarity items.

### Round 15 — ANTHROPIC-OPUS — tip 87ac214 — VERDICT: CHANGES-REQUESTED findings=3
BLOCKER: `--approves` joined with spaces where the parser splits on `;`;
the refusal walked SR/LLR/TC only; the adjudication-lane exemption untested.

### Round 19 — OPENAI-TERRA — tip 29a819a — VERDICT: CHANGES-REQUESTED findings=1
The exemption admitted any flip on an adjudication lane, not only the rows
it adjudicated.

### Round 23 — ANTHROPIC-OPUS — tip 6af1e4a — VERDICT: CHANGES-REQUESTED findings=5
The refusal still blind to SN and the off-spine registries; `{registries}`
rendered unquoted; derived from rows offered, not approved; a
complexity-baseline row re-stamped upward; two generators still saying
"WHOLESALE".

### Round 28 — supervisor-drawn, independent Opus, hostile brief — tip d5b3e12 — VERDICT: CHANGES-REQUESTED findings=4
All five round-23 findings verified fixed by driving code; four bookkeeping
falsities remained (a copied complexity reason, a "two rows" miscount, two
stale byte stamps, one stale comment). Smoke green at the tip; the README
defect fixed.

### Round 29 — supervisor-drawn verification — tip 94b77a2 — VERDICT: APPROVE findings=2
The four fixed and each correction true; the SN extension driven at the
merge slot (flip and born-Approved refused by name; held rung mints nothing;
no accidental widening of the amendment warn or the intake mint; the
exhaustiveness pin holds). Two MINORs: a byte-stamp row credits a NO-COMMIT
session; the SN test's comment claims an undriven released-dial case.
(Full texts: the round files named above.)

VERDICT: APPROVE findings=2
