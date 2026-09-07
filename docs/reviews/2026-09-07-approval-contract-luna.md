# 2026-09-07 — approval repair contract independent review

## Reviewed artifact and scope

Reviewed `docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`
at SHA-256
`af6a7cc456d8912289b5ad4a4ad541c93bde7d2b2c7c241c4f4158d7830bc611`.
The file is authoring-only and was untracked at review time; this review does
not approve any disputed WI-605 cell or any live spine change.

I read the complete live and `docs/archive/last_approved/` rows for
`SR-140`, `SR-146`, `SR-148`, `SR-156`, `SR-174`, `SR-178`, `SR-144`,
`LLR-140`, `LLR-152`, `LLR-153`, `LLR-154`, `LLR-158`, `LLR-167`, `LLR-173`,
`LLR-207`, and `TC-146`, `TC-147`, `TC-148`, `TC-153`, `TC-161`, `TC-167`.
I also read the cited interface rows `IF-090`, `IF-091`, `IF-123`, `IF-124`,
`IF-127`, `IF-128`, `IF-129`, and `IF-175`, plus the parent SR rows and their
acceptance criteria. The affected live/snapshot rows are `Approved` in both
trees. The live tree already differs from the snapshot in `SR-146`'s
`rationale` and `LLR-167`'s `code_symbol`/`detail`; those differences are
outside this proposal's stated replacements and therefore remain unresolved
input, not approval evidence.

## Row dispositions

| Proposed row | Disposition | Finding |
|---|---|---|
| `LLR-140 Detail` | RETURN | The primary-turn carrier is compatible with `SR-156`'s serial seam and `SR-148`'s tracked deterministic selection, and ordinary claim/merge behavior is explicitly retained. The replacement does not define the exact pending-record fields or the reader's refusal when the bound candidate/turn is absent, stale, or duplicated. That omission is material because `IF-090`/`IF-091` still describe ordinary `integrate`/`lane_approval_refusal` callers and the proposal changes the same ownership seam. |
| `LLR-152 Detail` | RETURN | The no-bar decision can preserve `SR-148`/`TC-146`'s strict bar key only if “exact staged effects” and “declared generated records” are a closed path set. The proposal leaves that set open and gives no test disposition for a generated product artifact or a mixed ordinary/primary batch. It also changes the owner of the no-bar attestation from refresh to publication without specifying the carried evidence shape. |
| `LLR-153 Detail` | RETURN | The proposed stage-only projection preserves serial allocation and the existing trigger/idempotence promises in `SR-174`, but introduces “uncertain decision” without a shipped verdict grammar, parser, record field, or disposition rule. It also says a stale/malformed input refuses “before allocation or staging” without identifying the exact validation boundary. This is an undefined new state, not yet a stable-ID-equivalent amendment. |
| `LLR-154 Detail` | RETURN | Holding the existing slot through judgment and publication is consistent with `SR-156` and `SR-174`, and retaining the post-merge arm preserves the ordinary path. The proposal does not specify how the branchless turn's pending record is admitted, resumed, and closed under `IF-090`, nor how a refusal leaves exactly one durable resumable record. `TC-148`'s requested new case is therefore not a complete acceptance of the amended obligation. |
| `LLR-158 Detail` | RETURN | The worker-wide snapshot/approval-ledger refusal is directionally consistent with the clarified boundary and preserves the shared two-tree/cell-class basis required by `SR-178` and `IF-091`. Renaming `lane_approval_refusal` to `worker_approval_refusal` is an interface/code-symbol change, but no complete caller/reference disposition is supplied; `IF-091` still names the old symbol and the cited census gives counts rather than path-level dispositions. The new positive primary writer is also only described, not bound to a complete interface. |
| `LLR-167 Detail` | RETURN | Binding the in-process brief to primary root, WI, turn, base, candidate and scope preserves `SR-146`'s strict prompt filling and `IF-124`/`IF-127` evidence role. The proposal does not define how the same `session_body` engine receives those arguments or how its verdict record proves each binding. The existing live drift in this `Approved` row versus its snapshot must be resolved alongside the proposed text; silently replacing the pending `WI-603` question would violate the contract's own stable-ID rule. |
| `LLR-207 Detail` | RETURN | The proposed verified projection is compatible with `SR-156`'s tree identity and `IF-175`'s shared verdict reader, and it retains ordinary refresh peeling. The exact `CodeSymbol` replacement is incomplete (“add the primary-turn publication attestor” names no symbol/interface), and the proposed verifier lacks a complete path-to-ledger mapping for close, successor, generated-record and snapshot effects. `TC-205` cannot be accepted from the prose alone. |
| `TC-146 Method` | RETURN | It adds the required branchless/no-bar/resume behavior while retaining rank and strictness. It does not identify the exact assertion that proves no claim, merge, or direct integration interleaves, nor the publication evidence consumed by the no-bar check. |
| `TC-147 Method` | RETURN | It covers atomic projection, refusal, crash-before/after, and no duplicate mint, preserving `SR-174`'s allocation promise. “Uncertain” remains undefined, and the method does not name the exact durable record or verifier that distinguishes pending from complete after restart. |
| `TC-148 Method` | RETURN | It targets the slot ownership and resumable refusal required by `SR-156`/`LLR-154`, but the phrase “one resumable pending turn” has no existing record contract to exercise. It needs the exact pending-record identity and the direct-writer exclusion assertion. |
| `TC-153 Method` | RETURN | It preserves the existing drift-basis cases and adds worker/primary snapshot authorization cases consistent with `LLR-158`. The held-primary success case depends on the unspecified complete absorb ledger and does not enumerate all seven snapshot registries or prove every changed cell is accepted. |
| `TC-161 Method` | RETURN | It retains assembler, slot, digest, refusal and first-approval coverage, and adds primary binding. It does not provide a path-level disposition for the existing `IF-124` baseline semantics or define how a verdict-only record is proven to perform no approval write. |
| `TC-167 Method` | RETURN | Distinct author/committer and false-human-attribution tests are the right preservation of `SR-140`. The contract says automated publication “must set author identity from the bound adjudication session” but does not define how a human act is bound or how the test rejects an unbound forged author. The existing snapshot mirror and seed obligations remain intact only if the primary projection still satisfies the exact whole-file mirror invariant. |

