## 2026-08-01 — WI-387: three terminal outcomes, so a branch cannot hang

**Summary.** "WIs always land back in trunk; branches never hang" was a rule
someone had to follow. It is now a property of the tree.
[`concurrency-v2.md`](../concurrency-v2.md) §A3's three outcomes — **merged**,
**cancelled**, **handback** — are all merges, and a lane declares which one it
reached by the *directory it moved its claimed specs into*, which is the same
move that already made the branch finished. One fact, read twice; no fourth
option and no state file that could hold one. Two run-stops die with it (the
`EXIT_NEEDS_HUMAN` stop and the parked-branch stop), and so does
`drive._stranded_claims`, whose entire reason for existing was an ordering in
`integrate.claim` that this row inverts.

**Deliverables.**

- **The outcome is the folder.** `integrate.OUTCOME_DIRS` +
  `branch_outcomes(root, branch)` read the branch's own tree: `complete/` →
  `merged`, `cancelled/` → `cancelled`, any open folder (`queued/`, `draft/`,
  `deferred/`) → `handback`. A claimed spec that landed in no declared
  directory — or in **more than one** — resolves to *nothing* and
  `integrate_one` refuses on it. Both halves matter and only one was there in
  round 1: a basename-keyed dict let a spec left in two folders resolve by
  alphabetical last-wins, which put `queued` (handback, no verdict owed) ahead
  of `complete` (merged, an APPROVE owed) — a contradiction resolved silently
  toward the answer that *skips the gate*, with fail-closure depending on an
  unrelated duplicate-id rung in another script. Per-basename outcome **sets**
  now put it where the outcome is read. The merge commit and the console line
  name the outcome per id (`integrate: wi-401 merged (WI-401=handback)`), so a
  walk-away run cannot report a return as a completion.
- **The verdict gate is keyed off the OUTCOME, not the claim.** `_verdict_gate`
  took `wi_ids` from trunk's `active/<branch>/` and demanded an `APPROVE` for
  every one — but a handback leaves those ids claimed at merge time, so as
  written it demanded an approval for work being *returned*. Only `merged`
  asserts done and owes a verdict. This is not cosmetic: a review escalation is
  the commonest handback cause, so the unfixed gate would have deadlocked the
  common path on itself.
- **The claim is inverted: `write-tree`/`commit-tree` → `git branch` → advance
  trunk.** Trunk-first had a window between the two REF writes that left a
  claim no lane could reach — invisible to the frontier (the WI is no longer
  queued) and to the parked-resume read (no ref) — which cost an exit-2 refusal
  and hand repair. Branch-first moves that window to the benign side: a crash
  leaves at worst an orphan branch whose claim commit is not an ancestor of
  trunk while its WI is still `queued/`, which `_abandoned_claim` convicts and
  the next claim deletes and re-cuts, printing the sha and its restore command.
  **`drive._stranded_claims`, its exit-2 refusal and its test are deleted.**
  `_abandoned_claim` authorises a `git branch -D`, so it convicts on **four**
  facts, not three: the tip's subject is `_claim_subject(wi_id, branch)`
  **exactly**; the tip is not an ancestor of trunk; its parent is; and the
  commit **is the move this claim would make** — it ADDS this WI's spec under
  `active/<branch>/` and touches nothing but that move and declared generated
  paths. The fourth fact took two rounds to get right. Round 1 inferred it from
  ancestry, which proves only *one commit ahead*, not *carrying nothing*, so a
  hand-written `wip: nearly done -> active/wi-401 (bookkeeping)` was deleted
  with its work on it. Round 2 replaced that with "only the RULING-6
  bookkeeping surfaces" — still too wide, and round 2's review drove a commit
  adding **only** a `WI-401-hours.md` log fragment being convicted and that
  fragment lost, plus the same for a `docs/log.md` rewrite and a hand-written
  `PROJECT_STATE.html`. The rule is now what the claim actually writes, and the
  spec move is REQUIRED rather than merely permitted, so a regeneration that
  moved no spec is not a claim either. Six negatives now fail if any one fact
  is dropped. The `git branch -D` that acts on the verdict **reads its return
  code** and names the holding worktree: it refuses a branch a worktree has
  checked out, and round 2 printed `deleted the abandoned claim branch …` over
  a branch that still existed — the same reports-success-on-failure shape as
  the rename mis-parse, eight lines away.
