# WI-623 amendment judgment — sitting 029

Turn: WI-623-c492da3dd0e6247610bf0af116305e989d1d17f7
Base: c492da3dd0e6247610bf0af116305e989d1d17f7
Inspected checkout: ddfd2daa24b824efc2137aa37b029e475c02b376
Final candidate: recorded by the coordinator after the payload commit
Proposal: ef6086929ee50393352e6ed98be68d9c1f5e995b18a720c447c594c7d643298e
Proposal spec blob: e86549cf33a95cc8f28e56317b64608bae04462b
Judgment: docs/reviews/contract_split/029-ADJUDICATE-ddfd2da.md

Acceptance disposition: RETURN the entire bound scope, zero accepted cells.
This is the assigned rework of [024](024-ADJUDICATE-b064550.md) addressing
both findings in [REVIEW-A 025](025-REVIEW-A-8f6397d.md), under the same
pending turn. Unaffected row findings below are preserved from 024 as the
rework instruction requires; they are not a claim of a new complete per-use
semantic review, and supply no reusable partial or equivalent approval.

## Review findings resolved or dispositioned

R25-1 — The old artifact's Git identity did not establish ADJUDICATE authority.
The review correctly identified a DESIGN-CHECK invocation with empty bindings.
That historical log must not be relabelled. This sitting is the actual assigned
ADJUDICATE invocation, bound by its complete delivered prompt to this turn and
this new judgment path. Its delivery record identifies the actual Codex exec
request and gpt-6-astra model. The prompt's complete-file SHA-256 was verified
before inspection:
`a84c01c3d037d1a533a38ad24d7db03a6d423a140d687490a6cc86a1df13ef18`.

I inspected the real post-invocation path in `agent_loop.py`: after the provider
returns, it builds session metadata, merges actual invocation metadata, calls
`primary_adjudication.session_binding`, writes the log and commits telemetry.
For an ADJUDICATE plan with the selected primary turn, that function populates
`primary-turn`, this `judgment` path and the full final HEAD as `candidate`.
The order matters: this judgment is committed first, then every Approval evidence
reference binds its immutable commit. Only after that payload commit can the
coordinator truthfully record the final candidate. No model-authored session
log, invented invocation metadata or retrospective phase relabelling is used.

The coordinator must finish this actual invocation's log, commit it with a fresh
verdict rollup, and verify that `_judgment_records` returns this artifact at the
final candidate. Until that real record exists, the provenance blocker remains
held; this artifact alone does not certify that join. The next REVIEW-A must
receive the owner-authorized exact base-to-final-HEAD comparison through its
session-local override, including this judgment and the final Approval and
Dispositions. It must produce actual independent endorsement and provenance.
Neither this rework nor prior source reviews supply that endorsement. If the
join or review fails, retain REWORK under this same turn. Do not restart the
coordinator or invoke the publisher from this sitting.

R25-2 — Corrected the false set-equality claim. Independently parsed the supplied
Approval and both bound registry versions with `primary_approval.registry_rows`.
Every actually changed cell is covered by the complete supplied decision maps;
those maps also retain unchanged cells. There are 85 actually changed cells in
535 mapped cells, including 450 unchanged mappings. LLR-058 changes Title only,
while its map contains nine cells. All 52 unique scope rows remain `return`.
This is a structural evidence check, not semantic approval. The supplied maps
are preserved in full; no impact or absorption tables authorize acceptance.

The supplied queued spec matches the live queued spec at entry, and the real
`primary_turn.validate` accepts the original selection bindings. No registry
source change is part of this rework. The complete supplied impact population
remains UNJUDGED wherever the prior sitting did not settle it; it is available,
not absent or unreadable. No inventory or hash is treated as use acceptance.

## Row findings

