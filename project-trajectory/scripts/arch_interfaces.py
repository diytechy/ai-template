#!/usr/bin/env python3
"""Interface-registry rules: seam connectivity, contract bodies and seam-TC coverage.

Three rules over `docs/requirements/interfaces.toml` and the `Contracts:`
declarations in the source tree: connectivity coverage
(`interface_findings`, warn-first), the armed definition gate
(`contract_body_findings`), and seam-TC coverage with its migration allowlist
`docs/if-tc-coverage-allow` (`if_tc_coverage_findings`, and the allowlist's
hygiene and parse rules). Their inputs come from `arch_inputs`;
``trajectory_arch`` re-exports them for ``check_trajectory``.

Component: CMP-006

The rule surface ``trajectory_arch`` re-exports: each rule takes a repository
root and returns finding strings, `[]` when `[checks] interfaces_check =
false` or its input is vacuous: `interface_findings`,
`contract_body_findings`, `unchecked_contract_rows`,
`if_tc_coverage_findings`, `if_tc_allow_hygiene_findings` and
`if_tc_allow_parse_findings`. `parse_if_tc_allow(text)` gives the
allowlist's entries and its declared seed count, and `read_if_tc_allow(root)`
the ids it exempts with their reasons. `contract_homes(root)` gives the one
file stating each interface's body, for the interface-form gate's reach. The
caller decides each finding's severity, and the module performs no writes.
"""

import ast
import re
import sys
from pathlib import Path

try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

from arch_inputs import (
    IF_CSV,
    IF_ID_RE,
    TC_CSV,
    _arch_scan_profile,
    _norm_module,
    _rel_to,
    arch_inventory,
    component_headers,
    load_ifs,
    load_seams,
    read_interfaces_check_enabled,
)
from kitlib import spine as _kitspine

try:
    import gen_arch_map
except ImportError:
    try:  # pragma: no cover - in-process fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import gen_arch_map
    except ImportError:
        gen_arch_map = None


# The seam-TC coverage migration allowlist (OI-43 ruled (a), WI-488) — see
# `read_if_tc_allow`.
IF_TC_ALLOW = "docs/if-tc-coverage-allow"
# The allowlist's machine-readable baseline: how many of its entries are the
# SEEDED population (which shares one reason, stated once in the header). Past
# that count an entry is an addition and must carry its own ` — <reason>`.
IF_TC_SEED_RE = re.compile(r"^#\s*seed-count:\s*(\d+)\s*$")


def _contracts_grammar_findings(root):
    """Marker-grammar findings over the declared scan root, or `[]` where the
    tree cannot be read.

    Degrades to silence on a missing `gen_arch_map`, files-mode or an absent
    scan root, exactly as `arch_inventory` does — a detector that crashed in a
    scaffold would be removed from the floor, which is the same outcome as not
    having it."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "contracts_grammar_findings"):
        return []
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return []
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    if not src_dir.is_dir():
        return []
    found = []
    for path in sorted(src_dir.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        found.extend(
            gen_arch_map.contracts_grammar_findings(path.name, tree, text.splitlines())
        )
    # The header files — non-Python scripts, registries, config, hooks — read
    # through the same grammar (OI-67 slice 2), so a lossy marker is named too.
    if hasattr(gen_arch_map, "file_grammar_findings"):
        for label, path in _header_files(root):
            found.extend(gen_arch_map.file_grammar_findings(label, path))
    return found


def _header_files(root):
    """`gen_arch_map.header_files` over the declared surface: the non-Python
    files under the source root and the files `[arch-map] headers` lists; `[]`
    when the generator is absent or predates the declared surface."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "header_files"):
        return []
    src, _mode = _arch_scan_profile(root)
    return gen_arch_map.header_files(
        root, [root / src.strip().replace("\\", "/").rstrip("/")]
    )


def _header_declarations(root, out):
    """`{label: {IF ids}}` declared by the header files; a header the grammar
    refuses is reported into `out` and read as declaring nothing."""
    declared = {}
    for label, path in _header_files(root):
        try:
            ids, _bodies = gen_arch_map.file_contracts(path)
        except gen_arch_map.ContractsGrammarError as exc:
            out.append("{}: {}".format(label, exc))
            continue
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue  # the reference's own "could not read" list
        if ids:
            declared[label] = set(ids)
    return declared


