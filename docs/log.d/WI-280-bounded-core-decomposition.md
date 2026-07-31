## 2026-07-31 — WI-280 slices 2–9: gen_trajectory.py decomposed into six siblings + a facade

**BUILD (slices S2–S9 of the owner-approved decomposition; slices 10–11 — bootstrap
main + closeout — remain open).** `project-trajectory/scripts/gen_trajectory.py`
(5,274 splitlines at claim) is now a **941-line facade** — docstring (Contracts:
line kept), the guarded `check_trajectory` import (the family's ONE sys.path
repair), the sibling imports + consumer-read re-exports, `OUT_HTML`/`ASOF_RE`,
`HTML_TEMPLATE`, `build_html`, `main` — over six new siblings, every move a
verbatim cut-paste:

- **S2 `traj_graph.py`** (234debc, 614 lines): `_dag_ranks`/`_reorder`/
  `_layered_layout`, the `_port_fan` constants+helper, the whole WI-253/WI-323/
  WI-366 wire-router block. No imports.
- **S3 `traj_parse.py`** (2158f08, 434 lines): `_sn_rows`/`read_sns`/`_spine`,
  `spine_stats`, `project_vision`/`project_name`, `WORKSTREAM_LABELS`, the
  `_run_captured`/`_asof`/`_git` capture seam, `sw_modules`/`cmp_rows`, the OKF
  loaders (`OKF_DIR`/`OKF_TIER_ORDER`/`_okf_frontmatter`/`_okf_nodes`), the gate
  readers (`PROCESS_GATE_FILE`/`_gate_value`/`_process_doc`), and the guarded
  `schedule` import's ONE home (siblings read `traj_parse.schedule`).
- **S4 `traj_render.py`** (259b95a, 906 lines): `esc`/`SCROLL_CUE`/`_hscroll`,
  the declared vocabularies (`TIER_FILL`/`TIER_COL`, `STATUS_*`, `SW_NODE_FILL`,
  `OKF_TYPE_FILL`/`OKF_TYPE_CODE`, `PHASE_ACCENTS`, `SVG_RX`, `RING_INKS`), the
  responsive svg wrappers (`_FOCUSABLE`..`_svg_role`), `tab_button`/
  `tab_panel_open`/`_arrow_markers`, the ring-ink helpers, and the drill renderer
  (`DRILL_GEOM`..`_drill_layer_svg`/`_render_drill`).
- **S5 `traj_views.py`** (25b9ce6, 1,141 lines): `arch_icicle` (+ drill ids),
  the flat DAG (`dag_svg`/`_dag_layout` + `DAG_*`), the How-SW seam graph
  (`sw_graph`/`_sw_node` + `SW_*`) and containment drill (`sw_containment`),
  `_wi_status`/`_wi_st`, the tiered `when_view` (+ `_wi_phases`/`DEFAULT_PHASE`),
  `_sw_panel`/`_cmp_panel`.
- **S7 `traj_status.py`** (bd32d93, 508 lines — built BEFORE S6, see deviations):
  the `STATUS_MD` marker block, `_gate_facts`/`_spine_counts`, the open-item
  one-liners, the blocked/spine/pause pending sources + `pending_block` (still
  the one derivation `gen_open_items` imports, via the facade), `status_block`,
  the Ready-frontier lines, `_title_clause`/`_clip_title`, `_splice_status`/
  `run_status`; `main`'s `--status` arm calls `traj_status.run_status`.
- **S6 `traj_panels.py`** (d600969, 1,016 lines): `know_graph` + the type-tiered
  `know_view`/`_know_panel` (+ `KN_*`), the Process tab (`LOOP_GEOM`..
  `_loop_panel`, `process_panel`), the Next-work card (`_NEXT_WORK_*`,
  `_next_work_title`/`_next_work_html`).
- **S8** (1288520): `GraphGeom` (frozen, iterable dataclass) + `route_graph`
  (the shared fan/rects/route sequence; returns `(routes, out_off, in_off)`
  because the sw seam graph anchors labels to the fan) + `flat_graph`
  (adjacency + id-seeded layout + routing for the two flat graphs) in
  traj_graph; the four call sites parameterize exactly (dag 12/2, sw 12/2,
  know 12/2, drill 14/PORT_R+2).
- **S9** (this commit): `TierSpec` + module-level `_add_tier_rows` (arch_icicle's
  SR/LLR arms as one loop over a column declaration), `_subtree_modules`/
  `_layer_edges` lifted out of `sw_containment`, `_agg_edges`/`_wi_block` lifted
  out of `when_view`.

**Byte-golden proof, every slice:** `gen_trajectory.py --check` and
`--status --check` (and `gen_open_items.py --check`) green against the committed
artifacts after every slice AND after S8/S9's behaviourally-sensitive rewrites;
additionally the **pre-split baseline scripts** (a snapshot of `scripts/` at the
S2 parent) were run as `baseline/gen_trajectory.py --check` over each slice's
tree — old code and new code generate byte-identical output from the same
inputs. The one committed dashboard change (S4) was **input-driven**: the WI-280
spec title gained the sibling names (see deviations), which renders into the
When drill; the baseline scripts' `--check` passes over the regenerated
artifact, proving the render logic itself never moved. Test bar per slice:
`tests/test_gen_trajectory.py` + `tests/test_gen_trajectory_pending.py`
(174 passed, every slice) + the smoke tier (551 passed; the standing
`test_check_lane.py::test_this_repo_is_not_a_work_branch` red is the expected
claimed-branch signal) + `check_docs.py --stale` OK + `ruff format` clean.

