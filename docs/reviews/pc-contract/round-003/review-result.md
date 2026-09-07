# PC batch-contract proposal, round 003 review

**OUTCOME: RETURN** (narrow). The design direction stands and is not re-opened here. Round 002's F-1 through F-6 are applied as claimed, but the F-4 relocation of the resume refusal left the design/test trace inconsistent, and one cell's ownership is still unstated. Both fixes are small exact-text edits.

**Deletion/publication decision: NOT AUTHORIZED.** No live registry amendment, snapshot write, code deletion or test deletion is permitted by this review, before or after the corrections below. The preconditions listed at the end are inherent and unmet.

## What I could not verify

- The TOML parse and the "only the listed cells change" claim. I judged the diff text and the candidate absorption census as supplied; the census rows are consistent with the patch, which is weak corroboration only.
- The normalized impact TSV and the term inventory. Neither is reproduced. I did not review their every use and make no per-use acceptance.
- Whether WI-601's `adjudicates` cell covers TC-061 as well as LLR-061. The packet does not say.

## Round-002 findings, disposition

| Finding | Status |
|---|---|
| F-1 ownership of SR-144/LLR-152 drift | Applied. The PC turn owns cumulative before/after; WI-601 excluded. |
| F-2 legacy multi-spec close | Applied in LLR-144 and TC-138. Refusal before any report or state change. |
| F-3 assignment refusal anchor | Applied in SR-156 acceptance. LLR-061 parents untouched. |
| F-4 LLR-151 defects | Applied, but the move introduced the trace defect in F-7 below. |
| F-5 SR-148 rationale boundary | Applied. One sentence, precedence claim preserved. |
| F-6 impact TSV normalization | Claimed; not verifiable from the packet. |

## Row-by-row against the supplied chain

| Row | Kind | Verdict |
|---|---|---|
| SR-148 | MEANING | Sound under SN-025/SN-029/SN-027. Precedence, holds, replay and the no-pointer clause unchanged. Rationale addition correctly limits "here and nowhere else" to precedence. |
| SR-156 | MEANING | Sound under SN-027/SN-008/SN-025. See F-9 on the historical-records clause. |
| SR-144 | MEANING (narrowing) | Acceptance now single-item. See F-8 on the missing close-cardinality anchor. |
| LLR-058, LLR-123, TC-058 | CLARITY | Frontier and ordering stay distinct. Correct. |
| LLR-061, TC-061 | MEANING | Truthful single-row completion, prelaunch refusal, no semicolon form. Anchored through SR-156. See F-10 on TC-061 ownership. |
| LLR-149, TC-143 | MEANING | Barrier, adjudication-first partition, human-held stop and delegated single dispatch match the round-002 reading of `_admission`/`_kind_action`. Resume-refusal sentence has no test arm. See F-7. |
| LLR-150, TC-144 | MEANING (narrowing) | Refresh, handback, quarantine, pause and crash-resume contracts intact. Sequential exclusive turns stated honestly. |
| LLR-151, TC-145 | MEANING | Claim refusal before move/commit/worktree is right. TC-145 still asserts a resume refusal the row no longer states. See F-7. |
| LLR-144, TC-138 | MEANING (narrowing) | Sibling close clauses now agree. Cardinality refusal correctly precedes report and state change. |
| LLR-161, TC-156 | MEANING | Rollback and exactly-once disposition preserved. Injected-refusal arm is a genuine gain. |
| LLR-152 | CLARITY | Batch strictest value becomes the single turn's declared bar. Malformed-value refusal and no-product-bar scope retained. |
| TC-154 | CLARITY | Partition tested against a spine WI. Fine. |

No proposed row weakens a hold, changes the policy dial, reorders the adjudication-first partition, or touches a Status, parent, method-kind, evidence, phase or perspective field. SN-025, SN-027 and SN-029 remain satisfiable.

## Findings requiring correction

**F-7 MAJOR. The resume refusal is stated in one row and tested under another.** LLR-149 now carries "the dispatcher resume boundary refuses empty or multi-WI executable assignments", but TC-143's new method has no resume arm. TC-145 still reads "empty and multi-WI claims and resumes refuse before mutation", yet LLR-151 dropped its resume sentence. The result: a design clause with no test, and a test clause with no design anchor, across two SRs. Correction, exact:

