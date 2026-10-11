---
name: render-dashboard-critique
description: Use when critiquing this repo's PROJECT_STATE.html dashboard on how it RENDERS (layout, theme, legibility, responsive behavior) rather than its source — screenshot it across the declared width/theme/tab matrix, read the PNGs, and file findings as their own WIs.
stacks: [any]
domains: [any]
phases: [dev, gate]
tags: [dashboard, screenshot, playwright, critique, render, project-state]
scope: this-repo
---

# Render-critique the dashboard (this template repo)

Agent critiques of the generated dashboard `PROJECT_STATE.html` have
historically judged ~790 KB of markup, never what a viewer sees. This skill
turns the dashboard into **rendered pixels** you can actually look at (the Read
tool presents PNGs visually), so a critique judges layout, contrast, legibility,
and responsive behavior. It is **meta-only** dev tooling — the runner and its
Playwright dependency are never shipped downstream (the kit's install-nothing
posture governs `project-trajectory/scripts`, not this helper).

This is also the **artifact recipe** a future `Verification=Critique` TC on
dashboard quality would name (the critique-loop contract in
`project-trajectory/PROCESS_OPTIONS.md`, *"Critique verification"*, requires a
perceptual TC to name its render recipe): build it once, serve both the ad-hoc
critique and the TC.

## When this applies

- You're asked to critique / review the dashboard's **appearance** or a
  dashboard-UX change, or to see how a `gen_trajectory.py` change actually
  renders.
- **Not** for judging the dashboard's *data* (that's the registries + the
  `check_trajectory` / `trace` checkers), and **not** for a downstream repo
  (this tool is meta-only).

## The loop

Full details — pinned versions, the OS browser-cache location, the matrix
rationale, and the read caveats — live in `scripts/dashboard-shots/README.md`.

1. **Install once.** From the repo root:
   ```sh
   cd scripts/dashboard-shots && npm ci && npx playwright install chromium
   ```
   `sh scripts/dev-setup.sh --check` reports whether it's present (warn-only,
   optional).
2. **Shoot** — one command regenerates the dashboard and emits the whole matrix
   to the gitignored `scripts/dashboard-shots/shots/`:
   ```sh
   node scripts/dashboard-shots/shoot.mjs
   ```
   It prints every path. The matrix (widths × themes × tabs, full-page + a
   landing fold) is **declared as constants in `shoot.mjs`** — change it there,
   not per session. `TABS` declares every tab the page can render (What, When,
   How, Knowledge, Process, Retired), intersected with the tabs this render
   carries: a declared tab the page does not render is `SKIPPED` by name, and a
   rendered tab `TABS` omits is printed as `NOT shot`.

   **A judgment is never made on a failed run or an incomplete matrix.** A run
   that exits non-zero (a Playwright error, a timeout, a failed regenerate) or
   prints any `NOT shot` tab gives a smaller matrix than the page renders: stop,
   then repair it (add the tab to `TABS`, fix the run) or escalate to the
   owner. Meanwhile no verdict and no observation record is written, so a
   re-judge stays open.
3. **Read & critique** — Read a representative spread (both themes; the
   graph-heavy `sw` / `dag` tabs; the `390px` mobile landing) and judge:
   contrast and legibility in **both** themes; label truncation and edge/box
   overlap in the graph views; responsive reflow and overflow at `390px`; wasted
   space. Heed the README caveat: a sticky-header overlap in a `-full` shot is
   often a `fullPage` capture artifact — confirm it against the matching `-fold`
   (viewport) shot before believing it.
4. **Brief a TC-055 judge with the test-bound scope.** When the critique is
   TC-055's judgment, each judge's brief carries, beside the rubric
   (`docs/rubrics/dashboard-usability.md`), the SN/SR intent, LLR-055 and the
   shots, the **scope lines of the test-bound rows**: for every live anchor,
   the row a test holds its core in, quoted from the registry at the judged
   commit with its TC id. Today that is LLR-099/TC-102 (T2), LLR-119/TC-124
   (T4), LLR-105/TC-108 and LLR-285/TC-296 (T5), and LLR-120/TC-125 and
   LLR-292/TC-305 (T8) — the rows the rubric's header and anchors name; when
   the rubric binds another, the brief carries it too. Quote each row's
   `SCOPE` statement, or its whole `detail` where it has none. The judge then
   rules only each anchor's residue: a clause it believes a test misses is a
   gap in that test, routed through change-intake, never a verdict. A judge
   that could not fully read the rubric records no verdict.
5. **File findings as their own WIs.** This loop **builds the eyes; it is not a
   redesign.** A rendered defect becomes a new WI (register it in
   `docs/work/`, cite the shot), never an inline dashboard
   edit inside the critique session.