def interface_findings(root):
    """Architecture-connectivity coverage warns (S5/WI-056; process.md §8), all
    warn-first — the caller prints them and they never change the exit code, at
    any gate. Returns the warn strings ([] when opted out or vacuous). A row
    names components, so connectivity is judged per component
    (`_component_connectivity`); the uncited-seam count, the marker grammar
    and a `Contracts:` id naming no row are reported beside it.

    Ruled opt-out, default-on: fires even with an empty/absent `interfaces.csv`
    (a multi-module arch-map with no declared seams reads "connectivity
    undeclared"); silenced only by `[checks] interfaces_check = false` or a ≤1-module
    inventory (nothing to connect).

    Implements: SR-159, LLR-042
    """
    if not read_interfaces_check_enabled(root):
        return []
    inventory, declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []  # nothing to connect (or no arch-map yet) — vacuous
    ifs = load_seams(root)
    out = []
    if not ifs:
        return [
            "connectivity undeclared: the {}-module architecture declares no "
            "interfaces — add IF-### rows to {}, or set docs/process.toml "
            "[checks] interfaces_check = false".format(len(inventory), IF_CSV)
        ]

    out.extend(_component_connectivity(root, inventory, ifs))

    # Seam-TC citation: each declared IF id should be cited by >=1 TC (the rung-2
    # seam-TC rule, and process.md §8's "every interface is backed by an SR and a
    # contract/fixture test").
    #
    # THE ARMING KEY HAS NOW MOVED TWICE, AND THE THIRD SPELLING IS "ALL ROWS".
    # It first read `Status == Active`, which armed EXACTLY the 5 rows already
    # TC-cited — zero findings by construction. WI-443 re-keyed it to
    # `Stability == Stable` (103 of 108 uncited). WI-442 retired `Stability` for
    # `Approval`, and copying the shape forward as `Approval == "approved"` would
    # have reproduced the ORIGINAL tautology in a new column: every row reads
    # `draft` today, so the rule would arm on nothing and report a clean zero.
    #
    # So it arms on EVERY real IF row, and the maturity column drops out of the
    # rule entirely. That is the honest reading of the obligation anyway — an
    # interface is backed by a contract test or it is not; how settled its
    # contract is was never the question — and it is the one spelling that cannot
    # be silently disarmed by a vocabulary change.
    #
    # SUMMARISED, not one line per row, and that is a deliberate ergonomic choice
    # rather than a softening: this function runs in the shipped pre-commit hook,
    # where 103 warn lines is a check nobody reads and therefore a check that does
    # not work. One line carries the count, which is the number that has to fall.
    #
    # STAYS PURE WARN-FIRST, FOREVER, EVEN UNDER --strict — the promotable half
    # split off at WI-488 (OI-43 ruled (a)) into `if_tc_coverage_findings` below,
    # which reports only the seams NOT on the migration allowlist. This line keeps
    # reporting the TOTAL uncited count (allowlisted seams included) so the whole
    # debt stays visible even once the actionable subset goes quiet.
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    uncited = [r["id"] for r in ifs if r["id"] not in tc_cited]
    if uncited:
        shown = ", ".join(uncited[:5])
        out.append(
            "{} IF seam(s) are cited by no TC (a seam should carry a "
            "contract/fixture test, process.md §8){}: {}".format(
                len(uncited), " — first 5" if len(uncited) > 5 else "", shown
            )
        )

    # Marker-grammar honesty (OI-66): the `Contracts:` marker must OPEN its line
    # and parse as an id list, which is what stops prose that DENIES a
    # declaration from making one. Tightening a shipped grammar may not lose an
    # adopter's seams in silence, so both lossy forms — a marker-shaped line
    # whose id list will not parse, and a `Contracts:` carrying ids mid-line —
    # are reported by name. Warn-first: on this repo the count is zero, and on
    # an upgrading repo it is the migration list.
    out.extend(_contracts_grammar_findings(root))

    # Docstring citation: a `Contracts: IF-###` a script or header declares must
    # exist in the registry. Where a row's body sits, and that there is one, is
    # the definition gate's (`contract_body_findings`).
    registry_ids = {r["id"] for r in ifs}
    file_declared = _header_declarations(root, out)
    for module, ids in sorted(declared_contracts.items()):
        for iid in sorted(ids - registry_ids):
            out.append(
                "module {!r} docstring declares Contracts: {} but no such IF-### "
                "row exists".format(module, iid)
            )
    for owner, ids in sorted(file_declared.items()):
        for iid in sorted(ids - registry_ids):
            out.append(
                "{!r} header declares Contracts: {} but no such IF-### row "
                "exists".format(owner, iid)
            )
    return out


