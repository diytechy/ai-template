10523f27 NOT YET SOUND

- [blocker] `project-trajectory/scripts/agent_common.py:985` — live SN approval still bypasses `authority.rung_for()` and remains unmapped/held even at `DevStg-Below`; this contradicts the owed DevStg-Needs classification and amended LLR-246. Use `rung_for(registry)` here and test held/released live SN paths.

- [major] `project-trajectory/RESYNC_PACK.md:5334` — advising a person to merge a loop lane themselves is false: both slot rungs now run regardless of merger. Remove that advice; require moving the commit to a personal lane or adding the well-formed trailer.

- [minor] `tests/test_loop_provenance.py:547` — the duplicated subject-pattern contract is not exercised for quarantine or mechanical-close commits, despite `provenance.py` claiming every real writer is driven. Add both real-writer cases or share their subject composers with provenance.