- **`handback.py`, a new sibling kit script** (`hand_back` + `quarantine`):
  - `hand_back` commits the work so far **as-is** (`--no-verify` — "as-is" has
    to mean it, and the branch's own §A2 refresh regenerates and bars this tree
    before anything merges), moves each claimed spec back to `queued/` with a
    `## Handback` section naming what remains and **the commit range it lives
    in**, and sets `blockref` to the spec's own path.
  - The blockref is load-bearing, not decoration: `schedule._disposition` reads
    queued+blockref as `blocked`, so a returned WI leaves the ready frontier
    until a human clears it. Without it the driver would claim, hand back and
    re-claim the same WI forever — and because each handback *merges*, trunk
    would move every cycle and the stall guard would never fire.
  - `quarantine` is the ruled red arm (owner decision 1): revert the product
    paths to the merge base, keep the failing diff as a bar-inert `.patch` in a
    `handback/` directory under `docs/work/`. Nothing is lost — the reverted
    commits stay reachable in trunk history once the branch merges — and
    nothing is live.
    Bookkeeping paths (`docs/work/`, `docs/log.d/`) are exempt by construction:
    reverting them would revert the handback itself.
  - **It reads `--name-status -z` as RECORDS, not pairs.** `diff.renames` has
    defaulted true since Git 2.9, so `R<score>`/`C<score>` are ordinary output
    and each emits **three** fields. Round 1 paired two at a time: the stream
    desynchronised at the first rename, paths were read as statuses, the
    bookkeeping filter went blind, the failing file fell past the loop bound,
    and the run printed a confident *"4 path(s) reverted"* over a branch that
    still held it — while four no-match git calls had their **return codes
    discarded**. A rename is now two undo steps (remove the new path, restore
    the old), a truncated stream refuses rather than quarantining a partial
    list, every revert step's code is checked and a failure resets the lane to
    its tip, and the artefact is staged **by name** instead of `git add -A`.
- **`drive.py`: the decision, not the write.** `_worker_stop_code` is replaced
  by `_lane_close`. A *decided* worker exit (`_WORKER_OUTCOMES`) hands back and
  the run continues; a **crash** (any other code) is deliberately not a hang
  and keeps the parked-resume path exactly as it was, bounded by the stall
  guard. A lane that **already closed its specs** is left alone whatever it
  exited with: its tree has named an outcome and the drain merges it on that.
  Round 1 did not have that arm, and a review escalation lands at the *end* of
  a lane — so a decided exit after the close made `hand_back` read a spec out
  of an `active/` directory the lane no longer had, fail with an `OSError`, and
  stop the run over a branch that would have merged cleanly. `_drain` gained
  `_refresh_or_quarantine`: a red refresh still stops the run for a branch
  whose outcome asserts *done*, but a branch that merges nothing is
  quarantined once and refreshed again.
- **The `## Handback` section joined the spec body grammar** — `SPEC_HANDBACK`
  plus a four-line partition in `parse_spec_deliverable`, identical in all
  three F5 copies (`agent_common`, `check_trajectory`, `schedule`) and in
  `wi_convert`, which reads past it and does not reproduce it (it maps to no
  CSV column; `--verify` round-trips from a CSV and never sees one). **This is
  the change that made the section possible at all, not a nicety**: a sibling
  lane confirmed today that a body the grammar does not know makes the row
  **silently absent from the scheduler** (`read_spec_rows` skips a malformed
  spec with no sink) while `check_trajectory` ERRORs on the same file — a
  reader disagreement of exactly the §B3 kind, and a returned WI that vanishes
  from the frontier without a word is a hanging branch by another route.

**How the invariant is tested.** [`tests/test_handback.py`](../../tests/test_handback.py)
(13 tests, new; filed in `conftest.SLOW_MODULES` beside its two siblings — real
claims mean the real `trunk_step --regen` subprocess) constructs every topology
it measures. The anti-livelock property is asserted against `schedule.frontier`
itself, driven both ways (ready before the claim, `blocked` after the return);
the quarantine is proven bar-inert in **four** diff shapes (edit, add, delete,
rename) *and* lossless (`git apply --check` then `git apply` restores the lane's
work); all four registry readers are driven over one real returned spec. In
`tests/test_drive.py` the two run-stop deletions are driven end to end against a
**conditional** stub bar — red exactly while the lane's broken file is present,
which is what lets the red-handback ruling be *shown* (refresh red → quarantine
→ refresh green → merge) rather than asserted. `tests/test_integrate.py` gains
the crashed-claim shape (re-claimed) beside four negatives, the outcome read in
both failing shapes, and the outcome-keyed gate driven at the helper and through
the whole slot.

