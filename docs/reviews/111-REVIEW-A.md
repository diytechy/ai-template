# 111-REVIEW-A — WI-255/256 (edge-router hardening + desktop clip affordances)

Independent adversarial review (REVIEW-A) of the range `4a0d6db..cd444aa` on
`dualplan-routing-fix` — two build commits: `3e0fc24` (WI-255, edge-router
hardening; consumes 110-REVIEW-A MINORs 1 & 3) and `cd444aa` (WI-256, desktop
clip affordances; 079-CRITIQUE tracked-but-passing imperfections). Reviewer did
not write the code and read no builder self-assessment; judged the artifacts and
drove the shipped paths. Rubric: `docs/rubrics/code-review-adversarial.md`. The
RENDER acceptance (T7/T8 pixels, the WI-243 staleness re-fire) is a separate
critique session's job — this review covers the code and the driven behavior only.

## Scope / subject frame (R1)

Two changes to the WI-253 single-sourced wire router in `gen_trajectory.py`:

- **WI-255** hardens `_detour_d`. Formerly a box overlapping only a port-stub
  corridor was dropped from the lane search, silently keeping a through-box direct
  cubic (110-REVIEW-A MINOR 1, a fail-open). Now `_clear_lane_y` → `_lane_candidates`
  (nearest-first, stable-sorted), and `_detour_d` re-verifies the FULL routed
  polyline (`_detour_points`, sharing one curve with the emitted `_detour_str`)
  against every obstacle in the routed x-span, two passes (lane-span boxes, then
  all span boxes), returning the first fully-clear lane or a least-obstructed
  deterministic fallback. `_routed_label_xy` rides a detoured `sw_graph` label to
  the routed lane midpoint (110-REVIEW-A MINOR 3, a T4 float).
- **WI-256** (a) drives the WI-219 scroll cue from ACTUAL overflow
  (`scrollWidth > clientWidth`) at any width via a client-side `syncScrollCues`
  (resize + tab-switch + `ResizeObserver` + `window.__syncCues` on drill descend),
  the `max-width:760px` media rule kept as the no-JS fallback; and (c) snaps each
  wire TERMINAL to the port center (`sy`/`ty` threaded through `_route_edges` →
  `_detour_d`/`_detour_points`/`_detour_str`) while the first/last control keeps
  the fanned `y1`/`y2`, so a steep fanned wire lands on its port circle.

Blast radius: the generated `PROJECT_STATE.html` render surface (When DAG, How-SW,
Knowledge, drill layers) + the WI-243 staleness gate (both commits re-fire it —
a fresh critique is owed before the next green G3). Specs of record: the WI-255 /
WI-256 rows in `work-items.csv`; findings origins `docs/reviews/110-REVIEW-A.md`
(1, 3) and `docs/reviews/079-CRITIQUE.md`.

Worst failure classes hunted first (R3): the WI-255 fix NOT actually closing the
fail-open (a residual clear-lane-exists-but-through-box class); the WI-256 snap
re-introducing a through-box or loosening the scan's endpoint-exclusion to MASK
one; byte instability / legacy drift; dead (non-biting) tests; label float on a
detour; the scroll cue firing wrongly / a duplicated WI-219 idiom / a static-shot
race; nondeterminism; O(n³) blowup.

## What I verified (driven, not assessed — R2)

**1. Byte-stable regeneration + legacy preservation (WI-255/256 Done-when).**
```
$ python .../gen_trajectory.py --check   -> project-state dashboard up to date.  EXIT=0
$ python .../gen_trajectory.py --check   -> project-state dashboard up to date.  EXIT=0
$ python .../gen_trajectory.py           -> gen_trajectory: already up to date
$ git status --short                     -> (PROJECT_STATE.html unchanged)
```
Cross-commit byte-claims confirmed by diff: `4a0d6db..3e0fc24` changes
PROJECT_STATE.html by **exactly 1 line** — the `state as of commit` stamp
(`2aa9b10`→`4a0d6db`); WI-255 is otherwise byte-identical (`sw_graph` is
fallback-only for meta; 0 stub-corridor violations today). `3e0fc24..cd444aa`
changes only the scrollcue CSS/JS additions plus the fanned `wire` path bytes
(terminal snap). An unfanned wire is byte-identical — pinned by
`test_route_edges_leaves_a_clear_wire_byte_identical` (passes) and the WI-256
docstring invariant (sy==y1, ty==y2 → same format string), driven §6.

