+++
id = "WI-366"
title = "Spread the port fans the WI-323 advisory critique measured FUSED (docs/reviews/WI-323-CRITIQUE.md, pixel-measured 2026-07-29): strokes leaving a shared port should reach >= 8 CSS px separation within ~15 CSS px of the port. Two named sites on the Roadmap DAG at 1680px: right of the unphased block's port (two edges at 2.5-3 CSS px pitch for ~55 CSS px of descent - reads as one thick line; was 3.5-5.5px and diverging BEFORE) and right of block 1's port (a NEW 25 CSS px fused stretch the WI-323 lane stack introduced - two edges render as one from y~378 to the port). The critic also found the How-SW emitter's new lanes at 8 CSS px pitch where the roadmap's floor is 10, plus a pre-existing 4.5px SW pair - unify the floor. The implementer's note stands: fan offsets are computed by the caller BEFORE routing, so corridor-aware fans need a two-phase pass - but the critic's ask is narrower (stagger departure offsets near the port), so measure whether the narrow form suffices before building the rewrite. Perceptual clause: no crossing-count proxy (standing rule); judged by before/after shots + the periodic advisory critique."
workstream = "dashboard"
specref = ""
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

DONE 2026-07-30. `_route_edges` now hands every SHARED port a **harness**: each
strand rises from the port center to its own `_FAN_PITCH` (8.0) height over
`_PORT_LEAD` (11) px, coasts to its own staggered turn-off (`_lead_rung`, capped at
`_LEAD_RUNGS` = 3 so the harness never exceeds 27 px of the 60 px column channel),
and only the REMAINDER of the span is routed. `_port_fan`'s step became
`_FAN_PITCH` and its cap became the row SLOT (`row_h + row_gap - _FAN_PITCH`, so a
port's outermost strand still clears its vertical neighbour's by a pitch) — it now
takes `row_gap`, which is the only caller-visible change (4 emitters). A
single-wire port is untouched, so every unfanned wire stays byte-identical.

**The narrow form alone was measured first and did NOT suffice.** Raising the fan
step 6.0 -> 8.0 with a wider cap left the `unphased` site at 0.47 px separation 15
px from the port (from 0.67): the offset only moved a CONTROL point, and where a
strand's fan rank and its WI-323-assigned lane disagreed the pair still crossed
back over itself at the port. The harness materializes the offset before any lane
can pull. The x-stagger is the second half and is also load-bearing: a vertical
offset collapses to `off * cos(angle)` on a near-vertical stroke, so 8 px of fan
read as ~4.7 px down a steep plunge until the strands' plunges were staggered in x
too. Turn-off ORDER matters as much as the stagger — furthest traveller first, or
the early diver crosses every strand it is still inboard of (measured: the naive
order made the aggregate worse, 92 -> 100 bad pairs).

**Measured, roadmap root layer, SVG user units (pixel-anchored at 1.000 CSS px per
user unit at 1680px), separation at 10/15/20/30 px along the stroke from the port:**

| site | BEFORE | AFTER |
|---|---|---|
| block 1's out port, the fused pair (WI-323's new 25px stretch) | 0.17 / 0.07 / 0.49 / 1.88 — never 8 px clear within 60 px, 50 px fused | 5.19 / **8.00** / 9.24 / 7.33 |
| `unphased`'s out port, 3 of 10 pairs | held at 0.27–4.4 for the whole 60 px window (the critique's 2.5–3 px over ~55 px of descent) | every pair reaches 8 px; the two tightest adjacent pairs at 16.9 / 18.9 px from the port, worst pair 39.9; min sep at 15 px rose 0.59 -> 6.15 |
| all 48 emitted layers, pairs not 8 px clear within 15 px | 118 of 271 | **62 of 271** |

**Pixel corroboration** (2x DPR, 1680px light, `*` = composited darker than a
single stroke = two strokes on the same pixels). Right of block 1's port: BEFORE
one 20-device-px `*` run at +10 CSS px — two edges rendering as one — and 5.5/7.0
px gaps at +5; AFTER three single-stroke runs with **7.8 / 8.0** px centre gaps at
+10 and 9.8 / 10.5 at +15. Right of `unphased`'s port: BEFORE the fan collapsed to
a single run by +15; AFTER five single-stroke runs at +10 with 10.5/5.0/6.0/9.5 px
gaps and 7.5/8.0 at +20. Before/after crops read as a fan-out instead of a thick
line, in both themes; no lane newly crosses a node box (the T8 sweep still passes
over every emitter) and 390/1280px are unchanged.

**The How-SW "8 px vs the roadmap's 10" is a RENDER-SCALE artifact, not an emitter
divergence** — both already share one `_LANE_SEP` = 10.0. Pixel-measured at
1680px: the roadmap root layer renders at 1.000 CSS px per user unit (it fits its
card), the How-SW root at 0.800 (904 natural units scaled to fit a ~723 px card by
`_svg_fit_style`), so the same 10 units render as 10.0 and 8.0 CSS px. Unifying the
CSS-px floor would need `_LANE_SEP` = 12.5 units, which WI-323's dialling note
already rules out (it pushes a lane out of the 22 px inter-row channel). Recorded
rather than "fixed" by moving a constant that would regress T8. The critique's
"pre-existing 4.5 px SW pair" could not be reproduced as a LANE pair: sw-0's lane
pitches are 10 / 60.2 / 70.2 / 80.2 units (8.0 / 48 / 56 / 64 CSS px). Its tightest
pairs are port-fan strokes, which this WI moves from 2.7 to 4.8 CSS px at 10 px
from the port.

**Deviations from spec.** (1) The harness is applied at BOTH ends, not only
departures: it is one helper used twice, and leaving arrival fans fused beside
fixed departure fans would have been arbitrary — the named sites are output ports.
(2) `_route_edges` gained four extracted helpers (`_port_strands`,
`_harness_ends`, `_routed_dx`, `_spliced_harness`) so it stays under the C901 bar
instead of earning a complexity-ratchet entry; that cost lines to save branches, and
the module-size baseline is re-stamped 5037 -> 5195 with its reason.

**Residue, stated.** The departure clause lands inside 15 px at block 1's port and
at 17–20 px for the tightest adjacent pairs at `unphased`'s (one pair at 40 px) —
better than fused, short of the letter at the 5-wire port. The `_LEAD_RUNGS` cap
gives no x-stagger to the shallow end of a >3-wire fan (the right end to give up: a
near-level strand leaves shallow, where the fan offset already reads as full pitch);
raising the cap moved one pair of 271, so the bound stays. The `unphased` INPUT fan
still has one pair that never gets 8 px clear within 60 px (it had three). The
periodic advisory critique judges the residue.
