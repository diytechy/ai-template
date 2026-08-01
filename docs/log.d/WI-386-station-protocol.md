## 2026-08-01 — WI-386: the station protocol (refresh before merge)

**Summary.** Rebuilt the integrator on the one constraint of
[`concurrency-v2.md`](../concurrency-v2.md) §A2 — *a branch may not enter the
merge queue unless trunk is already an ancestor of it* — and deleted the
machinery that constraint makes unrepresentable. The bar now runs ONCE per WI,
mechanically, on the branch, instead of once self-reported by the builder and
again on a composed candidate tree. Round 1 of review found the constraint's
second half (*and its bar passed on this tree*) satisfiable by a string; round 2
makes it a binding git verifies. Both are recorded below, because what shipped
is the second one.

**Deliverables.**

- **The constraint, enforced.** `integrate.trunk_is_ancestor` (one
  `git merge-base --is-ancestor`) plus `refresh_attestation` are the two reads
  `_merge_ready` makes before the slot merges `--no-ff`.
- **The attestation is a binding, not a message.** The refresh commit carries
  `Bar-Green: tree=<sha> work=<sha> <summary>`, and all three names are checked
  against git: `tree=` must equal the commit's own tree, `work=` its first
  parent, and the subject must be this branch's `refresh: <branch> onto trunk`.
  The refresh learns the tree before it commits by staging and running
  `git write-tree`, then refuses to leave a commit whose attestation it cannot
  itself verify. Amend, rebase, cherry-pick, a copied message and a hand-written
  trailer all fail the tree or parent check.
- **THE BOUND, STATED PLAINLY: this defeats accident, not intent.** A lane that
  *deliberately* constructs a valid attestation merges unbarred, and the cost is
  **three git commands** — `add -A`, `git write-tree`, `git rev-parse <branch>`,
  then a commit carrying those two values. Not "re-implementing the refresh":
  round 1's fix note said that and round 2 drove the real price, landing
  `never-barred.txt` on trunk with the bar never invoked. The format is printed
  in every refresh commit on trunk, and the operator of this system is an agent
  that reads the source, so the cost is reading. **This is accepted
  deliberately**, because the only structural closure is a bar the slot itself
  runs and cannot skip — and DECISION 3 (owner ruling 2026-07-31) deleted the
  merge bar outright, a kept-just-in-case bar being exactly the shape §0 warns
  against. The threat model is the one the rest of the integrator holds: bugs,
  drift and a lane that goes wrong, not a lane that lies on purpose. **An owner
  may want to rule on that boundary**; if it is ever reopened the answer is a
  slot-side bar and a revisited DECISION 3, not a longer trailer. Pinned by a
  test that asserts the LIMIT rather than a defence, so nobody later reads the
  guarantee as stronger than it is.
- **`integrate.py refresh`** — the lane-side station refresh, in the branch's
  own lane worktree: merge trunk in → `trunk_step.py` (compile, then regen) →
  stage → the declared bar → commit. Order pinned by recording stub harness
  scripts, so a reordering fails a test instead of quietly changing what was
  barred.
- **The refresh is a disposable commit** (§A2.1). `_work_tip` peels it off at
  the work sha the refresh itself recorded; a retry resets there and redoes the
  sequence, so a second refresh REPLACES the first rather than stacking a merge
  that would conflict on `docs/log.md`'s append-compiled end. Every failure path
  — conflicting trunk merge, failed trunk step, red bar, floor-refused commit,
  an attestation that does not verify — leaves the branch at that work commit
  with a clean tree and nothing parked for a human to unpick.
- **Deleted** from `integrate.py`: the merge-conflict arm, all four
  `merge --abort` paths, `_candidate_worktree` (with its parked-half-merge
  cleanup), the composed-tree bar call, `_teardown`, `CANDIDATE_BRANCH` and the
  `candidate-red` parking branch. `drive._ensure_worktree` went too — the lane
  worktree has one home now (`integrate.lane_worktree`), shared by the worker
  and the refresh so a red is fixable where the lane already lives.
