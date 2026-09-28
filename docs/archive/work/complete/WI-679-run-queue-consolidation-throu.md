+++
id = "WI-679"
title = "Run queue consolidation through the kit's own census, adjudication and close, and repair what kept this repository's 2026-09-27 consolidation out of it"
workstream = "process"
specref = ""
sr_refs = ["SR-220"]
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

Built by one builder in three Codex Sol rounds (wave-5 arbitration rulings
5 to 9), SOUND at fb9ca52a. The end-to-end bullet is the coordinator's, run
on trunk in the commits right after this close. Its record, with the census
output, the verdict and the open count before and after, is the section
"WI-679's end-to-end run" in `docs/log.d/2026-09-27-wave5-coordinator.md`.

- **Guard 1 (`_pending_refusal`), changed.** The census now refuses only
  while a judgement is active, while another consolidation row is queued,
  while a queued judgement's `Adjudicates` names a candidate row, or while a
  queued judgement would sort at or before the consolidation in
  `schedule.evaluate`'s own order. Each refusal names the judgement. The
  population is queued work rows: judgement rows and the `-000` example are
  never candidates (the example had been one).
- **The surface signal: not added, on measurement.** At 8aae3af3 (the 50-row
  queue before the hand consolidation) the existing signals found 12 of the
  66 table pairs and joined 1 of 11 groups. With the population fix, the
  one-union candidate set holds 34 of the table's 40 ids, and 6 of the 11
  groups whole. A component signal found 0 of 66 pairs. A module-by-spec
  signal bought one more group for about 200 more noise lines in the brief.
  Grouping by shared surface is the judge's reading, which the brief already
  asks for.
- **Guard 3: the hand hosts are not judged.** A successor is read only from
  a judgement that ENACTED a consolidation: a done `consolidate` row whose
  recorded outcome is `consolidate` and whose draft supersedes the absorbed
  row. A hand consolidation's host is an ordinary row. `{prior}` marks each
  absorbed row "judged by WI-###" or "by hand", and keeps an absorption event
  after its successor is itself absorbed. No live host needed a mark.
- **The hand-merge gap.** `intake.py sweep --merged WI-### --branch <lane>
  --before <pre-squash> --after HEAD` mints what the merge slot's
  `intake_after_merge` would have: amendment and first-approval rows,
  dispositions and spot checks, merged adjudications' drafts, and the
  re-judge checkpoint. It says by name when the Done-when arm cannot run
  (a hand-cut lane has no trunk claim). `intake.py consolidate [--dry-run]`
  runs the census.
- **SR-220** states one obligation with one `shall` and stays Drafted.
  LLR-210 and TC-208 were amended in place (status Approved). LLR-264,
  LLR-265, TC-260, TC-261, IF-243 and IF-244 are new Drafted rows. PROCESS.md
  has no queue-consolidation rule, so the one doctrine sentence went at the
  `restructured` definition in PROCESS_OPTIONS.md (+300 bytes, re-stamped).

Recorded, not built: a hand-merged `consolidate` row that is then swept
enacts absorption without `close_refusal`'s scope and drift rungs; and
`handback.close_adjudication` has no CLI.

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

Folded 2026-09-27 (spine-acts batch B's close): WI-681 APPROVED LLR-210, TC-208 and TC-254 and
RETURNED SR-220, whose requirement carries two `shall`s ("shall hand that set to a single judgement,
... and shall enact the judgement's outcome ..."), a form finding `trace.py --strict` gates on an
Approved row. The fix is item 4 of WI-681's Dispositions
([`docs/archive/work/complete/WI-681-adjudicate-batch-b-first-approvals.md`](WI-681-adjudicate-batch-b-first-approvals.md)): drop the
second `shall`, or split the enactment into its own row under SN-025. This row realises SR-220 and
may restate it anyway, so the fix is taken here. The adjudicator recommends the owner widen SN-025's
acceptance ("the loop keeps its own queue free of duplicated work") and keep the derived label until
then; that is the owner's call and is recorded, not acted on. LLR-210, TC-208 and TC-254 are now
Approved, so a change this row makes to their meaning (for example, to `_pending_refusal`) is an
in-place amendment, status left Approved, for the next spine-acts batch.

A second finding on the same surface (the hand path bypassing the kit's own machinery), from batch B's
adjudicator and wave-5 arbitration ruling 4: the coordinator's hand squash-merges do not run the kit's
merge checkpoint, so the five observation cases `rejudge.due_cases` reports due (TC-036, TC-055, TC-209,
TC-210, TC-211, none with a result on record) have no re-judge rows, although WI-657, WI-621 and
WI-581 merged after WI-638 declared their inputs. The consolidation bypass and this one are one gap:
what the kit's merge does that a coordinator's hand merge skips.

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
- The coordinator's integration step runs the kit's merge checkpoint (or the handoff names the command that does), and the five due observation cases have their re-judge rows minted by it, not by hand.
- SR-220 states one obligation with one `shall` (or its enactment is split into its own row), stays Drafted, and is listed for the next spine-acts batch's first approval.
- The commit bar passes.
