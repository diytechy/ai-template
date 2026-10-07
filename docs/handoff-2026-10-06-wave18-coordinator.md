# Handoff 2026-10-06/07 (wave 18, coordinator): all five rows landed; no lane is open

It replaces [handoff-2026-10-06-wave17-coordinator.md](handoff-2026-10-06-wave17-coordinator.md)
as the resume map. The wave-11 handoff's roles and "never" list still hold. This
session's record is
[log.d/2026-10-06-wave18-coordinator.md](log.d/2026-10-06-wave18-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Claimed under one scoped unpause** (`465cceab`, restored byte-identical in
  `d69e04f3`): WI-841, WI-838, WI-839, WI-840 and WI-842. WI-842 was filed at
  the session start from the owner's question about the stranded lease.
- **Landed, all five:**

  | Row | Squash | What it does |
  |---|---|---|
  | WI-839 | `2648d1dd` | The docs state the module-size ratchet's lane-carried re-stamp |
  | WI-842 | `f9265d99` (act 41) | A closing coordinator hands its lease back (`coordinator_guard.py handback`) |
  | WI-838 | `0ccebafb` (acts 42-43) | A route's first retained mint takes the lease |
  | WI-840 | `76b1d212` | Passing tests' temp dirs are removed; one dated scratch root per session |
  | WI-841 | `68e0ee87` (acts 44-59) | An in-lane Done-when change is blessed in the lane; verdict trust centralized |

  WI-841 was finished past the 50% context guard at the owner's direction
  (coordinator D-010). It took six narrow Sol rounds, then eleven fresh
  full-lane gates; the last, `2874ff0a`, was SOUND. Each gate found real
  cross-round defects, so it ended with:
  - one verdict parser, reading strictly per physical line;
  - an acceptance outcome the route records;
  - one accepted-verdict reader for every consumer;
  - row-tied act authority;
  - one carrier resolver;
  - one dispatch-point hold.

  The re-mints WI-843, WI-844 and WI-845 are closed citing their acts.
  `archive/lanes` is at `9b506465`.
- **Filed:**
  - **WI-846 (P9):** the adjudicator's dedicated home authenticates with the
    owner's long-lived token, and an auth failure retires nothing. The owner
    ran `claude setup-token`; the coordinator holds the file's PATH in local
    memory only and never reads the file.
  - **WI-847 (P5):** the loop's reviewer resumes within a lane, and the
    merge-gating review stays fresh and full-lane.
- **Acts** run to seq 59. Watermark: SR 232, LLR 310, IF 287, TC 329, WI 847.
  `docs/work/pause` is tracked and unchanged.
- **Full suite:** at `76b1d212`, 5291 passed, 17 skipped, 0 failed, in 711 s.
  At the final trunk tip: 5397 passed, 13 skipped, 0 failed, in 674.5 s at `1f610bb7` (detached worktree, fixed basetemp; 274 MB left, deleted once recorded).

## Next (owner's scope to choose)

1. **WI-834, the blackout row,** under one scoped unpause. Its adjudications
   use the combined sitting WI-841 added.
2. **WI-846, the long-lived token,** shares WI-834's sign-in step. Build it
   first or beside it. Until it lands, the dedicated home's OAuth refresh fails
   at each expiry and needs the owner's `/login`.

## Corrections learned this session

- **Review rule (owner, 2026-10-07):** narrow round-delta reviews while a lane
  iterates. The last review before landing is a FRESH, FULL-LANE Codex Sol
  review from the lane's trunk base to its tip.
- **Treat crafted-input findings as possible design holes.** A gate finding
  that a consumer trusts input on its own should be fixed as a class (one
  parser, one reader, a recorded outcome), not instance by instance. Ask the
  builder for the class fix at the first such finding.
- **Brief Terra to re-read every whole cell it splices, and to write UTF-8
  only.** It wrote cp1252 dashes and verbless spliced sentences this session.
- **Check that a lane commit landed** (`git log -1` moved) before launching a
  review. A hook-refused commit makes Sol review an empty range.
- **A TC citing an LLR must also cite that LLR's SR,** or `registry-integrity`
  refuses the commit.
- **A traced-only change** (an evidence cell) owes no adjudication. If the
  squash touches its registry's snapshot, re-anchor it with
  `intake.py snapshot --approves <registry>=<ref>` (coordinator D-012).
- **Never reuse a commit-message file** across a lane act and a trunk landing
  (D-013).
- **Rebasing parallel lanes:**
  - RESYNC_PACK: keep both sides' entries, trunk's first.
  - The watermark: take `--ours`, then run `trace.py --bump-ids`.
  - Byte-budget skill rows: take each side's own row.
- **A handoff links the one it replaces.**
- **The adjudicator's OAuth refresh fails headless.** WI-846 holds the fix.
- **Codex plan limit:** hit twice, after about 20 sessions in roughly 2.5
  hours. Wait it out.

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the archived lane
  worktrees (`wi-806`, `wi-818`, `wi-821`, `wi-822`, `wi-835`, `wi-838`,
  `wi-839`, `wi-840`, `wi-841` and `wi-842`) when convenient.
- **Decisions to confirm or overrule, high risk first:**
  - `coordinator-2026-10-06.toml`:
    - D-001 (WI-842 joined the batch);
    - D-010 (WI-841 finished past the guard);
    - D-012 (the traced-only copy act);
    - then D-002 to D-009, D-011, D-013 and D-014.
  - `wi-841.toml` D-001 to D-029, especially:
    - D-021 (the requested-kinds binding);
    - D-022 and D-023 (legacy unbound verdicts are refused at merge, and every
      act needs an accepted verdict);
    - D-027 (the row coverage you ruled).
  - The lane records of WI-842, WI-838, WI-840 and WI-839.
- **Rule** OI-107, OI-106, OI-98 and OI-105.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Read first, in order: CLAUDE.md;
docs/status.md; docs/handoff-2026-10-06-wave18-coordinator.md (state, next
rows, corrections, decisions for the owner); the wave-17 and wave-11
handoffs for the in-lane cycle, the roles and the "never" list; your memory
index.

No lane is open. Scope: the owner names it; by default WI-846 (the
adjudicator home's long-lived token; never read the token file, use only
its path from memory) and WI-834 (the blackout row), claimed under ONE
scoped unpause (a reviewed deletion commit, the claims, a byte-identical
restore). Take the coordinator lease first. Roles: Claude Opus builds
(kit-builder, medium); GPT Terra (medium) authors rows, UTF-8 only,
re-reading every cell it splices; Codex 6.1 Sol (high) reviews, with narrow
rounds while a lane iterates and one FRESH FULL-LANE review as the last gate
before landing; adjudicate from the lane through coordinator_adjudicate.py
adjudicate, never a subagent. Fix crafted-input findings as a class.
Check every lane commit landed before a review. Rebase onto trunk before
landing; land by squash, archive the tips, sweep with
--before/--after/--branch/--merged, and close the re-mint citing the acts.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; ask the owner to confirm or overrule, never to approve. Push
and merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md.

At the end (or at 50% context): update docs/status.md (forward-only), write the
next handoff linking this one and a log fragment, run the full unfiltered suite
once from a detached worktree with a fixed --basetemp under one dated
review-tmp root and delete it once recorded, then hand the lease back with
`coordinator_guard.py handback --handoff <the new handoff>` as the last act.
```
