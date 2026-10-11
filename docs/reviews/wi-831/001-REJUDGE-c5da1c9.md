# WI-831: TC-055 re-judged (cross-family critique) at c5da1c94

**Why now:** TC-055's declared trigger, `component:CMP-009`, fired after its work-item floor
at merge `a8458c2` (inputs digest `sha256:463ba32184eb…`).

**Judges:** six independent Codex Luna (`gpt-6-luna`, high effort, codex-cli
0.162.0-alpha.17.2, read-only sandbox) sessions, one per width and theme: 390, 1280 and
1680 px, light and dark. The dashboard code is Claude-authored, so the judges are
cross-family (TC-055's Method). A Claude agent rendered, tiled, launched and compiled; it
judged nothing.

**Rendered:** lane `wi-831` at HEAD `c5da1c94`. `PROJECT_STATE.html` was regenerated with
`gen_trajectory.py` first; the only difference from the committed file is the as-of stamp
(`4e47130a7` -> `c5da1c943`). The declared `shoot.mjs` matrix (device scale 2) exited 0 and
printed:

```
gen_trajectory: already up to date -> PROJECT_STATE.html
declared tab(s) not in this dashboard, SKIPPED: know (Knowledge (OKF))
shooting 5 tab(s): arch, dag, sw, process, retired

wrote 36 screenshot(s) to C:\Projects\ai-template.wt\wi-831\scripts\dashboard-shots\shots
```

No rendered tab was reported `NOT shot`, so the skill's step-2 stop rule did not apply. Five
tabs were shot: What, When, How, Process and Retired. Knowledge is absent because its dial is
off.

Each judge received:
- the rubric verbatim, which states the live anchors T2, T4, T5 and T8, each with only the
  residue the rubric leaves to the judge;
- SR-054's requirement and acceptance, SN-023 and SN-024 (need and acceptance), LLR-055's
  detail, and TC-055's method and expected, quoted from the registries at HEAD;
- the scope lines of the test-bound rows (skill step 4), quoted from the registries at HEAD
  with their TC ids: LLR-099/TC-102 (T2), LLR-119/TC-124 (T4), LLR-105/TC-108 and
  LLR-285/TC-296 (T5), and LLR-120/TC-125 and LLR-292/TC-305 (T8). Each was the row's
  `SCOPE` statement, from `SCOPE` to the end of `detail`. LLR-292 carries no `SCOPE`, so it
  was quoted as its whole `detail`;
- a statement that the run shot the complete declared matrix, split one width x theme cell
  per judge, and that T5 is judged in the judge's own theme and compiled across all six;
- its width and theme of the matrix, cut into native-resolution tiles of at most
  1500 x 1500 px. The tiles were attached through `codex exec -i` with an ordered manifest:
  landing fold, then What, When, How, Process and Retired. There were 314 tiles: 42 per
  390 px judge, 46 per 1280 px judge and 69 per 1680 px judge.

Judges were told to judge only the live anchors, each only on the clause the rubric leaves to
them. They were told to route a clause a test holds as a test gap, never as a fail, and not
to open `docs/reviews/`, `docs/log*`, `docs/test/observations/`, `docs/work/` or
`docs/status.md`. Their session logs show none did. All six read `PROJECT_STATE.html`, five
also read `CLAUDE.md` (all but 390 dark), and two (1280 light, 1680 dark) also read
`.agents/skills/render-dashboard-critique/SKILL.md`. None saw earlier verdicts or the
implementers' self-assessment.

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

- [PASS] **T2** (reads legibly at default density) at all six. 1680 light: "The What view
  opens as a readable stack of SN blocks, with labels that remain legible. The When roadmap
  groups work into spaced phase blocks; its visible density is high, but it does not read as
  a wall of nodes." (`1680px-light-arch-full-r03of03-c1of3`,
  `1680px-light-dag-full-r03of03-c1of3`). 390 dark: "These views are dense, but their
  default presentation reads as structured content rather than a wall of overlapping nodes."
- [PASS] **T4** (truncation is actionable) at all six. 390 light: "Truncated node summaries
  have a visible “click a block to read its full text” instruction. Clipped wide content is
  signaled with sideways-scroll cues, so the cuts have an action available to the reader"
  (`390px-light-arch-full-r03of04`, `390px-light-dag-full-r04of05`,
  `390px-light-sw-full-r03of19`). 1680 light: "The next-work card’s title truncation uses a
  native disclosure with a visible reveal cue." (`1680px-light-arch-fold-r02of02-c1of3`).
- [PASS] **T5** (controls not painted over a node fill, own theme) at all six, three per
  theme. 1280 dark: "the active tab text and underline are clearly distinguishable, and the
  inactive tab labels remain readable against the page background." 390 light: "the active
  tab’s purple label and underline distinguish it from the readable inactive tabs."
  (`390px-light-arch-full-r03of04`, `390px-light-sw-full-r03of19`,
  `390px-light-process-full-r03of07`, `390px-light-retired-full-r03of03`).
- [PASS] **T8** (crossings minimized, unavoidable ones in open space) at all six. 1680
  light: "The visible diagram wires are faint and busy, especially in the roadmap, but
  crossings appear in open space. I do not see a crossing beneath a label or inside a port
  fan that makes the routes unattributable." (`1680px-light-dag-full-r03of03-c1of3`,
  `-c2of3`, `1680px-light-sw-full-r08of08-c1of3`).

## Findings, verbatim

None. Every judge wrote `findings=0`, and no judge raised a test gap.

## Non-anchor observations (not counted)

The 390 light judge saw the sticky header mid-page in full-page tiles: "The mid-page sticky
header in the full-page captures is consistent with the landing viewport header shown in
`390px-light-arch-fold-r01of02`." That makes it a capture artifact. The same judge noted
"sideways-scroll cues where maps exceed the viewport" under T2 and T4. The rubric binds
viewport fit to T7/TC-121.

## Coordinator's note (facts for confirm-or-refute; no judge is overridden)

- **No anchor failed**, so there is no FAIL for these notes to check against source.
- **Discarded first attempt.** The first 390 px pair ran on a brief that lacked the "matrix
  and your share" statement. The 390 light judge recorded no verdict. It read "one cell of
  the render matrix" as the incomplete matrix TC-055's Method forbids judging, and said T5
  "cannot be determined" from one theme. The 390 dark judge approved. The section was added
  to all six briefs, and both 390 px judges were rerun so all six judged the same text. Only
  the reruns are compiled here. The discarded outputs and their brief are kept beside the
  tiles (`review-tmp/2026-10-10-leg01/wi831/discarded-attempt1/`).
- **The matrix differs from the previous re-judge.** The Retired tab is now in the declared
  `TABS`, and this run shot it at all six cells. The previous re-judge's matrix left it
  unshot.
- **The previous re-judge's findings did not recur.** That re-judge found a T5 amber focus
  ring at 390 light and a T2 31-SN What root at 1680 dark. Neither recurs in any verdict
  here. The briefs did not mention them.
- **One judge tried an unrelated path.** The 1680 dark judge's first command also tried to
  read a path under its own Codex plugin cache (`C:/Users/Peter/.codex/plugins/cache/...`).
  It touched nothing in the repo outside the paths above.

## Verdict

All six judges approved, with every live anchor passing at every width and theme, so the
compiled outcome is APPROVE. Not recorded; the coordinator records it.

VERDICT: APPROVE findings=0 — ANCHORS: T2=pass T4=pass T5=pass T8=pass
