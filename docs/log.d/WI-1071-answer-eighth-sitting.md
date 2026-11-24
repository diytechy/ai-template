## 2026-11-24 — WI-1071: WI-1068's verdict answered: four rows restore dropped clauses, three test cases fixed, LLR-423's overlap resolved

Built on `maint/wi-1071`, cut from `refactor_again` at `ec188f984`, planning
`single` (plan `docs/plans/WI-1071/plan.md`, revision 1, approved by the
coordinator with D1 to D13 confirmed). The spec's Deliverable holds the
per-item record, the mutants and the acts owed.

- **Dropped clauses** (text only, each still `Accepted`): LLR-047 restates
  literal run-section values, kept name case and the dropped orphan
  description and empty command; LLR-039 the JSON-quoted front matter, the
  guide-edit and missing-file staleness and the legacy opt-out's precedence
  (its duplicated-loaders clause reported no longer enforced); LLR-199 the
  generated-file header and the trunk re-derivation, pointing at LLR-403
  for placement and the unplaced design rows; LLR-281 the SHORT line, its
  length and the floor checked first. TC-047, TC-042, TC-195 and TC-291
  state them, their code names scrubbed. Nine new or extended tests, each
  red against a one-line mutant, none committed.
- **TC-398**: reads each unequal-identity refusal for both digests, which
  three tests already assert; "one judged-text line per row shown for
  judgement" (routed from WI-1070).
- **TC-530** (still `Drafted`): a constrains-only range and a companion-only
  range, walked and minted apart. **TC-571** (still `Drafted`): its method
  names the rendered row that also moves its phase cell, and the test pins
  that cell under the no-act label.
- **The session variable** has one home, LLR-423 and TC-533: LLR-300 no
  longer states it and is scrubbed of its code names; TC-316 no longer
  checks it or verifies IF-277 (still reached through LLR-423 and LLR-424);
  its test re-tagged to TC-533, and TC-533 cites IF-277 instead (the strict
  trajectory check's seam rule needs one citing test case). Three older LLR-300 test gaps closed by added
  cases (the threshold's bounds, four unreadable shell forms, the window
  check tagged TC-339).
- **Rows.** Eleven `Accepted` rows amended in text and TC-316's `verifies`
  routed (owed); TC-530 and TC-571 rewritten, LLR-423 and TC-533 owed a
  first acceptance. No id minted, no status moved, no kit file changed.
- **Deviations from spec:** none beyond the plan the coordinator approved,
  plus the coordinator's TC-398 wording routed from WI-1070 and TC-533's
  `verifies` gaining IF-277, which the plan did not foresee.
- **Byte deltas on budgeted files:** none touched.
- **Left:** the component view header's stale placement sentence (D13);
  `trace.py --strict` fails on LLR-484's "such as" form finding, on this
  branch and its base alike, outside this row.
- **Review round 1:** Hydrogen APPROVE; Sol four MINORs, ruled by the
  coordinator and fixed: LLR-039 (and TC-042) bound to an edit that
  changes a guide's derived title or summary, with a title arm in its
  test; LLR-047's inherited "dev-setup" restated; the Deliverable no
  longer claims one obligation for LLR-300 (D8); TC-571's test asserts the
  phase cell's before and after under the no-act label on both surfaces.
  Round-1 modules `235 passed, 18 skipped in 323.09s (0:05:23)`;
  `check_trajectory.py --strict` exit 0.
- **Review round 2** (narrow): Hydrogen and Sol APPROVE findings=0.
- Deferred open items: none — no decision owed to the operator.
- **Tests:** the twenty-one touched and ratchet modules `942 passed, 3
  skipped in 745.71s (0:12:25)`; `check_trajectory.py --strict` exit 0;
  `check_docs.py` 0 broken; `trace.py --strict` exit 1 on LLR-484 alone (as
  on the base), which stops `run_menu.py smoke` before its tier; the
  chain's later steps run by hand pass, the tier `3933 passed, 3 skipped,
  18 warnings in 331.13s (0:05:31)` (CPU 848.4 s over the 540 s budget,
  reported only).

<!-- fig: cmd="python -m pytest -q -n auto <the twenty-one modules>; python project-trajectory/scripts/check_trajectory.py --root . --strict; python project-trajectory/scripts/run_menu.py smoke, then its later steps by hand" rev="maint/wi-1071 at dcb748c9a and its close-out tree" -->
