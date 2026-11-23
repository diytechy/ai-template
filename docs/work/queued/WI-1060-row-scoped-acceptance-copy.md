+++
id = "WI-1060"
title = "An acceptance act's copy writes only the rows the act names, so one unblessed row no longer blocks its registry"
workstream = "process"
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md"
sr_refs = ["SR-179", "SR-207"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, on the
operator's ruling given in the coordinator's session ("Yes please file the
row-scoped copy as a work item"). That chose this design over multi-verdict
carry-forward (the specref, §0 step 4).

**The problem.** The acceptance record (`docs/archive/last_accepted/`)
holds a byte-for-byte copy of each registry file, and an act refreshes a
registry by copying the live file over its record. SR-207 refuses that
copy while any row of the file outside the act has drifted from its
recorded text, since the copy would bless text no verdict judged. That
rule is right. But it couples every row of a file: one unblessed amendment
blocks every blessed amendment and every first acceptance in the same
registry. The design registry alone holds 356 rows.

The drill met the coupling at every sitting but the last:
- WI-1047's act was refused outright, and the row was cancelled and
  superseded.
- WI-1049 and WI-1055 each needed an operator ruling to revert the
  unblessed rows on trunk so the rest could be recorded, then a follow-up
  row (WI-1050, WI-1056) to re-land them. Until they re-landed, the
  reverted rows described code that no longer existed.

The operator has given a standing revert ruling to keep sittings moving;
this row removes the need for it.

**Why this design** (the coordinator's recommendation, adopted by the
ruling). PROCESS.md lets a lane land with amendments still owed: its merge
is refused only for an act no verdict backs, and a MEANING row or a first
draft "neither holds a lane". A held rung's acceptance is the operator's,
taken later. So drift from several landings sharing one registry on trunk
is the kit's normal state. Carry-forward (an earlier verdict's blessed
rows, digest unchanged, joined into one later whole-file act) would end the
re-judging but keep the coupling: blessed rows, and new rows waiting to
flip, would still wait on every drifted sibling. Writing only the named
rows ends both. Blessed rows are anchored at once and drop out of the next
sitting, so carry-forward is not needed.

**The rule it keeps.** The record is still written only by copying live
text (SR-179, LLR-178), now at the row: an act copies, byte for byte, the
live text of exactly the rows it names (accepted, re-accepted, retired).
Every other row keeps its recorded text. An act cannot carry an unnamed
row's drift into the record by construction. SR-207's refusal becomes this
construction, and a drifted row outside the act simply stays drifted and
owed. The mirror rules restate the same thing: a record written at a
commit equals the previous record with exactly the act's named rows taken
from live at that commit.

**Trust.** The row adds no authority to any act. An act still writes only
what a verdict or the operator authorizes, and now can write no more than
that. The surface that changes is the record writer and the two checks
that judge what it wrote. A defect there could bless unjudged text, so the
tests must show a laundering attempt refused at each check, and the row
runs the unfiltered suite before it lands.

**The plan settles** (`planmode = "single"`), before any edit:
- **Traced cells of rows the act does not name** (links such as
  `verifies`, which need no acceptance and ride today's whole-file copy):
  refreshed with the act, or left for each row's own act. State the choice
  and why. Today every act's copy refreshes every row's traced cells, the
  ones routed to adjudication included, since only drift in accepted cells
  refuses the copy. The choice weighs that against how a routed traced
  change is found owed. The plan writes its rule into this spec's
  Done-when, in the three items that name it, before any edit, and the
  coordinator approves the plan before the build.
- How a retired row leaves the record, and how a new row enters it.
- The rows' order and every byte between rows, so the record stays
  diffable against live.
- Tiers that share one file.
- The off-spine registries (interfaces, components, external), which today
  no combined sitting shows.
- **The first (seed) snapshot,** which blesses whole files once, stays as
  it is.
- Each accepted row whose text states the whole-file copy: at least SR-179,
  LLR-178, SR-207 and LLR-245 (search for others). Its amendment is text
  only and goes to a sitting; SR-207's is shown to the operator.

**Coverage bound.** The writer's and the checks' promises reach the
records that supported workflows and the kit's own routes produce: acts
taken through the snapshot command, with the registries as committed.
Hand-edited kit-written state (a hand-edited record copy or snapshot stamp)
is outside them (PROCESS.md §6, "Review threat model"), apart from what the
Done-when names inside: the laundering attempts the checks must refuse.

**Ordering.** WI-1045 moves `acceptance_record.py`'s landing rules into a
new module. This row changes the snapshot checks in the same file, so the
two land one after the other, never side by side.

## Done-when

- [ ] An act writes into the record only the rows it names, each copied
      byte for byte from live; every other row of the recorded file keeps
      its recorded text, apart from what the traced-cell rule refreshes. A
      drifted row the act does not name stays drifted, is reported as owed,
      and no longer refuses the act.
- [ ] The writer re-reads its result and refuses, writing nothing, unless
      the result reads as the previous record with exactly the named rows
      replaced, plus what the traced-cell rule refreshes.
- [ ] The checks that judge a written record judge it at the row: a record
      written at a commit equals the previous record with exactly that
      act's named rows taken from live at the commit, plus what the
      traced-cell rule refreshes. (The traced-cell rule is the one the plan
      settles and writes into these three items.) Tests show refused,
      at the commit hook and on a committed revision: an unnamed row's
      drift carried in, a named row copied with an edit, and a row dropped
      that no act retired.
- [ ] A test reproduces the drill's case: one registry holding a blessed
      amendment, an unblessed amendment and a row ruled ACCEPT. The act
      records the first and third and leaves the second drifted and owed.
- [ ] The seed snapshot still copies whole files, and existing records
      read clean under the new checks with no migration.
- [ ] The accepted rows that state the whole-file copy are amended (text
      only, no code names) and listed in the Deliverable as owed to
      adjudication. Any new row is `Drafted`. A RESYNC entry tells adopters
      what changed and that their records need no migration.
- [ ] The unfiltered suite passes on the branch before the merge, and its
      summary line is quoted in the Deliverable.
