+++
id = "WI-399"
title = "CONTAINMENT IS OWED WHERE A MODULE IS ADDED, NOT WHERE THE STATION REGENERATES THE INVENTORY. MECHANISM: docs/architecture.md is trunk-owned and its freshness step legitimately SKIPs on a claimed work branch (SR-133), so a NEW shipped module enters the arch-map inventory only when the station's refresh regenerates the map - AFTER the last review round - at which point an inventory module in no CMP-### component is a --strict ERROR that nobody in the lane could have seen, and the station is the FIRST place the red can exist. TWO DRIVEN INSTANCES of the class, identical two-registry-row remedies, each costing a review round and a station red: drive.py (WI-374 era) and handback.py (WI-387 - the 2026-08-01 blocking red, whose 'tested and refuted' hypothesis was in fact correct because the refuting probe measured a trunk-vintage map; handoff-2026-08-01.md §2 and §6). THE CONSTRAINT: make the lane's own bar owe the containment at the commit that ADDS the module, keyed off what the lane CAN see with no arch-map regeneration - the shipped-module set (bootstrap.py's MAPPING and the scripts dir) joined against the LLR Component cells - so the red surfaces beside the module's first commit and the station can never be the first to know. DONE-WHEN, driven at both ends: a lane-runnable check reds on a tree that adds a shipped module carrying no component tag and greens when the tag lands; and the station-first shape is reproduced by a test as the class this row closes (a module visible to the lane check but absent from a stale arch-map must still red the lane, which is exactly the wi-387 topology). SCOPE GUARD: this row narrows WHERE an existing rule fires; it invents no new containment policy, no new registry surface, and does not touch the station's own --strict behaviour, which stays as the backstop."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

**Built 2026-08-02 (commit 278eea0f; reworked same day under REVIEW-A, one
commit).** The knowledge⇒component containment rule now fires in the lane's
own bar at the commit that ADDS a shipped module — `check_trajectory.py`
`added_module_findings`, the fourth rule of `component_findings`. The
lane-visible shipped-module set is derived from the declared arch-map scan
root (`docs/stack.ini` `[paths] src` + `[arch-map] mode`) and mirrors
`gen_arch_map.build_map`'s symbol-mode collection EXACTLY: `*.py` under the
root (absolute or repo-relative, the path the generator would scan), the same
hidden/`__pycache__` skip, keys relative to the root's parent, and the same
symbol-emptiness skip (`_would_be_inventoried` — a module with no docstring
summary, no internal import, no `Contracts:` comment and no public symbol
never enters the MODULE MAP, so the delta never reds what the regeneration
could never absorb). Files mode is dormant by parity: a real files-mode map
has no `### ` module headers, `arch_inventory` reads it as empty, and the
whole containment family — station rule and early firing point alike — is off
there. The delta against the COMMITTED `arch_inventory` is joined through the
LLR `Component` cells exactly as the station rule joins; a delta module in no
real CMP is the same finding class at the same tier (WARN plain, ERROR under
`--strict`), same pack arming, same `docs/components-check: off` opt-out. A
fresh map empties the delta, so the station's own `--strict` behaviour is
untouched and stays the backstop — `docs/architecture.md` stays trunk-owned
and SR-133's freshness skip stands. The spec's MAPPING parenthetical resolved
to the declared scan root (MAPPING is kit-only; the scan root is the same
declaration in any adopter repo).

**Done-when, driven at both ends (watched red-then-green,
`tests/test_trajectory_arch.py`, 12 new tests):** a tree that adds a shipped
module with no component tag REDS the lane-runnable check and greens when the
tag lands; and the station-first class is reproduced as a test — a
stale-but-contained committed map plus an untagged on-disk module (the exact
wi-387 topology) reds the lane while the station rule itself is silent. Both
redded pre-implementation (2 failed, watched) and green under the fix, with
no-double-report, shared-arming, shared-opt-out, pre-arch-map-vacuity,
symbols-mode `*.py` scope and hidden-skip pinned beside them.

**REVIEW-A rework (2026-08-02, findings 1–3, one commit):** (1 MAJOR) the
first cut collected every non-hidden `*.py`, so a symbol-empty module (bare
`__init__.py`, comment-only, private-only) redded `--strict` and STAYED red
after the trunk regen forever — accidental new policy; fixed by mirroring
`build_map`'s emptiness predicate, and pinned DIFFERENTIALLY: `regen_map`
runs the REAL `gen_arch_map` over the fixture tree and the tests assert the
delta empties exactly when the regenerated map absorbs the module
(public-symbol module: lane red → regen absorbs → delta empty with the
station rule holding the same red → tag clears both; symbol-empty module:
green on BOTH sides). (2) the files-mode test pinned an unreachable state;
replaced with the honest dormancy/parity claim against a real
`--mode files` map. (3) an absolute `[paths] src` no longer remaps to a
silent repo-relative miss — it scans the path the generator would.

**Scope guard held:** no new containment policy, no new registry surface, no
station behaviour change; no module added, so no registration owed (the rule
is an internal of `component_findings`, LLR-049/SR-087). Bookkeeping with
reasons in place: `check_trajectory.py` size baseline 3261 → 3359 → 3428; the
stack.ini reads collapsed onto one `_stack_ini_get`, dissolving a sanctioned
dupe block (`docs/dupes-allow` `declared-file` 13 → 12), and the rework's
import-walk mirror sanctioned under the F5 `module-path` class (2 → 3),
drift-guarded by the differential tests.
<!-- fig: derived="baseline stamps in tests/test_module_size_ratchet.py and docs/dupes-allow at the rework commit, each carrying its reason" -->

**Verified 2026-08-02 on the rework tree (build 278eea0f + one rework
commit):** `tests/test_trajectory_arch.py` 57 passed in 1.28s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=this-rework-commit -->;
smoke 619 passed / 2 skipped in 9.98s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=this-rework-commit -->;
full suite at the build commit 1853 passed / 10 skipped in 282.47s (0:04:42)
<!-- fig: cmd="python -m pytest -q -n auto" rev=278eea0f -->;
`check_trajectory --strict` / `check_doc_refs --strict` / `check_figures
--strict` all rc=0 on the rework tree.
