# WI-865 — combined adjudication at c5861df (first-approval, re-sit)

Independent adjudicator, one sitting. I re-read LLR-314 and TC-334 as shown in
the brief, against SR-234 and LLR-315 (both approved in the first sitting),
`kitlib/dispute.py` and the reworked `tests/test_dispute.py` (`f309fb31`).

Runs:
- The dispute tests across both modules pass as built (`38 passed, 48 deselected in 7.66s`).
- I repeated the first sitting's probe: I weakened `_finding`'s exact-key check to a superset check in my working tree. The malformed-findings test now fails (`1 failed, 16 passed, 17 deselected`). Restored with `git checkout`; the tree is clean.

## first-approval

- [APPROVE] LLR-314 -> `kitlib.dispute` must:
  - accept a findings file of only a non-empty `range` and a non-empty `[[finding]]` list;
  - require each finding to carry exactly a unique letter-led id, held_by builder or coordinator, and non-empty finding and position texts, kept verbatim apart from leading and trailing newline characters;
  - write and read the request line;
  - parse one RULING per requested id under the declared grammar, refusing anything missing, duplicate, unrequested, malformed or incomplete, with nothing defaulted.

  -> UPWARD, it is the grammar half of SR-234, which is approved. SIDEWAYS, LLR-315 is the assembly half, and the two share no decision. DOWNWARD, the gap the first sitting named is closed: TC-334 now drives an extra key and each of the four keys missing, each refusing with "a finding takes exactly", and the superset probe reds it (observed). The reworded verbatim clause matches `_finding`'s `value.strip("\n")` (dispute.py:148): edge newlines go, while spaces and interior lines stay. Every other clause was verified in the first sitting -> ready.
- [APPROVE] TC-334 -> its named tests must show:
  - the four-input composition, and its refusals, including the exact-key finding refusals;
  - the verdict grammar's acceptance and refusals;
  - no approval authorization;
  - the routing through the shipped template;
  - the entry point's binding and pre-launch refusal.

  It verifies SR-234, LLR-314, LLR-315 and IF-290 -> DOWNWARD, each Method step, now including the extra-key and missing-key refusals, has a named test that asserts it. The Expected cell claims nothing the Method does not drive. Every clause of the four rows it verifies is covered -> ready.

OUTCOME: APPROVE rows=2

SITTING: JUDGED kinds=first-approval
