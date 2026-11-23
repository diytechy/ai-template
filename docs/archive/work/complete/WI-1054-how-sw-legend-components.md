+++
id = "WI-1054"
title = "The flat How-SW graph's legend names the component nodes it draws"
workstream = "scripts"
sr_refs = ["SR-169"]
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1054`, cut from `refactor_again` at
`3c33b3783`, with the commit hooks on. One test case was minted from the
lane's range, TC-508, and `trace.py --bump-ids` raised the TC mark from 484
to 508. No status moved and no act was taken. The specref (WI-1048's
archived spec, whose "Found and not changed" list this row was filed from)
is cleared at close, as a terminal row's is.

- `7fee67b8a`: the code, the test, TC-508, a `RESYNC_PACK.md` entry anchored
  `[since 3c33b3783]` and the regenerated views. The hook's 29 steps all
  passed.
- The commit after it: the close-out, this Deliverable, the move to
  `complete/` and the log fragment.

**The legend names every node kind the graph draws (Done-when 1).** The
flat graph draws each node in `SW_NODE_FILL[kind]`, its kind one of the four
`_sw_node` returns: component, module, file or external party. Its legend
was written out by hand and named three of them. `rendering/traj_render.py`
now holds, beside `SW_NODE_FILL`, one table of the words each kind's legend
entry reads (`SW_NODE_LABEL`: component, module, file (shared-contract hub),
external actor) and `sw_legend`, which emits one entry per kind whose swatch
is `background:` that kind's `SW_NODE_FILL` value, the same dict entry the
node's `fill` reads. The flat legend is `sw_legend()`, so it gains the
component entry in the component nodes' own fill, and the graph's caption
names component nodes beside the other three. No colour is copied: swatch
and node read one dict entry, which the test's changed-fill arm shows. The
legend stays static, as both How-SW legends were: it names all four kinds
whatever one graph draws.

The containment drill's legend calls the same helper and passes its own
component swatch, since a drill component block is a surface-filled
container (`var(--surface)` with a `var(--border)` edge), not the stone
fill. Its output is byte for byte the old literal: the two strings compare
equal, and the regenerated `PROJECT_STATE.html`, whose How-SW panel is the
drill, changed only in its counts and in the What view's new TC-508 leaf.
The flat panel's stale comment ("component containers never render here,
so three entries") and `sw_graph`'s docstring now name the four kinds.
`traj_views.py`'s SLOC fell 999 -> 987, under the size ratchet's threshold
of 1000; `traj_render.py`'s rose 556 -> 570.

**The test (Done-when 2).**
`tests/test_traj_views.py::test_the_flat_graph_legend_names_every_node_kind_it_draws`,
tagged TC-508. With no component holding a module, it renders the How-SW
panel in-process as the generator does, over two rows whose endpoints reach
a component, an external party, a file and a module, and reads the kind
and fill of every node drawn and the swatch and words of every legend
entry. It asserts that the graph draws every kind `SW_NODE_FILL` declares,
so a kind the palette gains fails until the fixture draws it; that each
drawn kind has an entry whose words open with the kind's name beside a
swatch equal to its nodes' fill; and, with the component fill changed to a
sentinel, that the component node and its swatch both carry it.

- Red first, on the code before the change:
  `1 failed, 66 deselected in 0.70s`, "the legend omits the component node
  (#44403c)".
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_traj_views.py -k flat_graph_legend" rev="3c33b3783 with only the test and TC-508 added" -->
- Two mutations of the new code, each reverted before the commit: the
  component dropped from the words table,
  `1 failed, 66 deselected in 0.52s` (the same message); the flat legend's
  component swatch given a copied hex, `1 failed, 66 deselected in 0.48s`
  (the changed-fill arm).
  <!-- fig: cmd="a scratch script applying each mutation in turn, then python -m pytest -q -p no:cacheprovider tests/test_traj_views.py -k flat_graph_legend" rev="7fee67b8a (its tree before the commit, less ruff's whitespace-only reformat of the new test)" -->

**TC-508** (new, Drafted, Unit, Full; verifies SR-052 and LLR-113). Its
Method renders the flat interface graph, no component holding a module,
over rows that make it draw all four node kinds, then again with the
component kind's declared fill changed; its Expected is that the legend
holds, for each kind drawn, an entry naming it in words beside a swatch of
its nodes' fill, and that after the change the component node and its
swatch both carry the new fill. Its text names no code; its evidence cell
is generated from the tag.

It verifies LLR-113 because that Accepted row already states the
obligation the flat legend broke: every vocabulary member painted in a
rendered document resolves to a legend swatch labelled in words in that
same document. TC-118's sweep never rendered a flat graph with a component
node (its flat fixture draws module, file and external nodes), which is how
the gap shipped. LLR-080 and TC-081, under the spec's SR-169, state what the
graph draws, not how its key reads. So no requirement text changed and no
design row was minted. LLR-113's `test_refs` keeps its pointer
`(see TC-118)`; TC-508 links through its `verifies` cell. The new table's
`Implements: SR-052, LLR-113` tag sits in `traj_render.py`, already
LLR-113's one tagged file, so the row's realizing files do not change. The
frontmatter's `sr_refs` still reads SR-169, as filed.

Its phase is 3, LLR-113's and TC-118's. A `Drafted` case verifying SR-052, a
phase-3 requirement, moves phase 3's live stage from DevStg-Impl to
DevStg-Tests (`docs/stage`), so `check_trajectory` now warns that new
content entered the closed phase 3 and a `[3]-[DevStg-<rung>]` work item is
due. The stage derivation places a case in the phase of the requirement it
verifies, whatever its own cell says: set to 6, the cell moved nothing
(tried, and reverted). The warning is advisory, it clears at the case's
first acceptance, and whether to file that work item is the coordinator's
call; no work-item id is in this lane's range.

**Tests.**

- The modules importing `traj_render` or `traj_views` (and the facade's
  dashboard renderers), the modules `trace.py --tests-for` names for them,
  the RESYNC pack's two, the registry readers and the whole-tree tests:
  `test_bootstrap`, `test_changed_selection`, `test_complexity_ratchet`,
  `test_gen_open_items`, `test_gen_open_items_render`,
  `test_module_size_ratchet`, `test_smoke_tier`, `test_traj_graph`,
  `test_traj_lanes`, `test_traj_render`, `test_traj_render_sweeps`,
  `test_traj_views`, `test_traj_panels`, `test_traj_parse`,
  `test_traj_status`, `test_trajectory_staged`, `test_retire_dashboard`,
  `test_gen_trajectory`, `test_gen_trajectory_pending`,
  `test_gen_trajectory_splice`, `test_dashboard_size_budget`,
  `test_generated_newlines`, `test_frame_context`, `test_resync_pack`,
  `test_check_resync`, `test_id_watermark`, `test_id_landing`,
  `test_cell_classes`, `test_check_test_first`, `test_evidence_join`,
  `test_llr_trace_cells`, `test_check_doc_refs`, `test_import_layers`,
  `test_dogfood_sync`, `test_smoke_budget`:
  `798 passed, 1 skipped, 18 warnings in 685.86s (0:11:25)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n 12 --basetemp D:/rt1054/t <the 35 modules listed>" rev="7fee67b8a (its tree before the commit, less ruff's whitespace-only reformat of the new test)" -->
  After that reformat, the new test again:
  `1 passed, 66 deselected in 1.17s`.
- `trace.py --root . --strict`: `orphans=0 integrity=0`, exit 0.
  `check_trajectory.py --root . --strict`: clean, exit 0. Each on the
  build's tree and again on the close-out's.
  `scripts/check_resync.py`: "OK, 2 shipped path(s) changed; entry anchored
  at 3c33b3783".
- `run_menu.py smoke`, once at the end, on the close-out's tree:
  `3724 passed, 3 skipped, 18 warnings in 315.98s (0:05:15)`, exit 0. Its
  budget line reads CPU 695.5 s against 540, a WARN only, not charged to
  the lane.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="7fee67b8a with the close-out's tree, before its commit" -->

**Byte deltas** (none budgeted or watched):
`docs/test/test-cases.toml` 693,595 -> 694,389 (+794);
`project-trajectory/RESYNC_PACK.md` 752,486 -> 753,539 (+1,053);
`rendering/traj_render.py` 55,055 -> 56,207 (+1,152);
`rendering/traj_views.py` 58,604 -> 58,249 (-355).

**Acts owed for automated adjudication.**

- Amendments to `Accepted` rows: none.
- Routed traced changes to `Accepted` rows: none.
- First acceptance: TC-508 (`Drafted`), verifying SR-052 and LLR-113, both
  `Accepted`.

**Found and not changed** (outside this row's scope):

- The A3 sweep's flat fixture still draws no component node, so TC-118's
  sweep alone would not catch a flat legend that dropped it again; TC-508
  catches it. Giving that fixture a component endpoint would change a
  document every whole-document sweep reads, so it is left to its own row.
- The drill's component swatch states `var(--surface)` and `var(--border)`
  a second time beside its block's own `fill` and `stroke`. They are theme
  tokens, not a colour, and the drill is outside this row.

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, from
WI-1048's Deliverable. Since F-2 (WI-1022) the flat How-SW graph draws
component nodes, but its legend lists only module, file and external actor
(`rendering/traj_views.py`, the legend spans near lines 960 and 1315). A
reader meets a node kind the key does not name.

## Done-when

- [x] The flat graph's legend names every node kind it draws, the
      component node among them, with the swatch the node uses taken from
      the same token or class (no second copy of a colour).
- [x] A test fails when the graph draws a node kind its legend omits.
