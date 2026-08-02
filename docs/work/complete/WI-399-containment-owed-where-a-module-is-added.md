+++
id = "WI-399"
title = "CONTAINMENT IS OWED WHERE A MODULE IS ADDED, NOT WHERE THE STATION REGENERATES THE INVENTORY. MECHANISM: docs/architecture.md is trunk-owned and its freshness step legitimately SKIPs on a claimed work branch (SR-133), so a NEW shipped module enters the arch-map inventory only when the station's refresh regenerates the map - AFTER the last review round - at which point an inventory module in no CMP-### component is a --strict ERROR that nobody in the lane could have seen, and the station is the FIRST place the red can exist. TWO DRIVEN INSTANCES of the class, identical two-registry-row remedies, each costing a review round and a station red: drive.py (WI-374 era) and handback.py (WI-387 - the 2026-08-01 blocking red, whose 'tested and refuted' hypothesis was in fact correct because the refuting probe measured a trunk-vintage map; handoff-2026-08-01.md §2 and §6). THE CONSTRAINT: make the lane's own bar owe the containment at the commit that ADDS the module, keyed off what the lane CAN see with no arch-map regeneration - the shipped-module set (bootstrap.py's MAPPING and the scripts dir) joined against the LLR Component cells - so the red surfaces beside the module's first commit and the station can never be the first to know. DONE-WHEN, driven at both ends: a lane-runnable check reds on a tree that adds a shipped module carrying no component tag and greens when the tag lands; and the station-first shape is reproduced by a test as the class this row closes (a module visible to the lane check but absent from a stale arch-map must still red the lane, which is exactly the wi-387 topology). SCOPE GUARD: this row narrows WHERE an existing rule fires; it invents no new containment policy, no new registry surface, and does not touch the station's own --strict behaviour, which stays as the backstop."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

**Built 2026-08-02 (commit 278eea0f).** The knowledge⇒component containment
rule now fires in the lane's own bar at the commit that ADDS a shipped module —
`check_trajectory.py` `added_module_findings`, the fourth rule of
`component_findings`. The lane-visible shipped-module set is derived from the
declared arch-map scan root (`docs/stack.ini` `[paths] src` + `[arch-map]
mode` — the exact inventory `gen_arch_map` reads: `*.py` in symbols mode,
every non-hidden source file in files mode, the same hidden/`__pycache__`
skip, keys relative to the root's parent), and the delta against the COMMITTED
`arch_inventory` is joined through the LLR `Component` cells exactly as the
station rule joins. A delta module in no real CMP is the same finding class at
the same tier (WARN plain, ERROR under `--strict`), same pack arming, same
`docs/components-check: off` opt-out. A fresh map empties the delta, so the
station's own `--strict` behaviour is untouched and stays the backstop —
`docs/architecture.md` stays trunk-owned and SR-133's freshness skip stands.
The spec's MAPPING parenthetical resolved to the declared scan root (MAPPING
is kit-only; the scan root is the same declaration in any adopter repo).

**Done-when, driven at both ends (watched red-then-green,
`tests/test_trajectory_arch.py`, 9 new tests):** a tree that adds a shipped
module with no component tag REDS the lane-runnable check and greens when the
tag lands; and the station-first class is reproduced as a test — a
stale-but-contained committed map plus an untagged on-disk module (the exact
wi-387 topology) reds the lane while the station rule itself is silent. Both
redded pre-implementation (2 failed, watched) and green under the fix, with
no-double-report, shared-arming, shared-opt-out, pre-arch-map-vacuity,
symbols/files-mode scope and hidden-skip pinned beside them.

**Scope guard held:** no new containment policy, no new registry surface, no
station behaviour change; no module added, so no registration owed (the rule
is an internal of `component_findings`, LLR-049/SR-087). Bookkeeping with
reasons in place: `check_trajectory.py` size baseline 3261 → 3359; the
stack.ini reads collapsed onto one `_stack_ini_get`, dissolving a sanctioned
dupe block (`docs/dupes-allow` `declared-file` 13 → 12).
<!-- fig: derived="baseline stamps in tests/test_module_size_ratchet.py and docs/dupes-allow at 278eea0f, each carrying its reason" -->

**Verified 2026-08-02 on 278eea0f:** `tests/test_trajectory_arch.py` 54 passed
in 1.15s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=278eea0f -->;
smoke 615 passed / 6 skipped in 10.42s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=278eea0f -->;
full suite 1853 passed / 10 skipped in 282.47s (0:04:42)
<!-- fig: cmd="python -m pytest -q -n auto" rev=278eea0f -->;
`check_trajectory --strict` / `check_doc_refs --strict` / `check_figures
--strict` all rc=0.
