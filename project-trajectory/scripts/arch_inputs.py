#!/usr/bin/env python3
"""The inputs the architecture rules read: registries, dials, scan profile and inventory.

The registry paths, the two opt-out dials (`[checks] interfaces_check` and
`[checks] components_check`), the interface and component row loaders, the
declared arch-map scan profile and the live source inventory. The rule
modules beneath ``trajectory_arch`` (`arch_interfaces`, `arch_tags`,
`arch_seams`, `arch_components`) read each of them from here, so every
architecture rule sees one reading of each input, and ``trajectory_arch``
re-exports them for ``check_trajectory``.

Component: CMP-006

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
default; `component_headers(root)` gives each in-scope file's `Component:`
declaration and the census's findings, `({}, [])` with no live component
row; `implements_index(root)` gives `{spine id: [file, ...]}` from the
`Implements:` tags on that same surface, `{}` with none. The registry paths
are repository-relative constants. Every reader is lenient, and none writes.
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


def _component_scope(root):
    """`(scoped, other, missing)`: the files owing a `Component:` declaration
    and the files of another type under `[paths] src`, each `{repository-
    relative path: path}`, and the declared header paths that are not files.
    The scope is closed: every file under the declared source root of a type
    the grammar has a carrier for, `README.md` excluded, and every file
    `docs/stack.ini` `[arch-map] headers` lists (`kitlib.config.declared_headers`),
    the one scan surface the contract scan reads too. A path part that is
    hidden or a bytecode cache is not source.

    Implements: SR-159, LLR-397"""
    src, _mode = _arch_scan_profile(root)
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    scoped_paths, other_paths = gen_arch_map.source_files(src_dir)
    scoped = {_rel_to(root, p): p for p in scoped_paths}
    other = {_rel_to(root, p): p for p in other_paths}
    found, missing = _kitconfig.declared_headers(root)
    for _rel, path in found:
        scoped.setdefault(_rel_to(root, path), path)
    return scoped, other, missing


def _rel_to(root, path):
    """`path` relative to `root` in forward slashes, or whole when outside it."""
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()


def component_headers(root):
    """`(declared, findings)`: each in-scope file's component as its header
    declares it (`{repository-relative path: CMP id}`), and one finding per
    in-scope file whose declaration is absent, doubled, malformed or names an
    id no live component row has, and one per declared header path that is
    not a file, each naming the file. A file of another
    type under `[paths] src` is outside the rule unless its header states a
    `Contract IF-###:` body, which is then a finding naming its type. A file
    outside the scope may carry a declaration, read by the same reader where
    it is read; nothing here walks for it.

    THE MEMBERSHIP INPUT. A file absent from `declared` belongs to no
    component, so every rule reading membership treats it as unclassified,
    never as internal or exempt. Vacuous, `({}, [])`, with no live component
    row: below DevStg-Arch there is no partition to declare into.

    Implements: SR-159, LLR-397
    """
    root = Path(root)
    if gen_arch_map is None or not hasattr(gen_arch_map, "file_component"):
        return {}, []
    live = {c["id"] for c in load_cmps(spine_carrier.load(root / CMP_CSV, "CMP-ID"))}
    if not live:
        return {}, []
    scoped, other, missing = _component_scope(root)
    declared = {}
    findings = [
        "{}: is listed in {} [arch-map] headers and is not a file".format(
            rel, _kitconfig.STACK_INI
        )
        for rel in missing
    ]
    for rel, path in sorted(scoped.items()):
        component, problem = gen_arch_map.file_component(path)
        if problem is None and component not in live:
            problem = "declares {}, which no live component row in {} has".format(
                component, CMP_CSV
            )
        if problem is None:
            declared[rel] = component
        else:
            findings.append("{}: {}".format(rel, problem))
    for rel, path in sorted(other.items()):
        if gen_arch_map.states_contract_body(path):
            findings.append(
                "{}: states a contract body, and a `{}` file has no "
                "`Component:` carrier (the grammar covers {})".format(
                    rel,
                    path.suffix,
                    ", ".join(
                        sorted(t or "no suffix" for t in gen_arch_map.COMPONENT_TYPES)
                    ),
                )
            )
    return declared, [
        "{} — every file in the component scope names its one component in "
        "its header (process.md §8)".format(f)
        for f in findings
    ]


def implements_index(root):
    """`{spine id: [file, ...]}`: every file whose literal `Implements:` line
    names the id, repository-relative and sorted. THE ONE INDEX the readers of
    a design row's realization read, since a row names no file (WI-1023): it is
    generated from the tags in the code, which point up, and never authored.

    The surface is the declared source root (`[paths] src`) and the files
    `[arch-map] headers` lists, the one scan surface the contract scan and the
    component census read. Read as text through the one declaration grammar
    (`gen_arch_map.scan_backlinks`), so it holds in `files` mode and in any
    language. `{}` with no source root, or without `gen_arch_map` beside this
    script. Back-links stay encouraged, never obliged: a row no tag names is
    simply absent.

    Implements: SR-250, LLR-405"""
    root = Path(root)
    if gen_arch_map is None:
        return {}
    src, _mode = _arch_scan_profile(root)
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    base = src_dir.parent if src_dir.name else src_dir
    found = {}
    for rid, paths in gen_arch_map.scan_backlinks([src_dir]).items():
        found.setdefault(rid, set()).update(_rel_to(root, base / p) for p in paths)
    headers, _missing = _kitconfig.declared_headers(root)
    for rel, path in headers:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for line in lines:
            for rid in gen_arch_map.backlink_ids(line):
                found.setdefault(rid, set()).add(_rel_to(root, path))
    return {rid: sorted(paths) for rid, paths in sorted(found.items())}


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
