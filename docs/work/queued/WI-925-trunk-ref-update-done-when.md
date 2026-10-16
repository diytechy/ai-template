+++
id = "WI-925"
title = "A move of the trunk branch is judged for an unblessed Done-when change at the reference update, against the trunk it moves from, whatever command made it"
workstream = "process"
sr_refs = ["SR-156", "SR-019"]
specref = "docs/archive/work/complete/WI-921-hook-floor-done-when-census.md#trust"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-921"]
+++

## Context

Drafted on 2026-10-15 for filing on trunk at WI-921's landing, as the
successor the owner ruled in wi-921 D-014. (A work branch never mints a WI id,
so the id is assigned at filing.)

WI-921 armed the `done-when-blessed` pre-commit step. On trunk, the step
judges a commit that changes a claim copy's Done-when (under
`docs/work/active/<branch>/`), whether it closes the row or not. It compares
the index with HEAD, and treats HEAD as the commit's parent. Its Trust section
names the commits for which that is wrong, or for which no pre-commit hook
runs at all. The owner ruled them a stated residue (D-014), caught only after
the fact by the merge-time mint, and only when the sweep's hand-chosen
`--before` is the trunk commit before the change:

- **an amend** is judged against the commit it replaces. Two shapes were
  confirmed through a real `git commit --amend` (wi-921 D-014): an amended
  trunk close that gains a Done-when edit, and an amend that drops a trunk
  edit's only ruling. Both pass;
- **a cherry-pick, a revert or a rebase** runs no pre-commit hook;
- **a non-conflicting `git merge`** that makes a merge commit runs no
  pre-commit hook. Git runs only `pre-merge-commit` for it, and the kit ships
  none (wi-921 009 F1);
- **a hand fast-forward onto trunk** makes no commit at all;
- **a commit in a linked worktree on the trunk branch while the primary
  checkout sits on another branch** is read as "elsewhere". The cause is that
  `agent_common.trunk_name` names the trunk as the branch the primary checkout
  is on. So a Done-when change that closes nothing is not judged, and a later
  close there compares against the edited copy (wi-921 005 F4).

Every one of these commits reaches trunk in the same way: git updates the
reference `refs/heads/<trunk>`. Git's `reference-transaction` hook runs at
that update. In its `prepared` state the new objects exist, the reference is
locked but not yet moved, and a non-zero exit aborts the whole transaction.
WI-921's builder found no reliable amend signal at pre-commit: the hook's
environment is byte-identical for a plain commit and an amend (Git 2.49,
Windows). The reference update is the one boundary every route onto trunk
crosses. That includes routes that skip hooks by design: `--no-verify` does
not skip `reference-transaction`.

The owner's ruling estimated the build at 250 to 350 lines and named its
side effects (D-014):

- the hook runs under `--no-verify`, so the kit's own `--no-verify` commits
  (`handback._loop_commit`, used by `close_partial`) would be judged;
- a single fetched commit fast-forwarded onto trunk would be refused if it is
  unblessed;
- it needs git 2.28 or later;
- it has been verified on Windows only.

This row settles each one (see `## Calls for the owner at filing`).

**Found while reading for this draft (not reproduced).**
`spec_move._relink_inbound_links` rewrites every inbound markdown link in
every `.md` file when a spec moves. That includes a link inside another row's
claim copy, inside its Done-when section. `kitlib.done_when.changes` reads a
rewritten link target as a reworded item. So a hand landing staged with
`spec_move` can already be held by WI-921's trunk arm, over a Done-when change
nobody made, if another claimed row's Done-when links the moved spec. This
row moves the same reading onto plumbing routes: the claim and the intake
mint advance trunk through `bookkeeping.commit` (`update-ref`), which the new
hook sees and pre-commit never did. The loop's own claim could then be
refused. Call Q5 settles whether this row fixes it.

**Carried from WI-921's post-checkpoint gate** (wi-921 D-020; each a MINOR this
row's surface holds): the hook comment's and the RESYNC entry's residue lists
omit the linked-worktree shape (014 F1), which this row's rewrite of that
comment replaces; TC-325's method and expected never name the deletion-only
pin its evidence cites (013 F2, 014 F3), for this row's amendment of the TC
rows covering LLR-309; `staged_closes` keeps no non-test caller yet changed
its return shape (014 F4), for the new reader's design; and
`check_trajectory`'s hold-by-rename remedy still offers deleting the stranded
claim, which the trunk floor now refuses (014 F2), for this row's trunk-hold
text.

