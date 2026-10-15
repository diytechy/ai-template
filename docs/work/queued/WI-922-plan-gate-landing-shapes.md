+++
id = "WI-922"
title = "The plan gate judges a single row's landing by the commits and the close it carries, whatever branch, merge shape or HEAD state the commit is made from"
workstream = "process"
sr_refs = ["SR-154"]
specref = "docs/archive/work/complete/WI-913-plan-gate.md#deliverables"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-913", "~WI-921"]
+++

## Context

Filed on trunk on 2026-10-15 by the attended coordinator, from a planner's
draft, as WI-913's successor: row 2 of the 2026-10-15b handoff's queue, from
the coordinator's bindings in wi-913 D-006 and D-010. Round 3's convergence
reviews raised three MINORs in one class, landing shapes the hook does not
judge:

- 008 F1: a build commit on a detached HEAD in a `single` lane's worktree;
- 008 F2: a hand `git merge --no-ff --no-commit` of a lane on trunk;
- 009 F1: a squash from an alias branch whose tip the lane branch does not
  contain.

Each lets an unplanned build reach trunk only when two failures meet: a lane
commit the lane's hook did not judge, and a landing the walk does not see. The
first can be a `--no-verify` commit, an amend, a commit on a detached HEAD or
an alias branch, or a checkout without the hook. WI-913 Q1 made the walk the
answer to that first failure ("`--no-verify` lands nothing"). This row makes
the answer hold for every landing the hook runs for.

The three share one cause. The gate finds a change's lane from the current
branch's name, or from the names of the local branches that contain a squash's
tip, and it reads git's in-progress state only through `SQUASH_MSG`. Ruling 1
(closed coverage, construction first) governs, so this row closes the class,
not the three instances.

The planner's notes, kept in the coordinator's 2026-10-15 scratch root,
enumerate 24 shapes with their code sites, and record a probe of which hooks
git runs for each (git 2.49):

- 8 are judged as designed;
- 3 are judged only by the landing walk;
- 7 run the hook but are not judged;
- 6 are out of scope.

WI-913's post-checkpoint gate added two MINORs that D-010 routes here,
because this lane re-touches SR-154's gate chain and the gate's code:
SR-154's single-plan predicate reads as scoped by its unattended-integration
condition (013 F1, 014 F1), and the gate's cap check keeps a branch the filing
step makes unreachable (013 F3).

## Deliverables

One lane, one landing. The `(Qn)` marks are the calls ruled at filing, below.

1. **What a commit carries, read once** (`project-trajectory/scripts/plan_gate.py`;
   shipped, RESYNC entry). Every commit the hook runs for is judged by the
   commits git's in-progress state says it brings:
   - for a merge finished by commit, every commit reachable from any
     `MERGE_HEAD` tip and not from HEAD, once each: git writes one tip per
     line, and a multi-tip merge lists several;
   - `HEAD..<tip>` for a squash, as today;
   - the picked commit for a cherry-pick finished by commit;
   - nothing, for any other state.

   A `MERGE_HEAD` that is malformed, or that names a tip git cannot resolve,
   holds, naming why.

   Each carried commit that trunk does not already contain goes through the
   existing rider, oldest first, under deliverable 2's identity order,
   whatever branch or HEAD state the commit is made on. The commit's own
   change is judged as today when it is made on a branch that names a claim
   folder.
2. **Whose claim copies judge a change: one order, deny by default.**
   - A carried commit is judged under two sets of lanes:
     - the lane the commit's own staged close names, that is, the claim folder
       of a spec it moves out of `docs/work/active/<lane>/`, read by
       `kitlib.done_when.staged_closes`;
     - each claim-named local branch that contains the carried commit.
   - A commit made on a detached HEAD is judged as the own commit of each
     claim-named local branch that contains HEAD. If trunk contains HEAD, it
     is trunk's own.
   - A carried or detached commit that resolves to no lane and carries build
     output is unattributed. It holds by name while HEAD's tree carries a
     `single` or out-of-set claim copy.

   This default is today's `_unattributed_squash`, made the one default; its
   remedy names the lane's own branch. A branch that names no claim folder
   (`archive/lanes` contains every archived tip) no longer stands in for a
   lane.
