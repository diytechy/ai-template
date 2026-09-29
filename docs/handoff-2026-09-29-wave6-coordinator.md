# Handoff 2026-09-29 (wave 6, coordinator) — the new roles run end to end; the spine's drafts fall from 12 to 2

For the next session's **coordinator**: an Opus session that coordinates Codex
Sol builders, Sonnet reviewers and independent Opus adjudicators and arbiters,
and lands work on trunk.

This replaces
[handoff-2026-09-28-wave5-coordinator.md](handoff-2026-09-28-wave5-coordinator.md)
as the resume map. That handoff's roles, hand-integration recipe and traps
still hold, with the corrections below folded in. This session's record:

- the log fragment [log.d/2026-09-28-wave6-coordinator.md](log.d/2026-09-28-wave6-coordinator.md):
  every landing, its review rounds and its bar;
- [reviews/2026-09-28-wave6/](reviews/2026-09-28-wave6/): every Sonnet
  review, and [ARBITRATION.md](reviews/2026-09-28-wave6/ARBITRATION.md)
  (one ruling);
- the owner's rulings:
  - [log.d/2026-09-28-owner-rulings-oi95-oi96.md](log.d/2026-09-28-owner-rulings-oi95-oi96.md)
    and [log.d/2026-09-28-owner-ruling-oi97.md](log.d/2026-09-28-owner-ruling-oi97.md);
  - the OI-96 direction of 2026-09-29, in the row's `decision` cell.

## What happened

**The open count is 11 at the start and 11 at the end** (10 queued, 1
deferred). Twenty-two rows were minted and twenty-three closed; most mints
were the bookkeeping the loop generates (see "The backlog" below).

- **Owner rulings:** OI-95 (a), OI-96 (a), and OI-97 (a) with its directions.
- **Lanes landed** (Sol build, Sonnet review, coordinator squash):
  - WI-720, WI-721, WI-723, WI-727, WI-545;
  - WI-729, WI-732 and WI-736, which answered the adjudicators' returns;
  - WI-740.
- **Spine-acts batches G to K:** five sittings, each an independent Opus
  adjudicator taking one act, seq 9 to 13, each cross-reviewed by Sonnet and
  found SOUND.
  - The spine's Drafted rows went from 12 to 2.
  - Every carry-over has cleared. The chain that went round four times
    (SR-222, SR-227, TC-264) is anchored.
- **Spot checks** (WI-725, WI-735, WI-738, WI-743): three CONFIRMED. WI-743
  found a real defect, which batch K found independently too.
