<!-- Claude Sonnet (Agent-tool subagent, model "sonnet", read-only) review of WI-721, build/wi-721 4dd6827d..3496344e. Built by Codex Sol; committed by the coordinator (the builder's sandbox refused git metadata writes). -->

3496344e SOUND

BLOCKER: none

MAJOR:
- `docs/requirements/low-level-requirements.toml`, LLR-286 `detail` (not changed by this commit) still reads "the id is SN, SR, LLR or TC with a nonzero number and is a live row of its tier's TOML registry".
  - This is now stale. `retire._judge` calls `live_ids` (`project-trajectory/scripts/retire.py:233-253`), which resolves liveness through `spine_carrier.load` / `load_need_tier`. That reader is carrier-agnostic.
  - The new test (`tests/test_retire.py:307-322`) proves that a CSV or Markdown row counts as live.
  - This drift is introduced by this change. The sentence was accurate before it.
  - Fix: drop "TOML" from LLR-286's `detail`. *Coordinator: in scope; amendment grant for fix round 1.*

MINOR:
- `docs/test/test-cases.toml`, TC-299 `evidence` does not list the new test `tests/test_retire.py::test_legacy_registry_rows_are_live_and_only_a_spent_id_is_reported`, beside its listed sibling `test_a_spent_id_without_a_record_is_reported`. *Coordinator: in scope for fix round 1.*
- `project-trajectory/scripts/spine_carrier.py:55-73`, the `Contract IF-102:` caller list omits `retire`, `check_test_first` and `rejudge`, which `interfaces.toml` IF-102 lists as requestors.
  - The drift predates this commit.
  - `retire.py` correctly carries no `Contracts: IF-102` marker, since a module lists only the interfaces it owns.
  - *Coordinator: folded into fix round 1.*

**Verification:**
- `live_ids` reads all four tiers through one carrier:
  - `spine_carrier.load` for SR, LLR and TC (`CARRIERS=(".toml",".csv")`);
  - `load_need_tier` for SN (`.toml`, `.md`).
- `-000` rows, absent registries and empty files behave as before.
- **One behaviour change:** a registry that exists but does not parse now raises instead of reading as zero rows. That matches every other spine reader's fail-loud policy, so it is not a regression.
- IF-102 already lists `scripts/retire`.
- **The new test** reproduces the defect faithfully:
  - it builds a legacy-carrier scaffold;
  - it bumps SR's watermark to 2;
  - it asserts one finding, naming SR-002 and no live row.

  It runs in the smoke tier, as the rest of the module does.
- The fixture description is now 132 characters, against a `DESCRIPTION_FLOOR` of 100 (`gen_skills_index.py:207`), which is unchanged.
- No golden was touched.

**Run:** `python -m pytest -q -n 2 tests/test_retire.py tests/test_generated_freshness_wiring.py tests/test_trace_golden.py -p no:cacheprovider` → **43 passed in 52.34s**.
