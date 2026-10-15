+++
id = "WI-914"
title = "Review-churn batch 2: the strict lints run in every build round's commit bar, before every sitting and at every landing, from a clean trunk"
workstream = "process"
sr_refs = ["SR-054", "SR-157"]
specref = "docs/plans/2026-10-11-review-churn/README.md#6-run-the-strict-lints-after-every-build"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "none"
needs = ["~WI-911"]
+++

## Context

Filed on trunk on 2026-10-14 by the attended coordinator as the review-churn
program's batch row B2 (`docs/handoff-2026-10-11-attended-coordinator.md`,
the queue table): plan item 6. Ruling 6 of 2026-10-11 is the spec of record,
and this row cites it rather than restating its reasons. `trace.py --strict`
and `check_trajectory.py --strict` run in the commit-bar command after each
build round, in the closure check before a sitting, and in the landing check.
They never run in the pre-commit hook.

B2 is split at filing under S1. This row is item 6's first proposal: clear
trunk's last strict-lint finding, then keep trunk at zero at the three
boundaries. The RESYNC-presence check is WI-916, which needs this row. It
carries item 6's second proposal and K4's retirement from its third.

Trunk's only strict-lint red is LLR-292's Detail: `trace.py --strict` exits 1
on "uses 'minimal' — no test can settle it". `check_trajectory.py --strict`
has been clean since 45d867e51.

## Deliverables

One lane, one landing.

1. **LLR-292, amended** (this repo's registry).
   - **The clause.** The Detail ends "no claim is made that crossing count is
     minimal". That is a scope exclusion, not a claim: the T8 critique keeps
     "crossings minimized" as its judged residue
     (`docs/rubrics/dashboard-usability.md`, T8).
   - **The amendment.** It names the measurable the clause refers to, the
     number of perpendicular crossings, and says the row sets no bound on it.
     For example: "Perpendicular crossings remain under the T8 critique; this
     row sets no bound on their count". The obligation is unchanged, and
     SR-054 and TC-305 are untouched.
   - **Sitting and act.** The lane's spine author drafts the amendment and an
     amendment sitting judges it. Its act re-attests LLR-292 as the lane's
     last spine commit; LLR amendments sit above `human_approval_through`.
     The act takes trunk's next seq, 113 at filing. B4 decides the acts
     WI-902's lane holds.
2. **The commit-bar command** (this repo's own; no RESYNC entry).
   - **`docs/stack.ini` `[run] smoke`** is the one declared bar command ("the
     per-commit bar"). It runs, in order: the smoke tier, `trace.py --strict`,
     `check_trajectory.py --strict`, `check_docs.py --root . --stale`, and
     then the budget check. `check_docs --stale` is session-protocol §3's
     third bar line, which this command lacks today. Running the budget check
     last means a breach under parallel-lane load never hides a lint red, and
     the timed run is unchanged. Its `.desc` says so.
   - **The bar's homes name that one command** instead of restating its parts
     (`run.cmd smoke`; `run_menu.py smoke` from a shell), so a build round's
     bar cannot skip the lints:
     - `CLAUDE.md`'s per-commit bar (byte-capped: run `byte-budget-guard`
       before and after);
     - `session-protocol` §3;
     - `coordinator-cycle` recipes §6.

     Both skills are `scope: this-repo`; their synced copies follow.
   - **The builder brief.** `.claude/agents/kit-builder.md` adds
     `trace.py --strict` beside the `check_trajectory.py --strict` it already
     runs. The builder runs its tests at `-n 2`, not through the launcher.
   - **The Terra brief.** `scripts/coordinator/terra-spine-prompt.template.md`
     already runs both lints. It drops its line calling LLR-292's finding
     pre-existing.
3. **The closure check** (shipped: RESYNC entry).
   - `project-trajectory/skills/spine-authoring/references/in-lane.md`, "Close
     the edges before the sitting": `trace.py --strict-integrity` becomes
     `trace.py --strict` from DevStg-Impl. Below that rung,
     `--strict-integrity` stands in, because an SR still lacking its LLR or TC
     is the rung's own open work. That is also why the harness's traceability
     step starts at DevStg-Impl.
   - Recipes §1, "Closure checks", names both strict lints.
4. **The landing check** (recipes §3; this repo's hand landing). The landing
   commit runs the bar command on the staged squash. That replaces the
   separate `trace.py --strict-integrity` and `check_trajectory.py --strict`
   lines. The shipped merge slot is unchanged: its refresh's bar
   (`check.py --tier all` at the derived stage) already runs both strict
   forms from DevStg-Impl.

The pre-commit hook does not change.

## Done-when

- LLR-292's Detail names the measurable in place of "minimal", and an
  amendment sitting's act re-attests it. SR-054 and TC-305 are unchanged.
- **The commit bar matches deliverable 2:**
  - `[run] smoke` runs the smoke tier, both strict lints,
    `check_docs --stale` and then the budget check, in that order;
  - `CLAUDE.md`, `session-protocol` §3 and recipes §6 name it as the commit
    bar;
  - the builder and Terra briefs read as deliverable 2 states;
  - `CLAUDE.md` stays within its byte budget;
  - the skill copies match their source (`bootstrap.py --dest . --sync`).
- The closure check (`in-lane.md`, recipes §1) and the landing check (recipes
  §3) read as deliverables 3 and 4 state.
- Nothing under `project-trajectory/hooks/` changes.
- `RESYNC_PACK.md` carries one entry for `in-lane.md`'s closure check. It is
  anchored at the landing's parent and forces no migration.
- The row lands only after the phase-0 baseline manifest is committed on
  trunk (the plan's revision 37; the handoff's row M).
- The bar is green on the landing tip: `run.cmd smoke` exits 0, the smoke
  tier is within its budget, and `trace.py --strict` reports no finding.

## Scope answers

- **S1:** one deliverable set, kept together. The bar this row adds is red
  until LLR-292's act, so the amendment lands with it. The RESYNC-presence
  check is independently landable and is WI-916, which needs this row.
- **S2:** no file gains authority over a hold, an act or a gate. The two lints
  read the registries that already gate the harness from DevStg-Impl
  (SR-157). This row runs them at more of this repo's boundaries, and the act
  is the ordinary amendment act. No Trust section.
- **S3:** no promise over an input space: two named lints, three named
  boundaries, and the harness's own rung condition.
- **S4:** `none`. There are no script changes and no interface seam: IF-049's
  `[run]` format is unchanged, and only this repo's value of one line
  changes. There is no Trust section and no input space; the rest is text and
  one spine amendment. It does not wait for the plan gate.
- **Architectural delta:** within scope. The verdicts of the commit bar, the
  closure check and the landing check gain the two lints' exit codes as
  inputs. The bar also gains `check_docs --stale`, already in
  session-protocol's bar. No state, domain value or boundary is added, and no
  preparatory refactor is needed.
- **Dependencies:**
  - `~WI-911`, soft. This row lands after WI-911: every later row's critique
    and review run under its rules, and both rows edit the
    `coordinator-cycle` recipes and the Terra brief. It may be built beside
    it.
  - The baseline-manifest hold is a Done-when bullet.
  - No third-party dependency.
  - It does not wait on B4 (WI-902).
