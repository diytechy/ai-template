# WI-685: TC-055 re-judged by a cross-family Critique session (wave-5 arbitration ruling 31)

The first verdict in this folder (`001-ADJUDICATE-fe96ec6.md`) was taken by a
session of the same model family as the rendering code's authors. TC-055's
approved Method asks for "a fresh, family-heterogeneous CRITIQUE session", and
a cross-family judge was available, so that session did not qualify. Its
observation record was withdrawn before merge; nothing on trunk records it.
This verdict is the qualifying one.

The judge: Codex Sol (gpt-5.6-sol), a different model family, run read-only by
the coordinator. It was given the rubric (`docs/rubrics/dashboard-usability.md`,
live anchors T2, T4, T5, T8), the intent (SN-023, SN-024, SR-054, LLR-055), and
the 30-shot matrix `scripts/dashboard-shots/shoot.mjs` rendered at fe96ec69
(390, 1280 and 1680 px x light and dark x the arch, dag, process and sw tabs).
It was not given any earlier verdict on TC-055. The coordinator recorded the
result through the kit's writer.

## First pass: the whole matrix

- [PASS] T2 -> default views remain collapsed and manageable at all three
  widths in both themes; no exploded node wall in the What hierarchy, the When
  roadmap, the How architecture or the Process diagrams.
- [FINDING, withdrawn below] T4 -> labels in the 390 px Process station-cycle
  and How diagrams judged too small at default zoom.
- [PASS] T5 -> tab labels, active underlines, graph ports and arrows, and drill
  affordances stay distinguishable in both themes at all three widths.
- [PASS] T8 -> crossings in the wired When, How and Process diagrams route
  through open channels, not through labels or port clusters.

## Second pass: T4 at 390 px, at native resolution

The 390 px full-page shots are 780 px wide (2x) and 8,704 to 24,076 px tall. As
single attachments they were downsampled heavily. The same four shots were cut
into 58 consecutive 780 x 1200 px tiles (a 390 x 600 CSS px window, unscaled)
and T4 alone was judged again:

- [PASS] T4 at 390px -> native tiles show readable, non-overlapping diagram
  labels in the Process station-cycle nodes (dark and light process tiles
  t04-t05) and the How system-context and component diagrams (dark and light
  sw tiles t03 and t18). Edge-clipped wide content carries the explicit
  "Scroll sideways" affordance. The first finding resulted from full-page
  image downsampling.

Non-blocking: the bar crossing the Next Work card in the 390 px full-page
captures is absent from the matching fold shots, consistent with the
documented sticky-header capture artifact.

The Critique's own line: `VERDICT: APPROVE findings=0 anchors=T2,T4,T5,T8`.

OUTCOME: RECORDED result=pass
