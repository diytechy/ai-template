# WI-991: TC-055 re-judged (cross-family critique) at 2ebfb6951

**Why now:** TC-055's declared trigger, `component:CMP-009`, fired after its work-item floor
at merge `8894988` (inputs digest `sha256:bccad912db94…`; full digest
`sha256:bccad912db94480d13f443e3e1d05fb30c0472f07b9c7c13853035efebe85893`, from the spec at
`docs/work/active/wi-991/`). The latest result on record was
`TC-055.2026-10-25T092405Z.toml` (pass, observed 2026-10-25T09:24:05Z). Between `8894988` and
the rendered HEAD the rubric, `gen_trajectory.py` and `rendering/` did not change, and the
SR-054 and LLR-055 rows compare equal. The digest itself was not recomputed.

**Judges:** six independent Codex Luna (`gpt-6-luna`, high effort, codex-cli 0.162.1,
read-only sandbox) sessions, one per width and theme: 390, 1280 and 1680 px, light and dark.
The dashboard code is Claude-authored, so the judges are cross-family (TC-055's Method). A
Claude agent rendered, tiled, launched and compiled; it judged nothing. Each session's header
and rollout confirm `model: gpt-6-luna`, `sandbox: read-only`, `reasoning effort: high`,
workdir the lane root. All six were children of one foreground command that waited. No judge
failed to launch and none was re-run.

**Rendered:** lane `wi-991` at HEAD `2ebfb6951`. `PROJECT_STATE.html` was regenerated with
`gen_trajectory.py` first; the only difference from the committed file is the as-of stamp on
line 273 (`bfbfda55d` -> `2ebfb6951`). The declared `shoot.mjs` matrix (device scale 2) exited
0 and printed:

```
gen_trajectory: already up to date -> PROJECT_STATE.html
declared tab(s) not in this dashboard, SKIPPED: know (Knowledge (OKF))
shooting 5 tab(s): arch, dag, sw, process, retired

wrote 36 screenshot(s) to C:\Projects\ai-template.wt\wi-991\scripts\dashboard-shots\shots
```

(followed by the 36 shot paths). No rendered tab was reported `NOT shot`, so the skill's
step-2 stop rule did not apply. Five tabs were shot: What, When, How, Process and Retired.
Knowledge is absent because its dial is off.

Each judge received:
- the rubric verbatim, read from the lane at HEAD (compared equal to the file after the brief
  was built), which states the live anchors T2, T4, T5 and T8, each with only the residue the
  rubric leaves to the judge;
- the A4 threshold paragraph of `docs/rubrics/dashboard-accessibility.md`, verbatim, because
  T5 points there for its numbers and no judge can open it;
- SN-023 and SN-024 (need and acceptance), SR-054's requirement and acceptance, LLR-055's
  detail, and TC-055's method and expected, quoted from the registries at HEAD;
- the scope lines of the test-bound rows (skill step 4), quoted from the registries at HEAD
  with their TC ids: LLR-099/TC-102 (T2), LLR-119/TC-124 (T4), LLR-105/TC-108 and
  LLR-285/TC-296 (T5), and LLR-120/TC-125 and LLR-292/TC-305 (T8). Each was the row's
  `SCOPE` statement, from `SCOPE` to the end of `detail`. LLR-292 carries no `SCOPE`, so it
  was quoted as its whole `detail`. The rubric's header binds no other row;
- a statement that the run shot the complete declared matrix, split one width x theme cell
  per judge, and that T5 is judged in the judge's own theme and compiled across all six;
- how to read the tiles: a tile edge is a cut made for the review, not a clipped label; the
  README's sticky-header capture caveat; and that the shots show initial states only, with no
  hover, focus or descended state;
- its width and theme of the matrix, cut into native-resolution tiles of at most
  1500 x 1500 px (Playwright clips of the device-scale-2 shots). The tiles were attached
  through `codex exec -i` with an ordered manifest: landing fold, then What, When, How,
  Process and Retired. There were 328 tiles: 44 per 390 px judge, 48 per 1280 px judge and
  72 per 1680 px judge. The largest tile is 1280 x 1482 px.

Judges were told to judge only the live anchors, each only on the clause the rubric leaves to
them; to cite only live anchor ids; to route a clause a test holds as a test gap, never as a
finding or a verdict; to grade each finding MAJOR or MINOR, an anchor with only MINOR findings
passing; to record no verdict if they could not read the rubric or all their tiles; and not to
open `docs/reviews/`, `docs/log*`, `docs/test/observations/`, `docs/work/`, `docs/status.md` or
`OWNER_SCRATCHPAD.md`. Because the sandbox is read-only, each judge's final message was written
to `verdict-<width>-<theme>.md` by the CLI's `-o` flag. None saw earlier verdicts or the
implementers' self-assessment.

**No judge read any repo file.** No session's rollout holds a tool call of any kind: no judge
attempted a shell command, so the sandbox failure the WI-920 record describes neither showed
nor was tested here. Each judge judged from its brief and its attached tiles. Each reported
seeing its full image count (44, 48 or 72), and no judge reported a rubric or a tile it could
not read.

## Per judge

| Judge | T2 | T4 | T5 | T8 | Verdict line |
|---|---|---|---|---|---|
| 390 light | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 390 dark | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 1280 light | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 1280 dark | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 1680 light | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 1680 dark | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |

## Per anchor

- [PASS] **T2** (reads legibly at default density) at all six. 1280 light: "The initial views read at a usable density"
  (`1280px-light-arch-full-r02of03-c1of2`, `1280px-light-dag-full-r02of03-c1of2`,
  `1280px-light-sw-full-r08of09-c1of2`). 1280 dark: "The graphs are substantial, but the visible labels and structure remain readable."
  (`1280px-dark-arch-full-r02of03-c1of2`, `1280px-dark-dag-full-r02of03-c1of2`,
  `1280px-dark-sw-full-r08of09-c1of2`). 390 light: "The default views do not read as walls of nodes."
- [PASS] **T4** (truncation is actionable) at all six. 390 light: "Truncated work-item text has visible “show all” affordances"
  (`390px-light-arch-full-r02of05`, `-r03of05`). 1680 dark: "Visible truncations have a reveal path: the next-work card offers “+9 more,” other excerpts show “show all,” and the diagrams explain that clicking a block reveals its full text."
  (`1680px-dark-arch-fold-r02of02-c1of3`, `1680px-dark-arch-full-r02of03-c1of3`,
  `1680px-dark-dag-full-r02of03-c1of3`). 1280 light: "Truncated node labels have visible descend arrows"
  (`1280px-light-arch-full-r03of03-c1of2`, `1280px-light-dag-full-r03of03-c1of2`).
- [PASS] **T5** (controls not painted over a node fill, own theme) at all six, three per
  theme. 1680 dark: "The active tab text and underline are distinct against the dark page, and inactive tab labels remain readable."
  (`1680px-dark-dag-full-r02of03-c2of3`, `1680px-dark-sw-full-r02of09-c2of3`,
  `1680px-dark-arch-full-r02of03-c2of3`). 1680 light: "In this light cell, the tab labels and active underline are distinct against the page, and visible “show all” links and graph controls are readable and identifiable"
  (`1680px-light-arch-full-r02of03-c1of3`, `-r02of03-c3of3`, `1680px-light-sw-full-r08of09-c1of3`).
- [PASS] **T8** (crossings minimized, unavoidable ones in open space) at all six. 1280 light:
  "Visible crossings in the roadmap and architecture diagrams appear in open space; I see no crossing under labels or inside port clusters"
  (`1280px-light-dag-full-r03of03-c1of2`, `1280px-light-sw-full-r08of09-c1of2`,
  `1280px-light-sw-full-r09of09-c1of2`). 1680 dark: "crossings are apparent in the When roadmap but do not visibly obscure labels or port clusters."
  (`1680px-dark-dag-full-r03of03-c1of3`, `-r03of03-c2of3`, `1680px-dark-sw-full-r03of09-c2of3`,
  `-r09of09-c2of3`).

## Findings by anchor and severity

| Anchor | MAJOR | MINOR |
|---|---|---|
| T2 | 0 | 0 |
| T4 | 0 | 0 |
| T5 | 0 | 0 |
| T8 | 0 | 0 |

None. Every judge wrote `findings=0` and "Findings: None".

## Test gaps (not findings, not counted)

Five judges wrote "Test gaps: None". The 1280 light judge wrote: "TC-055 does not capture focused controls, so this cell cannot show focus-ring contrast."
This is left for the coordinator to route. T5's residue names "a focus ring on page chrome", and
the shot matrix holds no focused state, so no judge at any width or theme saw that clause.

## Non-anchor observations (not counted)

The 390 dark judge's T4 paragraph also says: "the wide tables and diagrams include a sideways-scroll cue for revealing content beyond the viewport"
The rubric binds viewport fit to T7/TC-121.

## Each judge's verdict, verbatim

### 390 light

```
Cell: 390 light
Images seen: 44
T2: pass. The What view presents a readable vertical spine (390px-light-arch-full-r04of05, 390px-light-arch-full-r05of05); When describes a tiered roadmap and shows a compact roadmap card (390px-light-dag-full-r04of05, 390px-light-dag-full-r05of05); How opens on four top-level components (390px-light-sw-full-r18of20). The default views do not read as walls of nodes.
T4: pass. Truncated work-item text has visible “show all” affordances (390px-light-arch-full-r02of05, 390px-light-arch-full-r03of05). The What and How diagram instructions also tell readers how to reveal full text (390px-light-arch-full-r04of05, 390px-light-sw-full-r19of20).
T5: pass. In this light cell, active and inactive tabs, “show all” links, and diagram arrows are visibly distinguishable from their backgrounds (390px-light-arch-full-r03of05, 390px-light-dag-full-r03of05, 390px-light-sw-full-r19of20).
T8: pass. The visible How diagram routes its distinct edges through open space, with no apparent crossings under labels or port clusters (390px-light-sw-full-r19of20). The system-context diagram’s visible relationship also arcs through open space (390px-light-sw-full-r04of20).
Findings: None
Test gaps: None
VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass
```

### 390 dark

```
Cell: 390 dark
Images seen: 44
T2: pass. The views read legibly at their initial density: the What nodes are spaced in a readable column, the When view presents a tiered roadmap, and the How map shows a small set of components at once (390px-dark-arch-full-r04of05, 390px-dark-arch-full-r05of05, 390px-dark-dag-full-r04of05, 390px-dark-sw-full-r18of20, 390px-dark-sw-full-r19of20).
T4: pass. Truncated execution and next-work text has visible “show all” affordances; the wide tables and diagrams include a sideways-scroll cue for revealing content beyond the viewport (390px-dark-arch-fold-r02of02, 390px-dark-arch-full-r02of05, 390px-dark-sw-full-r05of20, 390px-dark-retired-full-r03of05).
T5: pass. In this dark cell, tab labels and active markers, “show all” links, node arrows, and disclosure controls are visibly distinguishable against their backgrounds (390px-dark-arch-full-r03of05, 390px-dark-sw-full-r19of20, 390px-dark-process-full-r03of07).
T8: pass. The visible graph wires use distinct routes through open space; no crossing appears under a label or within a port cluster (390px-dark-sw-full-r04of20, 390px-dark-sw-full-r19of20, 390px-dark-process-full-r05of07, 390px-dark-process-full-r06of07).
Findings: None
Test gaps: None
VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass
```

### 1280 light

```
Cell: 1280 light
Images seen: 48
T2: pass. The initial views read at a usable density: What shows the spine without expanding into its descendants (1280px-light-arch-full-r02of03-c1of2); When describes a tiered roadmap and shows phase groups (1280px-light-dag-full-r02of03-c1of2); How opens to four top-level components (1280px-light-sw-full-r08of09-c1of2).
T4: pass. The next-work summaries expose “show all” where text is truncated (1280px-light-arch-fold-r02of02-c1of2; 1280px-light-arch-full-r02of03-c2of2). Truncated node labels have visible descend arrows (1280px-light-arch-full-r03of03-c1of2; 1280px-light-dag-full-r03of03-c1of2).
T5: pass. Light-theme tabs and active markers are distinct and readable (1280px-light-arch-full-r02of03-c1of2). Diagram controls are visible against their fills, and the views explain how to descend or select items (1280px-light-dag-full-r02of03-c1of2; 1280px-light-sw-full-r08of09-c1of2).
T8: pass. Visible crossings in the roadmap and architecture diagrams appear in open space; I see no crossing under labels or inside port clusters (1280px-light-dag-full-r03of03-c1of2; 1280px-light-sw-full-r08of09-c1of2; 1280px-light-sw-full-r09of09-c1of2). Process flow crossings also appear in open space (1280px-light-process-full-r03of04-c1of2; 1280px-light-process-full-r04of04-c1of2).
Findings: None
Test gaps: TC-055 does not capture focused controls, so this cell cannot show focus-ring contrast.
VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass
```

### 1280 dark

```
Cell: 1280 dark
Images seen: 48
T2: pass. The default views read at their displayed density: What shows a legible requirement tree, When groups the roadmap into phases, and How opens to a four-component overview. The graphs are substantial, but the visible labels and structure remain readable. (1280px-dark-arch-full-r02of03-c1of2, 1280px-dark-dag-full-r02of03-c1of2, 1280px-dark-sw-full-r08of09-c1of2)
T4: pass. Truncated labels have a visible way to reveal their full text: What explains that clicking a block opens its detail, and the next-work summaries expose “show all.” (1280px-dark-arch-full-r02of03-c1of2, 1280px-dark-arch-full-r03of03-c1of2, 1280px-dark-arch-fold-r02of02-c1of2)
T5: pass. In dark theme, active-tab text and underlines, inactive tabs, “show all” links, and diagram expand controls are distinguishable and readable against their backgrounds. (1280px-dark-dag-full-r02of03-c1of2, 1280px-dark-sw-full-r09of09-c1of2, 1280px-dark-process-full-r02of04-c2of2)
T8: pass. The visible diagram crossings appear in open space; I see no crossing obscuring a label or port cluster. The When and architecture views are busy, but their wires remain visually separate from node text. (1280px-dark-dag-full-r03of03-c1of2, 1280px-dark-sw-full-r03of09-c1of2, 1280px-dark-sw-full-r08of09-c1of2, 1280px-dark-process-full-r03of04-c1of2)
Findings: None
Test gaps: None
VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass
```

### 1680 light

```
Cell: 1680 light
Images seen: 72
T2: pass. The When roadmap opens as a tiered summary, and the What spine and How architecture views present spaced, readable blocks at their initial density (1680px-light-dag-full-r01of03-c1of3, 1680px-light-arch-full-r02of03-c1of3, 1680px-light-sw-full-r08of09-c1of3).
T4: pass. Truncations I can see have a reveal affordance: the next-work card and open-item text show “show all,” and graph blocks indicate they can be opened for detail (1680px-light-arch-fold-r02of02-c1of3, 1680px-light-arch-full-r01of03-c2of3, 1680px-light-arch-full-r02of03-c3of3).
T5: pass. In this light cell, the tab labels and active underline are distinct against the page, and visible “show all” links and graph controls are readable and identifiable (1680px-light-arch-full-r02of03-c1of3, 1680px-light-arch-full-r02of03-c3of3, 1680px-light-sw-full-r08of09-c1of3).
T8: pass. The visible When, How and Process diagrams route edges through open space; I see no crossing beneath a label or within a port fan (1680px-light-dag-full-r03of03-c1of3, 1680px-light-sw-full-r03of09-c2of3, 1680px-light-process-full-r03of04-c2of3).
Findings: None
Test gaps: None
VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass
```

### 1680 dark

```
Cell: 1680 dark
Images seen: 72
T2: pass. The What view shows the SN tier in readable cards, the When view opens as a tiered roadmap, and the How view opens at a component-level overview. The Process view presents its cycle as separated, readable stages. Evidence: `1680px-dark-arch-full-r03of03-c1of3`, `1680px-dark-dag-full-r03of03-c1of3`, `1680px-dark-sw-full-r09of09-c1of3`, `1680px-dark-process-full-r03of04-c1of3`.
T4: pass. Visible truncations have a reveal path: the next-work card offers “+9 more,” other excerpts show “show all,” and the diagrams explain that clicking a block reveals its full text. Evidence: `1680px-dark-arch-fold-r02of02-c1of3`, `1680px-dark-arch-full-r02of03-c1of3`, `1680px-dark-dag-full-r02of03-c1of3`.
T5: pass. The active tab text and underline are distinct against the dark page, and inactive tab labels remain readable. Other visible controls, including “show all,” also stand out from their backgrounds. Evidence: `1680px-dark-dag-full-r02of03-c2of3`, `1680px-dark-sw-full-r02of09-c2of3`, `1680px-dark-arch-full-r02of03-c2of3`.
T8: pass. The visible diagrams route edges through open space; crossings are apparent in the When roadmap but do not visibly obscure labels or port clusters. Evidence: `1680px-dark-dag-full-r03of03-c1of3`, `1680px-dark-dag-full-r03of03-c2of3`, `1680px-dark-sw-full-r03of09-c2of3`, `1680px-dark-sw-full-r09of09-c2of3`.
Findings: None
Test gaps: None
VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass
```

## Operator's note (facts for confirm-or-refute; no judge is overridden)

- **No anchor failed**, so there is no FAIL for these notes to check against source.
- **Judges ran fast and used no tools.** All six launched between 08:33:52Z and
  08:33:54Z and exited 0 after 40 to 49 s, with between 87,116 tokens (390 light) and
  165,470 tokens (1680 dark). No session made a tool call.
- **The attachments are the tiles, in order.** Each rollout embeds its images as PNG, and they
  are byte-identical to that judge's manifest, in manifest order (`check_attachments.out`).
  Every tile a verdict cites is on that judge's manifest.
- **Every tile was checked against its shot.** All 328 tiles compared pixel-for-pixel with
  their region of the source shot: 0 differ (`verify_tiles.out`).
- **Two tile cuts were discarded before any judge launched**, and no judge saw them. The first
  held the shot in Chromium's image document, which rewrote the image's size on resize, so
  every tile came out shrunk and centred on the magenta host background
  (`attempt1-tiles-bad/`). The second used a plain host page, and one tile
  (`1680px-dark-sw-full-r02of09-c3of3`) came out with an unpainted magenta block from a
  compositor race (`attempt2-tile-race/`). The third cut waits for paint and is the one
  judged. The magenta in both is the operator's host page, not the dashboard.
- **The verdict line carries an ANCHORS suffix**, as in the WI-920 and WI-831 records, which
  is how the machine line "cites numbered anchors" (TC-055 Method).
- **The tile count is the same as WI-920's** (328), by the same rule: an even split, at most
  1500 px on each side.
- **The WI-920 briefs are not in `review-tmp/`**, so these briefs were built from that
  record's description. What they add to the description: the A4 paragraph, the tile-reading
  notes, the MAJOR and MINOR glosses, the `VERDICT: NONE` line and a fixed final-message shape.
- **The lane has no `.venv`**, so `shoot.mjs` would fall back to `python` on PATH. The primary
  checkout's `.venv/Scripts` was put first on PATH for the shoot, and its regenerate reported
  `already up to date`.
- **The lane was left as found.** `PROJECT_STATE.html` was restored (sha256 `eff0c0e83fde…`
  matches the copy taken first), `scripts/dashboard-shots/shots/` was deleted after copying,
  and the three `__pycache__` folders the regenerate created were removed. `git status` is
  clean. The `node_modules` junction stays.

## Verdict

All six judges approved, with every live anchor passing at every width and theme, and every
verdict cites only anchors the rubric lists live, so by TC-055's Expected the compiled outcome
is APPROVE. Not recorded; the coordinator records it.

VERDICT: APPROVE findings=0 — ANCHORS: T2=pass T4=pass T5=pass T8=pass
