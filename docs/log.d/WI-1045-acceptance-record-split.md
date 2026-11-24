## 2026-11-24 — WI-1045: the landing rules leave the acceptance record for a CMP-008 module; the record keeps the two-tree comparison

Deferred open items: none — the two pre-existing items the build surfaced
are the coordinator's to file (below), and no call is owed to the operator.

Built on `maint/wi-1045` (cut from `refactor_again` at `9e8eb6e57`) under the
plan `docs/plans/WI-1045/plan.md`, which the coordinator approved on
2026-11-24 before any build, with D1 to D12 confirmed. The spec's Deliverable
holds the per-item record, the cover and the acts owed.

- **What changed.** The ruling sync, the parent-first commit judgement and
  the trunk mint's settled-amendment filter and held-act arms (27 functions
  and 6 constants) move, byte-identical, from `acceptance_record.py` into a
  new `landing_rules.py` declaring CMP-008 and holding IF-308's body.
  `acceptance_record.py` keeps the two-tree comparison, the mirror rules, the
  merge-time acceptance-act refusal, the judged-text identity and the record
  readers the new module calls, under CMP-006. No re-export is left;
  `check`, `integrate`, `intake`, `text_then_act` and `adjudicate_act` import
  the new module. Every finding and refusal is unchanged.
- **The cover.** IF-308 re-owned to CMP-008; IF-091's data (156 characters,
  v2) and body state the readers the new module reads through it; IF-256
  drops its CMP-006 requestor. 122 crossings outside the kernel (121 before),
  none uncovered.
- **Rows.** No spine row amended or minted; the three interface rows are
  `Drafted` and owe the first acceptance they owed before.
- **Deviation from the spec:** `accepted_text_digest` stays in
  `acceptance_record` behind IF-129 (plan D3): one of its three readers is
  CMP-006, and moving it would add a crossing.
- **Sizes:** `acceptance_record.py` 989 -> 689 SLOC (no size-ratchet entry
  either side); `landing_rules.py` 340; `intake.py`'s baseline 1946 -> 1947
  (its import line). Deferred imports stay 46.
- **Byte deltas on budgeted files:** none (no budgeted file touched).
- **Tests:** red first `1 failed, 14 passed in 0.97s` (the boundary test)
  and `7 errors in 3.78s` (the switched modules); the 137 affected modules
  `5212 passed, 4 skipped in 5285.36s (1:28:05)`; `run_menu.py smoke` exit 0,
  `3957 passed, 3 skipped, 18 warnings in 150.36s (0:02:30)`.
  <!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 137 modules>; python project-trajectory/scripts/run_menu.py smoke" rev="36a476992's tree, then the close-out tree for the smoke run" -->
- **Review round 1:** Hydrogen `APPROVE`, findings=0; Sol one MINOR,
  adopted: the RESYNC entry named 10 of the 33 moved definitions. Fixed in
  `f21ab4907`, which lists all 33 and says a project's import of any of them
  from `acceptance_record` must move to `landing_rules` (no shim).
- **Left for the coordinator to file:** the uncalled
  `acceptance_record.verdict_rulings` alias, whose import of `kitlib/verdict`
  makes CMP-006's notes sentence on that module's edges untrue, and the
  unread `landing_rules.ARCHIVE_WORK_DIR`.
