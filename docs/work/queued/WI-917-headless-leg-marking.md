+++
id = "WI-917"
title = "A headless coordinator leg is a marked autonomous run, and every commit it makes carries the run's Loop-Session trailer"
workstream = "process"
sr_refs = ["SR-209", "SR-208"]
specref = "docs/plans/2026-10-11-review-churn/README.md#owner-rulings-2026-10-11"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-912"]
+++

## Context

Filed on trunk on 2026-10-14 by the attended coordinator as the review-churn
program's phase-1 row P9 (`docs/handoff-2026-10-11-attended-coordinator.md`,
the queue table). The spec of record is the plan's rulings: revision 35's
"The coordinator role" (an autonomous run when headless) and revision 36's
"Headless coordinator legs are marked now". Together they give P9 the marker,
the trailer through the leg prompt and the recipes, and one lane-mode rule
whose re-claim is P9's design. The sitting briefs' trailer line is WI-912's
(its deliverable 4). Where this row and a ruling differ, the ruling governs.

**Two owner rulings, 2026-10-14, in session:**

- **P9 is pulled forward.** It lands right after WI-912, as the queue's fifth
  landing (WI-913, WI-911, WI-914, WI-912, then this row), ahead of WI-916,
  WI-915 and WI-902's rebuild, so the overnight runner is usable sooner. It
  is filed on trunk now with its scope critique, and claimed under its own
  scoped unpause once WI-912 has landed. It is a mechanism change: it lands
  alone, after the cycle has run once through WI-912's act turn.
- **P9 is split.** This row is the marking: the launcher, the leg prompt and
  the skill's procedure, with the lane-mode rule and the re-claim as a recipe
  step. The merge slot's reading of the re-claim is WI-918, which lands
  before WI-808 puts coordinator landings on the slot.

**Today:**

