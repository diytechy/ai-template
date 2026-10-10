# Handoff 2026-10-10d (coordinator, overnight launch): the 10c state, a consolidation pass, and the headless-leg prompt

It replaces [handoff-2026-10-10c-coordinator.md](handoff-2026-10-10c-coordinator.md)
as the resume map. Nothing landed between them. This handoff carries 10c's
State forward unchanged, revises the queue after a consolidation pass over
the frontier (decision D-016 in `docs/decisions/coordinator-2026-10-10.toml`),
and replaces the attended session prompt with the headless-leg prompt that
`C:/Projects/ai-template.wt/coordinator-tools/overnight_legs.py` runs. Each
leg writes the next handoff. Procedure lives in the `coordinator-cycle`
skill; this handoff holds state only.

## State (trunk `refactor_again`, nothing pushed)

- **Landed:** WI-882 as `ad91c7b4` (re-mint WI-891 closed as settled).
  WI-828 closed partial as `e925bebb` (decision D-015).
- **Filed:** OI-113 (owner), WI-892, WI-893, WI-894 (minted: the
  disposition of WI-828's partial close) and WI-895.
- **In flight: WI-881** (`C:/Projects/ai-template.wt/wi-881`, base
  `24a3ff4f`). SR-238 is approved and LLR-026 and TC-026 are blessed (acts
  99 to 101). Gate 006's defects were fixed in rounds 4 and 5 (narrow
  reviews 007 and 008).
  - The rows were re-amended at checkpoint 2.
  - Sitting 009 returned them once, because the launch-window residual
    stood only in SR-238's Rationale. Terra's answer is `d90ac640`.
  - Sitting 010 blessed all three rows (act 102, `a955d787`; lane tip
    `136813e9`). Sitting 009's answered follow-up still sits under
    `### Dispositions`: move it under `### Answered in the lane`, as was
    done for sittings 001 and 004.
  - Then the fresh full-lane gate (`review_brief.py review --scope full
    --base 24a3ff4f`), a quiet smoke-budget reading, the rebase, and land.
  - Terra session `01a126a6-d22a-7dc0-8c34-59d2bcbf2424`. Decisions D-001
    to D-007 are in `docs/decisions/wi-881.toml`.
- **In flight: WI-884** (`C:/Projects/ai-template.wt/wi-884`, base
  `24a3ff4f`). Build round 1 is committed (`075ea4c0`). Its 10 builder
  decisions are recorded in `docs/decisions/wi-884.toml`; the high-risk
  ones are the deleted legacy window and the strict brief, both downstream
  migrations.
  - Next: Terra's intent pass over SR-154's chain, from the builder's
    change list, kept outside the repository at
    `C:/Projects/ai-template.wt/wi-884-spine-changes.md`: SR-154 acceptance,
    LLR-045, LLR-140, LLR-207, LLR-262, IF-175, TC-082, TC-205, and a flag
    on SR-156.
  - Then a narrow Sol review of round 1, the checkpoint, the gate, and land.
- **Claimed, not started: WI-831** (`C:/Projects/ai-template.wt/wi-831`),
  the TC-055 dashboard re-judge (recipes §8). Its Trust section is ruled
  and it declares no Done-when (a minted re-judge row).
- **Watermark** on trunk: SR 238, LLR 326, IF 293, TC 350, WI 895, OI 113.
  Acts run to seq 98 on trunk and 102 in WI-881's lane.
- `docs/work/pause` is tracked and unchanged: this session's scoped unpause
  was restored byte-identical (`f8e22961`).
- **Full suite** at `a1d05b50` (detached worktree): **1 failed, 5669
  passed, 22 skipped** in 868 s. The failure is
  `test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child`,
  the `taskkill` latency WI-881 removes in its lane (also recorded at the last
  handoff). Not yet run with WI-881 merged.
- **`check_docs --strict-orphans`** reports the gitignored
  `docs/test/report.md` as an orphan in a working checkout (since before
  WI-880). It is local, not a regression, and the recipes now say so; a
  clean checkout does not have the file.

## The queue (rows 1, 2 and 4 in flight or claimed)

