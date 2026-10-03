# WI-761 adjudication: LLR-289, TC-302 (amended by WI-759)

- [MEANING] LLR-289 Detail -> report every real open item's wi_refs entry that names no live or terminal work row, skipping only example open-item rows (so a reference to the example WI-000 IS reported) -> the same, but an example work-item reference (WI-000) is also skipped -> the reportable set shrank: an implementation correct under the old text (reporting WI-000) fails the new one, so the scope of the check moved.
- [MEANING] TC-302 Method -> assert one finding per absent work id for pending/ruled rows, none for a terminal-only id, none for an example row or absent registry -> additionally assert an example work-item reference yields none, and that an example reference beside a real missing id leaves the real finding intact -> two acceptance cases were added; a test satisfying the old method need not check either, so the acceptance condition moved.

Would bless both: `open_item_wi_ref_findings` skips `is_example(wid)` per entry while still reporting a real dangling id, and `tests/test_open_item_readiness.py::test_example_wi_refs_are_inert` (pending and ruled) asserts exactly `["OI-98: wi_refs names unknown work item WI-999"]` for a `"WI-000", "WI-999"` wi_refs; the module ran 10 passed.

VERDICT: MEANING rows=2
