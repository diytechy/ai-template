# 110-REVIEW-A — WI-253 (dashboard edge routing)

Independent adversarial review (REVIEW-A) of commit `30ed4c9` on
`dualplan-routing-fix` (single build commit). Reviewer did not write the code and
read no builder self-assessment; judged the artifacts and drove the shipped
paths. Rubric: `docs/rubrics/code-review-adversarial.md`. The RENDER acceptance
(T8, `docs/rubrics/dashboard-usability.md`) is a separate critique session's
pixel judgment — this review covers the code and the driven behavior only.

## Scope / subject frame (R1)

An obstacle-aware wire router, `_route_edges`, single-sourced across the layered
emitters in `gen_trajectory.py`. Each emitter builds `(key, x1,y1, x2,y2, src,
tgt)` tuples and a `{id: rect}` map and calls the router; a wire whose direct
horizontal-tangent cubic already clears every **non-endpoint** box keeps the
LEGACY `d` byte-for-byte, a blocked wire detours through a clear horizontal LANE
(`_detour_d`) found nearest the endpoint midline, entering each port on a short
stub. Geometry is pure/deterministic (Liang–Barsky clip `_seg_hits_rect`, cubic
sampling `_cubic_points`, nearest-free-band `_clear_lane_y`). Blast radius: the
generated `PROJECT_STATE.html` render surface (When DAG, How-SW, Knowledge,
drill layers) + the WI-243 fail-closed staleness gate (this touches the render,
so a fresh critique is owed before the next green G3). Spec of record:
`docs/specs/WI-253.md`.

Worst failure classes hunted first (R3): nondeterminism / byte instability;
the router silently emitting a through-box wire (fail-open degrade); a dead
(non-biting) invariant test; geometry edge cases (endpoint-in-rect, stub-corridor
obstacles); an emitter wired but never exercised; O(n³) blowup on a large
registry.

## What I verified (driven, not assessed — R2)

