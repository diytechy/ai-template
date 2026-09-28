# ADJUDICATE — WI-685 — re-judge TC-055 at fe96ec69

Independent re-judge of the observation case TC-055 (verifies SR-054 and
LLR-055, `Verification=Critique`, no result on record). Adjudicator: Claude
Fable 5.1, a fresh session that authored neither `gen_trajectory.py`, the
`rendering/` package, the rubric nor the case, and that received the rubric,
the SN/SR intent (SN-024, SN-023, SR-054, LLR-055) and the artifact recipe —
never an implementer's self-assessment. Judged from the kit-rendered brief, by
the case's Method against its Expected, on the tree at fe96ec69, reading the
declared inputs (`docs/rubrics/dashboard-usability.md`, SR-054, LLR-055,
`project-trajectory/scripts/gen_trajectory.py`,
`project-trajectory/scripts/rendering`). No earlier critique, note or log
entry about the case was taken as evidence; `docs/reviews/074-CRITIQUE.md`
(the Evidence cell) was opened only to learn the verdict format.

## Disclosure on the Method's "family-heterogeneous" clause

The Method asks for a family-heterogeneous session. The rendering code's
recent commits carry `Co-Authored-By` trailers from the Claude family (Fable
5 / 5.1, Opus 5 / 5.5), and this adjudicator is Claude. The session is fresh
and non-author, but not cross-family. SR-154 (the routing contract SR-184's
rationale defers family policy to) prefers a cross-family draw and degrades to
the documented same-family mode "never a silent skip"; this record is that
degradation, stated here so a reader can weigh it. The coordinator's brief
asked for the critique if the declared tooling runs on this box, and it does.

## The artifact recipe, as actually run

- `scripts/dashboard-shots/shoot.mjs` (pinned playwright 1.61.1, chromium
  build 1228), after `npm ci` and `npx playwright install chromium` on this
  box. It regenerated `PROJECT_STATE.html` (the only difference from the
  committed copy was the as-of stamp, `e520b6e6` → `fe96ec69`; the working
  copy was restored with `git checkout` afterwards so the tree stays at HEAD)
  and wrote the declared matrix: widths 390 / 1280 / 1680 × themes light /
  dark × tabs `arch` (What), `dag` (When), `sw` (How), `process` — 24
  full-page shots + 6 landing folds = 30 PNGs; the `know` tab was reported
  "declared tab(s) not in this dashboard, SKIPPED" as the README says for this
  repo's dial.
- The tall full-page shots were cut into 1800-px (2000-px at 390) tiles and
  read at retina scale; the roadmap, architecture and station-cycle diagrams
  were additionally cropped and enlarged 2× to inspect edge routing. The
  1680 shots render the same max-width layout as 1280 (identical page heights)
  and were spot-checked rather than read tile by tile.
- Limit of a static shot set: no element is focused or hovered, so focus
  rings and hover affordances (part of T5) could not be seen; the judgment on
  T5 rests on the resting-state controls in both themes.

## Anchors judged — the rubric's live set only (T2, T4, T5, T8)

The rubric header at fe96ec69 lists T2, T4, T5, T8 as live and binds T1, T3,
T6, T7 to tests (LLR-115/TC-120, LLR-100/TC-103, LLR-117/TC-122,
LLR-116/TC-121). Nothing below cites a retired anchor; anything that belongs
to a bound anchor is routed as a non-blocking note, never a verdict finding.

