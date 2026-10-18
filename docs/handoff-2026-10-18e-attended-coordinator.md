# Handoff 2026-10-18e (attended): WI-927 landed; WI-943 gated; the launcher row filed

Overnight: stop

It replaces [handoff-2026-10-18d-attended-coordinator.md](handoff-2026-10-18d-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:** WI-927 (9c6b7af35; act seq 130), its re-mint
  WI-947 closed citing the act (2d3dc0898), and on trunk: WI-946 filed with
  its calls ruled and WI-918 amended at its claim (7bbb8ad87,
  coordinator-2026-10-18 D-005), both rows' critiques recorded (45dfc9611).
- **Lanes** (every one committed, its tree clean):
  - `wi-943` at `51c08ad2a` (base `b120c4722`; pre-rebase tip `9b168865a`
    to archive at landing): sitting 003 accepted (verdict commit
    `7389c9125`; LLR-278, LLR-310, LLR-338 and TC-278 MEANING+BLESS), the
    convergence map recorded (D-006) and the gate filed (004 Sol APPROVE 0,
    005 Opus APPROVE 2 MINOR; D-007). Next: rebase onto trunk (trunk now
    holds WI-927's code; the lane also edits the recipes file and the
    byte-budget-guard skill rows that trunk changed; re-anchor its RESYNC
    entry), show the lane's diff unchanged by patch id, the unchanged-rows
    check against `7389c9125`, the act (`act --verdict
    docs/reviews/wi-943/003-ADJUDICATE-f01e04c.md --wi WI-943`), the close
    in the lane, land; at the landing, add D-007's two MINORs to status.md's
    follow-ups.
  - `wi-925` at `81d271c6d`, unchanged: stage 3 next (the 2026-10-18d
    handoff's notes; its two change lists are in
    `C:/Projects/ai-template.wt/review-tmp/2026-10-18d/wi925-s2/`).
  - `wi-926` at `d15adb2de`, unchanged: counted round 1 next. Its spec of
    record `docs/specs/WI-926.md` was relinked on trunk by WI-927's close,
    so its rebase meets that edit.
  - `wi-927` landed; its branch and worktree remain, archived.
  - Unchanged: WI-798, WI-902, and the landed lanes' branches and worktrees.
- **Ready to claim:** WI-946 (the launcher's follow-ups; its scope critique
  APPROVE 0) and WI-918 (the re-claim reader; its confirming round on the
  amendment APPROVE 0). Both are `planmode = "single"`, so each plans in its
  lane before its first build. They share LLR-248, TC-242 and the merge
  slot's lane-window code, with a soft edge only; the second to land re-sits
  the shared rows.
- **Id floor** (wi-925 D-003, wi-926 D-002), unchanged: wi-925 holds LLR-339
  and TC-369; wi-926 holds SR-240, LLR-340, TC-370 and IF-297. WI-925, WI-926
  and the landed WI-927 all amend LLR-300's detail: the later rebases
  reconcile it.
- **Watermark** on trunk: WI 947; SR 239, LLR 338, IF 296, TC 368, OI 114;
  acts to seq 130.
- **Strict lints:** clean on trunk and on every lane commit this session.
- **Full suite:** at trunk's `2d3dc0898` (WI-927's landing and its re-mint
  close), from a detached worktree: 6374 passed, 31 skipped, 0 failed
  (24 min 40 s).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-18e/` holds
  this session's logs and briefs; nothing in it is owed. The 2026-10-18c
  root is deleted. The 2026-10-18d root keeps only `wi925-s2/`, owed at
  WI-925's P9.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), reordered toward headless runs (coordinator-2026-10-18 D-004).
Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-943 | Rebase, patch-id and unchanged-rows checks, act, close, land |
| 2 | Gate rows: WI-946 and WI-918 | Claim both under one scoped unpause; plan each in its lane (single), then build; land after WI-943, one at a time (WI-918 first, so the shared LLR-248 and TC-242 are re-sat once, unless the plans say otherwise; record the order) |
| 3 | Clear the stop | The session that lands the second gate row writes its handoff without `Overnight: stop`; the owner starts `scripts/coordinator/overnight_legs.py` |
| 4 | WI-925 | Stage 3: Terra's P9, P10; counted round 1 |
| 5 | WI-926 | Counted round 1 |
| 6 onward | As before | WI-897 (amend its queued row first, per WI-927's plan deliverable 6), WI-902 (B4), WI-798, then P1 to P8, then leg 03's rows; WI-940 after the batch |

From row 3 on the queue runs in headless legs (the `coordinator-cycle`
skill's section 7); a leg brings an owner-held step to a safe point and
lists it under the next handoff's "For the owner".

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** wi-927 D-010 (high-interest: the ratchet line
  read through a Trust note instead of a Done-when edit, and the Trust
  count sentence corrected) to D-013; wi-943 D-006, D-007;
  coordinator-2026-10-18 D-005's C2 (the coordinator's own call: bind trunk
  through the kit's existing reader; C1, C3, C4 and C5 are your rulings,
  recorded); and the ones the 2026-10-18d handoff lists (wi-925 D-001 to
  D-004; wi-927 D-008, D-009; wi-943 D-003 to D-005; wi-926 D-001 to
  D-003; and the 2026-10-18c list).
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
