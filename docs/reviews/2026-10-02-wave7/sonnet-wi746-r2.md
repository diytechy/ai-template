# Sonnet review — WI-746, fix round 1 (build/wi-746 at acc1e195)

Reviewer: Claude Sonnet 5.5 (read-only). Range `56503928..acc1e195`, and the lane `2a902b50..acc1e195` as the landing candidate.

acc1e195 SOUND

**BLOCKER:** none. **MAJOR:** none (round 1's fixed). **MINOR:** none (all four wording minors fixed).

- `prompts/adjudicate-disposition.template.md:44` now says the machinery "lists the successor in the open item's `wi_refs`, so the successor stays queued but blocked until the owner rules" ("an OWNER GATE on the successor (IF-073)"); `CATALOG.md` digest `sha256:7b892bfd19c2`, `gen_prompt_catalog.py --check` fresh; `tests/test_prompts.py:43-47` asserts the new phrases and the absence of the old one (fails on the old text).
- `intake.py:297-304`, `kitlib/spine.py:205-222`, `schedule.py`'s header and the RESYNC entry corrected.
- The two round-1 cosmetic notes (a row with both kinds of wait reports only `blocked`; `_frontier_lines`'s `out = []`) unchanged; neither blocks landing.
- No remaining claim in the kit that intake writes an OI id into `needs`. The fix commit changes comments and docstrings only in scripts (11+/11-); the legacy reader (`split_pred_edges`) untouched; worktree clean.

**Commands:** `pytest -q -n 2 tests/test_open_item_readiness.py tests/test_schedule.py tests/test_intake.py tests/test_prompts.py tests/test_resync_pack.py`: `212 passed in 58.89s`; `gen_prompt_catalog.py --check`: fresh (9 prompts); `pytest -q tests/test_module_size_ratchet.py tests/test_dogfood_sync.py`: `45 passed, 1 skipped`.
