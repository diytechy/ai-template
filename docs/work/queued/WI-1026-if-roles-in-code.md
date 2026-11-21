+++
id = "WI-1026"
title = "A file consuming or requesting an interface cites it with a role tag; each local side hands over from the row to code"
workstream = "process"
sr_refs = ["SR-159", "SR-157"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md"
needs = ["WI-1025"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Context

Variant F's sixth row (F-6), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Ruled in the review-churn plan: consumers and requestors
follow the form's hand-over (revision 35), side by side (revision 36). An
interface's local consumer or requestor side is an authored component id
on the row (WI-1022) until a file whose `Component:` header declares that
component takes the interface with a role-typed tag; from then on that side
is generated from the code. An `external:` side has no file to cite it and
stays authored, as an `external:` owner does. The owner stays authored
permanently (F-call 1 (i)), for its independent over-claim check.

The role tag is its own grammar, never a `Contract IF-NNN:` body, so exactly
one file still states each contract (WI-1022's uniqueness rule).

**WI-1015 under F.** WI-1022 made the cross-component rule's cover a `call`
row naming the importer's component as a requestor. Once the importing file
carries a requestor tag, the requestor is the file's own citation, so the
rule binds at the file. WI-1015's item 3 (each requestor imports the owner)
is retired as stated (HANDOFF §3.1 Q1); a citation is checked against the
row, not against the import graph.

**Needs:** WI-1025 (the transition check this row's hand-over reuses).
WI-1022 and WI-1021 transitively (component endpoints, file headers).

## Scope answers

- **S1.** One deliverable: the tag grammar, the per-side hand-over and its
  transition check, and the tags written where code already consumes or
  requests a local interface. The tags land with the check, or the check
  reports every side.
- **S2.** No new authority: findings over files and registries.
- **S3.** The tag grammar is closed (Done-when 1); a malformed tag, a role
  outside {consumer, requestor}, or an id with no live row is a finding.
- **S4.** `single`: a grammar, a generator and every file that consumes a
  local interface.
- **S5.** No new state or boundary; a side's home moves from row to code.
- **S6.** No new package, tool or service.

## Done-when

- [ ] A role tag reads `Consumes IF-NNN` or `Requests IF-NNN` (the exact
      spelling settled in the plan before the build), in the file's header
      block beside its `Component:` line. One reader returns each file's
      tags; a malformed tag, an unknown role or a dead id is a finding.
- [ ] Side by side: a local consumer or requestor side whose component has
      a file carrying the matching tag is generated from the tags (the
      file's component) and an authored edit to it fails as stale; a side
      with no such file stays authored; an `external:` side stays
      authored. The owner cell stays authored.
- [ ] A transition check, against the parent, reports a side whose last
      citing file is removed with no retirement, and a local side the row
      names that no file of that component has taken yet (warn, not
      error).
- [ ] Every file that today imports or reads a local interface it does not
      own carries the matching tag, so the generated sides equal the
      authored ones they replace; the Deliverable lists any that differ
      and why.
- [ ] The cross-component rule reads the requestor from the importing
      file's tag where one exists.
- [ ] A RESYNC entry (variant F, after WI-1025's) gives adopters the tag
      grammar and the hand-over.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean;
      red-before tests for each finding; every importer of a changed module
      runs green.