**Round 2 added the tests that can FAIL**, which is the honest lesson of the
review: round 1's `_abandoned_claim` negatives were both structured so a looser
matcher could not red them (one built two commits so the tip was a work commit;
the other had no claim-ish subject at all), so a stated invariant shipped with
no guard. The three new ones each ISOLATE one fact — an exact claim subject
carrying `real-work.txt` (only the content fact can reject it); a subject that
merely *ends* like a claim, touching **only** a bookkeeping surface (only the
exact subject can); and a genuine claim subject for a **different id**, likewise
bookkeeping-only (only the `wi_id` half can). Isolation was not free and the
first attempt did not have it: a mutation run showed the suffix-match mutant
passing all three, because every negative still carried product content that
fact 4 rejected. Re-driven after the fix, **each mutant reds exactly the
negative that isolates the fact it drops** — suffix-match reds two, dropping the
content check reds one, and nothing else moves.

The rename parse is pinned twice: a record-shape unit test over the exact field
list the review drove, and the end-to-end revert in the *damaging* alignment
(the rename sorts first, the broken file last). Both mutation-proven — restoring
the pair-parse reds them and leaves the other 11 green. The discarded return
codes are covered by fault injection on the last revert step: the refusal names
the path and the lane is reset, rather than a count being printed for work that
did not happen.

**Round 3 closed two more of the same shape and mutation-proved both.** Three
new negatives — a bookkeeping-only branch (driven over a log fragment, a
`docs/log.md` rewrite and a hand-written `PROJECT_STATE.html`), a regeneration
that moved no spec, and an abandoned branch a worktree still holds. Restoring
the wide bookkeeping rule reds exactly the first two; discarding `branch -D`'s
return code reds exactly the third; nothing else moves. The held-branch case
also pins the failure DIRECTION: the branch survives, the spec stays claimable
in `queued/`, and trunk is clean — it fails closed, it just used to say
otherwise. (Building it caught a fixture trap worth naming: a lane worktree
created *inside* the repo is untracked dirt, so the clean-trunk rung refuses
first and the test proves nothing. It is created outside.)

**One arm is defensive and is recorded as such rather than left to look dead.**
`_revert_ops`' `C` (copy) branch cannot fire from the call `quarantine` makes:
even at `diff.renames=copies`, plain `--name-status` reports a copied file as
`A`, because git needs `--find-copies-harder` to emit `C`. It is kept because
the parse and the undo have to agree about the three-field forms as a pair —
and because a future caller that adds the flag would otherwise get a silently
wrong revert.

**One fixture was corrected rather than bent.** The content fact reads the same
allowed set as the RULING-6 audit (bookkeeping prefixes plus the declared
`[generated]` paths), and the claim folds `trunk_step --regen` into its own
commit — which, with a `docs/work/` registry present, writes `PROJECT_STATE.html`.
A fixture that declared no generated set therefore produced a claim commit its
own reader could not recognise. That is a repo `integrate audit` would flag too,
so the fixture now declares the set the shipped `stack.ini` template does. The
failure direction is worth stating: an undeclared repo fails **closed** — the
re-claim refuses instead of deleting.

**Deviations from spec.**

- **`hand_back`/`quarantine` ship in a new sibling module, not in
  `integrate.py`.** The row's scope said "while the file is open"; the file is
  a monolith ratchet away from its ceiling. The extraction is the ratchet's own
  documented escape and the WI-374 precedent (the drive loop went to `drive.py`
  rather than into `agent_loop.py`). It costs the scaffold surface — MAPPING
  row, README kit-contents, `test_bootstrap` file list — all three registered.
- **`integrate.py` still crosses THRESHOLD (1418 → 1692) and takes a NEW
  reviewed baseline entry.** What remains is irreducibly its own: the claim,
  the outcome read the merge slot gates on, and the verdict gate. Re-stamp
  DOWN with WI-390's deletions. (Every figure here measured with the ratchet's
  own metric, `len(text.splitlines())`, at the shipped tip — `integrate.py`
  1692, matching the stamp; THRESHOLD is 1500; the two siblings sit under it at
  `handback.py` **362** and `drive.py` 495, so neither needs an entry. This
  sentence has now gone stale twice: round 2's review caught `integrate.py`
  reading 1638 here against 1643 further down, and round 3's caught
  `handback.py` reading 353 — the number I had corrected the FIRST half of the
  sentence with, while the sibling in the same sentence went stale under the
  nine lines round 3 added to `_revert_ops`. The lesson is not "check harder":
  a hand-copied number beside a machine-stamped one is a second home, and the
  only reason this one survives is that the two siblings are under THRESHOLD
  and so have no stamp to disagree with. Re-measure the whole sentence, never
  the half that changed.)
