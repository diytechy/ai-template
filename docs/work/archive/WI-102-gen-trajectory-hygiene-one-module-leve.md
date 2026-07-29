+++
id = "WI-102"
title = "gen_trajectory hygiene - one module-level _esc + SVG node titles (M4/L7)"
workstream = "scripts"
order = 101
+++

## Deliverable

M4: gen_trajectory.py redefined the identical HTML-escape closure 7× (nested `def esc`) alongside a module-level `_esc` — plain within-module copy-paste (F5 licenses cross-script dup, not this). Consolidated to ONE module-level helper: renamed `_esc`->`esc` (def + 11 call sites) so the 65 existing bare `esc(` calls bind to it, deleted the 7 closures; left the unrelated embedded client-side JS `esc()` untouched (regenerated dashboard is byte-identical bar the asof-commit stamp). L7: added a `<title>` tooltip child to every SVG node across all 4 emitters (icicle cell, When-DAG WI node, How-SW containment box, OKF knode) — id + label/status/kind — a hover/a11y win (414 titles now render). Updated the one test whose regex assumed `<rect>` immediately followed the node `<g>`. No spine change (G3). Full suite 702 passed.
