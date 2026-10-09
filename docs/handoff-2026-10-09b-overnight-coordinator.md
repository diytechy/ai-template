# Handoff 2026-10-09b (coordinator, overnight): the consolidation round landed; a 20-row queue for unattended legs

It replaces [handoff-2026-10-09-coordinator.md](handoff-2026-10-09-coordinator.md)
as the resume map. The wave-18, wave-17 and wave-11 handoffs still carry the
in-lane cycle, the roles and the "never" list until WI-848 lands. This
session's record is [log.d/2026-10-09-coordinator.md](log.d/2026-10-09-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **The consolidation round landed:** WI-875 (`5f5f7762`), the owner's
  requested census over 30 queued rows. An independent adjudicator added five
  edges and absorbed nothing:
  - WI-858 needs WI-847;
  - WI-800 needs WI-858;
  - WI-809 needs WI-857;
  - WI-810 needs WI-856;
  - WI-811 needs WI-853.

  Sol's full-lane review `3f40ab16` was SOUND. `archive/lanes` is at
  `12ff03dd`.
- Earlier this session WI-852 and WI-869 landed and WI-874 was filed (see the
  [previous handoff](handoff-2026-10-09-coordinator.md)).
- **Acts** run to seq 75. `docs/work/pause` is tracked and unchanged. No lane
  is open.

## How the night runs (owner, 2026-10-09: "Headless leg loop")

The owner starts
`C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/coordinator-tools/overnight_legs.py --max-legs 6`
from the repo root, in a terminal it leaves open.

1. Each leg is one headless `claude -p` coordinator session, started from the
   newest added handoff's session prompt.
2. The leg works the queue until its context guard latches. It then closes
   out with a new handoff (`docs/handoff-2026-10-09-legNN-coordinator.md`)
   whose session prompt carries the remaining queue, hands the lease back,
   and exits. The loop then starts the next leg from that handoff.
3. Probed this session: a headless leg exits when its turn ends and kills its
   background tasks, so a leg runs EVERYTHING in the foreground. The launcher
   raises the shell tool's foreground cap to 60 minutes through `--settings`.
4. The loop stops on any of these:
   - a handoff line `Overnight: stop`;
   - a failed leg;
   - a lease left held;
   - a leg that wrote no handoff.

   A handoff line `Resume-not-before: <ISO local time>` makes it wait first
   (for a Codex plan limit). Logs go to `C:/Projects/ai-template.wt/overnight-logs/`.

## The queue (20 rows; four after it as stretch)

In order, the owner's stated order first and then the scheduler's. Every
`needs` edge is satisfied in this order.

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-870 | medium | The merge gate reads a review round's VERDICT line strictly, as filing does |
| 2 | WI-853 | medium | Every review finding is a clause the rework plan must cover |
| 3 | WI-848 | medium | The coordinator's procedure is one skill (it describes WI-865's landed dispute path) |
| 4 | WI-834 | medium (large) | Blackout pauses lanes on both routes; run checks the workstation first |
| 5 | WI-847 | medium | The loop's reviewer resumes within a lane; the merge-gating review stays fresh |
| 6 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention |
| 7 | WI-854 | medium | The adjudication briefs carry spine-authoring's tier questions |
| 8 | WI-859 | quick | The conftest isolation test reads pytest's summary line |
| 9 | WI-874 | medium | The runtime store's primary checkout is resolved once per operation |
| 10 | WI-831 | adjudication | Re-judge TC-055 (an observation re-judge; see its spec) |
| 11 | WI-828 | medium | A hand merge on trunk judges the commits it brings in |
| 12 | WI-798 | strong | Account tables and per-account homes for every CLI route |
| 13 | WI-851 | strong | Held-rung spine rows are protected by state |
| 14 | WI-850 | medium | A spine row is approved only after the rows it hangs from |
| 15 | WI-799 | strong | Lane-state provider, representation only |
| 16 | WI-832 | medium | A decisions record has an identity no other run can share |
| 17 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool |
| 18 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 19 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 20 | WI-807 | strong | The station authority, lane-side claims and cancellation |

Stretch: WI-857, WI-808, WI-802 and WI-804. Rows held by the owner are
skipped: WI-684 (OI-98), WI-795 (OI-105) and WI-871 (OI-112).

## For the owner (morning)

- Read `C:/Projects/ai-template.wt/overnight-logs/loop.log` first, then the
  newest handoff. Every call made on your behalf is in `docs/decisions/*.toml`,
  high risk first, for you to confirm or overrule.
- Push `refactor_again` and `archive/lanes`; remove archived worktrees.
- The decisions listed in the previous handoff still await you, plus
  `wi-875.toml` D-001.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator, running UNATTENDED as one headless leg of
