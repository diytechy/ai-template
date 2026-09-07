# PC — single-WI batch-contract proposal

Authoring baseline: `196bfb9c`. The owner requested PC on 2026-09-07, with
contract authoring and adjudication before code deletion, the coordinator
paused, and no control window, push or merge to main. The
[PC package](IMPLEMENTATION.md#pc--the-independently-agreed-cuts-unconditional-after-the-control-window)
is the scope of this sitting. The exact corrected patch was applied to live
source in `c40144d0`; it is not semantically accepted. OI-88 supersedes this
proposal’s earlier separate-owner clauses with the
[reviewed combined transfer](../reviews/pc-transfer/README.md). The proposal
record below preserves the authoring rationale.

## Exact proposed amendment

[The patch](PC-BATCH-AMENDMENTS.patch) contains the exact candidate cell values
against the baseline above. Applying it to a disposable copy parses as TOML
and changes only the listed cells; all Status, parent, method-kind, evidence
path, phase and perspective-reference fields remain unchanged. The exact live registry amendments preserve the snapshot baseline. Existing
tests have not been changed to assert the proposal already works.

| Rows | Proposed decision |
|---|---|
| SR-148 | Admission selects one WI per assignment while retaining the current precedence, deterministic ordering and human holds |
| SR-156 | A lane's executable claim has exactly one WI; multi-item inputs refuse before effects and historical batches remain evidence |
| SR-144 | Partial-close failure preserves a single-WI claim and removes the report created by that failed close |
| LLR-058, LLR-123; TC-058 | Preserve frontier and ordering as distinct decisions; order WIs rather than naming a first member of a traincar |
| LLR-061; TC-061 | One assigned row in the worker prompt and one completion predicate; remove the multi-WI walk while preserving truthful completion and collision-safe evidence |
| LLR-149; TC-143 | The exclusive barrier admits the first spine WI in order alone ahead of ordinary work, subject to adjudication-first partition and the human-held stop; delegated approval rows dispatch singly |
| LLR-150; TC-144 | The worker receives one WI; subsequent spine work waits for the exclusive lane to return; refresh, handback, quarantine and pause behavior stay intact |
| LLR-151; TC-145 | One-spec claim transaction under the existing dispatch lock; refuse unsupported cardinality before mutation and before resuming a provider |
| LLR-161; TC-156 | Preserve immutable reports, rollback on refused close and exactly-once disposition under single-WI execution |
| LLR-144; TC-138 | Reconcile the sibling terminal-close clauses to one claimed spec and the same rollback guarantee |
| LLR-152 | Replace batch strictness wording with the single adjudication turn's declared bar; retain malformed-value refusal and the no-product-bar boundary |
| TC-154 | Preserve adjudication-first stable partition, tested against a spine WI instead of a spine batch |

The parent outcomes remain wanted. SN-027 still requires bounded parallel
ordinary lanes and serialized integration. SN-025 still requires deterministic
selection from tracked state. SN-029 still requires actual delegated approval
and human holds at the declared tiers. None is amended. This is a design change
under those outcomes, not a retirement of parallel work or approval review.

The existing kind-by-human-held table already surfaces held rows even at a
`keep_nondependent` close. The old batch-specific LLR/TC prose still described
the retired single-approve behavior. The candidate follows the current hold
contract; it does not authorize weakening a hold or changing the policy dial.
Spine building remains dispatchable on either approval tier: it proposes work,
not an approval. The first review's suggestion to hold a spine row itself is
not adopted; current `_kind_action` distinguishes that from held approval rows.
For N spine WIs the proposed design costs N exclusive re-attestation windows
instead of one shared window; ordinary work waits for the spine chain to clear.
This is the explicit batching-efficiency tradeoff within the owner's PC scope.
SR-148's “here and nowhere else” still describes selection precedence; SR-156
owns executable lane claims. Their singleton clauses constrain those two
different boundaries and do not duplicate selection precedence.

## Scope census and retained obligations

The FABLE-REVIEW F-01 candidate list was checked against current cells, not
treated as an instruction to rewrite them all:

- SR-144 and SR-156 need the cardinality changes above.
- SR-170 and SR-173 retain their writer, ordering and no-partial-commit
  obligations unchanged. A batch of regenerated files is not a batch of WIs.
- LLR-159's stable partition and census remain unchanged; its TC-154 loses
  only the batch-shaped test setup.
- LLR-182's outcome vocabulary remains valid for one assigned WI and remains
  the existing shared reader. Historical sets are not new executable claims.
- LLR-210 remains Drafted and owned by its existing first-approval work. Queue
  consolidation can propose one successor over several old scopes without
  executing those scopes together on one lane. PC does not retire it.
- LLR-140/154/158/207/208 retain the primary-publication, evidence identity,
  no-product-bar, review and absorption contracts. Removing batch helpers is
  not permission to remove branch-tree identity, publication replay or review.

[The ID-use census](PC-BATCH-IMPACT.tsv) lists each selected row's tracked
references at the baseline, their exact blobs and their live/historical
treatment. Owner-only material is excluded. Historical records remain intact;
live references require review and, where necessary, updates before enablement.
This inventory is evidence for impact adjudication, not a blanket disposition
of every reference. The candidate patch's new references are part of the
proposal and must be included when a live candidate is bound later.
The complementary [term census and dispositions](PC-BATCH-USES.md) includes
the cited concurrency design and test-function discrepancies that ID matching
alone missed. Generated references must be regenerated against the accepted
candidate, not declared accepted merely because they occur in this inventory.

## Existing ownership and approval preconditions

LLR-061 already belongs to queued WI-601's amendment adjudication. This
proposal neither closes that WI nor claims its prior amendment accepted.
Ownership decision: retain WI-601 as the sole LLR-061 adjudication owner. Its
turn must bind and judge the actual final proposed text, including both prior
drift and this amendment, rather than reusing a verdict on the old text. Normal
intake for the remaining PC cells must exclude LLR-061. No transfer or duplicate
owner is proposed. The PC turn owns TC-061, conditioned on WI-601 accepting
the exact final LLR-061 text it tests; WI-601's scope is only LLR-061. A return
or rework there requires corresponding test re-adjudication before acceptance.
WI-605 owns only SR-161, LLR-183 and TC-178; its absorption
ledger confers no scope over PC cells. Its exact queued spec is included in the
supplementary review inputs as disjoint-scope evidence; it remains unchanged.
The queued-spec `adjudicates` census finds no owner for SR-144 or LLR-152.
The future PC amendment turn must own their cumulative snapshot-to-candidate
before/after, including SR-144's earlier Rationale drift and LLR-152's earlier
Detail drift. It cannot judge only this patch and call the rest accepted.
Intake must recheck ownership before binding; if another owner has appeared,
reuse that owner or record a transfer, never mint a competing scope. No automatic
intake deduplication is assumed by this proposal.
The [per-row ownership table](PC-BATCH-OWNERSHIP.tsv) states baseline drift
and the cumulative owner for every proposed row, checked against the queued
specs' actual `adjudicates` cells. The future PC adjudication WI must carry a
hard predecessor edge on WI-601, not merely rely on ID ordering. No new WI is
minted by this proposal packet; ownership must be rechecked at actual intake.
WI-604/606 keep their Drafted first-approval scopes unchanged.

[The pre-existing whole-file census](PC-ABSORPTION-PRECONDITIONS.tsv) was derived
through `primary_approval.absorption_census` against the live baseline. It is
the population already riding the three registries before this proposal.
The future candidate must regenerate it after applying the patch. The primary
publisher requires every absorbed changed cell to have an accepted scoped
judgment; neither PC authorization nor this packet supplies the older rows'
judgments. No whole-file snapshot copy is authorized here.
The [revised-candidate census](PC-CANDIDATE-ABSORPTION.tsv) was regenerated
with the patch applied only to a disposable Git index over the authoring
baseline. Its tree identifies the proposed registry bytes; it is not a commit,
primary turn or approved candidate. The real bound turn must regenerate this
population and supply the required scoped judgments.

A semantic review may accept the proposed design while publication remains
held. That is not enough to delete implementation governed by an unaccepted
live amendment. The sequence stays: exact authoring, normal amendment intake
with exclusive ownership, primary whole-chain adjudication and its publication
preconditions, then single-WI implementation and its independent review.

## Implementation and deletion acceptance, after contract acceptance

Each implementation WI must map every retired test to a retained obligation
or an explicit deletion entry. No blanket deletion of a test module containing
mixed behavior. In particular:

- Keep the exclusive barrier, adjudication-first partition, human holds,
  independent ordinary lanes and deterministic priority order.
- Replace batch admission/claim/worker fixtures with singleton cases and
  explicit zero-effect rejection of multi-item inputs.
- Keep per-WI completion, immutable close reports, required review phases,
  candidate identity, integration bars and crash recovery.
- Remove train assembly and the multi-WI walk only after those cases exist.
  Retain `train` as an existing branch/review-scope identifier where renaming
  it would only create migration work; a branch name is not a batch feature.
- Before switching runtime, enumerate live claims and finished-unmerged
  candidates. Any multi-WI claim holds the switch until supervised reconciliation
  under the prior contract. Preserve historical invocation membership rather
  than rewriting it as singleton evidence.
  LLR-144/TC-138 additionally require partial-close refusal before any report or
  state change when the active claim contains other than one spec. That makes
  unsupported cardinality explicit at close without inventing an upgrade policy.

The package's other cuts are separate ordinary WIs. The CSV converter is not
the whole `wi_convert` module: its live spec parser/writer has current intake
and validation callers. Safe resync and provenance remain wanted. The
[obligation map](P0-OBLIGATION-MAP.md#decision-ledger-and-unmet-evidence)
requires a supported-version boundary and fixtures before legacy expiry;
none is established by this sitting. The supported oldest kit revision is an
owner input, pending while contract work proceeds. Until then retain the CSV
conversion, retired-vocabulary enforcement and old resync instructions.

P0b's complexity re-key and uncalled selector decision are still in PC. They
may proceed once the contract prerequisite is settled, with a deletion record
and applicable tests. No replacement-coordinator, retention or rendering
expansion is included.

## Independent review record

[Round 001](../reviews/pc-contract/round-001/review-result.md) returned the
initial packet. [Round 002](../reviews/pc-contract/round-002/review-result.md)
accepted the design direction and returned remaining ownership and close-path
gaps. Frozen inputs and provider metadata are preserved beside each verdict.
The revised patch includes exact close-cardinality refusal, assignment anchoring
in SR-156, dispatch-owned resume refusal and wording corrections; cumulative
ownership is explicit above. This revision awaits its own independent opinion;
no proposal review is a primary-publication acceptance.

[Round 003](../reviews/pc-contract/round-003/review-result.md) returned the
resume trace and TC-061 ownership. The correction places dispatcher resume
in LLR-150/TC-144, the orchestration pair already under SR-156, and removes it
from LLR-149/TC-145; `_admit_parked` is the actual dispatcher site. This avoids
describing `_abandoned_claim` as the parked-lane resume path: that function
recognizes a crashed claim commit for safe re-cut, not a current active lane.
SR-144 now anchors close-cardinality refusal, LLR-151/TC-145 carry historical
claim evidence, and TC-061's conditional ownership is explicit above.

[Round 004](../reviews/pc-contract/round-004/review-result.md) **APPROVED
authoring/intake readiness conditionally**, with three specified corrections
and no fifth opinion required for those corrections alone. All three are now
applied: F-12 names `dispatch._admit_parked` explicitly as a cross-module
handoff to LLR-150's lane mechanics; F-13 puts close-cardinality refusal in
SR-144's Requirement as well as its acceptance; F-18 supplies the per-row
ownership table. F-14's hard predecessor is an explicit intake condition above.
The final candidate census has been regenerated. The
[correction verification](../reviews/pc-contract/authoring-corrections.json)
records the exact two changed candidate cells after the reviewed revision.
Optional clarity suggestions remain for the actual bound adjudication.
This is proposal readiness only: **live amendment acceptance, snapshot
publication and code/test deletion remain held** by the preconditions above.