**1. Byte-stable regeneration (Done-when #3).** Ran `--check` twice and a full
regenerate:
```
$ python project-trajectory/scripts/gen_trajectory.py --check   -> project-state dashboard up to date.  EXIT=0
$ python project-trajectory/scripts/gen_trajectory.py --check   -> project-state dashboard up to date.  EXIT=0
$ python project-trajectory/scripts/gen_trajectory.py           -> gen_trajectory: already up to date -> PROJECT_STATE.html
$ git status --short                                            -> (only OWNER_SCRATCHPAD.md; PROJECT_STATE.html unchanged)
```
Byte-identical. Determinism also driven directly: `_route_edges` over 200
random `dict`-insertion-order shuffles of the same rect map → **1 distinct
output** (no dict-order escape). Float path is `{:.1f}`-formatted throughout,
`t=i/n` IEEE division — cross-platform stable.

**2. The invariant tests BITE (revert-proof, R5-style).** Forced the router to
the legacy path (`_polyline_hits → False`, disabling all detours) and re-ran the
exact through-box scan the new tests use over the real meta panels:
```
[routed] How-SW: 0   Knowledge: 0   When: 0     through-box violations
[legacy] How-SW: 11  Knowledge: 464 When: 57    through-box violations   (532 total)
```
The three `test_meta_*_avoid_unrelated_boxes` tests would go red on revert; the
router genuinely eliminates 532 real through-box wires. `pytest -k "route_edges
or avoid_unrelated"` → **5 passed**. `test_route_edges_leaves_a_clear_wire_byte_
identical` pins the exact legacy cubic string, so any drift in the clear-wire
path fails it.

**3. All four wired emitters produce 0 through-box when driven (R2 / R4).** The
meta panels the invariant tests scan render `when_view`/`sw_containment` →
`_drill_layer_svg` (`class="wire"`) + `know_graph` (`kedge`). `dag_svg` and
`sw_graph` are **fallback-only** for this repo (`when_view(...) or dag`;
`sw_containment(...) or _sw_panel(..., sw_graph(...))`), so no test scans them.
I drove both directly and scanned their own output:
```
dag_svg : 286 edges (236 "edge" + 50 "edge soft") -> 0 through-box
sw_graph:  65 "swedge"                             -> 0 through-box
```
All four integrations are correct today; the automated invariant scan covers two
of them (see [MINOR] below).

**4. Geometry edge cases driven.**
- *Crowded lane:* col1 packed with 12 stacked boxes across the ±40 band — the
  router still lanes **outside** the whole obstacle band (detour used, 0
  through-box). `_clear_lane_y` always finds the topmost-edge−0.1 / bottommost-
  edge+0.1 candidate within the `[min−40, max+40]` span, so the "no clear lane →
  None" fallback is effectively unreachable when obstacles exist.
- *Endpoint-in-rect:* `_seg_hits_rect` correctly treats a zero-length segment
  inside a rect as a hit (all `pi==0`, `qi≥0`). Source/target rects are excluded
  from each wire's obstacle set, so a wire is never flagged against its own box.
- *Stub-corridor obstacle:* a box overlapping **only** the port stub zone
  (within `STUB=18px` of a port) is excluded from the lane search and the wire
  is NOT detoured — it keeps the direct cubic and passes through the box (see
  [MINOR]).

**5. Lint / complexity / dupes (the G3 quality gates).**
```
$ python -m ruff check project-trajectory/scripts/gen_trajectory.py   -> All checks passed!
$ python -m ruff check --select C901 ...gen_trajectory.py             -> 4 errors, ALL pre-existing
                                                    (_okf_nodes:15, + 3 others); no WI-253 helper listed
$ python -m pytest -q tests/test_complexity_ratchet.py                -> 1 passed
$ python project-trajectory/scripts/check_dupes.py --src project-trajectory/scripts
                                                    -> OK - no duplicate blocks in 34 file(s).
```
Every new helper (`_cubic_points`, `_seg_hits_rect`, `_polyline_hits`,
`_clear_lane_y`, `_detour_d`, `_route_edges`) is C901 ≤ 10; the single-sourced
router adds no copy-paste block. Stdlib-only, Python 3.8 interpreter.

**6. Performance proportionality (SN-012).** Timed `_route_edges` on synthetic
graphs: N=50/100e → 28 ms, N=150/300e → 204 ms, N=300/600e → 684 ms. ~O(E·N)
(quadratic), not O(n³); sub-30 ms at meta scale, bounded on a large downstream
registry, and it runs at regenerate/gate time, not a hot path. No finding.

**7. Smoke suite green.** `python -m pytest -q -n auto -m smoke` →
**991 passed, 3 skipped** (212 s).

## Done-when coverage map (R4)

| Done-when item | Status |
| --- | --- |
| No edge intersects an unrelated node rect (any tab/drill view) | **COVERED** — 0 across How-SW/Knowledge/When rendered panels (532→0 vs legacy, driven §2); dag_svg/sw_graph fallbacks also 0 when driven (§3) |
| Byte-stable regeneration (`--check` green twice) | **COVERED** — §1 |
| Crossings that remain occur in open space | **CRITIQUE-OWNED** — pixel judgment (T8), out of scope for code review |
| Fresh `*-CRITIQUE.md` passes T8 | **OUT OF SCOPE** — critique session (this build re-fires the WI-243 gate as designed) |
| Row `done`, Deliverable filled, SpecRef cleared, spec archived (R-F) | **OUT OF SCOPE** — close step; WI still `queued` during build+review |

Every code-verifiable Done-when item maps to a driven observation.

## Findings

- [MINOR] project-trajectory/scripts/gen_trajectory.py:1500 (`_detour_d`) -> a box
  overlapping ONLY a port stub corridor (within `STUB=18px` of a port) is dropped
  from `inrange`; if the direct cubic hits such a box, `_detour_d` returns `None`
  and the caller silently keeps the through-box direct cubic — a fail-open
  degrade. The docstring asserts the inter-column corridors "are kept empty", but
  the codebase already has 16px column gaps (`gen_trajectory.py:333`, the tier
  band layout) which are *narrower* than the 18px stub, so the guarantee rests on
  no wire happening to hit a box there rather than on geometry. Holds on all
  current rendered panels (invariant scan = 0, driven), so no live defect —
  downstream/robustness only -> after computing a detour, re-verify the full
  routed polyline clears every obstacle (fall through to a wider lane / different
  y if not), or fold stub-corridor obstacles into the tested set -> @owner
- [MINOR] tests/test_gen_trajectory.py:1930 (`test_meta_*`) -> the mechanized
  through-box invariant scans only the emitters the meta repo actually renders
  (`_drill_layer_svg` + `know_graph`); `dag_svg` and `sw_graph` are fallback-only
  here (`when_view or dag`, `sw_containment or sw_graph`) so no test exercises
  their routing integration, even though the build wires all four. I drove both
  directly → 0 through-box today (§3), but a future regression in those two
  integrations would not be caught by the suite -> add a synthetic-fixture scan
  over `dag_svg(...)` and `sw_graph(...)` output (both trivially constructible;
  the test regex already matches `edge`/`swedge`) so all four integrations are
  guarded -> @owner
- [MINOR] project-trajectory/scripts/gen_trajectory.py:820 (`sw_graph`) -> the
  edge label (`swlab`) is still anchored to the straight-chord midpoint
  `(x1+(x2-2))/2, (y1+y2)/2`, not updated to follow a detour, so a re-routed
  swedge's label floats off its wire (and may land over an unrelated box) — a T4
  attribution/legibility regression. `sw_graph` is fallback-only for meta (no
  live impact), but a downstream repo that renders it gets disconnected labels on
  detoured seams -> place the label on the routed path (the lane midpoint when a
  detour is taken) or anchor it to the lane segment -> @owner

All three are low-stakes and scoped to fallback/downstream paths; none affects the
meta repo's rendered Done-when. Every worst-class hunt (R3) — nondeterminism, a
silent through-box degrade on the live render, a dead invariant test, endpoint /
stub geometry, an unexercised emitter, O(n³) blowup — was driven and survived on
the shipped render.

- VERDICT: APPROVE findings=3
