# 116-CRITIQUE — dashboard accessibility (SR-052), post-WI-290 render surface

**Trigger:** the WI-243 perceptual re-fire — the dashboard render surface
(`project-trajectory/scripts/gen_trajectory.py`) last changed at `ffc4b0c`
(WI-290), *after* the previous perceptual evidence
[112-CRITIQUE.md](112-CRITIQUE.md) (`122ad01`, 2026-07-22), so
`check_trajectory --root . --strict` reported the fail-closed
`perceptual-stale SR-052;SR-053;SR-054` error. This session re-dates the
perceptual evidence past that render change and judges **SR-052** cold. It is one
of a batch of three filed together — see the numbering note in
[117-CRITIQUE.md](117-CRITIQUE.md).

**Critic:** `OPENCODE-GROK` (`opencode-go/grok-4.5`, OPENCODE family) — a fresh,
family-heterogeneous **non-Anthropic** session per SR-084 / SN-024, dispatched by
hand through the OpenCode-Go gateway, and a *different model* from the sibling
uniformity/usability critiques so the three verdicts are not one judge's opinion.
Its brief was built to the SR-084 contract: rubric + SN/SR intent + artifact
recipe, and **no build transcript and no implementer self-assessment**. It worked
in an isolated sandbox holding only the generated artifact, the shot matrix, the
rubric, and the recipe — it never saw this repo, the train branches, or any prior
verdict.

**Artifact:** `PROJECT_STATE.html` generated at HEAD `86b7ad2`, plus the full
declared matrix (36 PNGs: 390/1280/1680 × light/dark × 5 tabs, full-page + the
landing folds) from `node scripts/dashboard-shots/shoot.mjs`. Contrast ratios were
computed from hex pairs read out of the emitted artifact, not estimated from
pixels.

**Rubric:** [dashboard-accessibility.md](../rubrics/dashboard-accessibility.md),
anchors `A1`–`A4`.

---

## Anchor verdicts

**A1 — Keyboard reachability:** PASS — Tab buttons are native `<button>`s; icicle
`.cell`, drill `.block`, and process `a.stg` nodes use `tabindex="0"` (or native
links); descend controls wire `keydown` for Enter/Space; focus handlers open
detail panels. No pointer-only activate path found.

**A2 — Accessible names:** PASS — Sampled interactive controls carry names: tabs
have visible text; all 334 `.cell` and sampled `.block` nodes have `<title>`
(descend nodes also `aria-label` + `role="button"`); scroll `.view` regions have
`aria-label`; process stage links have `<title>` + visible labels. No unnamed
interactive control found.

**A3 — No information by color alone:** PASS — WI status uses glyphs + title words
(`✓`/`done`, `○`/`queued`, `⊗`/`retired`); type/kind shown as id text or sublabels
(`SN`/`module`/…); phase blocks label `1`/`1+2`/…; hard vs soft edges use solid vs
dashed stroke; legends pair swatch + text (see `1280px-light-dag-full.png`,
`…-know-full.png`, `…-sw-full.png`).

**A4 — Text contrast:** FAIL — Process hub label is white on `var(--accent)`; in
dark theme accent is `#818cf8`, so `#ffffff` on `#818cf8` is **2.98:1** (needs
4.5:1). Visible in `1280px-dark-process-full.png` (washed "LLM_Agent" hub). Light
theme hub (`#fff` on `#4f46e5` ≈ 6.29:1) and other sampled text pairs meet AA.

## Findings

- [MAJOR] A4 -> Process working-loops hub (`.hub` / `.hubname` / `.hubsub`): CSS
  sets `fill:var(--accent)` on the rect and `fill:#fff` on labels; under
  `prefers-color-scheme: dark`, `--accent` is `#818cf8`, yielding **#ffffff on
  #818cf8 = 2.98:1** (hubsub at 0.85 opacity is worse, ~2.57:1). 13px text is
  normal-size, so AA floor is 4.5:1. Confirmed in
  `1280px-dark-process-full.png`. -> Use a dark-theme hub fill that keeps ≥4.5:1
  with white (e.g. keep light-theme `#4f46e5` for the hub, or switch hub label to
  `--text` on a darker fill), and re-check `.hubsub`. -> @owner

## Notes

- Other text pairs checked in both themes clear AA, including body/muted
  (`#64748b`/`#f8fafc` ≈ 4.55:1 light; `#94a3b8`/`#0f172a` ≈ 6.96:1 dark), SVG
  whites on fixed fills (`#fff` on `#64748b` ≈ 4.76:1; on
  `#047857`/`#0e7490`/`#4338ca`/`#7c3aed` all ≥4.5:1), and queued dark labels
  (`#0f172a` on `#94a3b8` ≈ 6.96:1).
- Focus rings (amber `#f59e0b` / accent on saturated node fills) are often under
  3:1 as pure stroke contrast; focus still updates the detail pane, so not filed
  under A1/A4 text floor.
- Many inner `role="img"` SVGs lack their own name; parent `.view` `aria-label`s
  and per-node `<title>`s cover interactive naming for A2 as written against
  SR-052's interactive list.

VERDICT: CHANGES-REQUESTED findings=1