- [CLARITY] LLR-058 Title -> derive the dependency-ready frontier from registry and reservations -> the same derivation, the title no longer naming the ordering that LLR-123 owns -> Detail is byte-identical; a builder acting on the old title already built ordering under LLR-123.
- [MEANING] LLR-061 Detail -> assemble the worker prompt from the listed inputs and read completion from committed trailer evidence -> additionally show exactly one assigned row with id, title, SpecRef and completion state, complete only on a committed WI: trailer AND the spec gone from active/, refuse empty or multi-item assignments before launch, and give --wi no semicolon-list form -> a correct multi-item launch under the old text now fails; the completion predicate became conjunctive.
- [MEANING] LLR-123 Detail/Rationale/Title -> order eligible traincars by the tuple ending in the first WI id -> order eligible individual work items by the tuple ending in the WI id -> the ordered unit changed from a group to a single item; a grouping implementation of the old text fails the new.
- [MEANING] LLR-140 Detail -> read the adjudication spec through terminal-before-active branch precedence and merge an adjudication lane like other work -> read the queued spec and bound primary-turn record, resume a pending turn before selection, treat the terminal spec plus verified publication commit as the only completed form, and run adjudication in process under the held station lock instead of claim/integrate_one -> changes where adjudication executes and what completes it.
- [MEANING] LLR-144 Detail -> close every claimed spec of a lane and restore every report on refusal -> refuse a branch holding other than exactly one claimed spec before any report or state change, close the one spec, restore the single report and leave claim and terminal state unchanged -> a precondition was added and multi-spec close removed.
- [MEANING] LLR-149 Detail -> once lanes are back, admit all spine rows together as one exclusive batch with one worker -> admit the first spine row in LLR-123 order alone, keep the rest queued for later exclusive turns, dispatch spine work on either tier, and dispatch delegated attestation/gate rows singly -> admission cardinality and the approval table changed; human holds still bind.
- [MEANING] LLR-150 Detail -> lane mechanics with the tree signal over specs moved out of active/ -> the same mechanics over the one assigned spec, plus a parked-lane resume that refuses empty or multi-WI assignments before mutation or launch -> a resume-boundary refusal was added.
- [MEANING] LLR-151 Detail/Rationale/Title -> batch-aware claim moving every batched spec in one commit -> claim exactly one WI, refuse other cardinalities before any move, and leave historical multi-WI claim commits readable but never split or re-claimed -> executable batch claims are removed and a refusal added; the rationale now states the traded re-attestation cost.
- [MEANING] LLR-152 Detail -> the adjudication lane's refresh runs no product bar and pins the batch's strictest bar -> the kind runs as a branchless primary turn whose final projection runs no product bar only when its staged effects are confined to the listed publication surfaces, records that honestly, and pins the single turn's declared bar -> the checked object and the no-bar condition changed.
- [MEANING] LLR-153 Detail -> post-merge intake mint with drafts minting at the row's merge -> the same mint plus a stage-only deterministic projection from reviewed Approval bytes, exact close transformation, whole-file ledger, return/uncertain/meaning effects, refusal before allocation, adjudicator-revised RETURN, atomic commit and crash/replay completion -> a transaction contract was added; the allocation invariant is retained.
- [MEANING] LLR-154 Detail -> the post-merge intake hook and refresh bar directives -> additionally the held slot owns branchless publication from admission through judgment, review, projection and atomic commit, excluding claims, merges, integration and new selections, with the durable pending turn keeping writer ownership across processes -> lock lifetime and the excluded writer set were extended.
- [MEANING] LLR-158 Detail -> refuse a lane's approval act over the declared spine universe including needs -> additionally refuse every WI-branch snapshot or approval-ledger change including amendment-only ones, regardless of safety class, and name the held primary turn's projection as the only positive writer bound to decision, scope and ledger -> the forbidden effect set widened and acceptance was bound to exact scope.
- [MEANING] LLR-161 Detail -> restore every report the call wrote so a multi-spec lane cannot half-close -> restore the single report this single-WI call created and leave claim and terminal state unchanged -> the supported close cardinality changed and a rollback effect was added.
- [MEANING] LLR-167 Detail -> claimed-worker brief through one fork, a refusal falling back to the worker assignment, and conflict/amendment unrouted -> the primary turn invokes the review engine in process for both arms with explicit bindings, a blank-Brief adjudication gets a generic bound judgment assignment, a failed declared assembler stays HELD, all shipped briefs are routed with conflict retired and consolidation composed live, and the committed verdict names turn and candidate -> route, refusal and evidence obligations changed while strict filling and live derivation are retained.
- [MEANING] LLR-183 Detail -> row-level Hat-Refs mechanics with per-decomposition coverage stated as NOT DISCHARGED -> the same mechanics with per-decomposition coverage discharged by roster predicates, brief questions and the sitting's review record -> the claimed discharge and the coverage instrument changed.
- [MEANING] LLR-207 Detail -> two disposable classes for the read-only walk, refresh and the mechanical adjudication close admitted by subject and path reconstruction -> one disposable class, refresh, plus a verified primary publication carrier mapped only by exact cold reconstruction under LLR-153/LLR-154 with the listed refusals and no primary mutation -> which commits may carry a governing judgment changed.
- [CLARITY] SR-024 Rationale -> generated dimensional coverage with negative tests a separate obligation -> the same, minus the Hat-derived label -> the obligation is unchanged.
- [CLARITY] SR-033 Rationale -> generated warn-tier checklist as this project's answer to the charter -> the same, minus the label -> unchanged obligation and limit.
- [CLARITY] SR-043 Rationale -> supervised spawn gate, deliberate fail-open, human-held override -> the same, minus the label -> gate behavior unchanged.
- [CLARITY] SR-052 Rationale -> accessibility thresholds through the child chain under an always-ruled charter -> the same, minus the label -> the bar is unchanged.
- [CLARITY] SR-053 Rationale -> cross-view coherence derived from a lens, not a need -> the same, minus the label -> the reservation and verification are unchanged.
- [CLARITY] SR-054 Rationale -> usability with mechanical clauses and one recorded perceptual residue -> the same, minus the label -> the verification split is unchanged.
- [CLARITY] SR-111 Rationale -> record the scaffold's origin stamp for resync -> the same, minus the C-MNT-7 citation sentence -> no origin or resync behavior changed.
- [CLARITY] SR-112 Rationale -> generated, checked per-agent copies with drift as a finding -> the same, minus the citation sentence -> the generated-marking reason survives.
- [CLARITY] SR-129 Rationale -> cell-exact converter proof and single writer -> the same, minus the label -> representation-integrity obligation unchanged.
- [MEANING] SR-144 Requirement/AcceptanceCriteria/Rationale -> terminal partial close with immutable report and second-close refusal, a refusing multi-spec close restoring every report -> additionally refuse a close of a lane whose claim is other than one work item before any report or state change, and restore the single report leaving claim and terminal state unchanged -> a new refusal condition; the Rationale change alone is label removal.
- [CLARITY] SR-146 Rationale -> reviewable prompt files with a per-session digest and a declared inclusion rule -> the same, minus the label -> C-SEC-5 reasoning retained.
- [CLARITY] SR-147 Rationale -> one structured carrier proven cell-for-cell before the authority flip -> the same, minus the label -> migration evidence unchanged.
- [MEANING] SR-148 Requirement/AcceptanceCriteria/Rationale -> select the next work deterministically in the declared precedence -> select exactly one work item per admitted assignment, including exclusive spine admission, in that precedence -> admission cardinality was added.
- [CLARITY] SR-149 Rationale -> retired-vocabulary refusal with history and attestation carve-outs -> the same, minus the label -> no allowed rewrite changed.
- [MEANING] SR-156 Requirement/AcceptanceCriteria -> bounded isolated lanes narrowing to one serial seam -> exactly one work item per lane, with empty or multi-item claim, assignment and resume inputs refused before state change and historical multi-item records readable but not executable -> execution limits were added.
- [MEANING] SR-161 Requirement/AcceptanceCriteria/Rationale/Verification -> a machine-readable per-decomposition perspective record, missing applicable perspectives reportable, verified by Test -> applicable questions in the decomposition brief and each outcome in the sitting's review record, verified by Inspection -> the required artifact and verification method changed.
- [CLARITY] SR-162 Rationale -> the requirement/interface correspondence duty is a review obligation not mechanized here, and no SR states it yet -> the same duty without the coverage-absence claim -> the obligation is unchanged; only an account of coverage was dropped.
- [CLARITY] SR-167 Rationale -> hard perf verdict with stated opt-in scope and an owed re-pointing act -> the same, minus the label -> the owed act remains owed.
- [CLARITY] SR-175 Rationale -> declared inclusion rule derived from the data-protection, security and legal lenses with stated build gaps and the pull-channel limit -> the same derivation in plain wording -> the derivation, gaps and limit are unchanged.
- [CLARITY] SR-176 Rationale -> findings persist by class and location with a stated PII gap -> the same, minus the label -> no coverage extension implied.
- [CLARITY] SR-177 Rationale -> observable rather than budgeted throughput with an undecomposed aggregation gap -> the same, minus the label -> the narrowing and gap are unchanged.
- [MEANING] TC-058 Method -> the deterministic traincar order matches across surfaces -> the deterministic work-item order matches -> the fixture's ordered unit changed with LLR-123.
- [MEANING] TC-061 Method -> two concurrent explicit assignments with isolated evidence -> two concurrent single-WI assignments, prelaunch refusal of empty or multi-WI inputs, and the assigned row's identity, SpecRef and completion state in the prompt -> assertions were added; the LLR-061 trailer-AND-removal predicate is the completion oracle.
- [MEANING] TC-138 Method -> a partial close moves each claimed spec -> an empty or multi-spec claim refuses before any effect and one spec closes -> positive and negative construction changed; quarantine and rename recovery retained.
- [MEANING] TC-143 Method -> every spine row admits as one batch and the level table admits the queued batch at close -> the first spine WI admits alone, remaining rows queue, ordinary single-WI lanes fill only outside the barrier, held rows surface and never release, delegated rows dispatch singly -> expected admission behavior changed.
- [MEANING] TC-144 Method -> a spine batch claims as one commit and its worker receives both ids -> each spine assignment claims one WI whose worker receives only that id, the next waits for the exclusive lane, and _admit_parked refuses empty or multi-WI resumes before mutation -> integration observations changed; handback, quarantine and crash-resume duties retained.
- [MEANING] TC-145 Method -> a spine batch claims as one commit with every spec in active/ -> one spine WI claims with its sole spec, other cardinalities refuse without partial claim, historical multi-spec commits are neither split nor re-claimed -> batch success replaced by cardinality refusal.
- [MEANING] TC-146 Method -> an adjudication-only lane's refresh runs no bar and mixed batches bar -> a queued adjudication runs in primary without worktree, branch or claim, excludes other writers through publication, records a scoped no-product-bar attestation, resumes a pending turn first and completes only through its verified publication commit -> the evidence path changed; malformed bar values still refuse.
- [MEANING] TC-147 Method/Evidence -> adjudication drafts mint at the row's merge -> the stage-only writer derives reviewed Approval/Dispositions, exact accepted effects, exact close, successors and watermark into one atomic publication, with zero-effect invalid input, adjudicator-revised RETURN, reanchor independence and crash-before/after replay -> transaction, absorption and replay proofs were added.
- [MEANING] TC-148 Method/Evidence -> post-merge intake mint and dispatcher continuation cases -> additionally a branchless adjudication under the same slot whose callbacks at admission, verdict, review and pre-commit cannot claim, merge, integrate or start another turn, with the scoped bar directive and one immutable pending turn on refusal -> writer-lifetime verification was added.
- [MEANING] TC-153 Method -> the drift comparator's premise and four corners -> additionally refuse ordinary and adjudication-class WI-branch approval effects and drive the held primary writer over all seven snapshot registries with accepted, UNJUDGED, returned, stale and extra-cell variants -> approval-scope and whole-file verification was added.
- [MEANING] TC-154 Method -> an adjudication row admits ahead of a ready spine batch -> ahead of a ready spine WI -> the competing unit changed with LLR-149.
- [MEANING] TC-156 Method -> real partial-close validity, duplicate refusal and report-path dedup -> additionally inject a refusal after creating the single report and assert restoration with unchanged claim and terminal state -> a rollback obligation was added.
- [MEANING] TC-161 Method/Tier -> routed worker fixtures with fallback, two unrouted briefs, IF-127, at Smoke -> HELD failures, every shipped brief routed with conflict retired, IF-075, bound primary turn records, blank-Brief generic assignment, changed-binding staleness and verdict-only commits, at Full -> verified behavior and tier both changed.
- [MEANING] TC-178 Expected -> satisfies the acceptance folded into LLR-183 and SR-161 -> satisfies LLR-183's mechanics only, with SR-161's acceptance inspected by TC-211 -> this test's claimed discharge narrowed and a separate dependency was added.
- [MEANING] TC-205 Level/Method -> Unit-level verdict record with the mechanical close as a second disposable class and historical dial, scheduler and shared-spec cases -> Integration-level exact primary-carrier recognition with named refusal classes, construction and exclusion proofs delegated to TC-147/TC-148, and actual pending-primary dial, scheduler and shared-input proofs -> the carrier class and the verified behavior changed; Full is retained.

