#!/usr/bin/env python3
"""The inputs the architecture rules read: registries, dials, scan profile and inventory.

The registry paths, the two opt-out dials (`[checks] interfaces_check` and
`[checks] components_check`), the interface and component row loaders, the
declared arch-map scan profile and the live source inventory. The rule
modules beneath ``trajectory_arch`` (`arch_interfaces`, `arch_tags`,
`arch_seams`, `arch_components`) read each of them from here, so every
architecture rule sees one reading of each input, and ``trajectory_arch``
re-exports them for ``check_trajectory``.

Contracts: IF-316 — the interface seam this file declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-316: the architecture rules' shared inputs. `load_ifs(rows)` and
`load_seams(root)` give the real interface rows, each resolved into its
`owner` and its far side; `load_cmps(rows)` gives the real component rows;
`arch_inventory(root)` gives the module names, their `Contracts:`
declarations and their internal imports under the declared scan root, empty
where that root is absent, the scan is files mode, or `gen_arch_map` is not
beside this script; `_arch_scan_profile(root)` gives the `(src, mode)` it
scans; `read_interfaces_check_enabled(root)` and
`read_components_check_enabled(root)` read the two opt-out dials, on by
default. The registry paths are repository-relative constants. Every reader is
lenient, and none writes.
"""

import re
import sys
from pathlib import Path

try:
    from kitlib import config as _kitconfig
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import config as _kitconfig
    from kitlib import spine as _kitspine

try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

try:
    import gen_arch_map
except ImportError:
    try:  # pragma: no cover - in-process fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import gen_arch_map
    except ImportError:
        gen_arch_map = None


_first_declared_line = _kitconfig.first_declared_line
_process_check = _kitconfig.process_check
_split_refs = _kitspine.refs

TC_CSV = "docs/test/test-cases.toml"
IF_CSV = "docs/requirements/interfaces.toml"
LLR_CSV = "docs/requirements/low-level-requirements.toml"
CMP_CSV = "docs/requirements/components.toml"
SPECS_DIR = "docs/specs"

# An IF-### interface-seam id token (process.md §8). Matched word-bounded so a
# `Contracts: IF-003, IF-004` docstring line (harvested into the arch-map) or an
# id cell yields each id cleanly.
IF_ID_RE = re.compile(r"IF-\d+")
# A CMP-### component id token (process-options.md "Component layer"). trace.py
# owns CMP integrity; this loader is lenient (skips a malformed id) — it only
# feeds the warn-first top-view coverage.
CMP_ID_RE = re.compile(r"^CMP-\d+$")


def read_interfaces_check_enabled(root):
    """Whether the architecture-connectivity coverage warns are on (S5/WI-056).
    `docs/process.toml` `[checks] interfaces_check = false` opts out; else
    (migration window) `docs/interfaces-check` with the one word `off`; absent
    or any other value reads on — the ruled opt-out, default-on posture (same
    shape as `trajectory_check`). Default-on means the coverage warn fires even
    with an empty/absent `interfaces.csv`; the off-switch or a ≤1-module
    inventory is the only silence."""
    declared = _process_check(root, "interfaces_check")
    if declared is not None:
        return declared
    return (
        _first_declared_line(root / "docs" / "interfaces-check") or ""
    ).lower() != "off"


def read_components_check_enabled(root):
    """Whether the How-SW top-view right-sizing rule is on (WI-073/FB5).
    `docs/process.toml` `[checks] components_check = false` opts out; else
    (migration window) `docs/components-check` with the one word `off`; absent
    or any other value reads on — the ruled opt-out, default-on posture (same
    shape as `interfaces_check`)."""
    declared = _process_check(root, "components_check")
    if declared is not None:
        return declared
    return (
        _first_declared_line(root / "docs" / "components-check") or ""
    ).lower() != "off"


# Source-file extensions stripped when normalizing a module path, so the arch-map
# name (`scripts/check`), an LLR `Module` cell and an IF endpoint written with
# the full repo path (`project-trajectory/scripts/check.py`) collapse to one key.
# ONE HOME since WI-448 slice 4 (`kitlib.spine`), which also retired the false
# claim this comment carried: it promised the tuple was "kept in sync with
# trace.py._MODULE_EXTS", and `trace.py` has no such name — the sync partner
# named here did not exist. The real second copy was `gen_arch_map.py`'s.
_MODULE_EXTS = _kitspine.MODULE_EXTS
_norm_module = _kitspine.norm_module


