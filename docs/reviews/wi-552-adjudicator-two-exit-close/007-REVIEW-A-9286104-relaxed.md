# WI-552 REVIEW-A (007) — 9286104 (relaxed)

Independent unattended review of `WI-552-adjudicator-two-exit-close` at `9286104a`
(the REVIEW-A rework: cancelled-close refusal + scheduler/comment fixes).

Scope: `git diff contract_split...HEAD` (work under review, generated/telemetry
excluded), against AGENTS/PROCESS, the WI-552 spec-of-record
(`docs/archive/work/complete/WI-552-adjudicator-two-exit-close.md`), SR-144, and
the OI-70/OI-73 rulings.

Harness run by the reviewer (once each, summaries only):
- `trace.py --strict-integrity`: `SN=27 SR=76 LLR=188 TC=186 orphans=2 integrity=0 ... provenance-findings=1 paraphrase-advisories=3` — the LLR-197/SR-168/provenance advisories are pre-existing trunk state; the diff touches no `docs/requirements` spine row.
- `check.py --jobs 0`: `RESULT: PASS`.
- `pytest tests/test_intake.py tests/test_handback.py tests/test_dispatch.py tests/test_schedule.py tests/test_trajectory.py`: `194 passed in 49.44s`; structural `test_module_size_ratchet.py test_dogfood_sync.py test_dependency_ledger.py`: `46 passed, 1 skipped`.

Worst failure classes this change admits, hunted first: (1) fail-OPEN on the
refusal invariant — a partial/cancelled close queuing no successor slipping
through; (2) fail-OPEN on the typed OI edge — a `pending` open item satisfying a
successor's readiness; (3) silent content loss in the mechanical close /
inbound-edge rewrite. All three drove the real shipped paths.

Done-when map (each mapped to its covering test + a driven path, none UNCOVERED):
- DW1 (mechanical close) — `test_handback` close/merge tests + `dispatch._close_done_adjudication` wiring; read `close_adjudication`/`_adjudication_close_text`, confirmed specref cleared and Context/Dispositions preserved, idempotent Deliverable.
- DW2 (OI-mint gates successor) — `test_the_close_mints_a_pending_oi_that_gates_the_successor`, `test_the_oi_mint_refuses_on_a_non_toml_registry`; drove `hard_preds_satisfied` with a pending OI → `False`.
- DW3 (refusal invariant, incl. the CANCELLED gap 005 raised) — drove `intake.owes_successor` directly: cancelled/partial `dispose:` titles → `True`, spot-check/amendment/census → `False`; the pre-fix guard was `brief == "disposition"` (confirmed at `9286104^`), and the brief-less cancelled arm carries `brief=""`, so `test_the_refusal_invariant_stops_a_cancelled_close_with_no_successor` genuinely fails on pre-fix behavior. FIXED and covered at both the close-side (`close_adjudication`) and merge-side (`_disposition_drafts`) guards.
- DW4 (inbound-edge replacement) — `test_the_mint_replaces_inbound_edges_of_the_superseded_row`; see MINOR below on the single-line-`needs` corner.
- DW5 (typed OI edges) — drove `spine.split_pred_edges` (`~OI` collapses to a hard OI edge, no soft OI), `schedule._oi_satisfied` (pending→False, ruled→True, absent→False fail-closed), `check_trajectory.load_known_ois`/`_predecessor_errors`; `test_schedule`/`test_trajectory` OI tests green.
- DW6 (dead-dep → partial) — `test_open_wi_depending_on_partial_pred_is_flagged` + `_waiting_reasons` now emits `waiting:hard-pred-partial` (005's MINOR fixed).
- DW7 (contract text) — `adjudicate-disposition.template.md` now states successor-mandatory, `open_item` as a typed dependency (not a standalone exit), machine-performed close, and refusal-on-no-successor; CATALOG hash `0ff70d31d143` validated by the passing `prompt-catalog` gate. The two prior-round MINORs (partial dead-reason, the `_OI_PENDING` "row simply gone" comment) are both resolved.

An APPROVE means I tried to break it: I drove the cancelled-brief-less refusal, the OI-pending readiness gate, and the multi-line `needs` rewrite, and only the two cleanliness/robustness items below survived — both with a live backstop, neither a live defect.

## Findings

- [MINOR] project-trajectory/scripts/intake.py:1364 -> `_replace_inbound_edges` rewrites the superseded edge with the single-line regex `_SPEC_NEEDS_RE = ^needs\s*=\s*\[.*?\]\s*$` (no DOTALL), but `parse_spec_frontmatter` (tomllib) accepts a MULTI-LINE `needs = [\n ... \n]` array; driven directly, the regex matches the single-line form and MISSES the multi-line form (`single match: True / multi match: False`), so `subn` returns n=0 and the edge is silently left un-repointed (not added to `changed`, no error). The kit's own `write_spec_file` always emits `needs` single-line so no current spec triggers it, and arm 6 `dead_dependency_findings` (which reads the regenerated single-line CSV cell) still REPORTS the resulting strand — so DW4's guarantee degrades from "unrepresentable" to "merely visible" only for a hand-authored multi-line dependent, never silent data loss. -> either normalize the rewrite through the parsed frontmatter (re-serialize `needs`) instead of a line regex, or make `_SPEC_NEEDS_RE` DOTALL-tolerant, so a multi-line dependent is auto-repaired rather than falling through to the validator net. -> @owner
- [MINOR] project-trajectory/scripts/intake.py:305 -> `_OI_ID_RE = re.compile(r"^\[open_item\.(OI-\d+)\]", re.M)` is defined but never referenced (`next_oi_id` resolves the OI space through `trace.live_max_ids`, not this pattern); dead code beside the live `OPEN_ITEMS_REL` constant reads as an intended-but-unused parse path. -> drop `_OI_ID_RE`, or wire it where the OI id is actually scanned. -> @owner

VERDICT: APPROVE findings=2
