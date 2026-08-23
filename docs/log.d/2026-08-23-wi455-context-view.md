## 2026-08-23 — WI-455 slice 5: the `external.toml` context view lands; the lane's last executable half closes

**Summary.** Item 3 of WI-455's STILL OWED list is done: the depth-0 frame —
who is outside this system, what crosses its boundary, and the
external-to-external flows the system is not a party to — is now DERIVED from
`docs/requirements/external.toml` into `PROJECT_STATE.html`'s architecture tab,
above the derived module map. That derived view IS the boundary record
sitting-2 decision 8 kept "with the architecture", which is what let
`docs/architecture.md` be retired in slice 1; this slice is the execution of
that clause. Nothing in the locked frame was edited, and no `direction` /
`this_project` cell was touched (item 1's scope, still the owner's).

**The panel's shape.** One block, spliced into the `sw` panel directly after its
heading — above the structure, because what is outside and what crosses is
settled before what the inside is built of.

- **A self-contained SVG.** One lane per crossing, grouped so a party holding
  several keeps one card spanning them (`EXT-001` holds three); the system
  opposite as the emphasized card on the merge slot's theme-invariant `--slot`
  token; each crossing a directed wire whose heading is read from the SYSTEM's
  point of view (`in` heads at us, `out` at the party, `inout` both); the
  relationships bowed into the left gutter so they never cross the system card,
  because the system is not a party to them. A declared party holding no
  crossing keeps a card and simply has no wire — `EXT-003` and `EXT-005` are
  exactly that. Fixed geometry, `.1f` rounding, id-sorted inputs, no clocks.
- **Three tables** carrying every cell the wires truncate: crossings (with the
  realizing rows), parties, relationships. Plus the untied list below.
- **Theme-aware throughout, no new colour.** Every fill is an existing CSS token
  (`--slot`, `--surface`, `--muted`, `--border`, `--text`); the legend swatches
  take their paint by CLASS rather than an inline hex, so nothing restates a
  theme token as a literal and dark mode is not painted with light values.

**Tie-back rendering — the three decisions.**

1. **Realization is JOINED from `interfaces.toml`, never read off the frame
   row.** The frame is locked and a realization is the other side's claim — the
   same split that lets an SR state the crossing while an LLR states which piece
   provides it. So `realized_by` is derived per crossing from
   `interface_from_external` / `interface_to_external`, carrying which side it
   ties on.
2. **An unrealized crossing is DRAWN, not hidden.** `B-02` (Authority) is
   realized by no interface row; it renders dashed, its table cell reads "none —
   declared, not yet realized", and the legend names the idiom. The registry
   header's `SR-140` reason is linked to rather than restated: the view states
   the derived fact and points at the registry, which is where the ruling lives.
3. **The adjudicated absences are stated with their recorded reasons.** An
   interface row whose endpoint carries the `external:` marker but which ties
   back to no crossing is listed under "External endpoints that tie back to no
   crossing" with the whole reason its own row records. On this repo that is
   exactly `IF-032`, `IF-036`, `IF-041` — the three WI-455 slice 2 adjudicated —
   while `IF-080`/`IF-081`, the two that slice tied to `B-05`, now appear in
   `B-05`'s realizing set. A frame rendered silently shorter than the registry
   is indistinguishable from a complete one, which is why the absences are part
   of the picture rather than dropped from it.

**Where it lives.** `traj_parse.frame_context` is the read model (four id-sorted
lists; `None` when the repo declares no frame). `traj_context.py` — a NEW
shipped sibling — is the renderer. `gen_trajectory._splice_context_into_panel`
puts it at the top of the How panel, checked explicitly rather than asserted
(the L-02 `python -O` lesson the flows splice already carries).

**Deviations from the assignment, and why.**

- **A new module rather than a section of `traj_views.py`.** The view is ~440
  lines and `traj_views` was at 1,209; the ratchet reds at 1,500 with the rule
  *decompose, never bump*, and it did red at 1,655 before the split. So
  `traj_context.py` ships as the seventh `traj_*` sibling — a clean seam anyway
  (one data source, one tab block, no shared state), and a render leaf that
  imports only `traj_render`.
