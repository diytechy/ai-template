# Handoff 2026-10-17d (attended): WI-912 landed in the new verdict-then-act shape; WI-940 filed

Overnight: stop

It replaces [handoff-2026-10-17c-attended-coordinator.md](handoff-2026-10-17c-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:** WI-912 (a sitting ends at its committed verdict;
  its act is a later turn) as `5604f0fd9`, its RESYNC entry re-anchored at
  `702ce8511` with the regenerated prompt catalogue added to its overwrite
  list (wi-912 D-013). Its re-mint WI-941 closed as settled by sitting 005
  and act 126 (`773f77dd6`). The lane tips are archived to `archive/lanes`
  with both pre-rebase tips (`796c68ba8`, `9169e850c`) as extra parents.
  Its lane ran: counted round 1 triaged (D-008; the owner ruled the
  retired-row MAJOR accepted), the fix round (D-009: a retirement on a held
  rung owes no act), counted round 2 with MINORs only (D-010; two
  consolidated before the checkpoint), Terra's reconcile, combined sitting
  005 (ten amendments blessed, LLR-338 and TC-368 approved), the rebase,
  the lane's own act turn (acts 126 and 127, `act: complete`: the new
  shape's first live use, D-011), and the gate in convergence stance after
  the map (D-012): Sol APPROVE 0, Opus APPROVE 5 MINOR (D-013).
- **Filed this session:** WI-940, a CPU-time smoke budget (`702ce8511`),
  from the owner's ruling with its three filing calls
  (coordinator-2026-10-17 D-007). Queued after the current batch; its scope
  critique runs when it comes up for claim.
- **The next mechanism lane may start:** the cycle has run through WI-912's
  changed step (its own checkpoint took its act through the act turn).
  Every later checkpoint sits in that shape: `adjudicate --brief-file ...`,
  then `act --verdict <path> --wi WI-NNN` from the lane after the rebase.
- **Lanes:**
  - `wi-929`: claimed, no commits, no worktree; move it to trunk's tip
    before cutting it (recipes section 2). It is next.
  - Unchanged: `wi-915`, `wi-916`, WI-798, WI-902, and the landed lanes'
    branches and worktrees (`wi-912`'s included).
- **Two rows owed on trunk** (wi-912 D-008, D-009; status.md's unfiled
  follow-ups): the merge slot authorizes a MEANING re-attestation only for a
  blessed row; and it admits a retirement whose registry carries no other
  act in the branch. The second lands before the first lane whose sitting
  retires a row alone in its registry (item 14's sidecar retirement may).
- **Watermark** on trunk: WI 941; SR 239, LLR 338, IF 296, TC 368, OI 114;
  acts to seq 127.
- **Strict lints:** clean on trunk and on every lane commit this session.
  The full suite at trunk's `773f77dd6`: 6088 passed, 22 skipped, 0 failed
  (18 min 25 s, below normal priority).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/`
  may be deleted once the owner has read this handoff; nothing in it is
  owed.

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
| 1 | WI-929 | Move to trunk's tip, cut, build (`none`); its soft edge on WI-912 is met |
| 2 | WI-917, WI-916, WI-915 | WI-917 is critique-confirmed; claim it now that WI-912 is done |
| 3 | WI-925, WI-926, WI-927 | The hook rows, critique-clean |
| 4 | The two merge-slot rows | File on trunk (status.md's unfiled list); the retirement one before item 14's lane |
| 5 onward | As before | WI-902 (B4), WI-798, then P1 to P8 with WI-918 (critique-confirmed), then leg 03's rows; WI-940 after the batch |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** wi-912 D-009 (a retirement on a held rung owes
  no act, read as SR-228's scope), D-010 (two MINOR second homes
  consolidated before the checkpoint and reviewed at the gate, rather than
  filed as rows), D-011 to D-013; and the ones the 2026-10-17c handoff lists
  (coordinator-2026-10-17 D-005, D-006; wi-912 D-001 to D-006; and earlier
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
