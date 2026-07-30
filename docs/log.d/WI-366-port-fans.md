## 2026-07-30 — WI-366: the port harness (WI-323 advisory critique, follow-up 1)

**Summary.** Every shared port on every routed view now hands its wires a
**harness**: each strand rises from the port center to its own 8 px fan height
over 11 px, coasts to its own staggered turn-off, and only the remainder of the
span is routed — so the fan step IS the rendered pitch, and a pair that both
plunge steeply out of the port gets a horizontal gap as well as a vertical one.
The two sites [WI-323-CRITIQUE.md](../reviews/WI-323-CRITIQUE.md) pixel-measured
as fused are no longer fused.

**Deliverables** (`project-trajectory/scripts/gen_trajectory.py`):
`_port_fan`'s step is `_FAN_PITCH` (8.0, was a bare 6.0 the render damped to
~2.6) and its cap is the ROW SLOT rather than a fraction of the block, so a
port's outermost strand still clears its vertical neighbour's by one pitch — it
takes `row_gap` now, the one caller-visible change (4 emitters). `_route_edges`
grew the harness: `_harness_seg`, `_lead_rung`, plus `_port_strands` /
`_harness_ends` / `_routed_dx` / `_spliced_harness` extracted so it stays under
the C901 bar. A single-wire port is untouched, so every unfanned wire is
byte-identical. Four new unit tests on the pure geometry (pitch, row-slot cap,
turn-off order, and the harness reaching the pitch near the port) plus the
byte-identity of a lone port; the perceptual half stays with the shots and the
periodic critique (no crossing-count proxy — standing rule).

**Measured** (roadmap root layer, SVG user units, pixel-anchored at 1.000 CSS px
per unit at 1680px; separation at 10/15/20/30 px along the stroke from the port):
right of block 1's output port the fused pair went **0.17 / 0.07 / 0.49 / 1.88 →
5.19 / 8.00 / 9.24 / 7.33** (it had never reached 8 px within 60 px, running 50
px fused); right of `unphased`'s output port three of ten pairs had held at
0.27–4.4 px for the whole 60 px window — the critique's 2.5–3 px over ~55 px of
descent — and every pair now reaches 8 px, the two tightest adjacent ones at 16.9
/ 18.9 px from the port. Across all 48 emitted layers, pairs failing to get 8 px
clear within 15 px of a shared port: **118 of 271 → 62 of 271**. Pixel
corroboration at 2x DPR: right of block 1's port the single 20-device-px
composited-dark run at +10 CSS px (two edges as one line) is now three
single-stroke runs 7.8 / 8.0 px apart, and 9.8 / 10.5 px apart at +15.

**Deviations from spec.** The narrow form was measured FIRST, as the spec asked,
and did **not** suffice — the step raise alone left the `unphased` site at 0.47
px, because the offset only moved a control point and the WI-323 lane assignment
then pulled the strands back across each other; recorded rather than skipped. The
harness is applied at BOTH ends, not only departures (one helper used twice;
leaving arrival fans fused beside fixed departure fans would have been
arbitrary). The critique's "How-SW lanes at 8 px against the roadmap's 10" is a
**render-scale** artifact, not an emitter divergence: both already share one
`_LANE_SEP` = 10.0, and the pixel-measured scale is 1.000 CSS px/unit for the
roadmap root against 0.800 for the How-SW root (904 natural units fitted to a
~723 px card by `_svg_fit_style`). Unifying the CSS-px floor would need
`_LANE_SEP` = 12.5 units, which WI-323's own dialling note rules out — so it is
recorded, not "fixed" by a constant that regresses T8. The 4.5 px SW pair could
not be reproduced as a lane pair (sw-0's lane pitches are 10 / 60.2 / 70.2 / 80.2
units); its tightest pairs are port-fan strokes, 2.7 → 4.8 CSS px at 10 px out.

**Residue, stated.** The clause lands inside 15 px at block 1's port and at 17–20
px for the tightest adjacent pairs at the 5-wire `unphased` port (one pair at 40
px). The `_LEAD_RUNGS` cap leaves the shallow end of a >3-wire fan without an x
stagger — the right end to give up, and raising the cap moved one pair of 271.
The `unphased` INPUT fan still has one pair that never gets 8 px clear within 60
px (it had three). WI-367's clipped wrap-around stubs are untouched.

**Bars (real output).** Full unfiltered suite `python -m pytest -q -n auto` before
close: **1671 passed / 11 skipped / 2 failed (595s)** — both failures are standing
work-branch conditionals, verified red on the pristine branch tip before any edit.
`test_scaffold_omissions_list_is_current` went green when the spec moved out of
`docs/work/active/`; `test_this_repo_is_not_a_work_branch` stays red for the whole
branch by WI-357's design (the claim commit put `docs/work/active/wi-366-port-fans/`
into reachable history, and `_work_branch` reads history so the freshness gates
cannot re-arm inside the closing commit) — it re-greens on the trunk after merge.
Smoke `-m smoke` after close: **553 passed / 1 failed** (that same conditional).
`check_docs.py --root . --stale` green; `check_trajectory.py --strict` clean.

**Byte deltas on budgeted files:** none (PROCESS.md, AGENTS.template.md,
PROCESS_OPTIONS.md untouched). Module-size ledger: gen_trajectory.py **5037 →
5195**, reason in the ledger entry (five small helpers plus the prose recording
why a control-point-only fan damps, why turn-off order is load-bearing, and where
the cap's residue lands); re-stamps down with WI-280.
