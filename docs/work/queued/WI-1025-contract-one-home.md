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
exists, the row's `data` cell is the contract's home, judged at the sitting
of the row it serves. Once a file states `Contract IF-NNN:`, the whole body
is the form and the cell is generated from it. A body keeps today's grammar
(`gen_arch_map._contract_bodies`): it runs from the opener to the next
opener, a blank line or the end of the header, so a form is one paragraph,
wrapped over as many lines as it needs. Symbol names stay in the code
outside the body. One effective-contract reader returns the form from
whichever home holds it; check A (WI-1030), rendering and the interface
reference use it.

**The migration.** Each body shrinks to its form. Each behavioural sentence
either already exists in the LLR or SR that constrains the interface
(WI-1024 populated those links) and is deleted, or becomes that row's text.
Each crossing `call` row's form becomes a typed request and answer with no
symbol names. `external:`-owned rows keep their far-side body (WI-1022's
rule), its form our reading of the external surface.

## Scope answers

- **S1.** Deliverables, in order on one branch: (1) the reader and the
  transition check, warn-first; (2) the migration of bodies, cells and
  `call` forms; (3) the check made strict and the 160-character advisory
  retired for form cells. Kept together: (3) cannot land before (2), and
  the reader's comparison is what (2) is checked against.
- **S2.** No new authority: the check is a commit finding over files and
  registries; nothing releases a hold or authorizes an act.
- **S3.** Closed in Done-when 1 to 4: one normalization, one set of
  transition states over (parent, commit), one `call` form grammar.
  Bounded to what supported workflows and the kit's routes produce
  (PROCESS.md §6); a hand edit of a generated cell is what the stale rule
  catches.
- **S4.** `single`: reader, commit check, every script family with a body,
  and a migration.
- **S5.** Moves behaviour from interface to requirement rows. Re-cut LLRs
  (text only, drifting): LLR-042 (the contract gate's slices), LLR-041
  (the `data` cell advisory in `trace.py`), LLR-080 (the declared-interface
  rendering) and WI-1023's successor discharge LLR. The destination of each
  body's prose is the LLR or SR WI-1024 linked to its interface; the lane's
  plan lists them per body, with any unresolved destination recorded, and
  the Deliverable gives the final body-to-row map.
- **S6.** `needs` WI-1024: each moved sentence goes to the constraining row
  it populated. WI-1023 is an ancestor through it. No new package, tool or
  service.

## Done-when

- [ ] **One reader, one normalization.** The effective-contract reader
      returns each interface's form: the row's `data` cell while no body
      exists, the whole body once one does. Two texts are the same form
      when equal after converting line endings to LF, stripping each line,
      dropping empty lines and joining the rest with single spaces. The
      generated cell keeps the body's line breaks. Rendering and the
      interface reference read the reader.
- [ ] **Transitions, per interface, commit against parent** (a body exists
      when WI-1022's uniqueness scan finds one): no body in either, the
      cell is authored and unchecked; a body in both, the commit's cell
      must equal the commit's body, else stale; a body introduced, it must
      equal the parent's cell (or the new cell, for a row added in the
      same commit), and a commit changing the cell and introducing the body
      together is a finding; a body removed, the same commit must state it
      in another file (a move) or retire the row, else a finding.
      Warn-first, then strict.
- [ ] Every body is its whole form and carries no behavioural claim; every
      moved sentence is deleted as already stated or added to the
      constraining LLR or SR (accepted rows: text only, drifting, listed
      for adjudication).
- [ ] **The `call` form.** Every crossing `call` row's form reads
      `request: <what is passed>; answer: <what returns>`, in that order,
      and names no symbol: no token in it is a name the shipped scripts
      define (by `ast`) written as code (backticked, containing `_`, with
      an internal capital, or followed by `(`). That name reader is built
      once here; WI-1028 reuses it.
- [ ] Each `external:`-owned row's far-side body is checked against an
      authorized local endpoint (WI-1022's rule).
- [ ] The 160-character advisory retires for form cells. A form names no
      file: a `file`-channel form uses artifact-class wording (ruling 5;
      WI-1022 took file names out of the endpoint cells).
- [ ] WI-1023's successor discharge LLR gains its clause: where an LLR
      constrains an interface, the reader returns a valid realization.
- [ ] A RESYNC entry (variant F, after WI-1024's) gives adopters the
      one-home rule and the migration steps.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean;
      red-before tests for each transition state and the `call` form;
      every importer of a changed module runs green.