The consolidation pass (D-016) found no two rows that are one work item, and
one packing change: WI-823 lands before WI-831's re-judge. Its spec requires
the re-judge to run on the corrected rubric, and the rubric is a declared
input of TC-055, so the other order costs a second render-and-judge cycle.
The census itself cannot mint while a judgement is active or a lane is out,
so the formal pass is row 5, at the first idle station.

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-881 | medium | IN FLIGHT: spine settled; fresh full-lane gate, land |
| 2 | WI-884 | strong | IN FLIGHT: spine intent, narrow review, checkpoint, gate, land |
| 3 | WI-823 | medium | TC-055's rubric binds T2 and T5 to their test rows; the shot matrix covers every tab (before WI-831) |
| 4 | WI-831 | adjudication | CLAIMED: re-judge TC-055, on WI-823's corrected rubric |
| 5 | census | adjudication | Consolidation census at the first idle station (no lane out): mint, claim, sit, land; then follow its outcome's edges and absorptions for every row below |
| 6 | WI-894 | adjudication | Dispose of WI-828's partial close. Its successor WI-893 and OI-113 are already filed by hand; the brief says so, so the sitting does not draft a second successor |
| 7 | WI-892 | quick | The lane-commit walk and text-then-act move to their own module, shared, unchanged |
| 8 | WI-887 | strong | REVIEW retention; the configurable persisted final reviewer (needs WI-884) |
| 9 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention (needs WI-887) |
| 10 | WI-895 | quick | A keep-warm ping's tree-end failure stops the run (needs WI-881) |
| 11 | WI-798 | strong | Account tables and per-account homes for every CLI route |
| 12 | WI-851 | strong | Held-rung spine rows are protected by state (needs WI-892) |
| 13 | WI-850 | medium | A spine row is approved only after the rows it hangs from (needs WI-892) |
| 14 | WI-799 | strong | Lane-state provider, representation only |
| 15 | WI-832 | medium | A decisions record has an identity no other run can share |
| 16 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool |
| 17 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 18 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 19 | WI-807 | strong | The station authority, lane-side claims and cancellation |
| 20 | WI-878 | medium | A dispute sitting's binding records the findings file it ruled |

Stretch: WI-833, WI-857, WI-808, WI-802 and WI-804. Rows held by the owner are
skipped: WI-684 (OI-98), WI-795 (OI-105), WI-871 (OI-112) and WI-893
(OI-113); WI-827 is the owner's signature. Rows from 3 down owe their scope
critique before their claim. Adjudication rows need a claim like any row.

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the worktrees
  `wi-882` and `wi-828` (and the earlier `wi-880`, `wi-886`, `wi-888`,
  `wi-834`, `wi-854`, `wi-859`, `wi-847`, `wi-874`) when convenient. The
  parked WI-828 diff and change list are at
  `C:/Projects/ai-template.wt/wi-828-round1-parked.patch` and
  `wi-828-spine-changes-parked.md`; WI-884's change list is beside them.
- **Rule OI-113** (open-items.html): how a hand merge's walk tells its
  commits from trunk's history. The recommendation is (a), declare the trunk.
  It holds WI-893.
- **Decisions to confirm or overrule**, high risk first:
  - `docs/decisions/coordinator-2026-10-10.toml`: D-015 (WI-828 closed
    partial; its walk re-homed to WI-892) and D-014 (critiques closed at
    round 3). D-001 to D-013 still await you.
  - `docs/decisions/wi-881.toml` (in the lane; it lands with it): D-002 and
    D-004 (the bounded claim; an unopenable member raises), then D-001 and
    D-003 and D-005 to D-007.
  - `docs/decisions/wi-884.toml` (in the lane): D-001 to D-003 (downstream
    migrations), then D-004 to D-010.
  - `docs/decisions/wi-882.toml` (landed): D-001, option (a).
- **Still awaiting you:** everything the earlier handoffs listed, and OI-98,
  OI-105, OI-112 and OI-113.
- **New this handoff:** coordinator D-016 (the consolidation pass and the
  WI-823-before-WI-831 order), low risk.

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