- **The owner's two requirements, built.** `_slot()` is the only `acquire_lock`
  call site in the file AND `_slot(` occurs exactly twice in the source (its
  definition and its one call), both asserted against the source and both
  mutation-driven. `drive._drain`'s single speculative `refresh` call is the
  whole speculation, and deleting it restricts the design to pessimistic with no
  other edit and no config dial — the reviewer re-drove exactly that deletion
  and the queue still worked end to end. The pessimistic sequence is not dead
  code: `integrate_one` refreshes IN the slot for any branch that arrives
  un-refreshed or stale, which every drain that merges a second branch reaches
  by construction.

**Deviations from spec, and why.**

1. **`_composed_tree_script` was kept, renamed `_branch_tree_script`** — the
   only §A9 ledger row not deleted. Verified against the code before cutting:
   the helper exists because a branch may change a generator or the harness
   itself (WI-368), and the invoker is still trunk-vintage whenever `drive.py`
   drives the loop in-process. Deleting it would regenerate and bar the
   refreshed branch with the trunk's copy of `check.py` — reintroducing the very
   defect it was written for. The *composed tree* died; the behaviour did not.
   Its three tests were relocated, not deleted (the Phase 5 precedent). Round 1
   judged this real and the hazard MORE live under the station protocol, and
   noted the ledger row had conflated tree identity with script vintage.
2. **`check.py --trunk-lane` — a new flag, unanticipated by the plan.** The
   freshness gates stand down on a claimed work branch (SR-133/LLR-141), which
   rests on "a work branch never commits a generated artifact". The refresh
   makes that false for exactly one commit. Without the flag those seven steps
   SKIP and `_run_bar` reads any SKIP as a refusal, so **the refresh could never
   go green at all** — the flag is what MAKES the mechanical bar possible, not a
   rescue from a false pass. (Round 1 drove that: the first version of this
   deviation, in four places, had the failure direction backwards. Corrected in
   all of them.) The bar is equivalent, not weaker: `--trunk-lane` restores
   exactly the seven `_TRUNK_FRESHNESS_STEPS` the deleted candidate-tree bar
   ran. Opt-in, so a caller that forgets it gets the stricter answer.
3. **`_shed_residue` — added machinery the design did not predict.** The bar now
   runs in the lane worktree, so its own IGNORED tool residue (`.pytest_cache/`,
   `__pycache__/`, a coverage report) made §5.6's unload refuse to GC the lane
   over caches the integrator had itself just created — measured, not theorised.
   It enumerates ignored FILES (`git ls-files -o -i`) rather than diffing
   `git status --ignored=matching` lines, because that listing collapses an
   ignored directory to one line at any `-u` setting and so could not see into a
   directory that already existed — which round 1 drove, and which is the NORMAL
   case since the worker builds in the same lane worktree. It also prunes a
   directory its own deletions emptied, because git DOES report an emptied
   ignored directory (measured) and the unload would refuse over it — but only
   one absent from a directory snapshot taken before the refresh started, since
   an empty directory that predates the lane is the lane's. Round 2 drove that
   overreach, and this repo's own `docs/work/deferred/` is the live case of an
   empty untracked directory being load-bearing. **Scope stated honestly: this
   does not make a lane clean.** A lane the worker already built in still
   reports dirty at unload and the branch is still held; that is WI-359's rule
   working as designed and it predates this WI. All the refresh promises is that
   it adds nothing to the pile.
4. **`_verdict_gate` now measures code-time at `_work_tip`.** Structural
   consequence of moving the bar onto the branch: the refresh is the last commit
   before the merge and lands after the review by construction, so counting it
   as "code" would have made RULING-7 unpassable for every WI. Round 1 confirmed
   the gate still catches an ordinary post-review commit.
5. **The refresh stages BEFORE it bars, and commits the staged index.** A
   declared bar is the adopter's command; staging first means whatever it writes
   can never be swept into the attested commit by an `add -A` that ran after it.
   It is also what makes `git write-tree` able to name the barred tree.
6. **`refresh` refuses when the MAIN checkout holds the branch.** Trunk is
   "whatever the main checkout has out", so a main checkout sitting on the
   branch makes trunk BE the branch: round 1 drove it printing *refreshed onto
   trunk `<its own sha>`* and attesting a composition that never happened. There
   is no trunk to resolve while nothing has it checked out, so it refuses with
   the switch-back command. `lane_worktree` still returns the primary as a
   holder — the worker has no such problem.
