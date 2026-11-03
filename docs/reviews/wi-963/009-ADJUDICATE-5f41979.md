# WI-963 checkpoint sitting at 5f41979

## first-approval

This sitting re-judges TC-403, which sitting 008 (`008-ADJUDICATE-e3d9617.md`) returned alone. That sitting approved its parent LLR-364 and blessed LLR-153 and LLR-158.

**Only the returned cell moved.** Between e3d9617 and this tip, the only change is one line of TC-403 (its Method), and no code or test changed. A scan of the new Method finds no test-function name and no code file. `trace.py --strict` exits 0. TC-403's suite (`tests/test_intake_settled.py`) passed at 008, 24 tests, and nothing under it has changed since.

- [APPROVE] TC-403 -> assert, on both mint routes, that:
  - settled records are omitted;
  - later or unrecorded amendments and unproven copies still mint;
  - an absent ledger changes nothing, and the filter is not consulted without records;
  - a listed unreadable or unparseable ledger or copy refuses by name without minting;
  - whole-row comparison catches a restored cell and a routed traced cell moved after the act, while an unrouted one still settles;
  - a routed change absorbed by a later act re-attesting another row of the same registry still mints, over an unsquashed and a squashed range;
  - a later act copying only another registry leaves the row settled over both ranges;
  - a later same-registry or legacy act settles only when routed cells are unchanged across the range;
  - the replayed landings mint nothing.

  Expected: LLR-364's contract with both later-writer arms over both range shapes, and IF-091's outcome -> it is closed over every clause of LLR-364, approved at 008, and its 19 evidence nodes drive each arm -> ready:
  - Sitting 008's one return is answered. The enumeration is gone, and the range-shape coverage now sits inside the capability-voice assertions.
  - The Evidence cell is the one home of the test names.
  - It names no code carrier.

**Parent-first.** LLR-364 is approved (sitting 008), and its TC-403 follows it.

**What the act needs.** The rung is released, so the later act turn flips TC-403 and takes the test-cases copy. Nothing is held for the owner.

OUTCOME: APPROVE rows=1

SITTING: JUDGED kinds=first-approval
