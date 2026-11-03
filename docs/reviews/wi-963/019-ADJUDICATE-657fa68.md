# WI-963 checkpoint sitting at 657fa68

## first-approval

This sitting re-judges LLR-364 after the text-only fix that dispute sitting 018 (`018-ADJUDICATE-e5811b9.md`) ordered. TC-403 is unchanged since sitting 014 approved it, and is shown only as chain evidence.

**What moved, checked against the range e5811b9..657fa68.**
- No behaviour changed. The only code-adjacent line is the case count in a comment in `tests/conftest.py`.
- LLR-364's Detail gains one sentence.
- The claim copy's Trust section gains the bullet "The scope of Done-when item 1 under a later copy".
- The coordinator-cycle recipes' sweep step and their "What the sweep mints after the act" note are narrowed. The shipped copy and both dogfooded copies are byte-identical.
- IF-091's data cell was shortened. It is context only, with no approval status.

**The checks.** `trace.py --strict` exits 0.

- [APPROVE] LLR-364 -> as approved at 014, plus the consequence sitting 018 ordered named: "A row re-attested in the range whose routed traced cells moved in the range is not proven settled when a later act copies its registry, so it is minted even when its own act judged it" -> the row now states both sides of the later-writer arm: its one limit (a restore between two acts settles) and its one cost (a fully judged routed move under a later copy mints). Each is pinned in TC-403 (`test_a_routed_cell_restored_between_two_acts_copying_the_registry_settles`, `test_a_later_writer_leaves_a_row_with_moved_routed_cells_unsettled`). It names no code carrier, and its boundary is unchanged since 008 -> ready:
  - **The Done-when scope.** The new Trust bullet states the scope sitting 018 ordered for item 1. Item 1's settled row yields no amendment row whenever no later act copies its registry, or its routed cells are the same at the range's two ends. Under a later copy with moved routed cells the row still mints, because on a squashed range it cannot be told from an absorbed post-act move. The coordinator checks it against the lane's own act and closes it citing that act. The bullet sits beside item 5's, for the reason sitting 014 accepted.
  - **The recipes.** The sweep step no longer claims that every minted row is real work. It names the one case and tells the coordinator to close such a row citing the act.
  - **A wording note on the recipe, not a finding against LLR-364.** The recipe says to close the row "when that act re-attested the row and its text is unchanged since". "Text" should be read as every cell the settlement compares, approved and routed traced. A routed cell moved after the act is exactly the case the arm mints to catch, so a coordinator who checked only the approved text could close a row that owed judgement. A later edit of the recipe could say "every cell the filter compares" outright.

**Parent-first.** SR-178 is Approved, and LLR-364 is approved. Its TC-403, approved at 014 and unchanged since, belongs to the same act.

**What the act needs.** The rung is released, so the later act turn flips LLR-364 and takes the low-level-requirements copy. Nothing is held for the owner.

OUTCOME: APPROVE rows=1

SITTING: JUDGED kinds=first-approval
