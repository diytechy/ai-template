# WI-902 adjudication 013: lane checkpoint at 6bf895323 (amendment)

This judges LLR-335 and TC-360, approved at sitting 007, against the code as settled by rounds 5 and 6 (rulings 009 DB and 011 DC, review 010 F2). The LLR and TC rungs are released.

**What I checked:**
- **The text matches the code.** `_landing_commit` (`intake.py:1838-1856`) takes the oldest first-parent touch, and returns None when git names none or when that touch is a shallow-boundary commit (`retire.shallow_boundary`). `_tree_text` (`intake.py:1880-1891`) decodes `git show` bytes as strict UTF-8. `adoption_lineage` judges the close in the working tree and every sweep in the landing tree through one `row_refusal` rule.
- **The trace cells are current.** All 14 symbols in LLR-335's `CodeSymbol` exist, including the new `work_specs`, `_landing_commit`, `_tree_specs` and `_tree_text`. No registry row or live code still names the removed `_landed_before` or the deleted lineage-only test. The one remaining mention is a historical reason string in `tests/test_module_size_ratchet.py`.
- **All 18 TC-360 `Evidence` tests exist, and the new ones assert what the Method claims:**
  - `test_a_rejected_adoption_stays_refused_on_replay` runs for `complete` and `cancelled`; the replay exits 1, the dependent is unchanged and HEAD is unchanged.
  - `test_an_adoption_whose_landing_lies_past_a_shallow_boundary_refuses` runs for accepted and refused landings, on a real `_shallow_clone`; each refuses with nothing written and a clean status.
  - `test_an_adoption_whose_landing_commit_cannot_be_read_refuses` refuses with nothing written.
  - `test_an_adoption_of_a_successor_whose_landed_spec_is_not_utf8_stays_refused` refuses at landing, and refuses again on replay after only the current file is repaired.

## amendment

- [MEANING] LLR-335 Detail -> the close and the landing sweep judge the current registry with the open-state rule, a later sweep replays a consumed adoption by lineage alone (any state, workspace or archive), and neither consumer changes any of the adopted row's cells -> the close judges trunk's working tree; every sweep, landing or replay, judges the same open-state and Supersedes rule in the tree of the commit that landed the disposition on the first-parent line, so a verdict reached at landing holds on replay; a landing git cannot name, including one hidden by a shallow boundary, refuses; the adopted spec in that tree is read as strict UTF-8, and invalid text refuses as unreadable; neither consumer changes the adopted item's identity, scope or Supersedes, though the shared re-point may rewrite its needs edge to the disposed item -> the replay source and rule changed, two refusal cases were added, and the no-change clause was narrowed. A correct implementation of the old text (lineage-only replay) fails the new one, the very difference ruling 009 turned on. **Blessed.**
  - Upward: judging "open and superseding" in the landing tree is SR-148's "names an already-open item that supersedes it" evaluated where the choice was made, and it closes the fail-open that ruling 009 found.
  - Sideways: it remains the single home of the adoption decision, and LLR-153 still cites it rather than restating it.
  - Downward: every arm has a named test in TC-360.
  - It has no `shall`, and each refusal is observable.
  - The narrowed no-change clause answers review 008 F2 and sitting 007's advisory 2.
- [MEANING] TC-360 Expected and Method -> verify open-state acceptance at first consumption, lineage-only replay of an archived or closed successor, invalid lineage refusing, and the full successor set with no id -> verify that the close accepts from the working tree and every sweep only when the successor is open and superseding in the landing tree; that an accepted adoption stays accepted after completion; that adoptions refused at landing (complete or cancelled successor) refuse again without changing the dependent or trunk; that an unreadable or shallow-hidden landing refuses with nothing written; that a non-UTF-8 landed spec is unreadable at landing and on replay after only the current file is repaired; and that the successor-set re-point and no-op replay hold -> the verification obligations were replaced and extended, since the old Method required lineage-only acceptance that the new one forbids. **Blessed.**
  - It is closed over LLR-335's amended arms.
  - Its Expected is a condition, not an instrument.
  - Its Evidence drops the deleted test and cites the four new regressions, which I checked above, so it claims nothing its tests do not show.

VERDICT: MEANING rows=2

**Aftermath:** this session re-attests both rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests LLR-335,TC-360`

SITTING: JUDGED kinds=amendment
