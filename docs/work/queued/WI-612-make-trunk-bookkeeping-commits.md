+++
id = "WI-612"
title = "Make trunk bookkeeping commits stage and restore only what they wrote, so uncommitted edits survive"
workstream = "unattended"
specref = "docs/concurrency-restructure.md#23-the-claim-protocol-serial-on-the-trunk"
buildtier = "medium"
priority = 5
safety_class = "ordinary"
+++

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
