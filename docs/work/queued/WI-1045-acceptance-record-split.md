+++
id = "WI-1045"
title = "acceptance_record's landing rules move to a CMP-008 module; the file keeps the two-tree comparison"
workstream = "process"
sr_refs = []
needs = ["WI-1021", "WI-1023"]
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md"
buildtier = "strong"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Context

Filed on trunk on 2026-11-21 from WI-1021's one-component table, on the
operator's ruling (queue-drill HANDOFF §3.5 R2). Under one component per
file (§3.3 N3), a file doing two components' work is evidence about the
partition (OI-14): it keeps its one header and gets its own row, never a
split inside the row that found it.

`project-trajectory/scripts/acceptance_record.py` (2,392 lines) declares
CMP-006 under WI-1021. Its declared job is the spine's: comparing two git
trees cell by cell to say whether accepted text moved (LLR-158, LLR-178,
LLR-202, LLR-220, LLR-222, LLR-225, LLR-302). Beside it sit rules the
coordinator's landing runs on top of that comparison, which their design
rows tag CMP-008:

- the ruling-to-citer sync (LLR-298: `ruling_sync_lines` and its staged and
  commit forms);
- the parent-first commit judgement (LLR-358: `parent_first_lines` and its
  forms);
- the intake mint's acceptance arms (LLR-153) and its settled-amendment
  filtering (LLR-364);
- the held re-acceptance's text identity (LLR-359: `accepted_text_digest`,
  `amendment_values`).

The merge-time re-acceptance refusal (LLR-278) is tagged CMP-006 and reads
as the spine's; the plan says which side it falls on. Each of these design
rows also names functions in other files (`check.py`, `integrate.py`,
`text_then_act.py`, `intake.py`), so the exact set that moves is the plan's,
read from the code.

`check_doc_refs.py`, the table's other file doing two components' work, gets
no row until WI-1023 lands: its symbol-binding oracle's spine role retires
there (§3.5 R2).

**Order (settled by the scope critique, 2026-11-21).** After WI-1023 (F-3),
which itself follows WI-1022 (F-2). F-2 makes interface owners and endpoints
component ids and narrows the cross-component cover, so the move's seams are
written once, in that form. F-3 removes the design rows' `module` and
`code_symbol` cells, so the move re-points none of them.

## Done-when

- [ ] The CMP-008 rules above live in one or more modules whose `Component:`
      header declares CMP-008; `acceptance_record.py` keeps the two-tree
      comparison and its CMP-006 header. The plan lists every function that
      moves and every one that stays, with the design row behind each.
- [ ] Every cross-component import the move introduces or redirects is
      covered under F-2's rule: a `call` row owned by the imported file's
      component that names the importer's component among its requestors.
      That includes the edges between CMP-006 and CMP-008 and the callers
      in other components whose import now lands in the new module, such
      as `check.py` (CMP-007) on the parent-first rules through IF-308. The
      cover is a new `Drafted` row, a requestor added to an existing
      `Drafted` one, or an existing seam re-owned, each with its contract
      body; the cross-component rule reports nothing uncovered.
- [ ] Behaviour is unchanged: no design row's requirement text changes, and
      every test module importing `acceptance_record` or a module this row
      creates runs green with only its imports changed; a test that must
      change otherwise is named in the Deliverable with its reason.
- [ ] `acceptance_record.py`'s size baseline is re-stamped down by what left;
      `trace.py --strict` and `check_trajectory --strict` are clean.
