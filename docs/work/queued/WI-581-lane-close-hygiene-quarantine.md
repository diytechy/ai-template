+++
id = "WI-581"
title = "Lane-close hygiene: quarantine spares monotone and record paths, integrate.lock declared"
workstream = "process"
needs = ["~WI-579"]
specref = "docs/plans/2026-08-31-verdict-record-and-queue-blockers.md#2-the-other-things-that-stopped-the-queue"
buildtier = "quick"
priority = 6
safety_class = "ordinary"
supersedes = "WI-561;WI-562;WI-560"
+++

## Context

Minted by the owner-directed backlog restructure of 2026-09-02 (plan of record `docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.2; executed out of band as a hand trunk commit series, not by a lane). The absorbed rows are archived under `docs/archive/work/restructured/` with their scope text untouched; their Done-when blocks are QUOTED below under their old ids and remain the spec this row must satisfy — decompose, don't paraphrase.

**Why one row.** Three quick, edgeless, priority-3 items in the lane-close
path (`dispatch._refresh_or_quarantine`, the unload residue set, the trunk
step's regeneration list). One quick lane instead of three.

**Re-scoped 2026-09-26 (owner-approved backlog audit).** WI-560's item 3,
regenerating the approval brief, landed in `dc395734` as the trunk step's
`approval-brief` regeneration step, so it and its quote leave scope. Re-read in
the code, the rest is still open: the revert WI-561 names now runs in
`handback.quarantine`, whose `BOOKKEEPING` exemption
(`project-trajectory/scripts/handback.py`) spares `docs/work/`, `docs/log.d/`
and `docs/handbacks/` but neither `docs/id-watermark` nor `docs/reviews/`; and
`integrate._RESIDUE_OUT_FILES` declares `out/review-owed` and
`out/agent-loop.lock` but not `out/integrate.lock`.

## Done-when

- `handback.quarantine`'s revert leaves `docs/id-watermark` (and any other path
  monotone by contract) as the lane left it, and the reverted tree passes
  registry-integrity (WI-561 item 1).
- The revert keeps `docs/reviews/` as a record path, beside `docs/log.d/` and
  the handback report it already keeps (WI-561 item 2).
- `out/integrate.lock` is in `integrate._RESIDUE_OUT_FILES`, with the same
  test-and-fixture treatment `out/agent-loop.lock` received (WI-562 item 1).
- Tests drive both revert exclusions on a scaffold quarantine and the lock on
  an unload, and the full suite stays green with no other residue class
  regressing (WI-561 item 3, WI-562 item 3).

### From WI-561 (Done-when, verbatim)

1. `dispatch._refresh_or_quarantine`'s revert excludes `docs/id-watermark`
   (and anything else monotone by contract): a minted id is burned whether
   or not its row survives, and the reverted tree passes
   registry-integrity.
2. The revert preserves `docs/reviews/` and `docs/log.d/` as record paths,
   the way it already preserves the handback report — evidence of what
   happened survives the reverting of what was done.
3. Tests drive both exclusions on a scaffold quarantine.

### From WI-562 (Done-when 1 and 3, verbatim)

1. `out/integrate.lock` is declared in the unload residue set, with the
   same test-and-fixture treatment the agent-loop lock received.
3. The full suite stays green; no other residue class regresses.
