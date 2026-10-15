+++
id = "WI-805"
title = "The loop's per-item planning step, the replan at the family swap, and the build-below-planner dial"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-single-plan"
sr_refs = ["SR-154"]
needs = ["WI-804", "WI-799", "WI-913"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-single-plan (ch.3 §4.7-§4.9, §6). A
per-item plan runs by declaration (`planmode = "single"`: plan, gate, critique, at
most one revision; the gate itself is WI-913's, below) and on demand at the second
consecutive CHANGES-REQUESTED, folded into the family swap, as a trial re-measured
after 20 lanes (README Q-6, D-009). The swap follows README A1 step 3: it excludes
the latest build author's session hard and prefers another eligible family; where
only one family may build and plan (this repo) it draws a fresh session of that
family, logged (D-035). The OI-103 Q5 dial `[planning] build_below_planner` ships
false; it applies only to a declared plan made before the first build and is the
one sanctioned exception to "never downgrade a declared route" (README change 16).
LLR-081's ladder gains the replan (change 17). The accepted plan is re-shown in
every rework brief.

Split on 2026-10-14 (review-churn plan, owner ruling 9; the attended-coordinator
handoff's queue row G): the declared plan's gate is WI-913, filed with its own
`needs`. WI-913 carries the in-lane plan after the claim, the planner brief
(`prompts/plan-single.template.md`), the cross-family critique, the one revision,
the dispute sitting or the owner at the cap, the pass record, and the commit-time
gate that holds a `single` row's build until its plan passes. This row keeps the
loop's side: the loop's planning step for a declared row, writing WI-913's record
so that WI-913's gate releases the loop's build; the replan; the dial; and the
rework brief. WI-853 has landed (its shared findings step is what the replan
calls), so it leaves `needs`, and WI-913 joins it.

## Done-when

- The loop runs a declared row's planning step in its lane before the row's first
  build (`PLANNING.SINGLE`, from WI-799's provider), through `ask`'s `plan` and
  `plan-critique` kinds (WI-804), with WI-913's planner brief, revision cap and
  pass record. The loop's build dispatch asks WI-913's predicate beside the
  Done-when hold, so a lane WI-913's gate would refuse holds before a build
  session launches.
- The replan's gate runs `plan_coverage.py --item <spec> --findings <review>`
  through WI-853's shared findings step, and the build is refused until every
  `F#` is covered or excluded with a reason: WI-913's gate holds the rework build
  until the replan's record binds the replanned plan.
- CR CR yields one replan by the swapped (or, under A1, fresh same-family) session,
  and a third CR tiers up.
- Dial on: a strong-planned row builds medium with a recorded `tier-reason`; dial
  off: unchanged. Escalation still tiers up.
- `adjudicate-disposition.template.md` names `planmode = "single"`;
  `docs/knowledge/effort-tiering.md` and `co-planning.md` are amended.
- Each spine row the README matrix gives this row (SR-154's dial amendment, after
  WI-801's in `needs` order, its planning half being WI-913's; LLR-081 and TC-084,
  shared with WI-801; a new LLR and TC under SR-154 for the dial) is amended or
  added and passes adjudication of that row, on whichever adjudication path is the
  one path when this row lands.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`; no
  extra bar is named.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; a new dial (default false).