**2. WI-255 fail-open fix — the ORIGINAL 110 scenario now holds (R5).** The exact
110 case (a box overlapping only the inboard port-stub corridor, `S` at x[104,118]
inside A's output stub [100,118]) now detours and clears:
```
new router detoured: True | clears S: True
```
And the fix BITES: reconstructing the pre-WI-255 `_detour_d`, that scenario
returned `None` (S dropped from `inrange`) → caller kept the direct cubic, which
crosses S (`old direct cubic crosses S: True`). `test_route_edges_stub_corridor_
box_not_through_box` would go red on revert.

**3. WI-255 label anchoring — driven over the real `sw_graph` (R2).** 65 swedges,
26 detoured (carry an ` L` lane segment); for every detoured swedge the emitted
`swlab` x,y equals `_routed_label_xy`'s lane midpoint (5/5 spot-checked `match:True`,
e.g. `label(447.0,486.9) == routed_xy(447.0,486.9)`). A straight (direct-cubic)
edge has no ` L`, so `_routed_label_xy` returns the chord-midpoint fallback
byte-identical (`(999.0,888.0)` in-out). Handles negative lane coords.

**4. WI-256 terminal snap — 0 through-box on every real panel; the scan still
BITES (R2/R3).** With the snap in place, the mechanized T8 scan over the real meta
repo:
```
ROUTED  When=0  How-SW=0  Knowledge=0  dag_svg=0  sw_graph=0
```
To prove the snapped endpoints did not loosen the scan's endpoint-exclusion into
masking grazes, I disabled detours (`_polyline_hits→False`) and re-scanned the
same snapped-endpoint panels:
```
LEGACY  When=61  How-SW=11  Knowledge=464   (536 through-box violations detected)
```
The scan bites hard with the new terminals — the snap moves each endpoint to the
exact port center (narrower than the former fanned band), tightening, not
loosening, the `on_src`/`on_tgt` exclusion. `test_route_edges_terminals_snap_to_
port_circle` bites: terminals emit `120.0` (port center) with the fan offsets
`108/132` surviving in the controls; a reverted router would emit `108.0` and fail
the `==120.0` assertion.

**5. Determinism + degenerate termination.** A box straddling the source port
(no clear inboard lane) returns in **0.000 s**, detours, and over **200
dict-insertion-order shuffles → 1 distinct output**. Candidate set is finite;
always terminates.

**6. Scroll-cue correctness (static / mechanism).** Generated HTML carries: the
default `.scrollcue { display:none; … grid-column:1/-1 }`, the WI-256
`.scrollcue.cued { display:block; }`, and the preserved no-JS fallback
`@media (max-width:760px){ … .scrollcue{ display:block; } }`. `syncScrollCues`
is defined once, toggles `.cued` only on REAL overflow (`scrollWidth > el.clientWidth
+ 1` — the `+1` guards sub-pixel false positives, so no cue when nothing clips),
walks to the preceding `.scrollcue` sibling, and is re-run on load, resize, tab
switch, `ResizeObserver`, and `window.__syncCues` (called from `DRILL_SCRIPT`
after a descend, guarded `if(window.__syncCues)`). No duplicated WI-219 block
(check_dupes clean, §8). The runtime pixel behavior (does `.cued` appear at
1280/1680) is critique-owned — see UNVERIFIABLE below.

**7. Lint / complexity / dupes (G3 quality gates).**
```
$ python -m ruff check …gen_trajectory.py          -> All checks passed!
$ python -m ruff check --select C901 …             -> 4 errors, ALL pre-existing
        (arch_icicle:20, sw_containment:28, when_view:15, _okf_nodes:15 — no WI-255/256 helper)
$ python -m pytest -q tests/test_complexity_ratchet.py -> 1 passed
$ python …/check_dupes.py --src project-trajectory/scripts -> OK - no duplicate blocks in 34 file(s).
```
Every new/changed helper (`_lane_candidates`, `_detour_points`, `_detour_str`,
`_detour_d`, `_routed_label_xy`, `_route_edges`) is C901 ≤ 10; ratchet unworsened.
Stdlib-only, Python 3.8.

**8. Suites green.** Targeted `-k "stub_corridor or routed_label or terminals_snap
or avoid_unrelated_boxes or clear_wire_byte or detours_around or scroll_affordance
or reroutes_a_backward"` → **10 passed**. `python -m pytest -q -n auto -m smoke`
→ **995 passed, 3 skipped** (288 s).

## Done-when coverage map (R4)