the overnight loop (owner, 2026-10-09). The owner is asleep. Nobody will answer
a question: record assumptions instead of asking. This whole leg is ONE turn:
keep working until your close-out is done; ending your reply ends the leg.

FOREGROUND ONLY. A headless session kills its background tasks when it
exits. Never pass run_in_background to Bash or Agent (pass false to Agent).
Never use Monitor, ScheduleWakeup or a wait for a notification. Give long
commands an explicit Bash timeout of up to 3600000 ms (the launcher raised the
cap): sittings, Sol and Terra runs, the smoke bar, the full suite.

1. Take the lease FIRST, with your transcript so occupancy is readable:
   `python project-trajectory/scripts/coordinator_guard.py take --transcript "$(ls ~/.claude/projects/*/$CLAUDE_CODE_SESSION_ID.jsonl | head -1)"`.
   If the take is refused, write nothing, report why, and end.
2. Read, in order: CLAUDE.md; docs/status.md; the newest handoff (the one
   status.md's RESUME HERE names): its State, its queue and its corrections;
   the wave-18, wave-17 and wave-11 handoffs for the in-lane cycle, the roles
   and the "never" list; your memory index and the coordinator traps memories.
3. Work the handoff's queue IN ORDER. Before each claim, check occupancy with
   `coordinator_guard.py status`. Claim nothing once it reads 40% or more, or
   once the guard's drain notice arrives. Claim one or two rows at a time
   under ONE scoped unpause (a reviewed deletion commit, the claims, a
   byte-identical restore), cut each lane from trunk's tip after the restore,
   and land lanes one at a time.
   Per row, the in-lane cycle:
   - Claude Opus builds (kit-builder agent, medium, run_in_background false);
     re-run its claimed results yourself before committing.
   - GPT Terra (medium) authors spine text, UTF-8 only, re-reading every cell
     it splices (coordinator-tools/terra_author.sh).
   - An independent adjudicator judges spine text through
     coordinator_adjudicate.py from the lane (set AGENT_CLAUDE_TOKEN_FILE to
     the token file's path from memory first; never read the file), never a
     subagent.
   - Codex 6.1 Sol (medium) reviews (coordinator-tools/sol_review.sh): narrow
     rounds while a lane iterates, one fresh full-lane review as the last
     gate.
   - Apply the review threat model (PROCESS.md §6) to every finding: dismiss
     one that needs a compromised or contrived host in one recorded line; send
     a contested or third-round finding to the `dispute` sitting, whose ruling
     is final.
   - A lane that is not SOUND after the dispute ruling and two more full-lane
     rounds is left committed on its lane, recorded in the handoff; then move
     on.
   - Land by squash, after a rebase onto trunk. Before the landing commit:
     regenerate the views, run the smoke bar, and run
     `check_trajectory.py --strict`. Give a closed spec `specref = ""` and a
     `## Deliverable`. Archive the tips (empty tree), sweep, and close the
     re-mint citing the act.
4. Decisions: record every call made on the owner's behalf in
   docs/decisions/<branch>.toml (decided, alternative, reversal_cost,
   why_not_escalated, review = ""), high risk first. A decision only the owner
   can make that blocks a row becomes a pending open item holding that row
   (with its placeholder); skip to the next row.
5. Codex limit: if Sol or Terra reports a plan or usage limit, do not wait in
   the session. Bring every lane to a safe committed point, close out (step 6),
   and put a line `Resume-not-before: <ISO local time of the reset + 5 min>`
   in the new handoff. The loop waits for it. If the limit names no reset
   time, use 90 minutes from now.
6. Close-out, at 40% occupancy, at the latch, or when the queue is done:
   - Land or safely commit every in-flight lane.
   - Update docs/status.md (forward-only; its RESUME HERE names your new
     handoff).
   - Write a NEW handoff `docs/handoff-2026-10-09-legNN-coordinator.md` (NN
     is the next leg number). It links the handoff it replaces and carries
     the same sections: State, the remaining queue table, Corrections, For
     the owner. Its `## Session prompt (paste to start the next session)`
     block is THIS prompt, copied verbatim. Add the line `Overnight: stop` to
     the handoff only when the queue and stretch are done or no row can move
     without the owner.
   - Write a log fragment.
   - Run the full unfiltered suite once, in the foreground, from a detached
     worktree with a fixed --basetemp under one dated review-tmp root. Record
     its result, then delete the basetemp and the worktree.
   - Commit.
   - As the very last act, run
     `coordinator_guard.py handback --handoff <the new handoff>`.

Never: push or merge to main; rule an open item or sign an owner-held act;
leave docs/work/pause deleted; read OWNER_SCRATCHPAD.md or the adjudicator's
token file; self-review (Sol reviews; an independent adjudicator judges);
change ~/.claude settings or install software; bypass a commit hook.
```
