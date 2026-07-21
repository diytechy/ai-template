# 077 — CRITIQUE (post-WI-246/247/248 render; the three 076 nits confirmed closed)

**Scope:** SR-052/053/054 (T1–T7), the dashboard render **after WI-246/247/248**
(build `dd170fc`, palette rework `d3a3e04`). Judged against
`docs/rubrics/dashboard-{usability,accessibility,uniformity}.md`.
**Artifact:** the `scripts/dashboard-shots/shoot.mjs` PNG matrix re-shot on the
`d3a3e04` build, read directly by this critic (both the independent REVIEW-A
reviewer and the builder also read a subset of this same matrix during their
own passes, but this is a fresh render + fresh read, not a re-use of their
screenshots).
**Critic:** Claude (agent), via the `render-dashboard-critique` loop. Honest
caveat: an agent critique is weaker than an independent family-heterogeneous
critic or the owner's own eye (SR-047) — the strongest attestation is a human
pass, which the owner can do anytime. This verdict re-dates the perceptual
evidence past the WI-246/247/248 render change, clearing the WI-243 staleness
warn that `check_trajectory` raised the moment `d3a3e04` touched the render
surface.

VERDICT: APPROVE findings=0 (1 non-blocking observation recorded)

## Resolved since 076

1. **[T4, WI-246] How (SW) component-block labels — FIXED.** All five CMP
   blocks (Generators, Quality checkers, Unattended loop & floor, Traceability
   core, Scaffold & onboarding) now render their full names on an id/name
   two-line label — no ellipsis, no truncation. Checked both themes at 1280px;
   no overlap or clipping introduced by the two-line wrap. *Shots:*
   `1280px-{light,dark}-sw-full.png`.
2. **[T5/uniformity, WI-247] When (roadmap DAG) phase-accent palette — FIXED,
   with a REVIEW-A rework cycle along the way.** The first build (`dd170fc`)
   swapped in 8 well-separated hues but reused `#b45309`/`#047857` — byte-
   identical to `STATUS_FILL`'s "active"/"done" and `TIER_FILL`'s "tc" — a
   uniformity regression the independent reviewer caught before this critique
   ran. The rework (`d3a3e04`) replaced those two, and the render now confirms
   it: 8 clearly distinct phase swatches/blocks (teal-blue, violet, dark red,
   blue, crimson, indigo, magenta, purple) in both themes, and none reads as
   the green "done" / orange "active" / grey "queued" status legend sitting in
   the same panel. *Shots:* `1280px-{light,dark}-dag-full.png`.
3. **[T7, WI-248] What (SR breakdown) icicle 390px overflow — CONFIRMED
   already-resolved, no code change was needed.** At 390px (both themes) the
   "↔ Scroll sideways to see the full view" cue renders above the icicle, the
   `.view` container clips at the SR column's right edge, and LLR/TC are
   reachable by horizontal scroll — the WI-219 `_hscroll`/`SCROLL_CUE` idiom
   was already doing its job; the finding had simply never been independently
   re-verified since WI-189. *Shots:* `390px-{light,dark}-arch-full.png`.

## Non-blocking observation (not filed as a WI)

- **[T5, minor]** In the phase-accent legend, "1+2" (`#6d28d9`, violet) and
  "unphased" (`#7e22ce`, purple) sit close in hue to each other — closer than
  the other 6 pairs, though both are legitimately distinct from every other
  phase, from the status vocabulary, and from the icicle tier colors (the
  actual collision REVIEW-A caught). They are **not adjacent** in either the
  legend row or the rendered roadmap blocks (the roadmap's tallest/most-common
  phase, "unphased," renders far from "1+2" in the layout), so this reads as a
  minor residual softness, not a repeat of the 076 finding. Recorded here per
  the standing OI-8 "amendments arrive as future WIs" posture, but not rising
  to a filed WI — the8-hue palette already clears its validator targets and
  the reviewer's specific collision is resolved.

## Disposition

All three 076 nits are closed: two by code (WI-246, WI-247 — the latter after
a REVIEW-A-caught rework), one by honest re-verification with no change
needed (WI-248). The **dashboard-quality workstream is now fully closed** —
every finding from the original 075-CRITIQUE.md has a resolved disposition.
This clears the WI-243 fail-closed gate: `check_trajectory --strict` should
now pass clean at G3 (re-run as part of the closing gate).
