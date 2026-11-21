+++
id = "WI-1022"
title = "Interface rows name components, not files: each owner is a component id or external party; internal call rows retire"
workstream = "process"
sr_refs = ["SR-159", "SR-157"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md"
needs = ["WI-1021"]
buildtier = "strong"
safety_class = "ordinary"
supersedes = "WI-1015"
priority = 2
planmode = "single"
+++

## Context

Variant F's second row (F-2), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Ruled in the review-churn plan: F-call 1 (i) and decision 1
(revisions 17 and 18), the OI-67 (a) header amendment (revision 35:
"a component id or an `external:` party, never a requirement id"), ruling 5
(IF rows name no files), and the classification of `call` rows
(revision 20).

Today the 269 interface rows name files: 229 owners are `scripts/<module>`
paths, about 36 are other paths (`docs/requirements/`, `docs/work/`,
`docs/stack.ini`, `docs/process.toml`, templates, directories), and 4 are
`external:` parties. 176 rows carry the optional `component` cell, a
placement; decision 1 found 35 to 39 of them name where the seam sits, not
who produces it. 157 rows list requestors and 112 consumers, as paths.
`trajectory_arch`'s owner-exact check and the contract-body gate's
stray-declaration rule (`arch_interfaces._owner_files`,
`_owner_exact_findings`, `_stray_declaration_findings`) key on the owner
path. 268 rows are `Drafted`, so the migration needs no act; the one
`Accepted` row drifts for adjudication.

**WI-1015's item 1 lands here** (restructured into F, HANDOFF §3.3 N1). The
cross-component rule (LLR-067) counts any interface row naming both files
as cover, on any channel and whoever owns it. Rebinding cover to components
closes that: an import from a file of component X into a file of
component Y (X ≠ Y, Y's file not on the kernel allowlist) is covered only by
a `call` row owned by Y that names X among its requestors. WI-1026 later
reads the requestor from the importing file's role-typed citation; until
then it is the authored component id.

**`call` rows (revision 20).** The 133 `call` rows are classified. One whose
owner and every endpoint resolve to one component is internal: optional
under F (point 3), it retires unless its original rationale earns it,
judged row by row and never by its `kitlib` path or a code-naming `data`
cell. One crossing a boundary stays; its symbol-free typed form is
WI-1025's.

**Needs:** WI-1021 (the owner component is the producing file's header;
uniqueness checks the body's file header).

**Left to other F rows:** the `data` cell's whole form and the hand-over
(WI-1025); role-typed citations (WI-1026); the `constrains` link that
makes every interface reached by a requirement (WI-1024).

## Scope answers

- **S1.** One deliverable: the registry migration and the checks that read
  the migrated cells, which must change in the same commit or every owner
  check fails. The `call` classification lands in the same lane, after the
  migration, since it reads the migrated endpoints.
- **S2.** No: the cells feed existing strict checks; nothing gains
  authority over a hold, an act or a gate.
- **S3.** Each endpoint cell admits exactly a live `CMP-NNN` id or an
  `external:<party>` token; anything else is a finding.
- **S4.** `single`: registry schema, three check families and a migration.
- **S5.** Changes the boundary rule's cover (WI-1015 item 1) and retires
  internal seams; each retired row is named in the Deliverable.
- **S6.** No new package, tool or service.

## Done-when

- [ ] Every interface row's `owner` is a live `CMP-NNN` id or an
      `external:<party>`; its `consumers` and `requestors` hold only those
      forms. The `component` cell leaves the schema; its placement meaning
      is derived (the lowest component enclosing every endpoint, for the
      views only). A file-channel or directory owner (`docs/reviews/`,
      `docs/work/`) names its producing component, chosen in the lane's
      plan and listed in the Deliverable.
- [ ] The interface registry's header states the owner as "a component id
      or an `external:` party, never a requirement id", citing revision 35,
      and IF rows name no file in any cell (ruling 5).
- [ ] The stray-declaration rule becomes uniqueness: exactly one in-tree
      file states each `Contract IF-NNN:` body, and for a locally owned
      interface that file's `Component:` header names the owner. An
      `external:`-owned row's body sits in a file of a component that
      endpoint names. The scan surface is shipped scripts, configuration
      files and registry headers; the approval snapshot, `docs/reviews/`,
      `docs/plans/` and example documents are outside it.
- [ ] The cross-component rule counts as cover only a `call` row owned by
      the imported file's component that names the importer's component
      as a requestor. The kernel allowlist and the one-component exemption
      are unchanged. LLR-067's amendment is drafted (Accepted: text only,
      drifting for adjudication). Every crossing the stricter cover exposes
      is covered, or listed in the Deliverable with the row filed for it.
- [ ] Each `call` row is classified crossing or internal in the lane's
      plan. Internal rows retire unless the plan quotes the rationale that
      earns them; each retirement names the row and its reason.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean; the
      interface reference and the component views regenerate.
- [ ] A RESYNC entry (variant F, after WI-1021's) tells adopters to rewrite
      owners and endpoints to component ids, with the mapping rule.
- [ ] Tests: red-before for each endpoint finding, the uniqueness rule and
      the stricter cover; every importer of a changed module runs green.
