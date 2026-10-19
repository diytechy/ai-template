+++
id = "WI-925"
title = "The trunk is the branch the repository declares by name, and a spec move's own link redirect inside a claim copy's Done-when is not a Done-when change"
workstream = "process"
sr_refs = ["SR-156", "SR-170", "SR-137"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-921", "~WI-911"]
+++

## Deliverable

Closed at its landing on 2026-10-19, after its gate and act, in a headless
leg:

- The trunk is one declared name, `trunk` under `[policies]` in
  `docs/process.toml`, read by `agent_common.trunk_name` in any worktree; its
  fallbacks are gone, and an absent, non-string, empty or non-local value is
  refused naming the line. Every reader that judges or writes against the
  trunk refuses in turn (the worker preflight, the review, dispute and
  adjudication briefs, the reviewer's trunk slot, the rollup write, the
  partial close, the plan gate on a claimed lane, and the staged
  `done-when-blessed` step whenever a claim-copy change is listed); the step
  selection runs every opted-in step and the readability report skips naming
  the line. `default_base` is the merge base with the declared trunk. A
  scaffold writes the line from the branch it is scaffolded on, into a
  config the same run created. This repository declares `refactor_again`.
- A spec move's own relink is not a Done-when change: a claim copy's lone
  modification whose bytes are exactly the inbound relink of another
  specification's move into a terminal home in the same staged change, read
  by one shared stage (`spec_move.exact_relink`), which the claim
  recognizer, the plan gate and the staged reader all call.
  `staged_closes` is gone. The shipped hook's `done-when-blessed` comment
  states the promise and the one residue list, a claim's own relink
  included; the hold-by-rename finding names a recovery the trunk floor
  permits.
- Spine: new LLR-339 and TC-369, approved; LLR-307, LLR-208, LLR-337,
  TC-325, TC-206 and TC-367 amended (sitting 004-ADJUDICATE-6c9ac8f, all
  MEANING+BLESS), re-attested and approved by its act; IF-179, IF-189 and
  IF-286 aligned. `RESYNC_PACK.md` carries the entry, a forced migration,
  anchored at the landing's parent.
- Reviews: the single plan's two critiques and the cap's dispute sitting
  (001-ADJUDICATE-20a6044, DISMISS); counted round 1 (002-REVIEW-A, 2 MINOR;
  003-REVIEW-B, 1 MAJOR re-graded to the checkpoint and 6 MINOR) and the
  gate in convergence stance (005-REVIEW-A, 2 MINOR; 006-REVIEW-B, APPROVE
  with 2 MINOR, to status.md's follow-ups). Decisions:
  `docs/decisions/wi-925.toml` D-001 to D-011.

## Context

Filed on trunk at WI-921's landing as the successor the owner ruled in
wi-921 D-014. Re-scoped on 2026-10-15 by the owner's ruling
coordinator-2026-10-15 D-012: the row builds no reference-transaction hook.
It keeps three things a supported workflow reaches.

**The trunk's identity (the linked-worktree gap, wi-921 005 F4).**
WI-921's `done-when-blessed` step judges every Done-when change on trunk,
and only a close elsewhere. It learns which branch is trunk from
`agent_common.trunk_name`, which answers "the branch the primary checkout is
on", then the current branch, then the worker's base sha. Two supported
shapes read that wrong:

- a linked worktree on the real trunk while the primary checkout sits on
  another branch. The commit is read as "elsewhere", so a Done-when change
  that closes nothing is not judged, and a later close there compares
  against the edited copy (fails open);
- a single checkout switched to a branch not named for its claim. The
  current branch is read as trunk, so a Done-when change there is judged as
  trunk's and held (fails closed; the hook comment states it as residue).

The same reading feeds the lane base (`default_base`), the review brief's
trunk slot, `handback`'s lane-verdict lookup and the rollup's off-trunk
refusal. The fix is one declared name, read by every caller, with no
fallback.

**The relink (Q5; found by reading, not reproduced).**
`spec_move._relink_inbound_links` rewrites every inbound markdown link in
every `.md` file when a spec moves. That includes a link inside another
claimed row's claim copy, inside its Done-when section. `kitlib.done_when.changes`
reads a rewritten link target as a reworded item. So a squash landing whose
lane closed a row, or a hand close on trunk, can be held by WI-921's trunk
arm over a Done-when change nobody made, when another claimed row's
Done-when links the moved spec. The exact reading of a relink already
exists twice: `integrate._relinked_exactly` (the claim recognizer) and
`plan_gate._relinked` (the plan gate's close homes), both over
`spec_move.expected_relink`.

**Carried from WI-921's post-checkpoint gate** (wi-921 D-020). Each was
re-checked against the narrowed scope; each still has a home here:

- the residue lists in the shipped pre-commit hook's `done-when-blessed`
  comment and in WI-921's RESYNC entry omit the linked-worktree shape, and
  "One residue fails open" goes on to list five. Without the hook, the
  list's home is that comment and this row's RESYNC entry (deliverable 4);
- TC-325's method and expected never name the deletion-only pin its
  evidence cites (`test_a_trunk_commit_deleting_a_claim_copy_is_held_and_no_blessing_releases_it`).
  This row amends TC-325 anyway (deliverable 6);
- `kitlib.done_when.staged_closes` has no non-test caller, yet WI-921
  changed its return shape. WI-921 kept it for WI-922's carried-commit
  reader (wi-921 D-007, the plan's call C4), and D-013 dropped that reader. The row
  deletes it (deliverable 5; call C1);
- `check_trajectory`'s hold-by-rename finding still offers "delete the
  stranded claim". On trunk the floor refuses that commit, and no blessing
  releases it (deliverable 7).

**What becomes stated residue.** D-012 drops the hook. An amend, a
cherry-pick, a revert or a rebase onto trunk, a plain `git merge` of a lane,
and a hand fast-forward of trunk each need a hand act the process forbids or
one no landing recipe uses (a landing is one `git merge --squash`). So do
D-014's items 2 and 4. They are stated once, as residue, under PROCESS.md
section 6's threat model (deliverable 4).

## Deliverables

One lane, one landing. Shipped files are marked, so the RESYNC entry can
list them.

1. **The declared trunk** (shipped: `process.toml.template`,
   `agent_policy.py`, `bootstrap.py`, `agent_common.py`).
   - `docs/process.toml` gains one string key, `trunk`, in an existing
     section (the plan names it; no new section header). The template
     carries it with a comment saying what it names.
   - The kit schema reader registers it as a process-only `str` key, so a
     wrong type is refused by the config check, as for every dial.
   - Bootstrap writes it at scaffold from the branch being scaffolded on,
     through its in-place setter. An unborn repository gets the branch git
     will create.
   - `agent_common.trunk_name(root)` returns the declared name, or refuses.
     It reads no worktree list, no current branch and no worker base. The
     fallbacks are deleted, not kept behind a flag.
   - Deny by default. An absent key, a value that is not a string, an empty
     value, or a name with no `refs/heads/<name>` is refused by
     `trunk_name`, and the refusal names the key and the line to add.
2. **Every caller takes the one reading.** The callers found by grep:
   `agent_common.default_base` (and through it the worker preflight and the
   review brief slot), `agent_brief.py` (the reviewer prompt's trunk slot),
   `gen_verdict_rollup._off_trunk_refusal`, `handback._lane_verdict`, and
   `integrate.staged_done_when_refusal` (which hands it to
   `kitlib.done_when.staged_hold`). Each refuses, naming the key, when
   `trunk_name` refuses. `staged_hold` keeps asking for the trunk only when
   a claim-copy change is listed, so a commit that touches no claim copy is
   never refused over the key.
   - `default_base` keeps its claim-record arm only if the declared trunk
     still leaves it reachable. Its docstring's case (a single checkout
     switched to the lane branch, where the merge base "collapses to HEAD")
     arose from reading the current branch as trunk. The plan reads it and
     either deletes the arm or states the case that still reaches it.
3. **The relink is not a Done-when change** (shipped:
   `kitlib/done_when.py`, `spec_move.py`, `integrate.py`, `plan_gate.py`).
   - **Reproduce first.** The builder writes the fixture before any fix: a
     trunk with two claimed rows, where row Y's Done-when links row X's
     spec; X's lane closes through `spec_move` and lands by the squash
     recipe. If the landing commit is not held, this deliverable drops: the
     fixture stays as a pin that it passes, and the row records the result.
   - If it reproduces: in `staged_hold`, a claim-copy modification whose new
     bytes are exactly the inbound relink of a spec move the same staged
     delta carries is not a change. Anything else in that copy, a real edit
     beside a relink included, is still a change.
   - The exact reading is extracted once to one shared stage (0 to A to B,
     PROCESS.md section 3). `integrate._relinked_exactly`,
     `plan_gate._relinked` and the new caller all call it. The two existing
     copies differ (the plan gate also requires a non-empty rewrite); the
     plan states how the one stage serves both.
   - The fixture also checks the reach beyond the same delta (call C2).
4. **The residue text, in one list** (shipped: `hooks/pre-commit`'s
   `done-when-blessed` comment; and this row's RESYNC entry).
   - The promise: over supported routes (an ordinary commit, the squash
     landing, a hand close) a trunk commit is judged against its parent, on
     the declared trunk, in any worktree.
   - The residue, stated under PROCESS.md section 6:
     - an amend of a trunk commit is judged against the commit it replaces;
     - a cherry-pick, a revert or a rebase onto trunk runs no pre-commit
       hook;
     - a plain `git merge` of a lane that makes a merge commit runs no
       pre-commit hook (the merge slot's own merge is judged by the slot
       before it merges);
     - a hand fast-forward of trunk makes no commit;
     - if git fails mid-commit when the step asks whether it is in a work
       tree, the step reads "off a work tree" and judges nothing (D-014
       item 2);
     - the merge-time mint skips, without a word, a closed spec it cannot
       read or parse, which needs a forbidden hand act on trunk (D-014
       item 4);
     - on a detached HEAD, a Done-when change that closes nothing is not
       judged (D-008 item 3; coordinator-2026-10-15 D-020).
   - The fail-closed residue that stays: no route returns a claimed spec to
     the queue, so a hand return or re-cut of a claim copy on trunk is held.
   - Gone: the linked-worktree shape and the single-checkout shape, both
     closed by deliverable 1. "One residue fails open" is rewritten so its
     count matches its list.
   - The list lives in the hook comment. LLR-307 states the promise's bound
     and points to it, rather than listing the shapes a second time.
5. **`staged_closes` deleted** (shipped: `kitlib/done_when.py`; per call C1).
   It goes from `__all__`, the module docstring and the `Contract IF-286`
   text. Its two test assertions move to `staged_changes`.
6. **TC-325** names the deletion-only pin in its method and expected, and
   gains the cases of deliverables 1 and 3.
7. **The hold-by-rename remedy** (shipped: `check_trajectory.py`). The
   finding stops offering "delete the stranded claim". It names a recovery
   the floor permits; the plan reads `handback` and names it (for example,
   restoring the branch ref at the claim commit, then closing partial).
8. **This repository.** `docs/process.toml` declares this repository's
   trunk. `tests/test_dogfood_sync.py` holds the key's structure against the
   template. Test fixtures that run a trunk reader gain the key through one
   helper, not a copy per test.
9. **`RESYNC_PACK.md`**, one entry, anchored at the landing's parent:
   - **forced migration:** add the `trunk` line to `docs/process.toml`.
     Until it is there, every route that reads the trunk refuses and names
     the line. `process.toml` is never replaced; this is a new setting the
     adopter takes;
   - the residue list (deliverable 4), replacing what WI-921's entry said;
   - `staged_closes` is gone;
   - the kit-owned files to overwrite, as one set, which the plan lists.

## Trust

Deliverable 1 gives `docs/process.toml`'s `trunk` key authority over a hold
and a gate. It decides which arm of the `done-when-blessed` step judges a
commit, whether the rollup generator refuses a write, and which base a
lane's evidence is read from. This is a trust boundary in the sense of
PROCESS.md section 3, "When a guard is owed". Every carrier WI-921's Trust
section lists keeps its producer, write route and failed-write shapes. That
section is the record, and nothing below re-opens it.

- **The carrier: the `trunk` key.**
  - Producers: bootstrap writes it at scaffold. The adopter writes it by
    hand, which is a supported route for this adopter-owned file. A resync
    adds it as a new setting (LLM-applied).
  - Failed-write shapes: the key is absent; `docs/process.toml` does not
    parse; the value is not a string; it is empty; it names no local
    branch.
  - Ruling for each: `trunk_name` refuses, naming the key. Every consumer
    below refuses in turn. None falls back to another reading.
  - Not caught: a value that names an existing branch that is not the
    trunk (a lane, say). The key is trusted as written, like every dial.
    The config check cannot know which branch the adopter means.
- **Consumers, found by grep** (`trunk_name(`):
  - `agent_common.default_base`, the worker preflight and the review brief
    slot;
  - `agent_brief.py` (the reviewer prompt's trunk slot);
  - `gen_verdict_rollup._off_trunk_refusal`;
  - `handback._lane_verdict`;
  - `integrate.staged_done_when_refusal` to `kitlib/done_when.staged_hold`
    to `_staged_base`.
- **The relink exemption (deliverable 3)** adds no carrier. It reads the
  claim copy's old and new bytes and the move pair from the same staged
  delta, which WI-921's Trust already covers. It releases a change only on
  an exact byte match, so a hand edit that is not the ritual's write is
  still a change. A blob it cannot read, or bytes that do not decode as
  UTF-8, are not a match: the change is judged.

## Done-when

- **The trunk, declared.** Each case fails before the change:
  - on a fixture with a linked worktree on the declared trunk while the
    primary checkout sits on another branch, a trunk commit that changes a
    claim copy's Done-when unblessed is held, and passes once its tree
    carries a covering verdict or ruling;
  - in a single checkout switched to a branch not named for its claim, a
    Done-when change that closes nothing is not judged as trunk's;
  - with the key absent, not a string, empty, or naming no local branch,
    `trunk_name` refuses naming the key, and each caller in deliverable 2
    refuses in turn. A commit that touches no claim copy is not refused
    over the key;
  - the reviewer prompt's trunk slot renders the declared name, and the
    rollup's off-trunk refusal keys on it in a linked worktree.
- `trunk_name` reads no worktree list and no current branch: its fallbacks
  are gone, and a test pins that a repository with the key reads it and one
  without refuses.
- A bootstrapped scaffold carries the key, set to the branch it was
  scaffolded on. The config check refuses a non-string value.
  `tests/test_dogfood_sync.py` holds the key's structure.
- **The relink.** The reproduction fixture runs first, and its result is
  recorded in the lane's log. If it reproduces: the squash landing in that
  fixture is held before the change and passes after; the same landing with
  a real edit beside the relink is still held; and one shared stage holds
  the exact reading, called by the claim recognizer, the plan gate and the
  staged reader. The claim recognizer's and the plan gate's existing relink
  tests pass unchanged. If it does not reproduce, the fixture is kept as a
  passing pin and deliverable 3 is recorded as dropped.
- The shipped hook's `done-when-blessed` comment states the promise and the
  one residue list of deliverable 4, and no longer lists the linked-worktree
  or the single-checkout shape.
- `staged_closes` is gone, and no shipped file or test
  names it.
- `check_trajectory`'s hold-by-rename finding no longer offers deleting the
  stranded claim, and names a recovery the trunk floor permits. A test in
  `tests/test_trajectory_holdban.py` pins the new text and fails before.
- Spine, judged at the lane's checkpoint sitting:
  - LLR-307 amended: the trunk is the declared branch, in any worktree; the
    residue sentences become the promise's bound, pointing to the one list;
    the relink exemption is stated (if deliverable 3 stays); the sentence on
    the close listing's unreadable reason goes;
  - LLR-208 amended: the off-trunk refusal keys on the declared trunk, not
    the primary checkout's branch;
  - one new LLR under SR-156, with a TC, for the declared trunk (proposed
    text in `## Scope answers`);
  - TC-325 amended (deliverable 6);
  - IF-179 and IF-286, both Drafted, amended to match;
  - LLR-145's, LLR-151's and LLR-337's `code_symbol` cells follow the
    shared stage if it moves a symbol;
  - unchanged: SR-156, SR-170, SR-137, SR-019, LLR-309, TC-326.
- `RESYNC_PACK.md` carries the entry of deliverable 9.
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, `trace.py --strict` clean.

## Scope answers

- **S1: two independently landable deliverables, kept together.**
  - Q3, the declared trunk (deliverables 1, 2, 8, and the residue rewrite in
    4), could land alone.
  - Q5, the relink (deliverable 3), could land alone, and may drop after
    its fixture.
  - They share no function. Q3 changes `agent_common` and its callers, the
    schema reader and bootstrap; Q5 changes the staged reader and extracts
    a stage from `integrate` and `plan_gate`. The hook coupled them; without
    it, neither needs the other.
  - They share spine rows: both amend LLR-307 and TC-325, and both write
    the hook comment and a RESYNC entry. Split, LLR-307 would sit twice.
  - The four MINORs ride with whichever part owns their surface: the
    residue list and TC-325 with Q3, `staged_closes` with Q5's reader, the
    hold-by-rename text with either.
  - D-012 weighed the split ("Q3 alone, with Q5's relink filed as its own
    row") and ruled them together. So: one landing. If the critique splits
    them anyway, Q3 lands first, because it is the forced migration and
    the residue rewrite depends on it; Q5 follows as its own row, filed on
    trunk.
- **S2: yes.** See `## Trust`: the `trunk` key gains authority over the
  done-when hold's arms, the rollup's refusal and the lane base.
- **S3: closed by construction.**
  - The trunk is one declared name. Its reader refuses every shape but a
    non-empty string naming a local branch. No branch-reading fallback
    remains, so the set of checkouts and worktrees is irrelevant.
  - The relink exemption is one exact byte comparison. Every other
    modification of a claim copy stays a change (`classify_delta`'s deny by
    default is unchanged).
  - The bound, in PROCESS.md section 6's terms: the promise covers the
    supported commit routes onto trunk (an ordinary commit, the squash
    landing, a hand close) in any worktree. The routes in deliverable 4's
    residue list are outside it, stated once.
- **S4: `single`.** The row has a Trust section, touches several script
  families (`agent_common`, `kitlib/done_when`, `integrate`, `plan_gate`,
  `spec_move`, `agent_policy`, `bootstrap`, `check_trajectory`) and changes
  two interface seams (IF-179, IF-286).
- **Architectural delta (S5).**
  - A new domain value: the declared trunk name replaces the primary
    checkout's branch as the trunk's identity for every caller.
  - Outputs depend on a new input: the done-when step, the rollup refusal
    and the lane base read the key.
  - No new boundary and no new state. The one preparatory refactor is the
    shared relink stage, extracted in its own commit before its new caller.
  - Proposed new LLR text (capability voice): "The integration branch is
    named by one declaration in the policy home, read by every reader that
    needs the trunk. A checkout on that branch is the trunk whether it is
    the primary checkout or a linked worktree. An absent, non-text or empty
    declaration, or one that names no local branch, is refused by every
    reader, naming the declaration; no reader falls back to the branch a
    checkout is on."
- **Dependencies (S6).**
  - `needs = ["WI-921", ...]`: WI-921 has landed; this row extends its
    reader, its hook comment and its TC row.
  - `~WI-911` (soft): the residue list cites PROCESS.md section 6's
    plausibility text, which WI-911's lane adds, and the fresh critique
    runs under that language (D-009, D-012).
  - WI-922 (claimed, narrowed by D-013) writes its own residue into the
    same hook's comment block and IF-295, and deletes `_cap_problems` from
    `plan_gate` (LLR-337's `code_symbol`), beside this row's relink
    extraction. The two share no function. Whichever lands second rebases.
    D-013 also makes D-008's item 3 (a detached HEAD, where the step judges
    no non-close change) stated residue; by call C3 this row's list holds
    it, and WI-922's lane does not touch the `done-when-blessed` entry.
  - WI-926 (queued) changes the same hook's exit when it cannot find the
    kit scripts (D-014 item 5). No shared function; the hook comment may
    need a rebase.
  - No third-party package, tool or service.
- **B3:** the trunk is read from its declaration at the moment of asking,
  not recomputed from history. The relink exemption compares the staged
  bytes with the ritual's own output for the move in the same delta; it
  searches no history.
- **B4:** no Done-when item needs an owner act or a credential. The
  forced migration is an adopter's act after the landing, named in the
  RESYNC entry.

## Calls ruled at filing

The owner ruled these two calls in session, each as recommended
(2026-10-15, the attended coordinator session that landed WI-921). Each
keeps its options and reasoning. The other six (Q1, Q2, Q4, Q6, Q7, Q8)
dropped with the hook (coordinator-2026-10-15 D-012).

- **Q3: the trunk's identity.**
  - (a) A declared `trunk` key in `docs/process.toml`, read by
    `agent_common.trunk_name` for every caller. Bootstrap writes it, and a
    resync adds it. Absent, it holds the commits it is needed for.
  - (b) The key is read only by the new hook, and `trunk_name` is unchanged.
  - (c) No key: keep the primary checkout's branch and state the
    linked-worktree residue.

  **Ruled (a), as recommended.** (c) leaves 005 F4 open. (b) creates two
  trunk identities that can disagree, which is a second home for one fact.
  (a) **forces a migration**: every adopter adds one line, and an adopter
  who skips it is refused, naming the key. It also changes an input of six
  callers. It is still one rule, deny by default, with no fallback to the
  old reading (the owner's 2026-10-03 rule: fix the single point of
  failure). D-012 kept it because a supported workflow, a linked worktree on
  trunk, reaches the gap.
- **Q5: the relink reading.**
  - (a) Fix it here: a claim-copy edit that is exactly the inbound relink of
    a move in the same delta is not a Done-when change, through the existing
    exact reading, extracted once.
  - (b) File it as its own row before this one.
  - (c) Leave it: such commits are held, and an owner ruling releases each.

  **Ruled (a), as recommended.** (c) puts the cost on the owner for a
  change nobody made. One caution: the finding is from reading the code.
  The builder confirms it with a fixture before building the fix, and if it
  does not reproduce, the deliverable drops (D-012 kept this condition).
- **C1: `staged_closes`, now with no planned caller.** WI-921 kept it for
  WI-922's carried-commit reader, which D-013 dropped.
  - (a) Delete it. Construction first: no code path is better than an
    unused one. The cost is an adopter-visible removal, named in RESYNC;
    nothing in the kit calls it.
  - (b) Keep it and state in IF-286 that it has no kit caller.

  **Ruled (a) by the coordinator, coordinator-2026-10-15 D-020, for the
  owner to confirm or overrule.**
- **C2: a relink the same delta does not carry.** Deliverable 3's exact
  reading needs the move in the same delta. A relink can also reach a claim
  copy later: a lane that refreshes from trunk takes trunk's relinked copy,
  so its build hold and merge slot compare the claim (before the relink)
  with the relinked copy; and the merge-time mint compares the same pair
  when that row closes. The fixture checks both.
  - (a) If either reproduces, state it as residue: an owner ruling releases
    each. The row's ruled fix is the same-delta reading, and the case needs
    a link inside one claimed row's Done-when to another claimed row's spec.
  - (b) Widen the fix: compare Done-when items with link targets ignored
    (link text only), at every hold point. One change in one function, but
    a retargeted link is then never judged.

  **Ruled (a) by the coordinator, coordinator-2026-10-15 D-020, for the
  owner to confirm or overrule.**
- **C3: where the detached-HEAD residue is stated.** D-013 makes D-008's
  item 3 (a detached-HEAD Done-when change the step judges as nothing)
  stated residue, written by WI-922's lane "in the hook comment". It is a
  `done-when-blessed` shape.
  - (a) This row's one list (deliverable 4) carries it, and WI-922's lane
    does not touch that entry: one list.
  - (b) WI-922 writes it, and whichever lands second merges the two lists.

  **Ruled (a) by the coordinator, coordinator-2026-10-15 D-020, for the
  owner to confirm or overrule.**

## Critique dispositions

The two earlier rounds (coordinator-2026-10-15 D-006 and D-009) judged the
reference-transaction hook's design, which D-012 dropped. Their findings do
not apply to this scope. A fresh scope critique under PROCESS.md section 6's
new language follows before any claim.
