# Handoff 2026-10-11 leg 03 (coordinator, overnight): WI-798 at its checkpoint rework; WI-902 left committed

It replaces [handoff-2026-10-11-leg02-coordinator.md](handoff-2026-10-11-leg02-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The leg's record is
[log.d/2026-10-11-leg03-coordinator.md](log.d/2026-10-11-leg03-coordinator.md).
The leg closed out at the 40% occupancy mark.

## State (trunk `refactor_again`, nothing pushed)

- **Filed on trunk:** WI-908 (the owner-assisted two-login Claude isolation
  check), held by the pending open item OI-114. WI-798's spec gained its
  Deliverables-and-order, Trust and Owner-dependent-completion sections.
- **Lane 1, WI-798** (`C:/Projects/ai-template.wt/wi-798`, branch `wi-798`,
  tip `9437d0a1`, clean; trunk base `67bf3bf2`). Code is settled: rounds 1-4
  built units (b), (a) and (c); full review 001 and narrow 002 answered;
  narrow 003 APPROVE. Sitting 004 (`docs/reviews/wi-798/004-ADJUDICATE-028ecf8.md`)
  judged ten amendments MEANING but returned LLR-268, LLR-270, LLR-305 and
  TC-324 (text the account design made untrue), and returned all seven first
  approvals (LLR-336, TC-361..TC-366: the declared-account credential
  boundary, each parent link earned, every account test cited). No act was
  taken. **Next, in the lane:**
  1. Resume Terra (session `01a12c25-e6ba-7da0-b1ad-72b38ee4741e`) on both
     `## Dispositions` drafts of verdict 004, answered in the lane (S11).
  2. Move both `## Dispositions` headings under another heading, then re-sit
     every returned row plus any row the rework changes (amendment act, then
     first-approval act); also re-sit LLR-044, LLR-072, LLR-266, LLR-267,
     LLR-306 and TC-321 if their registry was held.
  3. The fresh full-lane Sol gate from trunk's tip, then land (rebase first;
     acts follow trunk's 112; the id watermark keeps LLR 336 and TC 366).
     Regenerate `docs/interface-reference.md` and the CLI reference at the
     landing. The smoke budget read 47.0 s against the parent's 42.7 s under
     load once: re-measure quiet before landing.
  Scratch root `C:/Projects/ai-template.wt/review-tmp/2026-10-11-leg03` is
  kept for this lane (arms map, spine change list, plans).
- **Lane 2, WI-902** (`C:/Projects/ai-template.wt/wi-902`, branch `wi-902`,
  tip `d3d30121`, clean; rebased on trunk `ccd66391`; pre-rebase tips
  `c1ab6585` and `6611b160`, which earlier verdicts cite: archive them with
  the lane). **Left committed under the two-round breaker**
  (coordinator-2026-10-11 D-015, lane D-010): after dispute ruling 011, full
  gates 014 (IF-294, built) and 015 were not SOUND. Review 015's MAJOR is
  accepted and unbuilt: `parse_disposition_section` harvests only complete
  TOML fences, so a valid block followed by an unclosed adoption block loses
  the second successor silently. Rows are approved through act 117 in the
  lane. Resuming is a build round (one complete-section parser refusing
  unmatched fences, close and sweep regressions), a narrow review and a fresh
  full-lane gate; whether to resume is the owner's call or the next leg's
  instruction. WI-810 needs WI-902.
- **No judgement is active.** `docs/work/pause` is tracked and byte-identical
  (sha256 `b0a709c8…`; one scoped unpause this leg, for WI-798).
- **Reviewer:** every review and critique ran on `gpt-6.1-sol` at medium; no
  Codex limit was reached.
- **Watermark** on trunk: SR 239, LLR 326, IF 293, TC 351, WI 908, OI 114.
  Lanes hold more: wi-902 LLR 335, TC 360, IF 294; wi-798 LLR 336, TC 366.
  Acts run to seq 112 on trunk (wi-902's lane holds 113-117).
- **Full suite** at `67bf3bf2` (detached worktree, fixed basetemp, then
  removed): **5811 passed, 22 skipped, 0 failed** in 933 s.

## The queue

Every queued row, in build order; a row whose `needs` are not yet met waits
for them. Rows needing a scope critique owe it before their claim (minted
adjudication rows excepted, D-020).

| # | Row | Tier | What |
|---|---|---|---|
| 0 | WI-798 | strong | **In flight:** Terra's rework of sitting 004's returns, re-sit, full-lane gate, land |
| 1 | WI-906 | medium | The coordinator lease under store-lock contention. Owes its scope critique and Trust first |
| 2 | WI-851 | strong | Held-rung spine rows are protected by state. Its merge-landing clause is met by a rider on WI-892's walk |
| 3 | WI-850 | medium | A spine row is approved only after the rows it hangs from |
| 4 | WI-799 | strong | Lane-state provider, representation only |
| 5 | WI-832 | medium | A decisions record has an identity no other run can share |
| 6 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool (moves WI-858's marker rule with the store) |
| 7 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 8 | WI-878 | medium | A dispute sitting's binding records the findings file it ruled (before WI-801 and WI-811) |
| 9 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 10 | WI-807 | strong | The station authority, lane-side claims and cancellation |
| 11 | WI-833 | medium | An owner's verdict stays bound to the decision text it judged. Merge-landing clause as WI-851's |
| 12 | WI-857 | strong | A verdict records its judging session; an act backed by the authoring session's verdict is refused |
| 13 | WI-816 | medium | Retire the runtime dual paths that need no adopter migration |
| 14 | WI-817 | strong | Retire the SN-028 one-word config window and the non-TOML carriers |
| 15 | WI-808 | strong | One landing per lane on both paths, the tip archived and the record checked |
| 16 | WI-804 | strong | Plan kinds through the entry point, with selection by the drafters |
| 17 | WI-805 | strong | Per-item planning, the replan at the family swap, the build-below-planner dial |
| 18 | WI-814 | strong | Weekly-pace account selection within a family (needs WI-798) |
| 19 | WI-815 | medium | Grok and FreeLLMAPI groundwork through OpenCode, and an untested Gemini route |
| 20 | WI-809 | strong | The in-lane sitting from LOCK to MERGE_ACTION (needs WI-802: redraft it now that WI-887 has landed) |
| 21 | WI-810 | strong | MINT in the lane (needs WI-809, WI-902) |
| 22 | WI-811 | medium | RESOLVE for disputed findings, and LS9's wording (needs WI-809, WI-878) |
| 23 | WI-812 | strong | The spine-authoring flow (needs WI-809, WI-802, WI-810) |
| 24 | WI-813 | strong | Restore the dual-plan pickup in a claimed lane (needs WI-804, WI-810) |
| 25 | WI-897 | quick | The guard hook costs less per tool call (owner request). **Always the last row**: it builds just before the owner's FileBackup resync test |

Held by the owner, skipped: WI-684 (OI-98), WI-795 (OI-105), WI-871
(OI-112), WI-893 (OI-113) and WI-908 (OI-114); WI-827 is the owner's
signature (SN-029); WI-902 is left committed (above).

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the landed lane's
  worktree `wi-858` when convenient (and those earlier handoffs list).
- **WI-902:** decide whether the next leg resumes the lane (one build round
  for review 015's MAJOR, then a narrow review and a fresh full-lane gate),
  or leave it for an attended session.
- **Rule OI-113** (holds WI-893) and **OI-114** (holds WI-908; recommendation
  (b), defer); OI-98, OI-105 and OI-112 still wait.
- **Decisions to confirm or overrule**, high risk first:
  - `docs/decisions/coordinator-2026-10-11.toml`: **D-009** (WI-798's Trust
    ruling), **D-010** (the token binds to one declared account; unqualified
    retained launches run on the ambient login), then D-008 (one row, two
    commits), D-011 (an unverified login account is printed, not refused),
    D-012, D-013, D-014 (WI-908 and OI-114 split out), D-015 (WI-902 left
    committed), D-016; and the earlier D-003..D-007 the previous handoff
    lists.
  - In the open WI-798 lane, `docs/decisions/wi-798.toml` (it reaches trunk
    with the landing): **D-001** (the shipped default route is the qualified
    `ANTHROPIC-OPUS-STRONG@ADJUDICATOR`; adopters declare the account or pass
    `--route`), D-002..D-009 (D-008 and D-009: the withheld credential lists
    per CLI, from the design and the Gemini and Claude sources).
  - In the open WI-902 lane, `docs/decisions/wi-902.toml`: D-001..D-010
    (D-006: dispute 009 superseded D-001's residual clause).
- **Follow-up topics, unfiled:** the scope rubric's proposed anchor B3
  ("owner-dependent completion is separated from unattended deliverables"),
  proposed three times now (WI-798 rounds 1-2; D-023 of 2026-10-10);
  shallow-boundary and lossy-decode sites outside WI-902's surface
  (`baseline_snapshot._shallow_commits` duplicating `retire.shallow_boundary`,
  `adjudicate_brief` and `rejudge._added_at`'s `--diff-filter=A` reads, about
  twenty `git_out` content reads); `spine_carrier.rows_from_toml` raises on a
  non-table `agent = 5` in agents.toml; a non-string route cell is silently
  stringified; `session_service._name_key` duplicates
  `agent_route.env_name_key`; Codex workload identity names no environment
  variable to withhold; intake.py is 1854 SLOC in the WI-902 lane (a
  decomposition row may be owed).

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
