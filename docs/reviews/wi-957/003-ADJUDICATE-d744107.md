# WI-957 checkpoint sitting at d744107

## first-approval

Four lane-added rows await a first approval: SR-241, LLR-341, TC-371 and TC-372. I read them as one chain, against SN-004 and SN-008 above them, IF-175, IF-288 and IF-289 beside them, the hat roster (`hats.py list`), the lane's arms map, and the cited tests. All ten evidence nodes exist. The chain is close, but it carries three findings in its text and one missing record. The rows are one decomposition, so they go back together.

- [RETURN] SR-241 -> the obligation: when an attended launcher requests a review brief for a lane commit, render it only when that commit, or one beneath it separated only by record changes or none, carries a verified record that the declared review bar and the named test set passed on its tree. Otherwise refuse without a brief, naming the reviewed commit, the cause and the recording step: both digests on a test-set mismatch, both values on a tree or parent mismatch -> what its chain shows: the row is honestly labelled DERIVED. SN-004 and SN-008 ask for trustworthy gate outcomes, not for withholding a review session. Its lens is PERFORMANCE, and that hat's `listens_for` ("a material resource or operating-cost risk left unassessed") names exactly the failure argued: a metered review spent on a tree already known to fail its bar. The Rationale argues the lens and the rejected alternative (running the bar at render) and feeds back to the needs. The Requirement fronts its `When`, speaks of artifact classes, and names no file. Its acceptance criteria are observable conditions with their pass lines. LLR-341 decomposes it -> why it is not ready: §2(c3) requires the decomposition's perspective record beside a derived row, so the adjudicator can run `hats.py record <file> --check` and judge each applicable hat's no-finding. No `*.perspectives.toml` names SR-241 anywhere in the tree, so there is nothing to check. The question that record exists to answer is therefore open: did the hats that apply to a gate trusting a prior record (an integrity or security lens, for instance) each produce nothing, or were they not weighed? The text itself is sound, and once the record exists and checks clean, this finding is answered.
- [RETURN] LLR-341 -> the obligation: resolve the reviewed commit and search it, then its first-parent ancestors while their non-record identities stay equal, without peeling, for one verified review-bar record whose tests digest equals the round's. Refuse on an absent, malformed or unverified record, another bar (landing or no-bar included), another test set, a non-record change, or "the existing walk bound". Report the cause and the compared values, write no brief, and report the attested commit and digest on success. It also requires the coordinator cycle text to state the review-tip precondition and direct lane commits through the attest step -> what its chain shows: the search, its stopping rule, the digest equivalence and each named refusal decompose SR-241 faithfully, and TC-371 drives each of them. The text names no code symbol (the attest step is the CLI verb, a boundary) and has no `shall` -> why it is not ready, two findings:
  - (1) **An unnamed, unverified threshold.** "The existing walk bound produces a refusal" points at a value the row never states, so a reader cannot tell where the refusal falls, and a refactor that changed the bound would keep the row true. No TC arm drives it: neither TC-371's text nor its evidence reaches the bound, and the arms map lists no such row. State the bound (or cite the requirement that owns it) and verify the refusal at it, or drop the arm if the search is meant to be unbounded below the walk's own limit.
  - (2) **A second decision SR-241 does not ask for.** The coordinator-cycle text clause is a documentation obligation on a different shipped artifact, verified by a different TC. SR-241 asks that the refusal name the recording step, which the render's own refusal already does. It does not ask that the skill direct every lane commit through attest. Either argue that clause under SR-241, or give it its own home (a derived row with its own lens, or the cycle skill's existing requirement), so this LLR states one decision.
- [RETURN] TC-371 -> the obligation: drive review rendering on real lane commits through every refusal and the render paths, and through the producer-consumer agreement on a reordered test set -> what its chain shows: every arm map row has a named, existing case. The tree/parent case does assert both values (`for value in values: assert value in err`), and the work-above and record-only contrasts are real -> why it is not ready: its Expected promises "both compared values" only for the another-bar and test-set refusals. It omits the tree-or-parent both-values clause that SR-241's acceptance and LLR-341 both require. The evidence holds an arm the cell does not claim, so a reader of the TC cannot see that obligation verified, and nothing stops the assertion being dropped. It also carries no clause for LLR-341's walk-bound refusal (finding (1) above). Add both to Expected and Method, adjusted to whatever LLR-341's rework keeps.
- [RETURN] TC-372 -> the obligation: read the shipped coordinator cycle and recipes and pin the review-attestation precondition and the recording step in their text -> what its chain shows: its one evidence node exists, and Smoke is an honest tier for a text pin -> why it is not ready: its own text is sound. It verifies SR-241 and LLR-341, though, and finding (2) asks whether the clause it pins belongs to LLR-341 at all. Approving it now would anchor a `Verifies` cell that LLR-341's rework may move. It re-sits with the set, likely unchanged in method.

OUTCOME: RETURN rows=4

## Dispositions answered in the lane (wi-957 D-011)

```toml
title = "WI-957 spine rework: SR-241's perspective record, LLR-341's walk bound and cycle-text clause, TC-371's tree/parent both-values clause; re-sit the four rows"
workstream = "process"
sr_refs = ["SR-241"]
needs = ["WI-957"]
safety_class = "ordinary"
buildtier = "medium"
```

This is spine text, plus one record file. No code change is called for, unless the walk-bound arm is kept and has no test yet.

1. **SR-241:** write its decomposition's perspective record beside the lane's decomposition record (`python project-trajectory/scripts/hats.py record <stem>.perspectives.toml --row SR-241 --row LLR-341 --by <who>`), with a one-line `no_finding` for each applicable hat that produced nothing. It must pass `record <file> --check`.
2. **LLR-341:** replace "the existing walk bound" with the stated bound or the id of the row that owns it. Then either verify the refusal at that bound with a case added to TC-371, or drop the arm.
3. **LLR-341's coordinator-cycle clause:** argue it under SR-241, or move it to its own home and re-point TC-372's `Verifies` to match.
4. **TC-371:** add the tree-or-parent both-values clause, and the walk-bound clause if kept, to Expected and Method.

Then re-sit all four rows together for first approval.

SITTING: JUDGED kinds=first-approval
