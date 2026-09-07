**Before starting:** this is a read-only adjudication of the frozen round-002 packet. No tools, no file writes, no live-state claims.

# PC batch-contract proposal, round 002 review

**OUTCOME: RETURN** (narrow). The design direction is accepted and should not be re-litigated in round 003. Two material gaps and four small text defects need exact fixes before the packet is fit for authoring and intake.

**Deletion/publication decision: NOT AUTHORIZED.** Nothing in this review permits applying the patch to a live registry, writing any snapshot, or deleting batch code or tests. That holds even after the corrections below land, for the preconditions listed at the end.

## What I could not verify

- The author's claims that the patch parses as TOML, changes only the listed cells, and leaves Status, parent and traced fields untouched. I judged the diff text as supplied.
- Whether the semicolon `--wi` form has documentary callers outside the ID inventory (AGENTS template, skills, resync prose). The term inventory is linked, not reproduced.
- Whether intake dedupes a new amendment onto an open adjudication row for the same cell. The LLR-061 ownership decision depends on this.

## Row-by-row against the supplied chain

| Row | Kind | Verdict |
|---|---|---|
| SR-148 | MEANING | Sound under SN-025/SN-029. Selection precedence, holds and replay unchanged. See note on overlap with SR-156 below. |
| SR-156 | MEANING | Sound under SN-027/SN-008/SN-025. Add "assignment" to the refusal clause (see LLR-061). |
| SR-144 | MEANING (narrowing) | Rides an unowned baseline Rationale drift (absorption census). Ownership must be stated. |
| LLR-058, LLR-123, TC-058 | CLARITY | Frontier and ordering stay distinct decisions. LLR-123's Rationale rewrite is an approved-cell edit and is correctly in scope. |
| LLR-061, TC-061 | MEANING | Truthful single-row completion predicate, prelaunch refusal. Parent SR-026 says nothing about cardinality, so the refusal clause has no SR anchor. |
| LLR-149, TC-143 | MEANING | Matches current `_admission` and `_kind_action`: spine dispatches on either tier, held attestation/gate rows surface including at the `keep_nondependent` close, delegated rows dispatch singly and exclusively. The round-001 held-spine suggestion is correctly not adopted. |
| LLR-150, TC-144 | MEANING (narrowing) | Refresh, handback, quarantine and pause contracts intact. |
| LLR-151, TC-145 | MEANING | Design sound. Two text defects (below). |
| LLR-161, TC-156 | MEANING | Rollback and exactly-once disposition preserved; injected-refusal arm is a real test gain. Shares the legacy-branch gap with LLR-144. |
| LLR-144, TC-138 | MEANING (narrowing) | Siblings now agree on one spec and one rollback guarantee. Same gap. |
| LLR-152 | CLARITY, pending code check | "Single turn's declared value" is what a per-WI primary turn implies. Rides an unowned baseline Detail drift. |
| TC-154 | CLARITY | Partition tested against a spine WI. Fine. |

No proposed row weakens a hold, changes the policy dial, or reorders the adjudication-first partition. SN-025, SN-027 and SN-029 remain satisfiable by the amended text.

## Findings requiring correction

**F-1 MAJOR. Ownership is settled for LLR-061 only.** The absorption census shows SR-144 (`Rationale`) and LLR-152 (`Detail`) already in `approved-change` at baseline. The patch edits both rows. The contract names WI-601 for LLR-061 and is silent on who owns these two pre-existing drifts. An amendment turn on SR-144 or LLR-152 will bind the whole row, including drift nobody has judged. Correction: add an ownership paragraph naming the owner of each, or stating there is none and that the PC amendment turn must judge the cumulative before/after under the same exclusion rule applied to LLR-061.

**F-2 MAJOR. A legacy multi-spec branch has no stated close path.** LLR-144 and LLR-161 now say "the one claimed spec". A branch whose `active/<branch>/` holds two specs at switch time would close one and leave the other, and `finished_branches` would never fire. That is the strand SR-144 exists to dissolve. The packet's "enumerate and hold the switch" precondition is sound but lives only in proposal prose. Correction: one clause in LLR-144 or LLR-161: `close_partial` refuses, before writing any report, a branch whose active directory holds other than one spec. Optionally mirror it in TC-138 as a named refusal.

**F-3 MINOR. LLR-061's refusal clause has no SR anchor.** SR-026 covers headless resume, not cardinality. Cheapest fix: SR-156's acceptance reads "empty or multi-item claim, assignment and resume inputs refuse". Do not add SR-156 to LLR-061's parents; that is a traced-cell change and WI-601 would have to absorb it.

**F-4 MINOR. LLR-151 text defects.** The detail contains `provider call.; and integrate()`, a byte-level defect in a cell offered as exact. The rationale cites "The PC design", a plan-package name that no future reader of the cell can resolve. Replace with "This single-WI contract". The resume-refusal sentence sits in the integrator's row while resume is the dispatcher's boundary; either name the integrate symbol that refuses or move the sentence to LLR-149.

**F-5 MINOR. SR-148 and SR-156 both state a singleton invariant.** The contract's distinction (admission versus executable claim) is defensible, and SR-148's rationale guards precedence only. Record the distinction in SR-148's rationale in one sentence so the "here and nowhere else" clause cannot be read as claiming cardinality.

**F-6 MINOR. Impact inventory labeling is inconsistent.** Most rows use long treatment phrases; LLR-144, LLR-152 and TC-138 use short labels. Normalize before the candidate is bound. Substantively, live hits in `docs/runtime-flows.md`, `PROCESS_OPTIONS.md`, `docs/interface-reference.md`, `docs/repo-lock.md`, `RESYNC_PACK.md` and the knowledge docs have no per-use disposition. That is acceptable for contract authoring but blocks implementation enablement.

## Impact inventory, honestly

The TSV is file and blob membership. It is not per-use acceptance and the packet says so. The uses document supplies concrete dispositions for the five retired tests, the concurrency design note, WI-605's disjoint scope and the CSV/resync retention. Those are reasonable proposals. The TC-205 handling is correct: the cited function is absent at baseline, PC deletes nothing there, and the stale citation belongs to the primary-publication migration scope, not this one.

## Inherent preconditions versus text flaws

Inherent to publication, not defects in the proposal:

- Every absorbed changed cell in the three registries needs an accepted scoped judgment; this packet supplies none for the older rows.
- WI-601 must run its turn on the final LLR-061 text.
- The supported oldest kit revision is an owner input still absent, so CSV conversion and old resync prose stay.
- Live claims and finished-unmerged candidates must be enumerated before any runtime switch.

Flaws in the text are F-1 through F-6 above.

## Next smallest admissible step

Author a round-003 packet against the same baseline with F-1, F-2, F-3 and F-4 applied as exact cell text, regenerate the patch and absorption census from the disposable copy, and freeze it for independent review. Coordinator stays stopped. No live registry, snapshot, code or test edit.
