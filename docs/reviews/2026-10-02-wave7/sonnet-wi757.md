# Sonnet review — WI-757 (build/wi-757 at 70b00b7e)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol, low). Range `a8dee5b7..70b00b7e`.

70b00b7e SOUND

**BLOCKER:** none. **MAJOR:** none. **MINOR:** none.

- LLR-290 `detail` and TC-303 `method` gained exactly the drafted text (pure insertions); both still Drafted; no production code changed.
- Test (a) `test_codex_inferred_compaction_holds_on_later_rising_requests` (~928): the third call's only new request rises, and it asserts compacted/inferred; it would fail if `_observe_compaction` started from an empty source.
- Test (b) `test_codex_reported_replaces_inferred_and_holds_on_new_drop` (~950): after the source becomes reported, the rollout is rewritten without the compacted entry (`_codex_rollout` replaces the file), so `CodexAdapter.compaction` returns reported=False and 15717 -> 10000 is a new inferred drop beyond the cursor; only the stored reported source keeps the result reported. It would fail if a later drop cleared or overwrote it. The drafted form's trivial pass is avoided. (Read, not mutation-tested.)

**Commands:** `pytest -q -n 2 tests/test_session_keep.py`: `65 passed in 18.56s`; git log/diff reads.
