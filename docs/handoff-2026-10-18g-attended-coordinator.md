# Handoff 2026-10-18g (attended): WI-918 landed; WI-946 rebased onto it and through counted round 1

Overnight: stop

It replaces [handoff-2026-10-18f-attended-coordinator.md](handoff-2026-10-18f-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:** WI-918 (b2bea0da4; acts 132 and 133), its
  re-mint WI-949 closed citing them (e57e647d2). WI-918's tips are archived
  to `archive/lanes`, with its pre-rebase tip `c539b02b1` as an extra parent.
- **Lanes** (every one committed, its tree clean):
  - `wi-946` at `c4feff497` (base `e57e647d2`, trunk's tip before this
    close-out): build P2 to P7 complete (stage 5 committed this session,
    D-005); rebased onto WI-918's landing (D-006 ordered it, D-007 records
    it); Terra's P8 set committed (D-008: LLR-248's detail and code_symbol,
    TC-242's method and expected, IF-065's data; Terra's retained session
    `01a15213-e656-7dc3-80f8-efb10b91d937`); counted round 1 filed (001 Sol
    APPROVE 0, 002 Opus APPROVE 1 MINOR; D-009); the bar at its tip is
    green (2797 passed; the tier 150 s beside the full suite, load). Next:
    rebase over this
    close-out's docs commit (re-anchor the RESYNC entry); the D-009 wording
    fix on a builder (the launcher docstring's bound and the spec's Trust
    state check-lane's trunk fallback from a lane worktree with the primary
    detached, which the trunk-by-name row ends; no code change); the
    convergence map (002 F1 to the corrected text); the checkpoint (Terra's
    reconcile only if the fix moves row text, the closure check, one
    combined sitting of `amendment:LLR-248;amendment:TC-242`, SR scope
    SR-209), the gate in convergence stance, the act, close, land. Its
    landing is the second gate row's: that session writes its handoff
    without `Overnight: stop`.
  - `wi-918` landed; its branch and worktree remain, archived.
  - `wi-925` at `81d271c6d` and `wi-926` at `d15adb2de`, unchanged: as the
    2026-10-18e handoff says (stage 3 next; counted round 1 next).
  - Unchanged: WI-798, WI-902, and the landed lanes' branches and worktrees.
- **Id floor** (wi-925 D-003, wi-926 D-002), unchanged: wi-925 holds LLR-339
  and TC-369; wi-926 holds SR-240, LLR-340, TC-370 and IF-297. WI-946 mints
  none.
- **Watermark** on trunk: WI 949; SR 239, LLR 338, IF 296, TC 368, OI 114;
  acts to seq 133.
- **Strict lints:** clean on trunk and on every lane commit this session.
- **Full suite:** at trunk's `e57e647d2` (WI-918's landing and its re-mint close), from a detached worktree: 6401 passed, 31 skipped, 0 failed (29 min 01 s).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-18g/` holds
  this session's briefs, verdict drafts and logs; nothing in it is owed.
  The 2026-10-18f root's `wi946/build/` holds WI-946's builder brief and
  change list, both consumed; the 2026-10-18d root keeps only `wi925-s2/`,
  owed at WI-925's P9.

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
| 1 | WI-946 | Rebase over the close-out; the D-009 wording fix; the convergence map; the checkpoint (sitting of LLR-248 and TC-242); the gate; act; close; land |
| 2 | Clear the stop | The session that lands WI-946 writes its handoff without `Overnight: stop`; the owner starts `scripts/coordinator/overnight_legs.py` |
| 3 | WI-925 | Stage 3: Terra's P9, P10; counted round 1 |
| 4 | WI-926 | Counted round 1 |
| 5 onward | As before | WI-897 (amend its queued row first, per WI-927's plan deliverable 6), WI-902 (B4), WI-798, then P1 to P8, then leg 03's rows; WI-940 after the batch |

From row 2 on the queue runs in headless legs (the `coordinator-cycle`
skill's section 7); a leg brings an owner-held step to a safe point and
lists it under the next handoff's "For the owner".

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** wi-918 D-005 to D-008 (D-006: the coordinator
  applied sitting 003's dictated TC-242 deletion itself; D-008: the gate's
  three MINORs to status.md's follow-ups, and F3's correction of D-005's
  brace-form reasoning); wi-946 D-005 to D-009 (D-006: P8 and round 1 moved
  after WI-918's landing, a reorder of the queue row; D-007: a builder
  resolved the rebase; D-009: the round-1 MINOR fixed in wording, no
  guard); and the ones the 2026-10-18f handoff lists (wi-943 D-006 to
  D-008; wi-918 D-001 to D-004; wi-946 D-001 to D-004; the 2026-10-18e
  list).
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