- **`EXIT_BUDGET` and `EXIT_STALL` now block a WI that used to be resumable —
  a real cost, recorded rather than traded in a set literal.** They are decided
  exits, so under §A3 the lane hands back; `hand_back` sets a `blockref`; and
  `schedule._disposition` reads queued+blockref as `blocked`. Before this row,
  a worker that hit its session ceiling stopped the run with the claim parked
  and a **relaunch resumed the same lane**, so a WI needing more than one
  worker budget finished across relaunches with no human in the loop. Now it
  returns blocked and an unattended run can never pick it up again. §A3's
  ruling is "any non-zero worker exit that is not a crash" and its
  justification is about `EXIT_NEEDS_HUMAN`, not about a ceiling — but the
  alternative (hand back *without* a blockref so a ceiling stays resumable)
  re-opens the claim/return/re-claim loop this row spent its effort closing,
  bounded then only by `--max-iterations`. That is an owner call, not a
  builder's, so it is filed below rather than decided here.
- **No CLI subcommand for `handback`.** The driver is the only mechanical
  caller; a lane agent that wants to cancel or hand back by hand writes the
  move and the reason, which is a judgement, not a command.
- **The spine is untouched**, per the standing ruling that spine work waits and
  batches. `LLR-143` and `TC-137` still describe `_stranded_claims` and
  "NEEDS-HUMAN propagates as exit 7"; both are false as of this merge and are
  owed to WI-390 along with `PROCESS_OPTIONS.md`'s attended-mode
  "the loop stops `NEEDS-HUMAN`" sentence. Nothing mechanical enforces LLR
  `Code`/`Detail` cells, so this is prose debt, recorded rather than absorbed.