3. **The close, judged by content (Q1).** A commit whose own change, against
   its first parent, closes a `single` row and carries build output holds
   unless its own tree holds a pass record binding that row's plan and
   Done-when as the commit leaves them. The rule needs no git state, so it
   judges a landing whose carried commits git no longer records wherever the
   close rides it:
   - a squash after a `git stash` (recipes §3's trap);
   - a file-copy landing.

   A close that carries no build output passes before any record, as today.
4. **Contract text** (shipped, same entry):
   - the module docstring and the IF-295 contract body in `plan_gate.py`;
   - the `plan-gate` entry in the shipped hook's comment block, whose "Trunk,
     and a lane with no such row, are never judged" becomes "trunk's own
     commits".
5. **SR-154's single-plan hold, under its own condition** (spine text, sat at
   the checkpoint; wi-913 D-010). SR-154's approved requirement opens with
   the condition "when unattended work reaches integration", and its
   single-plan clause reads as scoped by it, though the gate holds an attended
   lane at every lane commit and at its landing. The amendment gives that
   clause its own condition, so the unattended-integration condition scopes
   only the routing predicate, and keeps the row's one `shall` (the owner's
   ruling of 2026-10-15, wi-913 D-008, over a separate SR or a waiver). Every
   approved word is kept; the acceptance text changes only if the sitting
   asks.
6. **The cap check's unreachable branch is deleted** (`plan_gate.py`,
   `_cap_problems`; wi-913 D-010, 013 F3). Its hold for "the second critique
   does not approve and has no BLOCKER or MAJOR finding to dispute" guards a
   state the filing boundary already makes unrepresentable:
   `kitlib.verdict.filing_refusal` refuses a CHANGES-REQUESTED that names no
   finding, and one whose findings are all MINOR reads as an APPROVE.

Unchanged: the merge slot (`landing_refusal`), the pass record's grammar, the
filing step, and `kitlib.git.squash_commits`, text-then-act's reader (Q3).

## Trust

The pass record already releases the build gate; WI-913's Trust section
(`docs/archive/work/complete/WI-913-plan-gate.md#trust`) states that, under
PROCESS.md §3, "When a guard is owed". The record's producer, write route,
failed-write shapes and what it binds are unchanged. Two things are new:
deliverable 3 makes the record release a second hold, a `single` row's close
that carries build output, and deliverables 1 and 2 add arms to the gate's
one reader.

- **Consumers.** Every arm runs in `project-trajectory/scripts/plan_gate.py`
  (`staged_lines`), the pre-commit step that `check.py` runs.
  - The new arms are the carried-commit walk on a merge or cherry-pick
    landing, the identity order with its default, and the close rule.
  - The close rule reads the record from the closing commit's own tree,
    because a landing brings the record and the build in one commit.
  - The existing consumers are unchanged:
    `project-trajectory/scripts/integrate.py` (`_merge_refusal` →
    `landing_refusal`), and the coordinator through the `coordinator-cycle`
    skill.
- **Ruling per input.** Each holds; nothing here fails open.
  - **Absent.** A close that carries build output with no pass record in its
    tree holds, naming the row.
  - **Unreadable.** A git read or a decode that fails holds, naming why. So
    does a carried range git cannot list, a branch listing that fails, or a
    malformed or unresolvable `MERGE_HEAD` tip.
  - **Malformed.** A record outside its grammar, or one binding another row,
    plan or Done-when, holds, saying which.
  - **Unattributed.** A change that carries build output and resolves to no
    lane holds by name while HEAD's tree carries a `single` or out-of-set
    claim copy.
  - **Trunk's own.** A carried commit that trunk already contains is not
    judged.
- **What the authority binds to.** The work item, the plan bytes and the
  Done-when digest, as before. At a close, the record must be in the closing
  commit's own tree; a record left only in the lane's history binds nothing.

