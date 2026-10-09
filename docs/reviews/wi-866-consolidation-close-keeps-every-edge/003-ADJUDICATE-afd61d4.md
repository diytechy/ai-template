# WI-866 — combined adjudication at afd61d4 (amendment, second re-sit)

Independent adjudicator, one sitting. I judged the amendment on the before/after
cells given in the brief, against the anchor `docs/archive/last_approved`
(commit 8ab50ddb). To check that the one new Method clause describes what its
cited test asserts, I read
`tests/test_consolidate_close.py::test_a_row_claimed_between_close_and_merge_refuses_the_whole_mint`.
It passes as built (`1 passed, 15 deselected in 4.87s`), but a passing test is
not what I am judging here.

The re-sit's one finding was that Expected claimed a preflight at the MINT that no Method clause drove. The lane answered it by adding the clause and citing the mint's whole-refusal test. Every other new clause was judged blessable in that re-sit and is unchanged.

## amendment

- [MEANING] TC-254 Method + Expected -> before: the mint, the absorbing close, the claimed-row refusal at the close, queue-with-edge writing the hard needs edge, and return-to-draft keeping scope, all as acceptance folded into LLR-210 -> after: the same, plus five new things:
  - the successor mint refuses whole when a hand claim lands between the close and the merge (names the row, archives nothing, leaves the other absorbed rows queued);
  - the close preflight: a later unwritable edge or return target refuses by name and leaves `docs/work` byte-identical;
  - both blockers of a two-edge waiter land;
  - the link case: the linked row moves first, and both links resolve to its draft path, the adjudication link included after its own move to complete;
  - Expected now claims SR-220 through LLR-210 and LLR-312, with the mint and the close each preflighting before writing.

  -> not the same: cases were added and the claimed parent set widened. The pre-WI-866 close passes the old Method and fails the new one. Both cells carry the change. BLESSED:
  - Each Method clause now names an observable result, and a cited test drives each one.
  - The new mint clause matches its test, which asserts that the refusal names WI-402, that nothing is minted, that WI-401 and WI-403 stay queued, and that the restructured folder stays empty.
  - The Expected cell's two preflights are each driven: the mint's by that clause, the close's by the two refused-target clauses.
  - LLR-312's three clauses each map to a Method clause, and LLR-210's mint-time archive is covered without its census guards being restated.

  Re-attested by this sitting.

VERDICT: MEANING rows=1

SITTING: JUDGED kinds=amendment