- [MINOR] T2 default-density legibility, all widths and themes -> the landing view opens on the What tab with the spine drill at its top tier only: 31 SN blocks in one column (the drill SVG is 208 units wide, `data-descend` on each block), no SR / LLR / TC wall. The When tab opens on the tiered roadmap (13 phases as blocks, "renders as wired blocks only when it holds more than 3 members"), not 689 work-item nodes. The How tab opens on the depth-0 system context (5 entities, 7 crossings) and a 4-component architecture; the Process tab on seven stage cards and a 12-node station cycle. At 390 the same tiers stack vertically and the legends wrap; nothing opens exploded. Satisfied.
- [MINOR] T4 label legibility — the residue that stays with the critic: is a truncation a reader meets actionable? -> three truncation sites seen. (i) SN block summaries end in "…" and the view's own caption says "click to read its full text" into the persistent detail panel — actionable. (ii) Boundary-crossing labels on the system-context arrows end in "…" ("Governed writes: artifact, registry and config edits …") and the full `Carries` text sits in the Boundary crossings table directly below the diagram on the same tab — actionable. (iii) The next-work card ends with "+13 more — see the When roadmap", a named reveal — actionable. No label overlapped another or ran past its block in any of the 24 full shots at default zoom, in either theme. Satisfied.
- [MINOR] T5 interactive-control legibility in both themes -> tab buttons: inactive labels mid-grey on the light surface and light-grey on the dark surface, the active tab in the accent purple / lavender with a 2-px underline, legible in both. Drill affordances: the "➤" descend glyph on every SN block and component block is accent-coloured on both surfaces; the "▶" disclosure triangles on the four Runtime-flow summaries are ink-coloured in both; the "+13 more — see the When roadmap" reveal and the two `PROCESS*.md` links are underlined accent text in both. The selection legend ("→ selected: prerequisites" blue, "selected → dependents" orange in light, amber in dark) reads in both. No control washes into its background in dark. Focus rings not observable (limit stated above). Satisfied on what the shots can show.
- [MINOR] T8 edge routing — the residue that stays with the critic: crossings minimized and, where unavoidable, in open space -> Architecture (4 components, selected CMP-006): four blue/orange crossings, all in the gutter above the boxes where the prerequisite verticals rise from CMP-007's and CMP-008's out-ports to meet the dependent rails; none under a label, none inside a port fan (the rails clear the port circles). Station cycle: the three lane-outcome curves and the two return curves are nested, not crossed; the dashed "lost race → refresh again" loop has its own channel below the merge row; no edge crosses a box. System context: seven straight crossings, no crossing; the dotted REL-002 arc is alone on the left. Roadmap: the selected edges (6 → unphased → 1+3+4+5+6) run orthogonally through the inter-column channels; the faint context edges route through the same channels and along the row gutters and cross each other only there. Satisfied.

VERDICT: APPROVE findings=0 anchors=T2,T4,T5,T8

Result: the case meets its Expected on the tree at fe96ec69 — APPROVE citing
live anchors only. Recorded `pass` with
`python project-trajectory/scripts/record_observation.py --tc TC-055 --outcome pass --by "Claude Fable 5.1, WI-685"`;
the record file it writes is committed alongside this verdict.

## Non-blocking observations (route through change-intake, never a verdict)

1. **The What (spine) drill shows 9 of 31 SN blocks.** The top-tier SVG is
   2122 units tall inside a container with `overflow:auto; max-height:660px`,
   so at every width the card ends after SN-009 with 22 more below the fold of
   the card. Headless Chromium draws no scrollbar, and overlay-scrollbar
   platforms show none until the reader scrolls, so the shot set cannot tell
   whether a first-time reader sees an affordance; a "31 needs — scroll" caption
   or the count on the card would make it certain. Findability and return-path
   belong to `TC-120` / `TC-103`, so this is a candidate gap for those tests or
   its own WI, not a T-anchor finding.
2. **Faint context edges in the roadmap, dark theme.** With a card selected
   by default, the unselected edges are drawn so faint on the dark surface that
   they cannot be followed without selecting; in light they are barely
   followable. The rubric's own text makes selection the way to trace an edge,
   so T8 is not failed on it; the owner may want a slightly stronger faint tone
   in dark.
3. **"↔ Scroll sideways to see the full view" above the What (spine) drill
   at 390 px**, although that drill is 208 px wide and never scrolls sideways
   — the hint appears to be emitted per drill regardless of width. Cosmetic.
4. **Right-edge clipping of the roadmap at 1280 / 1680** (the "1+3+4+5+6" and
   "3" phase blocks cut at the container edge, with the scroll hint above) and
   the small scale-to-fit labels of the roadmap and system-context diagrams at
   390 are `TC-121`'s floor working as designed per the rubric's notes; recorded
   here only so a later reader knows they were seen and not judged.

OUTCOME: RECORDED result=pass
