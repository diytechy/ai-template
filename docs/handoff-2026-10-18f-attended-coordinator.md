# Handoff 2026-10-18f (attended): WI-943 landed; the gate rows claimed, planned and built

Overnight: stop

It replaces [handoff-2026-10-18e-attended-coordinator.md](handoff-2026-10-18e-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:** WI-943 (96c6ce1dc; act seq 131), its re-mint
  WI-948 closed citing the act (4a5d9f068). The gate rows' scoped unpause:
  the pause deleted (73b369229), WI-918 and WI-946 claimed (1f31d0078,
  44562adf4), the pause restored byte-identical (7c59c67d1).
- **Lanes** (every one committed, its tree clean):
  - `wi-918` at `c539b02b1` (base `7c59c67d1`): single plan, critique 1 (one
    MINOR, an all-MINOR critique passes; D-001), pass record; build P1 to P6
    (stages 1 and 2 committed together, D-001; the plan places the spine
    turn at the checkpoint, so no intent turn ran, D-002); counted round 1
    filed (001 Sol CHANGES-REQUESTED 1 MINOR, 002 Opus APPROVE 1 MINOR;
    D-003) and both wording MINORs fixed (D-004). Next: the checkpoint.
    Rebase onto trunk first (trunk moved by WI-943's landing and this
    close-out; the lane meets RESYNC_PACK.md only; re-anchor its entry),
    then Terra's first turn (one retained session from here) authors the
    plan's P7 set from the settled code (SR-209's acceptance, LLR-248's
    detail, TC-242's method and expected, IF-194's data and rationale; its
    spine change list is `C:/Projects/ai-template.wt/review-tmp/2026-10-18f/wi918/build/spine-changes.md`),
    the closure check, one combined sitting, the convergence map (both
    round-1 findings map to the corrected text at c539b02b1's sites; no test
    asserts the wording), the gate in convergence stance, the act, close,
    land. It lands before WI-946.
  - `wi-946` at `6f6ecc8dc` (base `7c59c67d1`): single plan, critique 1
    APPROVE 0, pass record; build stages 1 to 4 committed (P2 the
    extraction, P3 the checked claim reader, P4 the trunk bind and checkout
    hold, P5 the archive's descent; D-001 to D-004). Next: stage 5 (P6 the
    launcher's docstring, P7 the skill section 7 clause) on a fresh
    kit-builder (the brief is
    `C:/Projects/ai-template.wt/review-tmp/2026-10-18f/wi946/build1-brief.md`),
    then Terra's P8 (LLR-248's detail and code_symbol, TC-242's method and
    expected, IF-065's data; spine change list
    `C:/Projects/ai-template.wt/review-tmp/2026-10-18f/wi946/build/spine-changes.md`),
    counted round 1, and the rest of the cycle. It rebases onto WI-918's
    landing, which edits the same functions (`_loop_window`, `lane_refusal`)
    and the same rows (LLR-248, TC-242), and re-sits the shared rows.
  - `wi-925` at `81d271c6d` and `wi-926` at `d15adb2de`, unchanged: as the
    2026-10-18e handoff says (stage 3 next; counted round 1 next).
  - `wi-943` landed; its branch and worktree remain, archived
    (archive/lanes `2cc7a18d3`).
  - Unchanged: WI-798, WI-902, and the landed lanes' branches and worktrees.
- **Id floor** (wi-925 D-003, wi-926 D-002), unchanged: wi-925 holds LLR-339
  and TC-369; wi-926 holds SR-240, LLR-340, TC-370 and IF-297. Neither gate
  lane has minted an id yet; brief their Terra turns with that floor.
- **Watermark** on trunk: WI 948; SR 239, LLR 338, IF 296, TC 368, OI 114;
  acts to seq 131.
- **Strict lints:** clean on trunk and on every lane commit this session.
- **Full suite:** at trunk's `4a5d9f068` (WI-943's landing and its re-mint close), from a
  detached worktree: 6386 passed, 31 skipped, 0 failed (27 min 21 s).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-18f/` keeps the
  two lanes' build folders (`wi918/build/`, `wi946/build/`: the spine change
  lists, owed at each checkpoint) and WI-946's build brief; the rest is
  logs. The 2026-10-18e root holds nothing owed (kept: the owner had a file
  in it open); the 2026-10-18d root keeps only `wi925-s2/`, owed at WI-925's
  P9.

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
| 1 | WI-918 | Rebase; the checkpoint (Terra's P7 set, closure check, combined sitting, convergence map, gate); act; close; land |
| 2 | WI-946 | Stage 5 (P6, P7); Terra's P8; counted round 1 onward; rebase onto WI-918's landing and re-sit LLR-248 and TC-242; land |
| 3 | Clear the stop | The session that lands WI-946 writes its handoff without `Overnight: stop`; the owner starts `scripts/coordinator/overnight_legs.py` |
| 4 | WI-925 | Stage 3: Terra's P9, P10; counted round 1 |
| 5 | WI-926 | Counted round 1 |
| 6 onward | As before | WI-897 (amend its queued row first, per WI-927's plan deliverable 6), WI-902 (B4), WI-798, then P1 to P8, then leg 03's rows; WI-940 after the batch |

From row 3 on the queue runs in headless legs (the `coordinator-cycle`
skill's section 7); a leg brings an owner-held step to a safe point and
lists it under the next handoff's "For the owner".

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** wi-943 D-006 to D-008; wi-918 D-001 (stages 1
  and 2 committed together; the all-MINOR critique passed with the plan
  unedited) to D-004; wi-946 D-001 to D-004; and the ones the 2026-10-18e
  handoff lists (wi-927 D-010 to D-013; coordinator-2026-10-18 D-005's C2;
  wi-925 D-001 to D-004; wi-927 D-008, D-009; wi-943 D-003 to D-005; wi-926
  D-001 to D-003; and the 2026-10-18c list).
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
