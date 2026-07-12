# WI-087 Dashboard Visual Critique Rubric

Review the generated root `PROJECT_STATE.html` at 1440×900, 1024×768,
768×1024, and 390×844 in light and dark mode. Use keyboard-only navigation for
every drill/select/back path. Record `APPROVE` or `CHANGES-REQUESTED` plus
anchored findings in `docs/reviews/WI-087-CRITIQUE.md`.

## Blockers

- **Truth:** What includes every parent edge; When labels its line as a delivery
  frontier rather than calendar time; How uses declared IF seams only.
- **Hierarchy:** Phase→Workstream→WI and Component→Module levels are obvious;
  Campaign is an alternate grouping; aggregate edges disclose child edges/IFs.
- **Legibility:** cards are readable without hover, arrows are directional,
  containers are visually bounded, and unrelated edges do not obscure cards.
- **State:** Draft, active, queued, done, deferred, Cross-phase, and Unphased
  meanings are distinguishable without color alone.
- **Interaction:** drill/back/detail works by keyboard and pointer; focus remains
  visible; a semantic static fallback exposes the same information.
- **Responsive/accessibility:** no essential content is clipped or unreachable;
  mobile scrolling, dark-mode contrast, and reduced-motion behavior are usable.

## Non-blocking polish

Record density, typography, spacing, edge bundling, and animation suggestions as
MINOR only when they do not compromise the blocker criteria.
