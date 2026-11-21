+++
id = "WI-1019"
title = "An LLR states WI-1001's rule that an accepted automated test case no test tag names is a finding"
workstream = "process"
sr_refs = ["SR-157"]
specref = "docs/archive/work/complete/WI-1017-llrs-yield-to-design.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "none"
+++

## Context

Filed on trunk at WI-1017's landing (2026-11-21), from the evidence sample
in its Deliverable ("Causes outside the guidance", row 2; case B10).

WI-1001 built the rule that an accepted automated TC no test tag names is a
finding. No LLR states it: TC-428 and TC-429 verify SR-157 directly. Its
builder stopped at the accepted row, since whether LLR-366 is amended or a
new LLR is minted was the operator's call, and nothing filed the gap.

**Settled at the scope critique (2026-11-21,
`docs/reviews/2026-11-21-scope-critiques/WI-1019.md`): a new row.** WI-1001's
rule says which test cases owe a declaration at all; LLR-366 says a case's
evidence parts equal its declarations, Drafted cases included. Two contracts,
so two rows, and LLR-366 stays as accepted. The new row is LLR-395, minted
`Drafted` under SR-157. Its text is in contract voice and names no code: the
review-churn plan's item 5 refuses code names in requirement text, and
variant F's text check (WI-1021 to WI-1030) will hold it to that. Its
`module` and `code_symbol` cells are filled, since today's schema requires
them until variant F removes them.

**The acts it leaves.** LLR-395 is `Drafted`, and TC-428 and TC-429
(`Accepted`) drift when their `verifies` cell changes. The operator-acceptance
dial releases these rungs to automated adjudication (queue-drill HANDOFF §3.1
Q5, §3.3 N4), so the lane ends at the registry edits and lists what is owed;
no status moves and no hold sits inside the lane.

**Changed at the build (2026-11-21).** The parent-first rule (SR-245 and
LLR-357 at the trace, SR-246 and LLR-358 at the commit) refuses an `Accepted`
TC verifying a `Drafted` LLR: re-pointing TC-428 and TC-429 at a new `Drafted`
LLR-395 fails `trace.py --strict`, and the commit hook refuses it. So this row
mints LLR-395 and links it from the code tag, and TC-428 and TC-429 move to
verify it after LLR-395's first acceptance, under WI-1038 (filed on trunk by
the coordinator). The re-point's drift is WI-1038's.

## Done-when

- [ ] LLR-395 (`Drafted`, under SR-157) states WI-1001's rule as built: which
      live test cases owe a test-file declaration, the inputs that make the
      check vacuous or stop it, and its severity by rung and by strict
      checking, all as TC-428 and TC-429 expect. Its text names no code.
- [ ] LLR-395's `test_refs` name TC-428 and TC-429, whose rows are unchanged
      here; their re-point to verify LLR-395 is WI-1038's, after LLR-395's
      first acceptance. `trace.py --strict` stays clean.
- [ ] The function implementing the rule names LLR-395 in its `Implements:`
      tag, SR-157 kept.
- [ ] The Deliverable lists the act owed: LLR-395's first acceptance, for
      automated adjudication; the re-point's drift is WI-1038's.
