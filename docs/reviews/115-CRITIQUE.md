# 115-CRITIQUE — dashboard usability (SR-054), post-WI-290 render surface

**Trigger:** the WI-243 perceptual re-fire — the dashboard render surface
(`project-trajectory/scripts/gen_trajectory.py`) last changed at `ffc4b0c`
(WI-290), *after* the previous perceptual evidence
[112-CRITIQUE.md](112-CRITIQUE.md) (`122ad01`, 2026-07-22), so
`check_trajectory --root . --strict` reported the fail-closed
`perceptual-stale SR-052;SR-053;SR-054` error. This session re-dates the
perceptual evidence past that render change and judges **SR-054** cold. It is one
of a batch of three filed together — see the numbering note in
[117-CRITIQUE.md](117-CRITIQUE.md).

**Critic:** `OPENCODE-KIMI` (`opencode-go/kimi-k3`, OPENCODE family) — a fresh,
family-heterogeneous **non-Anthropic** session per SR-084 / SN-024, dispatched by
hand through the OpenCode-Go gateway. Its brief was built to the SR-084 contract:
rubric + SN/SR intent + artifact recipe, and **no build transcript and no
implementer self-assessment**. It worked in an isolated sandbox holding only the
generated artifact, the shot matrix, the rubric, and the recipe — it never saw
this repo, the train branches, or any prior verdict.

**Artifact:** `PROJECT_STATE.html` generated at HEAD `86b7ad2`, plus the full
declared matrix (36 PNGs: 390/1280/1680 × light/dark × 5 tabs, full-page + the
landing folds) from `node scripts/dashboard-shots/shoot.mjs`. Beyond reading the
matrix, this session cropped and magnified regions for the tab-control and
edge-routing checks, and — for T8 — parsed all 43 embedded SVGs (including the
hidden drill layers) to sample wire paths geometrically rather than by eye.

**Rubric:** [dashboard-usability.md](../rubrics/dashboard-usability.md),
anchors `T1`–`T8`.

---

## The three core reading tasks

1. **Find the project state — 0 tab switches** — the landing fold itself carries
   the state: DEFINITION COMPLETENESS 100% (110 of 110 SRs verified), EXECUTION
   93% (270 of 289 done · 0 active · 1 retired), plus the six count tiles
   (`390px-light-arch-fold.png`, `1280px-dark-arch-fold.png`). For "what gate": 1
   tab switch to *Process*, where a "Current gate: **G3**" banner sits directly
   under the tab bar (`1280px-light-process-full.png`). Either reading ≤ 1 switch.
2. **Find the next work — 1 tab switch** — *Process* tab → "2 · The resume loop"
   panel (read status → PLAN → BUILD → REVIEW-A/B → CRITIQUE → INTEGRATE → commit
   → hook/gate → repeat), the rubric-sanctioned surface; the landing "0 active"
   and the When-tab status legend (done / active — you are here / queued /
   retired) supplement it.
3. **Find how the parts connect — 1 tab switch** — the labelled *How (SW
   architecture)* tab opens directly on the module map: 5 components
   (CMP-001…005) with wired seams and per-module counts, no expansion needed
   (`1280px-light-sw-full.png`).

## Anchor verdicts

**T1 — Task findability:** PASS — 0/1/1 tab switches for the three tasks; entry
points are labelled tabs, not unlabelled regions (`1280px-light-arch-fold.png`,
`1280px-light-process-full.png`, `1280px-light-sw-full.png`).

