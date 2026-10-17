# Handoff 2026-10-16d (attended): four lanes built and committed, WI-930 gated and ready to land, landings wait for a quiet box

Overnight: stop

It replaces [handoff-2026-10-16c-attended-coordinator.md](handoff-2026-10-16c-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **On trunk this session:** only the close-out commit: this handoff,
  status, the log fragment, the coordinator-cycle fold and
  coordinator-2026-10-16 D-012 and D-013. No lane landed (D-013).
- **The box:** every bar reading this session was over the 60 s budget
  (67 to 142 s; the trunk base itself read 131.4 s in the same window),
  from the owner's own applications plus parallel lanes. By the owner's
  ruling (D-012) every local test job runs at below-normal priority
  through `C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/lowprio.py`
  (`python lowprio.py <program> [args...]`). Lane commits carry their
  breach and the window's parent reading. **A landing needs a quiet
  reading within budget: ask the owner for a quiet box before each one.**
- **Lanes** (each rebased onto or cut at trunk's 785b29e11; trunk has not
  moved since, so none owes a rebase):
  - `wi-930` (filing no longer refuses a rollup-named branch): **ready to
    land.** Build `bb71acb1d`, intent `3f68c5425` (LLR-313, TC-333),
    round 1 `6cbacac8d` (001 Sol, 002 Opus: both APPROVE, no findings),
    sitting 003 (LLR-313 and TC-333 MEANING, both blessed; act
    `ce6ba764f`), convergence map `416f3b993` (D-004, empty), gate
    `d04261180` (004 Sol, 005 Opus: both APPROVE, no findings). Next: the
    landing (recipes section 3), on a quiet reading; it lands alone.
  - `wi-928` (the blackout hook drops the rare shell forms): P1 to P6
    and P8 built and committed (`19ea84a4b` to `402899846`), P7's spine
    text at intent `3e10cad94` (GPT Terra, session
    `01a14808-b2c3-7783-a798-47056f74f8c9`). Next: counted round 1 (Sol
    and Opus high), then the checkpoint (combined sitting: amendment
    LLR-300, TC-339), the gate and the landing. For the reviewers'
    attention, from the builder: `time claude` has no pin (the plan adds
    no test), and `_heredoc_body`'s return value is now unused.
  - `wi-931` (the session kill drops its guards): the plan revised for
    critique 1's MAJOR on the owner's WSL route (wi-931 D-002), critique 2
    APPROVE, pass record `31dc6df4b`; P0's claim-base evidence `67bd3d086`
    (Windows 15 passed; WSL Ubuntu 11 passed, 4 skipped, as expected);
    P1 `21aa35b36`, P2 `92ed09752`; P3 `8b2b4870a` (its census re-check at the tip found no handler to fix). Next: the remaining steps
    of the plan (P5's spine prose by Terra, from the spine
    change list in this session's scratch, P6's RESYNC entry), then P7's
    tip evidence on both platforms (the WSL clone is `~/wi-931-posix`)
    and P8's completion check, then the rounds. The plan commits one
    step at a time.
  - `wi-935` (the bar runs the tier once): built and committed
    (`1c20b6eb6`); no spine. Next: counted round 1; it lands alone, and
    its quiet reading is the Done-when's.
  - `wi-929`: claimed, no commits, no worktree. Move it to trunk's tip
    before cutting it (recipes section 2).
  - Unchanged: `wi-912`, `wi-915`, `wi-916`, WI-798, WI-902 and the
    landed lanes' branches and worktrees (`wi-922`, `wi-914`, `wi-923`,
    `wi-911`, `wi-921`, `wi-913`).
- **Watermark** on trunk: WI 936; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 122 (WI-930's in-lane act lands with it).
- **Strict lints:** clean on trunk and on every lane commit this session.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/`
  (per-lane folders, `lowprio.py`, WI-931's P0 logs and spine change
  list). Keep it until those lanes land.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each at
below-normal priority while D-012 holds.

## The queue

The owner's order (coordinator-2026-10-16 D-004, with D-006 placing
WI-935). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-930 | Land it on a quiet reading (moved up: it is ready, and it lands alone) |
| 2 | WI-928 | Counted round 1, the checkpoint, the gate, the landing |
| 3 | WI-931 | The remaining plan steps, P7's two-platform tip evidence, P8, the rounds |
| 4 | WI-935 | Counted round 1, the landing (its quiet reading is its Done-when's) |
| 5 | WI-912 | Continue its lane (claimed) |
| 6 | WI-929 | After WI-912 (its soft edge); `none` |
| 7 | WI-917, WI-916, WI-915 | WI-917 owes its confirming scope-critique round before a claim |
| 8 | WI-925, WI-926, WI-927 | The hook rows, critique-clean |
| 9 onward | As before | WI-902 (B4), WI-798, then P1 to P8 with WI-918 (owes its confirming round), then leg 03's rows |

## For the owner

- **A quiet box** for each landing's bar reading (D-012, D-013).
- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** coordinator-2026-10-16 D-013 (D-012 records
  your ruling); wi-928 D-001; wi-930 D-001 to D-004; wi-931 D-001 (D-002
  records your ruling); and the earlier unseen ones the 2026-10-16c
  handoff lists.
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
