> **ARCHIVE** — design history as of 2026-07-20; not current guidance.

# Owner intake 2026-07-13 — six items: triage, dedupe, WIs

> **ARCHIVED 2026-07-20 — WI-251 spec-lifecycle sweep.** Spec-of-record for **WI-134, WI-135, WI-136, WI-137, WI-141, WI-142, WI-143, WI-144** (all `done`; deliverables in `docs/requirements/work-items.csv`, session records in `docs/log.md`). Absorb-verified before archiving: every durable decision has a live spine/architecture/process home (dispositions in the log, 2026-07-20 entry).

Owner-handed batch (six items), triaged against the open registry per the
change-intake flow. **Dedupe findings first** — what already exists, so no
queued work is duplicated:

| Item | Already covered? | Disposition |
|---|---|---|
| 1 (UI critiques) | **Mechanism exists, never armed**: SR-047's critique loop fires when a build touches a `Verification=Critique` SR — but the spine has **zero** Critique SRs today | Arm it: v3 Critique SRs + rubrics → [WI-134](#v3-dashboard-ux) |
| 1A (ingest/human process map) | Process tab exists (SR-050); the ingest/open-items/human loops are **not** in it | v3 scope → [WI-134](#v3-dashboard-ux) |
| 1B (columns/arrows/hover) | Not covered | v3 scope → [WI-134](#v3-dashboard-ux) |
| 1C (Simulink-style wiring, deeper nav) | **Partially**: the hierarchy shipped (WI-087/SR-051, done); the graph-DATA extensions (typed-IF contracts, cyclic render) are deferred **WI-064** | Render side is new v3 scope (soft edge to WI-064); note the ratified in-place-expand ruling below |
| 2 (live console lines) | Not covered | [WI-136](#live-console) |
| 3 (telemetry commit hygiene) | Not covered — and observed live this session (the dangling session-021 telemetry commit `f4b8a9f`) | [WI-137](#telemetry-hygiene) |
| 4 (hats for SRs) | **Answered by existing design** — see [the hats answer](#the-hats-answer) | Folds into WI-134 (arming), no new mechanism |
| 5 (TRIP research emphasis) | Plan/implement/release, multi-LLM review, ARCHI.md-style memory: all covered (PLAN/BUILD/gates, REVIEW-A/B, architecture.md+OKF). The **research track** is the real gap | [WI-138](#research-knowledge) |
| 6 (durable module specs) | Not covered; converges with 5 on "a durable knowledge home" | [WI-138](#research-knowledge) |

## v3 dashboard-ux

**The `dashboard-ux` phase (v3)** — the graphics iteration the owner
anticipated at the 2026-07-13 ratification ("amendments arrive as future WIs,
not blockers"). Two archetype batches are filed now (WI-134 `[v3]-[g1]`
structuring, WI-135 `[v3]-[g2]` decomposition); the dev slices are defined *by*
the g2 batch, not pre-filed. Requirement inputs the g1 batch must structure:

- **Critique arming (items 1 + 4):** accessibility, UI uniformity, and
  usability become `Verification=Critique` SRs with rubrics
  (`docs/rubrics/`) — the first Critique rows in the spine, so SR-047's
  critique loop finally fires on dashboard-touching builds.
- **Ingest/human process map (1A):** the Process tab gains the two circular
  flows — (A) agent intake → new items become WIs with spec detail → the
  resume loop → merge; (B) open-items population (incl. the gate-ratification
  table) → human review/feedback → merge — with the LLM_Agent entry point
  shared by both.
- **Decomposition render (1B):** narrower columns; a horizontal parent→child
  arrow per containment edge; hover highlight **persists on the last-hovered
  item** (kill the flash-on-exit).
- **Interface-wired diagrams (1C):** How-SW + trajectory views render
  Simulink-style — interfaces connect to block inputs/outputs; crisp visuals;
  **double-click descends a layer**. *Honesty note:* deeper-layer navigation
  amends the ratified in-place-expand/no-zoom ruling (OI-1, 2026-07-13) — the
  amendment is sanctioned by the owner's ratification note, and the g1 batch
  should draft it as an explicit SR-051 rev (the reopen flow: the phase revs,
  the derived gate for it drops until re-verified). Data-side graph extensions
  stay **WI-064** (soft edge).

## The hats answer

Item 4 asked how the resume chain knows to wear a UI hat. The mechanism
already exists end-to-end: a WI's `SR-Refs` names the SRs it delivers; when a
committing build's scope touches a `Verification=Critique` SR, the coordinator
schedules a fresh provider-heterogeneous CRITIQUE session that receives **the
rubric + SN/SR intent + the artifact recipe** (never the implementer's
self-assessment) — that rubric *is* the hat. No per-SR agent allocation is
needed; the missing piece was only that no SR declares `Critique` yet
(WI-134 fixes that for the dashboard). Test-hat routing needs nothing: TCs
bind to SRs by construction.

## live-console

**WI-136 — per-workstream live status line for `agent-resume`.** Instead of a
rolling scroll, each lane/workstream owns one console line that updates in
place (ANSI cursor-up rewrite). Constraints discovered up front: TTY-only
(fall back to today's scrolling when `stdout` isn't a TTY — CI logs must stay
append-only); stdlib-only (raw ANSI, no curses dependency on Windows —
`colorama`-free; modern Windows terminals accept VT sequences once enabled);
the echoed session lines (`echo_session_line`) keep their verbatim log copy.
Off-spine, opt-in (`--live-status` or a declared file), never-breaking.

## telemetry-hygiene

**WI-137 — session telemetry commits with its content + WI-keyed labels.**
Observed defect-shape: the coordinator writes `docs/iteration/<n>-*.log` +
the `iteration_index.md` row *after* the session's own commit, so the
telemetry rides the **next** commit (or dangles — session 021, committed as
housekeeping `f4b8a9f`). Fix direction: the loop commits its own bookkeeping
immediately after writing it (a one-file `telemetry:` commit; honors the
hooks). Second half (owner question): carry the WI key — recommendation is a
`wi:` header line in the session log + a `WI` column in `iteration_index.md`
sourced from `docs/next-wi` at session start (filenames keep their stable
session-number scheme; renaming files breaks the index's relative links and
the WI is a *claim* the session may change mid-run, so a header records it
more honestly than a filename). Review verdict files already commit
themselves (the reviewer prompt mandates it); the WI key column covers their
tracking too.

## research-knowledge

**WI-138 — the research track + the durable knowledge/module-spec layer
(design WI; spec-first).** Items 5 and 6 are one design problem:

- **From TRIP** (evaluated 2026-07-13): plan/implement/release, multi-LLM
  review, and ARCHI.md-style persistent memory are already covered here
  (PLAN/BUILD/gates; REVIEW-A/B cross-family; `architecture.md` + the OKF
  bundle — generated and freshness-gated, stronger than a hand-curated
  ARCHI.md). The genuine gap TRIP exposes: a **first-class research task**
  ("investigation at a defined compute level, producing documented findings,
  not code") with a grounded-second-opinion step.
- **The storage gap (item 6, and the owner's "where are the knowledge kits"):**
  `docs/okf/` is **generated from the registries** — never a parallel source
  of truth — so research findings and durable module expectations have **no
  hand-owned home today**. Per-WI `docs/specs/` archive at close by design;
  using them as module memory duplicates analysis across WI iterations
  (the owner's exact concern).
- **Design questions the WI must answer (not pre-decided here):** the durable
  home's shape (per-component spec chunks under `docs/specs/components/`?
  a `docs/knowledge/` findings dir OKF exports alongside registry pages?);
  when research runs (at PLAN before WI creation, at WI ingest, or both —
  TRIP treats it as an optional track, which fits the proportionality
  doctrine); who runs it (mid-tier agents per the owner's instinct); and the
  anti-duplication rule tying module chunks to LLRs/architecture so the new
  layer doesn't compete with the spine.

Deliverable: a ratifiable design spec (the WI-088 pattern) — implementation
WIs get filed from it, not from this intake note.
