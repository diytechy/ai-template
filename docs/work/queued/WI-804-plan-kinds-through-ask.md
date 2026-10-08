+++
id = "WI-804"
title = "Plan kinds through the entry point, with selection by the drafters"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-plan-kinds"
sr_refs = ["SR-222", "SR-155"]
needs = ["WI-801", "WI-803"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-plan-kinds (ch.3 §4.2-§4.4, §6). The plan
runner stops drawing routes (`planner_pair`, `planner_fallback`, the ambient
template) and calls `ask` for `plan`, `plan-dual` and `plan-critique`, routed
through README A1's per-kind table (D-032, D-033). No arbiter model call: by README
Q-5 (a), each drafter selects after revision; agreement adopts, and a mutual
self-select PAGEs to the owner. The losing drafter's concession is a second
recorded independence exception (README change 15). `plan_round`'s `arbiter` stage
becomes `select` (`STEP_SELECT`), and `state.json` is persisted after every record
so a resumed round does not re-spend. A dual round that cannot draw two families
parks (README "Decided here"; risk 7). LLR-072 retires (README matrix, resolved).

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- A fixture round makes no direct `session_service.call` or `planner_pair` call.
- A one-family pair parks.
- Agreement adopts; a mutual self-select PAGEs.
- An interrupted round resumes from `state.json` without re-spending.
- `prompts/dual-plan-arbiter.template.md` is retired, and
  `dual-plan-planner.template.md` gains select mode and the `Tier` column (its
  `Excludes:` line landed with WI-803); `planner_pair`/`planner_fallback` are gone.
- Each spine row the README matrix gives this row (LLR-070/071/076, IF-058, IF-066
  amended; LLR-072 retired; SR-222 and LLR-269 for `_dp_session`, shared) is
  amended or retired and passes adjudication of that row, on whichever adjudication
  path is the one path when this row lands.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`; no
  extra bar is named.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; the arbiter template retires.