def load_ifs(rows):
    """Real (non-`-000`) IF-### interface rows as dicts, each already RESOLVED
    into its two sides — `owner` (one endpoint, possibly `''`) and the far side
    as `requestors` / `consumers` (lists; exactly one is meant to be set — the
    key name is the direction) plus `far`, whichever of the two it is. Lenient — `trace.py` owns IF integrity (malformed ids, owner
    shape); this loader only feeds the warn-first coverage views, so a
    malformed id is simply skipped here.

    `approval` is the tier's ONE maturity field. It replaced `stability` at
    WI-442, which had itself replaced `status` at WI-443 — the same defect twice
    (two columns on one row meaning different kinds of "settled"), fixed the same
    way. `direction`/`this_project`/`counterpart` went at WI-455 (OI-60 ruled
    (a)): flow is no longer a column but the shape of the row, so RESOLUTION
    happens here, once, and every view downstream (the connectivity credit in
    `arch_interfaces`, the declared pairs in `arch_seams`, `traj_views`' seam
    graphs) reads the same two keys instead of re-deriving the orientation
    from a flag. Since OI-67 the owner side is the row's own `owner` cell, one
    spelling, nothing derived."""
    out = []
    for r in rows:
        iid = (r.get("IF-ID") or "").strip()
        if not IF_ID_RE.fullmatch(iid) or iid.endswith("-000"):
            continue
        out.append(
            {
                "id": iid,
                "owner": _kitspine.seam_owner(r),
                "requestors": _kitspine.seam_requestors(r),
                "consumers": _kitspine.seam_consumers(r),
                "far": _kitspine.seam_far_side(r)[1],
                "approval": (r.get("Status") or "").strip().lower(),
                "notes": (r.get("Notes") or "").strip().lower(),
            }
        )
    return out


def load_seams(root):
    """`load_ifs` over the live registry — the one call every seam view makes."""
    return load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))


def arch_inventory(root):
    """`(module_names, {module: {IF ids}}, {module: {imported stems}})` derived
    STRAIGHT from the source tree under the declared arch-map scan root
    (`[paths] src` + `[arch-map] mode`, the same profile check.py reads),
    through `gen_arch_map.scan_inventory` — the one AST walk the map's
    consumers share. Until WI-455 (sitting-2 decision 8) this parsed the
    committed MODULE MAP block back out of `docs/architecture.md`; the
    registries→dashboard re-pointing retired that way-station, so the
    inventory is now the LIVE tree — on a work branch too, which is what
    dissolved the WI-399 committed-vs-disk delta rule (`shipped_modules` and
    the station-first firing gap died with it). `module_names` keep the map's
    grammar (`scripts/check`-style keys relative to the scan root's parent);
    the IF map carries each module's `Contracts: IF-###` docstring
    declarations; the import map carries the internal-import names — the
    cross-CMP rule's edge source (WI-064). Empty when the root is absent,
    files-mode (no parser), or `gen_arch_map` is not beside this script, so
    the coverage layers stay vacuous exactly where the committed map was.

    Implements: SR-159, LLR-067
    """
    if gen_arch_map is None:
        return set(), {}, {}
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return set(), {}, {}
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    names, contracts, imports = [], {}, {}
    for rel, _summary, imps, cons, _rows in gen_arch_map.scan_inventory(
        [src_dir], strict=False
    ):
        names.append(rel)
        if cons:
            contracts.setdefault(rel, set()).update(cons)
        if imps:
            imports.setdefault(rel, set()).update(imps)
    return set(names), contracts, imports


def load_cmps(rows):
    """Real (non-`-000`) CMP-### component rows as dicts (id, name, category,
    partof). Lenient — `trace.py` owns CMP integrity; a malformed id is skipped
    here, since this only feeds the warn-first top-view coverage."""
    out = []
    for r in rows:
        cid = (r.get("CMP-ID") or "").strip()
        if not CMP_ID_RE.match(cid) or cid.endswith("-000"):
            continue
        out.append(
            {
                "id": cid,
                "name": (r.get("Name") or "").strip(),
                "category": (r.get("Category") or "").strip(),
                "partof": [p for p in _split_refs(r.get("PartOf", "")) if p],
            }
        )
    return out


# --- the declared arch-map scan profile -------------------------------------
# (The WI-399 committed-vs-disk delta machinery that lived here —
# _has_internal_import / _would_be_inventoried / shipped_modules /
# added_module_findings — RETIRED at WI-455: arch_inventory reads the live
# source tree, so the delta it bridged no longer exists.)


def _stack_ini_get(root, section, option):
    """ONE lenient docs/stack.ini read (absent file / unreadable or broken
    profile / missing option all → None), shared by `_arch_scan_profile` and
    `_tests_dir` so the idiom has a single home here — check.py owns the loud
    reading of the same profile, and `kitlib.config.read_stack_ini` the parse."""
    try:
        cp = _kitconfig.read_stack_ini(Path(root) / _kitconfig.STACK_INI)
    except _kitconfig.StackIniError:
        return None
    if cp is None or not cp.has_option(section, option):
        return None
    return cp.get(section, option).strip()


def _arch_scan_profile(root):
    """`(src, mode)` from docs/stack.ini — the same `[paths] src` and
    `[arch-map] mode` check.py hands gen_arch_map — read leniently
    (`_stack_ini_get`): an absent or broken profile degrades to the defaults
    (`src`, `symbols`) rather than crashing a warn-tier rule."""
    return (
        _stack_ini_get(root, "paths", "src") or "src",
        _stack_ini_get(root, "arch-map", "mode") or "symbols",
    )
