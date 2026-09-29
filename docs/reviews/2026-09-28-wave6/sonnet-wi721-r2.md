<!-- Claude Sonnet (read-only) confirmation of WI-721's fix round, build/wi-721 3496344e..d7c43118. -->

d7c43118 SOUND

BLOCKER: none

MAJOR: none. The LLR-286 finding is resolved:
- Its `detail` now reads "...is a live row of its tier's registry, in whichever carrier form the kit's registry reader resolves...".
- That matches the code: `retire.live_ids` (`retire.py:233-253`) goes through `spine_carrier.load_need_tier` / `load`, and `resolve()` (`spine_carrier.py:692-722`) picks the live carrier.
- It is pinned by `test_legacy_registry_rows_are_live_and_only_a_spent_id_is_reported`.
- Only that cell changed, and the status is still Approved.

MINOR: none. Both are resolved:
- TC-299's `evidence` lists the new test, in the cell's format and in definition order.
- The IF-102 docstring's caller list matches `interfaces.toml` IF-102's requestors.

**Collateral:** the fix commit touches exactly those two registry lines. SR-226 and TC-299's attesting cells carry no "TOML" narrowing.

**Run:**
- Without `GIT_CEILING_DIRECTORIES`, the scaffold tests hung.
- With it, `-n 2` hit xdist worker crashes, a Windows infrastructure issue and not a test failure.
- A sequential run, `GIT_CEILING_DIRECTORIES=/c/Projects/ai-template.wt python -m pytest -q tests/test_retire.py tests/test_trace.py tests/test_rule_sync.py -p no:cacheprovider`, gave **127 passed, 1 skipped in 364.27s**. The skip is unrelated: `test_trace.py:1199`, an empty `provenance-allow`.
