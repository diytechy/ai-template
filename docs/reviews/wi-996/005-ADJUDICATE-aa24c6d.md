# WI-996 checkpoint sitting 005 (aa24c6d1)

This sitting judges two kinds of row:
- **Amendments:** two Approved rows whose text the lane moved, SR-156's
  AcceptanceCriteria and LLR-207's Detail.
- **First approvals:** seven new Drafted rows, LLR-368 and TC-421 to TC-426.

What I checked beyond the cells shown:
- The WI-996 spec, its rule table and Done-when, and both round-2 reviews
  (003, 004). The `aa24c6d1` reconcile answered their row-text findings:
  - SR-156's sentence now governs only a test file that remains;
  - LLR-207 keeps only the attest refusal, citing LLR-368;
  - LLR-368 states the review set's test-file rule and its coverage bound in
    its own words, not plan labels;
  - TC-132 is back at its approved text.
- SN-008, which SR-156 already cites, says "a pass verdict never hides a
  skipped check, a stub, or an unmet declared criterion". A strictly marked
  test passes the bar while it is red, so SR-156's new sentence follows from a
  need it already traces to.
- Every evidence node TC-421 to TC-426 cite exists, checked by function
  definition.
- `tests/test_red_mark.py` is not in `tests/conftest.py` `SLOW_MODULES`, so
  the Smoke tier of TC-421 to TC-423 is honest. `tests/test_red_mark_lane.py`
  is slow-only, matching TC-424 to TC-426's Full tier.
- `test_refresh_refuses_a_marked_tree_naming_each_file_and_count` is
  parametrized over both the landing and no-bar refresh arms.

I ran no suites; this sitting rules on text.

## amendment

Both rows change meaning, and I would bless both.

- [MEANING+BLESS] SR-156 AcceptanceCriteria -> the landing gate, lane, pause, close, Done-when and review-gating conditions -> the same, plus: a test held under the declared expected-failure mark is not green; a composed tree holding one is refused; a mark is removed from a test file that remains only against the lane's last review record over the same test set; and an undeclared mark refuses both -> new refusal conditions a seam that met the old acceptance could fail, so the obligation moved; I would bless it. It names no file. It is the "declared bar green" property made honest under SN-008, a need the row already cites, so it needs no new derived-requirement label. It is scoped to a file that remains, as both round-2 reviewers asked, which matches the child's not-judged case for a deleted file. Read literally, it covers only the declared text, so a differently spelled mark falls outside it, as LLR-368's bound states. LLR-368 decomposes it, and TC-424 and TC-425 verify it
- [MEANING+BLESS] LLR-207 Detail -> the attest route's preflight refusals (hooks, primary checkout, dirt, review-bar declaration, label, harness floor, derivation) -> the same, plus: the attest route reads the declared expected-failure mark with the review bar from one parse of the lane's declarations, with no default, and refuses before either bar when either declaration is unavailable or its mark transition is refused under LLR-368 -> a new refusal on the attest route; I would bless it. It adds only the attest route's entry for the new refusal and cites LLR-368 for the rule, so the reference and branch-and-index clauses round 2 flagged as restated now have one home. It adds no carrier name to the cell's text. TC-424 verifies it. Observation, not a finding: LLR-207's TestRefs does not list TC-424, although TC-424's Verifies names LLR-207; the trace's direction of record holds

The SR and LLR rungs are released, and neither registry holds another
unblessed drifted row among those judged here. The later act turn can
re-attest both rows.

VERDICT: MEANING rows=2

## first-approval

All seven rows are ready. LLR-368's parent, SR-156, is Approved. Its
amendment is blessed in this sitting's amendment section, so the act should
re-attest SR-156 before flipping LLR-368 and its test cases.

- [APPROVE] LLR-368 -> one declared, required mark text read with the review bar from one parse, naming key and cause for each unavailable state; counting over the review set's test files in bytes with whitespace removed; a reference that is the newest verified review record in the lane range, or the base; raised counts pass only when the set names the path, and lowered counts on a present path pass only with a same-set record whose set names it; unreadable reads refuse; every refusal comes before the bar and keeps branch and index; the refresh refuses any marked tree on both bars; and the plain-commit, merge-refresh, partial-close, rebase, scaffold and coverage-bound cases are stated -> SR-156's new acceptance sentence calls for it, and TC-421 to TC-426 cover every clause -> ready: its text names no code carrier and holds no `shall`. It states its refusals and its domain, now the review set's test-file rule that the code actually counts, and it gives its inside and outside sets in words. Observation, not a finding: "After a rebase the reference is the new lane base, and earlier marks and attestations are not judged" restates "rebasing changes the base reference". Its "earlier marks" is best read as history before the new base, the reading `test_a_rebase_makes_the_new_base_the_reference` pins; a later spine pass may tighten that sentence
- [APPROVE] TC-421 -> check that a non-empty stripped declaration is accepted, each unavailable state and both-unavailable are named, one parse supplies both values, and the shipped declaration carries its reference text and guidance -> it covers LLR-368's declaration clauses and IF-022's contract; it runs at smoke -> ready
- [APPROVE] TC-422 -> check the test-file domain (relative, no dot-led or `__pycache__` part, a declared suffix, a `.` root) and byte, whitespace-insensitive, non-overlapping counting, and that this repository's landing tree holds no mark -> it covers LLR-368's domain and counting clauses as reconciled; it runs at smoke -> ready
- [APPROVE] TC-423 -> check the reference choice, normalized naming, every count transition, unreadable reads and their refusals -> it covers LLR-368's transition table. Its Expected defers to the LLR's contract, the repository's accepted "satisfies" form, and its eleven named cases each pin one arm -> ready
- [APPROVE] TC-424 -> check that attest refuses every declaration state and invalid transition before its bar and keeps branch and index -> it covers LLR-368's attest arms and LLR-207's new refusal; declared Full over a slow module -> ready
- [APPROVE] TC-425 -> check that each refresh bar refuses each undeclared state and a marked tree, naming files and counts, that a mark-free tree refreshes unchanged, that a refused refresh keeps the work tip, and that a lane refreshes on a merged declaration -> it covers LLR-368's landing arm on both refresh bars -> ready
- [APPROVE] TC-426 -> check plain-commit removal, merge-refresh exclusion, partial-close quarantine, rebase and the bootstrapped scaffold -> it covers LLR-368's lane-history and packaging cases -> ready

Stopping boundary. The chain is SR-156 -> LLR-368 -> TC-421 to TC-426, with
LLR-207 beside it carrying only the attest route's entry for the new refusal:
- LLR-368 is the one mark rule that both the attest arms and the refresh's
  landing arm call. Splitting the declaration, the counting and the
  transitions into separate rows would add no independent decision, because
  each has no consumer but the rule.
- Each TC holds a distinct boundary: the declaration (421); the domain and
  counting (422); reference and transitions in process (423); the attest route
  (424); the refresh route (425); lane history and packaging (426).
- A further TC would only re-host scenarios that already have their own
  asserting tests.

OUTCOME: APPROVE rows=7

SITTING: JUDGED kinds=amendment;first-approval