- **`handback.py` declares no `Contracts:` line.** IF-080 already sits in the
  interface registry with no script declaring it (§A9.1's inherited drift);
  declaring it from the sibling rather than from `integrate.py` would
  paper over that. The module will add a fifth `connectivity undeclared` WARN
  once the trunk lane regenerates the arch-map — same pre-existing WARN class
  as `drive`, `traj_graph`, `traj_panels`, `traj_render`.

**Two false sentences RETRACTED from the claim rationale** (REVIEW-A round 1),
because a wrong record is the defect class this program keeps paying for and
`integrate.py`'s docstring is now the design's record of the inversion.
(a) *"Crash before the branch and there is nothing but an unreferenced object
git will collect"* — **false**. That window has the spec already `git mv`d out
of `queued/` and the regen staged, so it leaves a **dirty trunk with no branch
ref**; driven, the next claim refuses `the trunk working tree is dirty` and
drive.py's cycle-top check makes it `EXIT_PREFLIGHT`. It is not a regression
(the old order had the same window and the dirty check already fronted it), but
there are **three** interesting points, not two, and the deletion of
`_stranded_claims` is argued from the *second*. (b) *"the hook's live rung here
was the generated-artifact freshness floor"* — **false by omission**. `--regen`
covers six of the hook's ten `--run-steps`; it does not cover
`registry-integrity`, the `trajectory` SSOT check, `skills-sync` or
`ratify-fresh`, and outside `--run-steps` the plumbing commit also skips
`check_privacy --author`, the **always-on secrets floor**, the `format` step and
the `commit-msg` hook. Two of those are not vacuous: `ratify-fresh` reads the
registry the claim mutates, and the secrets floor would otherwise scan the
regenerated artifacts. Trunk advances to a commit no hook inspected and the next
thing to bar it is a lane's §A2 refresh — accepted for the window it buys, not
because nothing is given up. Both corrections are in the docstring, not only
here.

**Stamps re-stamped, each with its reason in
[`tests/test_module_size_ratchet.py`](../../tests/test_module_size_ratchet.py).**
`integrate.py` NEW 1588, re-stamped to 1643 across round 2 (the fourth
convicting fact, the exact-subject comparison, the outcome sets, and the
corrected claim rationale) and to **1692** at round 3 (the checked `branch -D`,
the narrowed content fact, and `_drop_abandoned` extracted so `claim` stays
under the C901 limit); `agent_common.py` 1731 → 1741 and
`check_trajectory.py` 3251 → 3261 (the body-grammar lines, identical text in
both by construction); `bootstrap.py` 2243 → 2250 (the scaffold registration).
`docs/dupes-allow`: the two F5 fingerprints moved again
(`221f967454e5` → `a17abce26cb8`, `e781cf6ec0e8` → `7a1470c3f0c1`) for the same
structural reason as WI-384 — the new lines land *inside* the matched block in
all three copies at once, and `check_trajectory == schedule` keeping its fp
(`1dbf7e455ac3`) is the tell that nothing new was copied. **No byte-budgeted
file was touched** (`AGENTS.template.md`, `PROCESS.md`, `PROCESS_OPTIONS.md`
unchanged).

**Bars (real output, repo `.venv` 3.11.9), AFTER merging trunk `4fb02de4`.**
Full unfiltered `pytest -q -n auto` → **1793 passed, 12 skipped, 0 failed**;
`ruff check .` and `ruff format --check .` → **All checks passed / 148 files
already formatted**; `check_trajectory --root . --strict` → **clean**;
`check_doc_refs --root . --strict` → **OK, no dangling path or `sym:`
references**; configured `check_docs --stale` → **OK, 0 broken**.

**There is no standing red any more, and that is a real change rather than a
lucky run.** Every pre-merge round of this row reported "1 failed" and named
`test_this_repo_is_not_a_work_branch` as expected-by-construction. Trunk's
`5f292892` retired that premise: the test asserted the CURRENT checkout carries
no claim, which is false by construction inside a lane worktree, and it was
redding the §A2 refresh's own bar so nothing could merge at all. Post-merge the
count is 1774 → **1793** (+19 from the three sibling lanes) with **zero**
failures. The pre-merge progression stands as history — 1762 → 1771 → 1774
across rounds 1–3, each step that round's new guards — but the closing figure
is the merged one above, and any red here now would be mine.

`check_doc_refs` earned its `--strict` twice on this branch, both times on THIS
fragment: round 2 it caught prose naming a `handback/` directory that does not
exist until a quarantine writes one, and round 3 it caught the log-fragment path
in the sentence above, invented to describe an exploit. Both rephrased to name
the shape without minting a path. It is a good check and asking its question
deliberately — *which prose now names a path this branch does not have?* — is
what catches it before a composed bar does.

**And the answer to "does this want a new idiom?" is NO** — reviewed and ruled
at round 3, recorded here so nobody re-opens it from the symptom. The repo
already carries three forms that partition the space: `docs/declared-absences`
(a path permanently not carried, with its reason), `path-ok` (prose whose
SUBJECT is a path that does not exist), and the record prefixes (compiled
history, judged loosely because it cannot be edited). A path that does not exist
*yet, because the code has not run* is none of these: it is a **description**,
not a reference — a reader cannot follow it — and `path-ok` would be wrong
twice over, since it exempts the whole line and would be spent on incidental
illustration. Rephrasing is the permanent answer, not a workaround. Being caught
in a fragment is the design working as written: `check_doc_refs.py` records that
`docs/log.d/` sits deliberately OUTSIDE the record prefixes so a fragment is
"judged strictly while its author can still edit it", and WI-384 built, measured
inert, and reverted that widening. The one thing worth adding is **guidance, not
machinery** — a line in the `session-protocol` skill saying a fragment may not
mint a path — and that belongs to **WI-396**, which owns this check's blind
spot. Filed there, not built here: a sibling lane hit this three times today and
five by the time round 3 reviewed it, so the frequency is real; the placement is
that row's call.

**Merging trunk `4fb02de4` — one conflict, and both intents kept.** This row is
the last of four lanes, so WI-378, WI-383 and WI-391's siblings landed first.
The single conflict is `_verdict_gate`'s docstring: WI-378 rewrote it with a
measured census of why `docs/work/` is NOT excluded from the freshness pathspec,
while this row rewrote the function's SIGNATURE and body to key off the outcome
map. **Neither is falsified by the other** — theirs governs which paths make an
APPROVE stale, mine governs which ids reach the comparison at all — so both
paragraphs stand verbatim, and the resolution adds one bridging paragraph
naming the single point where they meet: the freshness comparison only ever runs
for an id whose outcome is `merged`, so WI-378's `docs/work/` reasoning governs
exactly the branches that assert done, which is also the only place their
ordering rule ("close before the final verdict round") can bite — the closing
move being itself a `docs/work/` change. A returned or cancelled spec moves
under `docs/work/` too and owes no verdict for that move to stale. Nothing of
theirs was edited to fit.

**The ratchet was re-measured, not trusted.** `tests/test_module_size_ratchet.py`
auto-merged and kept this branch's `integrate.py: 1692`, which was stale — trunk
carried no `integrate.py` entry at all (its copy was 1449, under THRESHOLD), so
there was nothing to conflict with and nothing to warn. Measured on the merged
tree with the census's own metric: **1733**. The arithmetic checks the
resolution rather than agreeing with it — base `6b22f169` 1418, plus this
branch's +274, plus WI-378's +31, plus the 10-line bridge = 1733 exactly, so
dropping either side's paragraph would have shown up here as a shortfall. The
other three auto-merged entries were cross-checked the same way and are correct
by the same test (trunk changed none of their line counts). `handback.py` 362
and `drive.py` 499 remain under THRESHOLD.

**The `EXIT_TRAIN_END` deviation is now live, and it was load-bearing rather
than merely cautious.** It was excluded from `_WORKER_OUTCOMES` while WI-383's
deletion was still in flight on a sibling lane; that deletion has landed, and
`agent_common` now keeps only a note reserving the number. Had the set named the
constant, this merge would have made `drive.py` an `AttributeError` at import.
The comment is re-tensed to say the deletion happened rather than that it is
coming.

**One round-2 red was mine and is recorded rather than quietly fixed.** Adding
the `[generated]` declaration to `claim_repo` gave every fixture built on it a
`docs/stack.ini`, which changed the §4 refusal
`test_integrate_refuses_and_holds_the_trunk_when_the_bar_is_undeclared` sees
from *absent file* to *no `[product]` key* — two different refusals. The test
now deletes the file after the claim that needed it, so it still drives the arm
it names, instead of the assertion being softened to whichever refusal fires.

**Findings for their own WI (not fixed here).**

1. **A worker that reports DONE without closing its specs still parks.** One
   of two diagonals; the other — a *non-zero* exit from a lane that already
   closed — was found by the review and is now handled (the drain merges it on
   the outcome its tree names). This one remains: exit 0 with specs still in
   `active/<branch>/` leaves the branch parked and relies on the stall guard.
   Handing that back too would make the invariant airtight, but it changes the
   stall semantics this row was not asked to touch.
2. **A red refresh on a `merged` branch still stops the run.** Deliberate and
   unchanged (WI-386's rule: the lane that caused the red fixes it, and the
   branch is retried on every relaunch rather than stranded). It is the one
   remaining shape where a branch waits on a human, and whether it should also
   convert to a handback is a design question for §A3, not a builder's call.
3. **Should budget exhaustion be a handback at all?** The deviation above
   states the cost; the question is whether `EXIT_BUDGET`/`EXIT_STALL` should
   leave `_WORKER_OUTCOMES`, or hand back *without* a `blockref` so a ceiling
   stays resumable. Each answer trades a different property — the walk-away
   loop's ability to finish a long WI across relaunches, against the
   claim/return/re-claim loop the blockref closes. §A3 rules the shape ("any
   non-zero exit that is not a crash") but not this dial.
4. **A second handback of the same WI accretes a second `## Handback`
   section.** It parses correctly in all four readers (`Deliverable` stays
   empty, `BlockRef` intact) and reads as a history of returns, which is
   arguably right — but nobody decided that it should accrete rather than
   replace, and a WI returned five times would carry five sections.
5. **For WI-396, which owns the `check_doc_refs` blind spot: a fragment may
   not mint a path.** Not a new idiom — that was weighed and refused at round 3
   (see above); guidance, one line in the `session-protocol` skill. Filed
   because the frequency is measured rather than felt: this branch hit it twice
   and a sibling lane five times in one day, always in a `docs/log.d/` fragment
   describing a path the code has not created yet. Placement is that row's
   call, not this one's.

**One residual, recorded below the filing bar** (round 3's review reached the
same judgement independently): `_abandoned_claim` says "this WI's spec"
singular while the code allows plural, so a commit making the real move **plus**
a second `WI-401-*.md` file under the same claim directory is still convicted
and that extra file lost. It stays unfiled because the only reachable content is
a same-id duplicate the registry already rejects, the loss is bounded to that
directory, and the sha and its restore command print — and because no honest
flow produces it. Written down so the gap between the sentence and the code is
a known one rather than a discovered one.
