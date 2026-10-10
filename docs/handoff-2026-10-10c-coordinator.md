# Handoff 2026-10-10c (coordinator, attended): WI-882 landed; WI-881 at its last sitting; WI-884 built

It replaces [handoff-2026-10-10b-coordinator.md](handoff-2026-10-10b-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill; this
handoff holds state only. This session's record is
[log.d/2026-10-10c-coordinator.md](log.d/2026-10-10c-coordinator.md).

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

## The queue (rows 1 to 3 in flight)

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-881 | medium | IN FLIGHT: spine settled; fresh full-lane gate, land |
| 2 | WI-884 | strong | IN FLIGHT: spine intent, narrow review, checkpoint, gate, land |
| 3 | WI-831 | adjudication | CLAIMED: re-judge TC-055 |
| 4 | WI-894 | adjudication | Dispose of WI-828's partial close (successor WI-893 and OI-113 already filed) |
| 5 | WI-892 | quick | The lane-commit walk and text-then-act move to their own module, shared, unchanged |
| 6 | WI-887 | strong | REVIEW retention; the configurable persisted final reviewer (needs WI-884) |
| 7 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention (needs WI-887) |
| 8 | WI-895 | quick | A keep-warm ping's tree-end failure stops the run (needs WI-881) |
| 9 | WI-798 | strong | Account tables and per-account homes for every CLI route |
| 10 | WI-851 | strong | Held-rung spine rows are protected by state (needs WI-892) |
| 11 | WI-850 | medium | A spine row is approved only after the rows it hangs from (needs WI-892) |
| 12 | WI-799 | strong | Lane-state provider, representation only |
| 13 | WI-832 | medium | A decisions record has an identity no other run can share |
| 14 | WI-800 | strong | One session store with durable invocations, the usage ledger and the spool |
| 15 | WI-856 | medium | A queue-with-edge verdict edges a waiter with no needs line |
| 16 | WI-801 | strong | One labelled entry point for model calls, with the per-kind routing table |
| 17 | WI-807 | strong | The station authority, lane-side claims and cancellation |
| 18 | WI-878 | medium | A dispute sitting's binding records the findings file it ruled |

Stretch: WI-857, WI-808, WI-802 and WI-804. Rows held by the owner are
skipped: WI-684 (OI-98), WI-795 (OI-105), WI-871 (OI-112) and WI-893
(OI-113). Rows from 4 down owe their scope critique before their claim.
WI-894 is an adjudication row, so it needs a claim like any row.

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

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Take the coordinator lease FIRST
(`coordinator_guard.py take --transcript <your transcript>`), before reading
anything long. Read, in order: CLAUDE.md; docs/status.md; the newest handoff
(the one status.md's RESUME HERE names): its State, its queue and its "For
the owner"; the coordinator-cycle skill and its recipes; your memory index.

Scope: WI-881 first: its spine is settled (sitting 010); move sitting
009's answered follow-up out of Dispositions, then run the fresh full-lane gate, re-measure the smoke budget quiet, rebase and
land. Then WI-884: Terra's intent pass over SR-154's chain (from the
builder's change list the handoff names), a narrow Sol
review of round 1, the checkpoint, the gate, land. Then WI-831 (claimed),
then the queue in order, each row's scope critique before its claim,
claiming each batch under ONE scoped unpause. Roles: Claude Opus builds
(kit-builder, medium); GPT Terra (medium) authors spine text in one retained
session per lane; Codex 6.1 Sol (medium) reviews, with narrow rounds while a
lane iterates and one fresh full-lane review as the last gate; an
independent adjudicator judges spine text and disputes through
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
