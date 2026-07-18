# Rubric — Dashboard accessibility (SR-052)

**Adjudicates:** SR-052 (dashboard accessibility, `Verification=Critique`).
**Used by:** the SR-047 critique loop — a fresh, provider-heterogeneous CRITIQUE
session judges the generated `PROJECT_STATE.html` against the numbered anchors
below, receiving this rubric + the SN/SR intent + the artifact recipe and **never
the implementer's self-assessment**. Authored at `[v3]-[g2]` (WI-135) from the
SR-052 / SN-024 / SN-023 intent, **not** from the TC — a lax TC must not narrow
what "accessible" means here.

The verdict is `VERDICT: APPROVE|CHANGES-REQUESTED findings=N` with each finding
citing an anchor id (`A1`…`A4`). APPROVE requires every anchor satisfied.

## Anchors

**A1 — Keyboard reachability.** Every interactive element — the tab buttons, the
expandable `<details>` blocks, and each SVG node that opens a detail panel — is
reachable and operable with the keyboard alone (native focusable elements, or an
explicit `tabindex` + key handler). *Good:* tabbing walks every control in a
sensible order and Enter/Space activates it. *Bad:* a control that only responds
to a mouse click, or a focus order that skips a panel.

**A2 — Accessible names.** Every interactive element and every meaningful graphic
carries an accessible name — a `<title>`, `aria-label`, or visible text label.
*Good:* an SVG node exposes a `<title>` naming the work item / module it stands
for. *Bad:* an icon-only or color-only control a screen reader announces as
"button" with no name.

**A3 — No information by color alone.** Every status / phase / type encoding pairs
its color with a redundant text or shape cue, so the meaning survives without
color perception. *Good:* a `done` status shows a check glyph or the word `done`,
not just a green fill; a phase carries its `v2`/`v3` label beside its accent.
*Bad:* status distinguished only by hue.

**A4 — Text contrast.** Text keeps a readable contrast ratio against its own fill,
at or above **WCAG 2.1 AA: 4.5:1 for normal text and 3:1 for large text (≥ 18.66px
bold or ≥ 24px) and for graphical/UI boundaries**. This is the declared threshold
SR-052's "readable contrast" concretizes. *Good:* dark text on the light node
fills, light text on the dark accents, each measured ≥ threshold. *Bad:* mid-gray
label text on a mid-tone fill.

## Notes for the critic

- Judge the **generated artifact**, not the generator source. Open the emitted
  `PROJECT_STATE.html` (a data-less render is acceptable — the encodings are the
  same) and exercise the anchors.
- Contrast is measurable: sample the actual fill/text colors and compute the
  ratio; cite the pair and the number in the finding.
- A single un-named interactive control or one color-only encoding is an A2/A3
  failure on its own — these are floors, not averages.
