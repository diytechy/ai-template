# WI-963 dispute sitting at 93526df

DISPUTE: findings=F1;F2

**Disclosure.** I held checkpoint sittings 008 and 009, which approved LLR-364 and TC-403 with the arm both findings name. Sitting 008 also accepted the rationale sentence F2 calls false. I judge that sentence below as an error I passed.

## The behaviour both findings describe

`acceptance_record._settled_row` settles a re-attested row in one of two ways. If no range-added entry after its latest re-attestation wrote its registry (`_no_later_writer`), it settles. If a later entry did, it settles only when the row's routed traced cells at the range's after revision equal those at its before revision (`_routed_unmoved`).

The findings' sequence:
1. A lane re-points SR-001's `SN-Refs`, and act A re-attests the row.
2. The lane restores `SN-Refs` to its pre-range value.
3. Act B, re-attesting another row of the same registry, copies the registry.

B's copy holds the restored value, so the row equals its copy. Its routed cells equal those at the range's start, so it settles and no amendment row mints. I read this from the code and the cited cases, and the reviewers' probes agree. The behaviour is real.

## What the behaviour actually leaves unreported

- **The routed restore was re-anchored by the kit's existing rule.** The restore is a traced change. The snapshot refresh lets any act re-anchor traced pointer changes without a verdict (its own refusal text: "Traced cells ... and the ref pointers are never blocked here"). That rule is the kit's standing traced-refresh policy, not this lane's. Only approved-cell drift is refused unread, so B could not have absorbed an approved change.
- **Across the merged range nothing routed moved.** LLR-153's routed trigger is defined over the range's diff, so it has nothing to report even before this lane. The approved text change is exactly what A re-attested.
- **What is left is narrow.** A's sitting read the row's chain with the new parent pointer, and the row lands with the old one. That is a context the blessing did not see, but it is a pointer the snapshot already re-anchors without review. Before this lane, the same range minted only a redundant approved-text row, which the old workaround closed by citing the act.

## What each remedy costs

Every hand landing is a single squash commit, and the replay range Done-when item 6 names (`5245ac82c..08bbb71b6`) is one commit. On such a range, the re-attesting act's own copy is overwritten by the later copy and cannot be recovered.

- **F1's remedy:** evidence bound to the act's own copy. On a squash it cannot be met without an IF-220 format change, one recording each re-attested row's state, which this lane's scope and its adopters' ledgers do not carry. Without that change it reduces to minting.
- **F2's remedy:** delete the arm. That makes every later writer of the registry unsettle the row.

Either way, the standard act turn mints again. An amendment act followed by a first-approval act in the same registry is the two-part act every adjudication lane takes. WI-978's act would have re-minted TC-158, for example. So would the WI-926 replay that Done-when item 6 requires to mint nothing.

That is the redundancy this work item exists to remove. It would come back on the common path to catch a rare sequence (restore a routed pointer between two acts in one registry) whose content the kit's traced-refresh rule already admits.

## Where the lane is genuinely wrong

The text claims more than the arm delivers, and the Done-when is now ambiguous.
- **The detail sentence.** LLR-364's detail says the second arm proves "that nothing routed moved for a later copy to absorb". It proves only that the routed cells are the same at the range's two ends. That is a false statement in an approved cell (K1), and I passed it at sitting 008.
- **Done-when item 5.** It promises that a row "edited after its act and restored to its pre-range text in one cell, still mints (the whole-row comparison)". It holds when no later act copies the row's registry. It does not say it is bounded there, so read literally it collides with item 6.

The fix is to state the bound honestly, not to change the behaviour:
- amend LLR-364's detail and rationale, and TC-403, through their authority, to say what the arm guarantees and its one limit: a routed pointer edited and restored between two acts copying the registry is re-anchored by the later copy, as any traced refresh is;
- add the restore-under-a-later-writer case to TC-403, pinned as settling, so the bound is driven rather than assumed;
- amend Done-when item 5 through its in-lane blessing so it is scoped to a range with no later copy of the row's registry;
- correct the RESYNC entry to match.

An owner who prefers redundant mints to this bound can overrule the coordinator's D-014 on review. The verdict leaves that choice where D-014's record puts it.

## F1

F1 asks for settlement evidence bound to the row's own re-attesting act. On the squashed landings every hand landing is, that evidence does not exist without a ledger format change, so the remedy collapses into minting on every later writer. That restores the redundant mint this lane removes, on the standard two-part act and on the replay Done-when item 6 requires, to report a net-zero traced change the snapshot already re-anchors. The text defect it touches is ruled under F2.

## F2

The behaviour stays. F2's K1 point holds: LLR-364 asserts a guarantee ("nothing routed moved") that the arm does not provide, and Done-when item 5 reads as a promise the arm breaks under a later writer. The deletion it proposes is the wrong fix, for the cost above.

RULING: F1 DISMISS not-worth-cost evidence bound to the re-attesting act's own copy is unrecoverable on squashed landings without an IF-220 format change, so the remedy degrades to minting every row a later act's registry copy touches, re-minting the standard amendment-then-first-approval act turn and the WI-926 replay Done-when item 6 requires, to report a net-zero routed restore that the snapshot's traced-refresh rule already lets any act re-anchor
RULING: F2 FIX LLR-364's detail claims the later-writer arm proves nothing routed moved, but it proves only equality at the range's two ends, and Done-when item 5 reads as unbounded; keep the arm, amend LLR-364, TC-403 and the RESYNC entry to state its guarantee and its one limit (a routed pointer restored between two acts copying the registry is re-anchored by the later copy), pin that case in TC-403, and scope Done-when item 5 through its in-lane blessing to a range with no later copy of the row's registry
