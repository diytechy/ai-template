+++
id = "WI-1065"
title = "The vocabulary migrator's record step works in a record that holds a row-by-row act"
workstream = "process"
specref = "docs/archive/work/complete/WI-1060-row-scoped-acceptance-copy.md"
sr_refs = ["SR-247", "SR-179"]
needs = ["WI-1060"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, from
WI-1060's review (Sol, round 1, a MAJOR the coordinator recorded as this
follow-up) and its plan's eighth decision.

WI-1060 makes an acceptance act write only the rows it names, and judges
each later write of the record at the row once the record holds an act
carrying kept rows. The vocabulary migrator's record step (SR-247,
LLR-369) writes every record copy equal to live, absorbing drift by design
(the test-tiers plan's D13, operator-ruled). In a record that holds a
row-by-row act with a row still kept, that write carries the kept row's
live text into the record without an act, and the hook refuses the commit.
So after an adopter's first act on the new kit, the migrator's record step
no longer lands while any row is owed. WI-1060's RESYNC entry tells
adopters to run the migrator before that first act.

**The design call is the operator's.** SR-179 says the record is written
only by copying live text. The migrator's absorption was ruled because a
vocabulary move changes spellings, not meaning. The candidates:
- (a) The migrator rewrites the spellings inside each record copy in
  place, leaving every row's own text, so a kept row stays kept in the new
  spelling. This writes the record other than by copying live, so SR-179
  and SR-247 are amended to allow that one kind of write.
- (b) The migrator's record write becomes an act of its own. It names the
  rows whose only difference from live is spelling, keeps every other
  drifted row, and adds a ledger entry, so the row-by-row judge passes it.
- (c) Nothing changes beyond WI-1060's RESYNC guidance: run the migrator
  before the first row-by-row act, and refuse it after with a message
  saying so.

**Operator ruling (2026-11-23): refined (c).** Keep SR-179's mirror
invariant untouched and keep the vocabulary migrator standalone (no
compatibility readers in the mirror judge and no forged acceptance acts).
Once the record's act ledger holds any entry carrying `kept` (even an
empty list, which turns on the row-by-row judge for every later write):
- **Record already in the current vocabulary** (current directory name,
  current ledger keys, no earlier spellings in record copies): skip
  writing record copies from live, so running the migrator (or `--check`)
  for non-record files leaves kept and pending-drift rows untouched,
  exits 0 when nothing else is owed, and lands cleanly past both the
  commit hook and the committed-history check.
- **Record still carrying earlier vocabulary** (earlier directory name,
  earlier ledger keys, or earlier spellings in a record copy): refuse
  before writing any record file — including in the registry step, which
  currently walks the record directories before the record step runs —
  exit 1, and point to WI-1060's RESYNC guidance (run the migrator
  before the first row-by-row act).
- **Pre-row-by-row records** (no ledger entry carrying `kept`): keep
  today's behavior unchanged.

SR-179 and LLR-178 need no amendment; only SR-247, LLR-369 and TC-427
take text-only amendments.

Operator's choice recorded; owes a scope critique before it is built.

## Done-when

- [x] The operator's choice among (a), (b) and (c) is recorded here.
- [ ] In a record whose act ledger carries `kept` (including with a kept
      row), the migrator skips record copies when the record is already
      in the current vocabulary (so non-record rewrites pass the commit
      hook and the committed-history check, and `--check` does not flag
      pending drift) and refuses before modifying any record file —
      including in the registry step — when the record still stores
      earlier vocabulary; tests cover both paths and verify the commit
      hook and the committed history.
- [ ] Any accepted row this changes is amended (text only, no code names)
      and listed as owed to adjudication.