| Done-when item | Status |
| --- | --- |
| WI-255: re-verify the full routed polyline clears all obstacles | **COVERED on the render surface** (0 through-box, §4), the reported 110 scenario fixed (§2) — but the re-verification span omits the ±18px outboard stub extension: a driven residual fail-open remains (MINOR 1) |
| WI-255: anchor a detoured `sw_graph` label to its routed lane | **COVERED** — §3, driven over the real sw_graph |
| WI-256: desktop clip affordance (extend WI-219 cue via actual overflow) | **COVERED (mechanism)** — §6; pixel appearance is critique-owned (T7) |
| WI-256: wide-drill-layer clip cue on descend (`__syncCues`) | **COVERED (mechanism)** — §6 |
| WI-256: steep wires terminate on the port circle | **COVERED** — §4, snap driven + bite-proof |
| Byte-stable regeneration (`--check` green twice) | **COVERED** — §1 |
| Fresh `*-CRITIQUE.md` clears the WI-243 gate (T7/T8) | **OUT OF SCOPE** — critique session (both commits re-fire the gate by design) |
| Row `done`, SpecRef cleared, spec archived (R-F) | **OUT OF SCOPE** — close step; WIs `queued` during build+review |

Every code-verifiable Done-when maps to a driven observation; the two findings
below are narrower residuals, not uncovered acceptance.

## Findings

- [MINOR] project-trajectory/scripts/gen_trajectory.py:1575-1594 (`_detour_d`) ->
  the WI-255 full-polyline re-verification computes its obstacle set `full` over
  `[min(x1,xe), max(x1,xe)]`, but the detour's stubs reach `xa=x1+stub` /
  `xb=xe-stub` — 18px OUTSIDE that span. A box sitting in that outboard stub zone
  is never hit-tested, so the router reads `hits==0` and returns a detour that
  grazes it: a residual of the very fail-open class WI-255 set out to close, and
  the docstring/commit's absolute "never a silent through-box when a clear route
  exists" is falsified. Driven — replaying a random adversarial sweep, trial 679
  (a backward seam D→C): the emitted detour's left stub reaches x=296.3, box E at
  x[206.9,298.8] overlaps [296.3,314.3] but not the router's `full` span
  [314.3,586.1] (`E in full? False`), the router path DOES cross E, and a far lane
  clears every box (a clear route exists). 13/3000 random cases (8 outboard-stub,
  5 where the nearest bands graze and the clear lane sits beyond the ±40 lane
  window). **0 on every real meta/fallback panel (§4) — tiered/columnar layouts
  never place a box in an outboard stub zone — so no live defect; downstream
  robustness only** -> widen `full` and the hit accounting to the stub-extended
  span `[min(x1,xe,xa,xb), max(x1,xe,xa,xb)]` (and/or extend the ±40 lane window
  when the nearest bands still graze), or soften the docstring's absolute claim ->
  @owner
- [MINOR] project-trajectory/scripts/gen_trajectory.py:1586-1598 (`_detour_d`) ->
  WI-255's two-pass × per-candidate full-polyline re-verification makes
  `_route_edges` ~30-50x slower on DENSE-overlap geometry than pre-WI-255 (driven,
  identical harness old vs new): N=150/300e **447 ms → 24.1 s**, N=300/600e
  **1.18 s → 37.9 s** (each detour is ~O(bands·samples·obstacles) over two passes).
  A realistic tiered layout is unaffected — 6col×20row (120n/100e): **124 ms vs
  128 ms** — and the layered emitters only ever produce tiered geometry (the real
  meta panels build in ~3.1 s total, `--check` byte-stable), so no live impact; but
  a downstream repo with a dense/overlapping diagram could see multi-second-to-
  tens-of-seconds regenerate. It runs at regenerate/gate time, not a hot path ->
  short-circuit (skip the second `full` pass when `lane_span` already clears; cap
  the candidate set) or memoize the per-edge obstacle filter -> @owner

Both findings are downstream/pathological robustness only; the meta render's
code-verifiable Done-when (0 through-box across all five panels, byte-stable, the
scan proven to bite, label anchoring fixed, terminal snap correct and non-masking,
the scroll-cue mechanism statically correct) holds. This matches how 110-REVIEW-A
disposed of the same fail-open class (MINOR, APPROVE): WI-255 genuinely fixes the
two reported MINORs and shrinks the fail-open dramatically, leaving a narrower
residual worth the owner's note.

## Unverifiable (and why)

- **WI-256 render/pixel acceptance** — whether the `.cued` cue actually appears on
  the icicle at 1280/1680 and on the When›unphased / How›CMP-004 drill layers, and
  whether the snapped wires land on their port circles in pixels — is client-side
  runtime + perceptual judgment, owned by the bundled `*-CRITIQUE.md` (T7/T8, the
  WI-243 re-fire). I confirmed the emitted mechanism is correct and race-free for a
  static shot (synchronous `syncScrollCues()` on load + observers), but I do not
  run a browser here.

- VERDICT: APPROVE findings=2