def _component_connectivity(root, inventory, ifs):
    """The connectivity warns over components: each component holding an
    inventory module by its header that no row names, that owns no row (no
    Provides) or that is on no row's far side (no Consumes). The `source` and
    `sink` valves (a FIRST word in Notes) mark the owner and the far side
    deliberate, so neither breeds a boilerplate opposite-facing row.

    Implements: SR-159, LLR-042
    """
    members = _component_members(root, inventory)
    named, provides, consumes = _seam_roles(ifs)
    out = []
    for cid in sorted(members):
        if cid not in named:
            out.append(
                "connectivity undeclared: component {!r} holds {} inventory "
                "module(s) and no IF-### row names it".format(cid, members[cid])
            )
            continue
        if cid not in consumes:
            out.append(
                "component {!r} declares no Consumes seam (mark it `source` in its "
                "IF row Notes if it deliberately consumes nothing)".format(cid)
            )
        if cid not in provides:
            out.append(
                "component {!r} declares no Provides seam (mark it `sink` in its IF "
                "row Notes if it deliberately provides nothing)".format(cid)
            )
    return out


def _component_members(root, inventory):
    """`{CMP id: number of inventory modules}` by the modules' headers."""
    declared = component_headers(root)[0]
    mod_cmps = _kitspine.module_components(
        {path: cid for path, cid in declared.items() if path.endswith(".py")}
    )
    members = {}
    for module in inventory:
        for cid in mod_cmps.get(_norm_module(module), ()):
            members[cid] = members.get(cid, 0) + 1
    return members


def _seam_roles(ifs):
    """`(named, provides, consumes)` endpoint sets over the rows: every
    endpoint a row names; each owner, and each far side marked `sink`; each
    far side, and each owner marked `source`."""
    named, provides, consumes = set(), set(), set()
    for r in ifs:
        named.update([r["owner"]] + r["far"])
        provides.add(r["owner"])
        consumes.update(r["far"])
        marker = r["notes"].split()
        first = marker[0].rstrip(":;,.") if marker else ""
        valve = {"source": (consumes, [r["owner"]]), "sink": (provides, r["far"])}
        if first in valve:
            valve[first][0].update(valve[first][1])
    return named, provides, consumes


# --- the armed definition gate (OI-67 slice 6) --------------------------------


def _declaration_sites(root):
    """`({path: (label, ids, bodies, component)}, problems)` — every file on
    the scan surface that declares a seam, read through the one harvester the
    interface reference uses (`gen_arch_map.scan_contracts`): the modules under
    the declared scan root and the header files (`_header_files`), each keyed
    by its repository path, with the component its `Component:` header declares
    (`component_headers`; None for a file with no valid declaration).
    `problems` is `[(label, message)]` for every header the contract GRAMMAR
    refused, so a refusal is reported rather than read as "declares nothing"
    and never DISARMS the gate (adversarial review 2026-08-29, F1); a refused
    source is absent from the sites. A source the scan could not READ is the
    reference's own "could not read" list, not a problem here. `(None,
    problems)` when there is no surface to read — files-mode, an absent scan
    root, no generator beside this script (`_no_surface_reason`)."""
    if _no_surface_reason(root):
        return None, []
    src, _mode = _arch_scan_profile(root)
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    headers = dict(_header_files(root))
    refused = []
    records, _unreadable = gen_arch_map.scan_contracts(
        [src_dir], sorted(headers.items()), grammar_errors=refused
    )
    declared = component_headers(root)[0]
    sites = {}
    for label, _summary, ids, bodies in records:
        path = headers.get(label) or src_dir.parent / (label + ".py")
        rel = _rel_to(root, path)
        sites[rel] = (label, set(ids), set(bodies), declared.get(rel))
    return sites, refused


