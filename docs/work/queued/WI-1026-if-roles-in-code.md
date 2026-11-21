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
interface's local consumer or requestor endpoint is an authored component
id on the row (WI-1022) until a file whose `Component:` header declares
that component takes the interface with a role tag; from then on that
endpoint is generated from the code. An `external:` endpoint has no file to
cite it and stays authored, as an `external:` owner does. The owner stays
authored permanently (F-call 1 (i)), for its independent over-claim check.

The role tag is its own grammar, never a `Contract IF-NNN:` body, so exactly
one file still states each contract (WI-1022's uniqueness rule).

**WI-1015 under F.** WI-1022 made the cross-component rule's cover a `call`
row naming the importer's component as a requestor. Once that requestor
endpoint is handed over, cover binds at the file: the importing file must
carry the tag itself. WI-1015's item 3 (each requestor imports the owner)
is retired as stated (HANDOFF §3.1 Q1): a citation is checked against the
row, not against the import graph.

## Scope answers

- **S1.** One deliverable: the tag grammar, the per-endpoint hand-over and
  its transition check, and the tags written where code already consumes
  or requests a local interface. The tags land with the check, or the
  check reports every endpoint.
- **S2.** No new authority: findings over files and registries.
- **S3.** The grammar and every state are closed in Done-when 1 to 3: a
  malformed tag, a tag in a file with no valid `Component:` header, a
  self-citation, a dead id, or a citation the row does not name is a
  finding. Bounded to supported workflows and kit routes (PROCESS.md §6).
- **S4.** `single`: a grammar, a generator and every file that consumes a
  local interface.
- **S5.** No new state or boundary; an endpoint's home moves from row to
  code. Re-cut LLRs (text only, drifting): LLR-067 and LLR-374 (the
  cross-component rule and its import resolution), LLR-042 and LLR-041 (the
  endpoint cells' checks); the lane's plan completes the list.
- **S6.** `needs` WI-1025: the hand-over reuses its transition machinery.
  WI-1021 and WI-1022 are ancestors through it (headers, component
  endpoints). No new package, tool or service.

## Done-when

- [ ] **The tag.** A line `Consumes: IF-NNN[, IF-NNN …]` or
      `Requests: IF-NNN[, IF-NNN …]` in the file's header, placed as
      WI-1021's grammar places `Component:` for that file type; only these
      two keywords are tags. One reader returns each file's tags. A
      finding: a tag line that does not parse; a tag in a file with no
      valid `Component:` header; a cited interface the file's own
      component owns; a dead id; a (interface, role, component) the row's
      side does not name, authored or generated (the design adds the
      endpoint first).
- [ ] **Hand-over per endpoint.** Each (interface, role, component) endpoint
      hands over on its own: once a file of that component carries the
      matching tag, the endpoint is generated from the tags, and an
      authored edit removing it is refused as stale. Other local endpoints
      on the same side stay authored until taken; `external:` endpoints
      and the owner stay authored.
- [ ] **Losing a citation.** Over (parent, commit): when a handed-over
      endpoint loses its last matching citation (the tag deleted, the file
      removed, or its `Component:` changed), the same commit must remove
      that endpoint from the row, or another file of that component must
      take the tag; otherwise a finding, failing `--strict`. A local
      endpoint the row names that no file has taken yet is reported as a
      warning.
- [ ] Every file that today imports or reads a local interface it does not
      own carries the matching tag, so the generated endpoints equal the
      authored ones they replace; the Deliverable lists any that differ and
      why.
- [ ] **Cover at the file.** For a handed-over requestor endpoint, the
      cross-component rule counts cover for an import from a file of that
      component only if that file carries the matching `Requests` tag; an
      endpoint not yet handed over keeps WI-1022's authored cover. No check
      compares a requestor with the import graph (WI-1015 item 3 is not
      built). The S5 LLRs are amended (drifting, listed for adjudication).
- [ ] A RESYNC entry (variant F, after WI-1025's) gives adopters the tag
      grammar and the hand-over.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean;
      red-before tests for each finding, the mixed side and each way of
      losing a citation; every importer of a changed module runs green.
