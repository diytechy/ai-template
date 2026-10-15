+++
id = "WI-921"
title = "The shipped commit hook holds a hand close on an unblessed Done-when change, and no built-in check step goes unclassified for the commit floor"
workstream = "process"
sr_refs = ["SR-156", "SR-019"]
specref = "docs/archive/work/complete/WI-841-done-when-blessed-in-lane.md#deliverable"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
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

**The step itself fails open on this repository's two-commit landing**
(found while answering the scope critique's S2; owner ruling, 2026-10-15, in
session: fixed in this row). On trunk the step reads the claim copy at HEAD
(`integrate.staged_done_when_refusal`), assuming trunk's copy is the one
claimed. The `coordinator-cycle` recipes' two-commit landing (recipes §3,
"land two commits: the squash up to the commit before the close, then the
close") breaks that assumption. Its first commit stages no close, so it is
not judged, and it writes the lane's Done-when edit into trunk's claim copy.
The close then compares the edit with itself and passes. WI-835's landing
has that shape: squash `181ec9001`, then close `dc0333a32`, whose Done-when
digest no verdict or ruling covers. The same step also reads an index delta
git cannot list as no close.

**Blast radius.** Armed, the step judges only a commit that moves a claimed
spec out of `docs/work/active/<branch>/` into a closed folder. That means this
repository's landing commits and a lane's own partial close.

- **Trunk's history.** Replayed read-only over trunk's last 400 first-parent
  commits (to `323930653`), the step as it stands would judge 47 closes and
  hold one: WI-847's landing (`d0a4b6237`). WI-886 later adjudicated that
  Done-when edit by hand. Deliverable 5 also holds WI-835's two-commit
  landing, at its squash `181ec9001`.
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
     owner ruling binds, and a trunk commit that changes a claim copy's
     Done-when unblessed (deliverable 5);
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
     now refused at commit, as the merge slot already refuses it, and so is a
     trunk commit that changes a claimed row's Done-when unblessed, whether
     it is a landing's first commit or a trunk amendment;
   - the step changes nothing in a repository that never claims into
     `docs/work/active/<branch>/`;
   - no forced migration.
5. **The step judges the commit that first carries a Done-when change onto
   trunk** (shipped, same entry; owner ruling, 2026-10-15).
   - A commit made on trunk that changes the Done-when of a claim copy under
     `docs/work/active/<branch>/`, closing it or not, is judged against its
     parent like a close: it holds unless its own tree carries a covering
     accepted verdict or owner ruling. The two-commit landing is then held at
     its first commit, and its close compares against a blessed copy.
   - The reading is computed from the commit being made and its parent,
     never by searching history for a claim commit (B3; enforce at the
     commit).
   - A read the step cannot complete, the index delta included, holds,
     naming why: deny by default, as IF-286's contract already says of an
     unreadable tree.
   - A commit on the claim's own branch keeps today's lane reading. A close
     made off trunk and off the claim's branch (a detached HEAD or an alias
     in a lane's worktree) is WI-922's identity class, and the landing
     re-judges it.

## Trust

Deliverable 1 gives existing files authority over a hand close at commit.
Armed, the hook refuses a staged close whose changed Done-when is bound by
neither an accepted done-when verdict, with its acceptance binding, nor an
owner ruling. All three are files on disk, and the verdict is model output
(`project-trajectory/PROCESS.md` §3, "When a guard is owed"). Deliverable 5
gives them the same authority over a trunk commit that changes a claim
copy's Done-when.
LLR-307 and LLR-309 state the reader's rulings; they are cited here, not
restated.

- **Carriers.**
  - **The verdict:** a file under `docs/reviews/` holding one
    `DONE-WHEN: CLARITY|BLESSED|SUCCESSOR changes=<n> digest=<digest>` line,
    alone in a `done-when` verdict or in the `## done-when` section of a
    `combined` one. Its one parser is `kitlib.sitting.parse` (LLR-308,
    LLR-310).
  - **The acceptance binding:** `<verdict>.requested`, three lines:
    `brief = <class>`, `kinds = <kind>;…` and
    `outcome = pending|accepted|failed` (`kitlib.sitting.read_requested`,
    LLR-310).
  - **The owner ruling:** a `[decision.D-<n>]` entry in
    `docs/decisions/<run>.toml` (IF-255) carrying `done_when = "<digest>"`
    and `owner = "confirmed"` or `"overruled"`.
  - **What owes a blessing:** the claim copy under
    `docs/work/active/<branch>/`, written by `integrate.py claim`, compared
    with the copy the commit closes.
- **Producers and write routes.**
  - The adjudicator writes the verdict, copying the digest that
    `adjudicate_brief.py` renders (`kitlib.done_when.digest`). The coordinator
    launches it from the lane with `coordinator_adjudicate.py adjudicate`
    (LLR-306) and commits it there; the loop launches its own.
  - The route that ran the call writes the binding through
    `kitlib.sitting.write_binding`: `pending` before the call, then
    `accepted` or `failed` from `adjudicate_brief.record_outcome`, committed
    alone in a `telemetry:` commit (LLR-310).
  - No script writes the owner ruling. The refusal names the line to write
    (`kitlib.done_when.hold_reason`). The coordinator writes the entry in the
    lane, and the owner sets `owner` in place (IF-255).
