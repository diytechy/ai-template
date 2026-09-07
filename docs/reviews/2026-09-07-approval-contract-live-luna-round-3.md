# 2026-09-07 — approval repair live-cell judgment, round 3

## Verified artifacts and scope

I verified the supplied design proposal and final authoring record before
judging the live cells:

- Proposal `docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`:
  SHA-256 `89f61c67cab0a8dcfbb3cf05bad615ee58b94fca3b7b7cbcc4ceab586751cc42`.
- Final authoring record
  `docs/reviews/2026-09-07-approval-contract-spine-authoring-round-3.md`:
  SHA-256 `23061840937bd265cbf029483a2e7e4940d9e74a3d976951d1cc282ce9d17ee7`.
- Authored `docs/requirements/low-level-requirements.toml` Git blob:
  `e819616aa75be76fc84d6cfbf063551d92b7f5ef`.
- Authored `docs/test/test-cases.toml` Git blob:
  `354a27de0df76fa86c195d023d7b835bdd25d4d6`.

Both registries parse as TOML. I re-read the earlier whole-chain judgments,
the round-2 RETURN/reanchor delta, and the round-3 delta. The complete chains
include each changed LLR's SR parent, cited TC rows, and cited IF seams;
SR-140, LLR-173 and TC-167 remain preserved. Unlisted fields and cells,
including Status and CodeSymbol, remain preserved by the authoring record.

This is an exact semantic judgment. It does not approve a Status transition,
snapshot, WI-605 cell or preserved WI-605 snapshot proposal. No runtime or
live registry was changed by this review.

## Exact row dispositions

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

## Findings resolved and boundaries checked

The prior whole-file snapshot deadlock is resolved by the round-2 contract
clarification: when another scoped owner's `UNJUDGED` or out-of-scope drift
makes a whole-file approval unpublishable, the adjudicator records `RETURN`
with zero accepted cells and no Status or snapshot effect, plus a concrete
reanchor or corrective continuation that preserves the existing scope owners.
Equivalence observations remain findings only. A later complete-scope reanchor
must independently judge every cell before whole-file publication. A malformed
or inconsistent mechanical projection remains pending for REWORK rather than
being silently converted to RETURN. This preserves same-commit approval and
releases the exclusive turn without accepting incomplete evidence.

The round-3 blank-Brief amendment is bounded to a generic primary judgment
assignment carrying the turn, queued WI, base, candidate, scope and verdict
path. It carries no claim, branch, model-side close or snapshot instruction.
A declared Brief whose assembler fails remains HELD and cannot fall through to
that generic assignment; ordinary non-adjudication work retains its worker
assignment. This preserves the specialized grammar and avoids inventing a
legacy adjudication worker path.

The author/committer amendment preserves SR-140: automatic publication derives
the machine Git author from the actual committed ADJUDICATE log's provider,
roster row, model, session and invocation binding. Ambient or configured Git
identity is not evidence, and an automatic human-looking identity refuses and
surfaces the turn. A real human remains author only through the existing manual
primary path with the actual human act bound; the coordinator remains
committer.

The complete carrier cases remain covered: changed proposal or candidate,
wrong primary binding, extra or missing paths, cross-WI close, malformed
successor, partial snapshot, `UNJUDGED` or out-of-scope absorption, stale
review, and author/committer mismatch all refuse toward more review. The
seven-registry whole-file absorption and complete stable-ID impact census stay
required. No new workflow, actor registry, lifecycle phase or model-side
approval path is introduced.

## Verdict

`APPROVE — exact live semantic amendments and test obligations accepted for implementation review.`

This approval is limited to the reviewed meaning and evidence contract. It is
not approval of any Status transition, snapshot publication, WI-605 cell,
preserved WI-605 snapshot proposal, or runtime implementation result.
