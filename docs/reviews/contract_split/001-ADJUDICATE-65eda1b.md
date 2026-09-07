# ADJUDICATE — WI-605 — amendment at 65eda1b (primary turn WI-605-b830f202c551c7c11d1a63ea4baff84a7ff6e596)

Question judged, per scoped row, and the only one: did the amendment change the
requirement's MEANING, or only its CLARITY? Scope is the turn binding's three
rows — SR-161, LLR-183, TC-178 — and nothing else is ruled on here.

## Bindings verified independently

Every binding in the turn record was re-derived from the checkout rather than
taken on trust: HEAD is `65eda1bff8ec37a2594f2d205e12569df350663d` (base
`b830f202` is its first parent); `git hash-object` on the three live registries,
their three `docs/archive/last_approved/` copies and the queued spec reproduces
every blob the binding names. Both sides of each registry were loaded as TOML
and every key of every row diffed. The diff agrees with the derived census on
every approved-change and rider row, and additionally shows the traced-only
movement the census correctly omits (`module` on 30 LLR rows and `code_symbol`
on LLR-160; `Module`/`CodeSymbol` are declared traced in
`acceptance_record.SPINE_TRACED_CELLS`, so they are outside the drift basis
and owe no judgment, though a whole-file copy would carry them).

The migration record `docs/reviews/2026-09-07-WI-605-supervisor-migration.md`
was read first. Nothing from the preserved lane, its round files or the two
handback patches is relied on below; every claim is re-derived.

## The owner ruling this amendment applies

The SR-161 Rationale cites `docs/log.d/2026-09-06-sn036-owner-ruling.md`. No
such path exists in the tree at HEAD (`docs/log.d/` holds only
`2026-09-06-snapshot-ownership-gaps.md` for that date). The ruling itself is
real and was read: `docs/log.md` heading
"2026-09-06 — SN-036 / SR-161 owner ruling: review pass, not a guard", whose
acts 2 and 3 are exactly the SR-161 re-point (brief injects every applicable
hat's question; the sitting's review record is the perspective record;
`hat_refs` stays provenance; Verification becomes Inspection of one real
review record) and the LLR-183 NOT-DISCHARGED closure. The approved SN-036
acceptance (byte-identical live and snapshot) already reads "Each decomposition
round is reviewed against every applicable declared perspective, and the review
record names each perspective and its outcome." The amended SR-161 restates
that need one tier down; the amended meaning is coherent with its parent.

## Per-row judgment

- [MEANING] SR-161 Requirement -> deliver, with every decomposition, a machine-readable record holding each declared perspective's applicability decision and the requirements or explicit no-finding it produced, such that an applicable perspective missing from the record is a reportable finding -> when a decomposition round is reviewed, put every applicable declared perspective's question in the decomposition brief and require the sitting's review record to name each perspective's outcome -> the artifact (a machine-readable record with a reportable-finding check) is replaced by two different artifacts (brief content plus a review record), the finding class is dropped, and the trigger moves from "every decomposition produced" to "when a round is reviewed"; a correct build of the old text (record file plus checker) satisfies none of the new clauses, and a correct build of the new text fails the old on both the record and the reportable finding.
- [MEANING] SR-161 AcceptanceCriteria -> a record written beside the artifacts; a missing applicable perspective reported; NOT-APPLICABLE distinguished from CONSIDERED-WITH-NO-FINDING; the adequacy review reads the record, not the transcript -> applicable perspectives resolve from the hats roster; the brief presents each applicable question; the review record names an outcome for every one; the adequacy review reads that record -> the reportable-missing-perspective condition and the not-applicable/no-finding distinction are gone and the roster-resolution condition is new; the acceptance test a reviewer runs is a different test.
- [MEANING] SR-161 Verification -> Test -> Inspection -> the verification method is itself an acceptance condition; the row's evidence moves from an automated unit case (TC-178) to a document Inspection (TC-211, Drafted, whose 2026-09-06 PASS result is recorded in docs/test/inspection-procedures.md).
- [MEANING] SR-161 Rationale -> realizes SN-036; the roster is the inventory; the record proves coverage and provenance -> the roster and plan briefs already supply the questions and the review record preserves outcomes; a separate machine-readable record and checker would duplicate the review; Hat-Refs remain row-level provenance; applies the owner ruling of 2026-09-06 -> carried by the row's change rather than carrying it, but NOT blessable as shown: the closing sentence cites `docs/log.d/2026-09-06-sn036-owner-ruling.md`, a path that does not exist, and a dated ruling citation is a record citation of the kind an approved cell must not depend on; the ruling's real home is the docs/log.md heading named above. Cell RETURNED for a citation correction (Disposition 1).
- [MEANING] LLR-183 Detail -> the machine-readable half of the perspective record; NOT DISCHARGED debt stated explicitly: the parent asks for a record distinguishing not-applicable from no-finding, this cell expresses neither, and the no-finding half needs a per-decomposition artifact that does not exist -> the row-level provenance part of perspective review; per-decomposition coverage is discharged by the existing review path (roster predicates, brief questions, review-record outcomes); Hat-Refs keep the narrower role of naming the hats that raised a row -> the design row's claim about what the parent still owes changed from "a per-decomposition artifact is owed and absent" to "nothing further is owed; the review path discharges it", and the cell's own role narrowed from half of a record to provenance; a reader of the old text owed a future artifact and a reader of the new owes none. The mechanics sentences (load_hat_names, hat_findings severity split, effective_hats union, TRACED classification) are byte-for-byte unchanged and the nine TC-178 test functions they cite all exist in tests/test_trace_hats.py. The cell reads coherent against the amended SR-161 and against the recorded TC-211 Inspection; that observation is evidence only and accepts nothing, because the registry it sits in cannot be published (below).
- [MEANING] TC-178 Expected -> "Satisfies the acceptance folded into LLR-183 (parent SR-161)": the unit evidence is offered as SR-161's Test verification -> "Satisfies LLR-183's Hat-Refs provenance, name-resolution, severity and effective-set mechanics; SR-161's perspective-review acceptance is inspected by TC-211" -> the claim narrowed: this case no longer offers itself as satisfying SR-161's acceptance and names the Inspection case that does. That is a changed verification claim, which is the parent-satisfaction wording the assignment asked to be judged against the new Inspection method; the answer is that the Unit evidence is correctly NOT treated as the perspective-review Inspection. Retention of `Verifies = [SR-161, LLR-183]` is judged acceptable as supplementary traceability and only because the Expected text now says so in words: Hat-Refs provenance survives in SR-161's amended Rationale ("Hat-Refs remain the row-level provenance"), LLR-183 is still SR-161's child, and removing SR-161 from Verifies would be a routed traced-cell change owing its own adjudication for no gain. The weakness is recorded rather than hidden: provenance is in SR-161's Rationale, not its Requirement, so the direct link rests on the child chain; and until TC-211 is approved (WI-606, which needs WI-605) the Approved SR-161 has no Approved carrier for its Inspection method. Neither point blocks this row; both belong to the reanchor and to WI-606.

