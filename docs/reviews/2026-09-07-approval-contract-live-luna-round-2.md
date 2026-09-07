# 2026-09-07 — approval repair live-cell judgment, round 2

## Reviewed identities and limits

I verified the supplied frozen design proposal:

`docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`

SHA-256: `89f61c67cab0a8dcfbb3cf05bad615ee58b94fca3b7b7cbcc4ceab586751cc42`

The final live authoring record is
`docs/reviews/2026-09-07-approval-contract-spine-authoring-round-3.md`,
SHA-256:
`23061840937bd265cbf029483a2e7e4940d9e74a3d976951d1cc282ce9d17ee7`.
The exact live registry identities are Git blobs
`e819616aa75be76fc84d6cfbf063551d92b7f5ef` for
`docs/requirements/low-level-requirements.toml` and
`354a27de0df76fa86c195d023d7b835bdd25d4d6` for
`docs/test/test-cases.toml`. Both parse as TOML.

I re-read the prior whole-chain judgments and the round-2 RETURN/reanchor
authoring. This review covers the complete parent chains and cited IF seams,
including SR-140, LLR-173 and TC-167, which remain unchanged. Every amended
row keeps its prior Status, CodeSymbol, identity, references, rationale and
tier. No snapshot, runtime source, WI-605 cell or approval record was changed
or approved by this review.

## Exact live dispositions

Each changed cell is a meaning amendment: it adds the primary-turn,
projection, refusal, restart, brief-routing or provenance obligation that was
not present in the prior text. The exact amended meanings are accepted as
consistent with the frozen design and their complete chains.

| Changed cell | Parent and cited evidence | Disposition |
|---|---|---|
| LLR-140 Detail | SR-156; TC-132 | APPROVE semantic amendment |
| LLR-152 Detail | SR-148; TC-146 | APPROVE semantic amendment |
| LLR-153 Detail | SR-174; TC-147, IF-091 | APPROVE semantic amendment |
| LLR-154 Detail | SR-174; TC-148, IF-090 | APPROVE semantic amendment |
| LLR-158 Detail | SR-178; TC-153 | APPROVE semantic amendment |
| LLR-167 Detail | SR-146, SR-144, SR-148; TC-161, IF-124, IF-075 | APPROVE semantic amendment |
| LLR-207 Detail | SR-156; TC-205, IF-175 | APPROVE semantic amendment |
| TC-146 Method | SR-148/LLR-152 | APPROVE semantic test obligation |
| TC-147 Method | SR-174/LLR-153/IF-091 | APPROVE semantic test obligation |
| TC-148 Method | SR-174/LLR-154/IF-090 | APPROVE semantic test obligation |
| TC-153 Method | SR-178/LLR-158 | APPROVE semantic test obligation |
| TC-161 Method | LLR-167; IF-124, IF-075 | APPROVE semantic test obligation |
| TC-205 Method | SR-156/LLR-207/IF-175 | APPROVE semantic test obligation |

## Findings checked against the prior RETURN

The prior whole-file snapshot deadlock is resolved within the existing owner
contract. When another scoped owner's `UNJUDGED` or out-of-scope drift makes a
whole-file approval unpublishable, the requested decision becomes `RETURN`
with zero accepted cells and no Status or snapshot effect. Its concrete
reanchor or corrective continuation preserves the existing scope owners and
closes atomically. Equivalence observations remain findings only; a later
complete-scope reanchor must judge every cell independently before publication.
A mechanical inconsistency remains pending for REWORK rather than being
silently converted to RETURN. This preserves same-commit approval and gives
the pending turn a finite release path.

I also checked the newly authored boundaries:

- A blank-Brief adjudication receives only a primary judgment assignment bound
  to the turn, queued WI, base, candidate, scope and verdict path. It carries
  no claim, branch, model-side close or snapshot instruction.
- A declared Brief whose assembler fails stays HELD and cannot fall through to
  the blank-Brief route; ordinary non-adjudication work retains its worker
  assignment.
- Automatic publication derives the machine Git author from the actual
  committed ADJUDICATE log/provider/session binding. Ambient or configured
  identity is not evidence; an automatic human-looking identity refuses and
  surfaces. A real human remains author only through the existing manual
  primary path, while the coordinator remains committer.
- The carrier cases retain refusal coverage for stale or changed proposal,
  candidate, primary binding, extra or missing paths, cross-WI close,
  malformed successor, partial or UNJUDGED snapshot absorption, and
  author/committer mismatch. The seven-registry whole-file absorption and
  complete impact census remain required.

These clauses preserve the unaffected promises in the parent rows and do not
create a second workflow, actor registry, lifecycle phase or model-side
approval path.

## Verdict

`APPROVE — exact live semantic amendments and test obligations accepted for implementation review.`

This is a meaning judgment only. It does not approve any Status transition,
snapshot publication, WI-605 cell, preserved WI-605 snapshot proposal, or
runtime implementation result. Implementation must still satisfy the exact
record, scope, carrier, refusal and review tests before any primary
publication act.
