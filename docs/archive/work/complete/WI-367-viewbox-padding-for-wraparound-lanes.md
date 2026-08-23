+++
id = "WI-367"
title = "Give the DAG SVG viewBox left/right padding so wrap-around lanes visibly connect instead of ending in clipped stubs: the WI-323 advisory critique (docs/reviews/WI-323-CRITIQUE.md) measured hard ink boundaries at x=22/x=1406 (1680px, 2x DPR) where every U-turn lane terminates flat and its continuation re-enters 5 CSS px away - 'a long horizontal line that stops at nothing, and a curve that starts from nothing'. PRE-EXISTING (identical structure in the BEFORE shots; the WI-257 backward-edge stubs), but now the dominant unattributable feature because WI-323 fixed the corridor body it hid behind, and WI-323's spreading pushed ~30% more edge ink against the clip. Until a wrap-around lane visibly connects to its port, T8's one-source-one-target clause cannot fully pass regardless of corridor quality (the critic's ranked follow-up 2). Judged by before/after shots; no mechanized proxy."
workstream = "dashboard"
specref = ""
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

DONE 2026-07-30. **The critique's open question is answered from the code: it is a
viewBox CLIP, not a routing margin.** Every emitted diagram declared
`viewBox="0 0 width height"`, and that `width` is the LAYOUT box `_layered_layout`
returns (`pad * 2 + nranks * col_w + (nranks - 1) * col_gap`, `pad` = 18 roadmap /
16 How-SW) — the node grid plus its margin, and nothing else. The router
deliberately sends a wrap-around (backward) edge around the OUTSIDE of its own
endpoint boxes: `_detour_d` turns its lane at `x1 + _WIRE_STUB` / `xe - _WIRE_STUB`
(18 px), a WI-366 harness lead (11–27 px) further out again. At rank 0, and at the
last rank, that turn lands outside `[0, width]` and the SVG viewport cuts it.

Measured on the shipped dashboard in SVG user units — the four layers with outboard
ink, out of the dashboard's 49 drill layers:

| layer | box | wire ink | over L | over R |
|---|---|---|---|---|
| `when-0` — the roadmap ROOT, the critique's site | 0..692 | −17.5 .. 711.0 | 17.5 | 19.0 |
| `when-1` | 0..585 | −6.5 .. 596.0 | 6.5 | 11.0 |
| `when-22` | 0..996 | −6.5 .. 963.0 | 6.5 | — |
| `sw-0` — the How-SW ROOT | 0..904 | 0.0 .. 923.0 | — | 19.0 |

Every extreme is a lane's own `L` endpoint, not a control point — e.g.
`… 703.0,146.9 L-17.5,146.9 C-8.5,146.9 …`, which is exactly the critic's "long
horizontal line that stops at nothing". Both routed-SVG tabs were affected, so both
are fixed.

**The fix grows the box to the ink, not the ink to the box.** Pulling the U-turn
back inside would push it through its own endpoint box — the defect WI-257 removed —
and widening `pad` instead would grow *every* layer, shrinking 45 diagrams to fix
four. `_svg_frame` measures the outboard ink off the emitted BODY (the
`_svg_role` precedent, so no emitter has to remember it and a successor emitter
cannot forget it), adds `_INK_PAD` = 2.0 to clear the widest stroke's 1.25
half-width, rounds out to whole units, and grows the declared natural `width` with the box so a diagram
that already fits its card keeps its scale. `_path_xs` bounds the ink from the
control hull rather than sampling — on this dashboard the bound is exact, since every
extreme is an endpoint — and stops at a command it does not know rather than reading
that command's arguments as coordinates. `<defs>` is cut before the scan: a
`<marker>`'s path is drawn in the marker's own viewBox, not user space. AFTER:
`-20 0 733 354`, `-9 0 607 286`, `-9 0 1005 490`, `0 0 925 150`, and zero outboard
ink anywhere in the document.

**Measured before/after, 2x-DPR shots, 1680px** (1280px renders identically — both
sit at the 1120px `.wrap` cap, and the page heights moved by the same 10 device px):

