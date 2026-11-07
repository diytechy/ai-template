# WI-995 checkpoint sitting 006 (3982d3ce)

This sitting re-judges the WI-995 spine change set after `3982d3ce`, which
answered sitting 005's four returns. That commit changed text only: one cell
each in LLR-207, LLR-367, TC-333 and TC-414, plus a decision entry and the
renamed heading in 005.

The four answers, checked against the cells shown:
- **LLR-207:** the run sentence now opens "On the attest route the producer
  runs the review bar then the derived files…". The cell's "One producer writes
  every attestation" clause still holds for the station refresh's landing and
  no-bar records.
- **TC-333:** its Expected now states that listed non-executable evidence and
  reported gaps render beside the test command, or beside the line saying there
  is none. Its Method now runs `test_the_sets_notes_render_beside_its_test_command`.
- **LLR-367:** a system requirement is a gap only when no scoped test case
  verifies it "directly or through a scoped low-level requirement". The
  direct-verification clause stays.
- **TC-414:** its Tier is now Full, which matches its cited set. Two of its
  nodes are in `tests/test_review_set.py`, which is in `SLOW_MODULES`.

The cited walk nodes `test_an_sr_verified_only_through_its_llr_has_no_gap` and
`test_each_gap_is_named` exist in `tests/test_review_set_walk.py`. I ran no
suites; this sitting rules on text.

The owner's open call (whether `[product] test` must accept the appended
arguments) is still not in either section's question and is not ruled here.

## amendment

Every row changes meaning against the 1189202cf and 889498874 anchors, and I
would bless all eight. Sitting 005 already ruled six of them on the same
text, and their identities are unchanged. The other two are LLR-207 and
TC-333, as answered.

- [MEANING+BLESS] LLR-313 Detail -> Round requires its test list, and the review render always fills a test command -> no test list is required; an empty derived set is a valid round that renders no test command and states that the row touches no code; listed evidence and reported gaps render beside the test command -> a round the old text refused now renders, so the obligation moved; I would bless it: it carries SR-241's non-code permission to the render, adds no new name, and TC-333 and TC-419 now verify every new clause (unchanged since sitting 005)
- [MEANING+BLESS] TC-333 Expected+Method -> check that an empty test list refuses -> check that an empty derived set renders with no test command and says the row touches no code, and that listed evidence and gaps render beside the command or beside the line saying there is none -> a check that passed the old text fails the new one; I would bless it now: sitting 005's finding is answered, because the notes clause LLR-313 adds is stated in the Expected and its test is run in the Method
- [MEANING+BLESS] LLR-344 Detail -> a draw needs any verified review attestation -> it must be for the derived test set; a derivation refusal is a red that draws no round, rebuilds with rework naming the refusal and counts toward the red cap; a closed lane derives through its closed claim copy -> a new comparison, a new source of red and a new input home; I would bless it: it reuses the existing red route, and TC-418 covers each arm (unchanged since sitting 005)
- [MEANING+BLESS] LLR-207 Detail -> the attest route reads the review bar and named tests from the lane's declarations -> it derives the set, refuses before the bar when derivation refuses and leaves branch and index unchanged; on the attest route the producer runs the review bar then the derived files, records their digest and prints the set, listed evidence and gaps -> a new refusal and new output; I would bless it now: the run sentence belongs to the attest route, so it no longer claims the refresh runs the review bar, and that matches the code, where the shared producer runs whatever bar its route hands it
- [MEANING+BLESS] TC-132 Method -> attest after the bar and the named-tests command -> after the review bar and the test command for its derived set -> the test command's input changes; I would bless it: it matches LLR-207's attest route, and the derivation-refusal arm is TC-417's (unchanged since sitting 005)
- [MEANING+BLESS] SR-241 Requirement+AcceptanceCriteria -> the record must be for the named test set -> it must be for the test set derived from the work item's requirements; a review also refuses when, for code-touching work, derivation reports no requirements, an empty set or a partial set; a non-code change may render with an empty set and reported gaps -> a different set binds the record and refusal classes are added; I would bless it: it names no file, its `When` trigger is unchanged, the refusals are scoped to code-touching work, and its PERFORMANCE rationale covers withholding a metered review over an incomplete set (unchanged since sitting 005)
- [MEANING+BLESS] LLR-341 Detail -> compare against the round's named-tests digest; the refusal names the attest step with a test list -> compare against the derived set's digest; the attest step is named without a test list; a derivation refusal keeps its text whole and reports the reviewed commit and the attest step -> the comparison input and the refusal text change; I would bless it: TC-419 and TC-371 cover it (unchanged since sitting 005)
- [MEANING+BLESS] TC-371 Expected+Method -> producer and consumer agree on a reordered equivalent test list; a record for another named set -> they agree on the derived set; a record for another derived set -> the check moves to the derived set; I would bless it. LLR-341's ordering-equivalence clause is held by the shared digest's order-independence cases in TC-205 (unchanged since sitting 005)

