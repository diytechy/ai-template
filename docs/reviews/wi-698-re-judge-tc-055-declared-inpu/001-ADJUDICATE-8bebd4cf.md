# WI-698: TC-055 re-judged at 8bebd4cf by a cross-family Critique session

TC-055's approved Method asks for a family-heterogeneous Critique session.
The judge is Codex Sol (gpt-5.6-sol), a different model family from the
rendering code's authors, run read-only by the coordinator. It was given the
rubric (`docs/rubrics/dashboard-usability.md`, live anchors T2, T4, T5, T8),
the intent (SN-023, SN-024, SR-054, LLR-055), and the full declared matrix
rendered at HEAD by `scripts/dashboard-shots/shoot.mjs` (390, 1280 and
1680 px x light and dark x the arch, dag, sw and process tabs; `know` is a
declared skip). The render was produced by an adjudicator session that did
not judge it. Every shot was cut into unscaled native-resolution tiles of at
most 1200 px (180 tiles), and the judge was given one width per pass, so
nothing it saw was downsampled. It was given no earlier verdict.

Declared inputs changed since the last record (fe96ec69): SR-054's
`boundary_refs` and `da_refs` only. The rubric, `gen_trajectory.py` and
`rendering/` are unchanged.

## 390 px

- [PASS] T2 -> large views start collapsed into manageable aggregates in both
  themes (`390px-{light,dark}-arch-full-t04`, `-dag-full-t05`, `-sw-full-t19`).
- [FINDING] T4 -> diagram labels are scaled below comfortable default-zoom
  readability in both themes, especially the station-cycle card annotations
  and the How system-context crossing descriptions
  (`390px-{light,dark}-process-full-t05`/`t06`, `390px-{light,dark}-sw-full-t04`).
- [FINDING] T5 -> in the light theme, the When diagram's white descend arrows
  wash into the pastel phase blocks and do not keep body-text contrast
  (`390px-light-dag-full-t05`, the phase blocks' upper-right corners; compare
  `390px-dark-dag-full-t05`).
- [PASS] T8 -> routes use separated orthogonal lanes, and crossings sit in
  open gutters, in both themes.

## 1280 px

- [PASS] T2, T4, T5, T8 in both themes (`APPROVE findings=0`). Ellipsized
  What-node summaries carry an explicit "click to read its full text"
  affordance.

## 1680 px

- [PASS] T2, T4, T8 in both themes.
- [FINDING] T5 -> in the When roadmap's graph, the default render's selection
  fading leaves non-selected phase cards and their ports too low-contrast to
  find and operate, especially the pale cards with white text in the light
  theme (`1680px-{light,dark}-dag-full-t03`). The coordinator checked the
  tile: the default render auto-selects a card, so the fade is the state a
  reader first sees, not a capture artifact.

## Disagreement recorded

The same judge, on the same rendering code at fe96ec69, passed T4 at 390 px
when shown only those tiles (`docs/reviews/2026-09-27-wave5/sol-tc055-t4.md`).
Here, in the full per-width pass, it raised T4 at 390 px again. The T5
findings at 390 and 1680 px are new: the first whole-matrix pass saw
downsampled images. The T5 findings carry this verdict; the T4 finding
stands as the judge's latest reading.

The Critique's line: `VERDICT: CHANGES-REQUESTED findings=3 anchors=T2,T4,T5,T8`.

OUTCOME: RECORDED result=fail
