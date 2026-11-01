# WI-977 dispute sitting at 6afea05

DISPUTE: findings=F1

## F1: TC-205's and TC-156's evidence cells were cut during the reconcile

**Disclosure.** I held checkpoint sittings 005, 006 and 007, which blessed TC-205's and TC-156's Method cells. Those sittings judged normative text, and the evidence cell is a traced cell, not normative text. Even so, at sitting 005 I saw TC-156's evidence change and passed over it as "not one of the amended cells". So this finding falls partly on what I did not check. My blessings covered the Method cells only, and this ruling does not change them.

**Observed at this range.** I parsed each cell at the lane base (55fe67d82) and at the tip (4dc0f7e29).
- **TC-205:** the evidence went from 88 entries to 4. Of the 87 dropped entries, only one names a test that no longer exists (`test_a_two_row_batch_close_peels_under_one_canonical_order`). The other 86 still exist. Three files left the cell entirely: `tests/test_bar_attestation.py`, `tests/test_integrate_station.py` and `tests/test_integrate_admission.py`.
- **TC-156:** the evidence went from 7 entries to 3. All five dropped entries are adoption tests that still exist. Their file, `tests/test_handback.py`, is still cited.
- **The impact, reproduced on the shipped reader** with `trace.py --tests-for`, at a temporary worktree of the base and at the tip:
  - at base, both `kitlib/verdict.py` and `integrate.py` list `tests/test_bar_attestation.py`; at the tip, neither does;
  - the two station and admission suites still reach both through other TCs;
  - `test_bar_attestation` now appears only inside TC-205's Method text, which still names it in "the cited set". The row contradicts itself.

**In scope, and reached by a supported workflow.** Nothing about the scenario is contrived. The reader is the kit's own test-selection route (`--tests-for`), and its input is the registry as this lane's own commits left it. A builder changing the Bar-Green grammar's home is no longer pointed at the suite that pins that grammar.

**It is a Done-when gap, so it cannot be SUCCESSOR.** The Done-when's spine item says "traced cells follow the code". The code deleted one test and added a few, and these cells dropped 91 entries that still exist. The coordinator does not contest the finding.

**The fix.** The coordinator's proposed fix is the right size:
- restore each cell's 9e1116b evidence;
- drop only the entries naming a test the lane deleted, and add the new nodes;
- sweep every other evidence, module and code_symbol cell of the 23 rows the same way.

It changes no normative cell, so none of the Method blessings from sittings 005 to 007 needs re-judging. The two same-class traced MINORs (REVIEW-B 008's Implements-tag finding, REVIEW-A 009's back-link finding) can ride the same fix, but this verdict rules only F1.

RULING: F1 FIX the W14 reconcile cut TC-205's evidence from 88 entries to 4 and TC-156's from 7 to 3, though only one dropped test was deleted; tests/test_bar_attestation.py is now cited by no evidence cell and has left trace.py --tests-for for both kitlib/verdict.py and integrate.py; this is a gap against the Done-when's "traced cells follow the code", fixed by restoring each cell's 9e1116b evidence less the deleted node, adding the new nodes, and sweeping the 23 rows' traced cells for the same loss
