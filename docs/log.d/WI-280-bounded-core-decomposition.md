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

(The follow-ups this section previously left open — the arch-map/top-view
resolution and the LLR containment — are CLOSED by slices 10–11 below.)

---

## 2026-07-31 — WI-280 slices 10–11: bootstrap main(), the spine/seam closeout

Trunk merged in first (`git merge ConcurrencyTrainRewrite`, 7cb7011): one
conflict, PROJECT_STATE.html, resolved by REGENERATION rather than by picking a
side; `project-trajectory/README.md` auto-merged with both edits intact (trunk's
WI-375 agent_common row + this branch's split clause). Trunk's archival of
docs/specs/unattended-entry-point.md also cleared the pre-existing orphan red
this branch had been carrying. Post-merge green set re-run: both `--check`
forms, the two gen_trajectory suites (174 passed), smoke (551 passed).

**Slice 10 — `bootstrap.main()` decomposed (83d6741).** 380 straight-line lines
at complexity **41** — the kit's largest single function, and the one an
adopter's FIRST command runs (the retired WI-082's subject, subsumed here). It
becomes a ~40-line sequencer over nine phases and two typed records:
`build_parser`, `resolve_profile` (the stack/omit ladder incl. `ap.error`),
`resolve_choices` → `ScaffoldPlan`, `copy_kit_files` → `CopyOutcome`,
`apply_stack_extras`, `materialize_agent_layer_phase`, `apply_declared_policies`,
`report_outcome`, `write_stamps`; the `--sync` early return and the final
initialize/exit block stay in `main`. `dataclasses` is stdlib, so the
stdlib-only rule holds.

*Proof that nothing about the scaffold changed*, three ways: the byte-compare
suites (`test_bootstrap` + `test_profile` + `test_stack_profile`, **94 passed**),
a pre/post `--dry-run` **stdout diff** (identical once the dest path and the
dirty-tree stamp are normalized), and a full pre/post **scaffold tree diff**
(identical excluding `kit-version`'s stamp and README's project-name
placeholder). Every print is byte-for-byte, in order.

*One extraction beyond the plan:* `copy_kit_files` measured 13, so its per-file
write went out again as `_write_scaffold_file`. The ratchet prefers
decomposition to a new baseline row, and both now sit under the limit.

**Slice 11 — spine/seam closeout (this commit).**

*(a) LLR pointer re-homes.* Every LLR symbol was resolved against the post-split
AST. **19 rows** whose cited symbols now live wholly in one sibling were
re-homed: `traj_views.py` ← LLR-052/057/085/086; `traj_panels.py` ←
LLR-051/056; `traj_parse.py` ← LLR-078; `traj_render.py` ←
LLR-100/101/102/105/106/109/110/113/114/116; `traj_graph.py` ← LLR-120;
`traj_status.py` ← LLR-139. Rows whose symbols span the facade and a sibling
(LLR-035/055/079/080/099/103/107/108/115/117/119/130) KEEP `gen_trajectory.py`
— the facade is the composition point and re-exports every name, so the pointer
is still true. **No CodeSymbol cell was edited:** nothing S8/S9 touched was
renamed (`route_graph`/`flat_graph`/`GraphGeom`/`TierSpec` are new names, not
renames). Recorded finding, NOT fixed here: ten cells carry symbol names that
already did not exist before this WI (`_nav`, `_tier_column`, `_svg_node`,
`_descend`, `_breadcrumb`, `_drill_svg`, `_drill_edges`, `sw_view`,
`know_graph_svg`, `build_module_map`) — pre-existing staleness, out of scope,
and fixing it would owe a re-attest for reasons unrelated to WI-280.

*Verified in a THROWAWAY copy* (no regenerated artifact committed — §5.2 keeps
them trunk-owned, and the harness confirms `arch-map`/`trajectory-map`/
`status-map`/`open-items`/`ratify-fresh` all SKIP on a work branch): with the
arch map regenerated over the post-split tree the inventory grows 40 → **46**,
all six siblings join **CMP-002**, and the How-SW top view stays **5 items ≤
TOP_VIEW_MAX 10** with **zero uncontained** modules. `component_findings` →
NONE. This closes the follow-up the S2–S9 record left open.

