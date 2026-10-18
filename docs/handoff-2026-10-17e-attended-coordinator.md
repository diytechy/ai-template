# Handoff 2026-10-17e (attended): WI-929 landed; WI-917 planned and built; the merge-floor rows filed and confirmed

Overnight: stop

It replaces [handoff-2026-10-17d-attended-coordinator.md](handoff-2026-10-17d-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:** WI-929 (the shared machine-line reader stops
  refusing a repeated field) as `e45ed5a75`, its RESYNC entry re-anchored
  at the landing's parent `1b4d9d7af` (wi-929 D-002). Its lane: build
  round 1, the intent set from the spec's dictated text, counted round 1
  (Sol APPROVE 0; Opus APPROVE 1 MINOR, the anchor), the reconcile turn
  omitted (D-003), combined sitting 003 (LLR-310 and TC-327
  MEANING+BLESS), the act turn after the rebase (act seq 128), and the gate
  in convergence stance (Sol and Opus APPROVE 0). Its re-mint WI-944 closed
  as settled (`be439a482`); the tips are archived (`8fe1e366b`, with the
  pre-rebase tip `e6997274d` as an extra parent).
- **Claimed this session** under one scoped unpause (`1abcb06ee`, restored
  byte-identical at `fc0d9f7d4`): WI-917, WI-925, WI-926 and WI-927 (owner,
  coordinator-2026-10-17 D-008).
- **Filed this session:** WI-942 (a retirement alone in its registry) and
  WI-943 (a MEANING re-attestation only for a blessed row), the two
  merge-floor rows wi-912 owed (`1b4d9d7af`). The owner ruled that WI-808
  owns the gap their drafter found: the coordinator's squash landing runs
  no approval-act floor (D-009). D-010 settles WI-943's second call by the
  owner's standing rules. Scope critiques: WI-943 approved at round 1;
  WI-942's one MINOR (the absent act ledger) was adopted (`cffbccec3`) and
  its confirming round approved. Both are ready to claim.
- **Lanes:**
  - `wi-917`: claimed `single`, cut at `fc0d9f7d4`. Plan, critique (Sol
    APPROVE 0) and pass record committed; built in the plan's three stages
    (`5403b4323`, `44dc01225`, `e70ef55e5`), each re-run and committed by
    the coordinator. Decisions D-001, D-002. It owes no spine rows and so
    no sitting (its spec's S5: the launcher is not a kit component; the
    builder reported no row-text change). Next: the rebase onto trunk's
    tip, where its stage 3 and this close-out both edit the
    coordinator-cycle recipes (keep both), then counted round 1.
  - `wi-925`, `wi-926`, `wi-927`: claimed, no commits, no worktree; move
    each to trunk's tip before cutting (recipes section 2). Each is
    `single`.
  - Unchanged: `wi-915`, `wi-916`, WI-798, WI-902, and the landed lanes'
    branches and worktrees (`wi-929`'s included).
- **Watermark** on trunk: WI 944; SR 239, LLR 338, IF 296, TC 368, OI 114;
  acts to seq 128.
- **Strict lints:** clean on trunk and on every lane commit this session.
  The smoke budget read OVER on almost every commit (65 to 169 s, the box
  loaded throughout); every same-window pair read the parent as high or
  higher (D-005, D-011).
- **Full suite** at trunk's `cffbccec3`: 6087 passed, 22 skipped, 0 failed (34 min 33 s, below-normal priority on the loaded box); one fewer than 2026-10-17d's 6088, the case WI-929 deleted.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-17e/` may be
  deleted once the owner has read this handoff; nothing in it is owed.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-917 | Rebase, counted rounds, gate, land (the lane above; no sitting owed) |
| 2 | WI-916, WI-915 | Claimed; move each to trunk's tip, cut, plan (`single`) |
| 3 | WI-925, WI-926, WI-927 | Claimed; move each to trunk's tip, cut, plan (`single`) |
| 4 | WI-942, WI-943 | Critique-confirmed; claim under a second scoped unpause (D-008); WI-942 lands before item 14's retirement lane |
| 5 onward | As before | WI-902 (B4), WI-798, then P1 to P8 with WI-918 (after WI-917), then leg 03's rows; WI-940 after the batch |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** coordinator-2026-10-17 D-010 (no exemption for
  verdicts sat before WI-912) and D-011 (a records-only commit cites the
  session's same-window pairs instead of timing its parent); wi-929 D-001
  to D-005; wi-917 D-001 and D-002 (the leg prompt goes on stdin); and the
  ones the 2026-10-17d handoff lists (wi-912 D-009 to D-013;
  coordinator-2026-10-17 D-005, D-006; wi-912 D-001 to D-006; and earlier
  unseen ones).
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
