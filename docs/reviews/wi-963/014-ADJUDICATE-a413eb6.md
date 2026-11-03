# WI-963 checkpoint sitting at a413eb6

## first-approval

This sitting re-judges LLR-364 and TC-403 after the fix round that dispute sitting 013 (`013-ADJUDICATE-93526df.md`) ordered. Its F2 FIX was: keep the later-writer arm, state its guarantee and its one limit, pin the limit in TC-403, and scope Done-when item 5. No act has been taken since sittings 008 and 009, and both rows moved, so both are judged again here.

**What moved, checked against the range 93526df..a413eb6.**
- In `acceptance_record.py` the diff touches docstrings only, so the behaviour is unchanged, as the coordinator states.
- `tests/test_intake_settled.py` gains the two pinned cases:
  - a routed cell restored between two acts copying the registry settles;
  - the same restore with no later copy still mints.
- LLR-364's Detail and Rationale, TC-403's Method and Expected, the RESYNC entry, and one Trust bullet in the claim copy changed.
- The Done-when is untouched, so the plan's pass record stays bound.

**The checks.** `pytest tests/test_intake_settled.py`: 28 passed. `trace.py --strict` exits 0.

- [APPROVE] LLR-364 -> as approved at 008: the trunk mint excludes only a record re-attested within the range whose whole approved and routed cell set equals its copy at the range's end, and either no later range-added entry wrote, or may have written, its registry, or its routed traced cells are the same at the range's two ends. Unreadable carriers refuse by name, the recovery is named, and the scope is bounded. It now states that the second arm "proves the row's routed traced cells are the same at the range's two ends", and names its one limit: a routed traced cell moved before the re-attesting act and restored after it is re-anchored by a later act's copy, as any traced refresh is, and the row settles. The Rationale says why that bound is accepted rather than minting on every later copy -> this is exactly sitting 013's F2 FIX. The over-claim ("nothing routed moved") is gone, the guarantee matches `_routed_unmoved`, and the limit is stated where a reader will find it -> ready. It names no code carrier, and its decomposition boundary is unchanged from 008.
- [APPROVE] TC-403 -> as approved at 009, plus the arm's limit pinned. A routed traced cell moved before the re-attesting act and restored after it settles when a later act re-attesting another row copies the same registry, over an unsquashed and a squashed range. The same restore with no later copy of the registry still mints over both. The later-writer equality is restated as "the same at the range's two ends", and the Expected names the limit -> both pinned cases exist and pass, and the Method names no test function -> ready:
  - **The Done-when scope.** The Trust bullet "The scope of Done-when item 5 under a later copy" states the scope sitting 013 ordered. Item 5's restore still mints whenever no later act in the range copies the row's registry. It always mints for an approved cell, since no later act can copy one unattested. Under a later copy of the registry, a routed traced restore is re-anchored and settles.
  - **Its placement.** Sitting 013 asked for the scope "through its in-lane blessing" of the Done-when. The lane put it in the spec's Trust section instead, because an edited Done-when would unbind the `single` plan's pass record (OI-119 (a)). I accept that placement: the bullet sits in the same spec, names item 5 and the ruling, and states the scope verbatim in substance. TC-403 pins both sides of it.
  - Note, not a finding: a reader of the Done-when alone still sees item 5 unbounded. The scope is one section away, cited by name.

**Parent-first.** SR-178 is Approved. LLR-364 and its TC-403 are approved together.

**What the act needs.** The rung is released, so the later act turn flips LLR-364 and TC-403 and takes the low-level-requirements and test-cases copies. Nothing is held for the owner.

OUTCOME: APPROVE rows=2

SITTING: JUDGED kinds=first-approval
