+++
id = "WI-866"
title = "A consolidation close writes every edge its verdict names, several on one waiter included"
workstream = "process"
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 7
+++

## Deliverable

`handback`'s consolidation close now resolves and validates every affected queued specification before its first write (a later edge target with no readable needs line, or a return target no longer queued, refuses by name and leaves the lane's `docs/work` byte-identical), plans one ordered rewrite sequence per specification so every blocker a verdict names for one waiter lands in its needs, and applies each sequence over the specification as it then stands, so a link an earlier move redirected survives the later writes, the adjudication specification's own link included after its move to complete. Rows: LLR-312 approved (verdict 002); TC-254 re-attested (verdicts 003 and 004, the second after the fresh full-lane review's one MINOR on the mint clause's window was fixed in the lane). Codex 6.1 Sol: the fresh full-lane review SOUND (`d144b1ae`, at medium; `docs/reviews/wi-866-consolidation-close-keeps-every-edge/sol-review-full.md`). The rebase onto WI-860's landing renumbered the lane's acts to 65-67. Decisions: `docs/decisions/wi-866.toml` (D-001, D-002).

## Context

Filed by hand by the coordinator on 2026-10-08. WI-864's consolidation verdict named three edges on one waiter (WI-848 needs WI-852, WI-853 and WI-860); the mechanical close (`handback.close_adjudication`) wrote only the last. `handback._enact_plan` computes each planned write from the spec's on-disk text before any write, so two writes to one file keep only the last (docs/decisions/wi-864.toml D-003; the coordinator restored the lost edges by hand).

## Done-when

- The close's plan composes every edge on one waiter into one write, and any other two planned writes to one file likewise; none is lost.
- A test closes a verdict naming two edges on one waiter and finds both in its `needs`; it fails before the fix.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.

## Adjudication follow-ups, answered in this lane

The checkpoint sitting (`docs/reviews/wi-866-consolidation-close-keeps-every-edge/001-ADJUDICATE-931d0f1.md`) ruled TC-254's amendment MEANING without blessing it and returned LLR-312, with one drafted follow-up. Under the owner's ruling of 2026-10-06 (a return is answered in the lane, not minted), it is answered here as TC-254 row text, with no behaviour change:

- TC-254's Method and Evidence carry LLR-312's preflight clause (a later unwritable edge or return target refuses by name and leaves `docs/work` byte-identical), citing the two existing preflight tests, and its Expected says so.
- TC-254's link clause states exactly what the cited test drives: the linked row moves first, and both links resolve to its `draft/` path, the adjudication spec's included after its own move to `complete/`.

LLR-312 needs no text change. The re-sit judges TC-254 for re-attestation and LLR-312 for first approval in one sitting.

The re-sit (`002-ADJUDICATE-09d62f8.md`) approved LLR-312 and ruled TC-254 MEANING, not blessed: its Expected claimed a preflight at the mint that no clause drove. Answered the same way: TC-254's Method and Evidence now cite `test_a_row_claimed_between_close_and_merge_refuses_the_whole_mint`, which drives the mint's whole-mint refusal. The next re-sit judges TC-254 alone.

The second re-sit (`003-ADJUDICATE-afd61d4.md`) blessed TC-254 and re-anchored it. The fresh full-lane review then found that the new mint clause placed the hand claim "between the close and the merge", while its test claims after the merge and before the successor mint; the Method now states that window. The next sitting judges TC-254 alone again.