| | BEFORE | AFTER |
|---|---|---|
| roadmap root, flat terminations at the box edge | every wrap-around lane, both edges | none |
| roadmap node box (device px) | 240 | 237 |
| roadmap fit scale (CSS px per user unit) | 1.000 | 0.9877 (−1.23%) |
| How-SW port-to-port pitch (device px) | 371.0 | 362.75 |
| How-SW fit scale | 0.800 | 0.782 (−2.23%) |
| How-SW 12px label, rendered | 9.60 px | 9.38 px |
| 390px roadmap node box (device px) | 150 | 150 (unchanged) |

The 390px column is unchanged *by construction*: below the legibility floor the SVG
renders at `min-width` = `SHRINK_FLOOR` × its OWN natural width, so a wider natural
width cancels exactly and only the scroll extent grows (page height 6358 device px,
before and after; no new `.scrollcue`). At 1280/1680 the roadmap card is ~724 CSS px
wide, so the 692→733 box crosses from "fits" to "fit-scaled" and pays 1.23%; the
How-SW root was already fit-scaled and pays the full 904→925 ratio. Both are far
above `SHRINK_FLOOR` (0.62) and the labels stay crisp in the crops.

**No port-fan regression.** The whole-document diff is four `<svg>` open tags plus
the `state as of commit` stamp — every `d` is byte-identical, so WI-366's user-unit
separations are untouched. Their RENDERED CSS-px values move by the same −1.23% /
−2.23% the diagram does (block 1's out-port pair: 8.00 → 7.90 px at 15 px from the
port). That is a render-scale artifact, the same class WI-366 recorded for the
critique's "How-SW 8 px vs the roadmap's 10" finding, not a geometry change.

**Tests** (`tests/test_gen_trajectory.py`, no perceptual proxy, no pixel
assertions): `test_svg_viewbox_contains_every_routed_wire` sweeps every emitter that
really renders and asserts each SAMPLED wire polyline sits inside its own viewBox
with the full `_INK_PAD` clearance. It EXCLUDES the repo's own committed
`PROJECT_STATE.html` — that artifact's freshness belongs to the trunk lane, not to a
work branch (concurrency-restructure §5.2), so reading it would assert this emitter's
property against markup an older one wrote, a standing red on every work branch — and
replaces what it contributed with a `WRAPAROUND_WIS` fixture whose rank-0 item
carries a SOFT edge after the last rank, generated inside the test run. Non-vacuity
is ASSERTED, not assumed: that fixture must emit a padded (negative min-x) box, or
the sweep is the tautology that an emitter which never routes outboard never clips.
`test_svg_frame_pads_only_the_side_that_carries_outboard_ink` pins the
roadmap's measured numbers; `test_svg_frame_leaves_a_diagram_with_no_outboard_ink_untouched`
locks the byte-identity of the other 45 layers (including the `-0` formatting trap
and the `<defs>` cut); `test_path_xs_reads_the_emitted_vocabulary_and_bails_on_anything_else`
covers the relative `h` and the unknown-command bail.

**Deviations from spec.** (1) The spec says "the DAG SVG"; the same clip was
measured on the How-SW root layer and on two roadmap drill layers, and the fix is in
the shared wrapper, so all four are covered — scoping it to one layer would have
meant writing the same rule twice. (2) `_INK_PAD` is a small constant, not a
dialled one: it exists so a stroke's half-width is inside the box, not to create
visual margin. (3) The module-size baseline is re-stamped 5195 → 5274 with its
reason (`tests/test_module_size_ratchet.py`).

**Residue, stated.** The How-SW root layer renders 2.23% smaller at 1280/1680 —
unavoidable while its card is ~724 CSS px and its natural width is 925; the only
lever that would recover it is widening the panel's diagram column, which is a
layout change this WI does not own. Whether the reconnected U-turns now read as
attributable end-to-end is the periodic advisory critique's call, not this
implementer's.
