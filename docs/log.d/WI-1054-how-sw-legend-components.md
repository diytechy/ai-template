## 2026-11-22 — WI-1054: The flat How-SW graph's legend names the component nodes it draws

Deferred open items: none. The row changes a renderer, a test module and
one new test case, and takes no operator decision; it needed no decisions
record.

Built on the maintenance branch `maint/wi-1054` from `3c33b3783`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1054-how-sw-legend-components.md`).

- **The legend:** both How-SW legends are built from one table of node-kind
  words beside `SW_NODE_FILL` in `rendering/traj_render.py`
  (`SW_NODE_LABEL`, read by `sw_legend`), each swatch the fill its nodes
  are drawn with. The flat graph's legend gains its component entry and its
  caption names the component node; the drill's legend reads byte for byte
  as before. `traj_views.py`'s SLOC fell 999 -> 987.
- **TC-508** (new, Drafted, Unit, Full; verifies SR-052 and LLR-113): the
  flat graph draws all four node kinds and its legend names each with its
  nodes' own fill, also when a kind's fill changes. Its test,
  `test_the_flat_graph_legend_names_every_node_kind_it_draws`, was red
  first on the missing component entry. No requirement text changed:
  LLR-113 already states the obligation the flat legend broke.
- **Tests:** the 35 modules reading the changed renderers, the RESYNC
  pack, the registries and the whole tree:
  `798 passed, 1 skipped, 18 warnings in 685.86s (0:11:25)`.
  `trace.py --strict`: `orphans=0 integrity=0`; `check_trajectory.py
  --strict`: clean. `run_menu.py smoke`:
  `3724 passed, 3 skipped, 18 warnings in 315.98s (0:05:15)`, with a CPU
  budget WARN only.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
  `test-cases.toml` +794, `RESYNC_PACK.md` +1,053.
- **Acts owed:** the first acceptance of TC-508. No amendment and no routed
  traced change to an `Accepted` row. Until that act, phase 3 reads
  DevStg-Tests live and `check_trajectory` warns that a `[3]-[DevStg-<rung>]`
  work item is due (advisory; the coordinator's call).
