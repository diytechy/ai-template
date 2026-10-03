# Sonnet review — WI-746 (build/wi-746 at 56503928)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range `2a902b50..56503928`.

56503928 NOT YET SOUND

**Key question.** (a) Removing intake's injection of an open-item id into `needs` breaks no approved row: TC-253 (`docs/test/test-cases.toml:2620`, Approved; verifies LLR-058 and IF-176) requires only the READER (the scheduler reads open-item states, holds a row waiting on a pending item, fails closed with no registry). The only authority for the injection is ruled OI-73 ("OI ids become valid hard tokens in needs"), superseded for the writer by the owner's 2026-10-02 ruling. Keeping the reader was right; retiring it needs an adjudicated amendment of TC-253 (method, expected), IF-176 (data, notes) and LLR-058. (b) Coherent on the write side: both mechanisms release when the open item leaves `pending`, fail the same on a missing item, and go through the single `hard_preds_satisfied`; nothing writes OI ids into `needs` any more and no live row carries one. Smallest fix: correct the stale statements now; file a follow-up to retire the legacy reader through adjudication. (c) Stated once: IF-073 in the open-items header, IF-054 in `docs/work/README.md`; PROCESS.md and the templates link.

**BLOCKER:** none

**MAJOR**
- `project-trajectory/prompts/adjudicate-disposition.template.md:44` (shipped) still says the machinery "lands its id in the successor's `needs`" — now false, and it contradicts the README's "`needs` names work items only". Reword: the successor is listed in the minted item's `wi_refs` and stays queued but blocked until the owner rules.

**MINOR**
- `intake.py:297-304` (the `"open_item"` allowed-key comment) still says intake lands the OI id in `needs`.
- `kitlib/spine.py:205-222` calls OI edges "the typed dependency the OI-70/OI-73 exits mint"; note nothing mints them now and the reader stays for TC-253.
- The RESYNC entry ("Owner-registry gates for queued work") omits the changed prompt template; add it with the fix.
- `schedule.py`'s header claims it never imports sibling engines; `_load` now lazily imports `spine_carrier`. Qualify the claim.
- A row with both a pending `wi_refs` gate and an unmet work-item predecessor reports only `blocked` (cosmetic).
- `traj_status._frontier_lines` has an odd `out = []` reset (works; untidy).

**Checked and correct:** one shared readiness predicate (`schedule.py:477-492`, mutex at 667; dispatch, integrate, traj_status, agent_brief all through `schedule._load`; census/consolidate use only ordering); non-vacuous tests incl. release on ruling with spec bytes unchanged; dangling `wi_refs` checks ruled rows and sees archived WIs; OI-98/OI-99 well-formed; status.md hand edit only the paragraph; PROCESS.md +131 stamped, three guard copies identical; ratchet re-stamps pass.

**Commands:** `pytest -q -n 2 tests/test_open_item_readiness.py tests/test_schedule.py tests/test_traj_status.py tests/test_intake.py`: `167 passed in 62.30s`; `check_trajectory.py --strict`: clean (745 WIs, 665 done); `pytest -q tests/test_module_size_ratchet.py tests/test_dogfood_sync.py`: `45 passed, 1 skipped`.
