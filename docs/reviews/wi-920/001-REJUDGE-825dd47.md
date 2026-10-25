# WI-920: TC-055 re-judged (cross-family critique) at 825dd47de

**Why now:** TC-055's declared trigger, `component:CMP-009`, fired after its work-item floor
at merge `b803dd0` (inputs digest `sha256:5bdf43dafa30…`; full digest
`sha256:5bdf43dafa301850c36ca3d73bb69abea194c283c6004ea66dd2e2ce80a36d73`, from the spec at
`docs/work/active/wi-920/`). The latest result on record was
`TC-055.2026-10-11T012305Z.toml` (pass).

**Judges:** six independent Codex Luna (`gpt-6-luna`, high effort, codex-cli 0.162.1,
read-only sandbox) sessions, one per width and theme: 390, 1280 and 1680 px, light and dark.
The dashboard code is Claude-authored, so the judges are cross-family (TC-055's Method). A
Claude agent rendered, tiled, launched and compiled; it judged nothing. Each session's header
confirms `model: gpt-6-luna`, `sandbox: read-only`, `reasoning effort: high`, workdir the lane
root.

**Rendered:** lane `wi-920` at HEAD `825dd47de`. `PROJECT_STATE.html` was regenerated with
`gen_trajectory.py` first; the only difference from the committed file is the as-of stamp
(`f8d02acb7` -> `825dd47de`). The declared `shoot.mjs` matrix (device scale 2) exited 0 and
printed:

```
gen_trajectory: already up to date -> PROJECT_STATE.html
declared tab(s) not in this dashboard, SKIPPED: know (Knowledge (OKF))
shooting 5 tab(s): arch, dag, sw, process, retired

wrote 36 screenshot(s) to C:\Projects\ai-template.wt\wi-920\scripts\dashboard-shots\shots
```

(followed by the 36 shot paths). No rendered tab was reported `NOT shot`, so the skill's
step-2 stop rule did not apply. Five tabs were shot: What, When, How, Process and Retired.
Knowledge is absent because its dial is off.

Each judge received:
- the rubric verbatim, read from the lane at HEAD, which states the live anchors T2, T4, T5
  and T8, each with only the residue the rubric leaves to the judge;
- SN-023 and SN-024 (need and acceptance), SR-054's requirement and acceptance, LLR-055's
  detail, and TC-055's method and expected, quoted from the registries at HEAD;
- the scope lines of the test-bound rows (skill step 4), quoted from the registries at HEAD
  with their TC ids: LLR-099/TC-102 (T2), LLR-119/TC-124 (T4), LLR-105/TC-108 and
  LLR-285/TC-296 (T5), and LLR-120/TC-125 and LLR-292/TC-305 (T8). Each was the row's
  `SCOPE` statement, from `SCOPE` to the end of `detail`. LLR-292 carries no `SCOPE`, so it
  was quoted as its whole `detail`. The rubric's header binds no other row;
- a statement that the run shot the complete declared matrix, split one width x theme cell
  per judge, and that T5 is judged in the judge's own theme and compiled across all six;
- its width and theme of the matrix, cut into native-resolution tiles of at most
  1500 x 1500 px (Playwright/Chromium canvas crops of the device-scale-2 shots). The tiles
  were attached through `codex exec -i` with an ordered manifest: landing fold, then What,
  When, How, Process and Retired. There were 328 tiles: 44 per 390 px judge, 48 per 1280 px
  judge and 72 per 1680 px judge.

Judges were told to judge only the live anchors, each only on the clause the rubric leaves to
them; to cite only live anchor ids; to route a clause a test holds as a test gap, never as a
finding or a verdict; to grade each finding MAJOR or MINOR; to record no verdict if they could
not read the rubric or all their tiles; and not to open `docs/reviews/`, `docs/log*`,
`docs/test/observations/`, `docs/work/`, `docs/status.md` or `OWNER_SCRATCHPAD.md`. Because
the sandbox is read-only, each judge's final message was written to
`verdict-<width>-<theme>.md` by the CLI's `-o` flag. None saw earlier verdicts or the
implementers' self-assessment.

**No judge read any repo file.** Every shell command a judge attempted failed in the Codex
sandbox with `Failed to create unified exec process: helper_unknown_error: setup refresh had
errors` (exit -1 in 0 ms). Five judges attempted reads, of `CLAUDE.md`,
`docs/rubrics/dashboard-usability.md` and `PROJECT_STATE.html`, plus
`.agents/skills/antidote/SKILL.md` (390 dark) and `Get-Location` (390 light). The 1680 dark
judge attempted none. No attempted path was a forbidden one. Each judge then judged from its
brief, which carries the rubric verbatim, and its attached tiles. No judge reported a rubric
or a tile it could not read.

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

- [PASS] **T2** (reads legibly at default density) at all six. 1680 dark: "The What view
  opens as a readable spine of individual SN blocks, and the When view groups the roadmap
  into phase blocks. The How and Process views also present their maps in distinct sections,
  rather than opening as an undifferentiated wall of nodes." (`1680px-dark-arch-full-r02of03-c1of3`,
  `1680px-dark-dag-full-r03of03-c1of3`, among others). 1280 light: "the When view opens as a
  tiered roadmap rather than a wall of work-item nodes." (`1280px-light-dag-full-r02of03-c1of2`).