Deliverable 6 removes no hold a filed critique can reach: the filing step's
refusal stays the one boundary for that state.

This ruling goes to the owner to confirm or overrule (`coordinator-cycle` §1).

## Done-when

- A test drives each shape on a fixture trunk and lane, and fails on the code
  before the change:
  - on trunk, a hand `git merge --no-ff --no-commit` of an unplanned `single`
    lane is held and a planned lane's passes; the same holds on a detached
    trunk checkout;
  - a hand-finished multi-tip merge whose later tip carries an unplanned
    build, with no close, is held; a `MERGE_HEAD` naming a tip git cannot
    resolve is held, naming why;
  - a conflicted cherry-pick of an unplanned lane's build commit onto trunk
    is held;
  - a build commit on a detached HEAD at a `single` lane's commit is held,
    and one at a commit trunk contains is not;
  - a squash of an alias whose tip the lane branch does not contain is judged
    under the lane its close names. Without a close it is held by name, and
    so is one whose only containing branch is `archive/lanes`;
  - a landing that closes an unplanned `single` row and carries its build
    output is held in two forms: a squash whose `SQUASH_MSG` a stash removed,
    and a file copy. A planned row's landing passes in both;
  - a cherry-pick of a commit that no claim-named branch contains, carrying
    build output, is held by name while a `single` claim copy is in the tree.
- Tests pin what does not change:
  - a lane's own commits and its refresh merge;
  - the prescribed squash and the merge slot;
  - trunk's own plain commits;
  - a partial or cancelled close before any record.
- `_cap_problems` has no branch for a second critique that neither approves
  nor names a BLOCKER or MAJOR finding, and the filing step's refusal of that
  state stays pinned by a test the lane names.
- The change's spine rows are authored in the lane and sat at its
  checkpoint:
  - SR-154 is amended: its single-plan hold reads under its own condition,
    with one `shall` and every approved word kept;
  - LLR-337 is amended: its judged shapes, the identity order, the close rule
    and its trunk clause;
  - TC-367 is amended;
  - IF-295's contract body is restated in the code.
- `RESYNC_PACK.md` carries one entry for `plan_gate.py` and the hook's
  comment. It forces no migration on a repository with no `single` row, and it
  names the new holds: a hand merge, a cherry-pick, an alias or unattributable
  landing, and a close that carries build output without a binding pass
  record.
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, and `trace.py --strict` with no finding
  beyond LLR-292's, or none once WI-914 has landed.

## Scope answers

- **S1:** deliverables 1 and 2 (the reader and the identity order) and
  deliverable 3 (the close rule) could each land alone. They stay together
  because they close one input space, the commits the hook runs for, and
  either part alone leaves S3 open: 1 and 2 cannot judge a landing that left
  no git state, and 3 cannot judge the order of a lane's commits. If the
  critique splits them, 1 and 2 land first, since they close D-006's three
  findings. Deliverables 5 and 6 could land alone too; they ride here because
  D-010 bound them to the lane that next re-touches SR-154's chain and the
  gate's code, which saves a second sitting on SR-154.
- **S2:** yes. Deliverable 3 makes the pass record release a second hold, and
  deliverables 1 and 2 add arms to its one reader; see `## Trust`.
- **S3:** the hook's inputs are three closed axes, and every combination has a
  ruling.
  - **Where the commit is made:** a claim-named branch, any other branch, or
    a detached HEAD.
  - **What git's in-progress state names:** nothing, `MERGE_HEAD` (one tip
    or several), `SQUASH_MSG` or `CHERRY_PICK_HEAD`. Any other state (a revert, a rebase
    stop that names none of these, an `am` session) names nothing.
  - **What a change's identity resolves to:** a lane, trunk's own, or nothing.
    Nothing, with build output, holds by name: that is the default.
  - **Out of reach.** Some shapes git makes without pre-commit:
    - `--no-verify`;
    - a `git merge` that git commits itself (Q2): git runs only
      pre-merge-commit, before `MERGE_HEAD` exists;
    - a fast-forward or a ref move;
    - a clean cherry-pick, revert, rebase or `am`.

    A forge merge is also out: forge mode has no landing code. Each of these
    is the hook-bypass equivalent that PROCESS.md §6's threat model leaves out
    of scope. An unplanned build reaches trunk through one only if a second
    failure in the lane let a commit past the lane's own hook, and the close
    rule still judges whichever later commit carries the row's close.
  - **An amend** is judged against the commit it replaces, because the hook
    has no signal for it (probed). The landing walk judges it against its real
    parent.
