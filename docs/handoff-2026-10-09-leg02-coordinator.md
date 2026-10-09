# Handoff 2026-10-09 leg 02 (coordinator, overnight): WI-870, WI-853 and WI-848 landed; WI-834 in flight; Codex limit

It replaces [handoff-2026-10-09-leg01-coordinator.md](handoff-2026-10-09-leg01-coordinator.md)
as the resume map. **Procedure now lives in the `coordinator-cycle` skill**
(`.claude/skills/coordinator-cycle/`, landed this leg as WI-848): the in-lane
cycle, the roles, the recipes and the "never" list. This handoff holds state
only. This leg's record is
[log.d/2026-10-09-leg02-coordinator.md](log.d/2026-10-09-leg02-coordinator.md).

Resume-not-before: 2026-10-09T11:48:00-05:00

## State (trunk `refactor_again`, nothing pushed)

- **Landed this leg.** Each went by squash after a rebase, with the views
  regenerated and the smoke bar and `check_trajectory.py --strict` run first:

  | Row | Squash | Acts | Re-mint closed |
  |---|---|---|---|
  | WI-870 | `03db0ead` | 76 | WI-876 (`0b550da9`) |
  | WI-853 | `c6a2eab8` | 77, 78, 79 (SR-236 approved) | WI-877 (`75fc5a68`) |
  | WI-848 | `9aace2e9` | none | none minted |

- **Filed:** WI-878 (P4), the follow-up WI-853's dispute 006 named: a dispute
  sitting's binding records the findings file it ruled. Until it lands, give
  a lane's dispute findings ids that are unique within the lane.
