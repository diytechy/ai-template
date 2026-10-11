# Handoff 2026-10-11 leg 02 (coordinator, overnight): WI-858 landed; WI-902 at its checkpoint rework; Codex limit

Resume-not-before: 2026-10-11T09:41:00-05:00

It replaces [handoff-2026-10-11-leg01-coordinator.md](handoff-2026-10-11-leg01-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The leg's record is
[log.d/2026-10-11-leg02-coordinator.md](log.d/2026-10-11-leg02-coordinator.md).
The leg stopped because Codex (Terra) reported its usage limit, resetting at
9:36 AM local; the loop waits for the line above.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this leg:** WI-858 (`8b7e25e5`; act 112; re-mint WI-907 closed
  as settled). Its lane tip is archived in `archive/lanes`.
- **Filed:** WI-906 (the coordinator lease under store-lock contention,
  split from WI-858's coordinator_guard check; needs WI-858, now met). It
  owes its scope critique and a `## Trust` section before its claim.
- **One lane is out: WI-902** (`C:/Projects/ai-template.wt/wi-902`, branch
  `wi-902`, tip `af4b610c`, clean, rebased onto trunk `fd14c4a5` after
  WI-858 landed; pre-rebase tip `6611b160`, which reviews 001-002
  cite: archive it with the lane). Code is settled: rounds 1-4 built,
  dispute 004 ruled DA FIX and round 4 built it, narrow review 005
  APPROVE. Checkpoint sitting 006 judged seven amendments MEANING (SR-148
  anchored, act 113 in the lane) and RETURNED LLR-335 and TC-360, which
  holds the LLR and TC registries. **Next, in the lane:**
  1. Resume Terra (session `01a12ab4-0ea0-7d51-982d-973e27bd66e1`) on the
     rework prompt saved at
     `C:/Projects/ai-template.wt/review-tmp/2026-10-11-leg02/t902-3.md`
     (it hit the limit before editing anything): sitting 006's
     `## Dispositions` items 1-3, LLR-335 as the adoption decision's one
     home, LLR-153 narrowed to the mint's arms, TC-360's evidence trimmed.
  2. Apply the `Implements:` retags Terra lists (kitlib/adoption.py and the
     adoption functions in intake.py and handback.py to `SR-148, LLR-335`)
     as a recorded coordinator trace edit.
  3. Move verdict 006's `## Dispositions` under another heading (answered
     in the lane), then re-sit LLR-153, TC-147, LLR-335, TC-360, LLR-161,
     LLR-312, TC-156 and TC-254 in one combined sitting (amendment act,
     then first-approval act).
  4. The fresh full-lane Sol gate from `fd14c4a5`'s trunk base, then land
     (rebase first; acts 113+ follow trunk's 112).
  The scratch root `2026-10-11-leg02` is kept for this lane (the arms map,
  spine change list, coverage plans and the rework prompt live there).
- **WI-798 is not claimable yet.** Its scope critique (Sol, round 1) found
  three MAJORs (coordinator-2026-10-11 D-007): S1, no recorded landing order
  or keep-together decision for its account tables, home retirement,
  cooldown keys and adjudicator-authentication move; S2, no `## Trust`
  (route/account selection and the account home carry the adjudicator's
  sign-in); B3 (proposed new rubric anchor), the Windows two-login check and
  the live sign-in migration need owner-provisioned credentials and are not
  separated from the unattended deliverables.
- **No judgement is active.** `docs/work/pause` is tracked and
  byte-identical (sha256 `b0a709c8…`; one scoped unpause this leg, for
  WI-858 and WI-902, restored in the next commit).
- **Reviewer:** every review and critique ran on `gpt-6.1-sol` at medium
  until the limit. The limit came from Terra's resume, after about twenty
  Codex sessions in the leg.
- **Watermark** on trunk: SR 239, LLR 326, IF 293, TC 351, WI 907, OI 113
  (the WI-902 lane holds LLR 335, TC 360). Acts run to seq 112 on trunk.
- **Full suite** at `fd14c4a5` (detached worktree, fixed basetemp, then
  removed): **5811 passed, 22 skipped, 0 failed** in 796 s.

## The queue

Every queued row, in build order; a row whose `needs` are not yet met waits
for them. Rows needing a scope critique owe it before their claim (minted
adjudication rows excepted, D-020).

| # | Row | Tier | What |
|---|---|---|---|
| 0 | WI-902 | medium | **In flight:** the checkpoint rework above, re-sit, gate, land |
| 1 | WI-798 | strong | Account tables and per-account homes. Owes S1 (order), its Trust section and the owner-dependent split (B3) first (D-007) |
| 2 | WI-906 | medium | The coordinator lease under store-lock contention. Owes its scope critique and Trust first |
| 3 | WI-851 | strong | Held-rung spine rows are protected by state. Its merge-landing clause is met by a rider on WI-892's walk |
| 4 | WI-850 | medium | A spine row is approved only after the rows it hangs from |
| 5 | WI-799 | strong | Lane-state provider, representation only |
| 6 | WI-832 | medium | A decisions record has an identity no other run can share |
| 7 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool (moves WI-858's marker rule with the store) |
| 8 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 9 | WI-878 | medium | A dispute sitting's binding records the findings file it ruled (before WI-801 and WI-811) |
| 10 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 11 | WI-807 | strong | The station authority, lane-side claims and cancellation |
| 12 | WI-833 | medium | An owner's verdict stays bound to the decision text it judged. Merge-landing clause as WI-851's |
| 13 | WI-857 | strong | A verdict records its judging session; an act backed by the authoring session's verdict is refused |
| 14 | WI-816 | medium | Retire the runtime dual paths that need no adopter migration |
| 15 | WI-817 | strong | Retire the SN-028 one-word config window and the non-TOML carriers |
| 16 | WI-808 | strong | One landing per lane on both paths, the tip archived and the record checked |
| 17 | WI-804 | strong | Plan kinds through the entry point, with selection by the drafters |
| 18 | WI-805 | strong | Per-item planning, the replan at the family swap, the build-below-planner dial |
| 19 | WI-814 | strong | Weekly-pace account selection within a family |
| 20 | WI-815 | medium | Grok and FreeLLMAPI groundwork through OpenCode, and an untested Gemini route |
| 21 | WI-809 | strong | The in-lane sitting from LOCK to MERGE_ACTION (needs WI-802: redraft it now that WI-887 has landed) |
| 22 | WI-810 | strong | MINT in the lane (needs WI-809, WI-902) |
| 23 | WI-811 | medium | RESOLVE for disputed findings, and LS9's wording (needs WI-809, WI-878) |
| 24 | WI-812 | strong | The spine-authoring flow (needs WI-809, WI-802, WI-810) |
| 25 | WI-813 | strong | Restore the dual-plan pickup in a claimed lane (needs WI-804, WI-810) |
| 26 | WI-897 | quick | The guard hook costs less per tool call (owner request). **Always the last row**: it builds just before the owner's FileBackup resync test |

Held by the owner, skipped: WI-684 (OI-98), WI-795 (OI-105), WI-871
(OI-112) and WI-893 (OI-113); WI-827 is the owner's signature (SN-029).

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the landed lane's
  worktree `wi-858` when convenient (and those earlier handoffs list).
- **Rule OI-113** (holds WI-893); OI-98, OI-105 and OI-112 still wait.
- **Decisions to confirm or overrule**, high risk first:
  - `docs/decisions/coordinator-2026-10-11.toml`: **D-004** (WI-858's Trust
    ruling: one per-publisher store marker, publish-then-apply, clock-first
    locked reads, folded lockless reads), **D-005** (WI-902's Trust ruling:
    the one-key adoption block, the disposed row read from the title, never
    from the adjudicator), then D-003 (WI-906 split from WI-858), D-006
    (WI-902 claimed on an answered round-3 MINOR), D-007 (WI-798 deferred).
  - `docs/decisions/wi-858.toml`: **D-002** (the replay fix binds consumption
    to the per-call lease, not a consumed set), D-001 (smoke membership
    ceiling 2495 to 2600).
  - In the open WI-902 lane, `docs/decisions/wi-902.toml` (it reaches
    trunk with the landing): **D-001** (the sweep's open-state check runs on
    the landing sweep, lineage only on replay), D-002 (intake.py size stamp
    1719 to 1823 over four rounds), D-003 (the drafts-only replay gap fixed
    with the adoption one), D-004 (dispute 004's ruling).
  - Everything the previous handoff lists as still pending.
- **Follow-up topics, unfiled:** the scope critic proposed rubric anchor B3
  again, now as "owner-dependent completion is separated from unattended
  deliverables" (WI-798), beside the earlier B3 wording (D-023 of
  2026-10-10); intake.py is 1823 SLOC and grows each lane that touches the
  sweep: a decomposition row may be owed.

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
