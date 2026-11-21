+++
id = "WI-1022"
title = "Interface rows name components, not files: each owner is a component id or external party; internal call rows retire"
workstream = "process"
sr_refs = ["SR-159", "SR-157"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md"
needs = ["WI-1021"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
supersedes = "WI-1015"
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
Seven `external:` parties are in use (`agent CLI`, `coordinator`,
`downstream adopter`, `git`, `run.* launcher templates`, `run.* launchers`,
`upstream docs`). `trajectory_arch`'s owner-exact check and the
contract-body gate's stray-declaration rule (`arch_interfaces._owner_files`,
`_owner_exact_findings`, `_stray_declaration_findings`; OI-67's slices,
tagged LLR-042) and `trace.py`'s refusal of an id-shaped owner (LLR-041) key
on the owner path. 268 rows are `Drafted`, so the migration needs no act;
the one `Accepted` row drifts for adjudication.

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

**The component registry's prose.** CMP-006's `notes` cite cover rows
(IF-093, IF-175, IF-214, IF-314, IF-315); this row amends any sentence the
stricter cover or a retirement makes untrue.

**Left to other F rows:** the `data` cell's whole form and the hand-over
(WI-1025); role-typed citations (WI-1026); the `constrains` link that
makes every interface reached by a requirement (WI-1024).

## Scope answers

- **S1.** Two deliverables, in order on one branch: (1) the registry
  migration and the checks that read the migrated cells, which must change
  in one commit or every owner check fails; (2) the `call` classification
  and retirements, which read the migrated endpoints. (2) could land alone;
  it is kept here by choice, so that it lands before WI-1024 populates
  requirements for every live interface and no retiring row gets one.
- **S2.** No: the cells feed existing strict checks; nothing gains
  authority over a hold, an act or a gate.
- **S3.** Each endpoint cell admits exactly a live `CMP-NNN` id or an
  `external:` token from the declared party list (Done-when 1); anything
  else is a finding. A row whose owner and every endpoint are `external:`
  stays refused, as today.
- **S4.** `single`: registry schema, three check families and a migration.
- **S5.** Changes the boundary rule's cover (WI-1015 item 1) and retires
  internal seams. Re-cut LLRs (text only, drifting): LLR-041 (the owner's
  form), LLR-042 (the owner-exact and contract-gate slices), LLR-067 (the
  cover), LLR-199 (placement in the component view); the lane's plan
  completes the list. Each retired row is named in the Deliverable.
- **S6.** `needs` WI-1021: the owner component is the producing file's
  header, and uniqueness checks the body's file header. No new package,
  tool or service.

## Done-when

- [ ] Every interface row's `owner` is a live `CMP-NNN` id or an
      `external:` token; its `consumers` and `requestors` hold only those
      forms. An `external:` token is `external:` followed by a party on the
      list the registry header declares (the seven in use); a new party is
      added to that list by the row that introduces it, and an unlisted
      party is a finding. The `component` cell leaves the schema; its
      placement meaning is derived (the lowest component enclosing every
      endpoint, for the views only). A file-channel or directory owner
      (`docs/reviews/`, `docs/work/`) names its producing component, chosen
      in the lane's plan and listed in the Deliverable.
- [ ] The interface registry's header states the owner as "a component id
      or an `external:` party, never a requirement id", citing revision 35,
      and IF rows name no file in any cell (ruling 5).
- [ ] The stray-declaration rule becomes uniqueness: at most one in-tree
      file states each `Contract IF-NNN:` body. Zero is valid while the
      row's `data` cell is the contract's home (WI-1025 guards the
      transitions); two or more is a finding. Where a body exists: for a
      locally owned interface, its file's `Component:` header names the
      owner; for an `external:`-owned one, its file's header names a
      component the row lists among its `consumers` or `requestors`, and
      any other component is a finding. The scan surface is shipped
      scripts, configuration files and registry headers; the approval
      snapshot, `docs/reviews/`, `docs/plans/` and example documents are
      outside it.
- [ ] The cross-component rule counts as cover only a `call` row owned by
      the imported file's component that names the importer's component
      as a requestor. The kernel allowlist and the one-component exemption
      are unchanged. Every crossing the stricter cover exposes is covered,
      or listed in the Deliverable with the row filed for it.
- [ ] Each `call` row is classified crossing or internal in the lane's
      plan. Internal rows retire unless the plan quotes the rationale that
      earns them; each retirement names the row and its reason.
- [ ] The S5 LLRs and CMP-006's `notes` are amended where this row makes
      them untrue (text only, drifting); the Deliverable lists the acts
      owed for adjudication.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean; the
      interface reference and the component views regenerate.
- [ ] A RESYNC entry (variant F, after WI-1021's) tells adopters to rewrite
      owners and endpoints to component ids, with the mapping rule.
- [ ] Tests: red-before for each endpoint finding, the party list, zero,
      one and two bodies, the external-body rule and the stricter cover;
      every importer of a changed module runs green.
