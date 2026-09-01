# WI-552 REVIEW-A (016) — the adjudicator's two exits (OI-70/OI-73)

Independent review of `contract_split...HEAD` (relaxed hold). Scope: the seven
Done-when arms of OI-70/OI-73 — mechanical adjudication-row close, typed OI
mint, refusal invariant, inbound-edge replacement, typed OI `needs` edges,
the validator net, and the contract text. No SN/SR/LLR/TC registry rows change
in this diff (`docs/requirements` / `docs/specs` untouched), so the new-row
cross-sweep is vacuous.

## Harness (run by the reviewer, summaries only)

- `python project-trajectory/scripts/check.py --jobs 0` → **RESULT: PASS**
  (registry-integrity/vocabulary/need-form/privacy/doc-navigability/skills-index/
  prompt-catalog/staged-divergence/approval-immutable all PASS; derived-stage &
  approval-fresh SKIP on a work branch by design).
- `python project-trajectory/scripts/trace.py --strict-integrity` →
  `integrity=0 orphans=2` (orphans + LLR-197 finding are pre-existing, not in
  this diff).
- `pytest tests/test_handback.py tests/test_intake.py tests/test_schedule.py
  tests/test_dispatch.py tests/test_trajectory.py tests/test_module_size_ratchet.py`
  → **197 passed** (61.26s). Module-size ratchet green (prior REVIEW-A re-stamp
  landed).

## Behavior driven directly (not just tests read)

- `kitlib.spine.split_pred_edges` — `WI`/`~WI`/`OI` partition correct; `~OI`
  coerced to a hard OI edge (no soft-OI); bare-WI grammar unchanged.
- `schedule.hard_preds_satisfied` — a `pending` OI edge is NOT satisfied, a
  `ruled` OI edge IS, an OI id absent from the map is NOT (fail-closed). A
  missing `oi_status` holds the WI `waiting` — the worst class (scheduling a WI
  whose OI is still pending) is structurally impossible: absence → not-satisfied.
- `schedule._waiting_reasons` — emits `waiting:open-item-pending:OI-###` and
  `waiting:hard-pred-partial:WI-###`; never empty.
- `check_trajectory.dead_dependency_findings` — now fires on a `partial`
  predecessor; `validate` reports a dangling `OI-###` edge against the
  open-items id set.
- `intake.intake_after_merge` end-to-end (via tests): the mechanical close
  archives terminal + mints the drafted successor at merge; the OI mint lands a
  `pending` OI in the successor's `needs`; the inbound hard edge of a superseded
  row re-points to the successor while a `~`-soft edge is left alone; a
  brief-less CANCELLED close with no successor is refused (the exact gap
  REVIEW-A(005) found — regression is genuine, the merge-side guard is new so
  the pre-fix path returned no refusal).

All caller sites of `frontier`/`evaluate`/`simulate`/`hard_preds_satisfied`
thread `oi_status` (dispatch `_admit`, integrate `_claim_refusal`, traj_status,
traj_panels, schedule CLI); the OI-mint keeps the watermark consistent because
`bump_watermark` raises the OI mark off `live_max_ids`, which reads the
appended `open-items.toml` row. Byte-budget ledger matches on-disk bytes
(PROCESS_OPTIONS.md 181,326; SKILL.md 4,829 ≤ 5,000), three SKILL.md copies
identical.

## Findings

- [MINOR] project-trajectory/scripts/check_trajectory.py:812 -> `validate`'s docstring says a non-adopter's OI edge (`known_ois=None`) is "left to the scheduler's fail-closed `waiting`", but the code coerces `None -> frozenset()` so every `OI-###` edge is reported as a hard dangling-edge ERROR — vacuous for real repos (a registry-less repo carries no OI edges) yet the stated intent and the behavior disagree, and it nominally breaks the "validator ERROR and scheduler waiting cannot disagree" principle in the None case -> reword the docstring to state that None reports OI edges as dangling (defensive), or skip OI resolution when None -> @owner
- [MINOR] project-trajectory/scripts/intake.py:304 -> `_OI_ID_RE` is defined but never referenced anywhere (the OI mint derives ids from the watermark via `next_oi_id`, not this regex) -> delete the dead constant -> @owner

VERDICT: APPROVE findings=2
