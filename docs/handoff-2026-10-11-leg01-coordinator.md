# Handoff 2026-10-11 leg 01 (coordinator, overnight): WI-895, WI-887 and WI-901 landed; the queue from WI-858

It replaces [handoff-2026-10-10-leg01-coordinator.md](handoff-2026-10-10-leg01-coordinator.md)
as the resume map. (This leg took the lease at 22:38 local on 2026-10-10 and
ran past midnight; it is the first leg handoff dated 2026-10-11.) Procedure
lives in the `coordinator-cycle` skill and its recipes; this handoff holds
state only. The leg's record is
[log.d/2026-10-11-leg01-coordinator.md](log.d/2026-10-11-leg01-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Landed this leg:** WI-895 (`22f322da`; re-mint WI-904 closed as
  settled), WI-887 (`c10cce0b`; re-mint WI-905 closed as settled) and
  WI-901 (`043ec297`; the sweep minted nothing). Lane tips are archived in
  `archive/lanes` (WI-887's with its pre-rebase tip `01ac7b21`).
- **No lane is out and no judgement is active.** `docs/work/pause` is
  tracked and byte-identical (sha256 `b0a709c8…`; two scoped unpauses this
  leg, each restored in the next commit).
- **Reviewer:** `gpt-6.1-sol` is offered again on the signed-in account
  (probed 22:40 local); every review and critique this leg ran on Sol at
  medium. Terra works.
- **WI-858 is not claimable yet.** Its scope critique (Sol, round 1) found
  two MAJORs: S1, the `coordinator_guard` lock-site check is an
  independently landable deliverable with no recorded order or
  joint-landing decision; S2, durable bookkeeping and release markers give
  files authority over lease holds and retirement, and the spec has no
  `## Trust` (every carrier's producer, write route and failed-write shapes;
  every consumer, locked and lockless readers included; a ruling per
  consumer; the session, lease and call identity the authority binds to).
  Write both before the claim (coordinator-2026-10-11 D-002).
- **WI-902 is not claimable yet.** Its critique (round 1) found one MAJOR,
  S2: the adoption declaration, the disposition verdict and the named
  queued successor become carriers with authority over the close and the
  sweep; the spec owes a `## Trust` covering each (the close, the sweep,
  the verdict reader, the review scheduler and the merge gate as consumers).
- **WI-802** (in `docs/work/draft/`) can now be redrafted to name WI-887's
  two dials (`[reviewer] context_reset_pct` and `final_reviewer`), as
  WI-903's census required, so WI-809 can follow.
- **Watermark** on trunk: SR 239, LLR 326, IF 293, TC 351, WI 905, OI 113.
  Acts run to seq 111.
- **Full suite** at the close-out: see the log fragment.

## The queue

Every queued row, in build order; a row whose `needs` are not yet met waits
for them. Rows needing a scope critique owe it before their claim (minted
adjudication rows excepted, D-020).

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention. Owes its Trust section and S1's landing decision first (D-002) |
| 2 | WI-902 | medium | A disposition can name an already-filed successor (before WI-810). Owes its Trust section first |
| 3 | WI-798 | strong | Account tables and per-account homes for every CLI route (extends WI-887's scoped record key with the account) |
| 4 | WI-851 | strong | Held-rung spine rows are protected by state. Its merge-landing clause is met by a rider on WI-892's walk |
| 5 | WI-850 | medium | A spine row is approved only after the rows it hangs from |
| 6 | WI-799 | strong | Lane-state provider, representation only |
| 7 | WI-832 | medium | A decisions record has an identity no other run can share |
| 8 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool |
| 9 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 10 | WI-878 | medium | A dispute sitting's binding records the findings file it ruled (before WI-801 and WI-811) |
| 11 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 12 | WI-807 | strong | The station authority, lane-side claims and cancellation |
| 13 | WI-833 | medium | An owner's verdict stays bound to the decision text it judged. Merge-landing clause as WI-851's |
| 14 | WI-857 | strong | A verdict records its judging session; an act backed by the authoring session's verdict is refused |
| 15 | WI-816 | medium | Retire the runtime dual paths that need no adopter migration |
| 16 | WI-817 | strong | Retire the SN-028 one-word config window and the non-TOML carriers |
| 17 | WI-808 | strong | One landing per lane on both paths, the tip archived and the record checked |
| 18 | WI-804 | strong | Plan kinds through the entry point, with selection by the drafters |
| 19 | WI-805 | strong | Per-item planning, the replan at the family swap, the build-below-planner dial |
| 20 | WI-814 | strong | Weekly-pace account selection within a family |
| 21 | WI-815 | medium | Grok and FreeLLMAPI groundwork through OpenCode, and an untested Gemini route |
| 22 | WI-809 | strong | The in-lane sitting from LOCK to MERGE_ACTION (needs WI-802: redraft it now that WI-887 has landed) |
| 23 | WI-810 | strong | MINT in the lane (needs WI-809, WI-902) |
| 24 | WI-811 | medium | RESOLVE for disputed findings, and LS9's wording (needs WI-809, WI-878) |
| 25 | WI-812 | strong | The spine-authoring flow (needs WI-809, WI-802, WI-810) |
| 26 | WI-813 | strong | Restore the dual-plan pickup in a claimed lane (needs WI-804, WI-810) |
| 27 | WI-897 | quick | The guard hook costs less per tool call (owner request). **Always the last row**: it builds just before the owner's FileBackup resync test |

Held by the owner, skipped: WI-684 (OI-98), WI-795 (OI-105), WI-871
(OI-112) and WI-893 (OI-113); WI-827 is the owner's signature (SN-029).

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove landed lanes'
  worktrees when convenient: `wi-895`, `wi-887`, `wi-901` (and those the
  previous handoff lists).
- **Rule OI-113** (holds WI-893); OI-98, OI-105 and OI-112 still wait.
- **Decisions to confirm or overrule**, high risk first:
  - `docs/decisions/wi-887.toml`: **D-001** (the gate's final-scope evidence
    is the coordinator-written `# review-scope:` record, never reviewer
    text; SR-239 and LLR-140/LLR-207 state it), then D-002 (two upward size
    re-stamps: agent_loop 2408 to 2427, agent_common 1051 to 1053), D-003,
    D-004 and D-005 (dispute rulings DA, DB and DC, all FIX).
  - `docs/decisions/coordinator-2026-10-11.toml`: **D-001** (WI-887's lane
    re-anchored the LLR snapshot for a traced-only `code_symbol` change, act
    111, taken by the coordinator), D-002 (WI-858 deferred for its Trust;
    WI-901 claimed ahead of it).
  - `docs/decisions/coordinator-2026-10-10.toml`: D-023 (WI-895's Trust
    ruling: the stop never waits on telemetry). D-017 (Luna for Sol, leg
    01) no longer applies going forward; its landed gates stand.
  - `docs/decisions/wi-901.toml`: D-001 (no sitting: LLR-167 and TC-161 are
    incomplete, not false), D-002.
  - Everything the previous handoff lists as still pending.
- **Follow-up topics, unfiled:** the scope critic proposed rubric anchor B3
  a third time (a non-file carrier that authorizes continuing or stopping
  names its ruling when recording fails or is deferred; D-023), beside
  D-019 and D-021; LLR-167's detail and TC-161's method could state
  WI-901's empty-range case.

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
