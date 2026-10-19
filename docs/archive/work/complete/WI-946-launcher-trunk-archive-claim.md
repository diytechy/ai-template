+++
id = "WI-946"
title = "The overnight launcher judges every leg against the trunk it bound at run start and refuses a leg that moves the checkout off it or rewinds or deletes archive/lanes, and a lane claim git cannot read is a refusal at the merge slot and the launcher alike"
workstream = "process"
sr_refs = ["SR-209"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-917", "~WI-918"]
+++

## Deliverable

Closed at its landing on 2026-10-19, after its gate and act:

- The overnight launcher binds trunk once per run, through the kit's trunk
  reader, and logs it; a reader that refuses stops the run before any leg.
  Every leg is judged against that bound trunk: a pre-leg snapshot without
  it, or a leg that leaves the primary checkout detached, on another branch
  or unreadable, stops the run. Trunk and `archive/lanes` are judged by one
  descent rule: a ref present before a leg that is gone after it, or no
  longer descends from its pre-leg tip, stops the run naming the old tip.
  `check-lane` reads trunk through the kit's reader, and a refusal reads as
  "cannot judge".
- One checked claim reader, `agent_common.loop_claimed`, serves the merge
  slot and the launcher alike: a claim log git cannot read, or a record in
  it with no separator or commit id, is a refusal naming the read, never an
  unclaimed lane, at the slot's trailer and held-status rungs and at the
  launcher's audit. The launcher's docstring states the run's bound and the
  orders the trunk reader's fallback admits until the trunk-by-name row; the
  coordinator-cycle skill's headless section names the run's bound trunk.
- Spine: LLR-248's detail and code_symbol and TC-242's method and expected
  amended by addition (sitting 003-ADJUDICATE-8b630c5, both MEANING+BLESS),
  re-attested by act 134; IF-065's data names the reader. `RESYNC_PACK.md`
  carries the entry, anchored at the landing's parent.
- Reviews: the single plan's critique-1 (APPROVE, 0 findings); counted
  round 1 (001-REVIEW-A APPROVE 0, 002-REVIEW-B APPROVE 1 MINOR, fixed in
  wording before the checkpoint) and the gate in convergence stance
  (004-REVIEW-A APPROVE 0, 005-REVIEW-B APPROVE 1 MINOR, to status.md's
  follow-ups). Decisions: `docs/decisions/wi-946.toml` D-001 to D-012.

## Context

Filed on trunk on 2026-10-18 by the attended coordinator, under the owner's
direction of that day (`docs/decisions/coordinator-2026-10-18.toml` D-004):
turn the queue toward headless runs. D-004 names two gate rows that land
before the first headless run. WI-918 is one. This row is the other: the
overnight launcher's follow-ups that `docs/status.md` lists from WI-917's
rounds (`docs/decisions/wi-917.toml` D-003 and D-005) and from WI-925's build.
The owner ruled the filing calls in session (D-005; `## Calls ruled at
filing`). The spec of record is WI-917's `## Trust` section, which this row
amends in four places. Where this row and a ruling differ, the ruling
governs.

**What the launcher does today** (`scripts/coordinator/overnight_legs.py`).
Each finding below was reproduced at drafting, on scratch repositories built
with the launcher's own test fixtures (`tests/overnight_legs_fixtures.py`).

- **Trunk is re-read before every leg.** `pre_leg` calls the launcher's own
  `trunk_name`, which reads `git symbolic-ref HEAD` in the primary checkout.
  A leg that leaves that checkout on another branch makes the next audit
  judge that branch as trunk. The real trunk is then judged by the lane rule,
  which reads it as a person's lane and judges nothing. Reproduced: leg 1
  ran `git checkout -b elsewhere`, and leg 2 added an unmarked commit to the
  real trunk. Leg 2's audit read `trunk 1 commit(s); ... lane main window
  none`, and the run ended with exit 0. This is wi-917 D-003's F1, which the
  gate found again (D-005).
- **The rest of the run follows the checkout too.** `newest_handoff` reads
  the newest handoff from the checkout's branch. The main loop reads the
  `Overnight: stop` line and the progress check from it, and each leg starts
  in that checkout. In the same reproduction, leg 2 ran from a handoff that
  leg 1 had committed on `elsewhere`. The leg's log line prints `rev-parse
  HEAD` as trunk's new tip.
- **`check-lane` reads trunk the same way,** at its own run. Run with
  `--repo` set to the lane's own worktree, it judged the lane from the lane's
  own tip. That is an empty range, so it printed `passes (window 0)` for a
  lane holding an unmarked commit.
- **`archive/lanes` has no descent check.** `judge_archive` judges only the
  commits the leg added to its first-parent line. A rewind adds none. A
  reset to a commit that does not descend from the old tip has only its new
  commits judged. A deletion is "logged, not judged". Reproduced: a rewind
  logged `archive/lanes 0 commit(s)`, a deletion logged `deleted (logged,
  not judged)`, and both runs ended with exit 0. This is wi-917 D-005's
  coverage note.
- **The launcher keeps its own trunk reader.** It is a second home for the
  trunk's identity, beside the kit's `agent_common.trunk_name` (WI-925's
  build).

**What the merge slot does today**
(`project-trajectory/scripts/integrate.py`).

- **Two copies of the claim reader.** The slot reads whether the loop
  claimed a lane in `_loop_claimed`. The launcher's `lane_claimed` is a copy
  of it (wi-917 D-003 F3).
- **The slot's copy fails open.** A claim log git cannot read reads as
  unclaimed. A loop-claimed lane with no marked loop-writer commit is then
  a person's lane: the trailer rung and the held-status rung both pass it.
  Reproduced: a lane with a marked claim and one unmarked commit is refused
  by the trailer rung while its claim log is readable. With only the claim
  read failing, the rung returns no refusal, and `_loop_window` returns
  `(None, None)`.
- **The launcher's copy fails closed.** It raises `AuditStop` on a failed
  read.

**Why before the first headless run.** The audit is the run's history check:
it judges outcomes, not routes (WI-917's S3). So an off-procedure act by an
unattended leg is within its scope by design. The reviewers who found F1
judged it reachable only off procedure, and the owner ordered it fixed
before any headless run anyway (D-004). The owner kept the shared claim
reader in this row (D-005 C1), so the row also ships a fix to the merge slot.

## Deliverables

One lane, one landing. Each item names its ruling, and the builder writes the
rule in the target's own voice. Shipped files are marked, so the RESYNC entry
can list them.

1. **Trunk, bound once per run** (`scripts/coordinator/overnight_legs.py`;
   D-004's first item, wi-917 D-003 F1 and D-005; D-005 C2 and C3).
   - **The bind.** Before the first leg, alongside the run's other
     preparations, the launcher reads the trunk's name once. It reads it
     through the kit's one trunk reader, `agent_common.trunk_name(repo)`, and
     logs it in the run log (`run trunk <name>`).
   - **A refusal stops the run.** If the reader raises a `ValueError` (the
     shape of WI-925's `TrunkUndeclared`), the run stops before any leg, with
     exit 2, printing the reader's message, like the block and CLI stops.
   - **The launcher's own reader is deleted.** Its `trunk_name`, which reads
     `symbolic-ref HEAD`, goes. Every launcher reading of trunk is the bound
     name:
     - the audit's trunk rule;
     - the audit's exclusion of trunk from the lane loop;
     - the lane rule's base tip;
     - the leg's log line, which prints the bound trunk's tips from the two
       snapshots, never `rev-parse HEAD`.
   - **The checkout stays on trunk.** The checkout's branch is compared with
     the bound name; it is never read as trunk. The comparison runs
     immediately before every leg (`pre_leg`) and as the audit's last
     judgement after it, after the refs are judged, so a refused commit is
     still named first. Each of these stops the run (exit 3), naming what was
     read:
     - the pre-leg snapshot does not hold the bound trunk (this catches the
       reader's last resort today, `"HEAD"` on a detached primary checkout);
     - the checkout's HEAD is detached;
     - its HEAD names another branch;
     - its HEAD cannot be read or parsed.

     The handoff read, the stop line, the progress check and the next leg's
     working directory then all read a checkout on the bound trunk.
   - **`check-lane`** reads trunk through the same reader at its own run, in
     place of the checkout's HEAD. If the reader raises, or names no local
     branch, `check-lane` exits 3 with "cannot judge", printing why. It
     judges from that branch's tip, as before.
2. **`archive/lanes` descends** (`overnight_legs.py`; D-004's second item,
   wi-917 D-005; D-005 C5). The audit holds the archive to the trunk's rule,
   with one difference: the archive may be created.
   - **Present before the leg:** it must still resolve after the leg, and
     descend from its pre-leg tip (`merge-base --is-ancestor`, checked). A
     rewind, a reset to a commit that does not descend from that tip, or a
     deletion stops the run (exit 3), naming the pre-leg tip. Its
     first-parent additions are then judged as today.
   - **Absent before the leg:** judged as today. A created archive's commits
     are judged over the commits no pre-leg branch reaches. An archive absent
     before and after reads `absent`.
   - **The plan decides the form.** The trunk rule and the archive rule may
     become one function over two refs, differing only in whether the ref may
     be created (PROCESS.md §3, "Consolidate, don't duplicate"). The plan
     states whether they do.
3. **The audit's binding, stated** (the launcher's docstring; D-004's third
   item, second part; wi-917 D-003 F2). The docstring gains the bound in the
   Trust section below (`**The bound.**`): what the two snapshots cannot see,
   and what the audit does not judge. The "Stops" paragraph names the new
   stops of deliverables 1, 2 and 5.
4. **The `coordinator-cycle` skill's headless-leg section** (kit source
   `project-trajectory/skills/coordinator-cycle/`, synced to `.claude/skills/`
   and `.agents/skills/`; `scope: this-repo`, so no RESYNC entry). Section
   7's sentence on the launcher's audit gains one clause. The launcher judges
   every leg against the trunk it bound at run start, and stops the run when
   a leg leaves the primary checkout on any other branch. A leg's work stays
   in lane worktrees.
5. **One checked claim reader, shared by the merge slot and the launcher.**
   D-004's third item, first part; wi-917 D-003 F3; D-005 C1. The files:
   - shipped: `project-trajectory/scripts/agent_common.py` and
     `project-trajectory/scripts/integrate.py`;
   - this repo's tooling: `scripts/coordinator/overnight_legs.py`.

   The deliverable has these parts:
   - **The reader.** It lives in `agent_common`, beside `claim_subject` and
     `claim_base`, so the claim grammar's readers share one module.
     - **The question it answers:** did the loop claim `branch`? The answer
       is yes when the newest commit on the handed trunk tip's first-parent
       line whose subject is the claim grammar for `branch` carries a
       well-formed `Loop-Session` trailer.
     - **The reading is unchanged.** It is the slot's `_loop_claimed` as it
       stands: the same subject match, the newest match first, the same
       trailer parse.
   - **Its failure is the one change.** A claim log git cannot read, or a
     record in it that the reader cannot parse, is unreadable, never
     unclaimed. A record with no commit id is unparseable, as the launcher's
     copy rules today.
     - **Three answers:** the result tells claimed, unclaimed and unreadable
       apart, and an unreadable answer names the read.
     - **The shape is the plan's.** It follows `claim_base`'s `(value,
       readable)` convention, or returns a refusal string.
   - **The slot.** `integrate._loop_claimed` is deleted. `_loop_window`
     reads the claim through the reader, from the slot's trunk tip
     (`_head(root)`, as today).
     - **An unreadable claim** returns `_loop_window`'s refusal ("nothing
       was merged", naming the read), as a range git cannot read does today.
     - **The rungs do not change.** Both already return that refusal:
       `_loop_trailer_refusal` and `_held_status_refusal`.
     - **The docstrings follow.**
   - **The launcher.** `lane_claimed` is deleted. `lane_refusal` reads the
     claim through the reader, from the trunk tip it is handed. An
     unreadable claim stops the audit, or refuses `check-lane`, naming the
     read, as today.
   - **The contract text.** `agent_common`'s `Contract IF-065:` docstring
     names the reader, as IF-065's data does after its amendment
     (Done-when).

## Trust

Written before the claim, answering S2 under `project-trajectory/PROCESS.md`
§3, "When a guard is owed". WI-917's `## Trust` section is the record for the
audit's carriers (the commits a leg adds, and the two ref snapshots), and
nothing below re-opens it. This row changes three of its bindings, and the
claim log's failure ruling at the merge slot. The ruling goes to the owner
to confirm or overrule (coordinator-cycle §1 and §5).

**The gate.** The after-leg audit decides whether the next leg starts, and
`check-lane` decides whether a leg lands a lane (WI-917). The merge slot's
trailer rung and held-status rung decide whether a loop lane merges (SR-209,
SR-208). This row changes what they judge against:

- the trunk is the one bound at run start;
- the checkout must stay on it;
- `archive/lanes` must descend;
- a claim git cannot read is a refusal at the slot, as it already is at the
  launcher.

Nothing here releases anything a run or the slot would otherwise refuse.

**Producers and write routes.**

- **The trunk's name:** `agent_common.trunk_name(repo)`, the kit's one trunk
  reader.
  - **Today** it answers with the branch the primary checkout is on, from
    the first block of `git worktree list --porcelain`. It falls back to the
    current branch, and then to `"HEAD"`.
  - **WI-925** makes it the name `docs/process.toml` declares, and has it
    raise `TrunkUndeclared` on every other shape.
  - **Failed shapes:** the reader raises; or it returns a name no local
    branch holds; or, with the primary checkout detached, its fallback names
    the `--repo` checkout's current branch. For `check-lane` run at a lane's
    worktree, that is the judged lane itself: a name that resolves but is
    not trunk, so `check-lane` judges an empty range and passes. That order
    is off procedure, it is not guarded in this row (decision D-009 records
    why), and WI-925's declared name ends it.
- **The checkout's branch:** whatever last switched the primary checkout.
  Under the procedure, nothing does: lanes live in their own worktrees, and a
  landing's squash runs on trunk.
  - **Read with** `git symbolic-ref -q HEAD`, through the launcher's checked
    `read`.
  - **Failed shapes:** a detached HEAD, a failed read, an unparseable ref, or
    another branch.
- **`archive/lanes`:** written by the landing recipe (recipes §3).
  - **The write:** `git commit-tree` with the old tip as first parent, then
    `git update-ref refs/heads/archive/lanes <new> <old>`. That update
    refuses if the tip moved meanwhile.
  - **A failed or refused update** leaves the old tip. Git moves a ref
    atomically.
- **The claim log:** the claim commits on trunk's first-parent line.
  - **The writer:** `integrate.claim`, through `bookkeeping._commit_object`.
    It writes the subject `agent_common.claim_subject` composes. Under the
    loop marker, the commit carries a well-formed trailer (LLR-248).
  - **Failed writes:** a refused claim writes no commit and cuts no branch.
    An interrupted ref update leaves trunk at its old tip or its new one.
  - **Failed reads:** the log read fails; or a record in it cannot be
    parsed.

**What the authority binds to.**

- **The trunk:** the name read once at run start, recorded in the run log.
  Every audit in the run judges that ref, whatever the checkout's branch.
- **The checkout's branch:** only as compared with that name, never as
  trunk.
- **`archive/lanes`:** its pre-leg tip, in the snapshot taken immediately
  before the leg.
- **The claim:** the newest claim commit for the branch on the first-parent
  line of the trunk tip the caller hands the reader.
  - The slot hands its own HEAD, which is its trunk by design.
  - The launcher hands the bound trunk's tip.
  - The reading's grammar does not change.
- **Everything else:** the two snapshots of `refs/heads/*` around one leg,
  within the bound below. `check-lane` binds to the lane's tip and the
  trunk's tip when it runs.

**The bound.** The launcher's docstring states it (deliverable 3).

- **What the snapshots cannot see:**
  - a branch created and deleted inside one leg;
  - any ref outside `refs/heads/` (tags, `refs/stash`, notes).

  Their commits reach a judged ref in only three ways:
  - as a first-parent commit of trunk or `archive/lanes`, which the audit
    judges;
  - as a commit of a branch the leg created or moved, which the lane rule
    judges;
  - as a merge's non-first-parent commits, the next item.
- **A merge's non-first-parent commits,** on trunk's or `archive/lanes`'
  first-parent line, are judged by no rule.
  - The archive's extra parents are lane tips, by the recipe.
  - A lane merged onto trunk is off procedure while landings are squashes
    after `check-lane`. Once WI-808 puts landings on the merge slot, the
    slot's trailer rung judges the lane it merges.
- **Which branches a leg may move.** The audit judges provenance only. A
  marked commit on a branch the lane rule reads as a person's (`main`
  included) passes it. The owner-held steps belong to the procedure (skill
  §7), not to the audit.
