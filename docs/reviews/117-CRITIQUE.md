# 117-CRITIQUE — dashboard UI uniformity (SR-053), post-WI-290 render surface

**Trigger:** the WI-243 perceptual re-fire — the dashboard render surface
(`project-trajectory/scripts/gen_trajectory.py`) last changed at `ffc4b0c`
(WI-290), *after* the previous perceptual evidence
[112-CRITIQUE.md](112-CRITIQUE.md) (`122ad01`, 2026-07-22), so
`check_trajectory --root . --strict` reported the fail-closed
`perceptual-stale SR-052;SR-053;SR-054` error. This session re-dates the
perceptual evidence past that render change and judges **SR-053** cold.
112-CRITIQUE judged the usability anchor set (`T1…T8`); SR-053's uniformity
anchors were last judged at the 042/048/052 round, so this is a full re-judge.

**Numbering (deliberate):** the perceptual gate names all three Critique SRs, so
three critiques were dispatched together — [115](115-CRITIQUE.md) usability
(SR-054, APPROVE f=0), [116](116-CRITIQUE.md) accessibility (SR-052,
CHANGES-REQUESTED f=1), and this one, uniformity (SR-053, CHANGES-REQUESTED f=7).
`check_trajectory._latest_critique_file` selects the **highest-numbered** file and
`_latest_critique_verdict` reads its verdict, a proxy that assumes one live
critique at a time. Filing a batch breaks that assumption, so the batch is ordered
**worst verdict last**: this file is the one the critique-loop ratchet reads, which
keeps the ratchet armed rather than letting a sibling APPROVE mask the open
findings. Do not renumber these without preserving that property.

**Critic:** `OPENCODE-KIMI` (`opencode-go/kimi-k3`, OPENCODE family) — a fresh,
family-heterogeneous **non-Anthropic** session per SR-084 / SN-024, dispatched by
hand through the OpenCode-Go gateway. Its brief was built to the SR-084 contract:
rubric + SN/SR intent + artifact recipe, and **no build transcript and no
implementer self-assessment**. It worked in an isolated sandbox holding only the
generated artifact, the shot matrix, the rubric, and the recipe — it never saw
this repo, the train branches, or any prior verdict.

**Artifact:** `PROJECT_STATE.html` generated at HEAD `86b7ad2`, plus the full
declared matrix (36 PNGs: 390/1280/1680 × light/dark × 5 tabs, full-page + the
landing folds) from `node scripts/dashboard-shots/shoot.mjs`.

**Rubric:** [dashboard-uniformity.md](../rubrics/dashboard-uniformity.md),
anchors `U1`–`U5`.

---

## Anchor verdicts

**U1 — One type scale and spacing rhythm:** FAIL (minor) — all four graph
emitters share the `--nlabel:10px`/`--nsub:8.5px` node-label tokens and one
`.legend`/`.detail` text set, but the Process "working loops" SVG labels its
nodes at ad-hoc 12px/9.5px/13px (`.stgt/.stgn/.hooplab/.hubname`, line 301), a
per-view deviation for the same kind of node (1280px-light-process-full vs
1280px-light-sw-full).

**U2 — One status/phase/type color vocabulary applied consistently:** PASS —
every same-concept rendering matches to the exact hex: icicle cells = `tierColor`
(SN-001 `#4338ca`, SR-001 `#0e7490`, TC-001 `#047857`) = Knowledge
legend/blocks; WI fills = `statusColor` (done `#047857`, queued `#94a3b8`,
retired `#78716c`) = When status legend; phase key swatches = roadmap block fills
(8/8); SW legend = SW block fills (module `#0e7490`, file `#7c3aed`).

**U3 — Uniform node/edge/legend/detail-panel styling:** FAIL — nodes/edges/detail
asides are well unified (rx=8 drill blocks, ports, `.cedge` accent stubs, shared
`.detail` aside on all four data tabs), but the hover-highlight ring is `#f59e0b`
amber in the icicle (`#ice .cell.hl rect`, line 114) and `var(--accent)` indigo
in every drill emitter (`.drill .block.hl rect`, line 243); and the When tab's
phase key uses inline `.55rem`/2px-radius `span.ph` swatches while all other keys
use the `.legend` row of `.8rem`/3px-radius swatches (line 141-143).

**U4 — One interaction idiom per structure:** PASS — one shared drill controller
gives When/How/Knowledge identical dblclick-or-Enter descend, breadcrumb return,
hover ring, click/focus detail; the icicle documents its hover+click-only idiom
(it has no layers to descend). The invisible hover ring on the phase-3 block is a
color defect, cited under U5.

**U5 — One concept per colour:** FAIL — multiple same-hue-two-meanings
collisions, including the rubric's own named bad pattern: `#047857` is both
`done` (status legend, 473 WI fills, EXECUTION meter on every tab) and
`Test Case` (icicle TC lane, Knowledge TC block, both legends); `#b45309` is both
`active` and `Process Guide`; the phase key itself contains two indistinguishable
purples (`1+2 #6d28d9` vs `unphased #7e22ce`, ΔE≈7.4) rendered side by side in
one legend and one roadmap.

## Findings

- [MAJOR] U5 -> `#047857` carries two meanings: `done` (When tab status legend
  swatch `var(--done)`; 473 done-WI block fills; header EXECUTION meter
  `.meter.exe`, line 57) vs `Test Case` (`tierColor tc:'#047857'`, line 339;
  icicle TC lane + TC legend swatch; Knowledge TC block + "Test Case" swatch,
  line 276). Because the header meter renders on every tab, both meanings
  co-render on one screen — see 1280px-light-arch-full.png (green EXECUTION bar
  above the green TC lane and green TC legend swatch) and
  1280px-dark-know-full.png (green meter + green TC block/swatch). This is
  verbatim the rubric's named Bad pattern ("done-green reads as Test Case") ->
  give the TC tier a hue of its own (or move `done`); keep one green = one
  meaning -> @owner (dashboard / gen_trajectory.py)