- **That makes this a SCAFFOLD-SURFACE change**, which the assignment did not
  anticipate: `bootstrap.py` MAPPING + its module-list docstring line,
  `tests/test_bootstrap.py`'s file list, `project-trajectory/README.md`'s
  kit-contents row, and a `RESYNC_PACK.md` entry (copy the module with the
  generator or a scaffold `ImportError`s on its first render). Verified by
  BOOTSTRAPPING A REAL SCAFFOLD, not by reading the mapping.
- **One consolidation on the way past** (`cmp_rows`' inline "real rows"
  predicate lifted to `traj_parse._real_rows`, which the frame's four tiers
  would otherwise have restated four more times). `sort=False` preserves
  `cmp_rows`' file order exactly, so the CMP table's bytes are unchanged.
- **No new `IF-###` row.** `traj_parse` declares four seams and does NOT carry
  one per registry it reads (it reads the SN/SR/LLR/TC tiers, `components.toml`
  and `docs/stage` with no row each), so a row for this read would be a new
  convention, not an application of the existing one — and it would enlarge the
  population `OI-60` is pending on. Recorded as a judgement, not an omission.

**Ratchets re-stamped, with reasons.** `bootstrap.py` 3125 → 3126 in
`tests/test_module_size_ratchet.py`: one MAPPING row plus the module's name in
the sibling-set docstring line. That is the only bump; `traj_views.py` returns
to its pre-slice 1,209 lines and needs no entry.

**Spine acts.** `LLR-200` (the depth-0 frame as a generated context view;
module `traj_context.py`, `CMP-009`, parent `SR-168` — the state view a reviewer
reads the repository from "without consulting a second surface", which is
precisely what the boundary record no longer needs) and `TC-196` (the ten test
nodes below). Both mint **Drafted** — approval is the owner's act. Watermark
raised by `trace.py --bump-ids`: LLR 199 → 200, TC 195 → 196. The LLR was owed
rather than optional: a module with no design row reads as *uncontained* in
`component_top_view`, which `tests/test_traj_views.py::test_meta_component_top_view_smoke`
holds at empty.

**Two findings surfaced rather than fixed inline.**

- **`SR-168` now has 8 direct LLR children, one over the declared bound of 7**
  (`trace.py` advisory, warn-only). Introduced by `LLR-200` and stated rather
  than silenced: the remedies the detector names — split the parent by
  observable class, or record a per-row `fan-out re-stamp` in its Rationale —
  are edits to an approved SR, which is an owner-tier act and not this slice's.
- **The parenting itself is the weaker half of that finding.** No live SR
  states "the state view carries the boundary record": `SR-168` is the
  progress/decomposition half, `SR-169` the components-and-interfaces half, and
  `SR-162` is the harness's *resolution* obligation, not the view's. `SR-168`
  was chosen because its "without consulting a second surface" is exactly what
  retiring the architecture document and deriving the frame achieves — but the
  honest reading is that the derived-boundary-view obligation has no row of its
  own, and that is a requirements question for the owner, not a rendering one.

**Freshness, driven red.** `PROJECT_STATE.html` is already a declared generated
artifact, so the panel rides the existing machinery. Proven rather than assumed:
`gen_trajectory.py --check` green at HEAD → one `kind` cell edited in
`external.toml` → **`--check` exits 1, "project-state dashboard STALE"** → cell
restored → green again.

**Scaffold verification.** Bootstrapped a fresh scaffold into the session
scratchpad. `scripts/traj_context.py` ships; with the blank form's `-000`-only
`external.toml` the dashboard renders with **no context block at all** (the
vacuity guarantee — a project that declares no boundary pays nothing); with a
real three-row frame written in, the block renders, the self-referential
relationship draws as a loop rather than a degenerate curve, and
`gen_trajectory.py --check` is green.

**Lane state.** Item 3 is STRUCK. Item 1 — the `direction`/`this_project` shed
and the counterpart→consumers transform — remains, blocked on `OI-60` (pending,
the owner's) and on nothing else. The lane therefore stays ACTIVE holding item 1
alone; it is NOT closed.

<!-- fig: cmd="python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce && python -m pytest -q -n auto" rev=this-worktree -->
**Gates.** smoke + smoke-budget enforce + `check_docs.py --root . --stale` +
`check_trajectory.py --root . --strict` clean; full unfiltered suite green
(totals pasted in the commit body).

Deferred open items: OI-60