7. **No spine amendment — and the debt is larger than round 1 of this fragment
   said.** Not "Notes are out of date": these records are **actively FALSE**
   and nothing mechanical catches them (`check_trajectory --strict` exits 0 over
   all of it).
   - `SR-132` (*Local integrator: serial fail-closed merge queue*) describes the
     composed-tree bar and candidate worktree, both deleted.
   - **`LLR-140`'s Detail** — *"integrate_one: --no-ff --no-commit merge,
     trunk_step.py folded into the merge commit, check.py --jobs 0 at the
     declared tier on the composed tree read fail-closed, ff-only trunk advance,
     branch deleted on green, candidate parked on red"* — every clause of that
     sentence was deleted by this WI.
   - **`IF-080`'s Contract** — same clauses (*"--no-ff onto a candidate
     worktree, trunk step folded in, the DECLARED bar on the composed tree …
     before the ff-only trunk advance"*), and it additionally omits the new
     `refresh` operation entirely. §A9.1 item 2 scopes the interface registry
     only to the connectivity drift, so this is scope WI-390 does not yet know
     it has.
   - `LLR-141`'s Notes are incomplete rather than false (`--trunk-lane` is a
     documented exception the Notes do not mention).
   Per the owner ruling (spine work waits, batches, runs alone) that is still
   the program-close row's to fix — but it inherits *false records*, not stale
   ones.

**Known terminal state, for WI-387.** A genuine trunk-merge conflict at refresh
is a loud, self-describing handback: the branch is left at its work commit with
a clean tree and no `MERGE_HEAD`, the run exits nonzero, and the refusal names
the worktree and the `git merge <sha>` to run. What it does NOT do is record
that it happened — no handback artifact, no `docs/work/pause`, nothing in
status — so every relaunch re-hits the identical conflict with no automated
progress. Driven both in-slot and in a two-branch drain (where the first merge
stands and the second branch stays finished-and-claimed). That is §A3/WI-387's
handback outcome arriving one row early; recorded here so the next reader does
not have to derive it from a refusal string.

**Reviewed baseline bump, and one decomposition instead of a second.**
`check.py` 1523 → 1547 in
[`test_module_size_ratchet.py`](../../tests/test_module_size_ratchet.py) — +26/−2,
24 net, of which **13 are the argparse help (3) and the comment recording why an
opt-in override to a fail-closed rule is safe (10)**, plus 4 more in the module
usage docstring. Reason at the entry.

The complexity ratchet is untouched, but not because nothing crossed.
`check.py:main` stayed at 16 (the flag is an assignment, not a branch), and then
the round-2 guards pushed **`integrate.refresh` over C901 (13 > 10)**. Per the
ratchet's own instruction — *decomposition, not a baseline bump* — its
preconditions moved into `_refresh_preflight`; as shipped `refresh` measures 9
and `_refresh_preflight` 6, both under `MAX_COMPLEXITY = 10`. `integrate.py`
carries no baseline entry at all, so a bump would have meant creating one for a
function invented this session. No behaviour moved: the preflight runs
`_declared_bar_or_refusal` → the primary-checkout refusal → `lane_worktree` →
the dirty check → `_work_tip` → `reset --hard`, which is the round-1 sequence
with exactly the one new guard inserted.

**Bars.** Full unfiltered suite `pytest -q -n auto`: **1729 passed, 12 skipped,
2 failed in 394s**; `ruff check .` and `ruff format --check .` clean (146
files); `check_trajectory.py --root . --strict` clean (388 work items, graph
acyclic, only the pre-existing IF-registry connectivity warns §A9.1 already
records). Both failures are pre-existing on this branch and neither is this
change: `test_check_lane.py::test_this_repo_is_not_a_work_branch` (the standing
work-branch failure — the kit's own checkout IS a claimed branch in a claim
worktree), and `test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans`
via a stale `work/deferred/` link in `concurrency-v2.md`.

**Finding, not fixed here.** `docs/concurrency-v2.md` links `work/deferred/`
twice, and git tracks no such path — the trunk checkout only resolves it because
an EMPTY untracked directory survives there on disk. Every fresh clone and every
new worktree reds `check_docs` on it. Worth its own row.
