# WI-963 dispute sitting at e5811b9

DISPUTE: findings=F1

**Disclosure.** I ruled dispute sitting 013 on this same later-writer arm, and approved LLR-364 and TC-403 with it at sitting 014. This finding is the mirror image of 013's: there, a row restored after its act settled when it arguably should not have. Here, a row fully judged by its own act mints when it should not.

## F1: a fully judged row mints again under a later writer

**Observed at this range.** The finding's case is a lane that:
1. amends SR-001's approved text and re-points its `SN-Refs`;
2. re-attests SR-001 (act A);
3. then amends and re-attests only SR-002 in the same registry (act B).

At the range's end SR-001 equals its copy in every cell. But act B wrote the registry after A (`_no_later_writer` is false), and SR-001's routed cells differ between the range's two ends (`_routed_unmoved` is false), so `_settled_row` returns false and SR-001 mints. That outcome is deliberate and pinned at this tip. `test_a_later_writer_leaves_a_row_with_moved_routed_cells_unsettled` asserts that SR-001 mints, and its docstring gives the reason: "the ledger cannot tell a move act A judged from one act B absorbed".

**The defect is real, but it is not the one the remedy targets.** The proposed remedy is the one sitting 013 already dismissed: settlement evidence bound to the row's own re-attesting act. On a squashed landing, which every hand landing is, A's copy is overwritten by B's. Without a ledger format change recording each re-attested row's state at its act, two states cannot be told apart from the range's end state and the ledger:
- **this case:** the routed cells moved before A, and A judged them;
- **the pinned contrast:** the routed cells moved after A, and B's copy absorbed them.

Settling both would let a routed re-point made after the act, and never judged, disappear. Minting both costs one redundant row in this case. The arm mints, which is the fail-toward-more-review direction this kit takes wherever an identity cannot be proved, and it is the right choice. The cost argument from 013 holds unchanged.

**What is wrong is two promises that claim more than the arm delivers.** Both are reachable through the supported two-act lane the finding describes. That makes them a gap in the Done-when, so the ruling is FIX and not SUCCESSOR.
- **Done-when item 1** promises that an approved row amended in the range, re-attested by a range-added entry, and equal to its copy "yields no amendment row", without bound. Under a later copy of the same registry, with the row's routed traced cells changed across the range, it yields one.
- **The landing recipe** (`project-trajectory/skills/coordinator-cycle/references/recipes.md`, the sweep step) says the sweep "mints no row for an amendment the lane's own act settled, so every row it mints is real work and stays open". In this case the minted row is already settled. A coordinator following the recipe would keep it open as real work, and an adjudication would be spent judging a row its act had already judged.

**What the fix must do.**
- **The code.** It stays as it is.
- **The Done-when scope.** In the spec's Trust section, beside item 5's scope bullet, state item 1's scope in the same way. A row whose routed traced cells changed across the range mints when a later act in the range copies its registry, because the ledger cannot tell a move its own act judged from one a later copy absorbed. It still settles when no later act copies the registry, or when its routed cells are the same at both ends.
- **LLR-364.** Its Detail already states the arm's condition. It should name this consequence beside its one limit, so the row says what it costs as well as what it lets through.
- **The recipes, both copies (shipped and dogfooded).** Narrow the sweep step's claim. A minted amendment row whose registry a later act in the range copied, and whose routed cells moved, may already be settled. Check the row's own re-attesting act, and close the row citing it when the act re-attested the row with exactly those cells. Every other minted row stays real work.

RULING: F1 FIX the arm correctly mints a fully judged row whose routed cells moved when a later act copies its registry, since on a squashed range that row is indistinguishable from one whose routed move a later copy absorbed, but Done-when item 1 and the landing recipe still promise no row and real work for it; keep the code, state item 1's scope under a later copy in the Trust section beside item 5's, name the consequence in LLR-364, and narrow both recipe copies' sweep claim to tell the coordinator to check the row's own act and close it citing that act
