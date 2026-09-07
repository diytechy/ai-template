**OUTCOME: RETURN** for authoring/intake readiness. The design is sound under its parents and most rows are correct, but three text defects and one unresolved ownership precondition must be fixed before this can enter intake.

**Deletion / publication decision: NOT AUTHORIZED.** No code deletion, no snapshot copy, no Status movement follows from this review. See the last section.

## Row-by-row verdict

| Row | Class | Verdict | Note |
|---|---|---|---|
| SR-148 req + AC | MEANING | accept with MINOR | Cardinality clause fits under SN-025/SN-027. "Exactly one work item for each assignment an unattended run admits from the repository's tracked registries" reads as if the registries are the source of the count; reorder so "from the registries" binds to "select". |
| SR-156 req + AC | MEANING | accept | "Historical multi-item records ... never reinterpreted" is the right guard. Consistent with SN-027 ceiling. |
| SR-144 AC | MEANING | accept with MEDIUM | Narrowing to single-item close is fine. Sibling LLR-144 and TC-138 still say "moves each claimed spec" and "restores every report the call wrote" and are neither amended nor dispositioned in the census. |
| LLR-058 title | CLARITY | accept | Title had duplicated LLR-123's split. Detail unchanged. |
| LLR-123 detail + rationale | MEANING | accept | Tie-break moves from "first WI id" of a traincar to the WI id. Identical for singletons, so no ordering change on live data. |
| TC-058 | CLARITY | accept | |
| LLR-061 detail | MEANING | accept text; BLOCKED on ownership | Correct single-row brief and refusal of empty/semicolon input. See ownership section. |
| TC-061 | MEANING | accept | Refusal before provider launch is the right observable. |
| LLR-149 detail | MEANING | **MAJOR** | Two defects. (1) "first dispatchable spine row" lets admission skip a human-held first row, contradicting SR-148's "nothing admitted past a human-held stop". Replace with "the first spine row in LLR-123's order; if that row is human-held, admission stops there". (2) The old text stated what happens to attestation/gate rows that are NOT human-held. The new text only states the held arm. The released-tier dispatch of those rows is now stated nowhere. |
| TC-143 | MEANING | fix with LLR-149 | Drops "ahead of ordinary work" and the released-tier arm. Add both. |
| LLR-150 detail | CLARITY | accept | |
| TC-144 | MEANING | accept with MEDIUM | "Ordinary work waits until the exclusive barrier clears" means ordinary lanes idle for the whole spine chain, N windows instead of one. That is a real fan-out reduction under SN-027 and an ordering change. It is owner-authorized, but the packet says "not a retirement of parallel work" without naming this cost. State it. |
| LLR-151 detail + rationale | MEANING | **MAJOR** | The "upgrading a station ... is refused until reconciled under the prior contract" clause mints a migration-window obligation. SR-156 has no such clause, and the packet itself says no supported-version boundary exists. Remove it from the spine and keep it where the packet already puts it: the implementation WI's precondition. Rationale also silently drops the deleted trade-off ("N spine changes cost one re-attest window"); record that the owner accepted N windows. |
| TC-145 | MEANING | fix with LLR-151 | Delete the "blocks upgrade" arm. Keep the refusal-before-mutation arm. |
| TC-154 | CLARITY | accept | |
| LLR-161 detail | MEANING | accept | Consistent with amended SR-144. |
| TC-156 | MEANING | accept | Injected post-report refusal is the right probe. |

Dishonest equivalence check: the packet frames the old batch prose as describing "retired single-approve behavior". That is true of the attested/gate arm only. The batch admission itself is live LLR-149 mechanism, not retired text. Say so plainly.

Duplication check: SR-148 and SR-156 each now carry a one-item clause. Admission and claim are different stages with different children, so I accept this, but SR-148's rationale still says the selection invariant is stated "here and nowhere else". MINOR.

## Missing or excessive changes and census gaps

- **LLR-144 / TC-138 omitted.** Both sit under SR-144 and describe multi-spec close. Amend or record an explicit retained-unchanged disposition with the degenerate-singleton reasoning. MEDIUM.
- **docs/concurrency-v2.md is absent from the impact inventory.** LLR-149 and LLR-151 cite its §A4/§A8 for the batch rule. The census is keyed on IDs, so a document the cells cite by section escaped it. Confirm whether it is live and whether §A8 still describes batch admission. MEDIUM.
- **The ID-keyed census is necessary, not sufficient.** It misses term uses: "traincar", "train", "batch", the semicolon list form, and test names such as TC-205's `test_a_two_row_batch_close_peels_under_one_canonical_order`. That test is a retained obligation, because historical two-row closes exist in this repo and the verdict walk must still peel them. Name it in the obligation map so an implementer does not delete it as "batch". A term census is owed before implementation. MEDIUM.
- **LLR-152 retains "the batch's strictest value".** Not in scope, but it must be read at impact review since it has its own pending Detail change.
- **File/blob membership is not per-use acceptance.** The two treatment classes are a filing scheme. Generated files in the "review use" class regenerate rather than get reviewed. Nothing in the TSV records that any live use was judged.

Excess: none. The patch stays inside the ten rows and touches no Status, parent, phase or evidence field. The `"""` to `"` delimiter change is cosmetic; I could not run the TOML parse and take the author's claim as unverified.

## Ownership, holds and publication preconditions

**LLR-061 ownership is unresolved and blocks intake.** The live baseline already carries an unpublished LLR-061 Detail change riding WI-601's queued adjudication. This patch stacks a second change on that live text. The packet names two admissible resolutions but picks neither. A recorded disposition must exist before the candidate is authored, or WI-601 must absorb the final text. WI-605 also cites LLR-061, SR-144, SR-148 and TC-061 from a queued spec and two handback patches, and the packet's ownership section does not mention it at all. Confirm WI-605's scope is disjoint. **UNCERTAIN on WI-605; inputs do not show its scope.**

Holds: the patch changes no dial and no hold. The ordering change is the serialized spine chain described above.

Inherent external preconditions, not text flaws: the 40 plus rows in the absorption census need their own accepted scoped judgments; the census must be regenerated after the patch; primary whole-chain adjudication must run under exclusive ownership. None of this is supplied by PC authorization or by this review, and this review does not approve any older cell.

**Deletion/publication decision: NOT AUTHORIZED.** A semantic opinion on the proposal is not authority to apply the amendment, publish a snapshot, or delete `train` assembly, the multi-WI walk, or the batch claim path. Those wait on: accepted amendment through intake, publication with complete whole-file absorption, a single-WI implementation WI with the retired-test-to-obligation map, and the live-claim enumeration the packet already requires.

## Next smallest admissible step

The author revises the patch text only: fix LLR-149/TC-143 wording, strip the upgrade clause from LLR-151/TC-145, add the LLR-144/TC-138 disposition, add docs/concurrency-v2.md and a term census to the inventory, and record the accepted N-window cost in LLR-151's rationale. In the same revision, write the LLR-061 ownership disposition naming WI-601 and confirming WI-605's scope. Then redraw this adjudication against that revised packet. Coordinator stays stopped throughout.
