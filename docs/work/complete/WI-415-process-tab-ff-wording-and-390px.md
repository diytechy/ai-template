+++
id = "WI-415"
title = "Process-tab polish: the ff-wording one-string fix and the 390px legibility observation (WI-389 REVIEW-A findings 1-2, minted trunk-side at intake per the R3 invariant). FINDING 1, the one-string fix: the Trunk advance card's note reads 'ff trunk to the barred tree', which misstates the shipped act - trunk advances via the --no-ff merge commit itself (integrate.py's slot; a true ff is what the RULING-6 audit reds); the reviewer's replacement 'advance trunk to the barred tree' fits the 34-char note budget. One string in traj_panels' station panel + regen; the drawn picture must not contradict the code it derives from. FINDING 2, per the render-critique discipline (observations filed as their own WIs): at 390px the station's note lines render ~3.3 CSS px - illegible without pinch-zoom; no overflow or truncation, titles marginal, the esc list and svg title tooltips carry the content. JUDGE the fix honestly at the panel's design constraints (bigger notes at narrow widths, a two-line wrap, or dropping notes below a width threshold in favor of the tooltips) - verify by pixels per the skill matrix, and take the smallest change that makes the 390px render honest; recording a measured accept-with-tooltips is a legitimate outcome if every alternative damages the 1280/1680 reads. Scope: traj_panels station panel + its tests + pixel evidence."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

**Finding 1 (one string).** The Trunk advance card's note in
`project-trajectory/scripts/traj_panels.py` `_station_svg` read `"ff trunk to
the barred tree"`; replaced with `"advance trunk to the barred tree"` (32
chars, inside the 34-char `notemax` budget — no truncating `…`). Trunk
advances via `integrate.py`'s `--no-ff` merge at the slot
(`git merge --no-ff --no-commit`, `integrate.py`); a true fast-forward is the
shape the RULING-6 audit reds, so the old wording misstated the shipped act.
Regenerated `PROJECT_STATE.html` (`gen_trajectory.py`).

**Finding 2 (390px legibility), judged against the panel's own constraints.**
Measured before the fix: `#process .stationsvg` carried
`width:100%;height:auto;max-width:860px` with **no floor** — at a 390px
viewport (`.wrap` padding leaves ~350 CSS px for the ring) the whole 900x545
viewBox scaled down in lockstep, rendering the 8.5px note labels at ~3.3 CSS
px. Confirmed by a 1x-deviceScaleFactor Playwright crop of `#process
.station` (a 2x/3x retina crop reads legible at any underlying size and would
have hidden the defect — the earlier 3x crop looked fine and was the wrong
read).

Weighed the three options the spec named:
- **Bigger notes at narrow widths / two-line wrap** — both redesign the card
  geometry (`STATION_GEOM`, `_station_card`'s fixed `cardw`/`cardh`), which
  the spec rules out ("do not redesign the panel").
- **Drop notes below a width threshold, keep only the `<title>` tooltips** —
  legitimate per the spec, but not the smallest fix available: it discards
  information (a hover/focus-only tooltip is strictly worse than visible text
  someone can scroll to) when a smaller fix already exists in this exact
  codebase.
- **Reuse the SHRINK_FLOOR floor (taken):** the icicle / dag / seam / module
  views already solved this identical problem (WI-307/WI-219/WI-256) —
  `_svg_fit_style(width)` pins a `min-width` at `width * SHRINK_FLOOR` (0.62)
  so a diagram stops shrinking past that floor, paired with a `.tablescroll`
  wrapper (JS-toggled `.cued`/`.clipr` on real `scrollWidth`/`clientWidth`
  overflow) and the shared `SCROLL_CUE` + `_hscroll` affordance. The station
  SVG was the one emitted diagram NOT using this shared machinery. Applied it
  verbatim: the `<svg class="stationsvg">` tag now carries
  `style="width:100%;max-width:900px;min-width:558px;height:auto"`, and
  `_station_panel` wraps the `.station` block in
  `SCROLL_CUE + '<div class="tablescroll" ' + _hscroll(...) + '>'`.

**Measured after the fix** (real `PROJECT_STATE.html`, Playwright): at 390px
`scrollWidth=558 > clientWidth=350`, `cued=true` — the ring stops at its
floor and the container scrolls, with the visible "↔ Scroll sideways to see
the full view" cue and the existing right-edge clip-fade. At 1280/1680px
`scrollWidth == clientWidth`, `cued=false`, and the rendered ring is
byte-for-byte the same crop as before the change — **the 1280/1680 reads are
undamaged**. Note labels at the 390px floor now render at the SAME ~5.3 CSS
px (`8.5 * 0.62`) every other diagram in this dashboard already ships at —
not a new, weaker legibility bar, the EXISTING one, confirmed legible-if-small
by a matching 1x crop of the `dag` tab's own floor. Since the floor already
keeps the notes themselves readable, "accept with tooltips" was not needed —
the spec's fallback is recorded here as considered and not taken, not as
silently skipped.

**Tests** (`tests/test_traj_panels.py`):
`test_station_advance_card_names_the_shipped_merge` (finding 1: the new
wording renders, the old string is gone, and the length still fits
`notemax`) and `test_station_narrow_width_scrolls_instead_of_blurring`
(finding 2: the emitted inline style matches `_svg_fit_style`'s floor ratio,
and the block is wrapped in the standard scrollcue + tablescroll pair).

**Verification:** `pytest -q -n auto -m smoke` — 880 passed, 6 skipped (run
in an isolated worktree at this branch's HEAD, to keep the count free of two
other sessions' concurrent uncommitted work in the shared checkout;
`tests/test_traj_panels.py` alone: 36 passed). `check_docs.py --stale`: OK, 0
broken links. `gen_trajectory.py --check` / `gen_arch_map.py --check
--strict-parse`: both up to date. Pixel evidence: `scripts/dashboard-shots/`
(gitignored per repo convention — not committed), shot via `node
scripts/dashboard-shots/shoot.mjs` (the declared 390/1280/1680 x light/dark
matrix) plus ad-hoc 1x/3x crops of `#process .station` and the `dag` tab's
floor for the legibility comparison described above.