- **Until WI-925, `check-lane`** reads trunk at its own run: the branch the
  primary checkout is on at that moment, or, when the primary checkout is
  detached, the current branch of the `--repo` checkout. Two orders escape
  it:
  - a leg switches the primary checkout, runs `check-lane`, and switches
    back before its squash;
  - a leg detaches the primary checkout and runs `check-lane` with `--repo`
    at a lane's worktree, where trunk reads as the lane itself, the range
    is empty, and the lane passes.

  No supported workflow produces either order (PROCESS.md §6). WI-925's
  declared name ends both.

**Consumers and rulings.** Found by grep:

- over `scripts/coordinator` for `trunk_name`, `symbolic-ref`, `HEAD`,
  `ARCHIVE` and `lane_claimed`;
- over `project-trajectory/scripts` for `trunk_name(`, `archive/lanes`,
  `_loop_claimed`, `_loop_window` and `(bookkeeping)`.

**The run start, in `overnight_legs.py`.**

- **The bind.** If the reader raises, the run stops before any leg (exit 2),
  printing the reader's message.

**`pre_leg`, before every leg.** Each of these stops the run before the leg
(exit 3), naming what was read:

- the snapshot does not hold the bound trunk;
- the checkout's HEAD is detached, unreadable or unparseable;
- the checkout's HEAD names another branch.

