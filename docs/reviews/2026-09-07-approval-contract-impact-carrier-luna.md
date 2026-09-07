# 2026-09-07 — approval impact carrier independent judgment

Reviewed proposal: `docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`

Proposal SHA-256: `4ebfdbfeed1be8009e3a3fc9caf5fe535fcb14acefc03cd2efdb7d7709ee28b7`

Reviewed authoring clarification: `docs/reviews/2026-09-07-approval-contract-impact-carrier-authoring.md`

Authoring SHA-256: `317e15110396bbce87a01d304b012797648ffea49b03f91f7b9e092874f6e284`

## Scope

This judgment covers only the representational clarification for the selected
queued spec's `(id, path)` impact pair. It does not approve any live LLR/TC
cell, WI-605 cell, runtime implementation, snapshot, Status change, queued WI,
or publication.

## Findings

The general impact rule requires each `(id, path)` row to carry the reviewed
candidate blob. The selected queued spec cannot carry its own final candidate
blob inside `## Approval`: that value changes the blob containing the value.
Using the immutable initial `proposal_spec_blob` for exactly that one selected
pair removes the self-reference without removing the pair from the complete
census.

The clarification preserves the required binding when implemented as stated:
primary validation compares the proposal's frontmatter and definition outside
`## Approval` and `## Dispositions` to the immutable proposal, and final review
binds the actual authored `Approval` and `Dispositions` bytes to the reviewed
candidate. Other census pairs retain their reviewed-candidate blobs. This keeps
coverage and exact-set equality intact while making the selected pair
representable.

The authoring record also correctly states that no live LLR or TC wording
requires a per-path `source_blob` representation. The change is therefore a
scoped schema clarification, not a new workflow or an unreviewed governing
amendment.

## Disposition

**APPROVE — design clarification.** Implementation may use this exception only
for the exact selected queued-spec `(id, path)` pair, with the proposal blob
bound to the initial proposal and the final candidate identity bound after
`Approval` and `Dispositions` are authored. The complete census, duplicate and
missing-pair checks, immutable-definition comparison, and actual-candidate
review remain required.

This approval is a design judgment only. It accepts no approval cells and
creates no publication authority.
