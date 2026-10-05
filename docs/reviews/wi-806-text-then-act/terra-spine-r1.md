Drafted/amended spine rows only; no statuses changed.

- LLR-173 `detail`: before omitted the text-before-act constraint; after adds: “The copy rides an act whose approval-act registry rows change only Status … the text it records is committed earlier.” Why: records the new sequencing at the snapshot mechanism.

- LLR-173 `rationale`: before: “sound only while every amendment flips its row in the same commit…”; after: “Once text is committed before its approval act…” Why: removes the retired amend-plus-flip premise.

- LLR-245 `code_symbol`: before: `"refresh_refusal/_unattested_rows/..."`; after: `"refresh_refusal/_ledger_live_rows/_unattested_rows/..."`. Why: names the extracted helper.

- LLR-245 `detail`: before: “minus the rows the act flips minus the rows named by --reattests”; after: “minus the rows named by --reattests”. Why: a flip no longer subtracts drift.

- LLR-298 `code_symbol`: before omitted `_commit_parents` and `_each_lane_commit`; after includes both. Why: they are now its shared ruling-sync helpers.

- LLR-302: new, Drafted, under SR-140: “Approval-record text is committed before the approval act.” Why: separates the two-tree sequencing/landing guard from LLR-178’s mirror invariant.

- TC-173 `verifies`: before `["SR-179", "LLR-178"]`; after `["SR-179", "LLR-178", "SR-140", "LLR-302"]`. Why: preserves the mirror pairing and correctly pairs LLR-302 with SR-140.

- TC-173 `method`, `expected`, `evidence`: before covered only the mirror-invariant suite; after also specifies and cites the mixed-commit, two-commit, no-verify landing, refresh-merge, and squash tests from `test_text_then_act.py`. Why: verifies LLR-302 with actual test functions.

- `id-watermark`: `LLR = 299` → `LLR = 302` via `trace.py --bump-ids`.

Builder-list disposition:

- Confirmed: new separation LLR under SR-140, LLR-173/245/298 amendments, TC-173 expansion, no SR-140 or LLR-178 amendment, and no IF-129 amendment.
- Refuted TC-167 addition: its evidence does not exercise the new two-tree policy; TC-173 is the appropriate existing carrier.
- SN-029 was not edited, per the human-held rule. Proposed owner amendment: replace “the one signal the sanctioned amend-and-flip path would otherwise hide” with “the one signal a Status transition would otherwise hide.”
- Back-link retagging is code work and was not performed. Required tags:
  - `acceptance_record` `_text_changes`, `_row_text_moves`, `text_then_act_lines`, `commit_text_then_act_lines`, `staged_text_then_act_lines`: `Implements: SR-140, LLR-302`
  - `check` `_text_then_act_refusal`, `_text_then_act_mode`: `Implements: SR-140, LLR-302`
  - `integrate` `_text_then_act_refusal`: `Implements: SR-140, LLR-302`
  - `integrate` `_each_lane_commit`: retain `Implements: SR-148, LLR-298` and add `SR-140, LLR-302`.

Checks:

- `trace.py --bump-ids`: `LLR 299 -> 302`.
- `trace.py --strict`: integrity `0`; exits nonzero only for the documented pre-existing `LLR-292 Detail uses 'minimal'` finding.
- `check_trajectory.py --strict`: blocked by pre-existing unrelated stranded `WI-803` claim/ref error.
- `tests/test_text_then_act.py`: `12 passed`.
- `tests/test_spine_carrier.py`: `25 passed`.
- Relevant baseline tests: `2 passed`.
- TOML parse and `git diff --check`: passed.

The combined requested pytest command and `test_trace.py` exceeded the environment’s 30-second command window, leaving locked temp workers; I stopped those specific orphaned workers. Their complete summary could not be obtained in this environment.