## Why the turn is RETURN with zero accepted cells

A snapshot for any of the three registries would absorb Approved cells that no
completed judgment covers, and one scoped cell (SR-161 Rationale) is not
blessable as shown. The absorption population, re-read at execution:

- `docs/requirements/system-requirements.toml`: 17 Rationale cells (SR-024,
  SR-033, SR-043, SR-052, SR-053, SR-054, SR-111, SR-112, SR-129, SR-144,
  SR-146, SR-147, SR-149, SR-167, SR-175, SR-176, SR-177) are byte-identical
  to the text WI-547 judged CLARITY at reviewed commit fb0ed7c (verdict
  committed at 6162a3424255e7a053f0590f59fbf9be94599740; WI-593 concurred at
  ce072f72a5688f5d643b40fb9baa0df3078f8a6e). Whether those count as accepted
  judgments for a whole-file copy is the reanchor's question, not this turn's.
  SR-162 Rationale is UNJUDGED: the clause "and no SR states it yet" was
  dropped at sitting commit 77612fb2 with no adjudication minted (a sitting
  commit lands on trunk without the merge-side mint), and no queued WI names
  it; note that the SR it now leaves unstated is SR-185, still Drafted.
  SR-183–SR-186 are Drafted riders and stay Drafted.
- `docs/requirements/low-level-requirements.toml`: LLR-061 is owned by WI-601
  and LLR-167 by WI-603, both still queued — neither has a completed judgment
  to cite. LLR-140, LLR-152, LLR-153, LLR-154, LLR-158 and LLR-207 Detail
  (with CodeSymbol/Module) first appear at sitting commit 0f106ce9 and are
  UNJUDGED with no owner WI; the spec's ledger predates that commit and does
  not list them. LLR-210 is WI-604's Drafted rider.
- `docs/test/test-cases.toml`: TC-146, TC-147, TC-148, TC-153, TC-161 and
  TC-205 Method first appear at 0f106ce9 and are UNJUDGED with no owner WI.
  TC-208 (WI-604) and TC-209–TC-211 (WI-606) are Drafted riders.

No prior whole-chain judgment covering the exact live text exists for SR-162
or for the twelve 0f106ce9 LLR/TC cells; WI-605 does not acquire those scopes.
Each scoped decision is therefore `return`; no Status moves, no snapshot is
written, the prior anchors stay intact, and WI-601, WI-603, WI-604 and WI-606
keep their scopes untouched.

## Impact observations for the later MEANING reanchor (evidence only)

- LLR-202 (SR-Refs SR-161) and TC-198 (Verifies SR-161, LLR-202) are the
  Hat-Refs amendment guard; they decompose the provenance role SR-161's
  amended Rationale keeps, not the amended Requirement text. Retain; no cell
  change is needed, but the reanchor should say so.
- `project-trajectory/scripts/acceptance_record.py` ("Implements: SR-161,
  LLR-202") and `bootstrap.py` (the hats roster scaffold labelled SR-161)
  reference the provenance mechanics and the roster, both of which survive.
  Retain.
- `docs/test/inspection-procedures.md` already carries the revised procedure
  and TC-211's PASS result; `tests/test_trace_hats.py` is unchanged and
  matches TC-178's Evidence.

VERDICT: MEANING rows=3