**T2 — Default-density legibility:** PASS — every wired view opens collapsed per
the >3 rule, stated in-view ("A tier renders as wired blocks only when it holds
more than 3 members"): When = 8 phase blocks (`1280px-light-dag-full.png`), How =
5 components (`1280px-light-sw-full.png`), Knowledge = 6 type blocks
(`1280px-light-know-full.png`). The icicle is the flat overview map by design, not
an exploded graph.

**T3 — Detail in context:** PASS — descending swaps in-place layers within the
same tab; each drill view carries `<nav class="crumbs" aria-label="Breadcrumb">`
populated with a `›` trail back, and detail opens in the persistent inline side
panel ("Click a work item to read its detail…") without leaving the view (markup
+ `1280px-light-dag-full.png`).

**T4 — Label legibility:** PASS — no clipped or overlapping text in any of the 36
shots; the only truncations (icicle SN descriptions, Process loop stage sublabels)
are marked with "…" and carry full text via `<title>` plus click/link affordance
(`1280px-light-arch-full.png`, `1280px-light-process-full.png`).

**T5 — Interactive-control legibility, both themes:** PASS — measured from the
shipped CSS: inactive tabs 4.76:1 light / 6.96:1 dark; active tab text + 2px
underline 6.29:1 light / 5.98:1 dark; focus ring 6.29:1 / 5.98:1; collapse "−"
dashes and block labels ≥5.7:1; wires ≈4:1 light / ≈5.9:1 dark (`tabs` crops from
`1280px-light-arch-fold.png` / `1280px-dark-arch-fold.png`,
`1280px-dark-dag-full.png`, `1280px-dark-sw-full.png`).

**T6 — Theme-lock:** PASS — every tab renders wholly in the selected theme across
all widths; no light/dark seam anywhere in the matrix (all dark shots, e.g.
`390px-dark-process-full.png`, `1680px-dark-arch-fold.png`).

**T7 — Viewport fit at declared widths:** PASS — no page-level horizontal scroll
at 390px; nav wraps, cards stack, Process chips/cards reflow, the loops SVG scales
(`390px-light-dag-full.png`, `390px-light-process-full.png`). Above-the-fold at
390px has nothing clipped (`390px-light-arch-fold.png`). Wide diagrams sit below
the fold in signposted horizontal-scroll regions (visible "↔ Scroll sideways to
see the full view" hint + right-edge fade mask + focusable region — the deliberate
WI-219 pattern), never silently clipped.

**T8 — Edge-routing legibility:** PASS — traced individual edges in all four wired
views: the DAG back-edges (1→2, 1→2+3, unphased→4) wrap via horizontal channels
that run in open space ≥7px clear of every box; the Knowledge SR→TC bypass sweeps
under LLR without touching it; SW channels and Process loop fans stay clear of
node boxes. Verified geometrically too: parsed all 43 embedded SVGs (including
hidden drill views), sampled every wire path — **0 through-box hits**, and no wire
extends >7 units past its viewBox. Crossings land in open channels, not under
labels or port clusters.

## Findings

None.

## Notes

- **Collinear bus sharing on the roadmap (T8-adjacent, not a failure):** at the
  When top tier, up to four aggregated edges share the *same* channel line (e.g.
  y=146.9 carries 1→2, 1→unphased, 2→1, 2→unphased as coincident strokes in
  `1280px-light-dag-full.png`). Geometry and arrowhead taps keep each edge
  followable, and hover-highlighting disambiguates, but static source↔sink pairing
  on a shared channel is not visually attributable. This is the class of issue
  WI-253 tracks as filed; the rubric's binding render test (no through-box, no
  crossings under labels/ports) passes.
- **Next work is a pointer, not a named WI:** the dashboard shows 0 active and
  routes the reader to `docs/status.md` via the resume loop's "read status" stage;
  it does not itself name the next queued WI. The rubric's task-2 parenthetical
  explicitly accepts the resume-loop panel, so this is awareness only.
- **Mid-page sticky header in the 390px `-full` shots** (e.g.
  `390px-light-dag-full.png`): confirmed as the known `fullPage` capture artifact
  — the matching `-fold` viewport shots (`390px-light-arch-fold.png`,
  `390px-dark-arch-fold.png`) render the header correctly at top with no overlap.
- The `1+2` phase block, CMP-005, and the Knowledge IF/PG blocks render with empty
  ports (no wires) — data-derived (no crossing dependencies), consistent with the
  registries, not a rendering defect.

VERDICT: APPROVE findings=0
