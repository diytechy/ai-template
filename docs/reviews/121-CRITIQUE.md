# 121-CRITIQUE — dashboard usability (SR-054), fresh render after the attended render batch

**Trigger:** the render batch WI-305/306/307/315 + WI-317/314 all touch
`gen_trajectory.py`, re-dating the perceptual evidence past
[`120-CRITIQUE.md`](120-CRITIQUE.md). This is the **one** critique the batching
constraint calls for: dispatched once, against the last render commit, after
the whole batch landed — never per train (wrap-up-plan.md §4 + §7).

**Critic:** a fresh **OpenAI/`codex`** session — a genuinely
**family-heterogeneous** dispatch (the builder was Claude/Anthropic), the
stronger corroboration path SR-084/SR-085 prefer and that 120-CRITIQUE had to
degrade away from. Routed here by provider after the OpenCode-Go gateway again
returned nothing to a `kimi-k3` probe. Dispatched into an isolated sandbox
holding only the artifact, the rubric, the SN/SR intent brief, the render
recipe, and the 36 PNGs — no build transcript, no self-assessment, no repo
access, no writable path into this repo.

**Artifact:** `PROJECT_STATE.html` as generated at `ebc9b0f`, and the full
36-shot matrix from `scripts/dashboard-shots/shoot.mjs` — {390, 1280, 1680}px ×
{light, dark} × the five tabs, full-page plus the landing fold.

**Scope given:** the **live** anchors only — **T2, T4, T5, T8**. T1, T3, T6 and
T7 are each bound to a test now and were explicitly declared out of bounds; the
critic honored that, and used the "out of scope" section for what it could not
judge instead of inflating the count. It also applied the recipe's fullPage
caveat unprompted, checking an apparent sticky-header overlap against the
matching `-fold` shot and dismissing it as a capture artifact.

**Disposition:** the three findings are filed as their own work items —
**WI-318** (T4 clipped node descriptions), **WI-319** (T4 truncated next-work
title), **WI-320** (T8 roadmap edge routing). The critique loop builds the eyes;
it never edits the dashboard inline.

---

## Verdict

VERDICT: CHANGES-REQUESTED findings=3

## Per-anchor judgement

### T2 — PASS

Shots read: `1680px-light-dag-full.png`, `1280px-dark-dag-full.png`, `1680px-light-sw-full.png`, `1280px-dark-sw-full.png`, `1680px-light-know-full.png`, `1280px-dark-know-full.png`, and both `390px-*-arch-fold.png` shots.

The graph-heavy views open at summarized tiers: eight phases, five components, and six knowledge types, with member counts instead of hundreds of expanded members. The mobile landing remains a flat set of summary cards.

### T4 — FAIL

Shots read: `390px-light-arch-fold.png`, `390px-dark-arch-fold.png`, `390px-light-arch-full.png`, `1680px-light-arch-full.png`, `1680px-dark-arch-full.png`, and `1680px-light-process-full.png`.

The landing prose and summary cards are generally readable, but the Architecture decomposition clips every visible SN description across its node boundaries. The Next Work title is also truncated without a visible way to reveal it.

### T5 — PASS

Shots read: both `390px-*-arch-fold.png` shots, plus the light 1680px and dark 1280px renders of `arch`, `dag`, `sw`, `know`, and `process`.

Visible tab labels, active-tab underlines, node ports, expand/collapse marks, links, and process controls remain distinguishable in both themes. None of the captured controls washes into its background.

### T8 — FAIL

Shots read: `1680px-light-dag-full.png`, `1280px-dark-dag-full.png`, `390px-dark-dag-full.png`, `1680px-light-sw-full.png`, `1280px-dark-sw-full.png`, `1680px-light-know-full.png`, `1280px-dark-know-full.png`, `1680px-light-process-full.png`, and `1280px-dark-process-full.png`.

Knowledge and Process routing is clean, and the SW paths are individually traceable. The roadmap DAG is not: several dependencies share or cross the same horizontal corridors and converge in dense port fans, making individual source-to-target paths ambiguous.

## Findings

### [MAJOR] T4 — Architecture node descriptions are clipped

In `390px-light-arch-full.png`, the SN-001 through SN-009 descriptions begin outside the left edge of their boxes and terminate beyond the right edge. The same defect remains visible at desktop width in `1680px-light-arch-full.png` and `1680px-dark-arch-full.png`.

Fix by wrapping descriptions within each node, increasing node dimensions, or replacing the description with a deliberately constrained summary that stays inside the box.

### [MINOR] T4 — Next Work is truncated without a visible reveal affordance

In `390px-light-arch-fold.png`, `390px-dark-arch-fold.png`, and `1680px-light-arch-full.png`, the WI-308 title ends at “tiering expo…” even when ample card width is available. Nothing visible indicates how to expose the complete title.

Allow wrapping, show the full title, or add an explicit operable “view details” affordance.

### [MAJOR] T8 — Roadmap dependencies cannot be followed individually

In the Roadmap diagram of `1680px-light-dag-full.png` and `1280px-dark-dag-full.png`, multiple dependencies overlap along long horizontal rails between phases 2, 3, unphased, and 1. Several paths cross or converge around the phase-3 and unphased port fans, so a reader cannot reliably attribute each line to one source and target.

Route dependencies on distinct lanes, separate branches before port clusters, and avoid coincident segments; where crossings remain necessary, place them visibly apart in open space.

## Out of scope

- The header band appearing partway down `390px-*-arch-full.png` was not counted. The matching fold shots show the header correctly at the top, confirming the documented full-page/sticky capture artifact.
- The screenshots contain no keyboard-focused state, so activated focus-ring contrast could not be independently judged.
- Drill-down states are not captured, so routing inside drill views could not be inspected.