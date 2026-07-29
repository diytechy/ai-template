# BUILD DISPOSITION of 009-CRITIQUE U5 — c67e85b (corrected)

**This supersedes the prior version of this file, which overclaimed WI-272 as
"built and Review-A APPROVED … left complete."** That claim was withdrawn under
`011-REVIEW-A-057c5fb.md` (two MAJOR findings, both `@owner`): a
`Verification=Critique` WI cannot be called complete while its own uniformity
critique is CHANGES-REQUESTED and the `perceptual-stale SR-052;SR-053;SR-054`
G3 gate is red. The U5 follow-up is **pending**: it has no registry-authoritative
successor yet, and neither filing it nor re-running the critique can resolve U5
without first integrating its palette fix.
No code changes in this session; this is a documentation-fidelity correction.

## Status of WI-272 — OPEN (not complete)

WI-272 (dashboard work-item status fidelity, M-2 in
`docs/repo-review-2026-07-22.md`) is **open**. Its registry row is `queued`
(`docs/requirements/work-items.csv` — unchanged; a train worker does not edit
Status cells, the integrator does). Nothing here declares it done, and it must
not be flipped to `done` until the two gates in the next section clear.

WI-272's `SR-Refs` are `SR-038;SR-053`. **SR-053 (Dashboard UI uniformity) is a
`Verification=Critique` SR** judged by `TC-054` against
`docs/rubrics/dashboard-uniformity.md`. So WI-272's acceptance is not the
status-fidelity tests alone — it is also on the hook for the uniformity
critique, and that critique currently reads CHANGES-REQUESTED (009, finding U5).

## What must clear before WI-272 can close

1. **The integrator files a uniquely numbered U5 successor row with a reachable
   SpecRef.** That registry row, not this review prose or an unassigned CSV
   example, is the durable and schedulable plan for the palette defect.
2. **The U5 successor changes the palette and its affected render surfaces, then
   its fix is integrated.** The current renderer still maps status `done` and
   Test Case to `#047857`; it also retains the other cross-vocabulary collisions
   recorded by 009. A successor must declare disjoint status, phase, and
   type/tier tokens and regenerate every affected node and legend before a new
   critique can satisfy U5.
3. **Only after step 2, a fresh independent `TC-054` uniformity critique records
   APPROVE against the composed current render.** The 009 critique was fresh and
   family-heterogeneous, but it returned CHANGES-REQUESTED on U5, so simply
   filing its successor or re-firing the critique would not make WI-272 eligible
   to close.
4. **The integrator flips WI-272 → done** through the registry lifecycle *after*
   1–3, on the composed tree, with the two mechanized guards satisfied:
   - `check_trajectory` **perceptual-stale** (`SR-052;SR-053;SR-054`): git-time
     gate. On this train it is red **by construction** — `_latest_critique_file`
     globs only top-level `docs/reviews/*-CRITIQUE.md`, so the train-scoped
     `009-CRITIQUE` in this subdirectory is invisible to it and the newest
     top-level critique it sees is `112-CRITIQUE.md`, older than the
     `gen_trajectory.py` render change. It clears only when a fresh top-level
     `*-CRITIQUE.md` is recorded after the render change (the
     render→re-fire→re-critique→clear steady state; cf. `docs/reviews/112-CRITIQUE.md`).
   - `check_trajectory` **critique_ratchet** (WI-068): warns if a commit closes a
     Critique-verified WI while the latest CRITIQUE verdict is CHANGES-REQUESTED
     and the change set touches neither the TC registry, the tests dir, nor
     `docs/rubrics/`. Closing WI-272 before the re-fired critique APPROVEs would
     trip this.

## What is built and independently reviewed (the builder deliverable)

The six-state lifecycle (`queued|active|done|deferred|blocked|retired`) survives
into every When-tab render surface — this is the M-2 code deliverable, and
`008-REVIEW-A-c67e85b.md` recorded **APPROVE (findings=0)** on the code diff.
That is Review-A acceptance of the *diff*, not a completion verdict for the WI.

- `STATUS_FILL` + the `--deferred`/`--blocked` CSS vars carry `deferred`
  (`#6b21a8`) and `blocked` (`#b91c1c`);
- `STATUS_GLYPH` pairs each with a shape-distinct A3 glyph (deferred ▽,
  blocked ◼);
- the When legend lists both with their meanings (parked / impediment);
- the detail-panel badge colour is emitted straight from `STATUS_FILL`
  (`$status_color`), so it cannot drift from the vocabulary — the exact
  hand-kept four-state copy that was the M-2 defect;
- the flat-DAG fallback routes through the single `_wi_st` clamp helper, so no
  second inline copy can re-drop deferred/blocked.

