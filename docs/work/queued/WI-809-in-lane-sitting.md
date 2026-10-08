+++
id = "WI-809"
title = "The in-lane adjudication sitting from LOCK to MERGE_ACTION, with final evidence"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-sitting"
sr_refs = ["SR-178", "SR-228"]
needs = ["WI-808", "WI-806", "WI-802", "WI-849", "WI-850", "WI-851"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-sitting (ch.4 §1, §4.1-§4.4, §5, §8, §11).
A lane's `ADJUDICATION` runs in the lane under the station authority: `LOCK`,
`REFRESH` (commit-tier bar; the full bar once on the final tree, D-015), `JUDGE`
acting on a mechanically committed scope record (B6), and `MERGE_ACTION`; then the
final independent review, regeneration and the declared bar on the final tree (B5).
Acts move into the lane (README changes 7-9: only a lane in `ADJUDICATION`, under
the authority, mints or acts; "an adjudication runs alone" is replaced). Act
admission follows ch.2 §3 step 2's table and B10 (D-022). A `return` moves the specs
back to `active/<branch>/` (D-019). A fourth sitting that owes a return ends
`merge-partial`, and nothing red lands (D-024). Held-rung CLARITY acts follow
WI-851's state rule; the design's ch.4 row keeping `_held_status_refusal`
"unchanged" is superseded by WI-851. WI-791's contract is complete, so it is
dropped from `needs`.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- A build lane's Drafted rows are approved in the lane: the loop's sitting takes
  the act through WI-849's verdict-backed rung, extended with the ADJUDICATE
  range and ch.2's eligibility condition, with no second actor test.
- An out-of-scope act, an act outside an ADJUDICATE range, or an act by a session
  that ch.2's judged-scope table makes ineligible is refused.
- A rejected final review drops the act.
- Held-rung rows in an in-lane act are judged by WI-851's state-based check,
  and this row adds no CLARITY arm of its own. A re-attestation of a row below
  approval is still refused: it carries no signature to carry over (OI-100,
  SR-228; owner, 2026-10-04).
- A landing whose swap fails on a foreign trunk commit re-enters `REFRESH` under
  the same authority, and a stale act is retaken by a session.
- A fourth `return` is refused, and the sitting's outcome is `merge-partial` (green:
  the work lands; red: an empty keep set), with no red tree landed.
- The adjudicate prompts are amended for acts taken in the sitting
  (`worker.template.md`'s approval-act paragraph moved to WI-849).
- Each spine row the README matrix gives this row (SR-178,
  LLR-144/149/152/161/262/278, TC-143/146/153/257/278, IF-091; LLR-158 and
  TC-218's method moved to WI-849, and this row extends TC-218: a lane flip
  admitted only in an eligible ADJUDICATE range) is amended and passes
  adjudication of that row, on whichever adjudication path is the one path when this
  row lands.
- The row's test bar: its affected modules' tests (acceptance, integrate,
  agent_loop) plus the smoke tier at `-n 2`; no extra bar is named.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; acts move into the lane.