- **Failed-write shapes.** None of these releases anything.
  - A failed, timed-out or error-reporting call, an empty reservation and a
    verdict the grammar refuses are each recorded `failed` (LLR-306).
  - A binding that cannot be reserved refuses the launch (exit 2). A call
    interrupted after launch leaves `pending`. A vetoed telemetry commit
    leaves the binding unstaged, since `agent_common.commit_telemetry` is
    best-effort. A partial binding reads as no binding, or as not accepted.
  - A decisions file that does not parse is skipped. A record not staged or
    committed is not in the tree a hold reads.
- **Consumers.** One reader, `project-trajectory/scripts/kitlib/done_when.py`
  (`covering`, `blessing_owed`, `lane_hold`, `staged_closes`; IF-286). It
  reads a verdict only through `kitlib/sitting.py`'s `accepted_at`. Four code
  paths ask it:
  - **The hook step** (new here). `check.py`'s `done-when-blessed` runs
    `integrate.py done-when-hold` (`staged_done_when_refusal`) on the index.
    A hold exits 1 (`integrate.fail`); a crash or a missing script exits
    non-zero as well. `check.py` reports either as FAIL, and the hook refuses
    the commit. The step never skips: it needs no module or tool, and it is
    not a trunk-freshness step.
  - **The merge slot.** `integrate.py` `_merge_refusal` → `_done_when_refusal`
    reads the branch tip against the claim at trunk's HEAD. A hold refuses
    the merge.
  - **The loop's build hold.** `agent_loop.py` `routed_session` →
    `build_hold` reads the lane's HEAD against the claim at its integration
    base. A hold ends the worker `HELD`.
  - **The merge-time mint.** `intake.py` `_done_when_drafts`, from
    `intake_after_merge` or `sweep --merged` after a hand landing, reads the
    merged trunk. A cover mints nothing but a SUCCESSOR verdict's own drafts,
    and a SUCCESSOR with no draft refuses; no cover mints the goalposts row.
    It skips, without a word, a closed spec it cannot read or parse from the
    working tree.

  The coordinator acts on the hold through the `coordinator-cycle` skill.
  Other readers of these files take no Done-when part: `acceptance_record.py`
  (approval acts), `plan_gate.py` and `plan_coverage.py` (dispute bindings),
  and `kitlib/decisions.py` with its callers. `plan_gate.py`'s build hold
  binds the Done-when digest through its own pass record and reads neither
  carrier.
- **Ruling per input**, through the one reader (LLR-307):
  - an absent claim releases, and an unreadable claim holds naming why (the
    mint refuses);
  - at the three hold points, an unreadable current copy, or a claimed row
    with no copy, holds naming why;
  - a failed, pending, unbound or other-class verdict covers nothing, nor
    does a malformed one, which the parser refuses whole, or one whose digest
    names another row;
  - an unseen owner entry covers nothing, nor does one carrying the retired
    `reviewed` key, an `owner` outside the two values or a `done_when` that is
    not a string, nor an unparseable file;
  - a tree git cannot read reads as uncovered, so it holds.