VERDICT: MEANING rows=52

## Continuing RETURN and authority boundary

R1 of 024 remains in force: return every scoped row and every cell in its full
decision map. The complete cumulative approved-snapshot-to-final-candidate
semantic reanchor remains owed, with all meaning-changing uses and whole-file
absorption independently judged. No new corrective registry authoring is
ordered merely because inspection remains incomplete. The nine Drafted riders
and the outside-scope traced Module/CodeSymbol changes recorded in 024 remain
absorption obligations for that reanchor; this RETURN absorbs none of them.

The complete first continuation and its original Context, scope, prerequisites,
owners and reservations are preserved. WI-623 retains the transferred scope
under OI-88 until ordinary intake acts on its typed continuation. Preserve
WI-606, the IF-175 first-approval owner, WI-618 for IF-180, every other Drafted
rider and every PC-BATCH-USES retirement obligation. WI-601/WI-603/WI-605 remain
restructured history, not accepted or complete. Parent acceptance is unchanged;
no interface status is accepted by implication. LLR-061/TC-061 retain exactly
one assigned WI and committed trailer AND active-spec-removal completion.
LLR-167 retains every brief-validity purpose; LLR-153/TC-147 owns transaction
construction, LLR-154/TC-148 writer exclusion, and LLR-207/TC-205 recognition.
All retained parent/counterpart rationales and separate authorities remain.