- **WI-834 (the blackout row) is IN FLIGHT.**
  - **Lane:** `wi-834` at `C:/Projects/ai-template.wt/wi-834`, cut at
    `d2d8b8f4`, tip `9bc1eb2a`, committed and clean.
  - **Claim:** under its own scoped unpause (`dd3d6b64`; the claim is
    `756987d7`; the pause was restored byte-identical in `d2d8b8f4`).
  - **Built:** parts B, C and D, by the builder. The coordinator's lane
    re-run of the whole suite read 5592 passed, 20 skipped.
  - **Spine:** authored by Terra in its retained session
    `01a1212d-f1dd-7590-9fff-bf530c31df5f` (resume it). No sitting yet.
    - New: SR-237, LLR-316 to LLR-319, IF-291, IF-292, TC-335 to TC-342.
    - Amended: SR-229, SR-230, LLR-270, LLR-300, LLR-301, IF-157, IF-158,
      IF-246, IF-248, IF-271, IF-274, IF-275, IF-280, IF-281, and IF-283 to
      IF-285.
  - **Review:** round 001 (`docs/reviews/wi-834/001-REVIEW-A-785a004.md`) is
    full-lane, CHANGES-REQUESTED, with 5 findings.
    - F1 and F3 (code) are answered in `9bc1eb2a`, after `plan_coverage`
      passed (`docs/reviews/wi-834/001-PLAN-r1.md`).
    - F2, F4 and F5 (spine text) are excluded to the checkpoint.
  - **Owed, in order:**
    1. The narrow Sol review of `a2c94eed..9bc1eb2a`, answering round 001.
       Its brief is rendered at
       `C:/Projects/ai-template.wt/review-tmp/leg02/sol-834-r2-prompt.md`.
       The run died on the Codex limit, so no review exists. Re-render the
       brief if the tip moves.
    2. The checkpoint. Terra (resumed) reconciles round 001's spine findings:
       - F2: SR-227 carries the blackout exception to its rule that a session
         retires only when nothing it has a stake in is pending;
       - F4: SR-229's outside-window lease and latch apply only when the
         guard is enabled;
       - F5: SR-230's acceptance excludes blackout, and LLR-301 attributes
         the cancellation to the hook dispatch.

       It also reconciles LLR-300's detail (the shell reading), IF-275 (the
       unreadable-line denial) and the existing approved TCs TC-266, TC-267,
       TC-329, TC-315 to TC-318 and TC-322. Record OI-69 (c2) as overruled
       (the owner's 2026-10-05 ruling, quoted in the spec) in the same commit.
    3. One combined sitting:
       - amendments: SR-227, SR-229, SR-230, LLR-270, LLR-300, LLR-301 and
         the amended TCs;
       - first approvals: SR-237, LLR-316 to LLR-319 and TC-335 to TC-342.
    4. The fresh full-lane Sol gate, then land.
- **Full suite** at `d2d8b8f4`, trunk's tip before the close-out: **5510
  passed, 17 skipped, 0 failed** in 878 s. It ran from a detached worktree
  with a fixed basetemp, both deleted once the result was recorded.
- **Acts** run to seq 79 on trunk.
- **Watermark** on trunk: SR 236, LLR 315, IF 290, TC 334, WI 878. WI-834's
  lane holds SR 237, LLR 319, IF 292 and TC 342.
- `docs/work/pause` is tracked and unchanged.

## The queue (row 1 in flight; 17 queued; four stretch)

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-834 | medium (large) | IN FLIGHT: narrow Sol, checkpoint, sitting, full-lane Sol, land |
| 2 | WI-847 | medium | The loop's reviewer resumes within a lane; the merge-gating review stays fresh |
| 3 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention |
| 4 | WI-854 | medium | The adjudication briefs carry spine-authoring's tier questions |
| 5 | WI-859 | quick | The conftest isolation test reads pytest's summary line |
| 6 | WI-874 | medium | The runtime store's primary checkout is resolved once per operation |
| 7 | WI-831 | adjudication | Re-judge TC-055 (an observation re-judge; see its spec) |
| 8 | WI-828 | medium | A hand merge on trunk judges the commits it brings in |
| 9 | WI-798 | strong | Account tables and per-account homes for every CLI route |
| 10 | WI-851 | strong | Held-rung spine rows are protected by state |
| 11 | WI-850 | medium | A spine row is approved only after the rows it hangs from |
| 12 | WI-799 | strong | Lane-state provider, representation only |
| 13 | WI-832 | medium | A decisions record has an identity no other run can share |
| 14 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool |
| 15 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 16 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 17 | WI-807 | strong | The station authority, lane-side claims and cancellation |
| 18 | WI-878 | medium | A dispute sitting's binding records the findings file it ruled |

Stretch: WI-857, WI-808, WI-802 and WI-804. Rows held by the owner are
skipped: WI-684 (OI-98), WI-795 (OI-105) and WI-871 (OI-112).

## Corrections

None of its own. Procedure lives in the `coordinator-cycle` skill, which
WI-848 made its one home. This leg folded two lessons into the skill's
recipes §5: Terra's throughput on a large change set, and the closed set of
IF channels.

## For the owner (morning)

- Read `C:/Projects/ai-template.wt/overnight-logs/loop.log` first, then this
  handoff.
- **Decisions to confirm or overrule, high risk first:**
  - `coordinator-2026-10-09-leg02.toml`:
    - D-001: two lanes landed on a review whose only finding a final dispute
      ruling dismissed, with no further Sol round;
    - D-002: SR-236 was drafted and approved in the lane after a dispute
      ruled FIX;
    - then D-003 to D-006.
  - `wi-853.toml` D-004 to D-006, and D-001 to D-003 from leg 01.
  - `wi-848.toml` D-001 to D-010 (high risk: D-001 and D-003).
  - `wi-870.toml` D-001 to D-003. D-002 now names 87 files, listed in
    `log.d/2026-10-09-wi-870-verdict-migration.md`.
  - WI-834's lane record, `wi-834.toml` D-001 to D-012, which lands with the
    lane. High risk:
    - D-001: the guard's hooks ship to adopters;
    - D-004: every SendMessage is denied inside a window;
    - D-005: the dispatcher's tick holds inside a window;
    - D-010: an unreadable command line fails closed inside a window.
  - Still awaiting you: leg 01's `coordinator-2026-10-09-leg01.toml` D-001 to
    D-003, the earlier handoffs' decisions, and `wi-875.toml` D-001.
- Push `refactor_again` and `archive/lanes`. Remove the archived worktrees
  `wi-870`, `wi-853` and `wi-848` when convenient.

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
