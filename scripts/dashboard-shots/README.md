# dashboard-shots — dashboard render-critique loop (WI-189, meta-only)

Turns the generated dashboard [`PROJECT_STATE.html`](../../PROJECT_STATE.html)
into **rendered pixels** an agent (or human) can actually look at, so a critique
judges what a viewer sees — not ~790 KB of source markup. It also serves as the
**artifact recipe** for a future `Verification=Critique` TC on dashboard quality
(the critique-loop contract in
[`PROCESS_OPTIONS.md`](../../project-trajectory/PROCESS_OPTIONS.md), *"Critique
verification"*, requires a perceptual TC to name its render recipe).

> **Meta-only, dev-only.** This tool is **not** shipped downstream. The kit's
> stdlib-only / install-nothing posture governs `project-trajectory/scripts`;
> it does **not** govern this dev helper (owner ruling at WI-189 filing — same
> meta-only scoping as WI-175 Rec 3). Nothing here changes
> `dev-setup.template.*` or adds a runtime requirement to any kit script.

## Pinned versions

Recorded so screenshots stay comparable across sessions (bump deliberately):

| Package | Version | Browser |
|---|---|---|
| `playwright` (see [package.json](package.json)) | `1.61.1` | chromium build **1228** (Chrome 149.0.7827.55) |

## Install (once per machine)

Needs Node (any recent LTS; developed on Node 24). From the repo root:

```sh
cd scripts/dashboard-shots
npm ci                          # or: npm install — installs the pinned playwright
npx playwright install chromium # downloads the pinned chromium into the OS cache
```

The browser lands in the OS Playwright cache (`~/Library/Caches/ms-playwright`
on macOS, `~/.cache/ms-playwright` on Linux, `%USERPROFILE%\AppData\Local\
ms-playwright` on Windows) — **outside** the repo, and `node_modules/` +
`shots/` are gitignored, so nothing here is committed except the pinned
`package.json`. The meta `scripts/dev-setup.sh --check` reports whether the tool
is installed (warn-only; it is optional).

## Run

One command regenerates the dashboard and emits the full matrix:

```sh
node scripts/dashboard-shots/shoot.mjs
```

It prints every written path. Then an agent session **Reads** the PNGs (the
Read tool presents images visually) and critiques them.

## The declared matrix

Declared as constants at the top of [`shoot.mjs`](shoot.mjs) — **edit there,
never improvise per session**. The current matrix:

- **Widths:** `narrow` 390 · `laptop` 1280 · `wide` 1680 (the responsive
  breakpoints the layout reacts to).
- **Themes:** `light` · `dark` — driven by `prefers-color-scheme` (the dashboard
  is CSS-media-query themed, so emulating `colorScheme` is the whole toggle).
- **Tabs:** all five — `arch` (What) · `dag` (When) · `sw` (How) · `know`
  (Knowledge) · `process` (Process).
- **Shot type:** full-page for every cell; **above-the-fold** additionally for
  the landing `arch` tab (where "what you see first" is the critique that
  matters most).

Output names are deterministic: `shots/{width}px-{theme}-{tab}-{full|fold}.png`
(3 × 2 × 5 full = 30, + 6 landing folds = **36** shots). Pixel content is *not*
byte-deterministic (the git as-of stamp changes per commit) — that's fine; this
is a perceptual loop, not a pixel-diff (a pixel-diff baseline is a possible
follow-up, WI-189 non-goals).

## Caveats when reading the shots

- **`fullPage` + a sticky header.** In a full-page capture, a `position:sticky`
  element can render at an unexpected scroll offset (e.g. the top bar appearing
  to overlap a card). Confirm any sticky-overlap suspicion against the
  `-fold.png` (viewport) shot before filing it as a real defect — it is often a
  capture artifact, not what a viewer sees.
- **This WI builds the eyes, not a redesign.** Findings the loop surfaces are
  filed as their **own** WIs (WI-189 non-goals); don't fix the dashboard from
  inside a critique session.
