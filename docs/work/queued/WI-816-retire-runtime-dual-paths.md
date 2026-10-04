+++
id = "WI-816"
title = "Retire the runtime dual paths that need no adopter migration"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-retire-runtime-dual-paths"
sr_refs = ["SR-027"]
needs = ["WI-799"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-retire-runtime-dual-paths (ch.1 §7, §9.2;
risk 7: no fallback modes). It retires D7 (the dead CSV arm in `intake.py`), D8
(`work-items.csv` reads), D10 (the hand-written review rollup window), D11 (the
second terminal home `docs/archive/work/<t>/`, moving WI-689), D12 (the lock running
unguarded on ENOLCK/ENOTSUP, which now fails closed naming the filesystem; D-007) and
the `_name_status` shim from D13. It needs WI-799 because both edit `integrate.py`.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- Each path is deleted, and its tests become refusal tests.
- A lock on an unsupported filesystem exits with the filesystem named.
- Nothing reads `docs/work/<terminal>/`, and WI-689's spec is moved to the one
  terminal home.
- Each spine row the README matrix gives this row (SR-027, LLR-029, LLR-030,
  IF-023; LLR-140's rollup window and its TC) is amended and passes adjudication of
  that row, on whichever adjudication path is the one path when this row lands.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`; no
  extra bar is named.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; it names the end of the rollup
  window and the lock refusal.
