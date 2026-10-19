# Handoff 2026-10-19c (headless leg 01): WI-925 landed; WI-926 rebases onto it next

It replaces [handoff-2026-10-19b-attended-coordinator.md](handoff-2026-10-19b-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. This was the first headless leg
under WI-946's launcher (loop session `20261019T185432Z-8e4f05`). It landed
one machinery lane and closed out at about a third of its window, because
the next row's rebase does not fit before the close-out line. Like the last
handoff, it carries no `Overnight: stop` line: the next row moves without the
owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** `9f911f9a2` lands WI-925, the trunk declared by name (squash of
  wi-925). `1fd1bdf6f` is the sweep's re-mint, WI-951, closed as settled at
  `a0921eb7a`. The close-out commit follows. `archive/lanes` is at
  `ebca15da8`, with WI-925's rebased tip `25ff948a9` and its pre-rebase tips
  `cb54f657b`, `81d271c6d` and `a9a9ad61b` as parents.
- **What the landing changes for every later lane:** the trunk is now the
  `trunk` key under `[policies]` in `docs/process.toml` (`refactor_again`
  here). Every reader that judges or writes against the trunk refuses when
  the key is missing, the staged `done-when-blessed` step included whenever
  a claim-copy change is listed. If the owner moves the trunk, that line
  moves in the same commit. A spec move's inbound relink of another claim
  copy, in the same staged change, is no longer a Done-when change.
- **Lanes:**
  - `wi-926` at `93a141a9e`, still based on `342bd95ef`, unchanged this
    leg. Next: rebase onto trunk's tip, which now carries WI-925. The two
    rows share integrate.py, agent_loop.py, the shipped pre-commit hook,
    RESYNC_PACK, the module-size ratchet and a dozen test modules (recipes
    section 4; a kit-builder may take the conflicts, briefed to keep both
    sides and stop on any semantic choice). Then counted round 1. Its
    round-1 builder still owes, before the landing's bar, the two items the
    2026-10-19b handoff names. The first is the scaffold-floor test that
    fails at the pre-rebase tip. The second is the tier cost (D-004): the
    lane's hooked-checkout fixtures run git per test. Terra's retained
    session for the lane is `01a15060-3db9-7d72-9752-9100bf897959`. WI-925
    used LLR-339 and TC-369, and the watermark now reads LLR 339 and
    TC 369, so wi-926's floor (SR-240, LLR-340, TC-370, IF-297, CMP-008)
    still holds.
  - Unchanged: WI-798, WI-902, and the landed lanes' branches and
    worktrees (`wi-925` among them, archived).
- **Watermark** on trunk: WI 951; SR 239, LLR 339, IF 296, TC 369, OI 114;
  acts to seq 136.
- **Strict lints:** clean on trunk.
- **Tests this leg:** the full unfiltered suite at `a0921eb7a`, from a
  detached worktree: 6473 passed, 31 skipped, 0 failed (20 min). The
  landing's bar on the staged squash: 2814 passed, smoke tier 56.8 s against
  60 s. Its parent `8d64910f2`, in the same window: 83.8 s (box load).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-19c/` holds
  this leg's briefs, verdicts and bar logs. Nothing in it is owed, and it
  may be deleted. The 2026-10-18d root's `wi925-s2/` is spent and may go
  too.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006). Each row changes machinery, so each lands alone. WI-925's change is
the trunk reader. The next machinery landing waits until the cycle has run
through it: the next leg's claims, briefs, rollup and staged done-when step
all read the declared trunk.

| # | Row | Next |
|---|---|---|
| 1 | WI-926 | Rebase onto WI-925's landing; counted round 1 (its builder answers D-004's tier cost and the scaffold-floor test before the landing) |
| 2 onward | As before | WI-897 (amend its queued row first, per WI-927's plan deliverable 6), WI-902 (B4), WI-798, then P1 to P8, then leg 03's rows; WI-940 after the batch |

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).
A leg continues the lanes claimed attended as they stand, with no re-claim;
its first loop-writer commit opens the lane's trailer window.

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** wi-925 D-006 to D-011. The riskiest: D-008 S1,
  where the readability report skips a gating measure, naming the line,
  while the trunk is undeclared, because LLR-256's approved exit contract
  stays untouched. D-006 retags the scaffold writer to LLR-339 so the
  declaration has one home. D-007 re-grades a round-1 MAJOR on TC-325's
  text to the checkpoint. Also confirm or overrule the 2026-10-19b list:
  wi-925 D-005, wi-926 D-004 and D-005, and the ones before them.
- **Still open from earlier handoffs:** the convergence-tag question; the
  `wi-880` worktree's uncommitted hook edit; the old `coordinator-tools`
  folder; OI-98 and OI-105, each waiting on its condition.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator, running ATTENDED in an interactive
session with the owner. Ask the owner at real decision points; record every
other call in docs/decisions/. Background tasks and notifications are fine
here (this is not a headless leg).

1. Take the lease FIRST, with your transcript so occupancy is readable:
   `python project-trajectory/scripts/coordinator_guard.py take --transcript "$(ls ~/.claude/projects/*/$CLAUDE_CODE_SESSION_ID.jsonl | head -1)"`.
   If the take is refused, report why and stop.
2. Read, in order: CLAUDE.md; docs/status.md; the newest handoff (the one
   status.md's RESUME HERE names), all of it; the Status and every "Owner
   rulings" section of docs/plans/2026-10-11-review-churn/README.md
   (2026-10-11 through revision 37) and its pointer-rules.md; the
   coordinator-cycle skill and its references/recipes.md;
   your memory index (review-churn-program-rulings first).
3. Run reviews the way the handoff's "How to run reviews now" says. It
   overrides the skill where they differ, until batch row B1 lands and the
   skill says the same.
4. Work the handoff's queue table in order: the "pre" trunk fix and the
   baseline manifest (M); file and
   land B1, then the plan gate G, then B2–B4 (B4 is WI-902's reshape), each
   filed on trunk with its scope critique and dispositions first; then
   continue WI-798; then P1–P9 under the dependencies their rows name; then
   re-order leg 03's rows against the plan with the owner. Claim under
   one scoped unpause per batch (a reviewed deletion commit, the claims, a
   byte-identical restore). Cut lanes from trunk's tip and land them one at a
   time. Roles: Claude Opus builds (kit-builder agent, medium); GPT Terra
   (medium) authors spine text in one retained session per lane; Codex Sol
   (medium) and Claude Opus (high) review in parallel (coordinator-2026-10-16
   D-008; the handoff's "How to run reviews now"); the independent adjudicator
   judges spine text and disputes through coordinator_adjudicate.py from the
   lane (set AGENT_CLAUDE_TOKEN_FILE to the token file's path from memory
   first; never read the file), never a sub-agent.
5. Before each landing commit: regenerate the views, run the smoke bar and its
   budget, run trace.py --strict and check_trajectory.py --strict, and read
   the summaries for failures.
6. Close out when `coordinator_guard.py status` reads 40% or more, at the
   latch, or when the owner says so (session-protocol section 4): land or
   safely commit every lane; update docs/status.md (forward-only); write a NEW
   handoff whose `## Session prompt (paste to start the next session)` block is
   this prompt, copied verbatim, keeping the `Overnight: stop` line unless the
   owner asks for headless legs; write a log fragment; fold procedural lessons
   into the coordinator-cycle skill; run the full suite once if code changed;
   commit; then `coordinator_guard.py handback --handoff <the new handoff>`.

Never: push or merge to main; rule an open item or sign an owner-held act;
leave docs/work/pause deleted; read OWNER_SCRATCHPAD.md or the adjudicator's
token file; self-review or adjudicate through a sub-agent; change ~/.claude
settings or install software; bypass a commit hook.
```