No unblessed drifted row is left in any of the three registries, so the later
act turn can re-attest all eight rows and copy the SR, LLR and test-case
registries.

VERDICT: MEANING rows=8

## first-approval

All nine rows are ready:
- LLR-367 and TC-414 were returned at sitting 005 and are answered.
- The other seven were ready on merit at sitting 005, and their text is
  unchanged.

Every parent is either Approved or approved in this same sitting. The later
act should flip LLR-367 before, or together with, the test cases that verify
it.

- [APPROVE] LLR-367 -> one derivation from the lane's claimed row: scope its SRs, every LLR under them and every TC verifying either; put each TC in one of four classes; return the sorted tagged files, the listed evidence and every gap (an SR no scoped TC verifies directly or through a scoped LLR, an unverified LLR, an untagged executable TC, a TC with no evidence); refuse code-touching work naming no SR or with a partial or empty set, and refuse named unreadable inputs; non-code work reports gaps and allows an empty set -> SR-241's amendment calls for it, and TC-413 to TC-420 cover its arms -> ready: the through-its-LLRs arm is now stated, matching TC-414 and the spec's Done-when 3. It names no code carrier, holds no `shall`, earns no own Hat-Refs, and states its coverage bound
- [APPROVE] TC-413 -> check in process the scope, the one-class rule, the sorted tagged files with listed non-test evidence, and no gap for a directly verified SR -> it covers LLR-367's scope, class and set clauses; every node runs at smoke -> ready (unchanged since sitting 005)
- [APPROVE] TC-414 -> check that every gap is named, an SR verified only through its LLR has no gap, partial outranks empty, and empty applies only with no tagged file and no gap -> it covers LLR-367's gap and precedence clauses, now stated in the LLR -> ready: its Full tier now matches its cited set, which includes the slow `test_review_set` module
- [APPROVE] TC-415 -> check that declared source or tests paths, both ends of a rename included, are code-touching; that a code-touching row naming no SR refuses; and that a non-code row allows an empty set and reports gaps -> it covers LLR-367's changed-path decision and SR-241's non-code permission -> ready (unchanged since sitting 005)
- [APPROVE] TC-416 -> check that malformed or unreadable inputs and a tag-reader refusal refuse by name, and that a closed lane reads its closed copy -> it covers LLR-367's input refusals and closed-copy read, with no scaffold duplication -> ready (unchanged since sitting 005)
- [APPROVE] TC-417 -> check that attest takes no hand list, derives before any bar, runs no bar and keeps branch and index on refusal, runs the review bar then derived files, records their digest and prints the result -> it covers LLR-207's attest-route clauses, as now worded, and LLR-367's attestation route -> ready (unchanged since sitting 005)
- [APPROVE] TC-418 -> check that an unattended draw compares against the derived set, that a derivation refusal takes the existing red route without a round and counts toward the cap, and that a closed lane derives through its closed copy -> it covers each arm of LLR-344's amendment -> ready (unchanged since sitting 005)
- [APPROVE] TC-419 -> check that the render takes no hand list, renders the derived set, refuses a mismatch naming both digests or a derivation refusal with its text, the reviewed commit and the attest step, and renders an allowed empty set without a command, saying why -> it covers LLR-341's amendment and LLR-313's empty-set clause; the notes clause is TC-333's -> ready (unchanged since sitting 005)
- [APPROVE] TC-420 -> check that a bootstrapped scaffold derives the set from its shipped scripts -> it is the only row checking the adopter's packaged path -> ready (unchanged since sitting 005)

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

OUTCOME: APPROVE rows=9

SITTING: JUDGED kinds=amendment;first-approval
