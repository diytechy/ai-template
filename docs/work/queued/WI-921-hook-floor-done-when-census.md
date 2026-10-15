+++
id = "WI-921"
title = "The shipped commit hook holds a hand close on an unblessed Done-when change, and no built-in check step goes unclassified for the commit floor"
workstream = "process"
sr_refs = ["SR-156", "SR-019"]
specref = "docs/archive/work/complete/WI-841-done-when-blessed-in-lane.md#deliverable"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "none"
needs = ["WI-913"]
+++

## Context

Filed on trunk on 2026-10-15 by the attended coordinator, from a planner's
draft, as row 1 of the 2026-10-15b handoff's queue.

WI-841's Deliverable makes a hand close one of the Done-when blessing's hold
points ("the `done-when-blessed` hook step"). Approved LLR-309 says the
pre-commit step invokes the staged-close arm. The step is registered in
`check.py`, but the shipped hook never runs it, for two reasons:

- its batched `--run-steps` floor omits the step;
- a built-in step cannot carry a path trigger (`extra_steps` refuses a
  `[step:]` section that shadows one).

The step reads the index, so in any full `check.py` plan, CI's included, it
has nothing to judge. This repository lands by hand, so WI-841's close hold
has never held a landing. WI-913's round-3 builder found the gap (wi-913
D-005; recipes §6, last bullet). WI-913 fixed the same gap for its own
`plan-gate` step, with a test that drives the hook's own step list.

The class is a registered step that no commit runs. Of the 38 built-in steps
on trunk since WI-913 landed:

- 21 are in the floor, `plan-gate` among them;
- `format` runs by name;
- 15 do not run at commit: six for a reason the kit's text states, and nine
  under only the hook header's general rule;
- `done-when-blessed` is the one gap.

The table and the search that found them are in the planner's notes, kept in
the coordinator's 2026-10-15 scratch root. Ruling 1 asks for
construction first: this row closes the class with a census and fixes the
instance. It is a mechanism change, so it lands alone (revision 37).

**Blast radius.** Armed, the step judges only a commit that moves a claimed
spec out of `docs/work/active/<branch>/` into a closed folder. That means this
repository's landing commits and a lane's own partial close.

- **Trunk's history.** Replayed read-only over trunk's last 400 first-parent
  commits (to `323930653`), the step would judge 47 closes and hold one:
  WI-847's landing (`d0a4b6237`). WI-886 later adjudicated that Done-when
  edit by hand.
- **Open lanes.** None is held as it stands. wi-798 and wi-914, and the
  empty wi-911, wi-912, wi-915 and wi-916, carry their claimed Done-when
  unchanged. wi-902's tip carries its pre-reshape text, but the difference is
  trunk's own amendment (`f200e285b`, `aac06695e`), which a squash or the
  planned re-cut takes.
- **What a lane owes.** A lane that changes its Done-when owes an accepted
  done-when verdict, or an owner ruling `done_when = "<digest>"`, before its
  landing commit. For a `single` row (WI-902, WI-911, WI-912, WI-915 and
  WI-916 are claimed so) that includes an adopted plan critique that changes
  what the row promises (WI-913 deliverable 5).

## Deliverables

One lane, one landing.

1. **The floor** (shipped; RESYNC entry). In `project-trajectory/hooks/pre-commit`,
   `done-when-blessed` joins the batched `--run-steps` floor. The floor's
   comment block gains its entry:
   - it reads the index;
   - it refuses a staged close whose changed Done-when no accepted verdict or
     owner ruling binds;
   - the commit that edits the Done-when is never refused;
   - the merge slot asks the same of the branch.

   This repository's `.githooks/pre-commit` delegates to the shipped hook and
   is unchanged.
2. **A test that drives the hook's own step list** (this repository's tests).
   - It reads the floor off the shipped hook's command line, as WI-913's
     `test_the_shipped_hooks_floor_refuses_an_unplanned_build` does, and runs it
     on `tests/test_done_when_blessing.py`'s lane fixtures.
   - A staged close with an unblessed Done-when change fails
     `done-when-blessed`, a covering verdict releases it, and the commit that
     edits the Done-when passes.
   - In a bootstrapped scaffold, the scaffold hook's floor resolves every name
     and passes on a clean tree.
3. **The census, this row's construction** (this repository's tests).
   - One in-process, smoke-tier test classifies every built-in step (the
     names `check.steps()` returns, which `tests/test_stack_profile.py`
     already pins inside `BUILTIN_STEP_NAMES`) as exactly one of: in the
     hook's batched floor; run by the hook by name (`format`); or listed as
     not run at commit, with a one-line reason.
   - Each reason cites where the kit states it: the hook header's gate-scoped
     rule, the floor rule at `trajectory-map`, ruling 6, or the step's own
     comment. Where no text states it, the builder writes the reason they
     confirm from the step.
   - It fails on a step in none of the three classes, a name in two, or a
     listed name that is not a step. One helper reads the hook's command line.
   - It records today's classification and moves no step except
     `done-when-blessed`. A step whose reason the builder cannot confirm goes
     to the coordinator and stays where it is.
