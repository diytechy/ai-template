+++
id = "WI-805"
title = "Per-item planning, the replan at the family swap, and the build-below-planner dial"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-single-plan"
sr_refs = ["SR-154"]
needs = ["WI-804", "WI-799", "WI-853"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-single-plan (ch.3 §4.7-§4.9, §6). A
per-item plan runs by declaration (`planmode = "single"`: plan, gate, critique, at
most one revision) and on demand at the second consecutive CHANGES-REQUESTED,
folded into the family swap, as a trial re-measured after 20 lanes (README Q-6,
D-009). The swap follows README A1 step 3: it excludes the latest build author's
session hard and prefers another eligible family; where only one family may build
and plan (this repo) it draws a fresh session of that family, logged (D-035). The
OI-103 Q5 dial `[planning] build_below_planner` ships false; it applies only to a
declared plan made before the first build and is the one sanctioned exception to
"never downgrade a declared route" (README change 16). LLR-081's ladder gains the
replan (change 17). The accepted plan is re-shown in every rework brief.

## Done-when

- A single row builds only after a gated, critiqued plan.
- The replan's gate runs `plan_coverage.py --item <spec> --findings <review>`
  through WI-853's shared findings step, and the build is refused until every
  `F#` is covered or excluded with a reason.
- CR CR yields one replan by the swapped (or, under A1, fresh same-family) session,
  and a third CR tiers up.
- Dial on: a strong-planned row builds medium with a recorded `tier-reason`; dial
  off: unchanged. Escalation still tiers up.
- `prompts/plan-single.template.md` is added; `adjudicate-disposition.template.md`
  names `planmode = "single"`; `WI-000.template.md` documents `"" | single | dual`;
  `docs/knowledge/effort-tiering.md` and `co-planning.md` are amended.
- Each spine row the README matrix gives this row (SR-154's planning and dial
  amendment, second in `needs` order; LLR-081 and TC-084, shared with WI-801; a new
  LLR and TC under SR-154 for the dial) is amended or added and passes adjudication
  of that row, on whichever adjudication path is the one path when this row lands.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`; no
  extra bar is named.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; a new dial (default false) and
  a new prompt.
