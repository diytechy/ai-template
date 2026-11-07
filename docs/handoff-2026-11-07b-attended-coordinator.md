# Handoff 2026-11-07b (attended): headless leg 36 stopped on the usage limit with WI-996 and WI-1002 claimed

It replaces [handoff-2026-11-07a-leg35-coordinator.md](handoff-2026-11-07a-leg35-coordinator.md)
as the resume map, and carries its queue, owner items and session prompt
unchanged except where this file says. The procedure is in the
`coordinator-cycle` skill and its recipes; this handoff holds state only.
This attended session is `3c08c037-5aaf-4966-971a-0109570bd30e`. It wrote this
handoff and built nothing.

## What happened

Leg 3 of run `20261106T053406Z-1dfd0f` (leg 36 in the handoff series; session
`5a2bd30c-d697-45f4-85fc-a6d179622784`) started from the replaced handoff at
00:23 on 2026-11-07. It claimed WI-996 and WI-1002 under one scoped unpause
(the pause restored byte-identical, `f28530899`), then hit the owner's weekly
usage limit and exited 1 at 01:55, before a close-out. It wrote no handoff and
left the coordinator lease held. The launcher's audit of the leg passed.

The owner released the lease on 2026-11-07 (attended, recorded by
`coordinator_guard.py release`). No commit was taken off either lane, and
nothing in either worktree was changed.

## State (trunk `refactor_again`)

- **WI-996** (lane `wi-996`, worktree `C:/Projects/ai-template.wt/wi-996`,
  `planmode = "single"`). Committed: the plan, revision 1; critique 1 APPROVE
  with no findings; the pass record; the ids reserved on the id carrier (LLR
  368, TC 421 to 426); the intent commit `01d2f543a` (SR-156's acceptance,
  LLR-368, LLR-207 and TC-132 amended by addition, and its new TCs).
  **Uncommitted, the build's first step (tests first):** six changed test files
  (`conftest.py`, `test_dispatch.py`, `test_id_landing.py`,
  `test_integrate_attest.py`, `test_integrate_station.py`,
  `test_loop_provenance.py`; 52 lines added, 13 removed) and two new ones,
  `tests/test_red_mark.py` and `tests/test_red_mark_lane.py` (966 lines),
  written between 01:36 and 01:52. The last run of them, at 01:55
  (`review-tmp/2026-11-07-leg36/wi996/runxfail.txt`), read **76 failed, 8
  passed**. Before committing them, have a builder read them against the plan
  and the row's TCs. Settle why 8 pass before any code exists, under the
  row's own red-before rule, and record what you find in the lane's decisions.
  Keep the work. Discard it only on a recorded finding.
- **WI-1002** (lane `wi-1002`, `planmode = "none"`). Committed: the intent
  commit `0cf8b550d` (LLR-143 and TC-137 amended by addition). No build has
  started, and its worktree is clean.
- **Scratch:** leg 36's root, `C:/Projects/ai-template.wt/review-tmp/2026-11-07-leg36/`,
  holds both lanes' briefs, logs and Terra outputs (`wi996/`, `wi1002/`). Keep
  it until both lanes land. The `wi-1002-terra-trace.*` files under
  `review-tmp/` are that leg's; their process is gone.
- **Watermark** (trunk): WI 1002, SR 246, LLR 367, IF 311, TC 420, OI 129, plus
  WI-996's reservations on the id carrier. Acts run to seq 178.
- **Bars:** the commit carrying this handoff states its smoke result. The last
  full suite is leg 35's, at `14bca49e0` (7819 passed, 29 skipped).
- **Usage:** `usage_ingest.py --session 495d0b46-d85a-4338-92f6-942532b3e330`
  (leg 35) and `--session 5a2bd30c-d697-45f4-85fc-a6d179622784` (leg 36, the
  stopped leg) both exited 0. This session's own run exited 1, as it did on
  2026-11-05: `refused ...3c08c037-5aaf-4966-971a-0109570bd30e.jsonl: line 32:
  type 'tools-used' is unknown`. The next close-out passes no `--session` for
  this attended session.
- **Pause:** `docs/work/pause` is tracked and unchanged (sha256 `b0a709c8…`).
- **Disk:** 29G free on C:.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:

