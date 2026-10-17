# Handoff 2026-10-16c (attended): WI-922 landed, the reviewer trial ended, the row-2 batch claimed

Overnight: stop

It replaces [handoff-2026-10-16b-attended-coordinator.md](handoff-2026-10-16b-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **On trunk this session:**
  - `0ab549a15`: the owner's rulings (coordinator-2026-10-16 D-006 to
    D-009): the reviewer trial ends (Sol and Opus stay), and the bar
    follow-up is filed as WI-935 with the owner's construction. The skill
    and the plan's revision 37 ruling record the trial's end.
  - `4bdf59231`, the claims `be28e46e4` to `d5ea8a40b`, `a278cb206`: one
    scoped unpause claimed WI-928, WI-929, WI-930, WI-931 and WI-935
    (D-007, D-010); the pause is restored byte-identical.
  - `6515aeed1`: **WI-922 landed** (the plan gate's landing shapes).
    Sitting 004 ruled SR-154 CLARITY, act seq 122; the gate approved
    (005 Sol, one MINOR dismissed; 006 Opus, none). Tips archived.
  - `b01ea19e8` and `1b081b146`: the re-mint WI-936, closed as already
    settled (act 122).
  - The close-out commit: this handoff, status, the log fragment, the
    coordinator-cycle fold and D-011.
- **Lanes:**
  - `wi-928`: cut at `a278cb206`; plan `879760993`, critique (one
    sequencing MINOR, read as an APPROVE), pass record `7c21e3589`. Next:
    the first build. The build brief orders P8 after P6 and P9 after P7 and
    P8 (wi-928 D-001).
  - `wi-931`: cut at `a278cb206`; plan `db45cd9b9` (DELTA none, coverage
    OK). Its first critique (Sol, at close-out) is CHANGES-REQUESTED with
    one MAJOR, not yet filed; the verdict is at
    `C:/Projects/ai-template.wt/review-tmp/2026-10-16c-coord/wi-931/plan/crit1/WI-931-plan-critique-1.md`.
    The MAJOR: the Done-when requires the kept ordinary-kill tests to pass
    on Windows and POSIX before and after the change, while the plan's P7
    makes POSIX evidence before landing optional. Next: file it
    (`plan-file --critique`, `--sha db45cd9b9`), then the one revision.
    The revision must name a POSIX route before landing. CI needs the
    owner's push of the lane, and a WSL run needs WSL present (installing
    it is not the coordinator's). If neither is available, the Done-when
    needs an owner act (B4): put it to the owner as a call before the
    revision.
  - `wi-929`, `wi-930`, `wi-935`: claimed, no commits, no worktree. Move
    each to trunk's tip before cutting it (recipes section 2).
  - `wi-922`: landed; branch and worktree stay until the open lanes have
    rebased. So do `wi-914`, `wi-923`, `wi-911`, `wi-921`, `wi-913`.
  - Unchanged: `wi-912`, `wi-915`, `wi-916`, WI-798 and WI-902.
- **Watermark** on trunk: WI 936; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 122.
- **Strict lints on trunk:** both clean; `check_trajectory --strict` keeps
  its advisory warnings by design.
- **Smoke tier:** 40 to 48 s quiet, up to 56 s under two reviewers' load;
  every budget reading within 60 s. The bar still runs the tier twice until
  WI-935 lands.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and restored.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-16c-coord/`
  (per-lane folders, the trial tally under `tally/`, the full-suite run
  under `full/`). Keep `wi-931/plan/crit1/` until its verdict is filed.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), the trial
having ended (coordinator-2026-10-16 D-008).

## The queue

The owner's order (coordinator-2026-10-16 D-004, with D-006 placing
WI-935). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-928 | The first build from its pass record, the counted rounds, the checkpoint (its spec's LLR-300 text), the gate and the landing |
| 2 | WI-931 | File its plan critique (one MAJOR: POSIX evidence before landing), settle the POSIX route with the owner if needed, then the one revision; then the build |
| 3 | WI-930 | Cut the lane; `none`, so the build first |
| 4 | WI-935 | Cut the lane; `none`; the bar runs the tier once. Lands alone |
| 5 | WI-912 | Continue its lane (claimed) |
| 6 | WI-929 | After WI-912 (its soft edge); `none` |
| 7 | WI-917, WI-916, WI-915 | WI-917 owes its confirming scope-critique round before a claim |
| 8 | WI-925, WI-926, WI-927 | The hook rows, critique-clean |
| 9 onward | As before | WI-902 (B4), WI-798, then P1 to P8 with WI-918 (owes its confirming round), then leg 03's rows |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **WI-931's POSIX evidence:** its Done-when needs the kept kill tests run
  on POSIX before and after the change. Either push the `wi-931` lane so CI's
  Linux and macOS jobs run it, or say whether a WSL run on this box is
  available.
- **Confirm or overrule:** coordinator-2026-10-16 D-007, D-010 and D-011
  (D-006, D-008 and D-009 record your own rulings); wi-922 D-003 to D-008;
  wi-928 D-001; and the earlier unseen ones the 2026-10-16b handoff lists.
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
