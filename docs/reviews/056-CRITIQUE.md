# 056 — CRITIQUE: PROJECT_STATE.html vs SR-052/053/054 rubrics

Independent critique session (fresh context, no implementer notes read). Artifact
produced by re-running `python project-trajectory/scripts/gen_trajectory.py`
(reported byte-identical to the checked-in `PROJECT_STATE.html` at commit
e781a72, so that file is the judged render). **Proxy disclosure:** this critic
cannot render HTML visually; the judgment is made from the emitted markup, CSS,
SVG geometry, and computed WCAG contrast ratios (luminance math on the actual
hex pairs). Contrast and geometry findings are exact; anything requiring true
pixel rendering (font metrics) is estimated and labelled as such.

What passes, briefly: tabs are native buttons; every SVG cell/block/knode
carries `tabindex="0"` + `<title>`; descendable containers carry
`role="button"`/`aria-label` with Enter/Space handlers and a breadcrumb; status
pairs color with ✓/●/○ glyphs and `(done)/(active)/(queued)` title text; the
three T1 reading tasks each resolve in 0–1 tab switches (state + next-WI on the
landing hero, connections one click away on the How tab); node label sizes are
unified via `--nlabel`/`--nsub`; the When and How-SW drills share one controller.

## Findings

- [MAJOR] A4 -> detail-panel status badge for queued work items: `renderDetail` sets the badge background to `statusColor.queued = #94a3b8` while `.detail .badge` fixes `color:#fff` at .68rem (~10.9px) bold — white on #94a3b8 measures **2.56:1**, far below the 4.5:1 normal-text floor; every one of the 27 queued WIs shows this badge when clicked -> use dark text on the queued badge (e.g. `#0f172a`, 6.96:1 — the same pair the queued blocks themselves already use) or darken the queued badge background -> @owner
- [MAJOR] A4 -> boundaries of the interactive container blocks (campaign/workstream blocks in the When drill, component/module containers in How-SW): rect `fill="var(--surface)"` with `stroke="var(--border)"` sits on a `.view` background that is also `var(--surface)` — the delimiting stroke measures **1.19:1** light (#e2e8f0 on #fff) and **1.22:1** dark (#1e293b on #0f172a), below the declared 3:1 graphical/UI-boundary floor, and these rects are `role="button"` descend targets whose only visual extent is that stroke -> give block strokes a ≥3:1 token (e.g. `var(--muted)`, 4.76:1 on white) or a fill tint distinct from the view background -> @owner
- [MAJOR] T4 -> container/campaign/file block labels overflow their blocks: `.blab` renders at 10px bold, centered, with **no truncation** (0 `textLength` attributes; the `…` affordance exists only on `.bsub`), so e.g. `working-surface-restructure-2026-07-11` (38 chars, est. ~200px) and `project-trajectory/hooks/pre-commit` / `CMP-004 — Unattended loop & floor` (35–37 chars) run past their 172px rects and over the port circles at the rect edges (estimated from char-count × bold-10px advance; the block is 172px, the text midpoint is the rect midpoint) -> apply the same ellipsis truncation to `.blab` that `.bsub` already gets (full name is preserved in `<title>`/`aria-label`), or size blocks to their label -> @owner
- [MINOR] U4 -> click-for-detail on containers differs between drills: in How-SW, clicking/focusing a component or module container fills the `#sw-detail` aside (the `.block[data-node]` wiring scoped to `#sw`); in the When view the same structure — a container block in the same shared drill — shows nothing on single click/focus (only leaf `.block[data-wi]` nodes are wired to `#dag-detail`), the exact "reveals in one view, nothing in another for the same node kind" divergence U4 names -> wire When-view phase/workstream/campaign blocks to `#dag-detail` with a summary detail (name, member count, status rollup) matching the SW idiom -> @owner
- [MINOR] U1 -> the small-text scale is ad-hoc across views: five near-duplicate sizes within .08rem (`.legend` .85rem vs `#dag/#sw p.tierlegend` .82rem — both legend captions, adjacent tabs; `.detail .status` .8rem vs `.detail .meta` .83rem in the same panel; `#process .pflow b` .85rem vs `.entry b` .88rem vs `.loopname` .82rem), plus `#ice .lane-head` at a one-off 11px beside the shared 10px `--nlabel` -> collapse to two shared tokens (e.g. `--small:.85rem`, `--xsmall:.8rem`) and reference them everywhere small text renders -> @owner
- [MINOR] T2 -> the Knowledge view opens fully exploded: one flat 812×3338px SVG holding 246 typed nodes and 267 edges inside a 660px-max scrolling viewport — roughly five viewport-heights of wall on first open, with no `>3` start-collapsed tiering, while the When and How-SW views correctly root at 5 phases / top components -> give the concept graph the drill idiom (root at SN, descend per tier) or start tiers collapsed with expand-in-place -> @owner
- [MINOR] U2 -> **new failure mode, proposed as new anchor U5**: distinct concept vocabularies collide on the same swatches — `#047857` means *done* (status legend) and *v3* (phase-accent legend) **within the same When tab**, and also *TC* (What tier) and *Test Case* (Knowledge type); `#b45309` means *active*, *v2+v3*, and *Process Guide*; `#0e7490` means *SR tier*, *module*, and *unphased*. U2 as written only bans same-concept-different-color, so this is not a U1–U4 breach; proposed **U5 — no cross-vocabulary color collision:** within one view, one swatch carries one meaning; status, phase, tier, and type vocabularies draw from visually distinct ramps -> give the phase-accent vocabulary its own hue ramp distinct from the status colors (glyphs and labels currently disambiguate, which is why this is MINOR) -> @owner
- [TC-HARDEN] add a generated-artifact test that extracts every emitted text/fill pair — including the JS-injected `.badge` inline backgrounds from `tierColor`/`statusColor`/`d.fill` against `.detail .badge`'s `#fff` — and asserts WCAG ratio ≥ 4.5 (normal) / 3.0 (large + strokes); this arithmetic check would have mechanically caught the 2.56:1 queued badge and the 1.19:1 container stroke -> routes via change-intake (process.md §5) -> @owner
- [TC-HARDEN] add a label-fit assertion over the emitted SVG: for every `<tspan>` inside a node rect, estimated width (char count × 0.62 × font-size) ≤ rect width, or the text ends in the `…` affordance; would have caught the 38-char campaign labels in 172px blocks -> routes via change-intake (process.md §5) -> @owner

VERDICT: CHANGES-REQUESTED findings=7