- TC-143 method: add "an empty or multi-WI assignment reaching the dispatcher resume boundary refuses before any repository mutation or provider launch" after the delegated-tier clause.
- Either delete "and resumes" from TC-145, or keep it and add to LLR-151 the integrator's own resume site: "_abandoned_claim re-cuts only a crashed claim whose active/<branch>/ holds exactly one spec and refuses otherwise". The second option is preferable because SR-156's acceptance names resume refusal and needs a child under SR-156 to carry it.
- LLR-149 detail: lower-case "The dispatcher resume boundary" after the semicolon. Also note LLR-149's `code_symbol` does not name the resume site; state the enforcing symbol in the sentence or accept that as a known imprecision. Round 002 directed the move, so this is not re-litigation.

**F-10 MAJOR. TC-061 has no stated owner.** The packet excludes LLR-061 from PC intake and assigns it to WI-601, but TC-061 is also in the patch and its new method verifies LLR-061's final text. If WI-601's `adjudicates` does not include TC-061, the PC turn would judge a test whose design row another owner may still return. Correction: one sentence stating either that WI-601 adjudicates TC-061 too, or that the PC turn owns TC-061 with its judgment conditioned on WI-601's outcome on LLR-061. Intake cannot bind cleanly until this is written.

**F-8 MINOR. LLR-144's close-cardinality refusal has no SR anchor.** SR-144's acceptance now says "a refused single-item close restores the report it created" but never says a close of other than one claimed spec is refused. SR-156's refusal list covers claim, assignment and resume, not close. Correction: add to SR-144 acceptance "a close of a branch holding other than one claimed spec is refused before any report or state change". This is a MEANING addition and the PC turn's cumulative ownership already covers the row.

**F-9 MINOR. SR-156's historical-records clause is unverified.** "Historical multi-item records remain readable as evidence and are never reinterpreted as executable single-item claims" appears in acceptance with no child or TC arm. Either move it to the contract prose where the enumeration precondition already lives, or add one arm to TC-145: a historical multi-spec claim commit in trunk history is neither re-claimed nor split by the claim path.

**F-11 CLARITY. LLR-061 detail grammar.** "assembles the worker prompt from ... rework finding (never the generated status surface), the one assigned row with ..." reads as a list continuation with a missing conjunction. Insert "plus" before "the one assigned row". Not blocking.

## Impact inventory, honestly

The ID census remains file and blob membership. It is evidence for impact adjudication and the packet says so. The uses document gives concrete dispositions for the five retired tests, the concurrency design note, WI-605's disjoint scope, the absent TC-205 function and the CSV/resync retention. Those are reasonable proposals, not acceptances. Live uses in runtime-flows, PROCESS_OPTIONS, the interface reference, repo-lock, RESYNC_PACK and the knowledge docs still need per-use dispositions before implementation enablement, which the packet correctly states as a precondition rather than claiming.

The candidate absorption census is consistent with the patch's cell list and shows the pre-existing population riding the three registries. The packet supplies no scoped judgments for those older rows and does not claim to.

## Inherent preconditions versus text flaws

Inherent to publication and deletion, not defects in this text:

- Every absorbed changed cell in the candidate census needs an accepted scoped judgment. This packet supplies none for rows outside its patch.
- WI-601 must run its turn on the final LLR-061 text, including both prior drift and this amendment.
- The supported oldest kit revision is an absent owner input, so CSV conversion and old resync prose stay.
- Live claims and finished-unmerged candidates must be enumerated before any runtime switch.
- The concurrency design note's supersession pointer is post-publication work.

Text flaws are F-7 through F-11.

## Next smallest admissible step

Author a round-004 packet against the same baseline applying F-7, F-8 and F-10 as exact cell text, with F-9 either moved to prose or given its test arm, regenerate the patch and candidate census from the disposable index, and freeze it for independent review. Coordinator stays stopped. No live registry, snapshot, code or test edit.