- `scripts/coordinator/overnight_legs.py` runs `claude -p` legs from the
  newest handoff's session prompt and sets no marker, so headless legs ran
  unmarked (the plan's revision 20 check).
- That prompt is the attended one ("Ask the owner at real decision points";
  "Background tasks and notifications are fine here (this is not a headless
  leg)").
- Earlier legs carried a second, headless prompt, copied from handoff to
  handoff. It has already drifted: leg 03's still prescribes narrow rounds.

**Under the marker (`KIT_LOOP_SESSION`):**

- the commit-msg floor, the held-status step and the loop writers' refusal
  arm (SR-209, SR-208);
- a claim made under the marker carries the trailer, which makes the lane a
  loop lane at the merge slot;
- any marked commit one of the loop's own writers makes in the lane's range
  does the same, from that commit on.

A headless leg makes such a commit at every sitting: the entry point's
`commit_telemetry` commits carry the loop-writer subject `telemetry:
session`. So the rule below reads "a lane claimed headless" as a lane a
headless leg marked. This is the coordinator's reading, recorded at filing
as `docs/decisions/coordinator-2026-10-14.toml` D-015.

## Deliverables

One lane, one landing. Each item names its ruling, and the builder writes the
rule in the target's own voice. No shipped file is touched (Done-when).

1. **The launcher marks its run** (`scripts/coordinator/overnight_legs.py`;
   this repo's tooling).
   - **The marker.** Before the first leg, the launcher calls
     `kitlib.provenance.mark_loop_process()` once, in its own process, and
     logs the session. That gives one session per run, inherited by every
     leg and by every process a leg starts. A well-formed inherited marker
     is kept, and a malformed one is replaced, as the function states.
   - **The prompt.** Each leg's prompt is composed of three parts, in order:
     - the newest handoff's session prompt (`coordinator_guard.session_prompt`,
       unchanged);
     - the headless block (deliverable 2);
     - `agent_brief.loop_provenance_note()`, the kit's standing trailer
       instruction, which names the session.

     A block that is absent, unreadable or empty, or an empty note, refuses
     the run before any leg (exit 2).
   - **The audit.** The launcher records the tip of every local branch
     before each leg starts and again after it exits (the binding; see
     `## Trust`). It then judges:
     - every commit the leg added to trunk's first-parent line and to the
       first-parent line of `archive/lanes`, with
       `provenance.loop_trailer_refusal(message, session)`, and trunk must
       still descend from its pre-leg tip;
     - every other branch the leg created or moved, over its range from
       trunk, by the merge slot's own rule: `provenance.loop_lane_window`,
       then the trailer check inside the window, which accepts any
       well-formed session, as the slot does.

     A refusal, or a read it cannot complete, stops the run (exit 3) and
     names the commit or the read. This stop sits beside the launcher's
     existing stops.
   - **The lane check before a landing.** The same lane rule runs as
     `overnight_legs.py check-lane <branch>` (exit 0, or 3 naming the first
     refused commit or the failed read). The skill's headless-leg section
     runs it before a leg squashes a lane, so a lane holding an unmarked
     commit is not landed.
   - **The marker's failure contract under its new producer** (with the
     audit's, in `## Trust`):
     - **Absent from a leg's shell** (the inheritance failed): the block's
       first check ends the leg before any write, and the launcher then
       stops because the leg added no handoff.
     - **A trunk or `archive/lanes` commit without the run's trailer**, by
       whatever route: the audit stops the run, naming the commit.
     - **Malformed and inherited:** it is never passed on, because
       `mark_loop_process` replaces it.
   - The docstring states the marker, the composition and the new stop.
2. **The headless block** (`scripts/coordinator/headless-leg.md`, this repo's
   tooling, linked from the skill's headless-leg section). It is fixed text
   and restates nothing of the session prompt. It says:
   - This session is one headless leg: one turn, ending the reply ends the
     leg, and nobody answers. Where the prompt above says otherwise
     (attended, asking the owner, background tasks or notifications), this
     block governs.
   - Before step 1, `echo "$KIT_LOOP_SESSION"` must print the session that
     the LOOP PROVENANCE line names. If it does not, write nothing and end
     the reply.
   - Follow the skill's headless-leg section (deliverable 3).
   - At close-out, the new handoff's session prompt block is the prompt
     above this block, copied verbatim, never this block or the provenance
     line. `Overnight: stop` is added only when the queue is done or no row
     can move without the owner.
3. **The `coordinator-cycle` skill** (kit source
   `project-trajectory/skills/coordinator-cycle/`, synced to `.claude/skills/`;
   `scope: this-repo`). It gains one headless-leg section, the procedure's one
   home. Recipes §1 (adjudication steps 4 and 7), §3 (landing and archive)
   and §7 ("Background or foreground") point to it.
   - **The trailer on every commit.**
     - Every message ends with the provenance line, inside its final trailer
       block. That includes the landing's message file and an amended
       message (the last trailer wins).
     - So does the archive commit's `commit-tree -F` message, the one
       plumbing commit the coordinator writes itself.
     - The kit's writers add the trailer themselves, and the adjudicator
       gets it from WI-912's line.
     - A step the marker refuses is never re-run unmarked or past a hook.
   - **Foreground only.** Every command runs in the foreground, with an
     explicit timeout up to the launcher's cap. Every Agent call passes
     `run_in_background: false`, and every builder, reviewer and planner is
     told to run its commands in the foreground.
   - **Owner-held steps.** A leg never takes a step only the owner can take.
     These are:
     - an act the marker refuses (a status move on a held rung);
     - an ESCALATE ruling;
     - an open item's ruling;
     - a Done-when item that needs an owner act or credential;
     - a push or a merge to main.

     Any other step that the prompt's Never list or skill §5 reserves to the
     owner is treated the same way. For each such step, the leg:
     - brings the lane to a safe committed point;
     - records the step and its evidence (the verdict, the rows, the
       command) in the lane's decisions record and under the new handoff's
       "For the owner";
     - turns a decision only the owner can make into a pending open item
       that the row's `needs` cites (§5, unchanged);
     - moves to the next row.

     When no row can move without the owner, the leg closes out with
     `Overnight: stop`. A Codex limit is answered with `Resume-not-before:`,
     as the launcher reads it.
   - **The lane-mode rule**, stated once. A lane that a headless leg marked
     (its claim, or a commit one of the loop's own writers made in its range
     under the marker, a sitting's telemetry commit included) lands
     headless. Otherwise, the attended coordinator re-claims it before its
     own first commit there, its sittings' verdict and act commits included.
   - **The re-claim recipe step.** The attended, unmarked coordinator writes
     an empty commit in the lane with the subject `reclaim: <branch>
     (attended)` and no trailer. The recipe also says how to place a missed
     re-claim before the first attended commit.
     - **Until WI-918 lands, nothing reads that commit, and nothing needs
       to.** Coordinator landings are hand squashes, which never run the
       merge slot's trailer rung.
     - **The recipe is the subject's one home** until WI-918 moves it into
       `provenance.py`, before WI-808 puts landings on the slot.
   - **A leg's landing.** A leg squashes a lane only after `check-lane`
     passes on it. Until WI-918 lands, a leg leaves a lane holding a
     re-claim to the attended session: the lane rule does not read
     re-claims yet, so the lane's attended commits would refuse the check.

## Trust

Written before the claim, answering S2 under `project-trajectory/PROCESS.md`
§3, "When a guard is owed" (the round-1 scope critique). The ruling goes to
the owner to confirm or overrule (coordinator-cycle §1 and §5).

**The gate.** The launcher's after-leg audit decides whether the next leg
starts, and `check-lane` decides whether a leg lands a lane (deliverable 1).
Both read the refs a leg may move and the commits it adds. Neither releases
anything a run would otherwise refuse: a pass only lets the next leg start
or the landing proceed, as every leg and landing did before this row.

**Producers and write routes.**

- **The commits:** the leg's processes write them by porcelain (under the
  commit-msg floor), through the kit's writers (which add the trailer
  themselves), or, for the archive commit, through `commit-tree` with the
  recipe's trailer. A hook-refused commit writes nothing. Git moves a ref
  atomically, so an interrupted update leaves it at its old tip or its new
  one.
- **The binding:** the launcher itself records the tip of every local branch
  (`refs/heads/*`) immediately before it starts a leg and again after the
  leg exits.

**What the authority binds to.** The two snapshots around one leg. Trunk and
`archive/lanes` are judged on their first-parent lines from the pre-leg tip
to the post-leg tip. Every other branch the leg created or moved is judged
over its range from trunk by the slot's rule. A branch the leg deleted is
logged, not judged. `check-lane` binds to the branch's tip when it runs.

**Consumer and rulings.** One consumer, `scripts/coordinator/overnight_legs.py`
(the audit and `check-lane`). It checks every git read's exit status and
never reads a failed or unparseable read as an empty range. It stops the run
(exit 3), or refuses the landing, naming what it could not judge, on:

- a git read that fails or returns output it cannot parse;
- a ref it cannot resolve, or a trunk that no longer descends from its
  pre-leg tip;
- a commit whose message it cannot read;
- a trunk or `archive/lanes` commit whose trailer is missing, malformed or
  names another session;
- a lane window refusal (a commit inside a loop window without a
  well-formed trailer).

It never repairs, skips or re-orders a commit.

## Done-when

- Every deliverable above is in its target, each citing the ruling it
  carries.
- **Launcher tests.** Each fails on the code before the change:
  - with a stub `claude` on `PATH`, two legs see one well-formed
    `KIT_LOOP_SESSION`, the same in both;
  - an inherited well-formed marker is kept, and an inherited malformed one
    is replaced;
  - each leg's prompt is the handoff's session prompt, then the block (which
    opens with the marker check), then the provenance line naming that
    session;
  - an absent, unreadable or empty block refuses the run before any leg
    (exit 2);
  - a leg that adds a trunk or `archive/lanes` commit without the trailer,
    adds one naming another session, or rewinds trunk stops the run
    (exit 3), naming the commit;
  - a leg that adds a commit without the trailer to a lane it marked, then a
    marked commit or a marked squash, stops the run, naming the unmarked
    commit, and `check-lane` refuses that lane before the squash;
  - a lane whose replayed commits carry another run's well-formed session
    passes;
  - a git read that fails during the audit or `check-lane` stops the run or
    refuses the landing; it is never read as an empty range;
  - a leg whose commits all carry the run's trailer runs the next leg.
- The skill copy in `.claude/skills/` matches the kit source
  (`bootstrap.py --dest . --sync`). `check_docs.py --root . --strict-orphans`
  passes with the new block.
- **No shipped file changes, so there is no `RESYNC_PACK.md` entry and no
  trace rows:**
  - `bootstrap.select_skills` materializes only `scope: kit` skills, and
    `delivery_inventory` lists a `this-repo` skill's whole directory as
    "never materialized downstream";
  - `scripts/coordinator/` and `tests/` sit outside the kit;
  - no check requires a TC to cite a test module (49 of 232 are cited by
    none today).
- The lane's plan is produced after the claim and passes the plan gate (S4).
- The bar is green on the landing tip:
  - the smoke tier within its budget;
  - `check_trajectory.py --strict` clean;
  - `trace.py --strict` with no finding beyond LLR-292's (WI-914, landing
    earlier, fixes that one).

