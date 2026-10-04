+++
id = "WI-813"
title = "Restore the dual-plan pickup in a claimed lane, and census the trunk writers"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-dual-pickup"
sr_refs = ["SR-155"]
needs = ["WI-804", "WI-799", "WI-810"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-dual-pickup (ch.3 §4.6, §4.10, §6). The
dispatcher admits a `planmode = "dual"` row like any row (still the exclusive
`high-risk` kind); the lane enters `PLANNING.DUAL`, runs the round through `ask` in
`docs/plans/<WI>/round-<n>/` (D-008, so no `DP` allocator; the `DP` watermark key is
frozen), and drafts provenance-keyed children that MINT allocates all or none. A
PAGE closes the parent `partial` and mints an open item and a successor
decomposition row that waits on it (D-023). By README A3, that open item offers the
owner an independent third agent of their choosing to select between the plans, run
only if the owner picks it. `--dual-plan`, `_dual_plan_entry`, the preflight refusal
and the off-lane writers retire. It follows WI-810 so children come from the one
allocator (B7; README order notes), and as the last writer move it carries the
writer census (D-026). WI-790 is complete and dropped from `needs`.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- Admit: a dual row is claimed and enters `PLANNING.DUAL`, with no refusal loop.
- Round: recorded fixtures reach SELECT.
- Children: provenance `source` keys, and an all-or-none mint.
- Duplicate: a repeated `source` is refused.
- Page: the parent closes `partial`; the minted successor carries the round and
  waits on the open item, and the open item offers the third-agent option (A3).
- Resume: a round continues from `state.json`.
- The census test: no tool writer to trunk remains outside the landing (ch.4 §3).
- PROCESS_OPTIONS' dual-plan layer is reworded (ch.3 §4.10).
- Each spine row the README matrix gives this row (SR-155, LLR-074/095/096/132,
  TC-074/097/098, IF-061) is amended and passes in-lane adjudication.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus the no-writer-outside-the-landing census.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; `--dual-plan` launchers stop,
  and a dual row is claimed like any row.
