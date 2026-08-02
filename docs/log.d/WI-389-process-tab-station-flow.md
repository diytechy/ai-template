## 2026-08-02 — WI-389: the Process tab draws the station/lane model

**SpecRef-clock re-validation (first act, standing WARN).** The row's SpecRef
(`docs/concurrency-v2.md`) changed after the row was minted: commit `f822e336`
(2026-08-01, "rulings: R3+R4 recorded and executed"). Diffed that commit's
concurrency-v2 hunk against the flow this row draws: the amendment RESTATES the
§B2 "Specs mirror it" paragraph (the spec-of-record archive stays one flat
folder — OI-11 ruled (a), WI-391's measurement) and touches nothing else in the
file. §A2 (station refresh + merge slot), §A3 (terminal outcomes), §A4
(dispatcher, barrier, empty-frontier ladder) and §A8 (policy arms) — the
sections this row's render draws — are untouched. The spec stands as written;
no re-scope needed.

**One line:** the Process tab's method picture is now the station cycle —
one directed SVG ring (claim → lane build → three terminal outcomes
converging on the station refresh → the serial merge slot → trunk advance →
intake mint → dispatcher tick), with the spine barrier gated onto the
admission edge and the intake arm visible; the WI-250 hoops and the
pre-station resume-loop chips delete.

**Deliverables:** `traj_panels.py` `_station_svg`/`_station_panel` (+
`STATION_GEOM`, `_ADMISSION_ARMS`, `_exclusive_kinds`, `_outcome_cards`,
`_station_card`, `_st_edge`; hoops/trig/`_loop_panel` deleted; 984→1145
lines, under the 1500 threshold); `gen_trajectory.py` re-export rename +
`--hub`→`--slot` token (950→952); the WI-389 station test suite in
`tests/test_traj_panels.py` (red-first: 9 failed pre-render) with the
derive-don't-pin discipline — outcomes/spec-dirs from
`integrate.OUTCOME_DIRS`, the attestation label from `integrate.BAR_GREEN`,
exclusive kinds from `schedule`'s ruled tables, and sync pins against
`dispatch._kind_action` + `intake.tier_signal` for the two label sets with
no exported constant; TC-051/TC-056 `Evidence` + LLR-056 `CodeSymbol`
(traced cells) re-pointed at the real tests/symbol.

**Pixel verification** (render-dashboard-critique matrix, 36 shots,
light+dark × 390/1280/1680, read back + 2x crops of the 1680 pair): ring
reads as a directed cycle, three arrowheads converge on the refresh, the
slot holds white-on-#4f46e5 in both themes, 390px scales without horizontal
overflow. Two findings driven out before close: the refresh card's
attestation note truncated mid-token at the 34-char budget (now
"green ⇒ Bar-Green @ branch tip"), and the lost-race dashed edge emerged
from under the slot card's shadow (start moved clear).

**Deviations from spec:** none from this row's own scope. Recorded for
WI-390 (the program close's spine scope): the RATIFIED prose of
SR-050/SR-055/LLR-051/LLR-056/TC-051/TC-056 still describes the
resume-loop/hoops picture this render replaced — only the traced pointer
cells moved here. Byte deltas on budgeted files: none (AGENTS.template.md /
PROCESS.md / PROCESS_OPTIONS.md untouched). PROJECT_STATE.html not
committed on the branch (§5.2 trunk-owned).

**Verification** (watched, work commit 56dc580d):
tests/test_traj_panels.py 34 passed in 6.12s
<!-- fig: cmd="python -m pytest -q tests/test_traj_panels.py" rev=56dc580d -->
smoke tier: 663 passed / 6 skipped in 13.14s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=56dc580d -->
full suite: 1959 passed / 10 skipped in 317.08s (0:05:17)
<!-- fig: cmd="python -m pytest -q -n auto" rev=56dc580d -->
`check_trajectory.py --strict` rc=0 · `check_doc_refs.py --strict` rc=0 ·
`check_figures.py --strict` rc=0.
