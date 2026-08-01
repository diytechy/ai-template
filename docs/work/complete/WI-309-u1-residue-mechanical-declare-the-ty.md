+++
id = "WI-309"
title = "U1 residue -> mechanical: declare the type scale and forbid raw font-size literals. Measured 2026-07-25: 18 raw literals against 5 declared tokens, with .7/.75rem, .9/.95/.98rem, 1.05/1.1rem and 8.5/9px each being near-duplicate steps for ONE role (3-7% apart - no reader distinguishes them, no rule justifies them), and .85rem/.8rem byte-identical to an existing token that simply was not used. LLR-104's residue ('whether the resulting sizes read as visually uniform') is undecidable only because the scale was never declared; declare it and the question is set membership."
workstream = "scripts"
sr_refs = ["SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 306
+++

## Deliverable

The dashboard type scale is DECLARED: eleven steps in three documented families - node (px, because SVG geometry is fixed px and a rem would resize labels out of their boxes), page (rem, scales with root), and one relative step (em, for text sized against its parent) - replacing 18 raw font-size literals. Four groups were near-duplicate steps for ONE role and merged into the nearer step (.7/.75rem, .9/.95/.98rem, 1.05/1.1rem, 8.5/9px - all 3-7% apart, which no reader distinguishes and no rule justified); two literals (.85rem/.8rem) were byte-identical to a token that simply was not being used. LLR-104's residue ('whether the resulting sizes read as visually uniform') was undecidable only because the scale was never written down - declared, it is set membership. Guard: tests/test_gen_trajectory.py::test_u1_every_font_size_resolves_to_a_declared_scale_step, over the shipped artifact plus SEVEN fixture renders, verified to fail against four separate regressions (a raw literal in a page rule, a raw literal in an SVG emitter, a font-size naming a non-scale token, and a declared step losing its definition). The check scopes to <style> blocks and inline style= attributes, because the rendered document also QUOTES CSS inside prose and a whole-document scan judges documentation as if it were code.
