# 123-CRITIQUE — dashboard usability (SR-054), fresh render after the WI-318/319/320 batch

**Trigger:** WI-318 and WI-319 both change `gen_trajectory.py`, re-dating the
perceptual evidence past [`121-CRITIQUE.md`](121-CRITIQUE.md). This is the **one**
critique the batching constraint calls for: dispatched once, against the last
render commit, after the whole batch landed — never per train
(wrap-up-plan.md §4 + §7).

**Critic:** a fresh **OpenAI/`codex`** session — a genuinely
**family-heterogeneous** dispatch (the builder was Claude/Anthropic), the
stronger corroboration path SR-084/SR-085 prefer. Routed by **provider**, the
2026-07-24 lesson; `codex` answered immediately. Dispatched into an isolated
sandbox holding only the artifact, the rubric, the SN/SR intent brief, the render
recipe, and the 36 PNGs — no build transcript, no self-assessment, no repo
access, and no writable path into this repo.

**Artifact:** `PROJECT_STATE.html` as generated at `33aa41c`, and the full
36-shot matrix from `scripts/dashboard-shots/shoot.mjs` — {390, 1280, 1680}px ×
{light, dark} × the five tabs, full-page plus the landing fold.

**Scope given:** the **live** anchors only — **T2, T4, T5, T8** — and, new since
121, the two clauses that left T4 and the one that left T8 for a test this
session (`LLR-119`/`TC-124`, `LLR-120`/`TC-125`). The critic honored all of it,
listing each test-bound clause under "out of scope" rather than counting it.

**Disposition — read this before filing anything.** The single finding is **not a
new work item**: it is [WI-323](../requirements/work-items.csv), filed earlier
the same day when WI-320 deliberately split T8's perceptual clause off from its
objective floor. An independent critic reaching the same finding, from pixels,
with no access to that reasoning, is **corroboration of the split** — so it is
recorded against the existing row rather than duplicated into a new one. Nothing
here is new work that was not already queued.

**What this verdict does and does not do to the gate.** `perceptual-stale`
requires a critique that *post-dates* the render change, not an APPROVE, so the
gate clears with this file committed. The CHANGES-REQUESTED verdict does arm the
warn-first critique-loop ratchet (WI-068) on a future WI-close that touches
`SR-054` without touching the TC registry, the tests dir, or a rubric — which is
correct: WI-323 must land with validation, not just with pixels.

---

## Verdict

VERDICT: CHANGES-REQUESTED findings=1

## Per-anchor judgement

### T2 — PASS
Shots read: 1280px-light-arch-full.png, 1280px-light-dag-full.png, 1280px-light-sw-full.png, 1280px-light-know-full.png, 1280px-light-process-full.png, 390px-dark-arch-full.png, 390px-dark-sw-full.png, 390px-dark-process-full.png

Views open at summarized levels: needs, phases, components, concept types, and lifecycle stages. Large subordinate collections are not exploded into walls of nodes.

### T4 — PASS
Shots read: 390px-dark-arch-full.png, 390px-dark-sw-full.png, 390px-light-know-full.png, 390px-dark-process-full.png, 1280px-light-arch-full.png, 1280px-light-sw-full.png

Default labels remain readable without collisions. Ellipsized diagram labels have actionable disclosure: the surrounding instructions explicitly direct readers to click nodes for full text or follow stage links. Narrow diagrams also provide a visible sideways-scroll cue.

### T5 — PASS
Shots read: 390px-light-arch-fold.png, 390px-dark-arch-fold.png, 1280px-light-arch-fold.png, 1280px-dark-arch-fold.png, 1280px-light-dag-full.png, 1280px-dark-dag-full.png, 390px-dark-sw-full.png, 390px-dark-process-full.png

Tabs, active underlines, links, ports, and expand/descend marks remain distinguishable in both themes. The rendered control colors correspond to contrast ratios of at least 4.55:1 for muted controls and 5.98:1 for accent controls against their relevant surfaces.

### T8 — FAIL
Shots read: 390px-light-dag-full.png, 1280px-light-dag-full.png, 1280px-dark-dag-full.png, 1680px-light-dag-full.png, 1280px-light-sw-full.png, 1280px-light-know-full.png, 1280px-light-process-full.png, 390px-dark-process-full.png

The How-SW, Knowledge, What, and Process diagrams have followable routing. The When roadmap does not: numerous dependencies share narrow horizontal lanes and cross within the central nodes’ port fans.

## Findings

### [MAJOR] T8 — Roadmap dependency routes collapse into ambiguous port fans
In 1680px-light-dag-full.png, the long routes spanning phases 2, 3, unphased, and 1 are stacked into the same narrow lanes, then intersect curved arrivals and departures immediately beside the phase ports. The congestion is especially pronounced around phase 2 and the unphased node. The same ambiguity persists in 1280px-light-dag-full.png, 1280px-dark-dag-full.png, and 390px-light-dag-full.png, preventing a reader from reliably attributing individual routes.

The fix must allocate distinguishable lanes or ports with sufficient separation, minimize crossings, and move any unavoidable crossing into open space away from port clusters.

## Out of scope

- T1, T3, T6, and T7 are test-bound or retired under the rubric and were not adjudicated.
- T4’s ink-inside-box and next-work-card truncation clauses, and T8’s edge-through-unrelated-node clause, are test-bound and were not used as findings.
- The shot matrix does not capture an actively keyboard-focused control, so focus-ring appearance was not directly exercised.
- Apparent sticky-header overlap in full-page mobile captures was not filed: the corresponding fold shots show the normal viewport without that overlap.

---

## What the two T4 fixes bought, measured against 121

121-CRITIQUE failed T4 twice — clipped architecture node descriptions (MAJOR) and
a next-work title truncated with no reveal (MINOR). **T4 now passes**, and the
critic's own reasoning names the affordance argument the fix rests on: an
ellipsis is acceptable *because* the reader is told, visibly, how to reach the
rest. Both are also now under `TC-124`, so the anchor cannot silently regress to
the same two defects.

**Three anchors of four pass, and the one that fails was already on the board.**
That is the batched-attended route working as designed: land the batch, dispatch
once, and let the critique tell you whether the queue you already hold is the
right queue. This round it said yes.
