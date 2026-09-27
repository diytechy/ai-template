+++
id = "WI-679"
title = "Run queue consolidation through the kit's own census, adjudication and close, and repair what kept this repository's 2026-09-27 consolidation out of it"
workstream = "process"
specref = "docs/log.d/2026-09-27-wave4-consolidation.md"
sr_refs = ["SR-220"]
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed by hand on 2026-09-27 at the owner's direction: "the consolidation of
work items may itself need to be a work item. The adjudicator is supposed to
look at that (mechanically, for other projects that adopt this process), and
perhaps all of that will work, I'm just not sure / a bit nervous."

**What happened.** The fourth coordinator session cut the queue from 50 open
items to 21 as a HAND trunk commit (97815a8c), following the 2026-09-02
restructure's precedent. It formed eleven host rows, each absorbing others
into `docs/archive/work/restructured/`. The kit ships machinery for exactly
this: `consolidate.census_draft` finds candidate clusters,
`intake.mint_consolidation` mints one `consolidate` adjudication row, an
independent adjudicator judges it from `adjudicate_brief.consolidate_values`,
and the consolidation close archives the absorbed rows. That machinery was
not used, for two reasons. Both are adopter-facing defects or gaps, not
local quirks:

1. **The census refused to run.** `_pending_refusal` refuses a mint while ANY
   adjudication row is queued or active. Three unrelated adjudications
   (WI-604, WI-675, WI-676) were queued. A project whose loop keeps even one
   adjudication open at every tick may never be able to consolidate.
2. **Its signals do not see surface-sharing groups.** The pair producer and
   the two widening signals key on a shared spec, a shared commissioning plan
   or OI, near-identical titles, and SRs whose design rows name one module.
   Most of the session's groups were rows that edit one surface from
   different specs (the snapshot and its readers; the claim, close and mint
   path; byte-budgeted doctrine). Nothing in the census would have proposed
   them.

**And a consequence the hand commit created.** `consolidation_successors`
reads any row whose `Supersedes` names a `restructured` row as a
consolidation's own successor, and guard 3 (`_seed_pairs`) stops such a row
from seeding a cluster. The eleven hand hosts (WI-615, WI-616, WI-620,
WI-621, WI-638, WI-651, WI-657, WI-672 and those since closed) all carry
that mark. So the census now treats them as already judged, although no
adjudicator judged them. The hand path bypassed the judgement, and it also
switched the guard on.

The obligation this row realises is SR-220 (Drafted, first approval owed in
the next spine-acts batch): overlapping queued work is consolidated through
one judgement per queue state.

## Done-when

- The two blockers are decided and, where the decision is a change, built
  test-first:
  - whether `_pending_refusal` should refuse only when a queued or active
    judgement touches a row the census would cluster, rather than any
    judgement at all;
  - whether the census gains a surface signal, such as rows whose specs or
    SRs reach the same module or component, measured against this
    repository's 2026-09-27 groups (the table in the specref) for recall and
    noise.
  Each decision states its reason. A change to an approved row's meaning is
  amended in place and judged in a spine-acts batch.
- The hand hosts' standing under guard 3 is decided and recorded. Options
  include: an independent adjudicator judges the eleven hand groups
  retroactively from the kit's consolidate brief, and its verdict is recorded
  as their judgement; or a hand consolidation is marked so the guard does not
  read it as judged.
- The machinery is then exercised end to end on this repository's live
  queue, with no hand archiving. The census runs, one `consolidate` row is
  minted, an independent adjudicator judges it, and the consolidation close
  enacts the verdict (or the census proposes nothing and says why). The log
  fragment records the census's output, the verdict and the open count
  before and after.
- The coordinator doctrine (the next handoff and, if it states one,
  PROCESS.md §3's consolidation rule) says consolidation runs through this
  machinery, and a hand consolidation is the stated fallback, not the path.
- The commit bar passes.
