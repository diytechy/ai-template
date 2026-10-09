# Handoff 2026-10-09 (coordinator): WI-852 and WI-869 landed; no lane is open

It replaces [handoff-2026-10-08c-coordinator.md](handoff-2026-10-08c-coordinator.md)
as the resume map. The wave-18, wave-17 and wave-11 handoffs still carry the
in-lane cycle, the roles and the "never" list until WI-848 (the
`coordinator-cycle` skill) lands. This session's record is
[log.d/2026-10-09-coordinator.md](log.d/2026-10-09-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Landed:**

  | Row | Squash | What it does |
  |---|---|---|
  | WI-852 | `f7e492bf` (acts 71-74) | The coordinator renders its review and critique briefs from the kit's templates (`review_brief.py`) |
  | WI-869 | `82f2866d` (act 75) | The smoke tier is back under its 60 s budget: three git-backed modules re-tiered, `max-tests` 2395 |

  The re-mints WI-872 and WI-873 are closed as settled. `archive/lanes` is at
  `ce0206d9`.
- **WI-852's last steps:**
  - The dispute ruling's patch was applied. Its seam was settled as (b): the
    rollup directory's one declaration moved into `kitlib.verdict` (D-006).
  - Terra amended LLR-313 and TC-333, and sitting 007 blessed both.
  - The fourth full-lane Sol review found that a branch named `Rollup` filed a
    review that the rollup generator then pruned, because Windows compares
    paths case-insensitively. The same class was already ruled FIX, so it was
    fixed in the lane, casefolded on every platform (D-007).
  - The fifth review, `90c2f740`, was SOUND.
  - The landing missed R-F (a closed row keeps no SpecRef) because the hook
    runs `check_trajectory` without `--strict`. It was cleared in `50570fab`.
- **WI-869:** measured before it was fixed
  ([log.d/2026-10-09-wi-869-smoke-tier-measurement.md](log.d/2026-10-09-wi-869-smoke-tier-measurement.md)).
  - The cause was membership, not the workstation.
  - After the re-tier, trunk's bar reads 2300 passed in 33.6 s; enforce read
    40.9 s.
  - The first full-lane review asked for the measurement in the log. The
    second, `931a6260`, was SOUND.
- **Filed:** WI-874, from WI-869's measurement. `session_keep.primary_out_dir`
  spawns git on every store access.
- **Acts** run to seq 75. `docs/work/pause` is tracked and unchanged: one
  scoped unpause (`b58714c9`) claimed WI-869, and `295687c7` restored the
  pause byte-identical.
- **Full suite:** see the log fragment (run at this handoff's commit).

## Next

1. **WI-870,** the merge gate reads a VERDICT line strictly. WI-852's filing
   boundary is now strict (one whole-grammar check). WI-870 brings the gate's
   `score_reviews.parse_verdict` and `kitlib.sitting`'s shared reader to the
   same bar.
2. Then WI-853 (the findings gate), WI-848 (the coordinator-cycle skill) and
   WI-834 (blackout).
3. WI-874 (the store-root spawn) is small and independent. It would make the
   heaviest remaining in-process smoke modules cheap.

Claim each batch under ONE scoped unpause.

## Corrections learned this session

- **Run `check_trajectory.py --strict` before committing a landing.** The
  pre-commit hook runs the non-strict form, so R-F (a closed row's SpecRef)
  slipped through WI-852's squash. A closed spec takes `specref = ""` and a
  `## Deliverable` section; the hook does refuse a missing Deliverable (R-A).
- **The integrator refuses to claim an id named in status.md's prose.**
  Reword the line by its subject, in its own trunk commit, before the claim.
- **A sweep's re-mint takes the next WI id.** File hand rows after the sweep,
  or cite them by subject until filed.
- **Archive commits carry the empty tree**
  (`4b825dc642cb6eb9a060e54bf8d69288fbee4904`). The parents are the previous
  `archive/lanes`, the lane tip and the pre-rebase tip.
- **A lane cut at a claim lacks the restored pause.** Move the commit-less
  branch to trunk's tip before adding its worktree.
- **The workstation is 12 cores / 24 threads.** CLAUDE.md's "4-core / 8-thread
  box" line describes another machine.

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the archived worktrees
  `wi-852` and `wi-869` (and the earlier list) when convenient.
- **Decisions to confirm or overrule, high risk first:**
  - `wi-869.toml` D-001: the three modules re-tiered. `test_decision_overrule`
    and `test_ruling_sync` stayed in smoke to keep `migrate_decisions`'s pin
    and three TCs true.
  - `coordinator-2026-10-08d.toml` D-001: WI-852 landed over the smoke budget,
    before WI-869 fixed it.
  - `wi-852.toml`:
    - D-006: seam (b). The rollup directory moved into `kitlib.verdict`; no
      new IF row.
    - D-007: the `Rollup` case-fold fix taken in-lane without a second dispute.
    - D-003 and D-005, still unseen from the last session.
  - `wi-869.toml` D-002 (TC-334 stays Smoke) and D-003 (the spawn finding
    filed as WI-874).
  - `coordinator-2026-10-08d.toml` D-002: the status.md rewording and the
    lane-branch move.
  - `wi-866.toml` D-002, still unseen.
- **CLAUDE.md's smoke-tier line** still cites the 2026-09-27 figures and a
  "4-core / 8-thread box". The current figures are in `docs/stack.ini` and the
  WI-869 log fragment. CLAUDE.md is byte-capped, so the wording is your call.
- **Rule** OI-112, OI-98 and OI-105, still pending.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Take the coordinator lease FIRST
(`coordinator_guard.py take`), before reading anything long. Read, in order:
CLAUDE.md; docs/status.md; docs/handoff-2026-10-09-coordinator.md (state, next
rows, corrections, decisions for the owner); the wave-18, wave-17 and wave-11
handoffs for the in-lane cycle, the roles and the "never" list; your memory
index.

No lane is open. Scope: WI-870 (the merge gate reads a VERDICT line
strictly), then WI-853, WI-848 and WI-834 as context allows; WI-874 (the
store-root spawn) may run beside one of them. Claim each batch under ONE
scoped unpause (a reviewed deletion commit, the claims, a byte-identical
restore). Roles: Terra (medium) authors spine text, UTF-8 only, re-reading
every cell it splices; an independent adjudicator judges it through
coordinator_adjudicate.py (set AGENT_CLAUDE_TOKEN_FILE to the token file's
path first; never read the file), never a subagent; Claude Opus builds
(kit-builder, medium); Codex 6.1 Sol (medium) reviews, narrow rounds while a
lane iterates and one fresh full-lane review as the last gate. Apply the
review threat model (PROCESS.md §6) to every finding: dismiss one that needs a
compromised or contrived host in one recorded line, never with code; send a
contested or third-round finding to the `dispute` sitting. Run
check_trajectory.py --strict before committing a landing.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; ask the owner to confirm or overrule, never to approve. Push
and merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md or the
adjudicator's token file.

At the end (or at 50% context): update docs/status.md (forward-only), write the
next handoff linking this one and a log fragment, run the full unfiltered suite
once from a detached worktree with a fixed --basetemp under one dated
review-tmp root and delete it once recorded, then hand the lease back with
`coordinator_guard.py handback --handoff <the new handoff>` as the last act.
```
