OUTCOME: pass

# WI-796: independent adjudication of the TC-055 re-judge at 5fb0fc74

**Adjudicator:** Claude Opus 5.5, independent. I did not author the dashboard code, the judges' verdicts or the compile in 001-REJUDGE-5fb0fc7.md. Under owner ruling OI-103 Q3, my call on each disputed finding is final.

**What I checked:** I read the rendered artifact C:/Projects/ai-template.wt/wi-796/PROJECT_STATE.html at lane HEAD 5fb0fc74 and the tiles the findings cite in review-tmp/wi-796-shots/tiles/. I read the judges' raw outputs in review-tmp/wi-796-judges/390-light.out.md and 1680-dark.out.md, and the rubric docs/rubrics/dashboard-usability.md as written. I also read the registry rows SR-054, LLR-055, LLR-099/TC-102 and LLR-105/TC-108, and the CSS cited at project-trajectory/scripts/gen_trajectory.py:544-561.

I also ran a browser probe that focuses nodes; it is not in the repo. It used the repo's pinned Playwright (scripts/dashboard-shots, chromium 1228) at a 390 px viewport. In both color schemes it loaded the rendered file, called `focus()` on every visible focusable SVG node in each tab, and read the computed `stroke` and `fill` of that node's `rect`.

## 1. 390 px light, MAJOR, T5: orange focus stroke on diagram nodes. REFUTED

The judge called the focused node's indicator the amber `--ring` fallback `#f59e0b`. That fallback is never painted in this render.

- **The verdict came from source, not pixels.** The judge says so: "The initial screenshots do not capture focus states; I confirmed the focus styling in PROJECT_STATE.html" (390-light.out.md). None of the five tiles it cites shows a focused node:
  - 390px-light-arch-full-r03of05-c1of1 shows the next-work card, the stat tiles and the tab bar.
  - 390px-light-sw-full-r05of18-c1of1 shows the boundary-crossings table.
- **The rule it cited cannot apply here.** `#ice .cell.hl rect { stroke:var(--ring,#f59e0b) }` (gen_trajectory.py:551) uses its fallback only when the cell has no `--ring` of its own.
  - In the rendered file, all 711 `g.cell` nodes carry an inline `style="--ring:#ffffff"` or `style="--ring:#0f172a"`. These are the per-fill inks from `_ring_ink` (LLR-105).
  - The `#dag .wi.hl` rule (gen_trajectory.py:559) has nothing to style: there are 0 `g.wi` nodes, because the When view renders as the tiered drill.
  - Drill blocks use `.drill .block:focus rect{stroke:var(--ring,var(--accent))}`.
  - In the whole document, `#f59e0b` appears only in these places:
    - the two dead fallbacks;
    - `#dag .edge.hl`, which has 0 matching `.edge` elements in `#dag`;
    - the dark-theme `--trace-out` token;
    - two retired-row descriptions.
- **What a keyboard user actually sees.** The probe found 0 amber strokes on focus in any tab, in either theme. The lowest ratio of the focus stroke against the focused node's own fill, per tab:

  | Tab | Light | Dark |
  |---|---|---|
  | What, at the root (31 SN blocks) | 6.29:1 (`#4f46e5` on `#ffffff`) | 5.98:1 |
  | What, one SN descended (22 icicle cells) | 4.76:1 (`#ffffff` on `#64748b`) | 4.76:1 |
  | When (20 blocks) | 4.99:1 (`#ffffff` on `#4d7c0f`) | 4.99:1 |
  | How (4 blocks) | 17.85:1 | 14.48:1 |
  | Process (9 stations) | 6.29:1 | 5.98:1 |

  Every one clears both 3:1 (the WCAG UI-boundary floor in the A4 anchor) and 4.5:1.
- **The arithmetic belongs to a test, not a verdict.** A ring's contrast against its host fill is LLR-105/TC-108's mechanized core: "the descend/hover/focus ring ... against EVERY node fill ... in BOTH themes". The accessibility rubric's retirement table says the same: "the focus ring also binds under SR-054 T5 as LLR-105/TC-108". A ring a critic believes fails is a gap in TC-108, routed through change-intake, not a verdict.

## 2. 1680 px dark, MAJOR, T2: 31 SN blocks in the What root layer. REFUTED

The What view does start collapsed. It is not a wall of nodes.

- **It opens tiered.** The landing layer, `data-layer="arch-root"` in PROJECT_STATE.html, holds only the 31 `g.block.sn` containers. Each one is a descend button (`aria-label="Descend into SN-0xx"`). There are 31 more layers below, all `hidden`, and the 711 SR/LLR/TC leaf cells live only in those layers.
  - Without the collapse, the view would show the whole spine at leaf scale: 31 SN, 120 SR, 278 LLR and 283 TC.
  - The collapse is exactly what LLR-099 specifies: "the What icicle start-collapses to one block per SN with descend-on-click". TC-102 expects "above 3 SNs it is a start-collapsed SN drill with NO leaf cell in the opening layer".
  - The `>3` rule decides whether a view tiers. Nothing in SR-054, LLR-099 or the rubric's T2 requires the root tier itself to hold 3 items or fewer.
  - The judge read "start-collapsed per the >3 rule" as "the root must collapse again". That is not the anchor's requirement.
- **What is left for a judge is whether the density reads legibly, and the tiles show it does.**
  - Tiles 1680px-dark-arch-full-r02of03-c1of3 and 1680px-dark-arch-full-r03of03-c1of3 show one column of evenly spaced, non-overlapping blocks. Each block has a bold id and a two-line summary, with a visible descend arrow and ports.
  - The column sits in a height-capped card whose bottom fade marks the cut. The `.clipb` mask is at gen_trajectory.py:534.
  - The rubric's Bad case is "opens fully exploded with hundreds of overlapping nodes". This view has 31 collapsed, labelled, non-overlapping containers and is not that.
  - The other five judges, including 1680 light on the same view, passed T2.
