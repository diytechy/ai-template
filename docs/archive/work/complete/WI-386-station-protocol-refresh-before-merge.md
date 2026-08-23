+++
id = "WI-386"
title = "RULED 2026-07-31 (docs/concurrency-v2.md §A2) - the design is ruled into log.md's Decisions, so this row is CLAIMABLE. THE STATION PROTOCOL: the largest deletion in the concurrency-v2 design, and the one row that works at lanes=1. ONE CONSTRAINT - a branch may not enter the merge queue unless trunk is already an ancestor of it (git merge-base --is-ancestor, exact and cheap). A lane that finishes REFRESHES (merge trunk in, run trunk_step.py compile-log then regen, run check.py --tier all, commit) and records bar-green at the resulting branch-tip sha; the merge slot then verifies the ancestor relation and that sha, and merges --no-ff. EVERYTHING FOLLOWS FROM THE ONE LINE. A merge CONFLICT becomes unrepresentable, so integrate.py's conflict arm, its merge --abort paths and _candidate_worktree's parked-half-merge cleanup all delete. The composed tree IS the branch tree byte-for-byte, so the integrator's composed-tree bar deletes outright along with the candidate worktree, _teardown, the candidate-red parking branch and _composed_tree_script - the bar runs ONCE per WI on the branch instead of twice (today's self-reported builder close bar plus the mechanical integrator bar; only the latter is mechanical at all). Class C composition failures are still caught and BETTER: whichever branch merges second must refresh onto a trunk containing the first and bar THERE, so every pair composes exactly once on the real tree with the red attributable to the refresh that caused it - which is why WI-382 retired. TWO OWNER RULINGS 2026-07-31 fix the shape here. DECISION 3 - DELETE THE MERGE BAR OUTRIGHT rather than keeping a cheap non-test tier at merge as defence-in-depth: provably-redundant is the whole argument for the constraint, and a kept-just-in-case bar is exactly the shape the governing principle warns about. DECISION 4 - SPECULATIVE REFRESH. THE SLOT is the exclusive turn to advance trunk (today out/integrate.lock, held by integrate() for a whole drain); only one branch may move trunk at a time and that IS the merge queue - the only question is how much work a branch does while holding that turn. PESSIMISTIC would be take slot, merge trunk in, bar 11 minutes, merge, release: no race is possible, but the slot is held ~11 minutes so trunk advances at most ~5.5 times an hour REGARDLESS OF LANE COUNT - the slot becomes the bottleneck and extra lanes buy nothing. SPECULATIVE (ruled) is merge trunk in, bar 11 minutes, THEN take the slot for a sub-second ancestor check plus the merge. At lanes=2 with both finishing at T0: pessimistic bars A while B sits idle waiting for a turn it cannot use; speculative bars both concurrently, A wins the slot and merges in a second, and B refreshes once - bar-time it would have paid anyway going second. As lanes grow, pessimistic gets strictly worse and speculative does not. The retry is BOUNDED, not open-ended: after ONE lost race a branch takes the slot for its retry, degrading to pessimistic exactly for the branch that is losing, so no lane is starved by faster neighbours and the common case still pays nothing. THE OWNER ATTACHED A CAVEAT TO DECISION 4 - this might need restricting to pessimistic in the future, since optimistic concurrency caused pain historically, though that may have been the implementation. CHECKED, AND THE SUSPICION IS CORRECT: the recorded failure is the deleted dispatcher's 19 reservations -> 8 integrations -> 0 gate-verified -> 11 rescues, and concurrency-restructure.md §2.3 diagnoses it as speculation held in STATE GIT COULD NOT ADJUDICATE - refs/llm/ reservation refs used as compare-and-swap, out/dispatch/events.jsonl as run state, plus the residue that came with them (36 stale worktrees, 34 llm/* branches, an orphaned stash) on a module whose threat model was named as bugs and fail-open. The eleven rescues were rescues of RESERVATIONS, not of merge races, and the fix was making the claim a serial trunk commit (atomic and race-free because step 1 is a serial trunk commit). What this row speculates on is categorically different - ANCESTRY AND NOTHING ELSE: no reservation, no CAS ref, no events file, no run state; git itself is the arbiter, the question is one command, and a lost race has NOTHING TO RECONCILE because the branch simply redoes a refresh it would have owed anyway going second. TWO REQUIREMENTS ON THIS ROW FOLLOW FROM THE CAVEAT AND MUST BE BUILT, NOT HOPED FOR. (1) SLOT ACQUISITION MUST HAVE EXACTLY ONE CALL SITE, so pessimistic is the same code with that call moved BEFORE the refresh instead of after - a one-line move rather than a rewrite. Do NOT add a config dial for it now: a knob for a decision nobody has needed to change is the shape the governing principle warns about. (2) THE PESSIMISTIC PATH MUST NEVER BE DEAD CODE - the one-lost-race fallback IS the pessimistic sequence and executes in production every time a lane loses a race, so a later restriction switches to a path that has been running and passing all along rather than to a branch that rotted untested. MEASURED PRECONDITION (2026-07-31, holds): lane-side trunk_step determinism was verified by regenerating on a detached worktree at a clean committed HEAD - exactly two files drift (PROJECT_STATE.html and docs/gate) and both drift only by a HEAD-derived stamp line the freshness gates already exclude by design (gen_trajectory ASOF_RE; derive_gate --check compares only the # basis: line). THAT MEASUREMENT FORCED ONE RULE THAT MUST BE BUILT WITH THIS - THE REFRESH IS A DISPOSABLE COMMIT: a retry is git reset --hard to the last work commit then a fresh merge-trunk/trunk_step/bar, never a second merge stacked on the first, because docs/log.md is append-compiled from log.d fragments and a stacked refresh would conflict on the file end. Order inside the refresh is load-bearing: merge trunk, then trunk_step, then bar, then commit. Needs no dispatcher, so it can land before any concurrency exists - if only one row of this design ships, it should be this one. RE-AFFIRMED 2026-07-31 against the concurrency-v2 §A9.1 addition (the program-close row WI-390): that section adds a NEW row's scope - the spine amendment, connectivity, prose and stamps that no single builder can own - and changes nothing in this row's own scope, so this row stands as written."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

