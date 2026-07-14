# Rubric — Dashboard UI uniformity (SR-053)

**Adjudicates:** SR-053 (dashboard UI uniformity, `Verification=Critique`).
**Used by:** the SR-047 critique loop — a fresh, provider-heterogeneous CRITIQUE
session judges the generated `PROJECT_STATE.html` against the numbered anchors
below, receiving this rubric + the SN/SR intent + the artifact recipe and **never
the implementer's self-assessment**. Authored at `[v3]-[g2]` (WI-135) from the
SR-053 / SN-024 / SN-023 intent, not from the TC.

The verdict is `VERDICT: APPROVE|CHANGES-REQUESTED findings=N` with each finding
citing an anchor id (`U1`…`U4`). APPROVE requires every anchor satisfied.
"Uniform" is judged across the whole document — every tab (When / How-SW /
Process / Knowledge) and every SVG emitter (`dag_svg`, `sw_graph`, `when_view`).

## Anchors

**U1 — One type scale and spacing rhythm.** Font sizes, weights, and the spacing
between elements come from one small, repeated set, not ad-hoc per view. *Good:*
headings, node labels, and legend text each render at one of a few shared sizes
everywhere they appear. *Bad:* the When tab's node label is a different size than
the How-SW tab's for the same kind of node.

**U2 — One status / phase / type color vocabulary.** The same concept renders in
the same color wherever it appears, from one declared palette. *Good:* `done` is
the same fill in the roadmap DAG, the module graph, and the campaign bins; each
phase keeps one accent across tabs. *Bad:* two different greens for `done` in two
views, or a phase accent that shifts between the When and Process tabs.

**U3 — Uniform node / edge / legend / detail-panel styling.** Across the SVG
emitters, a node of a given kind shares one shape, border, corner, and padding
treatment; edges share one stroke idiom; legends and detail panels share one
layout. *Good:* every containment edge is drawn the same way in both the When and
How-SW views. *Bad:* rounded nodes in one emitter and square in another for the
same concept, or a legend styled differently per tab.

**U4 — One interaction idiom per structure.** Wherever the same structure appears,
the same interaction reveals it: expand-to-descend, hover-to-highlight, and
click-for-detail behave identically across views. *Good:* descending a container
works the same in the roadmap and the module map. *Bad:* hover shows a tooltip in
one view and nothing in another for the same node kind.

## Notes for the critic

- Compare **across** views deliberately: put the same concept (a `done` item, a
  container block, a legend) side by side between tabs and check it renders alike.
- Cite the two divergent locations in each finding (view A vs view B), so the fix
  is unambiguous.
- Small, intentional differences that carry meaning (e.g. a phase accent) are not
  U2 failures — the failure is the *same* concept rendered *differently*.