- **The judged clause belongs to the test.** "Should this view open collapsed?" is LLR-099/TC-102's core, held by tests/test_traj_views.py::test_t2_what_icicle_starts_collapsed_above_the_sn_threshold. The finding re-judges that core, not T2's live residue. Item 3 explains why the rubric invited that.

## 3. T2 listed live while LLR-055 moves its start-collapse core to LLR-099/TC-102. A real inconsistency, but it does not change finding 2

- **The live list itself is correct.** LLR-099's SCOPE keeps a residue under TC-055: "T2's remaining 'reads legibly at default density' judgement stays perceptual under LLR-055/TC-055". So T2 belongs in the rubric's live set, just as T4 and T8 do while parts of them are test-bound.
- **The T2 body is not consistent.** T4 and T8 each state their test-bound half in place and name what stays with the judge ("What stays yours is ..."). T2's body does neither:
  - It does not say that its start-collapse clause is bound to LLR-099/TC-102.
  - It still cites "the SR-089 `>3` rule". SR-089 no longer exists in docs/requirements/system-requirements.toml; WI-451 commit 0d5a9432 demoted it.
  - So a judge reads the clause the test holds as live, against a rule it cannot look up. Finding 2 is that failure: the judge ruled on the collapse decision itself.
  - TC-055's Expected says "a clause a test now holds is verified through the LLR/TC chain the registry records, not by a verdict". The rubric should make that visible at T2.
- **T5 has the same gap.** The rubric's T5 text never names LLR-105/TC-108. Only dashboard-accessibility.md's retirement table does. That is why finding 1 re-judged ring arithmetic.
- **The fix belongs in docs/rubrics/dashboard-usability.md, in each anchor's body, not in the header's live set.**
  - **T2:** add an in-place note in the T4/T8 pattern:
    - The start-collapse clause is bound to LLR-099/TC-102: above the threshold, a view opens tiered with no leaf in the opening layer.
    - A view you believe should open collapsed is a gap in TC-102. Route it through change-intake.
    - What stays yours is whether the opened density reads legibly.
  - **T2:** replace "SR-089" with the live carrier, LLR-099's '>3' rule.
  - **T5:** add the matching note. The ring and containment-arrow contrast against the host fill, in both themes, is bound to LLR-105/TC-108. What stays yours is whether the affordance reads as findable and inviting, which is LLR-105's own SCOPE line.
- **Effect on finding 2: none.** The refutation stands on the rubric as written. The view is start-collapsed by the rule as the registry records it, and it is not the wall the anchor describes. The inconsistency explains the finding; it does not rescue it.

## 4. The rendered `retired` tab is missing from shoot.mjs TABS. A real gap in the declared matrix, but it does not block this outcome

- **It is a gap.** scripts/dashboard-shots/shoot.mjs:46-52 declares arch, dag, sw, know and process. The rendered page also carries `<section id="retired">`.
  - TC-055's Method names "the rendered PNG matrix from scripts/dashboard-shots/shoot.mjs (widths x themes x tabs)". The matrix is meant to be the declared superset of rendered tabs; the comment at shoot.mjs:38-45 says so.
  - The script's own message, "dashboard tab(s) not in the declared matrix, NOT shot ... add them to TABS in this file", names the fix.
  - So one surface a reader can open had no pixels judged in this round. This re-judge's pass covers the four shot tabs and the nav, not the Retired tab's body.
- **It does not block, because the tab gives the live anchors almost nothing new to judge.**
  - The section has no `svg`, so T2 and T8 have nothing to judge there.
  - It holds one 5-row table inside the same `.tablescroll` and scroll-cue idiom that was shot and passed on How. Examples: 390px-light-sw-full-r05of18-c1of1, and the T4/T5 passes at all six widths and themes.
  - It has no ellipsis-cut cells.
  - Its tab button appears in the nav in every fold tile, for example 390px-light-arch-full-r03of05-c1of1.
- The round followed the Method's recipe; the recipe is what is stale. That does not void this round, but it should be fixed before the next one.

## Follow-ups

- **Rubric fix.** In docs/rubrics/dashboard-usability.md, add in-place binding notes to T2 (LLR-099/TC-102) and T5 (LLR-105/TC-108), each with a "what stays yours" residue as T4/T8 have. In T2, replace the dead "SR-089 `>3` rule" with LLR-099's rule.
- **Matrix fix.** Add `["retired", "Retired"]` to the TABS list in scripts/dashboard-shots/shoot.mjs. The next TC-055 round then shoots every rendered tab.
- **Judge prompt.** The next re-judge prompt should give the judge LLR-099's and LLR-105's SCOPE lines, the LLR rows that state the residue, alongside LLR-055. A judge then knows which clauses a test holds.
- **No defect fix is owed.** Neither finding names a defect a viewer meets.
- **Separate observation, not counted under any anchor.** When a drill block is focused, the trace strokes paint its neighbours' rect edges in `--trace-out` or `--trace-in`. Light-theme `--trace-out` is `#ea580c` and `--trace-in` is `#1d4ed8`.
  - Against status fills these measure about 1.2-2.6:1, for example `#ea580c` on `#047857` is 1.54:1.
  - Against the page surface they measure 3.56:1 and 6.7:1.
  - A trace highlight is not a control under LLR-105, so this is not a T5 finding.
  - If the owner wants trace strokes held to the host-fill floor, it is a candidate for change-intake.