A failed read is a stop, as today.

**`audit`, after every leg.** It judges in this order:

1. The bound trunk, under the unchanged rule.
2. `archive/lanes`:
   - present before, and absent after or not descending from its pre-leg
     tip: a stop, naming the pre-leg tip;
   - present before and descending: its first-parent additions judged as
     today;
   - absent before: judged as today.
3. Every other branch the leg created or moved, from the bound trunk's
   post-leg tip (unchanged). Its claim is read through the shared reader:
   - claimed or unclaimed reads as today;
   - unreadable is a stop, naming the read.
4. The checkout's HEAD, as in `pre_leg`.

A failed or unparseable read stops the run, naming the read (unchanged).

**The reads after the leg** (`newest_handoff`, the lease, the progress
check). They run only after the audit passed, so they read a checkout on the
bound trunk. A failed handoff read already stops the run ("no handoff
found", or "wrote no new handoff"). A lease that cannot be read reads as
held, which also stops it.

**`check-lane`.**

- If the trunk reader raises, or names a branch that does not resolve,
  `check-lane` exits 3 with "cannot judge", printing why. It judges from
  that branch's tip.
- An unreadable claim is also exit 3, "cannot judge", naming the read.
- The detached-primary shape under **The trunk's name** above is not one of
  these: its name resolves, so `check-lane` judges the lane from its own tip
  and passes. It is off procedure and not guarded here (decision D-009).

**The merge slot's rungs** (`project-trajectory/scripts/integrate.py`).

- **Which rungs:** `_loop_trailer_refusal` and `_held_status_refusal`. Both
  read the claim through `_loop_window`.
- **The claim's three answers:**
  - **Absent** (no claim commit for the branch on trunk's line): unclaimed,
    as today. The window then opens only at a marked loop-writer commit.
  - **The newest claim carries no trailer, or a malformed one:** unclaimed,
    as today. Under the marker, the claim writer adds a well-formed trailer,
    and `mark_loop_process` replaces a malformed marker.
  - **Unreadable** (the log read fails, or a record cannot be parsed): a
    refusal from both rungs, "nothing was merged", naming the read. Before
    this row it was unclaimed.
- **A range git cannot read** is refused, as today.

**Not consumers, checked:**

- **The kit's other trunk readers:** `agent_common.default_base`,
  `agent_brief`'s trunk slot, `agent_loop`, `gen_verdict_rollup`,
  `handback._lane_verdict`, and `integrate.staged_done_when_refusal` to
  `kitlib/done_when.staged_hold`. WI-925's Trust section lists them, and this
  row does not change them.
- **The merge slot's trunk,** which it reads as the HEAD of the checkout it
  runs in (`integrate._head`). Neither this row nor WI-925 changes it.
- **The claim grammar's other readers.** Each reads the exact claim subject
  for another purpose, each fails closed, and none changes:
  - `agent_common.claim_base`, which returns `(None, False)` when it cannot
    read;
  - `agent_common._is_claim_move`;
  - `integrate._abandoned_claim`, where any failure means "not abandoned";
  - `claim_base`'s callers in `dispatch` and `agent_loop`, whose `None`
    meets the merge gate's own refusal.

## Done-when

- Every deliverable above is in its target, each citing the ruling it
  carries.
- **Launcher tests** (`tests/test_overnight_legs_git.py` on real git,
  `tests/test_overnight_legs.py` in process). Each fails on the code before
  the change unless it is marked as a pin:
  - **A leg that leaves the primary checkout off trunk.** A leg that ends
    with the primary checkout on another branch stops the run after that leg
    (exit 3), naming the branch, and no later leg runs. Before the change,
    the next leg ran from that branch's handoff. Its audit judged that branch
    as trunk and passed an unmarked commit on the real trunk.
  - **The bind.** Over two legs, the trunk reader is called once. The run
    log names the bound trunk, and the launcher has no trunk reader of its
    own.
  - **A refusing reader.** A trunk reader that raises a `ValueError` stops
    the run before any leg (exit 2), printing its message.
  - **A name no local branch holds.** A bound name absent from the pre-leg
    snapshot stops the run before the leg (exit 3), naming it. This one is a
    pin: today's detached-HEAD refusal stops the run there too.
  - **`check-lane` from the lane's own worktree.** Run with `--repo` set to
    a linked worktree of the lane, `check-lane` judges from the trunk the
    kit's reader names, and refuses the lane's unmarked commit (exit 3).
    Before the change, it judged from the lane's own tip and passed.
  - **The archive.** A leg that rewinds `archive/lanes` to an ancestor of
    its pre-leg tip stops the run (exit 3), naming that tip. So does a leg
    that resets it to a commit that does not descend from that tip, or
    deletes it. Before the change, each passed.
  - **Pins:**
    - a leg adding a marked archive commit on top runs the next leg;
    - an archive the leg creates is judged over the commits no pre-leg
      branch reaches;
    - a failed descent read stops the run, naming the read;
    - a failed claim read in the audit or in `check-lane` stops the run, or
      refuses the landing, naming the read. Today's copy fails closed too;
      the existing claim-read cases keep passing through the shared reader.
  - **The log line.** The leg's log line names the bound trunk's pre-leg and
    post-leg tips.
  - **In-process pins.** Each new rule has an in-process pin in
    `tests/test_overnight_legs.py`, so the smoke tier carries it. The
    real-git module is in `tests/conftest.py` `SLOW_MODULES`.
- **Claim-reader tests** (`tests/test_loop_provenance.py`). Each fails on the
  code before the change unless it is marked as a pin:
  - **The slot, with the claim log unreadable.** A loop-claimed lane holding
    an unmarked commit, whose claim log git cannot read (the claim read
    alone failing), is refused by the trailer rung, naming the read, and
    nothing is merged. The held-status rung refuses the same lane in the
    same way. Before the change, both read it as a person's lane and passed
    it (reproduced at drafting).
  - **An unparseable claim-log record** is unreadable at the slot, never
    unclaimed.
  - **Pins, on a readable log:** the reader's answer is unchanged.
    - a marked newest claim reads as claimed;
    - an unmarked or malformed newest claim, or no claim at all, reads as
      unclaimed;
    - another branch's claim is not read.
  - **One reader.** The slot and the launcher read the claim through the one
    reader: `integrate._loop_claimed` and the launcher's `lane_claimed` are
    gone.
- **The docstrings.** The launcher's states the new stops and the bound
  (deliverable 3). `integrate`'s and `agent_common`'s state the reader's
  failure rule.
- **The skill copies** in `.claude/skills/` and `.agents/skills/` match the
  kit source (`bootstrap.py --dest . --sync`).
  `check_docs.py --root . --strict-orphans` passes.
- **Spine, authored in the lane and judged at its checkpoint sitting.** The
  act is taken through WI-912's act turn, and SR-209 is unchanged.
  - **LLR-248 amended.** Its detail gains, in capability voice: a lane's
    claim record that cannot be read is a refusal, never a lane the loop
    did not claim. Its `code_symbol` cell names the shared reader in place
    of the slot's copy.
  - **TC-242 amended.** Its method gains the unreadable-claim case at the
    merge ladder: the loop lane is refused, naming the read, and nothing is
    merged. Its expected gains the same outcome.
  - **IF-065 amended.** Its data gains the reader, the shared primitive the
    integrator now reads a lane's claim through. The row is Drafted, so the
    edit takes no act.
- **`RESYNC_PACK.md` carries one entry,** anchored at the landing's parent.
  - The entry names `agent_common.py` and `integrate.py` as the kit-owned
    files to overwrite.
  - No migration is forced: an adopter's slot reads every lane as before,
    and refuses only where git cannot read the claim log.
  - The entry is written in the lane's first commit that touches a
    kit-owned file, since the bar's `check_resync` refuses the commit
    without it (WI-916).
- **The module-size ratchet's exact baselines** for `agent_common.py` and
  `integrate.py` are re-stamped
  (`tests/test_module_size_ratchet.py`).
- The lane's plan is produced after the claim and passes the plan gate (S4).
- **The bar is green on the landing tip:**
  - the smoke tier within its budget;
  - `check_trajectory.py --strict` clean;
  - `trace.py --strict` clean.

## Scope answers

- **S1: one landable unit, kept together by the owner** (D-005 C1, D-004).
  - **Deliverables 1 to 4 are one construction.** The bind, the checkout
    comparison and `check-lane`'s reader make one trunk name serve every
    reading. The archive rule shares the audit and its tests. The docstring
    and the skill clause describe both.
  - **Two parts could land alone:**
    - **the archive rule (deliverable 2);**
    - **the shared claim reader (deliverable 5).** It is the only shipped
      part. The owner kept it in this row over the coordinator's
      recommendation to split it (D-005 C1).
  - **Which lands first, inside the lane.** The reader's extraction from
    `integrate` into `agent_common` is a behaviour-preserving move, in a
    commit of its own (PROCESS.md §3). It comes before the commit that makes
    the reader checked and points the launcher at it. The plan orders the
    launcher's own commits.
- **S2: yes.** See `## Trust`.
  - **Already gates:** the audit and `check-lane` decide whether the next
    leg starts and whether a leg lands a lane. The slot's two rungs decide
    whether a loop lane merges.
  - **What changes:** the trunk's identity, the checkout's branch,
    `archive/lanes`' pre-leg tip, and the claim log's failure ruling at the
    slot.
- **S3: closed by construction, and by enumeration with deny by default.**
  - **The trunk:** one name, read once. The launcher keeps no reader of its
    own, so every reading is that name: the audit's three uses, the log line
    and `check-lane`.
  - **The checkout:** four states (on the bound trunk, on another branch,
    detached, unreadable). Only the first passes.
  - **`archive/lanes`:** five transitions, each with its ruling:
    - absent to absent: `absent`;
    - absent to created: judged as today;
    - unmoved: passes;
    - present to a descendant: its first-parent additions judged;
    - any other (an ancestor, an unrelated commit, deleted): refused.
  - **The claim:** three answers (claimed, unclaimed, unreadable), one
    reader, two callers.
    - Unreadable is a refusal at both.
    - The grammar that decides claimed or unclaimed does not change.
  - **The bound** (Trust) is stated in PROCESS.md §6's terms. The routes
    outside it are a hand act the procedure forbids, or an order no
    supported workflow produces.
  - **In flight:** no headless run has started (D-004). At the slot, a lane
    whose claim log reads reads as before.
- **S4: `single`.** Each of these alone makes it so:
  - the row has a Trust section;
  - it touches two script families: the launcher, and the kit's coordinator
    family (`agent_common`, `integrate`);
  - it changes an interface seam (IF-065);
  - it promises behaviour over an input space: every state the checkout,
    the archive and the claim log can be left in.
- **Architectural delta (S5): yes, carried within scope.** No preparatory
  refactor is needed beyond the reader's extraction, which is its own commit
  (S1).
  - **A new state:** a run holds a bound trunk for its lifetime.
  - **New domain values:**
    - two new launcher stops, a checkout off the bound trunk and an archive
      that does not descend;
    - one new slot refusal, an unreadable claim.
  - **Outputs depend on new inputs.** The audit and `check-lane` take
    trunk's identity from the kit's reader. The audit also compares the
    checkout's branch.
  - **A seam changes.** The claim reader moves to `agent_common`, so the
    integrator reads it across IF-065, which IF-065's data then names.
    `integrate` and `agent_common` are both CMP-008, so no component
    boundary is crossed.
  - **A non-kit caller.** The launcher calls `agent_common`'s trunk reader
    (IF-179's surface) and the claim reader. It is not a kit component, so
    no registry row names it, as in WI-917.
- **B3 and B4:**
  - **B3:** this row removes a re-derivation. Trunk is read once, at the
    event that starts the run, and recorded in the run log. No later leg
    re-reads it from the checkout. The archive's descent is judged against
    the pre-leg tip that the launcher recorded immediately before the leg.
    The claim stays read from the record written at the event (the claim
    commit). An unread record is a refusal, never a re-derived answer.
  - **B4:** no Done-when item needs an owner act or credential.
    - LLR-248 and TC-242 sit on rungs this repo's dial releases, so their
      amendment act is the adjudicator's. IF-065 is Drafted.
    - The first headless run stays the owner's to start (D-004), so it is
      not a Done-when item.
- **Dependencies (S6):**
  - **`needs` WI-917, hard (landed).** This row amends WI-917's audit,
    `check-lane` and Trust section.
  - **`~WI-918`, soft.** Both rows are claimed under one scoped unpause, so
    the edge is soft (recipes §2).
    - **Shared code:** both edit `integrate._loop_window`'s neighbourhood.
      WI-918 may hand the window reader each commit's parents and tree; this
      row changes the window's claim read and deletes `_loop_claimed`, which
      WI-918's Trust names as "not a consumer, checked".
    - **Shared spine rows:** both amend LLR-248 and TC-242. The second to
      land rebases onto the first and re-sits them.
    - **Shared text:** both edit skill §7.
    - **Boundary:** WI-918 owns `provenance.loop_lane_window` and the inputs
      each caller hands it, the launcher's `lane_refusal` included. This row
      owns the claim read and leaves the window call to WI-918.
    - **WI-918's spec is amended at its claim** by the coordinator (D-005
      C4). It then names the launcher's `lane_refusal` and `check-lane` as
      callers of the window reader, with a Done-when line that `check-lane`
      reads a re-claim as the merge slot does.
  - **Before WI-925, by D-004's order.**
    - **No launcher edit there.** WI-925 re-points `agent_common.trunk_name`
      at `docs/process.toml`'s `trunk` key. The launcher then follows with
      no edit: its bind and `check-lane` already stop on the reader's
      `ValueError`, which is WI-925's deliverable-2 rule for every caller.
    - **WI-925's rebase onto this row** adds `overnight_legs.py` to its
      Trust consumer list. Its one fixture helper (its deliverable 8) gives
      `tests/overnight_legs_fixtures.py`'s repositories the key. The
      coordinator records both at that rebase.
  - **A mechanism change.** It changes the launcher, which headless legs
    run on, and the merge slot's claim read, so it lands alone.
    - **The attended cycle runs neither.** Coordinator landings are hand
      squashes until WI-808, and coordinator-2026-10-18 D-001 read WI-917's
      launcher the same way. So this row holds no later attended landing
      behind it.
    - **First exercised:** the launcher's changed steps by the first
      headless run, which the owner starts; the slot's by its first landing
      of a loop lane.
  - **Later rows, not edges:** WI-808 first puts coordinator landings on the
    slot, where this reader then binds a coordinator lane.
  - **No third-party dependency.**

## Calls ruled at filing

The owner ruled C1, C3, C4 and C5 in session, one at a time, on 2026-10-18.
C2 is the coordinator's own call. All five are recorded in
`docs/decisions/coordinator-2026-10-18.toml#D-005`, with their options and
reasons.

- **C1: the one checked claim reader shared with the merge slot.**
  - **The options:**
    - (a) keep it in this row;
    - (b) split it into its own row, filed on trunk with `~WI-918`;
    - (c) leave it in the unfiled follow-ups.
  - **The coordinator recommended (b).** The fail-open is the slot's, and
    no headless leg reaches that slot before WI-808. Keeping it makes this
    gate row a shipped change.
  - **Ruled (a).** The row ships kit code, owes a RESYNC entry and the
    spine amendments its reader carries, and is judged at a checkpoint
    sitting (deliverable 5).
- **C2: where the bind reads trunk.**
  - **The options:**
    - (a) the kit's `agent_common.trunk_name`, once per run, with the
      launcher's own reader deleted;
    - (b) the launcher's own `symbolic-ref` read, once per run, re-pointed
      later by WI-925.
  - **The coordinator's call: (a).** It removes the second home now, and
    WI-925 needs no launcher edit.
  - **The cost:** until WI-925, the kit reader's fallbacks apply. With the
    launcher's default checkout they give the same answer, and the
    `pre_leg` snapshot check refuses their last resort, `"HEAD"`.
- **C3: stop the run when a leg leaves the primary checkout off the bound
  trunk,** checked before every leg and last in every audit.
  - **Ruled yes,** beyond D-004's literal "bind trunk once per run".
  - **Why:** the next prompt, the `Overnight: stop` line, the progress check
    and the leg's working directory all follow the checkout.
  - **The rejected option:** reading the handoff from the bound ref closes
    only the first three.
- **C4: WI-918's consumer list.**
  - **Ruled yes:** WI-918's spec is amended at its claim to name the
    launcher's lane audit and `check-lane` as callers of the lane-window
    reader, with a Done-when line that `check-lane` reads a re-claim as the
    merge slot does.
  - **Who does it:** the coordinator's edit to WI-918, not this row's.
- **C5: a deleted `archive/lanes`.**
  - **Ruled yes:** refused with a rewind or a reset, as part of the descent
    rule. The archive is append-only by recipe.
  - **What stays:** WI-917's "logged, not judged" rule for deleted lane
    branches.
- **Kept as Trust text, not a refusal:** the stated binding for a ref
  created and deleted inside one leg, and for a merge's non-first-parent
  commits on trunk (deliverable 3).

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-18; the spec as filed, its calls ruled):
APPROVE, no findings. Nothing to adopt, so no confirming round is owed and
the row may be claimed.