## Stable-ID impact and workflow boundary

The proposal correctly keeps the approval operation exclusive, primary-checkout
resident, and mechanically published after judgment. It does not add a second
general work-selection workflow: ordinary claim/merge/refresh behavior is
repeatedly stated as retained, and the branchless path is scoped to
`adjudication`.

It does not, however, provide the complete impact disposition required before
an existing ID's meaning can change. The census is only a count by broad path
class. It does not enumerate or disposition every live use/reference in the
affected parents, interfaces, tests, runtime symbols, generated views,
approval evidence, and the already-present live drift in `SR-146`/`LLR-167`.
The proposed `lane_approval_refusal` rename alone requires an explicit
`IF-091` and caller disposition. The contract also relies on a WI-596 absorb
ledger without specifying its exact rows, acceptance vocabulary, or how an
`UNJUDGED` cell is represented and checked.

The “adjudicator is Git author / coordinator is committer” split is compatible
with `SR-140` in principle and does not claim a human approved the change. The
proposal must still bind the adjudicator session identity and human evidence
mechanically; otherwise a forged author field remains query-distinguishable
from a human only by convention.

## Verdict

`RETURN — not ready for acceptance or runtime implementation.`

The owner clarification is preserved in direction: stable IDs, exclusive
primary publication, worker refusal, and separate implementation/spine work.
The exact surgical amendments are blocked by incomplete reference-impact
disposition, an undefined `UNCERTAIN` state, an unspecified pending-turn and
absorb-ledger contract, and incomplete author/committer evidence. This review
does not approve the disputed WI-605 cells.
