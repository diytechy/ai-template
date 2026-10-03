# WI-713 — TC-055 re-judged (cross-family Critique) at cafa07ab

**Judges:** three independent Claude Opus 5.5 (`claude-opus-5-5[1m]`) sessions, one per width, none of which directed the work. Rendering code by Codex Sol, so the judgement is cross-family (TC-055's Method; wave-5 ruling 31). Each received the kit-composed brief, the rubric `docs/rubrics/dashboard-usability.md`, SR-054, LLR-055 and SR-054's needs, and the declared matrix from `scripts/dashboard-shots/shoot.mjs` (3 widths x 2 themes x 4 tabs + the landing fold, device scale 2) cut into 270 native-resolution tiles of at most 1500 px, never downscaled. None saw the case's earlier results, earlier reviews or the coordinator's notes. Compiled by the coordinator; the judges' words are condensed, not changed.

Live anchors (rubric header): T2, T4, T5, T8. T1, T3, T6 and T7 are bound to tests.

## Per anchor

- [PASS] **T2** at 390, 1280 and 1680 px (light, dark) -> every view opens collapsed: What as one block per SN, When as the 15-phase tier, How at its 4 top-level components; Process short and flat. No wall of nodes.
- [MAJOR] **T4** at 390, 1280 and 1680 px (light, dark) -> FAIL. The How tab's System-context (depth-0) diagram: each crossing's `carries` caption is wider than its wire lane and is drawn before the boxes, so the external-party cards cover its start ("uardrail…", "HE TEMPL…", "ead: the", " hosted") and the system box covers its end ("…packaged deliverable. The delivere", "…model runner: the prompt and brie", the ellipsis lost). The caption is fitted by character count (`rendering/traj_context.py:53`, `carrymax = 54`), not measured against the lane, and centred in the 246-unit gap between the party column (x 364) and the system box (x 610). The full text is in the Boundary crossings table and a hover `<title>` (no hover on touch). These are wire labels, outside TC-124's drill-block scope, so the anchor's floor ("no clipped or overlapping text") applies. At 1680 px the dotted REL-002 curve also runs through its own label. Tiles: `*-sw-full-r02*`, `-r03*` (all widths), `390px-*-sw-full-r03c1`, `-r04c1`.
- [PASS] **T5** at 390, 1280 and 1680 px (light, dark) -> tabs, active-tab underline, links ("… show all", PROCESS.md), descend arrows, port rings, selected outline and ▶ Flow toggles legible in both themes. Focus and hover states are not in the shot set.
- [MAJOR at 1680 px; MINOR at 1280 px; PASS at 390 px] **T8** -> FAIL. Crossings are not minimised where they could be: the Process station cycle's two curves from "Lane build" to "merged" and "partial" cross just below their shared source (swapping exit points removes it); in the How top view the lane order is reversed in both colour families, so the descending verticals cut the sibling lane before converging into CMP-006's input fan; in the When roadmap a vertical routing trunk runs about 7 CSS px from the output ports of "1+5" and "4", crossing the stubs at the fans, and perimeter-routed wires cross every lane. At 390 px only the left part of each wired diagram is on screen and its visible crossings are in open space. (The 1280 judge rated its finding MINOR but marked the anchor fail; the 1680 judge's MAJOR decides it.)

## Non-anchor observations (not counted)

- Screenshot artefact: the sticky header is captured about 1020 CSS px down every `full` shot.
- The default-selected node in the When and How views sits off-screen at 390 and 1280 px, so its highlighted trace is not visible; dark-theme context wires nearly vanish (the copy says faint by design).
- 390 px: the Boundary crossings table leaves ~600 CSS px blank under B-05 (an off-screen 40-id column sets the row height); description columns squeeze to ~70 CSS px; "Hover to highlight" copy on a phone.
- 1280/1680 px: External parties ids wrap mid-token ("EXT-" / "001"); process ladder ids wrap at the hyphen; the How graph (4 components) still scrolls sideways at 1680 px with CMP-006 under the edge fade ("W1 Registry & confor…"); the What icicle uses about a third of its card's width.

## Verdict

VERDICT: REVISE — ANCHORS: T2=pass T4=fail T5=pass T8=fail

The T4 failure is likely a consequence of WI-722's type raise (the context caption uses `--nsub`, raised from 8.5 to 10.5 px, against a 54-character cut sized for the old scale); the earlier cross-family judgement passed T4 at 1680 px before it. The T8 findings are routing quality, not new. Successor: WI-750.

OUTCOME: RECORDED result=fail
