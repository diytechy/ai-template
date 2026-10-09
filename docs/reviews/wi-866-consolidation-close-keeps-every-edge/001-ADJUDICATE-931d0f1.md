# WI-866 — combined adjudication at 931d0f1 (amendment; first-approval)

Independent adjudicator, one sitting. I judged the amendment on the before/after
cells given in the brief, against the anchor `docs/archive/last_approved`
(commit 8ab50ddb). For first approval I read LLR-312's chain (SR-220, LLR-210,
LLR-264, TC-208, TC-254, TC-260) and WI-866's Done-when. To check what TC-254
can observe, I also read `handback._enact_plan` / `_apply_plan` /
`_archive_one_adjudication_row` and `tests/test_consolidate_close.py`. I did not
use them to work out what the author meant. The four tests at issue pass as built
(`4 passed, 12 deselected in 29.80s`), but a passing test is not what I am judging here.

## amendment

- [MEANING] TC-254 Method + Expected -> before: the mint, the absorbing close, the claimed-row refusal, queue-with-edge writing the hard needs edge, and return-to-draft keeping scope, all as acceptance folded into LLR-210 -> after: the same, plus two new cases. A verdict naming two edges on one waiter leaves both blockers in its needs, and when returned specs and the adjudication spec link a returned row, every link ends at its draft path. Expected now claims to satisfy SR-220 through LLR-210 AND LLR-312, so that "the close and its three outcomes preserve every effect owed to a specification" -> not the same: cases were added, and the claimed parent set and the oracle both widened. A correct implementation of the old text (the pre-WI-866 close, which lost all but the last edge) passes the old Method and fails the new one. The Method cell carries the new cases; the Expected cell carries the new claim. NOT blessed, for two reasons:
  - (1) Expected says TC-254 satisfies LLR-312, and through it "every effect", but the Method never exercises LLR-312's first clause: every affected spec is resolved and validated before the first write, and a refused target leaves nothing written. Tests for exactly that exist (`test_a_refused_edge_leaves_the_lane_tree_byte_identical`, `test_a_refused_return_leaves_the_lane_tree_byte_identical`), but no TC cites them, and TC-254's Evidence omits them. So the case claims more than it checks.
  - (2) The link clause, "when two returned specifications and the adjudication specification link a returned row", does not say what it tests. In the cited test, ONE returned spec (WI-403) and the adjudication spec link the other returned row (WI-402). The order dependency that makes the case meaningful (the linked row moves before the linking row is rewritten) is not stated.

  Returned: WI-866 spec `## Dispositions`, draft 1.

VERDICT: MEANING rows=1

## first-approval

- [RETURN] LLR-312 -> handback's consolidation close must (a) resolve and validate every affected queued spec before its first write, (b) plan one ordered rewrite sequence per spec so that every blocker named for one waiter lands in its needs, and (c) apply each sequence over the spec as it then stands, so an inbound link redirected by an earlier move survives, re-reading its own adjudication spec before composing its terminal text -> UPWARD, SR-220 requires an outcome to take effect only as a recorded restructuring, and LLR-210 already places the edge and return transforms under SR-220. So a row specifying how handback applies them faithfully is decomposition, not new scope. It matches WI-866's Done-when, and the text is a closed, observable obligation. SIDEWAYS, it does not overlap LLR-210, which keeps the census, the verdict parse, the close refusal and the pure transforms, while this row owns the application. DOWNWARD, its only TestRef, TC-254, verifies (b) and (c) but not (a): no TC-254 Method clause or Evidence test drives a refused target and observes that nothing was written, although such tests exist uncited. TC-254's amendment is itself judged MEANING and not blessed above -> not ready. The text is sound, but approving it would bless a row whose preflight clause has no verifying case on record and whose one TC is unsettled. It should come back with TC-254 in the same sitting. Returned: WI-866 spec `## Dispositions`, draft 1.

OUTCOME: RETURN rows=1

SITTING: JUDGED kinds=amendment;first-approval
