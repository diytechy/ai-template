5453f920 SOUND  
6defae22 NOT YET SOUND

## 5453f920

Context-only judgment: no incompatibility introduced by 6defae22 against WI-629’s names, carrier columns, classifiers, or assumption-row API.

## 6defae22

- **major** — TC-245 and TC-246 do not prove that the delivered checker invokes their rules. The tests call `hat_findings` and `obstacle_hat_findings` directly at tests/test_trace_hats.py:320 and tests/test_assumption_rules.py:379. Deleting the production wiring that loads `speaks_for` and composes both rules at trace.py:4774 and trace.py:5035 leaves every added TC-245/246 test green while the harness silently stops enforcing SR-213/SR-214. Fix in **6defae22**: add checker-level regressions that assert an undeclared `speaks_for` and a no-roster `ObstacleHats` value become strict `hat` findings. Keep the approved Smoke clauses intact; supplementary subprocess/scaffold cases belong in an existing Full/slow module.

- **minor** — The no-roster rendering correction is incomplete. `_hat_report_section` now exposes obstacle findings without a roster at trace.py:2317, but the report’s metric table still emits “Hat findings” only when `hat_names` is nonempty at trace.py:5339. Thus a real strict hat failure can appear below while its summary count is absent. Fix in **6defae22**: condition that metric block on `hat_names or hat_dangling`, and cover it in the checker-level regression above.

## CROSS-CHAIN

- SR-211/LLR-250’s ungated reading is explicit and intentional, not a row defect requiring amendment. Read-only evaluation at the tip produced exactly **43 bridge advisories and zero bridge failures**.
- SR-213’s no-stakeholder-list vacuity and SR-214’s no-roster failure behavior are faithful to their rows. Neither rule depends on a frame or assumption-tier adoption.
- IF-208 is justified as a distinct logical contract: unlike IF-190’s three-channel tier entry point, its two functions land in pre-existing interface and hat classes. Its Contract body is cited by TC-244 and TC-246.
- Hidden-inclusive repository search found no missed `load_hat_names` caller, including skills and prompts.
- Reusing `Coincident` through the single `SPINE_COLUMN` entry preserves the SR/IF schema legs and carrier bijection. The carrier inverse, schema coverage, module-size ratchet, dogfood, and RESYNC_PACK zero-argument checks passed.
- The required pytest command could not initialize because the read-only sandbox provides no writable temporary directory; failure occurred before collection. AST parsing and 44 directly callable behavior tests passed.