# 048-CRITIQUE — PROJECT_STATE.html vs SR-052/053/054 rubrics

Independent critique session (SR-047 loop). Artifact produced fresh by this session:
`python project-trajectory/scripts/gen_trajectory.py` at commit e781a72 → `PROJECT_STATE.html`
(695,057 bytes). Method note: judged by static inspection of the emitted HTML/SVG/CSS/JS
(markup walk of every emitter, handler trace of all five script blocks, WCAG 2.1 contrast
computed numerically from the emitted hex pairs) — not a browser render; the encodings and
handler wiring judged are the artifact's own, and I say so per the recipe's proxy rule.
No implementer notes, status.md, or log.md were read.

Contrast pairs measured (all pass the A4 floor): white on #4338ca 7.90, on #0e7490 5.36,
on #64748b 4.76, on #047857 5.48, on #b45309 5.02, on #7c3aed 5.70, on #475569 7.58;
#0f172a on #94a3b8 6.96; muted #64748b on bg #f8fafc 4.55 (tight but ≥ 4.5).

## Findings

- [BLOCKER] A1 -> When-roadmap and How-SW drill views: 213 of 265 `.block` nodes — every non-descendable leaf (work items with `data-wi`, modules/files/externals with `data-node`) — carry NO `tabindex`, while each opens the detail aside on click and has a `focus` handler wired (gen_trajectory's drill emitters + the `.block[data-wi]` / `.block[data-node]` listeners) that can never fire on an unfocusable element; a keyboard-only reader cannot open any WI or module detail in either drill (only the 52 descendable containers and the icicle/knowledge nodes are focusable) -> emit `tabindex="0"` on leaf blocks in the drill emitter, matching the containers' treatment (their `<title>` already supplies the A2 name) -> @owner
- [MAJOR] T1 -> "Find the next work" fails the one-tab-switch test: the active WI-144 is named only in a leaf layer three descents deep in the When drill; the landing hero says "1 active" without naming it, the When top layer shows 5 phase blocks with no "you are here" propagation (the legend promises "active — you are here" but no container on the entry layer carries any active cue), and Process §4 only links out to `docs/next-wi` rather than showing it -> surface the active/next WI id + title on the hero card or the Process resume-loop panel, and/or mark the container chain to the active leaf in the When top view -> @owner
- [MAJOR] U2 -> Phase-accent palette collides with the status and tier vocabularies inside the same document, and inside the same When tab: phase `v3` = `#047857`, the exact green the same tab's legend declares as `done` (and the TC tier color), yet v3 is the phase holding the *active* WI-144, so its container reads "done" while in progress; phase `v2+v3` = `#b45309` = the `active` amber (and the OKF Process Guide color); `unphased` = `#0e7490` (SR tier / module kind); `v2` = `#7c3aed` (file kind / Interface type) — the color vocabulary is not "one" when one hex means done-status on a leaf and phase-identity on its sibling container; this is a NEW failure mode (U2's letter bans same-concept-different-color, not different-concepts-same-color within one view), so per the accumulation rule propose anchor **U5 — No cross-vocabulary color collision: a hex assigned to one concept vocabulary (status, tier, kind, phase) is not reused by another vocabulary rendered in the same view** -> give phase accents their own hues disjoint from the status/tier/kind palettes -> @owner
- [MINOR] U3 -> The same spine concept gets a different node/edge treatment per emitter: a TC renders rx=3, stroke `rgba(255,255,255,.35)` .5px at 200×17 in the icicle vs rx=6, stroke `rgba(15,23,42,.15)` 1px at 150×30 in the knowledge graph (drill blocks are a third idiom at rx=8); knowledge `kedge` hardcodes `#94a3b8` 1.2px where drill `wire` uses `var(--muted)` 1.5px for the same directed-dependency stroke idiom (they diverge in light mode) -> share one corner-radius/stroke token set across the three emitters (or route kedge through `var(--muted)` and align rx), keeping the icicle's proportional-cell geometry if declared -> @owner
- [MINOR] T2 -> Knowledge view defaults to an unmanaged density: 125 nodes in a flat 812×3338 lane column (5× the 660px viewport) with spine edges spanning thousands of px, so tracing one edge means long scrolls with both endpoints never co-visible; no collapse/grouping applies (the >3 rule governs only the containment drills) -> add a density layer to the knowledge emitter (collapsible type lanes, or spine-family clustering) so a large bundle opens legible -> @owner
- [TC-HARDEN] A1 -> measurable sub-criterion for the TC: every emitted SVG `<g>` that the script wires a click/focus handler to (`data-wi`, `data-node`, `data-id` selectors) must carry `tabindex` — statically checkable on the generated HTML by check_trajectory-style assertion -> routes via change-intake (process.md §5) -> @owner
- [TC-HARDEN] U2/U5 -> measurable sub-criterion: the declared palettes (status, tier, kind, phase accents) collected from the emitted legends/CSS must be pairwise disjoint sets of hexes -> routes via change-intake (process.md §5) -> @owner

## What passed

A2 (every focusable node and all 265 blocks carry `<title>`; descendables add `role="button"`
+ `aria-label`; tabs/crumbs are native buttons with visible text), A3 (status pairs color with
✓/●/○ glyphs and `(done)/(active)/(queued)` title text; tiers carry id-prefix text + lane
headers; legends label every swatch), A4 (all pairs ≥ 4.5:1, table above), U1 (one `--nlabel`/
`--nsub` scale across icicle/drill/knowledge; shared `.panel h2`/`.cap`/`.legend` scale), U4
(hover=highlight, click=detail, focus=both is uniform across icicle/knowledge/drills;
dblclick-or-Enter=descend uniform across both drills), T3 (breadcrumb with `aria-current` on
descent; detail renders in a persistent aside beside the view in all four tabs), T4 (labels
truncate with an explicit `…` backed by full `<title>` + click-detail — truncation *with*
affordance; cell/text geometry leaves no computed overlap at default zoom).

VERDICT: CHANGES-REQUESTED findings=5
