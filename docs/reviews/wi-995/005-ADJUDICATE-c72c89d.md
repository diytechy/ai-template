# WI-995 checkpoint sitting 005 (c72c89dd)

This sitting judges the spine change set at c72c89dd: eight approved rows whose
text moved, and nine Drafted rows awaiting a first approval.

What I checked beyond the cells shown:
- The WI-995 spec, its Done-when and Trust ruling, and both round-2 reviews
  (003, 004).
- Every evidence node the new rows cite exists. I grepped each `def`. One name,
  `test_an_empty_set_renders_no_pytest_line_and_says_why`, exists in both
  `tests/test_review_brief.py` and `tests/test_review_brief_git.py`, as TC-333
  and TC-419 respectively cite it.
- `tests/conftest.py` `SLOW_MODULES` lists `test_review_set`,
  `test_review_brief_git`, `test_integrate_attest` and
  `test_agent_loop_review_gate`. `test_review_set_walk` is not listed.
- In `integrate.py`, the shared producer (`_attest_commit`) runs whatever bar
  callable its route hands it. Only the attest route hands it the review bar and
  then the derived files.
- In `review_brief.py`, the render's test lines put the set's notes after the
  test command, or after the no-command line when the set is empty.
- In `review_set.py`, the changed paths are read from the merge base to the
  index on every route, so "staged tree" in LLR-367 is true of the render and
  the draw as well as attest.

I ran no test suite. Both round-2 reviewers ran the lane's suites, and this
sitting rules on text.

The owner's open call (whether `[product] test` must accept the appended
arguments) is not in either section's question and is not ruled here.

## amendment

Every row changes meaning. I would bless six. I would not bless LLR-207 or
TC-333.

- [MEANING+BLESS] LLR-313 Detail -> Round requires its test list, and the review render always fills a test command -> the test-list requirement is gone; an empty derived set is a valid round that renders no test command and states that the row touches no code; listed evidence and reported gaps render beside the test command -> a round the old text refused now renders, and the brief gains lines, so the obligation moved; I would bless it: it carries SR-241's amended non-code permission to the render, adds no name beyond the ones the approved cell already carried, and matches the render code (the notes follow either the command or the no-command line)
- [MEANING] TC-333 Expected+Method -> check that an empty test list refuses (`test_a_round_with_no_tests_refuses`) -> check that an empty derived set renders with no test command and says the row touches no code -> a check that passed the old text fails the new one; NOT blessed: LLR-313's amendment adds a second clause, that listed evidence and reported gaps render beside the test command, and neither TC-333's Expected nor its Method states it. TC-419's Expected says only that the derived set renders. The test that asserts the clause, `test_the_sets_notes_render_beside_its_test_command`, sits in the Evidence cell, but no Expected outcome claims it, so to a reader of the rows the new LLR clause has no verifying case
- [MEANING+BLESS] LLR-344 Detail -> a draw needs any verified review attestation (in practice one for the empty list) -> the attestation must be for the derived test set; a derivation refusal is recorded as a red, draws no round, rebuilds with rework naming the refusal and counts toward the red cap; a closed lane derives through its closed claim copy -> a new comparison, a new source of red and a new input home; I would bless it: it serves SR-154's verdict-obtaining obligation through the existing red route (no new route), TC-418 covers each arm, and its own PERFORMANCE ref still names a failure this row prevents
- [MEANING] LLR-207 Detail -> the attest route reads the review bar and named tests from the lane's declarations -> it derives the set and refuses before the bar when derivation refuses, leaving branch and index unchanged; then "The producer runs the review bar then the derived files, records their digest in the unchanged grammar, and prints the set, listed evidence and reported gaps" -> a new refusal and new output, so the obligation moved; NOT blessed: that sentence's subject is the producer the same cell says "writes every attestation", which includes the station refresh's landing and no-bar attestations (TC-205: "refresh and attest both reach that producer"). Read as written, every refresh runs the review bar and the derived files and prints a set. That is false of the code, where the producer runs whatever bar its route hands it, and it contradicts the cell's own refresh clause. The sentence belongs to the attest route
- [MEANING+BLESS] TC-132 Method -> attest commits after the bar and the named-tests command -> after the review bar and the test command for its derived set -> the input to the test command changes, so a check of the old one fails the new one; I would bless it: it matches the attest-route half of LLR-207, which is correct, and the derivation-refusal arm is TC-417's
- [MEANING+BLESS] SR-241 Requirement+AcceptanceCriteria -> the record must be for the named test set -> it must be for the test set derived from the work item's requirements; a review also refuses when, for code-touching work, derivation reports no requirements, an empty set or a partial set; a non-code change may render with an empty set and reported gaps -> a different set binds the record, and new refusal classes are added; I would bless it: it names no file, its `When` trigger is unchanged, and the code-touching scope answers both round-2 MINORs (003 and 004 each raised it). Its PERFORMANCE rationale still covers it: a metered review is withheld when the process can already name, before dispatch, a tree that does not meet its review obligation, and an incomplete derived set is such a tree. LLR-367 and LLR-341 decompose it
- [MEANING+BLESS] LLR-341 Detail -> compare against the digest of the round's named tests; the refusal names the attest step with the lane and the round's test list -> compare against the derived set's digest; the attest step is named without a test list; a derivation refusal keeps the derivation's text whole and reports the reviewed commit and the attest step -> the comparison input and the refusal text change; I would bless it: TC-419 and TC-371 cover it
- [MEANING+BLESS] TC-371 Expected+Method -> producer and consumer agree on a reordered equivalent test list; a record for another named test set -> they agree on the derived test set; a record for another derived test set -> the check moves from caller-chosen ordering to the derived set; I would bless it. LLR-341's "equivalent spellings and orderings" clause is now held by the shared digest's order-independence cases in TC-205, since no caller hands the render an ordering any more

