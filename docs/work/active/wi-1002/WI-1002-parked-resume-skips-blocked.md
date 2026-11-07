+++
id = "WI-1002"
title = "The dispatcher's parked-lane resume leaves out a lane whose claimed row reads blocked, so a filed owner-held step launches no worker"
workstream = "process"
sr_refs = ["SR-026", "SR-148"]
specref = "docs/reviews/wi-993/012-ADJUDICATE-26b4d09.md"
buildtier = "medium"
safety_class = "ordinary"
planmode = "none"
priority = 5
+++

## Context

Filed on trunk at WI-993's landing, from the SUCCESSOR ruling of its gate's
dispute sitting (`docs/reviews/wi-993/012-ADJUDICATE-26b4d09.md`, finding PARK,
re-graded MINOR there). `dispatch._parked_branches` reads no schedule, so on the
unattended route a claimed row citing a pending item is relaunched, against the
worker brief's "no worker assignment". The state predates WI-993, which only
sanctions it. The fix reads the `blocked` disposition LLR-288 already derives; it
adds no second predicate and no detector for a session that stopped and filed
nothing (WI-993's call 7). LLR-143 owes its amendment and sitting. Owes its scope
critique before its claim.

## Done-when

- [ ] The parked-lane resume leaves out a lane whose claimed row reads blocked in
      the shared schedule: it launches no worker, keeps the claim, goes on to
      claim the next ready row and ends without a stall. A parked lane whose
      claimed row reads anything else keeps today's resume admission. The
      promise reaches supported workflows and the kit's own routes, as
      PROCESS.md §6 "Review threat model" bounds a spec's promise; hand-edited
      kit-written state, hand-chosen aliases and sub-second timing windows are
      outside it.
- [ ] The resume LLR is amended to say so.
- [ ] A `tests/test_dispatch.py` case over a parked blocked lane beside a ready
      row asserts no launch, the claim kept and the next row claimed.
- [ ] RESYNC entry, if the behaviour reaches adopters.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Critique dispositions

Round 1 (fresh Codex session, 2026-11-07): CHANGES-REQUESTED, two MINORs.

- **S3, the default for other dispositions and the supported-workflow bound:
  adopted.** The first Done-when item now reads "A parked lane whose claimed
  row reads anything else keeps today's resume admission", and it carries the
  bound.
- **S4, the planning ruling: adopted as `planmode = "none"`.** The change is
  one filter on the parked-lane list, reading a disposition that already
  exists, and the Done-when's `tests/test_dispatch.py` case fully specifies it,
  which is S4's stated exception.

Round 2 (fresh Codex session, confirming, 2026-11-07): APPROVE, no findings; both dispositions confirmed.
