# 005-REVIEW-A — 9b85f03 (composed WI-273 + WI-293)

**Reviewer:** `OPENAI-TERRA` (`gpt-5.6-terra`, OPENAI family) — the declared
cross-family review leg, dispatched by hand through the `codex` CLI after the
OpenCode-Go gateway stopped responding mid-session. The builder was `opus`
(Anthropic), so this is a genuine cross-family review. Brief built to
`docs/rubrics/code-review-adversarial.md` (R1-R5) with **no build transcript and
no implementer self-assessment**, in a disposable worktree where it could drive
the real code.

**Scope:** the composed tree `9b85f03` — train `3-g3-WI-273-b45e` merged onto the
WI-293 baseline. Supersedes `003-REVIEW-A-912356b`, which judged a stale head.

**What makes this an R2 review rather than a plausibility read:** the reviewer
wrote a live keyboard probe and drove the emitted dashboard through click,
Left/Right wraparound, Up/Down, Home/End, Space and Enter, asserting the state
invariants on every transition; generated a SECOND artifact (physical-CMP) to
exercise the dynamically-added tabs rather than only the two always-present ones;
shot the declared 36-cell matrix; and checked whether the document's duplicate
SVG-marker IDs were introduced here (they are pre-existing versus `662bc87` and
do not involve tab/panel IDs).

**Bottom line — the code half is sound; the block is the whole-document gate.**
Every worst-class hunt survived and the full suite passed at 1479. The single
finding is the same *process* gap `003-REVIEW-A` raised: SR-052's mandatory fresh
family-heterogeneous critique has not returned APPROVE. That critique has since
run ([004-CRITIQUE-9b85f03](004-CRITIQUE-9b85f03.md), `OPENAI-SOL`) and returned
CHANGES-REQUESTED on **A2** and **A4-boundaries** — two pre-existing
whole-document defects that neither WI-273 nor WI-293 touches. So this verdict's
stated condition is now resolved, and resolved *against* integration.

---

WI-273 changes the dashboard generator’s tab emission and controller for every generated `PROJECT_STATE.html`, including optional panels. Its SR-052 obligation is ARIA-operable tabs within the broader rubric-adjudicated accessibility requirement.

R3 worst-class hunt:

- State divergence: drove the emitted dashboard through click, Left/Right wraparound, Up/Down, Home/End, Space, and Enter. Each transition kept exactly one selected/active tab, one visible active panel, and the selected tab as the sole `tabindex=0` stop.
- Keyboard boundary/focus failure: both ends wrapped correctly and moved focus to the activated tab.
- Broken dynamic ARIA wiring: the current five-panel artifact has unique tab/panel IDs and one resolving `aria-controls`/`aria-labelledby` pair each. A separately generated physical-CMP artifact also activated and synchronized correctly. The document’s duplicate SVG-marker IDs are pre-existing versus `662bc87` and do not involve tab/panel IDs.
- Render regression: generated and inspected the declared 36-cell width/theme/tab screenshot matrix; no tab rendering or readability defect was observed. `gen_trajectory.py --check` passed.
- Regression suite: scoped tab tests passed (5), and full suite passed: `1479 passed, 7 skipped` in 319.05s.

R4 Done-when coverage map:

| Requirement clause | Coverage |
|---|---|
| Tabs expose selected state, panel relationship, and keyboard navigation | Covered by live Playwright interaction sequences and five scoped generator tests. |
| Dynamically generated tabs retain the pattern | Covered by current optional tabs, generated physical-CMP probe, and `test_every_tab_controls_a_labelled_panel`. |
| Every interactive element is keyboard-reachable and named | UNCOVERED for the current full artifact by the required fresh independent rubric critique. |
| Status/phase/type information is not color-only | UNCOVERED by the required fresh independent rubric critique. |
| Text contrast meets the declared floor | UNCOVERED by the required fresh independent rubric critique. |
| Fresh family-heterogeneous accessibility critique approves the current generated artifact | UNCOVERED; pending parallel dispatch. |

R5 re-drive: the prior process finding is not consumed. `check_trajectory.py --root . --strict` still reports `perceptual-stale SR-052;SR-053;SR-054`; no fresh `docs/reviews/*-CRITIQUE.md` exists for this changed render. The code half survived its new-seam probes, but this verdict remains conditional on—and blocked by—the pending critique’s APPROVE outcome.

- [MAJOR] docs/requirements/system-requirements.csv:53 -> SR-052’s mandatory fresh family-heterogeneous critique is still absent; strict trajectory verification reports the current dashboard perceptual-stale -> complete and record a fresh non-Anthropic `docs/reviews/*-CRITIQUE.md` APPROVE against `docs/rubrics/dashboard-accessibility.md` for this generated artifact -> @owner
VERDICT: CHANGES-REQUESTED findings=1