What the later act turn can reach. The act copies whole registries, so
LLR-207's unblessed drift holds the LLR registry copy and TC-333's holds the
test-case registry copy:
- SR-241 is the only drifted row in its registry, so the act re-attests it.
- LLR-313, LLR-341 and LLR-344 are blessed but stay unanchored until LLR-207 is
  answered.
- TC-132 and TC-371 are blessed but stay unanchored until TC-333 is answered.

### Answered in the lane

```toml
title = "WI-995 spine: LLR-207 gives the review-bar-then-derived-files run to the attest route, and TC-333 states that the derived set's notes render beside its test command"
workstream = "requirements"
buildtier = "quick"
sr_refs = ["SR-156", "SR-146", "SR-154", "SR-235"]
```

Text only. The code and tests already do the right thing. Scope:
(1) In LLR-207's Detail, change the sentence "The producer runs the review bar
then the derived files, records their digest ... and prints the set, listed
evidence and reported gaps" so the attest route owns it, for example "On the
attest route the producer runs the review bar then the derived files ...".
That way it cannot read as the refresh's behaviour, and the cell's
"One producer writes every attestation" clause still holds.
(2) Add to TC-333's Expected: listed non-executable evidence and reported gaps
render beside the test command, or beside the line saying there is none. Add
to its Method's run list `test_the_sets_notes_render_beside_its_test_command`,
which the Evidence cell already cites.
(3) Re-sit both rows for amendment. Their re-attestation releases the LLR and
test-case registry copies that hold the six rows blessed above.

VERDICT: MEANING rows=8

## first-approval

Seven of the nine rows are ready on their text. LLR-367 and TC-414 return.

None of the nine can be flipped in this sitting:
- The test-case registry copy is held by TC-333's unblessed drift, and the LLR
  registry copy by LLR-207's (amendment section).
- TC-413 to TC-420 each verify LLR-367, and a child is approved only after its
  parent.

The approvals below are rulings on merit, so the act turn knows which rows need
no further change. Each still needs its registry copy released and its parent
approved before it can be flipped.

