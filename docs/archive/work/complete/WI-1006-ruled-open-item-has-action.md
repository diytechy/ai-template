+++
id = "WI-1006"
title = "run.cmd audit reports each ruled open item with no action planned, done or handed on to a later open item"
workstream = "process"
sr_refs = ["SR-148"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Deliverable

`gen_open_items.py --ruled-cover` reports, warn-only, each `ruled` open item
whose action no work item, later open item or `follow_up` cell carries, and
`run.cmd audit` runs it ahead of the smoke budget. Built on the maintenance
branch `maint/wi-1006`, cut from `b696b6c36`, outside the lane workflow. The
spec of record is archived as `docs/archive/specs/WI-1006.2026-11-19.md`.

- **The critique's dispositions** (`8e08e7bbd`): `planmode = "single"`; the
  architectural delta (SR-148, a new LLR-370, IF-073's contract, no new
  module, seam or SR, and the check ships); the input space closed in the spec
  of record's "What is matched, exactly".
- **The plan** (`f2b1e08c6`): `docs/plans/WI-1006/plan.md`.
- **Tests first** (`b53384a44`): `tests/test_ruled_open_item_cover.py`, 27
  cases failing before the code because the report did not exist yet.
- **The check** (`6a9462d09`): the rule in `kitlib/spine.py`
  (`ruled_uncovered`), the read and the lines in `pending.py` (`ruled_cover`,
  `work_item_naming`, `ruled_cover_lines`), and the flag in
  `gen_open_items.py`, which stays under the module-size threshold (987 to
  996 code lines). It also carries the schema (`follow_up` in
  `OFFSPINE_KEYS`, both carrier maps, the template's header and `-000` row,
  this registry's header and `-000` row), IF-073's cells, the `[run] audit`
  line, LLR-370, TC-430 and TC-431 (Drafted), and the RESYNC entry, which
  adds an optional key and forces nothing.
- **The four items** (`c14c78489`): `follow_up` cells on OI-35, OI-89 and
  OI-90, each citing the commit, work item or record that carried its
  ruling out.
- **Review fixes** (`691ebc859`), from the review of the branch (Sol on the
  code, Argon on the prose):
  - only a later open item, one with a higher number, covers, whether it is
    pending or ruled and covered. `_earlier_items` replaces `_named_items`;
  - the token's trailing boundary now matches its leading one, so `OI-35abc`
    and `OI-35_x` name nothing;
  - LLR-370's `code_symbol` names `main`, and its detail says "done for
    `complete/`";
  - the rule's wording follows: "a later open item" in the spec of record,
    the template, the registry header, IF-073, LLR-370, TC-430, the RESYNC
    entry, the report and the audit description;
  - two new regressions: an earlier pending item and an earlier covered
    ruled item each cover nothing.
- **OI-80** (`ebecad203`): the later-only rule reports it, because the only
  item naming it is the earlier OI-72. Its ruling commit `525b2503c` carried
  the ruling out, and its new `follow_up` cell cites that commit.

**Measured at close.** Over this repository's 116 ruled items the report
finds 0. With this row's own file set aside it finds 1, OI-79.

**Left undone, and why.**

- **OI-79 has no `follow_up` cell.** Its ruling deletes the remote ref
  `wi508-architectural-remap-HELD-for-owner-verdict`, which is the operator's
  push. The fetch of 2026-11-19 still lists that ref at `fa3c99c4`, so there
  is nothing to cite. The report reads OI-79 as covered only because this
  row's Done-when names it. That is rule 1's stated upper bound, and this case
  is a real instance of it. Two ways out are the operator's to choose: record
  the delete in a `follow_up` cell once it is done, or file an operator-act
  row.
- **No SR states the coupling** between operator decisions and the work that
  cites them, as WI-790 recorded. LLR-370 sits under SR-148 beside LLR-298
  and LLR-299.
- **No review rounds.** On this maintenance branch the parent session reviews
  the diff.

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request). The spec of
record holds the rule, why it reads text rather than `needs`, and the numbers
a prototype measured on this repo. Its scope critique is owed before a claim.

No SR states this today. The critique decides whether one is owed, or whether
IF-073's registry contract carries it.

## Done-when

- [x] A check reports, warn-only, each `ruled` open item that has none of: a
      work item in an open or complete directory whose text names it; a later
      open item naming it that is `pending`, or `ruled` and itself covered;
      a `follow_up` cell. The rule is the spec's.
- [x] The open-items template's header documents the optional `follow_up`
      cell and asks a follow-up item to name the item it continues; the `-000`
      row shows it. This repo's registry follows.
- [x] `run.cmd audit` runs the check, and a finding does not change its exit
      code.
- [ ] The four ruled items it reports at filing (OI-35, OI-79, OI-89, OI-90)
      each gain a `follow_up` cell or a citing row, so it lands with 0
      findings.
      Open: OI-35, OI-89 and OI-90 carry cells citing their evidence, and so
      does OI-80, which the later-only rule added at review. The report lands
      with 0 findings. OI-79's ruled act, deleting a remote ref, is not done,
      so it has no cell, and only this row's own text covers it (see the
      Deliverable).
- [x] Regressions name each arm: covered by a draft, queued, active, deferred
      or complete row; not covered by a cancelled, partial or restructured
      row; handed to a pending item; handed through a ruled item
      that is itself covered; a cycle of ruled items with no row; a
      `follow_up` cell; no registry (vacuous); a registry that does not parse
      (stops, as the readers do).
- [x] A RESYNC entry if the check ships to adopters: a new optional key, no
      forced migration.

## Critique dispositions

Round 1 (Gemini Argon, 2026-11-19,
`docs/reviews/2026-11-19-scope-critiques/WI-1006.md`): CHANGES-REQUESTED,
two MAJORs and one MINOR. All three are adopted, and none grows the row.

- **S4, the planning ruling: adopted as `planmode = "single"`.** The check
  judges every ruled item against every work item and every other open item,
  and it touches three modules, so a short plan precedes the code.
- **S5, the architectural delta: adopted.** The spec of record's
  "Architectural delta" settles each of the three questions:
  - the anchor is SR-148 (Accepted), which already carries the ruling sync
    (LLR-298) and pending citation integrity (LLR-299). A new design row,
    LLR-370, states the check. No SR is minted;
  - IF-073's contract, in its row and in the registry's header, carries the
    optional `follow_up` cell and the cover rule. The check lives in modules
    that already read the registry: the rule in `kitlib/spine.py`, the read in
    `pending.py`, and the report as `gen_open_items.py --ruled-cover`. No
    module, seam or interface row is added;
  - the check ships, because all three modules and the open-items template
    are kit-owned. So Done-when item 6's RESYNC entry is owed: a new optional
    key, nothing forced.
- **S3, the input space: adopted.** The spec of record's "What is matched,
  exactly" closes the token boundary (`OI-35` never matches `OI-350`), which
  text is scanned (the whole work-item file, not its `specref` target), the
  `-000` rows, an item naming itself, the statuses, and when `follow_up`
  counts as set.

One reading was settled here and then reversed at review. Here, "a later
open item" in Done-when item 1 had been read as "another open item" with no
dates compared. The review of 2026-11-19 held the Done-when to its word: only a
later item, one with a higher number, covers (`691ebc859`). Two ruled items
can still name each other, so item 5's cycle stays a case. Cover then runs
from the later item to the earlier one only.
