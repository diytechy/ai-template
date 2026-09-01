# WI-552 REVIEW-A (009, relaxed) — the adjudicator's two exits

Independent review of `contract_split...HEAD` (HEAD `f1a7e6b8`, tree clean).
Requirement surface: `docs/archive/work/complete/WI-552-adjudicator-two-exit-close.md`
Done-when 1–7 (OI-70 as refined by OI-73).

## Harness (run once each, this reviewer's boxes)

- `python3 project-trajectory/scripts/check.py --jobs 0` → `RESULT: PASS`
  (registry-integrity PASS; orphans=2 / provenance-finding=1 are the
  pre-existing LLR-197 residue, untouched by this diff — no spine rows minted).
- `python3 project-trajectory/scripts/trace.py --strict-integrity` →
  `SN=27 SR=76 LLR=188 TC=186 … integrity=0`.
- `pytest -q tests/test_handback.py tests/test_intake.py tests/test_dispatch.py
  tests/test_schedule.py tests/test_trajectory.py tests/test_module_size_ratchet.py`
  → **1 failed, 196 passed**. The failure is `test_module_size_ratchet.py::
  test_module_sizes_exactly_match_the_committed_baseline`, and it reproduces
  under `-m smoke` (the per-commit bar) on the clean committed tree.

## Done-when coverage (verified, not read)

1. Mechanical close → `test_the_mechanical_adjudication_close_archives_terminal_and_finishes`. ✓
2. OI mint gates successor → `test_the_close_mints_a_pending_oi_that_gates_the_successor`,
   non-TOML refusal `test_the_oi_mint_refuses_on_a_non_toml_registry`. ✓ (minted row
   carries title/status/raised/one_line/wi_refs; `_brief_cards` omits the absent
   decision/options/recommendation fields rather than erroring — sparse but valid.)
3. Refusal invariant, both arms and both guards → `test_the_refusal_invariant_stops_a_
   disposition/..._cancelled_close_with_no_successor` (close-side) and
   `test_a_cancelled_close_with_no_successor_is_refused_at_merge` (merge/self-close side).
   The cancelled regression models `brief=""`, so it fails against the old brief-only
   guard — the pre-fix behavior the fix targets. ✓
4. Inbound-edge replacement → `test_the_mint_replaces_inbound_edges_of_the_superseded_row`
   (hard re-pointed, soft `~` left on the terminal row). ✓
5. Typed OI edges → `kitlib.spine.split_pred_edges` single-homes the grammar;
   schedule/validator/dashboard callers all thread `oi_status`; watermark OI space is
   raised by `_mint`'s `bump_watermark` (`_offspine_ids` counts open-items.toml, so no
   id-collision gap). ✓
6. `dead_dependency_findings` extends to `partial` (`_DEAD_PRED_STATES`); scheduler
   `waiting:hard-pred-partial` reason matches. ✓
7. ADJUDICATE brief + template CSV + PROCESS_OPTIONS prose widened tolerantly, CATALOG
   digest re-stamped. ✓

## Findings

- [BLOCKER] tests/test_module_size_ratchet.py:1929 -> the committed `intake.py` baseline is 1179 SLOC but the module measures 1177 (`check_complexity.module_sloc`), so `test_module_sizes_exactly_match_the_committed_baseline` FAILS — verified red under `-m smoke` on the clean HEAD `f1a7e6b8`. The per-commit bar is therefore red and the WI Deliverable's "Smoke tier green within budget; full unfiltered suite green (close commit)" is false; a later ruff/format pass shrank intake.py without the ratchet being re-stamped down in the same commit (this file's own rule). -> Re-stamp the `intake.py` entry to `1177` with a `RE-STAMPED DOWN -2` note, then re-run `pytest -q -n auto -m smoke` to confirm green before the close. -> @owner

    VERDICT: CHANGES-REQUESTED findings=1
