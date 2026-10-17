# Handoff 2026-10-17 (attended): WI-930 and WI-935 landed, WI-928 gated and ready to land, WI-931 owes P8

Overnight: stop

It replaces [handoff-2026-10-16d-attended-coordinator.md](handoff-2026-10-16d-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session**, each on a quiet reading the owner gave:
  - WI-930 as `87ceeafea` (its re-mint WI-937 closed at `61ee4e165`, citing
    act 123), coordinator-2026-10-17 D-001.
  - WI-935 as `8c72559ed`, placed ahead of WI-928 by the owner
    (coordinator-2026-10-17 D-002). **The commit bar now runs the smoke
    tier once**: about 66 to 69 s whole on a quiet box, against 112 to
    115 s before. Its gate's one MINOR is an unfiled follow-up in
    status.md (the date attached to OI-52 ruling (a), in three homes).
- **The box:** below-normal priority for every local test job still
  holds (coordinator-2026-10-16 D-012), through
  `C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/lowprio.py`.
  Quiet readings this session ran 42 to 50 s; parallel `-n auto` runs
  (a builder's module runs, the full suite) took a bar to 78 to 82 s, and
  the owner's applications at 36 to 53% CPU to 70 to 79 s.
  A landing still needs a quiet reading: ask the owner first.
- **Lanes:**
  - `wi-928` (the blackout hook drops the rare shell forms): rebased onto
    trunk's `8c72559ed`. Counted round 1 (001 Sol APPROVE 0, 002 Opus
    APPROVE 5 MINOR; filed at the then tip `548fd3053`), one fix round,
    the reconcile (`bcb892fc4`), sitting 003 (LLR-300 and TC-339 MEANING,
    both blessed; act seq 124, `62eb15881`). The gate over its
    checkpoint tip `c34dd2067` in convergence stance (004 Sol APPROVE 0;
    005 Opus APPROVE 1 MINOR, the anchor finding again; D-006), filed at
    `de8b10ce0`. **Ready to land** on a quiet reading.
    At the landing: re-anchor its RESYNC entry at the landing's parent
    (002's first finding, D-003), and archive `548fd3053`, `f82bcbe1e` and
    `3e10cad94` beside the rebased tip, since the verdicts cite them.
  - `wi-931` (the session kill drops its guards): rebased onto
    `61ee4e165`; P5 (`d8d84dc4a`, Terra; one approved clause kept beyond
    the spec's literal text, wi-931 D-004) and P6 (`4e6b1318f`, the RESYNC
    entry) committed. P7 ran at `4e6b1318f`: Windows 15 passed then 1
    passed, WSL Ubuntu 11 passed and 4 skipped (the Windows-only reasons)
    then 1 passed, the three module runs 258 passed, complexity unchanged,
    `agent_session.py` coverage 86.55% over a 16-module subset (floor 72);
    logs `p7-windows.log` and `p7-linux.log` in the scratch's `wi-931/`.
    Next: rebase onto trunk's tip (WI-935 changed files under
    `project-trajectory/`, so the tip moves and P7's two legs run again
    there), then P8: re-run P0's two legs at the new base (its check 2
    fails on a moved base), write the four records and the verdict line
    into the lane's log fragment, then counted round 1. One deletion
    beyond the plan's three in `tests/test_session_stdin.py` (an
    `import subprocess` only the deleted tests used) is for P8's check 3
    to record.
  - `wi-929`: claimed, no commits, no worktree. Move it to trunk's tip
    before cutting it (recipes section 2).
  - Unchanged: `wi-912`, `wi-915`, `wi-916`, WI-798, WI-902 and the
    landed lanes' branches and worktrees (`wi-930`, `wi-935`, `wi-922`,
    `wi-914`, `wi-923`, `wi-911`, `wi-921`, `wi-913`).
- **Watermark** on trunk: WI 937; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 123 (WI-928's in-lane act 124 lands with it).
- **Strict lints:** clean on trunk and on every lane commit this session.
  The full suite at trunk's `8c72559ed` (WI-935's landing): 6019
  passed, 22 skipped, 0 failed (16 min 49 s, below normal priority).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/`
  (per-lane folders, `lowprio.py`, WI-931's P0 and P7 scripts and logs).
  Keep it until WI-928 and WI-931 land. The detached `full-wt` worktree
  there is removed at close-out.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each at
below-normal priority while D-012 holds.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002 moved WI-935 up). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-928 | Land it on a quiet reading (gated; re-anchor its RESYNC entry, archive the cited pre-rebase tips) |
| 2 | WI-931 | Rebase, P7's legs at the new tip, P8, then counted round 1 |
| 3 | WI-912 | Continue its lane (claimed) |
| 4 | WI-929 | After WI-912 (its soft edge); `none` |
| 5 | WI-917, WI-916, WI-915 | WI-917 owes its confirming scope-critique round before a claim |
| 6 | WI-925, WI-926, WI-927 | The hook rows, critique-clean |
| 7 onward | As before | WI-902 (B4), WI-798, then P1 to P8 with WI-918 (owes its confirming round), then leg 03's rows |

## For the owner

- **A quiet box** for each landing's bar reading (D-012).
- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** coordinator-2026-10-17 D-001 (D-002 records
  your ruling); wi-935 D-001 to D-005; wi-928 D-002 to D-005; wi-931
  D-003 and D-004; and the ones the 2026-10-16d handoff lists
  (coordinator-2026-10-16 D-013, wi-928 D-001, wi-930 D-001 to D-004,
  wi-931 D-001) with the earlier unseen ones.
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