4. **`RESYNC_PACK.md`**, one entry:
   - the hook runs `done-when-blessed`;
   - the hook and `check.py` are a set (§2.3), with `integrate.py` and
     `kitlib.done_when` at WI-841's version or later;
   - a hand close whose changed Done-when no verdict or owner ruling binds is
     now refused at commit, as the merge slot already refuses it;
   - the step changes nothing in a repository that never claims into
     `docs/work/active/<branch>/`;
   - no forced migration.

## Done-when

- The shipped hook's batched floor runs `done-when-blessed`, and its comment
  block describes the step.
- The hook-driven test (deliverable 2), its scaffold case included, fails on
  trunk's hook before the change and passes after.
- The census (deliverable 3) runs in the smoke tier, and fails before the
  change, naming `done-when-blessed` as unclassified. It passes after, and a
  test case each shows that an unclassified step, a name in two classes and a
  listed name that is not a step fail it.
- `RESYNC_PACK.md` carries the entry, anchored at the landing's parent.
- The change's trace rows are authored in the lane and, where their text
  changes, sat at its checkpoint:
  - TC-325 gains the hook-driven case;
  - TC-019 gains the census;
  - LLR-019 states the floor-membership rule only if the sitting asks;
  - LLR-309 already names the hook step and needs no change.
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, and `trace.py --strict` with no
  finding beyond LLR-292's, or none once WI-914 has landed.

## Scope answers

- **S1:** two parts could land alone: the floor edit with its test and entry
  (1, 2 and 4), and the census (3). They stay together, because the census is
  this row's answer to the class and the floor edit is the one change it
  demands. Landed alone, the floor edit leaves the next registered step to
  repeat the gap. If the critique splits them, the floor edit lands first.
- **S2:** no new authority, so no `## Trust` section. Approved LLR-309 already
  makes the pre-commit step a hold point. The hold's carrier is an accepted
  done-when verdict, or an owner ruling that binds the digest. This row only
  makes the shipped hook run the step that row describes. The carrier, its
  producer, its readers and its ruling per input are LLR-307's, unchanged:
  - an absent claim releases;
  - an unreadable claim or current copy holds, naming why;
  - a failed, pending, unbound or other-class verdict covers nothing;
  - an owner entry the owner has not ruled on covers nothing.
- **S3:** the census's input space is the built-in step set, a closed one:
  the names `steps()` returns, all inside `BUILTIN_STEP_NAMES` and equal to it
  today, 38 on trunk. Each name falls in exactly one of three classes; by
  default a name in none fails the census. The step's own input, the staged
  closes, comes through LLR-307's closed reader, unchanged.
- **S4:** `none`. The row has no Trust section, touches one interface seam (the
  hook's floor list; IF-134 and IF-040 are unchanged) and no open input space,
  and two cheap tests, the floor driver and the census, specify the whole
  diff. If the critique asks for a Trust section, the criteria make the row
  `single`.
- **Architectural delta:** one. The hook's exit now depends on an input it
  never read: the staged close and its blessing. LLR-309 already declares that
  input at this hold point. That is within scope; no state, domain value or
  boundary is added, and no preparatory refactor is needed.
- **B3 and B4:** the step trusts the verdict or ruling that was bound by digest
  when it was written, and recomputes nothing from history. No Done-when item
  needs an owner act or credential.
- **Dependencies:**
  - `needs = ["WI-913"]`, met: WI-913 landed (`b803dd019`) and put
    `plan-gate` in the same floor line, so the census counts it there.
  - No third-party dependency.
  - With WI-922 this row shares no script. Both rows edit the shipped hook
    (this row its floor line and a new comment entry, WI-922 the `plan-gate`
    entry) and each adds a `RESYNC_PACK.md` entry, so whichever lands second
    rebases. This row lands first.

## Calls ruled at filing

The owner ruled the drafter's one call in session, as recommended (2026-10-15).

- **Q1: the census, not a derived floor.** In a derived floor, each step
  would declare whether it runs at commit, and the hook would call a new
  `check.py` flag instead of naming steps. That removes the hand list but
  costs a new field in the step tuple (33 `steps()` call sites in 14 files),
  a change to IF-040's contract and to the shipped hook's command line, and
  updates to six test modules that parse that line. The census closes the
  class at a fraction of that, and adopters re-sync one hook line.
