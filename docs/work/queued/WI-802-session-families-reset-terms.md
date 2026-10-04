+++
id = "WI-802"
title = "Session families with declared reset terms"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-session-families"
sr_refs = ["SR-227"]
needs = ["WI-801"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-session-families (ch.2 §2, §9). Five
families share one retention slot and one independence rule each: [plan and build],
[adjudicate], [adjudication review], [review], [judge]. `[adjudicator]` becomes
`[sessions.<family>]` with `context_reset_pct` (0 = every call). The template retains
both adjudication families at 55 and this repo stays at 0 (D-010; README changes 1,
2: S10 "reviewers never" narrowed, the template ships retention on). `rejudge` moves
to [judge] and `retain_for` retires (D-011, change 22). Directory-bound runners
(opencode, gemini) gain the term "the directory differs". Under README A1 this row
keeps only the reset terms; routing by kind is WI-801's. A1 also names where
strength is defined today, for this row's docs; the two effort value drifts A1 found
are follow-ups outside this row.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- The template retains both adjudication families at 55; this repo's values are
  unchanged.
- Each family's reset terms are pinned by tests, including the opencode directory
  term and the no-`used` rule (a route reporting no `used` resets every call).
- A spawn failure before the runner starts leaves the session active.
- The retained adjudication reviewer, builder retention at every call, `rejudge`
  under [judge] and the 1200 s lease wait are in place.
- Each spine row the README matrix gives this row (SR-227, LLR-270,
  TC-266/267/268/303, IF-247/248, IF-081/155, shared with WI-800) is amended and
  passes adjudication of that row, on whichever adjudication path is the one path
  when this row lands.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`; no
  extra bar is named.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; it moves `[adjudicator]`'s keys
  to `[sessions.<family>]` (risk 9), and adopters inherit the shipped 55.
