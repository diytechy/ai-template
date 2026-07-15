# 078-REVIEW-A — WI-163 (per-WI critique budget + exhaustion dial)

Independent review of commit `5007b88` (WI-163: add per-WI critique controls),
built session 077. Reviewed the diff against the spec-of-record
(`docs/specs/owner-intake-2026-07-14b.md#critique-budget`), the WI-163 registry
row, the PROCESS_OPTIONS "Critique verification & the critique loop" contract,
the work-items scaffold template, and the `agent_route.failure_action` gate-policy
surface. No SN/SR/LLR/TC rows were added or changed (off-spine `unattended` work
+ the derived arch code-map), so no registry sweep applies; this is a BUILD
commit, not a G1/G2 Status-change ratification, so no `--ratify` hierarchy applies.

## Harness run (observed, not reported)

- `python project-trajectory/scripts/check.py` (derived gate **G3**, tier all) →
  `RESULT: PASS` — all 15 steps PASS incl. `tests+coverage` (188.5s), `format`,
  `lint`, `dupes`, `derived-gate`, `traceability`, `doc-navigability`,
  `arch-map`, `trajectory-map`, `okf`, `skills-sync`, `trajectory` (`--strict`
  clean, 167 WIs, graph acyclic).
- `python -m pytest -q tests/test_agent_loop_critique.py` → `9 passed in 34.27s`
  (incl. the new `inf`, `move-on`, `block` shapes and the legacy default-path
  exhaustion test).
- `python project-trajectory/scripts/trace.py` → `SN=24 SR=56 LLR=57 TC=57
  orphans=0 integrity=0 components=5 interfaces=52`.
- `python project-trajectory/scripts/check_docs.py --stale` → `OK` (0 broken; the
  4 "possibly stale" hints are pre-existing archive/spec docs, not this diff).
- `wc -c project-trajectory/PROCESS_OPTIONS.md` → `138370` — matches the
  re-stamped byte-budget baseline in all three tracked `byte-budget-guard` SKILL
  copies (`137,877 → 138,370`, +493 B, flagged in the WI log).

## Assessment

The change is correct and satisfies every Done-when in the spec. `critique_control`
resolves the per-scope dial by reading the in-scope WI rows by column *name*
(`DictReader`), so a registry that never adds `CritiqueBudget`/`CritiqueExhaustion`
(including the kit's own 10-column `work-items.csv`) reads `None → "" → default`
— the never-breaking guarantee, and the reason the full G3 suite passes without
the kit registry carrying the new columns. Absent/`0`/negative/non-integer cells
fall to `default_max` (== `AGENT_CRITIQUE_MAX`), so the default path is behavior-
identical to the prior `critique_rounds >= critique_max` check; the legacy
`test_critique_budget_exhaustion_pages_human` (AGENT_CRITIQUE_MAX=2 → exit 7)
still passes, confirming it.

Batch composition is coherent and honors the most-demanding member on each
independent axis: `inf` (`None`) short-circuits to unbounded, else `max(budgets)`;
`block` outranks `move-on`. The exhaustion gate `if fa["mode"] == "attended" or
critique_exhaustion == "block"` forces `NEEDS-HUMAN`+`EXIT_NEEDS_HUMAN` under
*every* gate policy for `block` (attended already paged; autonomous/single-ratify
now also page), matching "block forces the page across gate-policies" — the
autonomous `block` case is covered by the parametrized test (exit 7 + NEEDS-HUMAN),
`move-on` under autonomous correctly falls through to DESIGN-CHECK (exit 6). `inf`
never trips the budget branch (`critique_limit is not None` guard) and is bounded
only by `--max-iterations`/session caps/pause-blackout, exactly as the runaway
guards are named in PROCESS_OPTIONS and the log — the inf test hits the iteration
ceiling (exit 6) without ever printing "budget exhausted".

The `build_scope_srs` → `build_scope_wis` split is behavior-preserving (the
dropped `if not wi_ids: return set()` early-out only skipped an empty loop that
now yields the same empty set), and `scope_wis`/`in_scope` are computed from the
same `commits` range so the dial applies to exactly the WIs that produced the
in-scope Critique SR(s). Both refactored helpers have a single caller each; the
derived `docs/architecture.md` code-map lists all three helpers and passes
`--check`. PROCESS_OPTIONS, the scaffold template (12 columns, `-000` row
inert/well-formed), the kit-contents README row, status.md (forward-only: WI-163
dropped as done per R-D, `next-wi` → WI-166), log.md, and the WI row are all
coherent; declared policies (`push-policy: human`, run-state RUNNING) match the
prose. Generated artifacts (`PROJECT_STATE.html`, `docs/architecture.md`) are in
sync. No defects found.

## Findings

(none)

VERDICT: APPROVE findings=0
