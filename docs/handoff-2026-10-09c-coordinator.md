# Handoff 2026-10-09c (coordinator, attended): WI-834 landed; the leg-03 lanes wait

It replaces [handoff-2026-10-09-leg02-coordinator.md](handoff-2026-10-09-leg02-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill; this
handoff holds state only. This session's record is
[log.d/2026-10-09c-coordinator.md](log.d/2026-10-09c-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Landed: WI-834** (the blackout row) as `fb1990aa`, after six fresh
  full-lane gates. The last gate's one MINOR was dismissed by dispute 040.
  Its in-lane acts run to seq 90. The re-mint WI-879 is closed as settled
  (`102486f7`): the registries equal their approved snapshots.
  `archive/lanes` is at `9a7d7ddd`.
- **Filed: WI-880** (P4), under the owner's ruling D-019: the kit entry
  points that still run kit Python on a bare `python`. These are this repo's
  committed `.claude/settings.json` hooks, the `docs/stack.ini` `[run]`
  lines, the shipped pre-commit hook, and `scripts/dev-setup.ps1 -Install`.
- **Two lanes from the stopped overnight leg 03.** The owner stopped that
  leg at 15:20 and released its lease ("lanes WI-834/854/859 left as-is").
  This session left both lanes untouched:
  - **WI-854** (`C:/Projects/ai-template.wt/wi-854`): the tip is
    `522d1d00`, and the low-level and test registries are uncommitted. Those
    edits are the stopped leg's spine work in progress. Read them before
    resuming, and decide whether to keep or redo them.
  - **WI-859** (`C:/Projects/ai-template.wt/wi-859`): the tip is
    `2e4dd305`, clean. Its build commit has had no review yet.
  - Both were claimed at `ed2533cb`. Rebase each onto trunk before its next
    review: trunk has moved by WI-834's landing.
- **Watermark:** SR 237, LLR 322, IF 293, TC 345, WI 880. Acts run to
  seq 90.
- `docs/work/pause` is tracked and unchanged.
- **Full suite** at `102486f7`: **1 failed, 5626 passed, 21 skipped** in 803 s. The failure, `test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child`, asserts a `wall < 40` s kill. It also fails 3 of 3 on the pre-landing base `ed2533cb` under this evening's machine load, and passed in leg 02's quiet full suite. It is a load-sensitive timing test that predates WI-834; the next session re-runs it on a quiet box.

## The queue (lanes 1-2 in flight)

| # | Row | Tier | What |
|---|---|---|---|
| 1 | WI-854 | medium | IN FLIGHT (leg 03): the adjudication briefs carry spine-authoring's tier questions |
| 2 | WI-859 | quick | IN FLIGHT (leg 03): the conftest isolation test reads pytest's summary line |
| 3 | WI-847 | medium | The loop's reviewer resumes within a lane; the merge-gating review stays fresh |
| 4 | WI-858 | strong | Lease release and bookkeeping survive store-lock contention |
| 5 | WI-874 | medium | The runtime store's primary checkout is resolved once per operation |
| 6 | WI-880 | medium | Every kit entry point runs kit Python on a floor-resolved interpreter |
| 7 | WI-831 | adjudication | Re-judge TC-055 |
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

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the worktree `wi-834`
  when convenient.
- **Decisions to confirm or overrule** (`docs/decisions/wi-834.toml`, which
  landed with the lane), high risk first:
  - D-027: the lane landed on gate 039, whose only finding dispute 040
    dismissed, with no seventh gate (WI-848's precedent);
  - D-025: round 028's `time -p` finding was answered under dispute 025's
    ruled line, with no fresh sitting;
  - D-021, D-022 and D-023: the builder's construction choices: the
    machine-local opt-in, command-level ownership, and the
    `kitlib/guard_hooks.py` split at the 1000-SLOC ratchet;
  - D-017, D-018, D-020, D-024 and D-026: the interpreter resolution, the
    resumption past D-016's bound, and the three dispute rulings recorded;
  - D-016 and D-001 to D-015, carried from the overnight legs;
  - D-019 is your own ruling, recorded.
- **Coverage lines the disputes drew**, final unless you widen them:
  - The hook supervises the word the shell's grammar makes the command.
    Wrapper commands (`Start-Process`, `iex`, `cmd /c`, `sh -c`, `exec`,
    `command`, `nohup`, `xargs`, scripts) are outside it (sitting 025).
  - A further grammar-only form no ordinary agent writes is dismissed
    (sitting 031).
  - A PowerShell function definition naming a model CLI is over-denied
    inside the window, accepted as failing closed (sitting 040).
- **Still awaiting you:** the leg-01, leg-02 and leg-03 coordinator decision
  records, `wi-848.toml`, `wi-853.toml`, `wi-870.toml` and `wi-875.toml` (see
  the leg-02 handoff), and OI-98, OI-105 and OI-112.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Take the coordinator lease FIRST
(`coordinator_guard.py take --transcript <your transcript>`), before reading
anything long. Read, in order: CLAUDE.md; docs/status.md; the newest handoff
(the one status.md's RESUME HERE names): its State, its queue and its "For
the owner"; the coordinator-cycle skill and its recipes; your memory index.

Scope: the two leg-03 lanes first (WI-854: read its uncommitted spine edits
before resuming; WI-859: rebase, then its review), then the handoff's queue
in order. Claim each batch under ONE scoped unpause (a reviewed deletion
commit, the claims, a byte-identical restore). Roles: Claude Opus builds
(kit-builder, medium); GPT Terra (medium) authors spine text in one retained
session per lane; Codex 6.1 Sol (medium) reviews, narrow rounds while a lane
iterates and one fresh full-lane review as the last gate; an independent
adjudicator judges spine text and disputes through coordinator_adjudicate.py
(set AGENT_CLAUDE_TOKEN_FILE to the token file's path first; never read the
file), never a subagent. Apply the review threat model (PROCESS.md section 6)
to every finding; send a contested or recurring-class finding to the dispute
sitting, whose ruling is final. Run check_trajectory.py --strict before
committing a landing.

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