## Deliverables

One lane, one landing. The shipped files are marked, so the RESYNC entry can
list them.

1. **The hook** (shipped, new: `project-trajectory/hooks/reference-transaction`,
   POSIX sh like its siblings).
   - It acts only when its argument is `prepared`. Every other state exits 0.
     Those states are notifications after the decision, and git always runs
     `prepared` before it commits a transaction.
   - It reads git's stdin lines (`<old> <new> <ref>`) and keeps only an
     update of a branch reference (`refs/heads/*`) whose new value is not the
     zero id and differs from the old one. Per Q1 it keeps only the trunk
     branch.
   - A cheap shell pre-filter asks git whether the update's delta touches
     `docs/work/active/`. That delta is the reader's own (deliverable 2): from
     `git merge-base <old> <new>` to the new value, or from an empty base when
     the old value is the zero id, never from the old value to the new. An
     amend that drops only a ruling leaves the claim copy's bytes the same in
     the old and new commits, so an old-to-new delta would never reach the
     reader. Only when the delta touches `docs/work/active/` does the hook
     resolve the interpreter (`kit-python.sh`) and run the reader. So a
     checkout, fetch, stash, tag, `pack-refs` or branch creation costs one sh
     process and spawns no Python. If either of the pre-filter's git calls
     fails (the merge base or the delta), the reader runs (deny by default).
     The pre-filter never decides a hold.
   - Its comment block states the boundary and IF row. It says that
     `--no-verify` does not skip it and that the merge slot asks the same.
     Like `pre-commit`'s header, it says how to disable it.
   - Locating the scripts, and the `KIT_SCRIPTS_DIR` override, follow the
     pre-commit hook. One difference: when the delta touches
     `docs/work/active/` and the scripts directory or interpreter is missing,
     it refuses and names why. The pre-commit hook skips a missing scripts
     directory, which is a skip here that would fail open.
2. **The reader** (shipped: `project-trajectory/scripts/kitlib/done_when.py`,
   IF-286 extended).
   - A new function, beside `staged_hold`, judges one reference update
     `(ref, old, new)`. It takes the update's base as
     `git merge-base old new`. For a single-commit update that base is the
     commit's real parent, whatever command made it: an amend's base is the
     replaced commit's parent, and a cherry-pick's, revert's, merge commit's
     or linked-worktree commit's base is the old tip. For a fast-forward or a
     rebase it is the trunk the update moves from (Q2).
   - It lists the delta base→new through `classify_delta`, unchanged. Each
     claim-copy change is judged by `lane_hold(root, new, base, branch,
     [wi])`, so covers are read from the new tree. That is the one predicate,
     with no second reading.
   - The trunk arm judges every change, close or not, as deliverable 5 of
     WI-921 does for the index.
   - A creation of the trunk reference (old is the zero id) is judged against
     an empty base. There every claim copy is a lone `A`, so nothing is
     judged. That is stated, not hidden.
   - The trunk is identified by the reference's own name against the
     declared trunk (Q3), never by `branch --show-current` or by the primary
     checkout's branch.
3. **The entry point** (shipped: `project-trajectory/scripts/integrate.py`).
   `done-when-hold` gains a mode that reads git's update lines from stdin and
   asks the new reader for each kept line, so the hook makes one call per
   transaction. A malformed line holds, naming the line. The existing index
   mode, `staged_done_when_refusal`, is unchanged (Q4).
4. **The git floor** (shipped: the probe beside `kit-python.sh`, sourced by
   `pre-commit`). The pre-commit hook refuses on a git older than 2.28 and
   names the floor. On such a git the reference-transaction hook would never
   run, and the trunk arm would silently lose every shape above (Q6). One
   home for the version parse.