The one constraint is built and enforced: `integrate.py` will not merge a branch
unless `git merge-base --is-ancestor <trunk> <branch>` holds AND the branch tip
is a VERIFIED refresh commit. Both reads are in `_merge_ready`, and both are
proven to have two answers on a topology the tests construct rather than
inherit.

The attestation is a binding, not a message. The refresh commit carries
`Bar-Green: tree=<sha> work=<sha> <summary>` and `refresh_attestation` checks all
three names against git: `tree=` must equal the commit's own tree, `work=` its
first parent, and the subject must be that branch's own `refresh: <branch> onto
trunk`. The refresh names the tree before committing it (stage, then
`git write-tree`, which writes the same index `commit` will use) and refuses to
leave behind a commit whose attestation it cannot itself verify. Review round 1
drove the earlier string form three ways - a forged trailer on an ordinary work
commit, a whole refresh message copied onto another commit, and
`git commit --amend` moving the tree under a genuine one - and each of those
landed unbarred content on trunk. All three are now regression tests.

The bound is stated rather than overstated: this defeats ACCIDENT, not INTENT.
A lane that deliberately constructs a valid attestation merges unbarred, and the
cost is four git invocations (`add -A`, `git write-tree`, `git rev-parse
<branch>`, and the `commit` carrying them) with no bar at all - review round 2 drove it and landed
`never-barred.txt` on trunk. That is accepted deliberately: the only structural
closure is a bar the slot itself runs and cannot skip, and DECISION 3 (owner
ruling 2026-07-31) deleted the merge bar outright as the kept-just-in-case shape
the governing principle warns against. The threat model is the integrator's
usual one - bugs, drift and a lane that goes wrong, not a lane that lies on
purpose. A test pins the LIMIT rather than a defence, so a later reader cannot
mistake the guarantee for a stronger one; reopening it means a slot-side bar and
a revisited DECISION 3, not a longer trailer.

`integrate.py refresh` is the lane-side operation that makes the constraint
true: in the branch's own lane worktree, merge trunk in, run `trunk_step.py`
(compile then regen), stage, run the declared bar, commit. The order is pinned
by recording stub harness scripts, so a reordering fails a test rather than
quietly changing what was barred. The refresh commit is disposable: a retry
resets to the work sha the refresh itself recorded and redoes the whole
sequence, so a second refresh replaces the first instead of stacking a merge
that would conflict on `docs/log.md`'s appended end. Because that reset is a
`reset --hard`, the peel is structural too - round 1 drove a work commit whose
message merely quoted the trailer being peeled away and its file deleted from
the branch.

Deleted, because the constraint makes them unrepresentable or redundant: the
merge-conflict arm, all four `merge --abort` paths, `_candidate_worktree` and
its parked-half-merge cleanup, the composed-tree bar call, `_teardown`, the
`integrate/candidate` and `candidate-red` branches, and `CANDIDATE_BRANCH`. The
bar now runs ONCE per WI, on the branch, instead of once self-reported by the
builder and again mechanically by the integrator - and the mechanical one is the
one that survived.

The owner's caveat is built, not hoped for. `_slot()` is the only
`acquire_lock` call site in the file, and `_slot(` occurs exactly twice in the
source (its definition and its one call) - both asserted against the source,
both mutation-driven, because counting the lock call alone let a second
acquisition through the existing helper slip past. The pessimistic sequence is
not a dormant branch: `integrate_one` refreshes IN the slot for any branch that
arrives un-refreshed or stale, which every drain that merges a second branch
reaches by construction. `drive.py`'s `_drain` is the speculative half - one
call, whose deletion restricts the design to pessimistic without any other edit
and without a config dial. The reviewer re-drove exactly that deletion: the
queue still works end to end against the real bar.

Three things the plan did not anticipate, all required by measurement rather
than argument. `check.py --trunk-lane`: the freshness gates stand down on a
claimed work branch (SR-133), those seven steps then report SKIP, and the
integrator reads any SKIP as a refusal - so without the flag the refresh could
never go green at all. It makes the mechanical bar possible; it does not rescue
it from a false pass. `_shed_residue`: the bar now runs in the lane worktree, so
its own ignored tool residue would otherwise make the §5.6 unload refuse to GC
the lane over caches the integrator had just created - it enumerates ignored
FILES rather than diffing `git status` lines, which collapse an ignored
directory to one line and so cannot see into a directory the worker already
made. It prunes a directory its own deletions emptied - git reports an emptied
ignored directory, so the unload would otherwise refuse over it - but only one
absent from a directory snapshot taken before the refresh ran, because an empty
directory that predates the lane is the lane's (this repo's own
`docs/work/deferred/` is the live case of empty being load-bearing). It does NOT
make a lane clean: a lane the worker built in still reports dirty at unload,
which is WI-359's rule working as designed. And `refresh`
refuses outright when the MAIN checkout holds the branch, because trunk is
whatever that checkout has out - refreshing there merges the branch into itself
and attests a composition that never happened.

Merging trunk `979d8e09` (WI-380 + WI-384) took four conflicts, each resolved so
both intents survive: this spec's home moved to `docs/work/complete/` under
WI-384's six-state model (and the `close_branch` test helper with it); the two
test conflicts kept WI-384's terminal-state vocabulary alongside this WI's
station-protocol assertions; and the size ratchet was RE-MEASURED on the merged
tree rather than picking a side - 1548 measured, which is exactly 1523 + WI-384's
+1 + this WI's +24, so the arithmetic checks the resolution.

The merge also surfaced a red, and the honest reading of it is narrower than a
first draft of this record claimed. WI-384's cancellation guard asserts the
string `disposition` appears nowhere in a cancelled spec; SEVEN of the sixteen
trip it (measured), six in the Deliverable body and one - WI-356 - in its
frontmatter title, and none carries the key. The fix makes two narrowings, each
doing distinct work: splitting to the frontmatter gives the guard its subject
(the schema), and matching a KEY ASSIGNMENT separates prose from schema inside
it, which the split alone cannot. Mutation-proven 16 of 16.

By SIGNATURE that is Class C - `live_csv` skips while any claim is in flight and
both parents of the merge had one, so neither branch could see it alone. By
CAUSE it is Class D: all seven specs and the guard itself are trunk-side at
`979d8e09`, this branch contributed only the drain, and it reproduces at trunk
the moment trunk next drains. The composed-tree bar this WI deletes would have
caught it identically, so the instance is NEUTRAL evidence for the station
protocol rather than support for it, and it is not entered in the design's
failure-class table.