- [RETURN] LLR-367 -> one derivation from the lane's claimed row: scope its SRs, every LLR under them and every TC verifying either; put each TC in one of four classes; return the sorted tagged files, the listed evidence and every gap; refuse for code-touching work that names no SR or has a partial or empty set, and refuse named unreadable inputs; non-code work reports gaps and allows an empty set -> SR-241's amendment calls for it, and TC-413 to TC-420 cover its arms -> not ready: the gap rule leaves the through-its-LLRs arm unstated. The cell says only that "directly verified system requirements have no gap" and that "an unverified system requirement" is a gap. Under this repo's OI-72 ruling an SR's coverage by its children is earned, not assumed, so "unverified" does not settle whether an SR whose only test case verifies one of its LLRs is a gap. The spec's Done-when 3 ("no TC verifies, directly or through its LLRs") and TC-414 say it is not, and round 1 had to pin that arm with a test. As the derivation's one home, this row must say so
- [RETURN] TC-414 -> check gap completeness, no gap for an SR verified only through its LLR, partial outranking empty, and empty only with no tagged file and no gap -> its Expected matches the spec. It is declared Smoke, but two of its four evidence nodes (`test_empty_is_refused_only_with_no_gap_and_no_tagged_file`, `test_partial_names_every_gap_and_outranks_empty`) are in `tests/test_review_set.py`, which `SLOW_MODULES` keeps out of the smoke tier -> not ready: registry-machinery-reference §12.2 names a Smoke TC whose test is absent from the cheap gate as "covered on paper", and TC-205 states the repo's rule that a row's tier is that of its whole cited set. TC-415 already cites both nodes
- [APPROVE] TC-413 -> check in process that the walk includes every scoped TC of any status, classifies each once, returns sorted tagged files with listed non-test evidence, and reports no gap for a directly verified SR -> it covers LLR-367's scope, class and set clauses; every node is in `test_review_set_walk`, which runs at smoke, so the Smoke tier is honest -> ready
- [APPROVE] TC-415 -> check that declared source or tests paths, both ends of a rename included, are code-touching; that a code-touching row naming no SR refuses by name; and that a non-code row allows an empty set and reports gaps -> it covers LLR-367's changed-path decision and the non-code permission in SR-241's amended acceptance; declared Full over a slow module -> ready
- [APPROVE] TC-416 -> check that malformed or unreadable inputs and a tag-reader refusal refuse by name, and that a closed lane reads its closed copy -> it covers LLR-367's input refusals and closed-copy read; the scaffold duplication both round-2 reviews flagged is gone (TC-420 alone holds it) -> ready
- [APPROVE] TC-417 -> check that attest takes no hand list, derives before any bar, runs no bar and keeps branch and index on refusal, runs the review bar then the derived files, records their digest and prints the result -> it covers the attest-route clauses of LLR-207 and LLR-367; it states the attest route correctly and does not repeat the producer sentence I did not bless -> ready
- [APPROVE] TC-418 -> check that an unattended draw compares its record with the derived set, that a derivation refusal takes the existing red route without a round, and that a closed lane derives through its closed copy -> it covers each arm of LLR-344's amendment, including the red-cap count (`test_a_derivation_refusal_counts_toward_the_red_cap`) -> ready
- [APPROVE] TC-419 -> check that the render takes no hand list, renders the derived set, refuses a mismatch naming both digests or a derivation refusal with its text, the reviewed commit and the attest step, and renders an allowed empty set without a test command, saying why -> it covers LLR-341's amendment and LLR-313's empty-set clause. The notes clause is TC-333's to state (amendment section) -> ready
- [APPROVE] TC-420 -> check that a bootstrapped scaffold derives the set from its shipped scripts -> its distinct purpose is the adopter's packaged path, which no other row checks now that TC-416 has dropped it -> ready

Stopping boundary. The chain is SR-241 -> LLR-367 -> TC-413 to TC-420, with
LLR-341 beside LLR-367 under SR-241:
- LLR-367 is the one derivation that attest, the draw and the render all call.
  Splitting the pure walk from the tree read would add no independent decision,
  because the walk has no other consumer.
- LLR-341 keeps a separate decision: how a verified record is searched for and
  compared.
- Each TC holds a distinct verification boundary: scope, classes and set in
  process (413); gap completeness and precedence (414); the code-touching
  decision (415); input refusals and the closed copy (416); the producer (417);
  the unattended draw (418); the attended render (419); scaffold packaging
  (420).
- A further TC would only re-host one of these boundaries' scenarios, and each
  scenario already has its own asserting test.
- The chains SR-154 -> LLR-344 -> TC-418 and SR-156 -> LLR-207 -> TC-417 and
  TC-132 each stop at the one route their LLR changes.

### Answered in the lane

```toml
title = "WI-995 spine: LLR-367 states that an SR verified through its LLRs has no gap, and TC-414's tier matches its cited set"
workstream = "requirements"
buildtier = "quick"
sr_refs = ["SR-241"]
```

Text only. Scope:
(1) In LLR-367's Detail, state the SR gap as "a system requirement that no
scoped test case verifies, directly or through a scoped low-level
requirement". Keep the direct-verification clause, so the cell itself carries
both no-gap arms that TC-413 and TC-414 check.
(2) Choose one fix for TC-414. Either set its Tier to Full, or drop the two
`tests/test_review_set.py` nodes and the lane-case sentence of its Method
(TC-415 already cites both nodes) and keep it at Smoke on the walk module's
gap cases. In the second case, confirm the walk module still asserts that
partial outranks empty.
(3) Re-sit LLR-367 and TC-414 for first approval. Re-sit TC-413, TC-415 to
TC-420 too, so their flips land once LLR-367 is approved and the registry
copies are released by the amendment section's draft.

OUTCOME: RETURN rows=9

SITTING: JUDGED kinds=amendment;first-approval
