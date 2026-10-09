# WI-853 adjudication sitting at 1ccd09d

## amendment

- [MEANING] LLR-069 Detail -> before, an F# exclusion that cites a dispute verdict resolves the finding when it cites an accepted DISMISS for that finding (or the cited ruling id) -> after, it resolves only if, in addition, the findings file beside that verdict records the ruled finding with that F#'s text; otherwise the exclusion is a finding -> not the same. The new text adds an acceptance condition: a finding has to correspond to the one the dispute actually ruled. Code that met the old text would accept a DISMISS of an unrelated finding, or of another round's finding with the same number, and the new text makes that exit 1.
- [MEANING] TC-069 Expected -> before, an F# exclusion citing a FIX, ESCALATE, non-accepted, mismatched or missing dispute verdict exits 1 -> after, an exclusion citing an unrelated finding, another round's finding with the same number, or a finding that can't be shown also exits 1 -> not the same. The test must now check three refusal cases that a test written to the old Expected never ran.

Both rows' new text is coherent and testable, and I would bless it. At 1ccd09d:
- `ruling_problem` refuses in `_correspondence_problem` when the dispute findings file beside the verdict doesn't show the ruled finding as this F#.
- `_finding_key` compares the two texts after removing list markers and severity tags, converting typographic quotes, dashes and arrows to ASCII, and collapsing whitespace. That is a fair reading of "that F#'s text".
- `python -m pytest -q tests/test_plan_coverage.py tests/test_plan_coverage_step.py`: 46 passed. That includes the unrelated-finding, other-round same-id, unshown-finding and typographic-drift cases cited in TC-069's Evidence.

The LLR/TC rung is released, so I re-attest both rows in a separate act commit.

VERDICT: MEANING rows=2

## first-approval

- [APPROVE] SR-236 -> what it requires: when a reviewed change needs rework, the delivered review workflow dispatches the rework only after its plan covers, or excludes with a reason, every finding of the review it answers, each finding being one clause in the order written. An exclusion that rests on a dispute ruling resolves a finding only when an accepted dismissal ruled that same finding. The acceptance is observable: one ordered clause per finding from either input form; dispatch refused while any clause is uncovered and unexcluded; a dismissal of another finding, of another round's same-numbered finding, of a finding that can't be shown, or a non-dismissal ruling is refused. -> what the chain shows: **Up:** it is a labelled DERIVED row under SN-024 (an independent critical eye drives rework). The deriving lens is named in Hat-Refs (UNATTENDED-OPS; the rationale quotes its "green because nothing looked"), the rejected alternative is argued (treating every reasoned exclusion as a resolution), and it is fed back to SN-024's acceptance. That is the same pattern as SR-235 and SR-234, and it matches the parent route dispute verdict 003 called for. **Sideways:** it does not overlap SR-155 (contested-planning rounds), SR-154 (reviewer routing and rework budget), SR-234 (composing and accepting adjudications) or SR-235 (recording attended verdicts). It states the one decision none of them states. **Down:** LLR-069 cites SR-155 and SR-236, and its Detail realises every acceptance clause: the two findings forms through `finding_clauses`, gap findings, and the dismissal-correspondence check. TC-069 verifies SR-236, and its Expected and Evidence cover each acceptance case. The dispatch refusal is the gate's exit 1, tested as `test_an_uncovered_review_finding_refuses_the_dispatch`. -> why it is ready: the requirement can be restated as a closed obligation with a named actor and observable acceptance, and nothing it says goes unverified. One note for later, not a reason to return it: the loop's replan half (WI-805) currently traces to SR-154. When WI-805 adopts the shared step, it should also cite SR-236.

OUTCOME: APPROVE rows=1

SITTING: JUDGED kinds=amendment;first-approval