*(a′) Four new cross-component seams.* The regenerated map exposed four real
CMP-002 → CMP-001/CMP-004 import edges that the split MOVED off the facade, each
an undeclared-seam finding. Declared as the rule itself directs, one row per
importing module, each pointing at the parent contract rather than restating it:
**IF-082** traj_parse → check_trajectory, **IF-083** traj_views →
check_trajectory, **IF-084** traj_status → check_trajectory (all three IF-056's
contract), **IF-085** traj_parse → schedule (IF-071's). The three modules are
marked `sink` (they provide nothing across a component boundary — their only
consumer is the facade in the same CMP) and declare their ids in a `Contracts:`
docstring line, which also clears the "connectivity undeclared" and "no Provides
seam" warns for them. **Deviation from the split plan**, recorded: the S2–S9
design said the siblings carry no `Contracts:` line because the seam stays
gen_trajectory's — true until these module-level seams existed; the registry
would otherwise warn on rows nothing declares.

*Residue, stated:* `traj_graph.py`, `traj_panels.py` and `traj_render.py` remain
"connectivity undeclared" WARNs — they genuinely have no cross-component
coupling, and inventing seam rows to silence a warn would be worse than the
warn. Same class as the pre-existing IF-055/080/081 warns on trunk.

*(b) The Verified-row amend discipline — the flip DID happen.* The 19 Module
edits tripped `check_trajectory --staged`'s amend-without-flip warn on all 19
rows. Both sanctioned responses were MEASURED before choosing:

  * flipping the 19 **LLR** rows silences the warn (the checker skips any row
    whose own Status moved) and leaves the derived gate at **G3**
    (`modified=19`) — but `trace.py --ratify modified` then reports "No
    `Modified` SR": the brief is per-SR, so the sitting would never see the
    change. That is precisely what the warn's own wording protects against, so
    this option was REVERTED rather than shipped.
  * flipping the **11 owning SRs** — SR-050, SR-052, SR-053, SR-054, SR-055,
    SR-056, SR-071, SR-088, SR-089, SR-090, SR-135 — clears the warn at its
    root and ARMS the brief: `trace.py --ratify modified` now renders 11
    sections, each showing only the `Module` cell before/after. This is what
    shipped.

Consequence, stated plainly: the derived gate computes **G3 → G2**
(`modified=11`; a Modified SR is simply not Verified, so `sr_gate` derives the
decomposed-unverified rung) until the sitting blesses them. `docs/gate` is generated and trunk-owned, but it is
committed here as a DELIBERATE exception, recorded: it derives from the spine
CSVs this very commit changes and from no trunk-only input (unlike the
dashboard, which needs the regenerated arch map), and
`tests/test_derive_gate.py`'s cache-freshness assertion is NOT branch-aware —
leaving it stale would strand a red in the full suite and in CI. The trunk
step re-derives the identical bytes. Under
`docs/gate-policy: autonomous` the review round's recorded verdict ratifies —
the WI-374 / LLR-143 precedent — flipping the 11 back to `Verified` and
restoring G3. No row that was not edited was flipped.

*(c) `_render_surface_paths` extended* to the whole generator FAMILY
(`gen_trajectory.py` + the `traj_*.py` glob, in both the co-located and the
two-home fallback arms). Required, not cosmetic: after the split every emitter
lives in a sibling, so a facade-only surface would have left the
render-critique-staleness warn running and always passing.

*(d) IF prose,* minimal and only where now false: **IF-071**'s "gen_trajectory
reads the scheduler" was false at module level (the guarded import moved) and is
now the family + a pointer to IF-085; **IF-024**/**IF-052** gained one clause
naming the sibling that holds the read; **IF-056** gained a clause naming its
three sibling-held rows. **IF-074 was left alone** — `gen_open_items` imports
`gt.pending_block`, which still resolves through the facade re-export, so the
cell is still true.

**Ratchet re-stamps, slices 10–11:** bootstrap.py size **2096 → 2224** (reviewed
bump: the extraction-grows-the-file shape WI-347's entry already records);
`("bootstrap.py","main"): 41` **DELETED** (improvement rule — `main` and every
extracted phase are under the C901 limit, and `copy_kit_files` was extracted
again rather than baselined); check_trajectory.py size **3077 → 3098** (the
render-surface family). Census: bootstrap's argparse preamble moving into
`build_parser` left the `cli` clique — eleven `74572e51bafc` bootstrap rows
become nine from check.py, and `ac856932503d` re-fingerprinted to
`495cd311f6ca` over the untouched check == gen_arch_map pair (the WI-347 effect
again); **cli 87 → 85**, header + distribution row re-derived, and the two
count-mutation fixtures in tests/test_dupes_census_audit.py re-pinned.

**Byte-golden, slice 11.** The four new IF rows are a dashboard INPUT, so the
committed PROJECT_STATE.html is legitimately stale on this branch (the trunk
lane regenerates it). Render-neutrality is therefore proven DIRECTLY instead of
through `--check`: the pre-split (S2-parent) renderer and the current split
renderer, run over the SAME repo inputs, both emit **1,776,473 bytes** and the
outputs are **byte-identical** (ASOF excluded, exactly as `--check` does).

**Full close set.** `pytest -q -n auto`: **1700 passed, 12 skipped, 1 failed**
— the failure is the standing
`test_check_lane.py::test_this_repo_is_not_a_work_branch`, which asserts this
repo is not on a work branch and is expected on a claimed branch.
`check_trajectory --strict`: clean (375 WIs, 359 done, 14 retired, graph
acyclic). `check_docs --stale`: OK, 330 docs, 933 links, **0 broken, 0 orphans**
(trunk's archival cleared the one this branch had inherited). `trace.py
--strict`: **exit 0** — SN=25 SR=135 LLR=126 TC=123, orphans=0, integrity=0,
component-findings=0, interface-findings=0. `ruff format --check`: 128 files
already formatted.

**`trace.py --strict --require-verified` exits 1 BY CONSTRUCTION, and that is
the correct state, not a defect to hide.** Its only findings are the eleven
`SR-0xx is Verification=Test but Status=Modified` lines — exactly the rows slice
11(b) flipped, saying the thing the flip exists to say: a ratified SR was
amended and owes a re-attest before the repo may claim G3. It goes green when
the review round blesses the eleven back to `Verified`. Any commit that follows
the amend+flip rule is in this state until its sitting; treating it as a red to
suppress would re-introduce exactly the silent-amendment defect WI-316 closed.
(One real defect WAS found this way and fixed: the first IF-056 edit put commas
into an UNQUOTED Contract cell, so the row parsed to 14 columns against an
11-column header — `trace --strict`'s integrity rule caught it; the clause was
rewritten comma-free and integrity is back to 0.)

**Left undone, deliberately:** the WI spec is NOT archived and no
docs/reviews/ file was written (the orchestrator owns the close ceremony); no
generated artifact (arch map, dashboard, gate, open-items, ratify brief) is
committed from this work branch (§5.2); the ten pre-existing stale CodeSymbol
cells above are recorded, not fixed; nothing was pushed.