- **Where the hook step reads the claim.** On the claim's own branch, at
  the lane's integration base, as today. On trunk, against the parent of the
  commit being made, which deliverable 5 makes sound: no commit can change
  trunk's claim copy's Done-when unblessed, so the copy a close compares
  against is either the claimed text or a blessed change. Residues, each
  stated:
  - a close in a lane's worktree on a detached HEAD, or on a branch not named
    for its claim folder, reads HEAD, which holds the lane's own copy; the
    landing re-judges it (WI-922's identity class);
  - a trunk commit made with the hook bypassed is outside the threat model
    (PROCESS.md §6); the merge slot and the landing sweep's mint still read
    the merged result.
- **What the authority binds to:** the digest, over the work item's id and
  the items the close carries, each claim item that is only ticked or
  evidenced read as that item (LLR-307). It binds neither the claim text they
  changed from, nor the lane, nor the record's path. Covers are read from the
  tree being judged, the index for the hook, so a record only on disk or only
  in history binds nothing. The binding fixes the class and kinds a verdict
  is judged against (LLR-310).
  - Nothing checks who wrote a binding's `accepted` or an entry's `owner`.
    The first is trusted as the route's record, the second by convention
    (`kitlib/decisions.py`). The merge slot and the loop carry that exposure
    today; in a repository that lands by hand, the hook is where it first has
    effect.

This row changes no carrier or producer. It adds the shipped hook as a new
path that runs the registered step, and changes the step's reader in two
places: deliverable 5's trunk arm, and a read it cannot complete, which now
holds.

This ruling goes to the owner to confirm or overrule (`coordinator-cycle` §1).

## Done-when

- The shipped hook's batched floor runs `done-when-blessed`, and its comment
  block describes the step.
- The hook-driven test (deliverable 2), its scaffold case included, fails on
  trunk's hook before the change and passes after.
- The census (deliverable 3) runs in the smoke tier, and fails before the
  change, naming `done-when-blessed` as unclassified. It passes after, and a
  test case each shows that an unclassified step, a name in two classes and a
  listed name that is not a step fail it.
- A test replays WI-835's two-commit landing on a fixture trunk and lane:
  the first commit, carrying an unblessed Done-when edit into trunk's claim
  copy, is held, and passes once its tree carries a covering verdict or
  ruling; a trunk amendment of a claimed row's Done-when is held the same
  way, and one that changes no Done-when is not judged. Each case fails on
  trunk's step before the change.
- A test shows that an index delta git cannot list holds the step, naming
  why, and fails before the change.
- `RESYNC_PACK.md` carries the entry, anchored at the landing's parent.
- The change's trace rows are authored in the lane and, where their text
  changes, sat at its checkpoint:
  - TC-325 gains the hook-driven case;
  - TC-019 gains the census;
  - LLR-019 states the floor-membership rule only if the sitting asks;
  - LLR-309 is amended if the sitting reads deliverable 5's trunk arm as a
    new hold point; LLR-307 if it reads the failed-read hold as new.
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, and `trace.py --strict` with no
  finding beyond LLR-292's, or none once WI-914 has landed.

## Scope answers

- **S1:** two parts could land alone: the floor edit with its test and entry
  (1, 2 and 4), and the census (3). They stay together, because the census is
  this row's answer to the class and the floor edit is the one change it
  demands. Landed alone, the floor edit leaves the next registered step to
  repeat the gap. If the critique splits them, the floor edit lands first.
- **S2:** yes. Deliverable 1 makes the shipped hook run the step that lets
  three existing carriers, an accepted done-when verdict, its acceptance
  binding and an owner ruling `done_when = "<digest>"` on a `docs/decisions`
  entry, authorize or refuse a hand close at commit for the first time, and
  deliverable 5 gives them the same authority over a trunk commit that
  changes a claim copy's Done-when; see `## Trust`.
- **S3:** the census's input space is the built-in step set, a closed one:
  the names `steps()` returns, all inside `BUILTIN_STEP_NAMES` and equal to it
  today, 38 on trunk. Each name falls in exactly one of three classes; by
  default a name in none fails the census. The step's own input is closed
  too: each staged change to a claim copy is a close, a Done-when change
  without a close, or neither, made on the claim's own branch, on trunk, or
  elsewhere. A close or a Done-when change made on trunk is judged against
  its parent (deliverable 5); one on the claim's branch keeps the lane
  reading; one elsewhere is WI-922's identity class and is re-judged at the
  landing; a read the step cannot complete holds.
- **S4:** `single`. The row has a Trust section, and it promises behaviour
  over two input spaces, the built-in step set and the step's staged changes
  (S3); either alone is enough. It touches one interface seam, the hook's
  floor list (IF-134 and IF-040 are unchanged), and the step's reader.
- **Architectural delta:** two, both within scope. The hook's exit now
  depends on an input it never read: the staged close and its blessing, which
  LLR-309 already declares at this hold point. And the step's verdict now
  depends on a trunk commit's Done-when change, not only on a close
  (deliverable 5). No state, domain value or boundary is added, and no
  preparatory refactor is needed.
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

The owner ruled both calls in session, each as recommended (2026-10-15).

- **Q1: the census, not a derived floor.** In a derived floor, each step
  would declare whether it runs at commit, and the hook would call a new
  `check.py` flag instead of naming steps. That removes the hand list but
  costs a new field in the step tuple (33 `steps()` call sites in 14 files),
  a change to IF-040's contract and to the shipped hook's command line, and
  updates to six test modules that parse that line. The census closes the
  class at a fraction of that, and adopters re-sync one hook line.
- **The two-commit landing's fail-open is fixed here** (raised while
  answering the critique's S2, below). Over a successor row (the hole stays
  open between two landings) or a recipe step (a procedure, not a check at
  the commit): this row arms the step, so it arms one that holds. The fix
  judges the commit that first carries the edit, against its parent, never
  by searching history; a trunk amendment of a claimed row's Done-when is
  held the same way (coordinator-2026-10-15 D-003).

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-15; CHANGES-REQUESTED, two findings):

- **S2, MAJOR: adopted.** Arming the hook gives the carriers that release
  the Done-when hold authority over a hand close at commit for the first
  time, and WI-841 never wrote a Trust section. The row gains `## Trust`:
  its carriers ("The verdict", "The acceptance binding", "The owner ruling",
  "What owes a blessing"), their producers and write routes, their
  failed-write shapes ("None of these releases anything"), the one reader
  with its four code paths by path and function, the ruling per input
  through LLR-307, where the step reads the claim, and what the authority
  binds to, with `project-trajectory/PROCESS.md` §3, "When a guard is owed",
  cited. The S2 answer now reads "see `## Trust`". Answering it found the
  two-commit landing's fail-open; the owner ruled it fixed here
  (deliverable 5).
- **S4, MAJOR: adopted.** `planmode = "single"`: "The row has a Trust
  section, and it promises behaviour over two input spaces, the built-in
  step set and the step's staged changes (S3); either alone is enough."