## Scope answers

- **S1:** one deliverable set, kept together. The launcher refuses to run
  without the block, the block points at the skill section, and the skill
  section describes the launcher's marking, so none is useful landed alone.
  The merge slot's reading of the re-claim is independently landable and is
  WI-918 (the owner's split ruling, 2026-10-14).
- **S2:** yes, one gate: the launcher's audit and `check-lane` decide
  whether the next leg starts and whether a leg lands a lane, from the refs
  the leg moved and the commits it added; see `## Trust` (round-1
  critique). Nothing else gains authority:
  - The marker is a process environment variable, not a file. Every reader
    of it only adds a refusal or a trailer: `check.py`'s floor and
    held-status step, the loop writers' `loop_held_status_refusal`,
    `provenance.with_loop_trailer`, `agent_brief.loop_provenance_note`, and
    the commit-msg hook's fail-closed check. Its failure contract under its
    new producer is in deliverable 1 and the Done-when.
  - The block's first check can only end a leg before any write.
  - The skill and the block govern the coordinator's own procedure.
  - The re-claim commit is read by nothing until WI-918, whose Trust section
    carries its authority.
- **S3:** closed by enumeration, with a declared default, and by
  construction.
  - **Every commit a headless leg makes**, by route:
    - **A porcelain commit** from any process in the leg's tree: `git
      commit` (with `-F` or `--amend`), a squash landing's commit, or `git
      merge`.
      - The marker is inherited by the leg's shell, its sub-agents, the
        Codex children and the adjudicator. `session_service` composes the
        adjudicator's environment over the ambient one, dropping only the
        launch's own names and competing credentials.
      - The commit-msg floor refuses a commit whose last `Loop-Session`
        trailer is missing, malformed or names another session.
      - This repo's `.githooks/commit-msg` delegates to the kit's hook in
        every worktree (`core.hooksPath`).
    - **The kit's plumbing and `--no-verify` writers** add the trailer
      themselves under the marker: the claim and the mint through
      `bookkeeping._commit_object`, `handback`, `commit_telemetry` and the
      merge slot.
    - **The coordinator's one plumbing commit**, the `archive/lanes`
      `commit-tree -F`, ends its message with the trailer (deliverable 3).
    - **A replay** (`rebase`, `cherry-pick`) keeps the message it was made
      with and never reaches the floor (checked on git 2.49). It is not a
      new authorship.
    - **Default:** any other route (`--no-verify`, `git revert`, other
      plumbing) is outside the procedure. The launcher's audit judges
      outcomes, not routes: every commit the leg added to trunk, to
      `archive/lanes` and to any branch it created or moved passes its
      rule, or the run stops.
    - **Lane commits** are judged by the rule the merge slot applies:
      before a leg's squash (`check-lane`) and after every leg (the audit).
      Once WI-808 moves landings onto the slot, its trailer rung judges them
      too. Until WI-918 lands, that rule does not read re-claims, so a lane
      with attended commits after a headless mark fails it: fail-closed,
      and a leg leaves such a lane to the attended session.
    - A commit on no landing ref (`refs/stash`) is outside the promise.
    - Builders, reviewers, Terra and planners never commit (Sol's and
      Terra's launchers check for a moved HEAD). One that did commit would
      still be in the marked tree.
  - **The prompt:** one composition with three fixed parts. The block
    restates nothing of the session prompt.
  - **Owner-held steps:** the enumerated set in deliverable 3, with its
    default.
  - **Lanes in flight:** every lane open when this lands was claimed unmarked
    and holds no marked writer commit, so each reads as a person's, as today.
- **S4:** `single`: the row has a Trust section, and it promises behaviour
  over an input space (every commit a headless leg makes, across every
  writer and route, and the set of owner-held steps). It changes one script
  plus text, and no interface seam: it calls
  `mark_loop_process`, `loop_trailer_refusal`, `loop_provenance_note` and
  `session_prompt` as they stand.
- **Architectural delta:** yes, carried within scope, and no preparatory
  refactor is needed.
  - **A new state:** a headless leg is an autonomous run, where legs ran
    unmarked.
  - **New domain values:** the headless block, in the leg prompt; and the
    re-claim subject, a lane-commit subject that nothing reads until WI-918.
  - **New inputs:** the leg prompt depends on the block and the run's
    session; the launcher's next leg depends on its audit of the commits the
    leg added.
  - **A boundary with a new producer:** the marker's existing crossing
    (IF-194: an environment variable a run sets once and its children
    inherit) now starts in this repo's launcher. That launcher is not a kit
    component, so no registry row changes.
- **B3 and B4:**
  - **B3:** the launcher's audit reads the commits the leg added (records
    written at the event) against the run's session. Nothing re-derives a
    lane's mode from the environment, the lease or dates.
  - **B4:** no Done-when item needs an owner act or credential. The first
    headless run is the owner's call to start (dropping `Overnight: stop`),
    so it is not a Done-when item. The next attended session reads that
    run's launcher log and handoff and records the result as a decision.
- **Dependencies:**
  - **`needs` WI-912, hard** (owner, 2026-10-14, in session). The row is
    claimed under its own scoped unpause once WI-912 has landed. WI-912's
    deliverable 4 is the adjudicator's trailer line: without it, a marked
    leg's first sitting is refused at the adjudicator's commit.
  - **No edge on WI-911 or WI-913.**
    - WI-911 lands before WI-912, by the queue and WI-912's own edge. This
      row edits the skill text both rewrite, building on WI-912's landed
      text.
    - The plan gate (WI-913) lands first in the queue, so it is in place at
      this row's claim.
  - **A mechanism change:** this row lands alone, after the cycle has run
    once through WI-912's act turn. The cycle first runs through this row's
    marking in a headless run, which the owner starts. Whether the next
    mechanism lane (WI-916) waits for that run is the coordinator's call at
    the landing, recorded as a decision.
  - **Later rows, not edges:**
    - WI-918 reads the re-claim. It needs this row (hard) and lands before
      WI-808, which the coordinator edges to it at filing.
    - WI-851 narrows its marker arm to a marked commit outside a lane, which
      this marking makes reachable from headless legs.
    - WI-801 deletes `coordinator_adjudicate.py`, so it must carry WI-912's
      trailer line, which this row relies on.
    - P2's per-call telemetry commits mark a lane under the rule above.
    - WI-857's premise holds: a leg's builder and adjudicator share one
      `Loop-Session`.
  - **No third-party dependency.**
- **Design calls** (recorded at filing as
  `docs/decisions/coordinator-2026-10-14.toml` D-016). Q3, how a re-claim
  clears the loop mark, is WI-918's.
  - **Q1, the session's scope:** one per run. This is `mark_loop_process`'s
    own "once per run" contract, as with the dispatcher. A lane that one leg
    claims and a later leg continues names one session within a run. Across
    runs, the slot accepts any well-formed session, and the floor judges
    only new commits, because replays never reach it. A per-leg session
    would add a second setter that no reader needs; the leg logs and
    handoffs already tell legs apart.
  - **Q2, the prompt:** the handoff's one attended prompt, plus a fixed block
    that only states the mode, plus the kit's own trailer note. Nothing is
    copied, so nothing can drift. The second headless prompt that leg 03
    copied between handoffs is what drifted.
  - **Q4, owner-held steps:** stop the row at a safe committed point, record
    it, move on, and close out with `Overnight: stop` when nothing can move
    (deliverable 3).
  - **Q5, the trailer's coverage:** the S3 answer: by construction for
    porcelain commits and kit writers, by recipe for the archive commit, and
    by the launcher's audit for every other route.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-14; CHANGES-REQUESTED, two findings):

- **S3, MAJOR: adopted, with a change to the remedy.** Lane commits were
  judged only through the squash's own message, so an unmarked lane commit
  could ride into a marked landing. The critic asked for a landing-recipe
  check; the row now has both a check before the landing and an outcome
  audit after every leg, from one rule (the merge slot's): "every other
  branch the leg created or moved, over its range from trunk, by the merge
  slot's own rule", and "`overnight_legs.py check-lane <branch>` ... runs it
  before a leg squashes a lane, so a lane holding an unmarked commit is not
  landed". The audit is kept as well because a construction the leg cannot
  skip covers a lane the leg never lands. The Done-when adds "a leg that adds
  a commit without the trailer to a lane it marked, then a marked commit or
  a marked squash, stops the run, naming the unmarked commit, and
  `check-lane` refuses that lane before the squash".
- **S2, MAJOR: adopted.** The audit gates the next leg, so the row gains a
  `## Trust` section: the commits and the launcher's two ref snapshots as
  carriers, their producers and failed-write shapes, the one consumer, the
  binding, and the rule that "It checks every git read's exit status and
  never reads a failed or unparseable read as an empty range". The Done-when
  adds "a git read that fails during the audit or `check-lane` stops the run
  or refuses the landing; it is never read as an empty range".

Round 2 (Codex Sol, medium, 2026-10-17, the confirming round, in
convergence stance): APPROVE, no findings. Both round-1 adoptions, S3's
pre-landing `check-lane` refusal and S2's Trust section, are carried by
the spec text they quote, so the row may be claimed once WI-912 is done.