def _no_surface_reason(root):
    """Why `_declaration_sites` has no surface to read, or None when it has
    one: files-mode, an absent scan root, or no generator beside this
    script."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "scan_contracts"):
        return "gen_arch_map.py is not beside this script"
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return "[arch-map] mode = files reads no source headers"
    if not (root / src.strip().replace("\\", "/").rstrip("/")).is_dir():
        return "the scan root {!r} is absent".format(src.strip())
    return None


def unchecked_contract_rows(root):
    """One line naming how many IF rows the armed definition gate
    (`contract_body_findings`) passed without judging, and why; `[]` when it
    judged them all or the gate is opted out. Every row, where there is no
    surface to read; otherwise each `external:`-owned row whose far side names
    no component a body's file could declare. Warn-only: it changes no
    verdict, it only stops a vacuous pass reading as a checked one."""
    if not read_interfaces_check_enabled(root):
        return []
    rows = load_seams(root)
    why = _no_surface_reason(root)
    if why is None:
        why = "external-owned, and no component on the far side to state them"
        rows = [
            r
            for r in rows
            if r["owner"].startswith("external:")
            and all(e.startswith("external:") for e in r["far"])
        ]
    if not rows:
        return []
    return ["contract bodies not checked for {} IF row(s): {}".format(len(rows), why)]


def contract_body_findings(root):
    """THE ARMED DEFINITION GATE: one body per interface, in a file of the
    right component (variant F, revision 35). Returns finding strings; the
    caller prints them WARN plain and promotes them to ERROR under `--strict`,
    the `if_tc_coverage_findings` idiom, sharing its `[checks]
    interfaces_check` opt-out.

    THE SURFACE is the shipped scripts under `[paths] src` and the files
    `docs/stack.ini` `[arch-map] headers` lists (configuration files, registry
    headers); nothing else is read, so a body quoted in a review record, a
    plan, the approval snapshot or an example document is never a second one.

    FOUR SHAPES. (1) Uniqueness: at most one file states each `Contract
    IF-###:` body. Zero is valid — the row's `data` cell is the contract's home
    until code states it — and two or more is one finding naming every file.
    (2) Where a body exists, its file's `Component:` header names the row's
    owner; for an `external:`-owned row it names a component the row lists
    among its consumers or requestors, since the external party's header is not
    ours to write and that file holds OUR READING of the surface. (3) A file
    whose `Contracts:` marker declares an id it states no body for. (4) A
    source whose header the contract GRAMMAR refuses: its declared rows count
    as unstated, the refusal named once per source.

    Vacuous where there is no surface (files-mode, an absent scan root); an
    unreadable source is the reference's own list, not a finding here.

    Implements: SR-159, LLR-398
    """
    if not read_interfaces_check_enabled(root):
        return []
    sites, refused = _declaration_sites(root)
    if sites is None:
        return []
    out = [
        "{!r} declares seams but its header is refused by the contract "
        "grammar: {} — its declared rows count as unstated".format(label, msg)
        for label, msg in refused
    ]
    stating = {}
    for rel, (_label, ids, bodies, _cid) in sorted(sites.items()):
        for iid in sorted(ids - bodies):
            out.append(
                "IF {} is declared by {!r} but states no `Contract {}:` body "
                "there — a declaration with no definition".format(iid, rel, iid)
            )
        for iid in bodies:
            stating.setdefault(iid, []).append(rel)
    out.extend(_uniqueness_findings(stating))
    rows = {r["id"]: r for r in load_seams(root)}
    for iid, rels in sorted(stating.items()):
        if len(rels) == 1 and iid in rows:
            out.extend(_external_body_findings(rows[iid], rels[0], sites[rels[0]][3]))
    return out


def _uniqueness_findings(stating):
    """The uniqueness arm of `contract_body_findings`: `stating` is `{IF id:
    [repository paths stating its body]}`; one finding per id two or more
    files state.

    Implements: SR-159, LLR-398
    """
    return [
        "IF {} is stated by {} files ({}) — at most one file states an "
        "interface's `Contract {}:` body; a second copy is a second definition "
        "waiting to disagree".format(iid, len(rels), ", ".join(rels), iid)
        for iid, rels in sorted(stating.items())
        if len(rels) > 1
    ]


def _external_body_findings(row, rel, component):
    """The header arm of `contract_body_findings` for one row and the one file
    `rel` stating its body, whose header declares `component` (None for no
    valid declaration): a local owner must be that component; an
    `external:`-owned row's component must be on its far side.

    Implements: SR-159, LLR-398
    """
    owner, iid = row["owner"], row["id"]
    shown = component or "no component"
    if not owner.startswith("external:"):
        if component == owner:
            return []
        return [
            "IF {} is owned by {}, but its body sits in {!r}, whose header "
            "declares {} — the body's file belongs to the owner".format(
                iid, owner, rel, shown
            )
        ]
    if component in {e for e in row["far"] if not e.startswith("external:")}:
        return []
    return [
        "IF {} is owned by {!r}; its body sits in {!r}, whose header declares {}, "
        "which the row lists among neither its consumers nor its requestors — "
        "our reading of an external surface is stated by a file of a component "
        "that faces it".format(iid, owner, rel, shown)
    ]


def contract_homes(root):
    """`{IF id: repository path}`: the one file stating each interface's body,
    for every id exactly one file on the surface states; None with no surface
    (`files` mode, an absent scan root). The interface-form gate reaches a
    requirement through it (`assumption_rules.if_reached_srs`).

    Implements: SR-212, LLR-244
    """
    sites, _refused = _declaration_sites(root)
    if sites is None:
        return None
    stating = {}
    for rel, (_label, _ids, bodies, _cid) in sites.items():
        for iid in bodies:
            stating.setdefault(iid, []).append(rel)
    return {iid: rels[0] for iid, rels in stating.items() if len(rels) == 1}


# --- seam-TC coverage promotion + its migration allowlist (OI-43 ruled (a),
# WI-488) -------------------------------------------------------------------


def _parse_if_tc_allow_full(text):
    """`(entries, seed, unparsed)` — the whole parse, both halves, the
    `docs/provenance-allow` split (`trace.read_provenance_allow`): `entries`
    and `seed` are exactly `parse_if_tc_allow`'s return (kept as a separate,
    pinned-arity wrapper below since `tests/test_trajectory_arch.py` unpacks
    it as a 2-tuple); `unparsed` is `[(lineno, line)]` for every DECLARING
    line the grammar dropped — not blank, not a `#`-comment, and whose first
    token does not parse as an `IF-###` id — so a malformed entry is reported
    rather than silently read as an empty file
    (`if_tc_allow_parse_findings`)."""
    entries = []
    seed = None
    unparsed = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            m = IF_TC_SEED_RE.match(line)
            if m and seed is None:
                seed = int(m.group(1))
            continue
        head, _, reason = line.partition(" — ")
        token = head.split()[0] if head.split() else ""
        if IF_ID_RE.fullmatch(token):
            entries.append((token, reason.strip() or None))
        else:
            unparsed.append((lineno, line))
    return entries, seed, unparsed


def parse_if_tc_allow(text):
    """`([(id, reason-or-None), ...] in file order, declared seed count or
    None)` for one allowlist file's TEXT.

    The SEED COUNT is a machine-readable header key, `# seed-count: <int>`,
    naming how many of the entries below are the migration BASELINE — the
    population measured when the promotion was seeded, which shares one reason
    stated once in the header rather than repeated per line. Entries past that
    count are ADDITIONS, and an addition is a judgment someone made, so it
    carries its own ` — <reason>`. A file that declares no seed count has no
    baseline to grow past; every entry is then read as seeded, which is what an
    adopter's freshly-seeded file looks like before it has ever grown.

    `_parse_if_tc_allow_full` is the same parse plus the malformed-line half;
    this wrapper's 2-tuple return is pinned by
    `test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set`, so it stays
    exactly as it was rather than growing a third element."""
    entries, seed, _unparsed = _parse_if_tc_allow_full(text)
    return entries, seed


def read_if_tc_allow(root):
    """`{IF-### id: reason-or-None}` from `docs/if-tc-coverage-allow` — the
    seam-TC coverage migration allowlist. Absent file: empty dict.

    Grammar, deliberately the cheap kind: one non-blank, non-`#`-comment line
    per entry, the first whitespace-run-delimited token an `IF-###` id,
    optionally followed by ` — <reason>`. FAIL-SOFT IN THE LOUD DIRECTION, the
    `docs/provenance-allow` rule: a line whose first token does not parse as an
    IF-### id declares nothing and is dropped, so the worst a malformed entry
    can do is leave the finding it was meant to silence still reported — never
    the reverse.

    AN ADDITION BEYOND THE DECLARED SEED NEEDS A REASON, and a bare one
    SUPPRESSES NOTHING — the same fail-soft-loud direction. The 2026-08-21
    review measured why: a new seam fails `--strict`, and the one-line edit that
    greened it was appending its bare id, which was lexically indistinguishable
    from the 120 seeded lines and produced no hygiene signal, no test failure
    and no reason anyone could review. The list is a burn-down; growth has to
    cost a sentence."""
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return {}
    entries, seed = parse_if_tc_allow(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    out = {}
    for i, (token, reason) in enumerate(entries):
        if seed is not None and i >= seed and not reason:
            continue
        out[token] = reason
    return out


def if_tc_allow_growth(root):
    """`([(id, reason-or-None), ...], seed)` — the entries past the declared
    seed count, and that count (None when the file declares none)."""
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return [], None
    entries, seed = parse_if_tc_allow(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    return ([] if seed is None else entries[seed:]), seed


def if_tc_coverage_findings(root):
    """The PROMOTABLE half of seam-TC coverage (OI-43 ruled (a), WI-488): an IF
    seam cited by no TC — the rung-2 seam-TC rule `interface_findings` already
    reports informationally, in full — becomes an ERROR when it is NOT on the
    migration allowlist `docs/if-tc-coverage-allow`. Returns the finding
    string(s) ([] when clean or opted out); the caller prints them WARN plain
    and promotes them to ERROR under `--strict` (DevStg-Tests+), the
    `component_findings` idiom.

    THE ALLOWLIST IS A MIGRATION DEVICE, NOT A PERMANENT EXEMPTION SURFACE. It
    was seeded at the population measured when the ruling executed (the file's
    own header carries the exact count, command and revision) — the standing
    rule that no list edit makes a check pass (session-protocol skill §2) governs every
    entry: adding one to silence a genuinely NEW uncited seam is ACCEPTING what
    it measures, not laundering it, and should carry its own reason. An
    allowlisted seam still counts in `interface_findings`' total; it simply does
    not error here. `if_tc_allow_hygiene_findings` reports — never blocks — a
    listed seam that has since gained a TC, so a shrinking list (the declared
    burn-down) stays visible rather than silently absorbed.

    Opt-out shares `interface_findings`' `[checks] interfaces_check` dial —
    same data, same switch — AND its ≤1-module arch-map vacuity: the promoted
    rule must arm on no MORE than the warn it promotes, so a `files`-mode or
    single-module adopter that never saw this warn does not suddenly see this
    error. Widening scope is a second, unruled change riding a severity one.

    DELIBERATELY UNCLAIMED — this function declares no back-link at all.
    `LLR-042` (`SR-159`) is
    `Accepted`, and its own `detail` says the connectivity layer emits its
    findings "without changing exit status" — true of `interface_findings`,
    which this function does not touch, and now FALSE of the seam-TC rule this
    function promotes. Amending an Accepted cell overrides acceptance (the
    sitting's act, the SR-006/LLR-060 precedent, WI-473); minting a fresh
    Drafted LLR under `SR-159` was considered and declined for the same reason
    that session gave first — `SR-159` is phase 1, and a Drafted child would
    drag that phase's derived stage down as a side effect of unrelated work. So
    the built behaviour is ahead of its requirement on purpose, recorded as
    owed on WI-488's own spec rather than claimed here.
    """
    if not read_interfaces_check_enabled(root):
        return []
    inventory, _declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []  # nothing to connect — vacuous, the interface_findings gate
    ifs = load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))
    if not ifs:
        return []
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    allow = read_if_tc_allow(root)
    new_uncited = [
        r["id"] for r in ifs if r["id"] not in tc_cited and r["id"] not in allow
    ]
    if not new_uncited:
        return []
    shown = ", ".join(new_uncited[:5])
    return [
        "{} IF seam(s) have no citing TC and are not on the migration allowlist "
        "({}) — cite the seam from a TC, or add a reasoned entry to the "
        "allowlist (process.md §8; OI-43/WI-488){}: {}".format(
            len(new_uncited),
            IF_TC_ALLOW,
            " — first 5" if len(new_uncited) > 5 else "",
            shown,
        )
    ]


def if_tc_allow_hygiene_findings(root):
    """`docs/if-tc-coverage-allow` hygiene (WI-488) — WARN-ONLY, never the exit
    code, not even under `--strict`: unlike a NEW uncited seam, a STALE entry is
    never a defect to fix under pressure. Two shapes:

    - a listed seam has since gained a TC citation — burn-down PROGRESS, so
      pruning the entry is housekeeping, not a fix owed to a failing build;
    - a listed id resolves to no live IF-### row (retired/renumbered).

    Kept structurally apart from `if_tc_coverage_findings` so a shrinking
    allowlist can never itself be mistaken for a new finding, and so this
    class can never gate even by an unintended promotion of that function.
    Shares that function's ≤1-module arch-map vacuity: reporting a listed
    seam as stale is meaningless while the coverage rule it tracks never arms.

    DELIBERATELY UNCLAIMED — see `if_tc_coverage_findings`' own note on why no
    back-link declaration names `LLR-042` here.
    """
    if not read_interfaces_check_enabled(root):
        return []
    allow = read_if_tc_allow(root)
    grown, seed = if_tc_allow_growth(root)
    # `grown` is consulted for the early return too: an addition the reader
    # DROPPED (no reason) leaves `allow` empty while the file still grew, and
    # that is exactly the state most worth reporting.
    if not allow and not grown:
        return []
    inventory, _declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []
    ifs = load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))
    all_ids = {r["id"] for r in ifs}
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    out = []
    unknown = sorted(i for i in allow if i not in all_ids)
    if unknown:
        shown = ", ".join(unknown[:5])
        out.append(
            "{} {} entries name no live IF-### row (retired/renumbered){}: {}".format(
                len(unknown),
                IF_TC_ALLOW,
                " — first 5" if len(unknown) > 5 else "",
                shown,
            )
        )
    if grown:
        # GROWTH IS REPORTED EVEN WHEN EVERY ADDITION IS REASONED, because the
        # list's declared direction is DOWN. A reasoned addition is legitimate
        # and still worth a sitting's attention; an unreasoned one suppresses
        # nothing (see `read_if_tc_allow`) and is named here rather than
        # vanishing silently.
        unreasoned = [i for i, reason in grown if not reason]
        out.append(
            "{} {} entr{} stand past the declared seed of {} — the list is a "
            "burn-down, so growth is a sitting's business{}: {}".format(
                len(grown),
                IF_TC_ALLOW,
                "y" if len(grown) == 1 else "ies",
                seed,
                " ({} carr{} no reason and therefore suppress nothing)".format(
                    len(unreasoned), "ies" if len(unreasoned) == 1 else "y"
                )
                if unreasoned
                else "",
                ", ".join(i for i, _ in grown[:5]),
            )
        )
    stale = sorted(i for i in allow if i in tc_cited)
    if stale:
        shown = ", ".join(stale[:5])
        out.append(
            "{} {} entries are now cited by a TC — prune them (burn-down "
            "progress, never a defect){}: {}".format(
                len(stale), IF_TC_ALLOW, " — first 5" if len(stale) > 5 else "", shown
            )
        )
    return out


def if_tc_allow_parse_findings(root):
    """PARSE HONESTY for `docs/if-tc-coverage-allow`, the
    `kernel_allow_parse_findings` idiom (WI-519): a declaring line the grammar
    cannot read is an explicit finding naming it, not a silent drop — the
    other half of "declares nothing" is that it also grants no exemption, and
    a malformed line that still reads like a live entry to a human is the
    state most worth reporting. Reported at the FIRST unparsed line with a
    count, not all of them, for the same reason `provenance_allow_parse_findings`
    does: the fix is the same edit for every one.

    Shares `if_tc_coverage_findings`' `[checks] interfaces_check` opt-out —
    deliberately NOT its ≤1-module arch-map vacuity, unlike that function and
    `if_tc_allow_hygiene_findings`: a malformed line is a fact about the FILE,
    not about whether the tree is currently large enough for the coverage
    rule to have anything to say, the same reasoning
    `kernel_allow_parse_findings` gives for riding only `components_check`
    and not the top-view bound."""
    if not read_interfaces_check_enabled(root):
        return []
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return []
    _entries, _seed, unparsed = _parse_if_tc_allow_full(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    if not unparsed:
        return []
    lineno, line = unparsed[0]
    return [
        "{}:{}: this line DECLARES a seam-TC exception and the grammar cannot "
        "read it ({} such line(s)) — `{}`. An entry's first token is an "
        "IF-### id, optionally followed by ` — <reason>`; a token that does "
        "not parse as IF-### suppresses nothing".format(
            IF_TC_ALLOW, lineno, len(unparsed), line[:80]
        )
    ]
