+++
id = "WI-812"
title = "The spine-authoring flow: adjudicator drafts, reviewer edits, unchanged final pass acts"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-spine-authoring"
needs = ["WI-809", "WI-802", "WI-810"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-spine-authoring (ch.4 §7, §11; OI-101 Q1).
Inside `JUDGE`, the adjudicator drafts spine text (or adopts the builder's), the
adjudication reviewer edits it, and the act is the adjudicator's final pass, valid
only if it changes no byte; a changed byte goes back to the reviewer, at most 3
rounds, after which the rows land unsettled and are minted. B10's non-mutating final
pass is the one exception to the independence rule, applied identically in
routing, session reuse and act admission (D-022). The amendment brief's "a judge
never amends the row it judges" becomes draft, commit alone, approve only on a later
unchanged pass (README change 14). Code findings still return to the builder
(D-017).

## Done-when

- A final pass that changes any byte cannot act.
- With the two-family pool, every kind in the flow has an eligible draw (ch.2 §3
  step 2 as amended by README A1), and the act admits exactly B10's exception.
- A fourth round is refused, and its rows are minted unsettled.
- `prompts/adjudicate-amendment.template.md:96` and its twin in
  `adjudicate-first-approval.template.md:99` carry ch.4 §7's wording.
- The README matrix names no spine row for this row; any it amends or adds passes
  in-lane adjudication.
- The row's test bar: its affected modules' tests (prompts and range rules) plus
  the smoke tier at `-n 2`; no extra bar is named.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; the shipped adjudicate prompts
  change.