- Two full-lane reviewers run per round: Codex Sol at medium (REVIEW-A,
  `codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched
  with the Agent tool's `effort: "high"`). Each gets only its rendered
  brief.
- In a headless leg, launch REVIEW-B first, and tell it never to hand a
  test run to a background sub-agent.
- WI-995 has landed: the review test set is derived, so `attest` and the
  render take no list. This is that change's first real use, so read the first
  attest's printed set.

## The queue

The owner's order stands (coordinator-2026-11-03 D-003 and D-004). Each row that
changes machinery lands alone, after the cycle has run through the last
landing's changed steps. WI-995's changed step runs at the next lane's first
attest and render. WI-993's held-act arm runs at the next landing that carries a
held MEANING row, and WI-983's at the next decomposition round; no scheduled row
is known to draw either.

**Only the rows in this table are claimed**, in order and under their `needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-910 | Held on OI-124: push, or the owner rules the WSL POSIX route. Skip it while held |
| 2 | WI-996 | **Already claimed** (lane `wi-996`). Continue its tests-first build from the uncommitted work below; never claim it again |
| 3 | WI-1002 | **Already claimed** (lane `wi-1002`). Continue from its intent commit; never claim it again |
| 4 | WI-1001 | Critique confirmed. Waits on WI-999 and WI-1000 (OI-129). Skip it while held |

**Never claimed by a leg:**

- WI-684 (waits on OI-98, the owner's re-sync);
- WI-795 (OI-105, then WI-820);
- WI-827 (attended only, though the frontier lists it as ready; it never lands
  from a lane);
- WI-908 (OI-122: the owner present);
- WI-964 (OI-123: the owner's Mac);
- WI-998 (off the table until a sample exists, though the frontier lists it);
- WI-999 and WI-1000 (OI-129);
- every row under `docs/work/deferred/` (D-011, D-016).

## For the owner

1. **Confirm or overrule wi-995 D-003 (high risk).** The review bar's named tests
   append paths and a `--basetemp=` argument to `[product] test`, and the unattended
   draw now reaches that step, so a runner refusing them reds every code-touching
   row. The leg took the note in the shipped template and the RESYNC entry, which
   fails closed and changes no code. A declared placeholder stays open if you want it.
2. **WI-1001, for your read before OI-129 frees it.** Reusing the WI-997 gating, an
   adopter goes strict-red across the repository on entering `DevStg-Impl` until every
   case is tagged, and its RESYNC entry is a second forced migration. Its Done-when
   also moves TC-035's `automated` cell to No, a third untagged automated case. Its
   spec grew past three times its filing size (7638 bytes against 775).
3. **WI-995's first real use.** Open adopter lanes re-attest once, since a hand-list
   record digests differently. It fails closed, and the RESYNC entry states it.
4. **OI-129** (holds WI-999 and WI-1000, and so WI-1001): build or retire SR-165's
   derivation record and SR-035's token scan.
5. **OI-124** (WI-910) and **OI-121**'s attended session for WI-827.
6. **WI-998:** moving it to `docs/work/deferred/` would stop it reading ready.
7. **The FileBackup re-sync (OI-98):** first fix the act ledger entry's overwrite list
   and the tag entry's PROCESS classing, and amend TC-036's inputs to add
   `RESYNC_PACK.md`. WI-997's entry is a forced migration: seed your tags before
   re-syncing past it. FileBackup is on `Rust-Rewrite`, so the scratch trial needs a
   copy.
8. **Your local branch.** `git branch -f rolling_review origin/rolling_review` drops
   only a copy of WI-983 that trunk already holds. Until then, do not push local
   `rolling_review`.
9. **Confirm or overrule:** coordinator-2026-11-06 D-001 to D-004, wi-993 D-003, and
   everything the [replaced handoff](handoff-2026-11-06a-leg34-coordinator.md) lists in
   its item 10. Its items 1, 3 and 4 stand as reported.
10. **Push** `refactor_again`, `archive/lanes` and `id-carrier`, after item 8.

11. **The weekly usage limit** stopped leg 36 mid-lane. A leg cannot see it
    coming, so it leaves no handoff. Starting a run near the limit's reset
    leaves less room.

## Usage

See "State" above.

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
