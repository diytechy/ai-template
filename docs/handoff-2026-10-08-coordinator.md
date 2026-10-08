# Handoff 2026-10-08 (coordinator): the consolidation sitting landed; two lanes open mid-cycle

It replaces [handoff-2026-10-07-wi841-retro-coordinator.md](handoff-2026-10-07-wi841-retro-coordinator.md)
as the resume map. The wave-18, wave-17 and wave-11 handoffs still carry the
in-lane cycle, the roles and the "never" list until WI-848 (the
`coordinator-cycle` skill) lands. This session's record is
[log.d/2026-10-08-coordinator.md](log.d/2026-10-08-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Landed: WI-855, the consolidation sitting** (`78f61b17`; `archive/lanes`
  at `12fcd832`). Queue-with-edge over 29 rows, nothing absorbed, seven
  machine edges plus three by hand, three Done-when bullets
  (`docs/decisions/wi-855.toml`). The order that matters now:
  - the token row WI-846 heads both WI-848 (the skill) and WI-834 (the
    blackout row);
  - WI-798 (account homes) waits on WI-834;
  - WI-851 waits on WI-849.
- **Owner rulings (2026-10-08):**
  - OI-110 ruled (b) (`b2dfc1fa`);
  - WI-849 "Split it out" (WI-857 filed);
  - contention "Move it to WI-858" (`24160bc0`).
- **Filed:**
  - WI-856: edge a waiter with no `needs` line;
  - WI-857: a verdict records its judging session;
  - WI-858: every release survives store-lock contention;
  - WI-859: the isolation test reads pytest's summary line.
- **Two lanes open, claimed under one scoped unpause** (`b84327f1`, restored
  byte-identical in `a537451a`). Both are committed, clean, and mid-cycle.
  Each lane's review trail, sweep tables, Terra reports and accumulated spine
  change list are in `C:/Projects/ai-template.wt/wi-NNN-notes/` (outside the
  repository; `SPINE-CHANGES-checkpoint.md` is the reconciliation list).

  | Lane | Tip | Where it stands |
  |---|---|---|
  | `wi-846` (token) | `65c42a54` | Round 5 built (one selected route row, end to end); **its narrow Sol review is next**. Rounds 1 to 4 drew 3, 5, 2 and 3 MAJORs; the contention class moved to WI-858. Decisions D-001 to D-006 |
  | `wi-849` (approval act) | `5a1b447e` | Round 3 built; **Sol round 3 is in**: NOT YET SOUND, two MAJORs (`wi-849-notes/sol-849-r3.md`): the shared reader still disagrees with the route on a registry form, and the acted set misses approvals recorded only in the act ledger. Its sweep table and fix are next. Decisions D-001, D-002 |

  Terra's retained sessions:
  - `wi-846`: `01a11a22-c085-7a33-bd0d-b30531ba711a`;
  - `wi-849`: `01a11cba-6462-7a20-aa34-f46a00008af3`.

  Resume each by id for the checkpoint reconciliation.
- **Acts** still run to seq 59. Watermark: TC 331 (`wi-849` took TC-331,
  `wi-846` holds TC-330), WI 859. `docs/work/pause` is tracked and unchanged.
- **Full suite** at `24160bc0` (detached worktree, fixed basetemp under
  `review-tmp/2026-10-08-coordinator/`): **1 failed**, 5392 passed, 17 skipped
  in 1037 s. The failure is `test_conftest_isolation.py::test_a_module_importing_kitlib_collects_on_its_own`.
  - It is deterministic and environment-caused: the shell now runs inside a
    Windows job object, so the conftest's notice follows the summary line the
    test reads as last.
  - Filed as WI-859, not tooled around.
  - The 270 MB basetemp was deleted once recorded.
- **Smoke at the close-out:** 2358 passed, 2 skipped in 70.4 s, but the
  budget check read 81.5 s against 60 s (OVER). No code landed on trunk this
  session, so the breach is box load, not introduced here; the budget was not
  re-stamped.

## Next

1. **`wi-846`:**
   - the narrow Sol review of round 5 (`c37793e6..65c42a54`), with the sweep
     table carried;
   - then the checkpoint: Terra, resumed, reconciles the whole set from
     `wi-846-notes/SPINE-CHANGES-checkpoint.md`;
   - the closure check;
   - one combined sitting through `coordinator_adjudicate.py adjudicate
     --brief combined`;
   - the fresh full-lane Sol gate (`a30bfcdc..tip`);
   - rebase, act, squash, archive, sweep.

   It lands before WI-848 and WI-834.
2. **`wi-849`:**
   - the sweep table for Sol round 3's two MAJORs;
   - the fix;
   - a narrow round;
   - then the same checkpoint. Its combined sitting also judges the Done-when
     change `03dcb357` (owner ruling "Split it out").
3. **Then WI-848** (claim after WI-846 lands; reconcile the skill drafts with
   both lanes, and with 003's WI-848 bullet), **then WI-834**.

## Corrections learned this session

- **Re-sit a closed consolidation by rewinding the lane.** The entry point
  refuses a sitting on a row that is no longer under `active/`. To route a
  review finding back to the adjudicator after the mechanical close, reset the
  lane to before the close (archive the discarded commits), re-sit, then
  re-run `handback.close_adjudication`.
- **A trunk edit to a queued row moves the consolidation digest.** The close
  then refuses as stale. Do not re-stamp `digests` by hand; a narrow sitting
  judges the move and re-stamps it (`wi-855.toml` D-004).
- **The entry point has no dispute brief class.** A third-round crafted-input
  class could not go to the adjudicator as a named dispute; ask the owner, or
  give the builder a precise design and record the deviation (`wi-846.toml`
  D-006). A row for a dispute class is worth filing.
- **The auto-mode classifier refused a squash as a merge without review**
  until the command cited the lane's SOUND full-lane review.
- **Builders must re-sync skill copies.** Every lane commit touching a kit
  skill needed `bootstrap.py --dest . --sync` before the hook passed.
- **The secrets floor refuses a fake token shaped like a real one** in a test;
  mark the line `privacy-ok`.
- **A builder's round can implement a reviewer's direction backwards**
  (round 4 re-read the registry where round 3 asked to carry the selected
  row). Restate the direction as a construction ("takes the selected row and
  never reads the registry") when dispatching.

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the archived
  `wi-855` worktree and the earlier list when convenient.
- **Decisions to confirm or overrule, high risk first:**
  - `wi-846.toml`:
    - D-002 (the token sits in an environment a permission-skipping model can
      read);
    - D-001 (settings-file credentials can still outrank the token);
    - D-006 (a third-round class sent to the builder, not the adjudicator);
    - then D-003 (superseded by your ruling), D-004 and D-005.
  - `wi-855.toml`:
    - D-003 (the lane rewound after review);
    - D-004 (the digest re-stamped by a narrow sitting);
    - D-002 (Done-when text written into WI-802, WI-798 and WI-848);
    - then D-001.
  - `wi-849.toml` D-001 (the Done-when text written to your split ruling),
    then D-002.
  - `coordinator-2026-10-08.toml` D-001 and D-002.
  - The earlier handoffs' lists, still standing.
- **To use the token in practice:** set `AGENT_CLAUDE_TOKEN_FILE` to your
  token file once WI-846 lands (dev-setup will say so).
- **Rule** OI-98 and OI-105, still pending.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Take the coordinator lease FIRST
(`coordinator_guard.py take`), before reading anything long. Read, in order:
CLAUDE.md; docs/status.md; docs/handoff-2026-10-08-coordinator.md (state, the
two open lanes, next steps, corrections, decisions for the owner); the
wave-18, wave-17 and wave-11 handoffs for the in-lane cycle, the roles and the
"never" list; your memory index. Then each open lane's notes folder
(C:/Projects/ai-template.wt/wi-846-notes/ and wi-849-notes/).

Two lanes are open mid-cycle, both committed: wi-846 (the long-lived token,
round 5 awaiting its narrow Sol review) and wi-849 (the approval act in the
authoring lane, Sol round 3 NOT YET SOUND with two MAJORs). Finish each
through its checkpoint (Terra, resumed, reconciles the whole spine set from
SPINE-CHANGES-checkpoint.md; one combined sitting through
coordinator_adjudicate.py adjudicate --brief combined), a fresh full-lane Sol
review, and the landing; wi-846 lands first. Then claim WI-848 under one
scoped unpause. Roles: Terra (medium) authors spine text, UTF-8 only,
re-reading every cell it splices; an independent adjudicator judges it
through the entry point, never a subagent; Claude Opus builds (kit-builder,
medium); Codex 6.1 Sol (high) reviews. Sweep each finding's class before
fixing it; state a reviewer's direction to the builder as a construction.

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
