# WI-866 — combined adjudication at 09d62f8 (amendment; first-approval, re-sit)

Independent adjudicator, one sitting. I judged the amendment on the before/after
cells given in the brief, against the anchor `docs/archive/last_approved`
(commit 8ab50ddb). For first approval I read LLR-312's chain as given (SR-220,
LLR-210, LLR-264, TC-208, TC-254, TC-260). To check what each TC-254 clause can
observe, I also read the cited tests in `tests/test_consolidate_close.py` and
`consolidate._archive_plan`. I did not use them to work out what the author meant.

The lane answered the first sitting's two points:
- TC-254's Method and Evidence now carry the close's preflight, citing both refused-target tests.
- The link clause now states exactly what its test drives.

One claim introduced by that answer goes further than the Method. It concerns the mint, not LLR-312.

## amendment

- [MEANING] TC-254 Method + Expected -> before: the mint, the absorbing close, the claimed-row refusal, queue-with-edge writing the hard needs edge, and return-to-draft keeping scope, all as acceptance folded into LLR-210 -> after: the same, plus four new things:
  - a close preflight: a later unwritable edge or return target refuses by name and leaves `docs/work` byte-identical;
  - both blockers of a two-edge waiter land;
  - the link case: the linked row moves first, and both links resolve to its draft path, the adjudication link included after its own move to complete;
  - Expected now claims SR-220 through LLR-210 AND LLR-312, including that "the mint and close preflight every affected specification before writing".

  -> not the same: cases were added and the claim widened. The pre-WI-866 close passes the old Method and fails the new one. Both cells carry the change. NOT blessed, for one reason. The Expected cell claims a preflight at the MINT, and no Method clause or Evidence test drives one:
  - The Method's "a cluster row claimed between mint and close refuses the close BY NAME" is the close's refusal (`test_the_close_refuses_by_name_when_an_absorbed_row_was_claimed` calls `close_adjudication`).
  - The new preflight clause is the close's too.
  - The test that does show the mint refusing whole (`test_a_row_claimed_between_close_and_merge_refuses_the_whole_mint`, over `consolidate._archive_plan`) is cited by no TC.

  Everything else in the new text is closed, matches its cited tests, and I would bless it. Returned: WI-866 spec `## Dispositions`, draft 1.

VERDICT: MEANING rows=1

## first-approval

- [APPROVE] LLR-312 -> handback's consolidation close must (a) resolve and validate every affected queued spec before its first write, (b) plan one ordered rewrite sequence per spec so that every blocker named for one waiter lands in its needs, and (c) apply each sequence over the spec as it then stands, so an inbound link redirected by an earlier move survives, re-reading its adjudication spec before composing its terminal text -> UPWARD, SR-220 requires an outcome to take effect only as a recorded restructuring, and LLR-210 already places the edge and return transforms under SR-220, so specifying how handback applies them faithfully is decomposition, not new scope. It matches WI-866's Done-when. SIDEWAYS, LLR-210 keeps the census, parse, refusal, transforms and the mint-time archive; this row owns only the close's application, so no decision is shared. DOWNWARD, each clause now has its own TC-254 Method clause and cited test: (a) the close preflight clause (`test_a_refused_edge_leaves_the_lane_tree_byte_identical`, `test_a_refused_return_leaves_the_lane_tree_byte_identical`); (b) the two-edge waiter (`test_several_edges_on_one_waiter_all_land_in_its_needs`); (c) the link case, including the adjudication spec's link after its own move (`test_a_link_one_close_move_redirects_survives_the_later_writes`). TC-254's one remaining defect is a mint claim that belongs to LLR-210's archive, not to this row -> ready. A closed, observable obligation whose every clause has a verifying case.

OUTCOME: APPROVE rows=1

SITTING: JUDGED kinds=amendment;first-approval