- [PASS] **T4** (truncation is actionable) at all six. 1280 dark: "The shortened spine-node
  text has a clear reveal path: the What-view instructions say to click a block to read its
  full text. I found no other truncation without an actionable way to reveal the rest."
  (`1280px-dark-arch-full-r02of03-c1of2`, `-r03of03-c1of2`). 390 dark: "The next-work card
  shows whole titles." (`390px-dark-arch-full-r04of05`, `-r05of05`, `390px-dark-sw-full-r19of20`).
- [PASS] **T5** (controls not painted over a node fill, own theme) at all six, three per
  theme. 390 dark: "The active tab is distinguished by a clear violet label and underline;
  the other tab labels remain legible." 1280 light: "In the light theme, the active tab text
  and underline are distinct from the inactive tabs and page background."
  (`1280px-light-arch-full-r02of03-c1of2`, `1280px-light-dag-full-r02of03-c1of2`,
  `1280px-light-process-full-r02of04-c1of2`).
- [PASS] **T8** (crossings minimized, unavoidable ones in open space) at all six. 1680 dark:
  "The When roadmap has dense paths, but the crossings I can see are in the space between
  blocks rather than under labels or port clusters." (`1680px-dark-dag-full-r03of03-c1of3`,
  `1680px-dark-sw-full-r09of09-c1of3`, `1680px-dark-process-full-r03of04-c2of3`).

## Findings, verbatim

None. Every judge wrote `findings=0` and "Test gaps: None".

## Non-anchor observations (not counted)

The 390 light judge's T4 paragraph also says: "The sideways-scroll instructions make the
clipped table and diagram content actionable." The rubric binds viewport fit to T7/TC-121.

## Operator's note (facts for confirm-or-refute; no judge is overridden)

- **No anchor failed**, so there is no FAIL for these notes to check against source.
- **Judges ran fast and without tool access.** Each session finished 29 to 43 s after
  launch (all six launched together at 09:17:24Z), with between 74,049 tokens (390 dark) and
  150,544 tokens (1680 light). Every in-sandbox shell command failed, so no judge
  cross-checked a tile against `PROJECT_STATE.html` the way the WI-831 judges did. The
  briefs offered that read as optional. The cause looks like the Codex Windows sandbox
  helper (`setup refresh had errors`), perhaps raced by six parallel sessions. That is not
  confirmed.
- **The verdict line carries an ANCHORS suffix.** As in the WI-831 record, judges were asked
  to end with `VERDICT: APPROVE|CHANGES-REQUESTED findings=N ANCHORS: T2=… T4=… T5=… T8=…`.
  The suffix is how the machine line "cites numbered anchors" (TC-055 Method).
- **The tile count differs from WI-831** (328 here, 314 there) because the page is taller
  now. The tiling rule is the same: an even split, at most 1500 px on each side.
- **An earlier attempt of this run** stopped at the shoot step on a missing Playwright
  install. It produced no tiles, briefs or verdicts, and it is kept apart (`rj920/attempt1/`).

## Verdict

All six judges approved, with every live anchor passing at every width and theme, so the
compiled outcome is APPROVE. Not recorded; the coordinator records it.

VERDICT: APPROVE findings=0 — ANCHORS: T2=pass T4=pass T5=pass T8=pass
