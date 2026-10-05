# WI-796: TC-055 re-judged (cross-family critique) at 5fb0fc74

**Why now:** TC-055's declared trigger, `component:CMP-009`, fired after its work-item floor
at merge `2e7cd53` (inputs digest `sha256:463ba32184eb…`).

**Judges:** six independent Codex Luna (`gpt-6-luna`, high effort, codex-cli 0.160.0,
read-only sandbox) sessions, one per width and theme: 390, 1280 and 1680 px, light and dark.
The dashboard code is Claude-authored, so the judges are cross-family (TC-055's Method).
A Claude agent rendered, tiled, launched and compiled; it judged nothing.

**Rendered:** lane `wi-796` at HEAD `5fb0fc74`. `PROJECT_STATE.html` was regenerated with
`gen_trajectory.py` first; the only difference from the committed file is the as-of stamp
(`797a873c` -> `5fb0fc74`). The declared `shoot.mjs` matrix (device scale 2) shot four tabs:
What, When, How and Process. The script reported that Knowledge was absent (its dial is off)
and that a rendered `retired` tab is not in the declared matrix, so it was not shot.

Each judge received:
- the rubric verbatim, which states the live anchors T2, T4, T5 and T8 (crossing legibility
  only);
- SR-054's requirement and acceptance, SN-023 and SN-024, LLR-055's detail, and TC-055's
  method and expected;
- its width and theme of the matrix, cut into native-resolution tiles of at most
  1500 x 1500 px and attached through `codex exec -i` with an ordered manifest. There were
  284 tiles: 37 per 390 px judge, 42 per 1280 px judge and 63 per 1680 px judge.

Judges were told not to open `docs/reviews/`, `docs/log*`, `docs/test/observations/`,
`docs/work/` or `docs/status.md`. None saw earlier verdicts or the implementers'
self-assessment. They could read the generated `PROJECT_STATE.html`.

## Per judge

| Judge | T2 | T4 | T5 | T8 | Verdict line |
|---|---|---|---|---|---|
| 390 light | pass | pass | **FAIL** | pass | `VERDICT: CHANGES-REQUESTED findings=1 ANCHORS: T2=pass T4=pass T5=fail T8=pass` |
| 390 dark | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 1280 light | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 1280 dark | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 1680 light | pass | pass | pass | pass | `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass` |
| 1680 dark | **FAIL** | pass | pass | pass | `VERDICT: CHANGES-REQUESTED findings=1 ANCHORS: T2=fail T4=pass T5=pass T8=pass` |

## Per anchor

- [FAIL] **T2** at 1680 px dark; it passed at the other five. The 1680-dark judge:
  "The What view opens with a root layer of 31 SN blocks; the screenshot shows a
  scrollable stack of individual nodes rather than a collapsed summary for a view with
  more than three items. The When view does show a tiered roadmap, and the How view
  starts at four components." The other five judges each found every view opening grouped
  or bounded. For example, 1280 light: "The What view opens at the SN layer, the When view
  shows grouped phase blocks, and the How view opens at its component level".
- [PASS] **T4** at all six. Shortened labels carry a stated click or descend reveal, and
  wide tables carry a sideways-scroll cue. 390 light: "I see no actionable truncation: the
  shortened diagram labels have a visible instruction to click for full text, and the
  clipped table content is accompanied by a sideways-scroll cue."
- [FAIL] **T5** at 390 px light; it passed at the other five. The 390-light judge: "The
  light theme's tab text and active underline are legible ... However, focused diagram
  nodes use the orange `--ring` fallback (`#f59e0b`) against light surfaces; that focus
  indicator does not meet the rubric's body-text contrast floor. The initial screenshots do
  not capture focus states; I confirmed the focus styling in `PROJECT_STATE.html`." The
  other judges passed the controls shown and said focus states are not in the shot set.
- [PASS] **T8** (crossing legibility only) at all six. Visible crossings sit in open space,
  with none under a label or inside a port cluster, in the What, When, How and Process
  diagrams.

## Findings (CHANGES-REQUESTED), verbatim

1. **390 px light, MAJOR, T5:** "Keyboard focus on diagram nodes is indicated by an orange
   stroke with insufficient contrast against light surfaces. A reviewer navigating by
   keyboard may have trouble seeing which node is focused." Tiles cited: 5, 10, 15, 17
   and 29 (`390px-light-arch-full-r03of05`, `390px-light-dag-full-r03of05`,
   `390px-light-sw-full-r03of18`, `-r05of18` and `-r17of18`).
2. **1680 px dark, MAJOR, T2:** "The What tab presents 31 SN blocks in its initial root
   layer. A reviewer opening it sees a long list to scan and scroll rather than a collapsed
   summary." Tiles cited: 10 and 13 (`1680px-dark-arch-full-r02of03-c1of3`, `-r03of03-c1of3`).

## Non-anchor observations (not counted)

All judges saw the sticky header mid-page in some full-page tiles. The fold shots show it
in place, so it is a capture artifact. The 390 px How tables extend past the viewport,
with sideways-scroll cues; the rubric binds that to T7/TC-121.

## Coordinator's note (facts for confirm-or-refute; no judge is overridden)

- **Finding 1 rests on source, not pixels.** Focus states are not in the shot set. The rule
  the judge cited is real: `gen_trajectory.py:551` `#ice .cell.hl rect
  { stroke:var(--ring,#f59e0b) }`, and `:559` for `#dag .wi.hl`, where focus adds `.hl`
  (`:724`, `:752`). In this render, however, every one of the 711 `.cell` nodes stamps an
  inline `--ring` (`#ffffff` or `#0f172a`), so the amber fallback is not what a focused
  icicle cell shows. Drill `.block` focus falls back to `var(--accent)`, not amber. Whether
  the stamped rings clear the floor is T5's test-bound core, `LLR-105`/`TC-108`.
- **Finding 2 concerns the root tier.** The What view opens at the SN tier with its SRs
  collapsed below it. The judge counted 31 SN blocks there and read SR-089's `>3` rule as
  requiring the root itself to collapse; the other five judges did not. LLR-055 says T2's
  start-collapse core has left for `LLR-099`/`TC-102`, while the rubric still lists T2 as
  live. Which of those governs is a ruling, not a verdict.
- **Discarded first attempt.** The first 390 px runs got image paths ending in a carriage
  return (CRLF tile lists), so no tiles attached. They were stopped before any verdict and
  rerun with clean paths; only the reruns are compiled here.

## Verdict

Two of six judges requested changes on live anchors, so the compiled outcome is
CHANGES-REQUESTED. Not recorded; the coordinator records it.

VERDICT: CHANGES-REQUESTED findings=2 — ANCHORS: T2=fail T4=pass T5=fail T8=pass