**Census (docs/dupes-allow), every number:**
- S3: five fingerprints re-homed in place (markdown-table `8c11d9f9d54a`/
  `6050c334ce2f`, declared-file `75b2bcbfcc04`/`8e99e263cf71`/`eff0eac572a0`)
  onto traj_parse.
- S4: one `99c2a2ac7eff` + one `e7ebc7f29c86` graph-layout copy re-paired onto
  traj_render.
- S5: tier-node-build `29c06640159e` → traj_views==traj_views; graph-walk
  `a2fa21743919` and okf-row `9205a1d4996b`/`fb06318154af` → traj_views;
  graph-layout 11 → 10 (`b860b104d408` + one `e7ebc7f29c86` dissolved,
  `f0492e98954e` appeared over the same know_graph==dag_svg sequence — the
  WI-347 clique re-pairing, read and classified).
- S6: all ten graph-layout lines re-homed onto traj_panels (know_graph moved).
- S7: spine-loader `4b5af82ebaa3` → traj_status.
- S8: **graph-layout class (10 blocks, debt WI-280) DISSOLVED** — census lost
  all ten fingerprints, zero new blocks; class + distribution row deleted.
- S9: **tier-node-build class (1 block, debt WI-280) DISSOLVED**, and the two
  okf-row gen_okf pairings dissolved with it (okf-row 3 → 1). Zero new blocks.
  Header counts + distribution table re-derived at each step
  (tests/test_dupes_census_audit.py green per commit).

**Ratchet re-stamps, every number:**
- Size (tests/test_module_size_ratchet.py): gen_trajectory.py 5274 → 4695 (S2)
  → 4304 (S3) → 3468 (S4) → 2381 (S5) → 1911 (S7) → **entry RETIRED at S6**
  (941 lines, under the 1500 threshold — the H-2 monolith is decomposed; bump
  history kept as prose). bootstrap.py 2085 → 2090 (S2) → 2091 (S3) → 2092 (S4)
  → 2093 (S5) → 2094 (S7) → 2096 (S6) — the six MAPPING rows + inventory lines,
  the same required-registration shape as WI-329/WI-374. No traj_* sibling
  crossed the threshold (largest: traj_views 1,141 at S5).
- Complexity (tests/test_complexity_ratchet.py): `_okf_nodes` 15 re-keyed to
  traj_parse.py (S3); `arch_icicle` 23 / `sw_containment` 28 / `when_view` 15
  re-keyed to traj_views.py (S5); S9 re-stamped **arch_icicle 23 → 19,
  sw_containment 28 → 17, when_view 15 → under the limit (entry deleted)**.

**Deviations, each with its reason:**
1. **Comment attachment at cut boundaries.** The spec's measured line ranges
   sometimes ended on a comment belonging to the NEXT item (e.g. `_spine`
   "210-256" includes TIER_FILL's WI-292 comment). Comments moved with the
   constant/function they describe, not with the numeric range; section-header
   comments moved with the section's first surviving item.
2. **S7 before S6.** `traj_panels._next_work_title` calls
   `traj_status._title_clause`; building status first avoids a facade import
   cycle. Commit labels keep the spec's slice names.
3. **Monkeypatch targets** (spec said `load_script("traj_graph")`): `load_script`
   builds a fresh, unconsulted module object, so the tests patch
   `gt.traj_graph` / `gt.traj_parse` — the cached sys.modules instances the
   moved functions actually resolve in.
4. **One test edit beyond the spec's list:** the U3 `rx`-literal source scan
   (test_gen_trajectory.py) follows the emitters across gen_trajectory.py +
   traj_*.py — it would have gone vacuous (and asserted) once the emitters
   finished moving. And at S9 the census-audit mutation proof
   (test_dupes_census_audit.py) now FABRICATES the debt-charged class it
   replays — S8/S9 dissolved the last live one, and the ownership rule must
   outlive the classes it policed.
5. **WI-280 spec row title amended** (docs/work/active/…, S4): the census
   audit's anti-catch-all rule requires a debt-charged class's WI row to NAME
   every module in the class, so the Modules-owned clause gained the six
   sibling names — the exact mechanism the row's own text declares itself for.
   That title renders into the dashboard, hence the one input-driven
   PROJECT_STATE.html refresh (4 lines), proven render-neutral by the baseline
   scripts' `--check`.
6. **S8 extension:** `flat_graph` added beside the spec'd `route_graph` —
   without it the graph-layout class left a 2-block adjacency-preamble residue
   (`76cdecd0d810`/`b240d68b0686`) instead of dissolving.
7. **`schedule` reads rewritten** to `traj_parse.schedule` in
   `_frontier_lines`/`_next_work_html` — the spec's own directive (traj_parse
   is the guarded import's one home).

**Known follow-ups for the orchestrator (slices 10–11 / closeout):** the six
new modules join the arch map only when the trunk regenerates
docs/architecture.md (work-branch lane rule §5.2 — generated artifacts are
trunk-owned, so this branch left it untouched); at that point the How-SW top
view gains six uncontained modules (5 → 11 items > TOP_VIEW_MAX 10) and the
knowledge⇒component coupling rule will flag them until LLR `Component` rows
contain the siblings (registry work deliberately left out of these slices —
Verified-row Module re-pointing owes re-attestation and is an owner act).
