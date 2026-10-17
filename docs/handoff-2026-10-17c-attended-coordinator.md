# Handoff 2026-10-17c (attended): WI-931 landed, WI-912's first build round and intent committed, counted round 1 filed

Overnight: stop

It replaces [handoff-2026-10-17b-attended-coordinator.md](handoff-2026-10-17b-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:** WI-931 as `ab16614fa`, on the box as it was
  (the owner's direction, coordinator-2026-10-17 D-005), its RESYNC entry
  re-anchored at the squash (D-006); the lane tips archived; its re-mint
  WI-939 closed as settled by sitting 003 and act 125 (`ace24c85c`).
- **The bar on a loaded box** (owner, in session; D-005): a landing no
  longer waits for a quiet box. Its staged squash is read beside its
  parent's in one window and both are recorded; a breach close to the
  parent's on the same tier is load. The recipes say the same.
- **Lanes:**
  - `wi-912` (an adjudication sitting ends at its verdict): rebased onto
    `ace24c85c` (D-003; its pre-rebase tip `9169e850c`, reaching the
    critique's reviewed `324787db5`, is archived at its landing). The
    first build round ran in three stages on one builder: stage 1 with
    Terra's rows it needed (`51ffd81b5`), stage 2 (`1dc1d23a0`, its new
    `tests/test_coordinator_act.py` moved to `SLOW_MODULES`, D-004),
    stage 3 (`a1ceb2aac`); Terra's resumed turn then authored the rest
    of the change set at intent (`cbf029136`, D-006). New ids: LLR-338,
    TC-368, IF-296. The prompt catalogue is committed in the lane (the
    hook demands it, D-003). The builder found the act assembler refuses
    a verdict ruling a retired row (fail-closed; D-005), left for the
    reviewers to classify. Counted round 1 (no stance): `001-REVIEW-A-cbf0291` Sol
    CHANGES-REQUESTED, 2 MINOR; `002-REVIEW-B-cbf0291` Opus
    CHANGES-REQUESTED, 1 MAJOR (the retired-row refusal) and 3 MINOR;
    filed at `cad8b7f2c` (D-007), untriaged.
    Next: triage under the threat model, a coverage plan per round file
    before any fix, then the checkpoint (Terra reconcile, closure check,
    one combined sitting), the gate, and landing alone. The checkpoint
    runs in the new shape from the lane root, as the plan's P11 orders:
    the judging turn through `adjudicate --brief-file`, then the lane's
    own `act` turn after the rebase and the unchanged-rows check,
    recorded as a decision.
  - `wi-929`: claimed, no commits, no worktree; move it to trunk's tip
    before cutting it (recipes section 2).
  - Unchanged: `wi-915`, `wi-916`, WI-798, WI-902, and the landed lanes'
    branches and worktrees.
- **Watermark** on trunk: WI 939; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 125. Lane `wi-912` holds LLR 338, TC 368, IF 296.
- **Strict lints:** clean on trunk and on every lane commit this session.
  The full suite at trunk's `ace24c85c`: 6012 passed, 22 skipped, 0 failed
  (16 min 45 s, below normal priority).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/`
  (WI-912's folder: briefs, the spine change list, the arms map, Terra's
  session id `01a14b07-c529-7063-8a1f-3a6083e6d9b1`, the round-1 reviews,
  stage patches). Keep it until WI-912 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each at
below-normal priority.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-912 | Triage counted round 1; fix rounds as owed; checkpoint; gate; land |
| 2 | WI-929 | After WI-912 (its soft edge); `none` |
| 3 | WI-917, WI-916, WI-915 | WI-917 is critique-confirmed; claim it once WI-912 is done |
| 4 | WI-925, WI-926, WI-927 | The hook rows, critique-clean |
| 5 onward | As before | WI-902 (B4), WI-798, then P1 to P8 with WI-918 (critique-confirmed), then leg 03's rows |

## For the owner

- **Asked in session, not yet answered:** should a row make the smoke
  budget step itself judge load (for example by timing the parent in the
  same run), or does the procedure (D-005) suffice? The coordinator leans
  to the procedure alone.
- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** coordinator-2026-10-17 D-005 and D-006; wi-912
  D-003 to D-006; and the ones the 2026-10-17b handoff lists
  (coordinator-2026-10-17 D-003; wi-931 D-005 to D-008; wi-912 D-001 and
  D-002; and earlier unseen ones).
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