Both new fills are byte-distinct from every other dashboard palette
(`STATUS_FILL` / `TIER_FILL` / `OKF_TYPE_FILL` / `PHASE_ACCENTS` /
`SW_NODE_FILL`) and clear WCAG AA under white label text (deferred 8.7:1,
blocked 6.5:1).

## U5 follow-up — pending registry filing and implementation (`@owner`)

U5 is **not handed off, durable, or schedulable.** It remains pending until the
integrator files a uniquely numbered successor in `work-items.csv` with a
reachable SpecRef and regenerates the coordination artifacts. The committed 009
critique is evidence of the defect, not its registry-authoritative plan.

The filing must make the following scope explicit: declare disjoint status,
phase, and type/tier palette tokens; move the colliding Test Case/SR/SN and phase
accents to non-overlapping families; regenerate every affected node and legend;
then obtain a fresh TC-054 critique. The successor must be integrated before
WI-272's critique is re-fired (the required order is above).

**Why the row insertion and number are an `@owner`/integrator step, not a train
worker's** (this is why `011-REVIEW-A` routed the finding to `@owner`):

- The parallel-dispatch worker contract forbids a train branch from editing
  root coordination truth, including `work-items.csv` Status/Deliverable cells;
  the integrator regenerates coordination state on the composed tree.
- Adding a `queued` WI row changes the DAG and the WI counts, which would force
  a regeneration of the freshness-gated `PROJECT_STATE.html` — a generated
  artifact a train worker must not regenerate. Leaving it stale instead would
  fail `gen_trajectory.py --check` and break the green bar. Either way the row
  belongs to the integrator, who regenerates the dashboard at composition.
- WI-number assignment is a cross-train collision hazard (concurrent trains have
  collided on ids before and were reconciled by renumbering at integration), so
  a worker must not unilaterally claim the next id.

An uncited live `docs/specs/*.md` file would trip the R-F spec-lifecycle gate
under `--strict`; the integrator must therefore create the SpecRef and its citing
row together. Until that integration action occurs, this WI is blocked rather
than merely awaiting a re-critique.

## Why U5 is out of WI-272's scope

U5 asks to *"declare disjoint palette tokens for status, phase, and type/tier,
move the colliding Test Case/SR/SN or phase accents to non-overlapping hue
families, and regenerate every affected node and legend"* — routed to `@owner`.

- The collisions U5 names are **pre-existing and systemic**, not introduced by
  WI-272: status `done` `#047857` == Test Case type `#047857` (What/Knowledge
  tabs); status `active` `#b45309` == Process Guide type `#b45309`; phase
  accents share hue families with the type palette. WI-272 touched none of
  `TIER_FILL` / `OKF_TYPE_FILL` / `PHASE_ACCENTS`.
- WI-272's own additions introduce **no** byte-identical collision: `#6b21a8`
  and `#b91c1c` are absent from every other palette (verified by grep of
  `gen_trajectory.py`).
- The remedy U5 asks for is a **cross-tab palette-token refactor** spanning the
  What, When, and Knowledge tabs and reassigning established semantic type
  colours — a design decision explicitly routed to `@owner`, and one that would
  itself require its own fresh render critique.

Per the repo's own pattern (M-2 → WI-272, M-3 → WI-273) and the
`render-dashboard-critique` skill ("file findings as their own WIs"), U5 needs
a new owner-decided dashboard-palette-uniformity WI. Expanding WI-272 to redesign
the palette would be scope creep. It remains blocked until the successor is
filed, implemented, integrated, and followed by WI-272's fresh APPROVE critique.

## Evidence (main-repo `.venv`, Python 3.11.9)

- `gen_trajectory.py --root . --check` → `project-state dashboard up to date.`
  (exit 0).
- targeted fidelity tests — **5 passed**:
  `test_deferred_and_blocked_render_their_own_buckets`,
  `test_status_render_vocabulary_cannot_drift_from_the_registry_lifecycle`,
  `test_a3_status_glyph_pairs_every_status_fill`,
  `test_a3_flat_dag_fallback_also_prefixes_the_status_glyph`,
  `test_every_multifill_panel_emits_a_palette_bijection_legend`;
  `test_module_size_ratchet.py` — **1 passed**.
- `check_trajectory --root . --strict`: the only render-related red is the
  by-construction `perceptual-stale SR-052;SR-053;SR-054` gate (top-level
  `112-CRITIQUE.md` vs the train's `gen_trajectory.py` change — clears at
  integration per above). The remaining reds are **WI-275**
  root-coordination-truth (status.md forward-only token + `docs/specs/WI-275.md`
  SpecRef archival) that the integrator scrubs at composition — not WI-272.
