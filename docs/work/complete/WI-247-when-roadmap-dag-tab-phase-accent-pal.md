+++
id = "WI-247"
title = "When (roadmap DAG) tab: phase-accent palette has low hue separation - adjacent phases near-identical maroon; raise separation so phases are distinguishable (T5/uniformity, 075-CRITIQUE)"
workstream = "dashboard"
sr_refs = ["SR-053"]
buildtier = "quick"
safety_class = "ordinary"
order = 244
+++

## Deliverable

PHASE_ACCENTS (8 near-identical maroon/plum hexes) replaced with a hue-wheel-spread, dataviz-skill-validated categorical palette (validate_palette.js: adjacent CVD deltaE, WCAG white-text contrast). First build (dd170fc) passed the separation goal but REVIEW-A opus CHANGES-REQUESTED (MAJOR): 2 of the new hexes were byte-identical to STATUS_FILL's active/done and TIER_FILL's tc, a uniformity regression (U5) since both vocabularies render on the same When/DAG panel. Reworked (d3a3e04): full STATUS_FILL/TIER_FILL exclusion set gathered first, new 8-hex set every value >=11 deltaE from the 3 same-tab status hues, re-validated ALL-PASS, re-rendered and independently re-confirmed by REVIEW-A rework + this critic. Also fixed the REVIEW-A MINOR (_drill_block_label now dispatches on an explicit wrap flag, not em-dash string-sniffing). 077-CRITIQUE.md: 8 clearly distinct blocks/swatches, no collision with the status legend, both themes.
