# Handoff 2026-10-10b (coordinator, attended): three rows landed; WI-881 and WI-882 in flight

It replaces [handoff-2026-10-10-coordinator.md](handoff-2026-10-10-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill; this
handoff holds state only. This session's record is
[log.d/2026-10-10b-coordinator.md](log.d/2026-10-10b-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Landed:** WI-880 as `945245e2`, WI-886 as `caafdb0e` and WI-888 as
  `c31a23cd`. The re-mints WI-889 and WI-890 were closed as settled.
- **Filed:** WI-887 (split from WI-884, D-012) and WI-888 (landed).
- **In flight: WI-881** (`C:/Projects/ai-template.wt/wi-881`, tip `a6cbaea8`,
  clean, base `b29650f6`). The build (a Windows job object in place of
  `taskkill`, D-001 in `docs/decisions/wi-881.toml`) and Terra's intent set
  are committed. Combined sitting
  `docs/reviews/wi-881/001-ADJUDICATE-291f389.md` blessed LLR-026 and TC-026
  (MEANING, not yet re-attested) and returned SR-238 (new, Drafted). Its
  `### Dispositions` holds two returns:
  1. A POSIX descendant that leaves the session's process group survives the
     kill. Either bound SR-238 and LLR-026 to the group or job and record
     the residual, or strengthen the mechanism. This is the coordinator's
     call.
  2. TC-026 has no real-process interruption test, no test that an
     uncontainable Windows child errors before it runs, and no single bound
     for "before the coordinator continues". Either wait until the job's
     active-process count is zero, or state a bound, and test that bound.
  Return 1's choice and return 2 need the builder (code and tests), then
  Terra in session `01a126a6-d22a-7dc0-8c34-59d2bcbf2424`, then a re-sitting
  of SR-238, LLR-026 and TC-026, then the fresh full-lane gate. The lane's
  ids: SR-238 (lane floor SR-238..239, LLR-330..332, TC-355..358).
- **In flight: WI-882** (`C:/Projects/ai-template.wt/wi-882`, base
  `dc071296`). The build is committed (`bc70379e`, option (a): the
  catalogue digests `spine-questions.md`), and so is Terra's intent set
  (`03427a1c`, session `01a126bc-5bc6-7853-ac9d-776e589d0e8a`; arms map
  `C:/Projects/ai-template.wt/review-tmp/2026-10-10b-coord/arms-882.md`).
  Next: rebase onto trunk (RESYNC: keep both entries, trunk's first), then
  sit LLR-162, LLR-164 and TC-192's amendments (IF rows carry no status),
  then the fresh
  full-lane gate. No narrow round was needed. Its floor is LLR-333..335,
  TC-359..362 and IF-297..299. Record the option choice in `docs/decisions/wi-882.toml`
  before its sitting (the builder's reason is in the build commit).
- **Watermark** on trunk: SR 237, LLR 326, IF 293, TC 350, WI 890. Acts run
  to seq 97.
- `docs/work/pause` is tracked and unchanged: this session's scoped unpause
  was restored byte-identical (`8d75bc6c`).
- **This workstation's guard hooks** are machine-local now (WI-880): on.
- **Full suite** at `19176f09`: **2 failed, 5662 passed, 22 skipped** in
  1351 s, beside a concurrent smoke run.
  `test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child`
  is WI-881 (in flight). The `[root]` case of
  `test_run_devsetup.py::test_at_a_windows_console_the_missing_runtime_is_offered_consent_first`
  failed with "the child never wrote its ready marker", then passed alone
  twice (both cases). It is load-sensitive; file it as a row if it recurs.

## The queue (rows 1 and 2 in flight)

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-881 | medium | IN FLIGHT: answer SR-238's two returns, re-sit, gate, land |
| 2 | WI-882 | quick | IN FLIGHT: spine intent, sitting, gate, land |
| 3 | WI-884 | strong | The loop schedules narrow rounds; the gate binds a fresh full-lane final review |
| 4 | WI-887 | strong | REVIEW retention in a lane; the configurable persisted final reviewer (needs WI-884) |
| 5 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention (needs WI-887) |
| 6 | WI-831 | adjudication | Re-judge TC-055 |
| 7 | WI-828 | medium | A hand merge on trunk judges the commits it brings in |
| 8 | WI-798 | strong | Account tables and per-account homes for every CLI route |
| 9 | WI-851 | strong | Held-rung spine rows are protected by state |
| 10 | WI-850 | medium | A spine row is approved only after the rows it hangs from |
| 11 | WI-799 | strong | Lane-state provider, representation only |
| 12 | WI-832 | medium | A decisions record has an identity no other run can share |
| 13 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool |
| 14 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 15 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 16 | WI-807 | strong | The station authority, lane-side claims and cancellation |
| 17 | WI-878 | medium | A dispute sitting's binding records the findings file it ruled |

Stretch: WI-857, WI-808, WI-802 and WI-804. Rows held by the owner are
skipped: WI-684 (OI-98), WI-795 (OI-105) and WI-871 (OI-112). WI-884 and
WI-887 have their scope critiques recorded (D-012, D-013); each row from 5
down still owes its critique before its claim.

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the worktrees
  `wi-880`, `wi-886` and `wi-888` (and the earlier `wi-834`, `wi-854`,
  `wi-859`, `wi-847`, `wi-874`) when convenient.
- **Decisions to confirm or overrule**, high risk first:
  - `docs/decisions/wi-880.toml` (landed): D-003, the narrowed `python3`
    claim (a Windows-run line declares `python`), and D-001, the widening
    to every git hook. Also D-002 (SR-032 scoped to this repository's own
    setup) and D-004 (the gate triage, with no test pinning the
    working-directory exception).
  - `docs/decisions/coordinator-2026-10-10.toml`: D-012 (WI-884 split; WI-887
    filed; WI-858 now needs WI-887) and D-013 (critiques closed at round 3).
    D-001 to D-011 from the earlier session still await you.
  - `docs/decisions/wi-881.toml` D-001 (in the lane; it lands with it): the
    job object, resumed through the undocumented `NtResumeProcess`.
- **The dashboard size budget** was restamped from 3,480,000 to 4,000,000
  bytes in WI-888's landing. The reason is in the test file.
- **Still awaiting you:** everything the earlier handoffs listed, and OI-98,
  OI-105 and OI-112.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Take the coordinator lease FIRST
(`coordinator_guard.py take --transcript <your transcript>`), before reading
anything long. Read, in order: CLAUDE.md; docs/status.md; the newest handoff
(the one status.md's RESUME HERE names): its State, its queue and its "For
the owner"; the coordinator-cycle skill and its recipes; your memory index.

Scope: WI-881 first. Decide its sitting 001's first return (bound SR-238 and
LLR-026 to the process group and job and record the POSIX residual, or
strengthen the mechanism) and record the call. Send the builder the code
and tests for both returns (a real-process interruption test, the
uncontainable-child refusal test, one stated bound), then Terra (retained
session) for the text. Re-sit SR-238, LLR-026 and TC-026 together, run the
fresh full-lane gate, and land. Then WI-882: finish its spine intent, sit,
gate, land. Then the queue in order, each row's scope critique before its
claim, claiming each batch under ONE scoped unpause. Roles: Claude Opus
builds (kit-builder, medium); GPT Terra (medium) authors spine text in one
retained session per lane; Codex 6.1 Sol (medium) reviews, with narrow
rounds while a lane iterates and one fresh full-lane review as the last
gate; an independent adjudicator judges spine text and disputes through
coordinator_adjudicate.py (set AGENT_CLAUDE_TOKEN_FILE to the token file's
path first; never read the file), never a subagent. Apply the review threat
model (PROCESS.md section 6) to every finding; send a contested or
recurring-class finding to the dispute sitting, whose ruling is final. Run
the smoke tier and its budget yourself before each landing commit, read its
summary for failures, and run check_trajectory.py --strict.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; ask the owner to confirm or overrule, never to approve. Push
and merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md or the
adjudicator's token file.

At the end (or at 45% context): update docs/status.md (forward-only), write the
next handoff linking this one and a log fragment, run the full unfiltered suite
once from a detached worktree with a fixed --basetemp under one dated
review-tmp root and delete it once recorded, then hand the lease back with
`coordinator_guard.py handback --handoff <the new handoff>` as the last act.
```
