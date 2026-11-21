+++
id = "WI-1023"
title = "LLR rows lose their module, code_symbol and component cells; readers use the Implements index and placement is derived"
workstream = "process"
sr_refs = ["SR-157", "SR-180", "SR-186"]
specref = "docs/plans/2026-10-11-review-churn/README.md#5-requirements-never-reference-code-code-points-up"
needs = ["WI-1021", "WI-1022"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Context

Variant F's third row (F-3), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). It is item 5's layer 1 ("make it unrepresentable in the
schema", owner ruling 2026-10-11, ruling 5), with revision 35's overruling
of "LLRs keep naming their component by id": LLR → CMP retires and
placement is derived.

Today all 347 LLR rows (345 `Accepted`) carry `module`, `code_symbol` and
`component`. `trace.py --strict-schema` requires the first two, and
`check_doc_refs --strict` binds the symbol. SR-180, LLR-180 and TC-175 state
that a design row is discharged only by a realization symbol that resolves:
the binding this row removes. The cells' readers include
`kitlib/spine.py`, `spine_carrier.py`, `migrate_carrier.py`, `trace.py`,
`check_doc_refs.py`, `check_privacy.py`, `kitlib/secret_classes.py`,
`lane.py`, `coherence.py`, `intake.py`, `acceptance_record.py`,
`gen_components.py` and the dashboard renderers; the lane's plan enumerates
them from the code, since a name match over-counts.

**Two down-pointing traced cells, one act.** The TC `evidence` cell's
test-file parts are already held equal to the test files' TC tags in both
directions (LLR-366). Ruling 8 (revision 8) and revision 35 make them
generated from those tags; CI workflows, inspection and review records stay
authored. They ride this row because both are layer 1 and both are covered
by the one batch act below.

**The batch act is the operator's (HANDOFF §3.3 N4).** Removing three cells
from 345 accepted rows is "trace cells removed, requirement text unchanged":
one ruling, recorded once, never 345 re-attestations. Every other act this
row creates (the SR-180 chain's retirement, the successor rows, amended
text) goes to automated adjudication; the lane lists them and flips nothing.

**SR-180's successor (F point 6, revision 18).** The discharge rule is
restated per evidence kind: a TC verifies the LLR; where the LLR constrains
an interface, the effective-contract reader returns a valid realization
(WI-1025 adds that clause); otherwise it is placed through its TC or
counted unplaced. New ids carry it; SR-180, LLR-180 and TC-175 retire with
a successor record (keep-or-mint, revision 26). This row mints one SR, its
LLRs and TCs, `Drafted`, from ranges the coordinator sets at launch (the
drill expects no SR mint without one).

**"Module" retires as a spine term (revision 35).** Shipped text that uses
it as a spine unit where this row removes the column is reworded:
`RUNTIME_FLOWS.template.md` (participants from the LLR `Module` column) and
the performance-budget template's `Refs`.

## Scope answers

- **S1.** Deliverables, in landing order on one branch: (1) the schema
  change, readers on the index and derived placement; (2) the SR-180
  chain's successor; (3) TC evidence generated. Kept together: one batch
  act covers (1) and (3), and (2)'s oracle is removed by (1).
- **S2.** No new authority: the index replaces cells as the input to
  existing checks.
- **S3.** The loader refuses any key a requirement tier does not declare
  (deny by default). The evidence generator reads the existing tag grammar
  and rewrites only the parts LLR-366's reader rule binds to the declared
  tests root; parts outside it and parenthetical notes are kept verbatim.
- **S4.** `single`: many script families, a schema and a migration.
- **S5.** Placement becomes an output derived from new inputs (interface
  owners; WI-1024 adds `constrains`). SR-180, LLR-180 and TC-175 are
  re-cut (PROCESS.md §5).
- **S6.** `needs` WI-1021: file membership no longer comes from LLR cells;
  WI-1022: placement derives through an interface's owner component. No new
  package, tool or service.
- **B4.** The batch act is held for the operator (Done-when 6).

## Done-when

- [ ] `module`, `code_symbol` and `component` leave the LLR schema in
      `kitlib/spine.py` and the template; the loader refuses a key a
      requirement tier does not declare, naming the row and the key.
- [ ] Every reader of the removed cells reads one index generated from the
      `Implements:` tags instead, or retires. `--strict-schema` and
      `check_doc_refs --strict` no longer require or bind them.
- [ ] An LLR's placement is derived: the owner component of an interface
      its verifying TC names (WI-1024 adds `constrains`). An LLR with
      neither is listed as unplaced and counted, not refused; one placed
      at several interfaces is placed at each. The views read placement.
- [ ] SR-180, LLR-180 and TC-175 retire with a successor record; a new SR,
      LLR and TC state the per-evidence-kind discharge rule, `Drafted`.
- [ ] Each TC `evidence` cell's test-file parts (the parts LLR-366's reader
      binds to the declared tests root) are generated from the test files'
      TC tags and checked current; parts outside the tests root, other
      evidence kinds and parenthetical notes stay authored, kept verbatim.
      The generated cells equal today's on every row.
- [ ] The batch act is held: the lane stops at a green tip with the cells
      removed and asks the operator for the ruling "trace cells removed,
      requirement text unchanged", recorded once in the Deliverable. It
      takes no other act, flips no status and runs no snapshot; the
      Deliverable lists every act owed for adjudication.
- [ ] A migration script removes the cells from an adopter's registries
      (`migrate_carrier.py` is the precedent), and a RESYNC entry (variant
      F, after WI-1022's) gives the steps and the `ADOPTING.md` note.
      `RUNTIME_FLOWS.template.md` and the performance-budget template stop
      naming a `Module` column.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean; every
      test importing a changed module runs green, plus
      `test_import_layers`, `test_module_size_ratchet` and
      `test_dogfood_sync`.
