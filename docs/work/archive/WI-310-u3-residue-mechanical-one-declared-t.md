+++
id = "WI-310"
title = "U3 residue -> mechanical: one declared token set for stroke-width, opacity and corner radius. Measured 2026-07-25: 8 distinct stroke-widths, 7 opacities, 5 border-radii, 4 rx values - drift, not a system, and exactly what LLR-103's residue ('spacing, exact visual weight') gestures at without measuring. Same shape as WI-309: declare the set, assert membership, merge near-duplicate steps into the nearer declared one."
workstream = "scripts"
sr_refs = ["SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 307
+++

## Deliverable

Fourteen declared tokens for the three properties that carry visual weight - stroke (--w-hair/node/line/emph), alpha (--o-wash/dim/ghost/soft/muted/full) and corner (--r-chip/ctl/card/pill) - plus SVG_RX for the rx presentation attribute, retiring 8 distinct stroke-widths, 7 opacities, 5 border-radii and 6 rx values. FIVE stroke widths (1, 1.2, 1.4, 1.5, 1.8) had been doing the single job 'draw a connector' and FOUR rx values (6,7,8,9) the single job 'round a node box' - that is what LLR-103's residue ('spacing, exact visual weight') was gesturing at without measuring. stroke-opacity is checked under the opacity scale deliberately: it is the same scale applied to a stroke, and letting it keep its own literals would leave exactly the hole this closes. SVG_RX is a DECLARATION the test enforces against both the source literals and every rendered document, not a value spliced into the rect templates - splicing with + rebinds .format to the last fragment of an implicitly concatenated string, a real bug this WI hit and backed out, recorded in the comment. Guards: tests/test_gen_trajectory.py::test_u3_every_weight_value_resolves_to_a_declared_token + ::test_u3_svg_corner_radii_match_the_declared_scale, over the shipped artifact plus seven fixture renders, verified to fail against six separate regressions.
