+++
id = "WI-612"
title = "Make trunk bookkeeping commits stage and restore only what they wrote, so uncommitted edits survive"
workstream = "unattended"
specref = ""
buildtier = "medium"
priority = 5
safety_class = "ordinary"
+++

## Deliverable

Built test-first from this spec's Done-when by a builder session in its own
worktree, reviewed, and squash-merged.

- `scripts/bookkeeping.py`, one shared helper both writers call (IF-186):
  `commit(root, scope, write, message, *, label, before_advance)`. The scope is
  the step's planned paths plus every file `trunk_step --regen` writes
  (`REGEN_STEPS` rows now name their writes). Any dirt inside the scope refuses
  by name before anything is written. The step's writes and the regeneration
  run, the in-scope changes are committed from a temporary index seeded from
  HEAD, and trunk advances by a compare-and-swap `update-ref`. No `add -A`,
  `reset --hard` or `clean` remains on these paths.
- The claim (`integrate._claim_locked`) and the intake mint (`_mint`, split
  into scope, write and message) commit through it; the claim's whole-tree
  clean rung is gone. `spec_move.planned_writes` and
  `consolidate.archive_scope` compute their scopes from the same traversal
  the writes use.
- The dispatcher's tick-top stop and the merge slot now use
  `substantive_working_tree_dirty`, so the owner's scratchpad no longer stops
  the loop.
- Honest contract: an owner edit landing on an IN-SCOPE path while the helper
  runs can still be swept in, overwritten or restored over. A restore leaves,
  and names, any in-scope path edited after the step wrote it, and a failed
  restore is attached to the re-raised exception. The isolated build that
  would close most of that window is WI-647.
- Tests: `tests/test_bookkeeping.py` (registered slow) plus cases in
  `test_integrate.py` and `test_dispatch.py`; 8 red before the build, and the
  follow-up's cases red against the first cut or under mutation.
- Six approved rows stated the old behaviour and were amended in their
  attesting cells (LLR-140, LLR-143, LLR-151 `detail`; TC-132, TC-144, TC-145
  `method`). Their adjudication is WI-648.

Review: codex Sol (medium) NOT YET SOUND, 1 blocker and 3 major, 1 minor. The
blocker (an owner edit to an in-scope path during the step) was arbitrated by a
Fable agent, ruling B: an honest contract and a leave-and-name restore now, and
the isolated build as WI-647. The rest were fixed: a restore failure
surfaced, pre-check tests that count writes, the six amendments, and the
`PROCESS_OPTIONS.md` byte re-stamp.

## Context

Found 2026-09-24 while filing the owner review pack's Part C, and verified
by the codex Sol review of that session. Filed at the owner's request: anything
left uncommitted in the primary checkout must survive the loop.

The two trunk-side bookkeeping commits run in the primary checkout and treat
its whole working tree as theirs:

- `integrate._claim_locked` (`integrate.py:796-857`) stages with `git add -A`,
  restores with `git reset --hard HEAD` on every refusal, and advances trunk
  with `git reset --hard <commit>`;
- `intake._mint` and `intake._bookkeeping_commit` (`intake.py:2069-2174`),
  which copy the claim's write sequence, do the same, plus
  `git clean -fd -- docs/work`.

So an uncommitted edit (the owner's scratchpad, a half-written doc) is either
committed into a claim or mint, or discarded when one refuses. The dispatcher
refuses to tick on a dirty trunk (`dispatch.py:1417-1425`), but it uses the
raw `working_tree_dirty`, so the owner-only scratchpad alone stops the loop,
although resume and done detection already exempt it
(`substantive_working_tree_dirty`). The check also runs only at the top of a
tick, so an edit made during a claim's regeneration is swept in. Manual runs
(the claim CLI, `intake.py sweep`) are not guarded at all.

The fix is one shared bookkeeping-commit helper that both call (the 0->A->B
rule), so the bad state is unrepresentable rather than guarded against: it
stages exactly the paths the step wrote (moved specs, the watermark, the
declared regenerated artifacts), restores only those on refusal, and advances
trunk without `reset --hard` over anything else. NOT IN SCOPE: the
lane-worktree resets in `handback.py` and from `integrate.py:2304` on, which
run in the loop's own worktrees. S11's single-commit plan may move the claim
off trunk; the mint stays, and its merge-slot commit should reuse this helper.

## Done-when

- The claim and the intake mint commit through one shared helper that stages
  only the paths the step wrote; no bookkeeping path in the primary checkout
  runs `git add -A`, `git reset --hard` or `git clean` over paths it did not
  write.
- A test leaves an unrelated modified file and an unrelated untracked file in
  the primary checkout, then drives a successful claim, a refused claim, a
  successful mint and a refused mint, and shows both files unchanged and
  absent from every commit.
- A dirty path the step itself must write (for example a hand-edited
  `docs/status.md` under regeneration) refuses by name before anything is
  written, rather than being overwritten or swept in.
- The dispatcher's clean-trunk refusal ignores `OWNER_ONLY_PATHS`, as resume
  and done detection already do, so a dirty owner scratchpad no longer stops
  the loop.
