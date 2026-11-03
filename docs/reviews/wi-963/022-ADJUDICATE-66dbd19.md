# WI-963 checkpoint sitting at 66dbd19 (the whole set, at the gated tip)

## amendment

This sitting judges WI-963's whole spine set together, so that one verdict authorizes the one act it needs. The set was judged in parts at sittings 008, 009, 014 and 019.

**The text has not moved since it was judged.** The judged-text identities here for LLR-153 (`2cdf7de6605da2cc`) and LLR-158 (`a2839bd43c88cce1`) are the ones sitting 008 blessed. Between 657fa68 (sitting 019) and this tip, no registry, script or test changed; the commits since are records only. `trace.py --strict` exits 0.

Both rows are MEANING, and I would bless both, as at sitting 008.

- [MEANING+BLESS] LLR-153 Detail -> before: trigger (a) mints one adjudication row from every approved or routed cell change on the merged commit -> after: the same, except that trigger (a) "excludes only records the merged range already settled under LLR-364" -> not the same: a class of amendment records no longer mints. Ready to bless. The exclusion is closed ("only"), and it points at the row that owns the condition rather than restating it (as at 008).
- [MEANING+BLESS] LLR-158 Detail -> before: the shared walk feeds the amend-without-flip warn and the intake amendment mint alike -> after: the same, plus the mint drops records the range already settled under LLR-364, while the pre-commit warn reads the unfiltered walk because it runs before any act -> not the same: the walk's two consumers now differ. Ready to bless. The warn half is this row's own obligation, stated with its reason, and the mint half points at LLR-364 (as at 008).

VERDICT: MEANING rows=2

## first-approval

Two new rows under SR-178 await a first approval: LLR-364 and its TC-403. Each is unchanged since the sitting that last approved it:
- LLR-364, approved at sitting 019 against 657fa68;
- TC-403, approved at sitting 014 against a413eb6, with no Method or Expected change since.

The stopping boundary recorded at 008 holds: LLR-153 decides when the mint runs, LLR-158 what a change is, and LLR-364 which changes a range has already settled.

- [APPROVE] LLR-364 -> the trunk mint drops an amendment record only when the range re-attests the row, its whole approved and routed cell set equals its copy at the range's end, and either no later range-added entry wrote, or may have written, its registry, or its routed cells are the same at the range's two ends. It names that arm's one limit (a restore between two acts settles) and its one cost (a fully judged routed move under a later copy mints). Unreadable carriers refuse by name, the recovery is named, and the scope is bounded -> it matches the code (`_settled_row`, `_no_later_writer`, `_routed_unmoved`, `_snapshot_copy_rows`), and TC-403 pins both the limit and the cost. The Trust section scopes Done-when items 1 and 5 under a later copy, as sittings 014 and 019 accepted -> ready, as at 019.
- [APPROVE] TC-403 -> on both mint routes and over squashed and unsquashed ranges, drives the settled and still-mints cases, the absent-ledger and unconsulted-filter cases, the unreadable and malformed carriers, the restored-cell, routed and unrouted traced cases, both later-writer arms with the pinned restore limit and its contrast, and the two replayed landings -> it is closed over LLR-364's arms, its 21 evidence nodes exist, and it names no code symbol in its Method -> ready, as at 014.

**Parent-first.** SR-178 is Approved. LLR-364 and TC-403 are approved together, beside LLR-153's and LLR-158's blessings.

**What the act needs.** The rung is released, so the later act turn does both parts in one act:
- re-attest LLR-153 and LLR-158;
- flip LLR-364 and TC-403, taking the low-level-requirements and test-cases copies.

Nothing is held for the owner.

OUTCOME: APPROVE rows=2

SITTING: JUDGED kinds=amendment;first-approval
