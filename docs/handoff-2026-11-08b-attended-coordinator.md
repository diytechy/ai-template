# Handoff 2026-11-08b (attended): OI-129 ruled build; WI-1000, WI-999 and WI-1001 join the queue

It replaces [handoff-2026-11-08a-leg38-coordinator.md](handoff-2026-11-08a-leg38-coordinator.md)
as the resume map, and carries its owner items unchanged except where this
file says. The procedure is in the `coordinator-cycle` skill and its recipes;
this handoff holds state only. The owner asked, in this attended session, for
the overnight leg runner to resume, so this handoff carries no stop line.

## What happened

- **OI-129 ruled** (`0032ffdd8`): Q1 (a) and Q2 (a). SR-165's derivation
  record (WI-999) and SR-035's token scan (WI-1000) are built. The owner:
  approved rows are built unless evidence shows substantial work, and none
  does. Both rows dropped their `needs` on the item, their Done-when lists
  now carry the build, and each `specref` names its LLR (LLR-172, LLR-171).
- **The coordinator-cycle skill** now states, beside the owner-held steps,
  that an approved row with nothing built behind it is build debt filed as a
  work item, never an open item, unless evidence shows substantial work.

## State (trunk `refactor_again`)

- **Open claims:** none.
- **Primary checkout:** on `refactor_again`, clean.
- **Bars:** the ruling commit's smoke bar: 3459 passed, 3 skipped; CPU 576.8 s
  against `cpu-seconds = 540`, reported only (leg 38 read 543.3 s). Judge both
  at the next `run.cmd audit`. The full suite last ran green at `633715041`;
  nothing since changed code.
- **Pause:** `docs/work/pause` is tracked and unchanged.
- **Scratch:** leg 38's root `C:/Projects/ai-template.wt/review-tmp/2026-11-07-leg38/`
  is still to delete.

## The queue

The owner's order stands (coordinator-2026-11-03 D-003 and D-004), with this
session's additions (owner, 2026-11-08). **Only the rows in this table are
claimed**, in order and under their `needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-1000 | SR-035's token scan. Owes its scope critique, then its claim |
| 2 | WI-999 | SR-165's derivation record. Owes its scope critique, then its claim. The derivation its records hold was worked in the 2026-08-16 derivation plans under `docs/plans/` |
| 3 | WI-1001 | Critique confirmed. Claimed once WI-1000 and WI-999 land (its `needs`). Reusing WI-997's gating sends an adopter strict-red at DevStg-Impl until every case is tagged (coordinator-2026-11-06 D-003) |
| 4 | WI-910 | Held on OI-124: push, or the owner rules the WSL POSIX route. Skip it while held |

**Never claimed by a leg:** WI-684 (OI-98, the owner's re-sync); WI-795
(OI-105, then WI-820); WI-827 (attended only; it never lands from a lane);
WI-908 (OI-122: the owner present); WI-964 (OI-123: the owner's Mac); WI-998
(off the table until a sample exists); every row under `docs/work/deferred/`
(D-011, D-016).

WI-996's changed steps run at the next lane's first attest, its refresh and
its hand landing: the lane's `[bars] red_mark` declaration is already on
trunk. WI-993's held-act arm and WI-983's decomposition arm are still waiting
for a row that exercises them.

## For the owner

1. **OI-129 is ruled;** items 1 and 6 of the replaced handoff are answered.
2. Unchanged from the replaced handoff: its items 2 (WI-996's forced adopter
   migration), 3 (wi-996 D-005), 4 (wi-996 D-007 and D-010), 5 (the usage
   ingest's `session-owner` refusal), 7 (OI-124 and OI-121), 8 (the
   2026-11-07c handoff's carried items) and 9 (leg 38's calls to confirm or
   overrule).

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
