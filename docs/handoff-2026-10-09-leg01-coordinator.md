# Handoff 2026-10-09 leg 01 (coordinator, overnight): WI-870 and WI-853 built and committed on their lanes; Codex limit

It replaces [handoff-2026-10-09b-overnight-coordinator.md](handoff-2026-10-09b-overnight-coordinator.md)
as the resume map. The wave-18, wave-17 and wave-11 handoffs still carry the
in-lane cycle, the roles and the "never" list until WI-848 lands. This leg's
record is [log.d/2026-10-09-leg01-coordinator.md](log.d/2026-10-09-leg01-coordinator.md).

Resume-not-before: 2026-10-09T06:18:00-05:00

## State (trunk `refactor_again`, nothing pushed)

- **Claimed under one scoped unpause** (`0b832cc2`; claims `fdaae1fa` and
  `471444ee`; the pause restored byte-identical in `c5076d62`): WI-870 and
  WI-853. Both lanes were cut at `c5076d62`, under
  `C:/Projects/ai-template.wt/wi-870` and `.../wi-853`. Both are committed
  and clean, and neither has landed.
- **WI-870 (lane tip `e72e3a2d`).**
  - **Built:** one strict review VERDICT-line reader, `kitlib.sitting.review_line`.
    The gate (`score_reviews.parse_verdict`) and filing (`review_brief`) both
    call it.
  - **The shared per-line reader** refuses a duplicated field.
  - **PROCESS.md** now teaches the one machine line.
  - **Spine:** Terra amended the rows. Sitting 001 judged LLR-046, LLR-207,
    LLR-310, LLR-313, TC-083 and TC-327 as MEANING and re-attested all six
    (act commit `205c9310`).
  - **Owed:** a fresh full-lane Sol review. Its prompt is
    `C:/Projects/ai-template.wt/review-tmp/leg01/sol-870.md`, at SHA `e72e3a2d`.
    The run died on the usage limit, so no review exists. If SOUND, land it.
  - **At the landing,** run `gen_verdict_rollup.py` on trunk. Four rollups
    go stale by design (wi-870.toml D-002); the lane cannot write them.
- **WI-853 (lane tip `ea348d61`).**
  - **Built:** `plan_coverage.py --findings` reads a review verdict.
    `finding_clauses` is the shared F# step. A dispute exclusion must cite an
    accepted DISMISS. The coordinator's half is a session-protocol §2 bullet
    (WI-848 moves it).
  - **Spine:** Terra amended LLR-069, TC-069 and IF-046's data.
  - **Owed, in order:**
    1. Rebase onto trunk AFTER WI-870 lands. Both lanes edit IF-046's `data`
       cell, so merge the two texts by hand and check the cell's meaning.
    2. The combined amendment sitting (`amendment:LLR-069;amendment:TC-069`).
       It is held until the rebase, so act seqs stay unique.
    3. A fresh full-lane Sol review, then land.
  - **Open note from Terra:** SR-155 ("Contested planning rounds") may not
    carry the rework gate. The spec names SR-155's chain, so let the sitting
    judge it.
- **Full suite** at `c5076d62`: 5492 passed, 17 skipped, 0 failed in 762.6 s.
- **Acts** run to seq 75 on trunk; WI-870's lane holds one more.
  `docs/work/pause` is tracked and unchanged.

## The queue (rows 1 and 2 in flight; 18 queued; four stretch)

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-870 | medium | IN FLIGHT: full-lane Sol review, then land |
| 2 | WI-853 | medium | IN FLIGHT: rebase after WI-870, sitting, full-lane Sol, land |
| 3 | WI-848 | medium | The coordinator's procedure is one skill (it moves WI-853's rework bullet too) |
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

## Corrections learned this leg

- **Codex capacity is the bottleneck.** The limit hit after only four Codex
  sessions (two Terra runs, then two Sol runs started together). The account
  was already depleted by the previous session. Run the two lanes' Sol
  reviews one at a time, so a limit takes out at most one review.
- **Order the sitting before Sol** (coordinator-2026-10-09-leg01.toml D-001).
  Then one fresh full-lane Sol review can be both the first review and the
  last gate.
- **Terra can drop an existing `code_symbol` entry** as "nonexistent". It
  did so with `_keyword_count_refusal`, which is restored in `847d782e`.
  Grep every symbol it removes.
- **Redirect every commit's output to a file.** The pre-commit hook prints
  about 80 KB.
- **Restamp the complexity baseline in the lane commit** when a function
  leaves it (`check_complexity.py --restamp`). The hook refuses a stale row.
- **`gen_verdict_rollup.py` refuses on a work branch.** A lane that changes
  how rounds read leaves its rollups to the trunk landing.
- **The claim's status.md prose guard** now has nothing to trip on: the
  resume list names the rows by subject.

## For the owner (morning)

- Read `C:/Projects/ai-template.wt/overnight-logs/loop.log` first, then the
  newest handoff.
- **Decisions to confirm or overrule, high risk first:**
  - `wi-870.toml` D-001 (PROCESS.md's review block teaches the machine line)
    and D-002 (86 historical review files now read as unparseable; listed in
    the log fragment, not rewritten);
  - `wi-870.toml` D-003;
  - `wi-853.toml` D-001 to D-003;
  - `coordinator-2026-10-09-leg01.toml` D-001 to D-003.
- The previous handoff's decisions and `wi-875.toml` D-001 still await you.
- Push `refactor_again` and `archive/lanes`, and remove archived worktrees.

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