- **WI-739** was cancelled, because WI-545 moved only traced cells.
- **Full unfiltered suite:**
  - WI-721's run was green, 4816 passed in 1:23:18.
  - A second run on WI-545's lane found one red, since fixed.
  - The phase-close run on a4919610 gave `1 failed, 4839 passed, 15
    skipped in 0:44:43`. The one failure is a test fixture coupled to the
    live spine: no LLR is Drafted any more. It is filed as WI-745.
  - The critical path fell from a 1160 s router test (WI-727's fix) to under
    3 minutes.

Nothing is pushed. Trunk is `refactor_again`. Every lane tip is reachable
through `archive/lanes`.

## Your first jobs, in order

1. **WI-745** first, so the full suite is green again: a quick Sol build.
   The re-seed test in `test_baseline_snapshot` must plant its own Drafted
   LLR instead of relying on a live one.
2. **WI-744** (the keep-warmer start failure): a quick Sol build.
   - `KeepWarmer.__init__` builds every routing row's argv. On Windows a
     `{prompt}` row behind a `.cmd` shim raises, and the dispatcher stops
     before its first poll when the keep-warm dial is on.
   - The row is an exact adjudicator draft: leave a refused row out, and add
     one cross-platform test.
3. **WI-722** (the diagram shrink floor): held mid-lane.
   - The first build (`build/wi-722` at d451cb64, worktree
     `C:/Projects/ai-template.wt/wi-722`) was NOT YET SOUND. The sub-label
     token (8.5 px) sits below the 9 px floor, so every diagram became
     fixed-width.
   - The owner's direction is in OI-96 and in the row: raise the type scale
     to 12 px labels and 10.5 px sub-labels, keep a 9 px floor, and assert
     that the floor never exceeds the natural width.
   - Send a fix round to the same lane.
4. **WI-713** (TC-055's re-judge) after WI-722. Codex wrote the rendering,
   so the judge must be non-Codex (a Claude session), reading
   native-resolution tiles.
5. **The owner's items below**, several of which gate the rest of the queue.

## The backlog, and what the owner asked about it

The owner saw the queue "still growing" and asked whether more consolidation
is possible, and whether the re-judge rows will lead to new rubrics.

**Why the queue keeps minting.** Every lane that changes the spine mints an
adjudication at its merge. A sampled spot check mints on some closes. Every
adjudication that returns rows mints a follow-up lane, whose merge mints
another adjudication. That chain is the intended mechanism, and it did clear
this session. But each pass is two to three rows.

This session:
- **Minted:** 22 rows.
- **Adjudication and spot-check bookkeeping:** 13 of them.
- **Closed:** 23.

The open count is flat. What remains is mostly gated on the owner or on a
person.

**What is open, by kind:**

| Kind | Rows |
|---|---|
| Buildable now | WI-745, WI-744, WI-722 |
| Follows WI-722 | WI-713 |
| Gated on the owner | WI-541 (live model runs), WI-657 (the rung question), WI-667 (re-arming the red-TC rung; WI-697 waits on it) |
| Gated on a person's act | WI-684 (TC-036: a person's re-sync of a stamped adoption), WI-688 (TC-211: needs the SR-161 perspective-record producer built) |
| Deferred, last | WI-625 (the id-prefix rename) |

**The re-judges do not create rubrics.** WI-684, WI-688, WI-697 and WI-713
re-judge observation test cases whose declared inputs changed. Three of them
(TC-036, TC-211, TC-279) are Inspections that follow existing procedures in
`docs/test/inspection-procedures.md`. Only TC-055 is a Critique, and it
scores against the existing `docs/rubrics/dashboard-usability.md`. A re-judge
re-scores against what exists. It is re-minted whenever an input's hash
changes, never to author a rubric.

**Consolidation the next coordinator can offer the owner** (each is the
owner's call, and none was done this session):

- **Park the rows that wait on a person or on the owner as `deferred`,** with
  the gate named, instead of leaving them `queued`. That covers WI-684,
  WI-688, WI-541, WI-657, WI-667 and WI-697. They then stop reading as
  backlog, and only buildable work stays queued.
- **Fold WI-697 into WI-667.** WI-697 is TC-279's re-judge, which WI-667's
  first Done-when already makes possible.
- **Lower the spot-check sample** (`[attestation] complete_review`).
  - Of four spot checks, three confirmed. The fourth found a real defect,
    which the adjudicator found anyway.
  - A lower rate would cut about one row per lane.
  - Keep some sampling. WI-725's and WI-735's observations improved the
    next adjudication.
- **Batch adjudication minting per wave rather than per merge.** That is a
  kit change to `intake.py sweep`, and belongs in the S11 plan.

## For the owner

- **The backlog questions above:** park the gated rows, fold WI-697, and
  choose the spot-check rate.
- **The temporary `Bash(codex exec *)` allow rule** in
  `.claude/settings.local.json` stays until the queue drains. Remove it then.
- **Sandbox leftovers:** folders under `C:\Projects\ai-template.wt\`
  (`wi-721`, `wi-723`, `wi-727`, `wi-545`, and others to come), holding
  sandbox-owned `.tmp` and `.pytest_cache` content. The coordinator's process
  cannot delete them; delete them from an elevated shell.
- **Unchanged from wave 5:**
  - the live codex and opencode fixture recordings (WI-541, WI-606's last
    lines);
  - the four need re-attestations (SN-003, SN-008, SN-009, SN-025);
  - SN-005's `process` tag for SR-224;
  - WI-657's rung question;
  - the pause (`docs/work/pause`);
  - S11 for the loop;
  - the four non-lane branches;
  - merge-to-main and push.
- **Kit gaps recorded, not filed:**
  - SR-195 against SR-212's Boundary arm, for a future
    `form = "interface"` SR at a crossing with no stakeholder (wave-6
    arbitration 1);
  - the session-adapter interface row omits `mint`, `resume`, `one_turn` and
    `bounds_one_turn` (batch K's observation);
  - WI-735's observation 4: SR-177's acceptance ends "the row's stated build
    gap", which whoever builds the aggregation must amend.

## Corrections to the role and the recipe (learned this wave)

- **Sol builders cannot commit.** Codex's `workspace-write` sandbox keeps
  `.git` read-only. Tell each builder to leave its change uncommitted and
  report "Commit SHA: none (left for the coordinator)". The coordinator
  commits it on the lane branch with the builder's co-author line, and the
  review covers that exact commit. Do not widen the sandbox.
- **Sandbox pytest temp directories.** Tell builders to put `--basetemp`
  under the system temp directory, and to set
  `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`. Otherwise scaffold
  tests inherit the parent repository and hang or fail.
- **A pure-move refactor needs the full suite before it lands.** WI-545's
  split kept behaviour but silently broke three kinds of consumer that
  address code by where it used to live:
  - ratchet keys;
  - path-keyed content scans that then read re-export stubs, checking
    nothing;
  - rebinding a moved symbol through its old module.

  Two review rounds caught the first two kinds. Only the full unfiltered
  suite caught the third. Run it on the lane composed onto trunk (a
  throwaway worktree plus a temp commit) before landing any move.
- **Carry held approvals into the next adjudication yourself.** When an
  act's snapshot is refused because one returned row drifts, the approved
  rows stay unflipped. The next merge's brief does not include them. Add
  them to the minted row's `adjudicates` list with a Context note, and
  check that the composer renders them.
- **Take a lane's snapshot again when trunk moved a registry since the lane
  was cut.** Batch J's copy of `test-cases.toml` predated WI-545's
  traced-cell moves, so it was not byte-identical.
  1. Check read-only that `refresh_refusal` accepts the same arguments on
     the merged tree.
  2. Reset `docs/archive/last_approved/` to trunk.
  3. Re-run the adjudicator's exact snapshot command.
  4. Say so in the log.
- **Answering returns without churn.** Two sittings in a row stalled on one
  rewritten approved cell that said more than its row. So a builder
  answering returns does the registry-blocking rows first and takes no
  optional rewrite of an approved cell. An adjudicator's draft should be
  replace-this-with-that, with prohibitions (batch I's was, and it landed
  in one round).
- **Spot checks have no composed brief** (the composer refuses rows without
  a `brief`). Brief the Opus spot-checker directly on the WI-719 and WI-725
  pattern. When a spot check finishes while an adjudication of the same
  rows is sitting, send its record to that adjudicator as chain evidence
  (SendMessage). That worked twice.
- **An adjudication with nothing in scope is cancelled,** not held, when
  the composer says so (WI-739).
- **Bash here-strings.** A long Python heredoc containing apostrophes can
  make Git Bash reject the whole command, running nothing. Write longer
  record-writing scripts to the scratchpad with the file tool, and run
  them.
- **Smoke seconds.** Every over-budget reading this session was
  contention, with builders, reviewers or the full suite running beside it.
  Every quiet reading was within budget (48 to 55 s). Keep taking a control
  reading before calling a breach.
- **The Sonnet alias** resolves to Sonnet 5 here, not 5.5.
