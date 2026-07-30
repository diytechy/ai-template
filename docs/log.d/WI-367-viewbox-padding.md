## 2026-07-30 — WI-367: the viewBox holds the wrap-around lanes (WI-323 advisory critique, follow-up 2)

**Summary.** Every emitted diagram declared its `viewBox` as the LAYOUT box — the
node grid plus `pad` — while the router deliberately sends a wrap-around (backward)
edge around the OUTSIDE of its own endpoint boxes, so at rank 0 and at the last rank
the SVG viewport cut the U-turn: a long horizontal lane stopping flat at nothing, its
continuation re-entering a few px away. The box now grows to the ink. The
[WI-323 critique](../reviews/WI-323-CRITIQUE.md)'s explicit open question — "whether
the x=22 boundary is viewBox clip or routing margin" — is **answered from the
emitter: it is the CLIP**, and the answer is recorded next to the fix.

**The evidence, in SVG user units, on the shipped dashboard.** `_layered_layout`
returns `width = pad * 2 + nranks * col_w + (nranks - 1) * col_gap`; `_detour_d`
turns a backward edge's lane at `x1 + _WIRE_STUB` / `xe - _WIRE_STUB` (18 px), a
WI-366 harness lead (11–27 px) further out again. Four of the dashboard's 49 drill layers
overflowed: the roadmap ROOT (the critique's site) reaching x=−17.5 and x=711.0
against a 0..692 box, `when-1` −6.5/596.0 against 0..585, `when-22` −6.5 against
0..996, and the How-SW ROOT x=923.0 against 0..904 — so **both** routed-SVG tabs were
affected. Every one of those extremes is a lane's own `L` endpoint, not a control
point: `… 703.0,146.9 L-17.5,146.9 C-8.5,146.9 …` is literally the critic's "long
horizontal line that stops at nothing".

**Deliverables** ([gen_trajectory.py](../../project-trajectory/scripts/gen_trajectory.py)):
`_svg_frame` measures the outboard ink off the emitted BODY — the `_svg_role`
precedent, so no emitter has to remember the rule and a successor emitter cannot
forget it — adds `_INK_PAD` (2.0, clearing the widest stroke's 1.25 half-width),
rounds out to whole units, and grows the declared natural `width` with the box so a diagram that
already fits its card keeps its scale. `_path_xs` bounds the ink from the control
hull (exact here, since every extreme is an endpoint) and stops at a command it does
not know rather than reading that command's arguments as coordinates; `_ink_overflow`
cuts `<defs>` first, because a `<marker>`'s path lives in the marker's own viewBox.
Both wrapper sites (`_svg_wrap`, `_drill_layer_svg`) shrank. AFTER: `-20 0 733 354`,
`-9 0 607 286`, `-9 0 1005 490`, `0 0 925 150`, and zero outboard ink in the
document. Four new tests in
[test_gen_trajectory.py](../../tests/test_gen_trajectory.py): a whole-document sweep
asserting every SAMPLED wire polyline sits inside its own viewBox with the full
`_INK_PAD` clearance — over freshly generated documents only, since the committed
`PROJECT_STATE.html` is the trunk lane's to refresh (concurrency-restructure §5.2)
and reading it would be a standing red on every work branch, so a `WRAPAROUND_WIS`
fixture (a rank-0 item with a SOFT edge after the last rank) supplies the U-turn and
must be seen to emit a padded box or the sweep is a tautology; the roadmap's measured
pad numbers, the
byte-identity of the other 45 layers (including the `-0` formatting trap and the
`<defs>` cut), and `_path_xs`'s relative-`h` / unknown-command behaviour. No
perceptual proxy, no pixel assertions in the suite — the render half is the shots
plus the periodic advisory critique, per the spec.

**Measured before/after** (2x-DPR shots; 1280px renders identically to 1680px, both
sitting at the 1120px `.wrap` cap). Roadmap root: flat terminations at both box edges
on every wrap-around lane → **none**; node box 240 → 237 device px, fit scale 1.000 →
0.9877 CSS px per unit (−1.23%). How-SW root: port-to-port pitch 371.0 → 362.75
device px, fit scale 0.800 → 0.782 (−2.23%), its 12px labels 9.60 → 9.38 px. At
390px the scale is unchanged **by construction** — below the legibility floor the SVG
renders at `min-width` = `SHRINK_FLOOR` × its OWN natural width, so a wider natural
width cancels exactly (node box 150 device px before and after; page height 6358
device px both, so no new `.scrollcue`). Page heights fell 10 (dag) / 6 (sw) device
px: the scale-down, nothing added.

**No port-fan regression.** The whole-document diff is four `<svg>` open tags plus
the `state as of commit` stamp — every `d` is byte-identical, so WI-366's user-unit
separations are untouched. Their RENDERED CSS-px values move by the same −1.23% /
−2.23% the diagram does (block 1's out-port pair 8.00 → 7.90 px at 15 px from the
port): a render-scale artifact, the same class WI-366 recorded for the critique's
"How-SW 8 px vs the roadmap's 10" finding, not a geometry change.

**Deviations from spec.** The spec names "the DAG SVG"; the same clip was measured on
the How-SW root and on two roadmap drill layers, and the fix belongs in the shared
wrapper, so all four are covered — scoping it to one layer would have meant writing
the rule twice. The alternatives were weighed and passed over: shrinking the ink to
the box would push the U-turn back through its own endpoint box (the defect WI-257
removed), and widening `pad` instead would shrink all 49 layers to fix four. The
module-size baseline is re-stamped **5195 → 5274** with its reason — most of the
delta is the comment that answers the critique's open question with the measured
extents.

**Residue, stated.** The How-SW root renders 2.23% smaller at 1280/1680, unavoidable
while its card is ~724 CSS px and its natural width is 925; the only lever that
recovers it is widening that panel's diagram column, a layout change this WI does not
own. Whether the reconnected U-turns now read as attributable end-to-end is the
periodic advisory critique's call, not this implementer's.

**Bars (real output).** Full unfiltered suite `python -m pytest -q -n auto`:
**1686 passed / 7 skipped / 1 failed (653s)** — the one failure is the standing
work-branch conditional `test_this_repo_is_not_a_work_branch`, red for the whole
branch by WI-357's design (the claim commit put `docs/work/active/wi-367-viewbox-padding/`
into reachable history, and `_work_branch` reads history) and green again on the trunk
after merge. Smoke `-m smoke` after close: **555 passed / 1 failed** (that same
conditional). `check_docs.py --root . --stale` green (0 broken links);
`check_trajectory.py --strict` exit 0.
