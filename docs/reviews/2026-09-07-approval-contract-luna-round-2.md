# 2026-09-07 — approval repair contract independent review, round 2

## Reviewed artifact and identity

The corrected proposal present in the shared checkout is
`docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`,
SHA-256
`49faa6a9a8a718de755dfad74a92e5e868487a0e84696babb346c2541b071701`.
The supplied identity `f2019089cf3f8faa8a789913c5bfcf66639174aefdf02b43e5ceb94c7ab3a08b`
does not match the file present here and was not found in tracked workspace
content. This review is therefore for the exact file hash recorded above.

The prior whole-chain read remains in
`docs/reviews/2026-09-07-approval-contract-luna.md`. I re-read the corrected
carrier/schema and surgical amendments against the same live and
`docs/archive/last_approved/` rows, parent SRs and cited IFs. No live spine row,
snapshot, or disputed WI-605 cell was changed or approved.

## Corrected design disposition

The corrected proposal resolves the prior design objections in substance:

- The pending turn now has a concrete immutable identity: WI, base, primary
  branch/root, exact spec blob, scope, live registry blobs and approved snapshot
  blobs. Duplicate, stale, dirty, mismatched and resumed-turn cases are
  explicitly refused.
- The `## Approval` payload supplies row-level classification, before/after
  identities, evidence, absorption rows/cells, and `UNJUDGED` handling. It
  makes `approve`, `equivalent`, `return`, `uncertain`, and `meaning` distinct
  semantic decisions while keeping `UNCERTAIN` out of Status and lifecycle
  vocabulary.
- The projection allowlist is now bounded to the queued spec, in-scope cells,
  named byte-identical snapshots, terminal move, parsed successors, watermark,
  and existing generated paths. The no-bar boundary is consequently a scoped
  implementation obligation, not a new workflow.
- The corrected tests enumerate the seven snapshot registries, worker refusal,
  primary-only publication, crash points, author/committer cases, and no
  publication from verdict/review files alone.
- The live/snapshot rows reviewed remain `Approved` in both trees. The existing
  live drift in `SR-146` and `LLR-167` is explicitly routed to the existing
  `WI-603` question rather than silently approved by this proposal.

The following proposed amendments are ACCEPTABLE IN PRINCIPLE, pending their
ordinary implementation and independent verification: `LLR-140`, `LLR-152`,
`LLR-153`, `LLR-154`, `LLR-158`, `LLR-167`, `LLR-207`, and `TC-146`, `TC-147`,
`TC-148`, `TC-153`, `TC-161`, `TC-205`. Their preserved parent/IF intent is
still visible: serial selection and landing (`SR-148`/`SR-156`), single-use
identity (`SR-174`), drift basis (`SR-178`), prompt evidence (`SR-146`),
acceptance record (`SR-140`/`LLR-173`), and shared verdict identity (`IF-175`).
The proposed author/committer tests are sufficient as a design obligation under
the repository's stated accident, drift and misbinding threat model; no
additional cryptographic authenticity requirement is imposed here.

This review treats missing runtime functions, exact parser wiring and test code
as implementation work that follows accepted design. They are not blockers in
this design review, provided the implementation obeys the explicit payload,
allowlist, binding and refusal contracts.

## Remaining actionable material blocker

One design gap remains: the stable-ID impact-review evidence is not typed or
complete enough to enforce the `meaning` rule. The payload has a generic
`evidence` list and an `absorption.judgment` reference, while the census has
path counts and a path/ID inventory. Neither says which complete reference set
was reviewed for a meaning change, which reference dispositions were accepted,
nor how the validator proves that every downstream requirement, test,
implementation, and approval-evidence reference to the ID is covered before a
`meaning` decision accepts cells. A generic committed review ref can therefore
be syntactically present while omitting one use. The smallest repair is to bind
the `meaning` decision to a typed, committed impact-review record whose scope
is the complete census for that ID and whose per-reference dispositions are
closed; `equivalent`/`CLARITY` may retain existing implementation judgments
without that impact review.

There is also an artifact identity discrepancy: the supplied f201 hash is not
the file reviewed here. Before treating this round as evidence for the named
proposal, the coordinator must bind the turn to the intended exact bytes.

## Verdict and limits

`RETURN pending the typed complete impact-review binding and exact-artifact
identity reconciliation.`

This is a narrow design return. The corrected proposal is otherwise acceptable
for scoped exclusive primary authoring/publication design. It grants no
approval, does not authorize snapshots, and does not approve disputed WI-605
cells. No implementation or live-spine change is authorized by this review.