- **S4:** `single`. The row has a Trust section and promises behaviour over
  an input space; either alone is enough. It changes the gate behind the
  IF-295 seam and newly reads another family's reader,
  `kitlib.done_when.staged_closes`.
- **Architectural delta:** yes, carried within scope.
  - A new input: the gate's verdict now depends on git's in-progress state
    and on the close a commit stages.
  - A new domain value: the unattributed identity outcome, held by default.

  No state or boundary is added, and no preparatory refactor is needed: the
  arms reuse `lane_rider`, `gate_rows`, `staged_closes` and the record reader.
- **B3 and B4:** every rule reads only the commit being made and its parents.
  The record is trusted as it was written at its event, never recomputed from
  history. No Done-when item needs an owner act.
- **Dependencies:**
  - `needs = ["WI-913"]`, met: the code this row changes landed with WI-913
    (`b803dd019`), and S4 makes the row `single`, so its plan goes through
    WI-913's gate.
  - `~WI-921`, soft: with WI-921 this row shares no script, but both rows
    edit the shipped hook (WI-921 its floor line and a new comment entry,
    this row the `plan-gate` entry) and each adds a `RESYNC_PACK.md` entry,
    so whichever lands second rebases. WI-921 lands first by the queue, and
    this row lands alone after it (revision 37).
  - No third-party dependency.

## Calls ruled at filing

The owner ruled the drafter's three calls in session, each as recommended
(2026-10-15); coordinator-2026-10-15 D-002 records the filing.

- **Q1: deliverable 3 stays in this row.** The stash trap is this
  repository's own (recipes §3), and a file copy is a plausible hand landing;
  without the rule, both stay open.
- **Q2: a `git merge` that git commits itself stays out of reach.** Git runs
  only pre-merge-commit for it, before `MERGE_HEAD` exists (probed), so the
  merge skips every floor step, not only this one. Shipping that hook would
  change every floor step, the merge slot's own merges included. It is listed
  under S3's "Out of reach", and nothing is built for it.
- **Q3: text-then-act is left alone.** Its hook path has the same hand-merge
  gap, and LLR-302 accepts it: the merge slot judges each lane commit. This
  row neither widens to text-then-act nor changes the shared `squash_commits`
  reader. Whether the walk's other riders (`ruling-sync`, `held-status`) share
  the shape is unchecked; it is an unfiled follow-up in `docs/status.md`.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-15; CHANGES-REQUESTED, one finding):

- **S3, MAJOR: adopted.** The merge arm read `MERGE_HEAD` as one tip, so a
  hand-finished multi-tip merge carried its later tips past the walk. The
  arm now reads "every commit reachable from any `MERGE_HEAD` tip and not
  from HEAD, once each: git writes one tip per line, and a multi-tip merge
  lists several", and "A `MERGE_HEAD` that is malformed, or that names a tip
  git cannot resolve, holds, naming why"; the Trust section's unreadable
  input adds "a malformed or unresolvable `MERGE_HEAD` tip", and S3's axis
  reads "`MERGE_HEAD` (one tip or several)". The Done-when adds "a
  hand-finished multi-tip merge whose later tip carries an unplanned build,
  with no close, is held; a `MERGE_HEAD` naming a tip git cannot resolve is
  held, naming why".

Round 2 (Codex Sol, medium, 2026-10-15; a confirming round in convergence
stance): APPROVE, no findings; the adoption confirmed in the spec as quoted.
