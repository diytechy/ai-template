+++
id = "WI-581"
title = "Lane-close hygiene: quarantine spares monotone and record paths, integrate.lock declared, approval brief regenerated"
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

## Done-when

1. WI-561 Done-when 1–3 below, as written.
2. WI-562 Done-when 1 and 3 below, as written.
3. WI-560 Done-when 3 below, as written.
4. Full suite green.

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

### From WI-560 (Done-when 3 and 4, verbatim — item 4 is shared with WI-579 and WI-580)

3. The trunk step regenerates the approval brief (`CURRENT.md`) after a
   merge that touched it, the same way the trunk lane owns every other
   generated artifact — a following lane is never redded by staleness it
   did not cause.
4. Tests drive all three.
