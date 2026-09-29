<!-- Claude Sonnet (read-only) confirmation of WI-723's fix round, build/wi-723 17b88731..35444157. -->

35444157 SOUND

BLOCKER: none

MAJOR: none

MINOR: none

**The siblings**, judged against the rationales:
- SR-024 → SR-157 is dropped correctly. No SR-024 sentence names SR-157.
- SR-129 → SR-148 is dropped correctly.
- SR-225 keeps SR-139 and SR-140, which its core SN-029 sentence carries. Its drop of SR-148 is correct: its own rationale says "The record is never a route for work".
- The other six rows are untouched.

**The advisories:**
- `_classify` (`assumption_rules.py:455`) computes the undeclared, unknown and disjoint siblings once. Both consumers read that one tuple.
- The `both` advisory is restored verbatim.
- The `unclassified` advisory is restored and extended for `Delivered-With`.
- The new `joint` advisories match that style.
- `test_unclassified_advisory_explains_every_missing_classification` pins the wording.

**The ratchet:** `assumption_rules.py: 1028` is stamped in the established style, and 1028 is the measured SLOC. No compaction was found.

**The skill copies:** the indent is restored, and the two copies are byte-identical.

**Scope:** the fix touches six files. SR-193's classes match `SR_CLASSES` (`:250`).

**Run:** `python -m pytest -q -n 2 tests/test_assumption_rules.py tests/test_cell_classes.py tests/test_traj_views.py tests/test_dogfood_sync.py tests/test_rule_sync.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py tests/test_resync_pack.py -p no:cacheprovider` → **360 passed, 1 skipped in 118.85s**.