I read the WI-620 README and PROOFS map and inspected the canonical `_subject`
writer/verifier use, the forged-subject fixture and the unwritable-status query
regression. The subject-only variant leaves the genuine tree intact; the status
query observes the actual returned writer refusal and compares primary file
bytes. These concrete observations do not settle all uses or enlarge the proof
map's limits: representative refusal cases, shared reconstruction inference,
deterministic required-bar replay, process-loss and explicit residue recovery,
uncached replay cost and fixture-versus-real-review provenance remain distinct.
No new full-suite result or general sandbox guarantee is claimed.

R2 of 024 retains the owner-authorized retrospective review range; R3/R4 retain
the separately drafted ordinary resume-deadlock/telemetry repair. That draft is
not substituted for the semantic continuation and is not a prerequisite of its
judgment. Prior publication-success probes are historical, not certification of
this candidate. After real session binding and independent APPROVE coincide,
only the existing exclusive primary publisher may publish the truthful RETURN
under the held slot. Its zero acceptance does not imply zero bookkeeping:
mechanical close, successor minting, watermark and generated effects are still
publisher responsibilities. There is no model-side close here.

No registry cell, Status, snapshot, batch implementation or test is changed.
The tracked pause and status stop instructions remain. No control window,
push or main merge is authorized.

## Validation

The declared smoke command, run through `scripts/check_smoke_budget.py --mode
enforce`, reported:

```text
1696 passed, 4 skipped in 59.52s
smoke wall-clock budget: 59.8s vs 90s budget -> within
```

`check_docs.py --root . --stale` exited zero:
`1572 doc(s), 2526 intra-repo link(s), 0 broken (1 orphan warning(s))`.
`check_trajectory.py --root . --strict` exited zero with existing warnings,
including the queued-WI/trailer reconciliation warning. The verdict rollup was
regenerated with its owning generator. No byte-capped doc was edited.

The unmodified provenance-enforcing projection refused the inspected candidate:
`candidate lacks independent APPROVE review at its bound tree`. The diagnostic
projection with provenance disabled returned `outcome=return`, `statuses={}` and
`approves={}`; that diagnostic was read-only and supplies no publication authority.
The scope/map count above comes from comparing the bound Git blobs at the
inspected checkout using `primary_approval.registry_rows` and the supplied
`parse_approval_payload` maps. Full impact acceptance remains explicitly UNJUDGED.
No publisher or review-bypass mutation was run. Prior sitting results remain
historical and are not reported as new runs.
