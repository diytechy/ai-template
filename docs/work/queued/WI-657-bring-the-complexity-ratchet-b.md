+++
id = "WI-657"
title = "Code-quality sensors: bring the complexity ratchet back to green, add the flag-axis measure, ship the sensor's opt-in layer and skill, and research duplicated-stage detection (OI-68, S14)"
workstream = "quality"
specref = "project-trajectory/scripts/check_complexity.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
needs = ["WI-538"]
supersedes = "WI-539;WI-623;WI-624"
+++

## Context

**State after the 2026-09-27 integration (wave-4 ruling 13): only part 4 remains.** Parts 1 to 3 landed on trunk in the commit after f7885a49, reviewed SOUND by Codex Sol (`docs/reviews/2026-09-27-wave4/sol-wi657.md`, `sol-wi657-fix.md`). Part 1 brought `check_complexity.py --mode enforce` back to green: three growths reduced, improvements re-stamped down, moved rows re-pointed, trunk debt stamped with reasons. Part 2 is the flag-axis measure (WI-623; Drafted LLR-261, TC-256, IF-239, IF-240). Part 3 is WI-539's shipping. The Done-when lines of WI-657, WI-623 and WI-539 below are met by that commit. What remains is WI-624's research write-up (its quoted Done-when): a result under `docs/plans/` with the ground-truth set, each method's recall and noise, and a recommendation, adopting no detector. The builder's finding for whoever takes it: the per-commit bar missed the ratchet's drift because `[step:complexity]` is declared `from-stage = DevStg-Impl` while the derived stage is DevStg-Tests, and no hook step runs the census. Selecting the step at the repository's actual stage, or in the hook, is a candidate for this row's close or for WI-679's sibling doctrine.

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-539 (Ship the complexity sensor's opt-in layer, structural-move commit rule and deep-module-design skill (OI-68 phase 3)), WI-623 (Report a flag-axis count: functions taking two or more boolean parameters, and bool-literal call sites (S14)), WI-624 (Research duplicated-stage detection: call-sequence and near-miss methods, measured against past consolidations (S14)). All four are the complexity and readability sensors (`check_complexity`, `check_readability`, `check_dupes_census`): the ratchet must be green before a new measure lands beside it, the shipping item documents the sensors downstream, and the research measures the next detector against the same census. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

Order: the ratchet first (it is red at every gate run), then WI-623's measure, then WI-539's shipping, then WI-624's research write-up. (WI-539's PROCESS.md and PROCESS_OPTIONS.md edits landed with parts 1 to 3, so the part left no longer shares the doctrine sitting's files; the WI-689 consolidation verdict noted the stale concurrency warning this replaced.)

`check_complexity.py --mode enforce` fails at b14d1808, so the
`[step:complexity]` step is red at any gate run. It first failed at 76a235bb.
Three kinds of finding:

- growth: `route_session` cognitive 37 -> 38, `trace.load_registries` 39 ->
  42, and a new unbaselined `tests/test_bookkeeping._whole_tree_git_calls`
  (25) (measured at HEAD by the backlog audit);
- improvements the ratchet wants re-stamped downward in the commit that made
  them (for example `agent_loop.run_iteration` 18 -> 16,
  `baseline_snapshot.refresh_ledger` 23 -> 21, `dispatch._advance` 20 -> 18);
- rows whose function is gone from the path the baseline names
  (`integrate._claim_refusal`, and the `traj_graph.py`, `traj_panels.py`,
  `traj_render.py` and `traj_views.py` rows left behind when those modules
  moved under `rendering/`).

IN SCOPE: re-stamp the improvements downward; re-point or delete the rows
whose function moved or went; for each growth (`route_session`, `load_registries`,
`_whole_tree_git_calls`), either reduce it or re-stamp it upward with a reason a reader can argue with, and record
which in the log. Find why the per-commit bar did not catch the drift (the
ratchet test's tier, or a step the bar skips) and say so in the Deliverable.

NOT IN SCOPE: refactoring other functions to lower their numbers.

## Done-when

- `python project-trajectory/scripts/check_complexity.py --mode enforce`
  passes at the landing commit, and the Deliverable pastes its output.
- Every upward re-stamp carries its reason at the baseline entry.
- The commit bar passes.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-539 (Done-when, verbatim)

- `PROCESS_OPTIONS.md` has the "Complexity ratchet" section and its
  Applies-when index row in document order, and the section names the shipped
  report step and census as the way to arm it.
- `PROCESS.md` §3 has the structural-move bullet between the 0→A→B bullet and
  Thin orchestrators, and both watched docs' byte deltas are flagged with a
  reason and re-stamped in `byte-budget-guard` (source and tracked copies).
- The `deep-module-design` skill is under `project-trajectory/skills/`,
  `INDEX.csv` is regenerated, `gen_skills_index.py --check-agents` passes, and a
  scaffold bootstrapped from the kit carries the skill byte-identical to its
  source.
- `RESYNC_PACK.md` has an entry for the layer and the skill, and the commit bar
  passes.

### From WI-623 (Done-when, verbatim)

- A stdlib check reports, per module, the functions taking two or more boolean
  parameters and the call sites passing boolean literals, with totals.
- It never fails a gate, even under `--strict`; its baseline sits beside the
  census's, downward-only by convention.
- Tests pin a two-flag function, a one-flag function (not counted) and a
  boolean-literal call site.

### From WI-624 (Done-when, verbatim)

- A written result under `docs/plans/`: the ground-truth set, each method's
  recall and noise on it, and a recommendation for the owner.
- Any prototype stays out of the gate and the commit bar.
- No detector is adopted by this item; adoption is the owner's ruling on the
  result.