- [MAJOR] U5 -> phase-accent key has two perceptually indistinguishable purples
  for different concepts: `1+2 = #6d28d9` vs `unphased = #7e22ce` (ΔE≈7.4
  CIE76), shown (A) side by side in the "Phase accent:" legend and (B) as the
  "1+2" block (top-left) and "unphased" block (center) in the same roadmap —
  1280px-light-dag-full.png, 1680px-dark-dag-full.png; a viewer cannot tell which
  purple means which concept (phase `3 #4f46e5` sits in the same violet family,
  ΔE 15–18, borderline) -> move `unphased` out of the violet family (a neutral
  stone/gray reads naturally for "no phase") and re-check pairwise ΔE across the
  8-swatch key -> @owner (dashboard / gen_trajectory.py)
- [MAJOR] U5 -> `#b45309` carries two meanings across the document: `active — you
  are here` (When tab status legend, line 233/340) vs `Process Guide` (Knowledge
  tab PG block + legend swatch, line 276) — 1280px-light-dag-full.png vs
  1280px-light-know-full.png; the status and type vocabularies reuse the identical
  hex, violating the anchor's whole-document one-hue-one-meaning rule -> shift PG
  (or `active`) to a hue outside the status set -> @owner (dashboard /
  gen_trajectory.py)
- [MINOR] U5 -> second-tier same-hex aliases: (a) `--accent #4f46e5` (links,
  active tab, `.cedge` containment stubs, `.port.in` rings, hover/focus rings,
  DEFINITION meter, Process hub) is also the phase-3 accent — in light theme the
  hover/focus ring on the phase-3 block is painted in the block's own fill, so
  highlight feedback vanishes on exactly that block (1280px-light-dag-full.png);
  (b) `#0e7490` = SR (What/Knowledge legends) and module (How legend); (c)
  `#64748b` = LLR (What/Knowledge legends) and external actor (How legend) and
  light-theme `--muted` body text, which co-renders with the LLR swatch on the
  What tab (1280px-light-arch-full.png); dark `--muted #94a3b8` likewise equals
  the `queued` swatch (1680px-dark-dag-full.png) -> pick a phase-3 accent distinct
  from the UI accent; give module/external their own hues or declare the aliasing
  intentional; keep muted text off legend hues -> @owner (dashboard /
  gen_trajectory.py)
- [MINOR] U3 -> hover-highlight ring token differs across SVG emitters: icicle
  cells ring in `#f59e0b` amber (`#ice .cell.hl rect{stroke:#f59e0b}`, line 114)
  while every drill block (When/How/Knowledge) rings in `var(--accent)` indigo
  (line 243) — the same "hovered node" concept rendered two ways (What tab vs
  Knowledge tab) -> one shared hl token for all emitters -> @owner (dashboard /
  gen_trajectory.py)
- [MINOR] U3 -> two legend idioms: the When tab's phase key renders inline in the
  explainer as `.55rem`/2px-radius `span.ph` chips, while the status key on the
  same tab and the tier/type keys on What/How/Knowledge render as `.legend` rows
  of `.8rem`/3px-radius swatches below the panel (1280px-light-dag-full.png vs
  1280px-light-know-full.png) -> render the phase key through the shared `.legend`
  component -> @owner (dashboard / gen_trajectory.py)
- [MINOR] U1 -> Process "working loops" SVG labels nodes at ad-hoc
  12px/9.5px/13px (`.stgt/.stgn/.hooplab/.hubname`, line 301) while the icicle,
  dag, SW, and knowledge emitters share `--nlabel:10px`/`--nsub:8.5px` for the
  same node-label role (1280px-light-process-full.png vs
  1280px-light-sw-full.png) -> reuse the shared node-label tokens (or add one
  documented scale step) -> @owner (dashboard / gen_trajectory.py)

## Notes

- The artifact ships dead wiring from the retired flat-DAG renderer:
  `dag.querySelectorAll('.wi')` matches 0 elements and the `#dag .wi`/`.edge`/
  `#knowgraph .knode` CSS (including the amber `.hl` rules) never applies in this
  render. Harmless to uniformity as rendered, but it means the When tab's "Hover a
  work item to highlight its neighbourhood" promise is backed by dead code in this
  mode — flagging for the usability critique (SR-054), not scored here.
- Dark theme keeps the status/tier/phase palettes on the same tokens (only chrome
  adapts) — good; the collisions above are therefore identical in both themes.
- `#7c3aed` Interface (Knowledge) vs file/shared-contract hub (How) is arguably an
  intentional alias (an interface *is* a shared contract); included in finding 4
  for an explicit ruling, not as a clear defect.
- The Process tab's lifecycle boxes (Vision/SN/SR/LLR/TC/code+tests) deliberately
  render neutral-white with an accent border only for the tiers the current gate
  spans, and the caption says so — judged meaningful encoding, not a U2 failure.
- The mid-page sticky-header overlap in 390px full-page shots is the documented
  `fullPage` capture artifact; the `-fold` shots show the header correctly fixed
  at top.
- DEFINITION meter (`--accent #4f46e5`) vs SN tier (`#4338ca`) are near-indigos
  (ΔE≈8.4) co-rendering on the What tab — chrome vs type, noted but not scored.

VERDICT: CHANGES-REQUESTED findings=7
