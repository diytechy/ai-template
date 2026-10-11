+++
id = "WI-902"
title = "A disposition can name an already-filed successor instead of drafting a duplicate"
workstream = "process"
sr_refs = ["SR-220"]
specref = "project-trajectory/scripts/handback.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by the coordinator on 2026-10-10 (overnight leg 01, decision D-022 in
`docs/decisions/coordinator-2026-10-10.toml`), from WI-894's disposition
verdict (`docs/reviews/wi-894/001-ADJUDICATE-3cd530b.md`, its second
finding). WI-828 closed partial after its successors (WI-892, WI-893) and its
open item (OI-113) were filed by hand. The sitting ruled PARTIAL and drafted
no successor, because a draft would mint a duplicate of WI-893. Two guards
then refuse the outcome the verdict reached:
`handback.close_adjudication`'s `owes_successor` guard refuses the mechanical
close (WI-894 was closed by hand), and `intake.py sweep` refuses the merge of
an early-close adjudication row whose `## Dispositions` is empty (OI-70/OI-73,
"no third exit"). No draft key names an existing queued row:
`intake._DRAFT_KEYS` mints a new row only.

## Done-when

- A disposition verdict can discharge the successor obligation by naming an
  existing queued row that carries `supersedes` of the closed row; the
  mechanical close and the sweep accept it, and still refuse an early close
  that names neither a draft nor such a row.
- The scope of OI-73's "no third exit" is kept: naming an existing successor
  is the same exit (a successor is queued), not a third one.
- Tests: an early close naming an existing superseding row closes and
  sweeps; one naming a row without `supersedes`, or a missing row, refuses;
  a drafted successor is unchanged.
- The rows the change makes untrue (LLR-312's chain, and the sweep's row)
  state it and pass adjudication.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (shipped scripts change).
