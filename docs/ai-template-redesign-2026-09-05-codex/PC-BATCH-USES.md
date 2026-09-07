# PC batch-use dispositions for the revised proposal

Baseline: `196bfb9cfb057cdc3df7f9feaf49403c0f57d90b`. These are author proposals
for independent judgment, not accepted live-cell or whole-file judgments.
The [contract packet](PC-BATCH-CONTRACT.md) governs their scope.

The [term inventory](PC-BATCH-TERMS.tsv) is produced by
`git grep -n -I -i -E 'batch|traincar|semicolon' <baseline> -- .
':(exclude)OWNER_SCRATCHPAD.md'`. It complements the
[ID inventory](PC-BATCH-IMPACT.tsv); lexical membership alone neither proves
semantic coverage nor authorizes deletion. A `train` identifier frequently
means a branch/review scope, not multiple executable WIs; its references are
reviewed through the affected module and ID inventory rather than a global
rename. Exact function-level mappings are required again on the implementation
candidate before any test is removed.

| Use | Proposed treatment and reason |
|---|---|
| SR-144 / LLR-144 / TC-138 and LLR-161 / TC-156 | Amend both sibling close descriptions to one spec and preserve immutable report identity, rollback and terminal disposition. No quarantine or rename-recovery obligation is retired. |
| SR-148 / LLR-149 / TC-143 | Amend batch admission only; preserve priority, held approval surface, delegated approval dispatch and adjudication-first partition. The source `_kind_action` dispatches spine building on either tier. A human-held **approval** remains a stop under the current policy. |
| LLR-152 | Amend the residual “batch's strictest value” to the single turn's declared bar. Malformed values still refuse; exact publication scope and recorded no-product-bar result remain. This proposes no new bar implementation or unrelated acceptance repair. |
| SR-148 rationale | Retain selection-precedence uniqueness; SR-156 constrains lane claim cardinality, not another precedence authority. |
| LLR-061 | Keep WI-601 as its sole adjudication owner. It must judge the full final text, including prior drift; no duplicate PC owner or reused old judgment. |
| WI-605 | Its exact `adjudicates` is SR-161, LLR-183, TC-178. The absorption list does not add scope. Retain queued spec and incident evidence byte-for-byte. |
| `docs/concurrency-v2.md` | This is a closed ruled design still cited by current clauses, not an irrelevant archive. Preserve its owner-ruling history; after contract publication add a dated supersession pointer for §A4 batch admission, §A4.4 component batching design note, §A6 spine grouping, §A8's old authority enum and the program-cost claim. The singleton contract replaces the grouping decision; current ordinal holds already supersede the old single-approve arm. Do not rewrite old rulings as if they always said singleton. |
| `tests/test_dispatch_admission.py::test_lanes_back_in_the_station_the_spine_batch_admits_together` | Replace the all-at-once assertion with the first ordered spine WI alone, others queued, plus subsequent exclusive-turn coverage (TC-143). Keep the high-risk singleton and held/released approval cases. |
| `tests/test_dispatch.py::test_the_spine_batch_admits_first_and_together` | Replace grouped worker assignment with sequential exclusive singleton admissions; retain priority over ordinary work and ordinary parallelism (TC-144). |
| `tests/test_integrate.py::test_a_spine_batch_claims_as_one_commit` | Replace supported multi-spec claim with zero-effect cardinality refusal; retain `test_a_spine_claim_succeeds_on_an_idle_station` and single-spec bookkeeping assertions (TC-145). |
| `tests/test_agent_loop_worker.py::test_worker_batch_prompt_names_every_assigned_row_and_its_state` | Replace all-row prompt with one assigned row plus truthful completion predicate and multi-item prelaunch refusal (TC-061). |
| `tests/test_agent_loop_worker.py::test_worker_multi_wi_assignment_builds_in_order` | Retire the multi-WI walk; carry collision-safe logs, provider evidence and per-WI completion into singleton and independent-worker cases (TC-061). |
| TC-205's `test_a_two_row_batch_close_peels_under_one_canonical_order` citation | The function is already absent from the current `tests/test_verdict_record.py` and test tree (`rg` exact name returns no match). Round 001 correctly flagged the cited historical obligation but incorrectly assumed a surviving test. PC deletes nothing here. Primary evidence/carrier semantics and historical multi-item readability remain wanted; reconcile the stale citation with the prior primary-publication migration in its own scope before acceptance that depends on it. Do not silently delete the citation or assert coverage. |
| LLR-140/154/158/182/207/208; SR-170/173 | Retain publication replay, historical evidence, shared outcome vocabulary, single-writer and ordering obligations. File batches, registry row sets and review-scope `train` names are not new executable multi-WI claims. |
| Drafted LLR-210; WI-604/606 | Retain current first-approval ownership. Consolidating several old scopes into a successor proposal is not executing a batch of WIs. |
| Historical logs, archived specs, review rounds and last-approved snapshots | Preserve as evidence; no blanket search/replace. Snapshot writes require the complete independently judged absorption population, not a current terminology cleanup. |
| Generated dashboards/status/rollups | Regenerate from the accepted candidate when it exists; current ID/term hits do not constitute review or acceptance of generated meaning. |
| CSV conversion, retired-vocabulary arms and old resync instructions | Retain pending the supported oldest upgrade revision and corresponding fixtures. Migration authority does not arise from the singleton contract. |

Round 001 described the original patch as ten rows; the exact-cell builder
actually listed seventeen. The revised patch also includes LLR-144, TC-138 and
LLR-152. These counts are derived from the unique keys of the author's
`proposed-cells.json`; they are not test or coverage claims.