5. **Installation** (shipped):
   - `kitlib/bootstrap_manifest.py` `MAPPING` gains
     `("hooks/reference-transaction", ".githooks/reference-transaction")`;
   - `gitattributes.template` gains its `eol=lf` line;
   - `ADOPTING.md` lists the hook, the git floor, and how a hook manager
     chains to it (Q7);
   - `setup.sh` and `setup.ps1` are unchanged, because `core.hooksPath`
     already covers every hook in the directory. Bootstrap marks the file
     executable (`bootstrap.py`'s `.githooks` arm).

   In this repository, `.githooks/reference-transaction` is a thin wrapper
   that sets `KIT_SCRIPTS_DIR` and delegates, as `.githooks/pre-commit` does.
   `.gitattributes` gains the line.
6. **The trunk identity** (shipped, per Q3: `agent_common.trunk_name` reads
   the declared key, `process.toml.template` carries it, and the kit schema
   reader validates it). Every caller inherits the one reading: `agent_brief`,
   `gen_verdict_rollup`, `handback`, `integrate`, and `kitlib/done_when` twice.
7. **The relink** (shipped, per Q5): a claim-copy modification that is byte
   for byte the inbound relink of a move the same delta carries is not a
   Done-when change. The test is the existing exact reading
   (`spec_move.expected_relink`, as `integrate._relinked_exactly` uses it),
   extracted to one shared stage, not copied (0→A→B).
8. **The residue text** (shipped): the `done-when-blessed` entry in
   `hooks/pre-commit`'s comment block drops the fail-open residue that this
   row closes and points to the new hook. The fail-closed residues stay
   stated.
9. **The census** (this repository's tests): `tests/test_commit_floor_census.py`
   learns where `done-when-blessed` runs. It is still in the pre-commit floor,
   and the new hook runs the reader by name. A test reads the new hook's
   command line, as the census reads the pre-commit hook's.
10. **`RESYNC_PACK.md`**, one entry, listing the shipped files above. It says:
    - the hook and `check.py`, `integrate.py`, `kitlib/done_when.py` and
      `agent_common.py` are a set;
    - the git floor is 2.28;
    - the trunk key to add, per Q3, is a new setting an adopter takes, and
      `process.toml` is never replaced;
    - what is now refused at the reference update that was not before;
    - a repository that never claims into `docs/work/active/<branch>/` sees
      no change.

## Trust

Deliverables 1 to 3 give the same files that WI-921's step trusts authority
over every move of the trunk reference, not only over a commit that runs
pre-commit. They add three carriers of their own: git's update lines, the
declared trunk name, and the inputs of the upstream exemption (Q8). This is a trust boundary in the sense of
`project-trajectory/PROCESS.md` §3, "When a guard is owed": files on disk,
another process, and a model's output (the verdict). LLR-307 and LLR-309
state the reader's rulings. They are cited here, not restated. Every carrier
WI-921's Trust section lists (the verdict, the acceptance binding, the owner
ruling, the claim copy) keeps its producer, write route and failed-write
shapes unchanged. That section is the record, and nothing below re-opens it.

- **New carriers and their producers.**
  - **The update lines.** Git writes them on the hook's stdin, one
    `<old> <new> <ref>` line per reference in the transaction, with the
    state as the hook's argument. Git is the tool itself: a tampered or fake
    git is outside the review threat model (PROCESS.md §6). Failed-write
    shapes the reader must still meet:
    - a line that does not split into three fields;
    - a value that is not a full object id of the repository's hash length
      (git 2.45 and later can show a `ref:<target>` value for a symbolic
      reference);
    - an empty stdin in `prepared` state, which is a transaction with nothing
      to judge.
  - **The declared trunk name** (Q3). The adopter writes it in
    `docs/process.toml` by hand. Bootstrap writes it at scaffold from the
    current branch, and a resync adds it as a new setting (LLM-applied).
    Failed-write shapes: the key is absent; its value is not a string; it is
    empty; or it names no local branch.
  - **The upstream exemption's inputs** (Q8). Git writes both: the trunk's
    upstream configuration (`branch.<trunk>.remote` and
    `branch.<trunk>.merge`), set by a clone, `push -u` or
    `branch --set-upstream-to`, and the remote-tracking reference it names,
    written by `git fetch`. Failed-write shapes the reader must still meet:
    - no upstream configured for trunk;
    - configuration git cannot resolve to a remote-tracking reference (a
      malformed value, or a remote with no fetch refspec);
    - a tracking reference that is absent or unreadable;
    - a containment query (`git merge-base --is-ancestor <new> <tracking>`)
      that exits with anything but 0 or 1.
  - **The hook file and `core.hooksPath`.** Bootstrap and `setup.*` write
    them. Both are opt-in per checkout, as `pre-commit` is (IF-134). A
    checkout without them runs nothing. That stays the stated residue, as it
    is for every hook, and the merge slot still reads the merged result.
- **Consumers, found by grep** (`kdone.`, `done_when as`, `trunk_name(`),
  listed by path and function:
  - **New:** `project-trajectory/hooks/reference-transaction` →
    `integrate.py done-when-hold` (the stdin mode) → `kitlib/done_when.py`
    (the new update reader) → `lane_hold` → `_wi_hold` → `claim_copy`,
    `spec_at`, `blessing_owed` → `covering` → `_verdicts`
    (`kitlib/sitting.accepted_at`) and `_rulings`. The new reader alone reads
    the upstream exemption's inputs, before it judges an update; the sh
    pre-filter never reads them, so the exemption has one home.
  - **Unchanged hold points that share the reader:**
    - `integrate.py` `staged_done_when_refusal` → `staged_hold` (the
      pre-commit step);
    - `_merge_refusal` → `_done_when_refusal` → `lane_hold` (the merge slot);
    - `agent_loop.py` `routed_session` → `build_hold` → `lane_hold` (the
      loop's build hold);
    - `intake.py` `_done_when_drafts` → `claim_copy`, `blessing` (the
      merge-time mint).
  - **Readers of the Done-when that hold nothing:**
    - `adjudicate_brief.py` (`claim_copy`, `spec_at`, `changes`, `digest`;
      it renders the brief);
    - `agent_brief.py` (`claimed_text`, `changes`; it flags to the builder);
    - `review_brief.py` (`items`, `spec_at`, `claim_copy`; it flags to the
      reviewer);
    - `kitlib/plan_pass.py` and `plan_gate.py` (the digest, and
      `_CLOSED_SPEC_RE`; plan binding, not the blessing);
    - `plan_coverage.py` (imports the module).
  - **Readers of the trunk name** (Q3 changes their input):
    - `agent_common.default_base`, the worker preflight and the review brief
      slot;
    - `agent_brief.py`, `gen_verdict_rollup.py`, `handback.py`,
      `integrate.py` (`staged_done_when_refusal`);
    - `kitlib/done_when.py` (`_staged_base`, and the new reader).
  - **Kit routes that move the trunk reference, which the hook now judges:**
    - `bookkeeping.commit` → `_install_and_advance` (`update-ref HEAD`), used
      by `integrate.claim` and `intake._mint`;
    - `integrate.py`'s merge slot (`git merge --no-ff` on trunk);
    - a hand landing.

    The claim's own delta is a lone `A` under `active/<branch>/`, so it is
    not judged. But its inbound relink can modify another claim copy (see
    Context, and Q5). The merge slot asks `_done_when_refusal` first, over the
    same predicate. If the two ever disagreed, the slot's "unreachable"
    `code != 0` arm would become reachable and would leave the trunk checkout
    holding the merged tree. Deliverable 2's agreement test pins that they
    agree.
- **Ruling per input** (each holds, naming why, unless it says otherwise):
  - a state other than `prepared`: exit 0, as above;
  - a reference outside `refs/heads/<trunk>` (Q1), a deletion, or an update
    whose old equals its new: not judged;
  - the upstream exemption (Q8): an update of trunk is not judged only when
    git resolves trunk's upstream to a remote-tracking reference and
    `merge-base --is-ancestor <new> <tracking>` exits 0. Every other outcome
    grants no exemption: no upstream, configuration git cannot resolve, an
    absent or unreadable tracking reference, an exit of 1, or any other
    exit. The update is then judged like any other, and holds where that
    judgement cannot complete. The exemption never holds by itself, and is
    never granted by default;
  - a malformed line, or a value that is not an object id: holds;
  - a declared trunk that is absent, malformed, or names no branch: holds,
    but only for a transaction whose delta touches `docs/work/active/`. Any
    other update cannot carry a claim-copy change, so nothing is owed;
  - a merge base git cannot compute (unrelated histories, a shallow
    boundary): holds;
  - a delta git cannot list: holds. This is `staged_changes`'s shape, and
    reuses its wording;
  - a claim copy, current copy, verdict, binding or ruling: as LLR-307
    rules for every hold point (WI-921's Trust, "Ruling per input");
  - a missing scripts directory or interpreter, when the pre-filter says the
    delta touches `docs/work/active/`: refuses;
  - a git older than 2.28: the pre-commit hook refuses (deliverable 4). The
    reference-transaction hook cannot speak on such a git, because it never
    runs.
- **What the authority binds to:** unchanged from WI-921. That is the digest
  over the work item's id and its bound items, read from the new tree. A
  record that is only on disk, only in the index, or only in history binds
  nothing. The hook reads no index, so a temporary index (`commit -a`, an
  amend) cannot make the hold and the commit disagree.
- **Consumers that fail open today (read in the code):**
  1. `agent_common.trunk_name`, which `staged_done_when_refusal` hands to
     `kitlib/done_when.staged_hold`, names
     the trunk as the primary checkout's branch. A linked worktree on the
     real trunk is then "elsewhere", and a Done-when change there is not
     judged. This is wi-921 005 F4, and it is closed here by Q3.
  2. `kitlib/done_when.staged_changes` reads a failing
     `rev-parse --is-inside-work-tree` as "off a work tree, nothing judged".
     That reading cannot tell a git that failed from a directory that is not
     a repository. In a pre-commit hook it is improbable (git is mid-commit
     there). It is reported, not fixed, because the new reader does not use
     it.
  3. `kitlib/done_when._staged_base` judges nothing for a Done-when change
     without a close on a detached HEAD, because `branch --show-current`
     answers empty with exit 0. That is WI-922's identity class. Once this row
     lands, the trunk reference update re-judges such a change when it
     reaches trunk.
  4. `intake.py` `_done_when_drafts` skips, without a word, a closed spec it
     cannot read or parse from the working tree. That is the after-the-fact
     catcher this row stops relying on. It is reported, not fixed.
  5. `hooks/pre-commit` exits 0 when the kit scripts directory cannot be
     found (unless privacy is declared). This is a skip for every step,
     `done-when-blessed` included. Deliverable 1 does not copy it.

  All five are reported for the coordinator. Only 1 is in this row's scope.
- **Residue after this row**, stated:
  - a checkout with no `core.hooksPath`;
  - a repository on a git older than 2.28 that bypasses pre-commit too;
  - a trunk move made by writing the reference file directly, outside git
    (outside the threat model);
  - a fast-forward to a commit that a remote-tracking reference contains
    because someone moved that reference by hand (`update-ref`) rather than
    by `fetch`: the exemption reads git's reference, not how it was written,
    so it is a deliberate act, like disabling the hook.

  The merge slot and the mint still read the merged result.

## Done-when

- On a fixture trunk with a claimed lane, each shape is held at the reference
  update, with the trunk reference unchanged, and passes once its new tree
  carries a covering accepted verdict or owner ruling. Each case fails on
  WI-921's hooks alone, before the change. The shapes:
  - an amended trunk close that gains a Done-when edit;
  - an amend that drops a trunk edit's only ruling, the claim copy's bytes
    the same in the old and new commits (only a pre-filter over the
    reader's merge-base delta reaches the reader here);
  - a cherry-pick and a revert that change a claim copy's Done-when;
  - a rebase that moves trunk;
  - a non-conflicting `git merge` making a merge commit;
  - `git merge --ff-only` and `git branch -f <trunk>`;
  - a `--no-verify` commit;
  - a commit in a linked worktree on trunk while the primary checkout sits on
    another branch.
- For each shape, the test records what the checkout holds after a refusal,
  and the refusal's text tells the operator that the reference did not move.
- An ordinary trunk commit gets the same answer from the pre-commit step and
  the new hook. The merge slot's `_done_when_refusal` and the new reader
  agree on `tests/test_done_when_blessing.py`'s lane fixtures.
- Reference updates that carry no claim-copy change are not refused and start
  no interpreter: checkout, branch create and delete, fetch into
  `refs/remotes/`, stash, tag, `pack-refs --all`, `gc`, and a lane-branch
  commit (per Q1).
- The kit's own trunk routes are not refused on fixtures where nothing is
  owed: `integrate.claim`, `intake` mint, the merge slot. Per Q5, a claim
  whose relink rewrites a link inside another claim copy's Done-when also
  passes. This case fails before the change.
- Each of these holds, naming why, in-process tests driving the reader with
  crafted inputs (each fails before the change, since no such reader
  exists):
  - a malformed update line;
  - a non-oid value;
  - an unreadable merge base;
  - an unreadable delta;
  - an absent or malformed declared trunk on an update touching
    `docs/work/active/`.
- The pre-commit hook refuses on a git reporting a version below 2.28, naming
  the floor, and passes on 2.28. This is a test of the probe with a version
  string supplied.
- Per Q8: a trunk fast-forward to a commit fetched from upstream is ruled as
  the owner chose, and the test pins it: a fast-forward to a commit trunk's
  upstream tracking reference contains is not judged; one to a commit it does
  not contain is judged; and with no upstream configured, an upstream git
  cannot resolve, or an absent tracking reference, the update is judged. The
  judged cases carrying an unblessed Done-when change fail before the change.
- A bootstrapped scaffold carries `.githooks/reference-transaction`, LF and
  executable, and its pre-filter and reader resolve. This repository's
  wrapper delegates to it. `tests/test_dogfood_sync.py` holds the structure.
- The census (deliverable 9) fails before the change, because it cannot place
  the new hook's call, and passes after.
- `hooks/pre-commit`'s `done-when-blessed` comment no longer states the
  fail-open residue. LLR-307 and LLR-309 no longer state it either. They
  gain the update of the trunk reference as a hold point, by the sitting's
  reading, at the lane's checkpoint. A new IF row states the seam (git
  invokes the hook with a state and update lines; non-zero aborts the
  transaction). The TC rows covering LLR-309 gain the hook-driven cases.
- `RESYNC_PACK.md` carries the entry, anchored at the landing's parent.
- The bar is green on the landing tip: the smoke tier within its budget (the
  new hook-driven cases go to `SLOW_MODULES` if they cost it),
  `check_trajectory.py --strict` clean, `trace.py --strict` clean.
- **Owner-dependent, held separately (B4):** the hook-driven tests pass in the
  repository's CI matrix (Linux, Windows, macOS). CI runs only on the owner's
  push (`push = "human"`), so this item is the last before close. The lane
  holds for that run and never ticks it from a local Windows run. If the
  owner does not push, the row closes `partial` with that item named.

## Scope answers

- **S1:** three parts could land alone.
  - The trunk identity (6) could land first and alone. It is a reading change
    with its own callers.
  - The relink exemption (7) could land alone, and would fix WI-921's hand
    landing today.
  - The hook with its reader, entry point, git floor and installation (1 to
    5, 8 to 10).

  The hook cannot hold the linked-worktree shape without 6, and it would
  refuse the loop's own claim without 7. So if the critique splits them, 6
  and 7 land first, in that order, and the hook last. Kept together they are
  one landing with one RESYNC entry.
- **S2:** yes. See `## Trust`. Deliverables 1 to 3 give the verdict, its
  binding, an owner ruling and the claim copy authority over every move of
  the trunk reference. They add two carriers: git's update lines and the
  declared trunk name.
- **S3:** the input space is closed by construction.
  - Each stdin line is either a kept trunk update or not judged. A line in
    neither shape holds.
  - Each kept update's delta is listed by `classify_delta`, which is already
    deny-by-default: any entry but a lone `A` under `active/<branch>/` is a
    change.
  - The commands that produce a trunk update are open-ended (any porcelain or
    plumbing). The construction makes that list irrelevant: the hook judges
    the update, not the command.
  - Every read the reader cannot complete holds.
- **S4:** `single`. The row has a Trust section, touches several script
  families (hooks, `kitlib/done_when`, `integrate`, `agent_common`,
  `spec_move`, bootstrap) and adds an IF seam. Any one of those is enough.
- **Architectural delta:** four.
  - A new boundary: the shipped kit gains its first hook at the reference
    update, a second commit-time seam beside IF-134.
  - The hold's verdict depends on a new input: git's update lines.
  - Per Q3, a new domain value: the declared trunk name, replacing the
    primary checkout's branch as the trunk's identity for every caller.
  - A new requirement on the environment: the git 2.28 floor.

  No state is added. No preparatory refactor is needed beyond extracting the
  exact-relink reading (deliverable 7) as its own commit.
- **B3:** the update is judged from its own old and new values and their
  merge base, which is the update's parent-equivalent. The merge base is
  computed for this update, not found by searching history for a claim or a
  blessing. Covers are read from the new tree. Nothing re-derives a past
  decision.
- **B4:** one item needs the owner's act, the CI matrix run on push. It is
  separated as the last Done-when item, with a stated hold and a partial
  disposition. No other item needs an owner act or credential.
- **Dependencies:**
  - `needs = ["WI-921"]`. WI-921 lands first. This row extends its reader,
    its census and its hook comment.
  - WI-922 (active) edits the shipped pre-commit hook's comment block and
    owns the branch-identity class for the plan gate. The two share no
    function. Q3 changes `trunk_name`, which WI-922's plan gate may read, so
    whichever lands second rebases and re-runs its tests.
  - No third-party dependency. Git 2.28 is a tool floor, not a package.
- **A separate finding, not in scope:** the plan gate's landing shapes
  (WI-922) are the same class at the same boundary. A later row could move
  `plan-gate`'s trunk judgement to this hook too. It is surfaced for the
  coordinator only.

## Calls ruled at filing

The owner ruled all eight calls in session, each as recommended (2026-10-15, the attended coordinator session that landed WI-921). Each call keeps its options and reasoning as asked.

- **Q1: which references the hook judges.**
  - (a) Only the trunk branch.
  - (b) Every `refs/heads/*` update, with WI-921's three arms (trunk, the
    claim's own branch, elsewhere).
  - (c) Every reference, `HEAD` on a detached checkout included.

  **Ruled (a), as recommended.** Every shape in D-014's class is a move of the trunk
  reference, so (a) closes the whole class. The lane side is already held by
  pre-commit, the loop's build hold and the merge slot. (a) also removes
  D-014's first side effect: `close_partial`'s `--no-verify` commit is on a
  lane branch, so the hook never judges it, and its stated reason ("a hook
  refusal here would only trade a merge that is checked for a branch that
  hangs") stays true. (b) judges `close_partial` and every rebase of a lane.
  (c) also judges each step of a rebase on a detached HEAD, which would stop
  rebases halfway.
- **Q2: how a multi-commit update is judged.**
  - (a) The new tip against the merge base of old and new, once, with covers
    read at the new tip.
  - (b) Each new commit against its own first parent.

  **Ruled (a), as recommended.** For every single-commit shape the two are the same: the
  base is the real parent, as D-014 asks. They differ only for a fast-forward
  or a rebase onto trunk. There (b) refuses a lane that edited its Done-when
  in one commit and was blessed in a later one, though the tree trunk would
  stand on is blessed. (a) is the merge slot's reading, so the two cannot
  disagree, and it costs one diff rather than one per commit. The cost of (a)
  is that trunk's intermediate commits are not each sound, only the tip it
  lands on. Trunk only ever stands on the tip.
- **Q3: the trunk's identity.**
  - (a) A declared `trunk` key in `docs/process.toml`, read by
    `agent_common.trunk_name` for every caller. Bootstrap writes it, and a
    resync adds it. Absent, it holds the commits it is needed for.
  - (b) The key is read only by the new hook, and `trunk_name` is unchanged.
  - (c) No key: keep the primary checkout's branch and state the
    linked-worktree residue.

  **Ruled (a), as recommended.** (c) leaves 005 F4 open and does not close the class
  D-014 names. (b) creates two trunk identities that can disagree, which is a
  second home for one fact. (a) **forces a migration**: every adopter adds
  one line, and an adopter who skips it has every update that touches a
  claim copy held, naming the key. It also changes an input of six callers.
  It is still one rule, deny by default, with no fallback to the old reading
  (the owner's 2026-10-03 rule: fix the single point of failure).
- **Q4: the pre-commit step's trunk arm.**
  - (a) Keep `done-when-blessed` in the pre-commit floor, unchanged. On
    trunk an ordinary commit is judged twice by the one reader.
  - (b) Retire the pre-commit trunk arm, and keep its lane and "elsewhere"
    arms.

  **Ruled (a), as recommended.** It is the smaller change. Pre-commit refuses before the
  message editor opens, and the reference update refuses after it. The
  second judgement spawns an interpreter only for a commit that touches
  `docs/work/active/`. (b) would make trunk commits depend on the git floor
  alone and re-open WI-921's census classification.
- **Q5: the relink reading.**
  - (a) Fix it here (deliverable 7): a claim-copy edit that is exactly the
    inbound relink of a move in the same delta is not a Done-when change,
    through the existing exact reading, extracted once.
  - (b) File it as its own row before this one.
  - (c) Leave it: such commits are held, and an owner ruling releases each.

  **Ruled (a), as recommended.** This row is what moves the reading onto the loop's
  plumbing claim. Landing the hook without the fix could refuse an
  unattended claim, so it belongs in the same landing. If S1's split is
  taken, it lands first. (c) puts the cost on the owner for a change nobody
  made. One caution: the finding is from reading the code. The builder
  confirms it with a fixture before building the fix, and if it does not
  reproduce, deliverable 7 drops.
- **Q6: git older than 2.28.**
  - (a) The pre-commit hook refuses and names the floor.
  - (b) It warns and proceeds.
  - (c) Keep a pre-commit-only path for old git.

  **Ruled (a), as recommended.** Git 2.28 shipped in July 2020. CI's runners and current
  Git for Windows are far above it. (b) silently drops every shape this row
  closes. (c) is a legacy path, which the owner's rule excludes. The cost is
  that an adopter on an older git cannot commit through the hook until they
  upgrade. The refusal names that.
- **Q7: an adopter's own `reference-transaction` hook.**
  - (a) Same as `pre-commit` today. The file is kit-owned. `core.hooksPath`
    overrides a hook manager, and an adopter with their own chain calls
    `.githooks/reference-transaction` from it (ADOPTING.md §1 gains the
    line).
  - (b) The kit hook execs a `reference-transaction.local` after its own
    verdict.
  - (c) Bootstrap refuses to overwrite an existing file.

  **Ruled (a), as recommended.** It is the one existing convention, and nothing in the
  kit's other hooks has an extension point. (b) adds a second path and a
  file name to maintain. (c) breaks the "kit-owned files are overwritten"
  rule a resync relies on.
- **Q8: a trunk fast-forward to commits fetched from upstream**
  (`git pull --ff-only`, `git merge --ff-only origin/<trunk>`), when they
  carry an unblessed Done-when change.
  - (a) Judge it like any update. A held pull leaves the local trunk behind
    the shared one, until a blessing lands upstream or the owner bypasses the
    hook.
  - (b) An update of trunk to a commit that trunk's own upstream
    remote-tracking reference already contains is not judged: the hold is
    where trunk is made, not where it is synced.
  - (c) Judge it, but only warn.

  **Ruled (b), as recommended.** Under (a), the local trunk can be stuck behind a remote
  it cannot change without first pulling, which is a deadlock only a bypass
  breaks. The exemption is tied to trunk's own upstream, not to any remote
  branch, so a hand fast-forward onto a pushed lane branch is still judged.
  Its residue is a commit that reached the remote trunk unjudged. With
  `push = "human"`, that is a commit the owner pushed. (c) is a hold that
  does not hold. The reading must fail closed: an upstream git cannot
  resolve is not "contained".

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-15, at `c0dfd1823`; CHANGES-REQUESTED,
two findings; coordinator-2026-10-15 D-006):

- **S3, MAJOR: adopted.** The pre-filter takes the reader's own delta.
  Deliverable 1 now reads: "That delta is the reader's own (deliverable 2):
  from `git merge-base <old> <new>` to the new value, or from an empty base
  when the old value is the zero id, never from the old value to the new",
  and "If either of the pre-filter's git calls fails (the merge base or the
  delta), the reader runs (deny by default)." The Done-when's amend shape now
  reads: "an amend that drops a trunk edit's only ruling, the claim copy's
  bytes the same in the old and new commits (only a pre-filter over the
  reader's merge-base delta reaches the reader here)".
- **S2, MAJOR: adopted.** The Q8 exemption gets its carrier contract in
  Trust: "The upstream exemption's inputs" names git as the producer of the
  upstream configuration and the remote-tracking reference, their write
  routes and four failed-write shapes; the consumer list names the new reader
  as the exemption's one home; and the ruling per input reads: "an update of
  trunk is not judged only when git resolves trunk's upstream to a
  remote-tracking reference and `merge-base --is-ancestor <new> <tracking>`
  exits 0. Every other outcome grants no exemption ... The update is then
  judged like any other, and holds where that judgement cannot complete."
  The residue list names a tracking reference moved by hand. The Done-when's
  Q8 item pins the contained, uncontained, unconfigured, unresolvable and
  absent cases.
