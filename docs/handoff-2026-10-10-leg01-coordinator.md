# Handoff 2026-10-10 leg 01 (coordinator, overnight): six landings, the census, and the queue from WI-887

It replaces [handoff-2026-10-10d-overnight-coordinator.md](handoff-2026-10-10d-overnight-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The leg's record is
[log.d/2026-10-10-leg01-coordinator.md](log.d/2026-10-10-leg01-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Landed this leg:** WI-881 (`b059c8a4`), WI-884 (`b6766302`), WI-823
  (`d40e9af0`), WI-831 (`a585d78c`, TC-055 RECORDED pass), the census WI-900
  (`13c18bec`), WI-894 (`2790c823`) and WI-892 (`8d498e13`). Re-mints
  WI-896, WI-898 and WI-899 closed as settled. Lane tips are archived in
  `archive/lanes`.
- **No lane is out and no judgement is active.** `docs/work/pause` is
  tracked and byte-identical to its earlier content (three scoped unpauses
  this leg, each restored in the next commit).
- **Reviewer:** the signed-in Codex account does not offer `gpt-6.1-sol`;
  every review ran on `gpt-6-luna` at high (coordinator D-017, high risk,
  pending the owner). Terra (`gpt-5.6-terra`) works. Probe the account's
  model list at the leg's start (recipes §7).
- **Census outcome:** WI-802 returned to draft (`docs/work/draft/`); it
  must be redrafted to name WI-887's two dials before it can queue. The
  census recorded, without enacting: WI-801 and WI-811 should each need
  WI-878; WI-808's Done-when should point at WI-892's walk, not WI-828's.
- **Filed:** WI-901 (a disposition brief for an empty commit range) and
  WI-902 (a disposition names an already-filed successor), both from
  WI-894 (D-022). WI-893 now carries `supersedes = "WI-828"`.
- **Watermark** on trunk: SR 238, LLR 326, IF 293, TC 350, WI 902, OI 113.
  Acts run to seq 105.
- **Full suite** at `8d498e13` (detached worktree): **5708 passed, 18
  skipped, 0 failed** in 1043 s.
- **Another session committed on trunk** during this leg's lease:
  `1f87388b` (WI-897 filed, "owner request", 17:43 local).

## The queue

The census reordered nothing it enacted; WI-878 moves ahead of WI-801 on
its recorded overlap. Rows needing a scope critique owe it before their
claim (minted adjudication rows excepted, D-020).

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-887 | strong | The loop's reviewer resumes within a lane; the final reviewer is configurable, fresh or persisted (WI-884 landed) |
| 2 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention (needs WI-887) |
| 3 | WI-895 | quick | A keep-warm ping's tree-end failure stops the run (WI-881 landed) |
| 4 | WI-897 | quick | The guard hook costs less per tool call (owner request) |
| 5 | WI-901 | quick | A disposition brief composes for an empty commit range |
| 6 | WI-902 | medium | A disposition can name an already-filed successor |
| 7 | WI-798 | strong | Account tables and per-account homes for every CLI route |
| 8 | WI-851 | strong | Held-rung spine rows are protected by state (WI-892 landed) |
| 9 | WI-850 | medium | A spine row is approved only after the rows it hangs from (WI-892 landed) |
| 10 | WI-799 | strong | Lane-state provider, representation only |
| 11 | WI-832 | medium | A decisions record has an identity no other run can share |
| 12 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool |
| 13 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 14 | WI-878 | medium | A dispute sitting's binding records the findings file it ruled (before WI-801, census) |
| 15 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 16 | WI-807 | strong | The station authority, lane-side claims and cancellation |

Stretch: WI-833, WI-857, WI-808 and WI-804. WI-802 is in draft (census).
Rows held by the owner are skipped: WI-684 (OI-98), WI-795 (OI-105), WI-871
(OI-112) and WI-893 (OI-113); WI-827 is the owner's signature.

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the worktrees of
  landed lanes when convenient: `wi-881`, `wi-884`, `wi-823`, `wi-831`,
  `wi-900`, `wi-894`, `wi-892` (and the earlier `wi-882`, `wi-828`,
  `wi-880`, `wi-886`, `wi-888`, `wi-834`, `wi-854`, `wi-859`, `wi-847`,
  `wi-874`). WI-828's parked patch is now a sketch only (WI-892 landed its
  shared-walk half).
- **Sign in a Codex account that offers `gpt-6.1-sol`**, or confirm Luna:
  D-017 below.
- **Rule OI-113** (holds WI-893); OI-98, OI-105 and OI-112 still wait.
- **Decisions to confirm or overrule**, high risk first:
  - `docs/decisions/coordinator-2026-10-10.toml`: D-017 (Luna for Sol on
    every review this leg, including the landed WI-881 and WI-884 gates),
    D-022 (WI-894's verdict accepted without a composed brief), then D-015
    and D-014 from 10c; D-018 to D-021 (WI-823 one lane; the B3 rubric
    proposal routed to you; minted adjudication rows claimed without a
    critique; WI-892's critique closed at round 1). D-001 to D-013 and D-016
    still await you.
  - `docs/decisions/wi-823.toml`: D-002 (landed on a gate whose one finding
    a dispute dismissed, with no second gate; the 2026-10-09 leg-02
    precedent, also pending), D-001.
  - `docs/decisions/wi-892.toml`: D-002 (the walk takes the caller's commit
    list), D-001, D-003.
  - `docs/decisions/wi-881.toml`: D-008, then D-002, D-004, D-001, D-003,
    D-005 to D-007. `docs/decisions/wi-884.toml`: D-011, then D-001 to
    D-003 (downstream migrations), D-004 to D-010.
- **Follow-up topics, unfiled:** the scope critic twice proposed a rubric
  anchor B3 (a scope covers its cited SN/SR intent; a move names the
  invariants it keeps) for `docs/rubrics/scope-critique.md` (D-019, D-021);
  LLR-055's child-row list omits T4, T5 and T8's test rows (predates
  WI-823); the hook's range listing lacks `--topo-order` (wi-892 D-002).

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator, running UNATTENDED as one headless leg of
the overnight loop (coordinator-tools/overnight_legs.py). The owner is away.
Nobody will answer a question: record assumptions instead of asking. This
whole leg is ONE turn: keep working until your close-out is done; ending your
reply ends the leg.

FOREGROUND ONLY. A headless session kills its background tasks when it
exits. Never pass run_in_background to Bash or Agent (pass false to Agent).
Never use Monitor, ScheduleWakeup or a wait for a notification. Give long
commands an explicit Bash timeout of up to 3600000 ms (the launcher raised the
cap): sittings, Sol and Terra runs, the smoke bar, the full suite. Where the
skill's recipes say "launch with run_in_background: true", run it in the
foreground with that timeout instead.

1. Take the lease FIRST, with your transcript so occupancy is readable:
   `python project-trajectory/scripts/coordinator_guard.py take --transcript "$(ls ~/.claude/projects/*/$CLAUDE_CODE_SESSION_ID.jsonl | head -1)"`.
   If the take is refused, write nothing, report why, and end.
2. Read, in order: CLAUDE.md; docs/status.md; the newest handoff (the one
   status.md's RESUME HERE names): its State, its queue and its "For the
   owner"; the coordinator-cycle skill and its references/recipes.md (the
   procedure's one home: roles, the in-lane cycle, landing, the "never"
   list); your memory index.
3. Work the handoff's queue IN ORDER, as the coordinator-cycle skill
   describes. Before each claim, check occupancy with
   `coordinator_guard.py status`. Claim nothing once it reads 40% or more, or
   once the guard's drain notice arrives. Claim one or two rows at a time
   under ONE scoped unpause (a reviewed deletion commit, the claims, a
   byte-identical restore), each row's scope critique answered first; cut
   each lane from trunk's tip after the restore, and land lanes one at a time.
   - Roles: Claude Opus builds (kit-builder agent, medium); GPT Terra
     (medium) authors spine text in one retained session per lane; Codex 6.1
     Sol (medium) reviews, narrow rounds while a lane iterates and one fresh
     full-lane review as the last gate; an independent adjudicator judges
     spine text and disputes through coordinator_adjudicate.py from the lane
     (set AGENT_CLAUDE_TOKEN_FILE to the token file's path from memory first;
     never read the file), never a subagent.
   - Apply the review threat model (PROCESS.md section 6) to every finding;
     send a contested or third-round finding to the dispute sitting, whose
     ruling is final. A lane not SOUND after the dispute ruling and two more
     full-lane rounds is left committed on its lane, recorded in the handoff;
     move on.
   - A queue row named "census" means: once no lane is out and no judgement
     is active, mint the consolidation row through
     `intake.mint_consolidation` (it refuses with a reason when the station
     is not idle; record the reason and retry at the next idle point), claim
     it, sit it through the entry point with the `consolidate` brief, land it
     (recipes section 8), and reorder the rest of the queue by its outcome.
   - Before each landing commit: regenerate the views, run the smoke bar and
     its budget, read the summary for failures, and run
     `check_trajectory.py --strict`.
4. Decisions: record every call made on the owner's behalf in
   docs/decisions/<branch>.toml (coordinator-<date>.toml on trunk), high risk
   first. A decision only the owner can make that blocks a row becomes a
   pending open item holding that row; skip to the next row.
5. Codex limit: if Sol or Terra reports a plan or usage limit, do not wait in
   the session. Bring every lane to a safe committed point, close out (step
   6), and put a line `Resume-not-before: <ISO local time of the reset + 5
   min>` in the new handoff. The loop waits for it. If the limit names no
   reset time, use 90 minutes from now.
6. Close-out, at 40% occupancy, at the latch, or when the queue is done
   (session-protocol section 4):
   - Land or safely commit every in-flight lane.
   - Update docs/status.md (forward-only; its RESUME HERE names your new
     handoff).
   - Write a NEW handoff `docs/handoff-<today, YYYY-MM-DD>-legNN-coordinator.md`
     (NN is one more than the newest leg handoff's number for today, else
     01). It links the handoff it replaces and carries State, the remaining
     queue table and For the owner. Its `## Session prompt (paste to start
     the next session)` block is THIS prompt, copied verbatim. Add the line
     `Overnight: stop` only when the queue and stretch are done or no row can
     move without the owner.
   - Write a log fragment; fold any procedural lesson into the
     coordinator-cycle skill or its recipes, never into the handoff.
   - Run the full unfiltered suite once, in the foreground, from a detached
     worktree with a fixed --basetemp under one dated review-tmp root. Record
     its result, then delete the basetemp and the worktree.
   - Commit.
   - As the very last act, run
     `coordinator_guard.py handback --handoff <the new handoff>`.

Never: push or merge to main; rule an open item or sign an owner-held act;
leave docs/work/pause deleted; read OWNER_SCRATCHPAD.md or the adjudicator's
token file; self-review or adjudicate through a subagent; change ~/.claude
settings or install software; bypass a commit hook.
```
