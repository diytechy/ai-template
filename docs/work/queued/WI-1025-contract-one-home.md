+++
id = "WI-1025"
title = "A contract has one home at a time: the row's form until code states it, then the body, with the hand-over checked"
workstream = "process"
sr_refs = ["SR-157", "SR-185", "SR-159"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md#where-the-contract-lives"
needs = ["WI-1024"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Context

Variant F's fifth row (F-5), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Ruled in the review-churn plan: F-call 9 (revision 17: the
code body is the contract's home once built, and the contract exists once),
decision 2 (revision 18: an interface's contract is its form only), the
lifted one-line limit (revision 20: the `data` cell holds the whole form),
and the `call` form "typed, no symbol names" (revision 20).

Today a contract is stated twice: the row's `data` cell (capped at 160
characters by `trace.py`'s advisory; 32 cells exceed it) and the code's
`Contract IF-NNN:` body (230 distinct bodies in scripts, 9 in configuration
and registry headers). The bodies mix form with behaviour: revision 12's
sample found eleven of fifteen carrying obligations. WI-1015's items 3 and
4 (requestors import their owner; `name(args)` signatures match the code)
retire here: the form names no symbols, and the hand-over compares the
row's form with the body exactly (HANDOFF §3.1 Q1's table).

**The model (pointer rules, "Where the contract lives").** Before a body
exists, the row's `data` cell is the contract's home: the whole form, as
many lines as it needs, judged at the sitting of the row it serves. Once a
file states `Contract IF-NNN:`, the body's opening is the form, the exact
text of the cell, and the cell is generated from it. One effective-contract
reader returns the form from whichever home holds it; check A (WI-1030),
rendering and the approval snapshot use it. A commit-versus-parent check
guards the transitions: a body's introduction must match the cell, and a
body's removal must move or retire the contract. An authored edit to a cell
whose body exists fails as stale.

**The migration.** Each body shrinks to its form. Each behavioural sentence
either already exists in the LLR or SR that constrains the interface
(WI-1024 populated those links) and is deleted, or becomes that row's text.
Each crossing `call` row's form becomes a typed request and answer with no
symbol names; the symbol binding stays in the body. `external:`-owned rows
keep their far-side body, checked against an authorized local endpoint.

**Needs:** WI-1024 (the constraining LLR or SR each behavioural sentence
moves to).

## Scope answers

- **S1.** Deliverables, in order on one branch: (1) the reader and the
  transition check, warn-first; (2) the migration of bodies, cells and
  `call` forms; (3) the check made strict and the 160-character advisory
  retired for form cells. Kept together: (3) cannot land before (2), and
  the reader's exact comparison is what (2) is checked against.
- **S2.** No new authority: the check is a commit finding over files and
  registries; nothing releases a hold or authorizes an act.
- **S3.** The form is compared byte-exact after one normalization the plan
  states (line endings, the body's indentation); anything else differs.
- **S4.** `single`: reader, commit check, every script family with a body,
  and a migration.
- **S5.** Moves behaviour from interface to requirement rows; the
  Deliverable names each LLR or SR amended or minted.
- **S6.** No new package, tool or service.

## Done-when

- [ ] One effective-contract reader returns each interface's form: the
      row's `data` cell while no body exists, the body's opening once one
      does. Rendering, the interface reference and the approval snapshot
      read it.
- [ ] A commit check, against the parent: a new body's opening equals the
      cell; a removed body comes with a move or a retirement; an authored
      edit to a cell whose body exists is refused as stale. Warn-first,
      then strict.
- [ ] Every body opens with its whole form and carries no behavioural
      claim; every moved sentence is deleted as already stated or added to
      the constraining LLR or SR (accepted rows: text only, drifting). The
      Deliverable maps each body to the rows it touched.
- [ ] Every crossing `call` row's form is a typed request and answer that
      names no symbol.
- [ ] Each `external:`-owned row's far-side body is checked against an
      authorized local endpoint.
- [ ] The 160-character advisory retires for form cells. Interface rows
      name no file (ruling 5).
- [ ] WI-1023's successor discharge LLR gains its clause: where an LLR
      constrains an interface, the reader returns a valid realization.
- [ ] A RESYNC entry (variant F, after WI-1024's) gives adopters the
      one-home rule and the migration steps.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean;
      red-before tests for each transition; every importer of a changed
      module runs green.
