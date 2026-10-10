# Handoff 2026-10-10 (coordinator, attended): four rows landed; WI-880 waits on three spine returns

It replaces [handoff-2026-10-09c-coordinator.md](handoff-2026-10-09c-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill; this
handoff holds state only. This session's record is
[log.d/2026-10-10-coordinator.md](log.d/2026-10-10-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Landed:**
  - **WI-859** as `c36cbc8c`: the conftest isolation test reads pytest's
    summary line. Gate 001, no sitting.
  - **WI-854** as `2b9817a2`: the briefs compose the tier questions from one
    home. Sitting 001 (act seq 91), gate 002. Re-mint WI-883 closed as settled.
  - **WI-847** as `d0a4b623`: step 1 only, the loop's narrow render, landed
    unwired (D-011). Sitting 001 (act seq 92), gate 002. Re-mint WI-885 closed
    as settled.
  - **WI-874** as `dbc949cb`: the store lookup runs once per root. Gate 001,
    no sitting. The quiet re-measure is in
    [log.d/2026-10-10-wi-874-store-lookup-measurement.md](log.d/2026-10-10-wi-874-store-lookup-measurement.md).
    The smoke tier fell to 35 s.
- **Filed:**
  - WI-881: a deadline kill waits on `taskkill`, which takes about 50 s on
    this workstation. That is why the idle-deadline test fails; it is not
    load-sensitive (D-007).
  - WI-882: the prompt catalogue does not cover the composed questions home
    (from WI-854's sitting).
  - WI-884: WI-847's step 2, split by the owner (D-008). It covers reviewer
    retention and the gate binding, with a configurable final reviewer. WI-858
    now needs it.
  - WI-886: the goalposts row for WI-847's narrowed Done-when. It stays open
    for its own `done-when` sitting.
- **In flight: WI-880** (`C:/Projects/ai-template.wt/wi-880`, tip
  `f151958f`, clean, rebased on `dbc949cb`). Both build rounds and Terra's
  intent set are committed. Combined sitting
  `docs/reviews/wi-880/001-ADJUDICATE-9a39f47.md` blessed SR-019, SR-020,
  SR-046, LLR-021 and TC-021. It took no act: the snapshot copy is refused
  while unblessed rows drift. It returned three findings, drafted under the
  verdict's `### Dispositions`:
  1. SR-032's new clause binds the shipped dev-setup templates to behaviour
     only this repository's `scripts/dev-setup.ps1` has. Scope it, or make the
     templates do it. LLR-326 and TC-350 (both Drafted) follow it.
  2. TC-345 asserts three obligations about this repository's settings that
     no row states. LLR-322 needs the text.
  3. On Windows, a `[run]` line's bare `python3` is not the menu
     interpreter. Make it exact (code, the builder) or narrow LLR-047's claim
     (text). This is the coordinator's call.

  Terra's session for this lane is `01a1249c-839b-7af2-816f-dc341eefb76f`.
  The lane's change list, arms map, Terra prompt and output, and the sitting's
  brief are kept in `C:/Projects/ai-template.wt/review-tmp/wi-880-carry/`.
  Delete that directory once the lane lands.
  The lane's ids run to LLR-326 and TC-350. Decision record:
  `docs/decisions/wi-880.toml` (D-001: the widening to `commit-msg` and
  `pre-push`). At landing, this workstation opts in with
  `<3.11+ python> project-trajectory/scripts/coordinator_guard.py --root . hooks --example .claude/settings.json.example --enable`
  in the same landing: the lane empties the committed `.claude/settings.json`.
- **Watermark:** SR 237, LLR 322, IF 293, TC 345, WI 886 on trunk; acts run
  to seq 92.
- `docs/work/pause` is tracked and unchanged: this session's one scoped
  unpause was restored byte-identical (`0503fef9`).
- **Full suite** at `dbc949cb`: **1 failed, 5646 passed, 21 skipped** in 790 s. The one failure is `test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child`, which is WI-881 (taskkill latency), not load.

## The queue (row 1 in flight)

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-880 | medium | IN FLIGHT: answer sitting 001's three returns, re-sit, gate, land |
| 2 | WI-881 | medium | A deadline kill returns at once, not after taskkill's latency (the full suite's one red) |
| 3 | WI-886 | adjudication | WI-847's narrowed Done-when, judged |
| 4 | WI-884 | strong | Reviewer retention and the gate binding, with a configurable final reviewer |
| 5 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention (needs WI-884) |
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
| 18 | WI-882 | quick | The prompt catalogue covers composed prompt text, or records that it excludes it |

Stretch: WI-857, WI-808, WI-802 and WI-804. Rows held by the owner are
skipped: WI-684 (OI-98), WI-795 (OI-105) and WI-871 (OI-112). Each queued row
not yet critiqued owes its Sol scope critique before its claim; WI-881,
WI-882, WI-884 and WI-886 have none yet.

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the worktrees
  `wi-834`, `wi-854`, `wi-859`, `wi-847` and `wi-874` when convenient.
- **Decisions to confirm or overrule** (`docs/decisions/coordinator-2026-10-10.toml`),
  high risk first:
  - D-003: WI-847's Trust ruling, carried into WI-884. The gate accepts only
    a fresh, full-lane verdict, and a doubtful store record mints fresh.
  - D-006: WI-859 closed with its full-suite clause read as met. Its own
    test passes; the suite's one red is WI-881.
  - D-010: WI-884 does not wait on WI-800, so the contention fix in WI-858
    is not held behind the store replacement.
  - D-001: WI-854's stopped-leg spine edits were kept, not redone.
  - D-002 and D-005: the landing orders the scope critiques asked for.
  - D-007: the idle-deadline test is not load-sensitive (it is WI-881).
  - D-009: the smoke membership ceiling went from 2395 to 2495; the seconds
    budget is unchanged.
  - D-011: WI-847's step 1 landed unwired, with WI-884 to wire it.
    Overrule toward folding it into WI-884 if you prefer no function ahead
    of its caller.
  - D-004 and D-008 are your own rulings, recorded.
- **In WI-880's lane:** `docs/decisions/wi-880.toml` D-001 (the widening to
  every git hook). It lands with the lane.
- **Still awaiting you:** everything the
  [2026-10-09c handoff](handoff-2026-10-09c-coordinator.md) listed
  (`wi-834.toml` D-001 to D-027, the leg records, `wi-848.toml`,
  `wi-853.toml`, `wi-870.toml`, `wi-875.toml`), and OI-98, OI-105 and OI-112.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Take the coordinator lease FIRST
(`coordinator_guard.py take --transcript <your transcript>`), before reading
anything long. Read, in order: CLAUDE.md; docs/status.md; the newest handoff
(the one status.md's RESUME HERE names): its State, its queue and its "For
the owner"; the coordinator-cycle skill and its recipes; your memory index.

Scope: WI-880 first. Answer its sitting 001's three returns (Terra, resumed
in its retained session, for the spine text; the builder only if you make
bare python3 exact on Windows rather than narrowing LLR-047), re-sit the
returned and blessed rows in one combined sitting, run its fresh full-lane
gate, and land it with the guard-hook opt-in on this workstation in the same
landing. Then the handoff's queue in order, each row's scope critique before
its claim, claiming each batch under ONE scoped unpause (a reviewed deletion
commit, the claims, a byte-identical restore). Roles: Claude Opus builds
(kit-builder, medium); GPT Terra (medium) authors spine text in one retained
session per lane; Codex 6.1 Sol (medium) reviews, narrow rounds while a lane
iterates and one fresh full-lane review as the last gate; an independent
adjudicator judges spine text and disputes through coordinator_adjudicate.py
(set AGENT_CLAUDE_TOKEN_FILE to the token file's path first; never read the
file), never a subagent. Apply the review threat model (PROCESS.md section 6)
to every finding; send a contested or recurring-class finding to the dispute
sitting, whose ruling is final. Run the smoke tier and its budget yourself
before each landing commit (the hook does not), and check_trajectory.py
--strict.

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
